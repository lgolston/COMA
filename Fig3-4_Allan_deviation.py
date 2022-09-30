# -*- coding: utf-8 -*-
"""
calculate and plot Allan deviation, using allantools package
Scuba tank day
+
EEL Day 2
"""

# %% load libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import allantools

plt.rcParams['axes.labelsize'] = 8
plt.rcParams['legend.fontsize'] = 8
plt.rcParams['xtick.labelsize'] = 7
plt.rcParams['ytick.labelsize'] = 7
plt.rcParams.update({'mathtext.default': 'regular' } ) # not italics

to_plot = 'CO'

# %% main loop    
for case in [1,2]:
    # select day
    if case == 1:
        filename_COMA = '../Data/2022-04-12/n2o-co_2022-04-12_f0000.txt' # scuba air run
    elif case == 2:
        filename_COMA = '../Data/2022-05-20/n2o-co_2022-05-20_f0000_cut_timechange.txt' # EEL Day 2
    else:
        print('Case unknown')
    
    # read COMA data
    LGR = pd.read_csv(filename_COMA,sep=',',header=1,skipinitialspace=True)
    LGR_time = LGR["Time"]
    LGR_time = [datetime.strptime(tstamp,"%m/%d/%Y %H:%M:%S.%f") for tstamp in LGR_time]
    LGR_time = pd.DataFrame(LGR_time)
    LGR_time=LGR_time[0]
    
    # index MIU valves
    if case == 1:
        ix = np.ravel(np.where(LGR["MIU_VALVE"]>-10)) # select all; MIU was not used

    if case == 2:
        ix = np.ravel(np.where(LGR["MIU_VALVE"].rolling(window=15).min()==7))
        
        # filter to peak position of 807 +/- 1
        # and not super volatile
        #ix = np.ravel(np.where((LGR["Peak0"]>800) & # was 807
        #                       (LGR["Peak0"]<820) & # was 812
        #                       (LGR["Peak0"].rolling(10,center=True).std() < 2) &
        #                       (LGR["MIU_VALVE"].rolling(window=15).min()==7)))
    
    # apply calibration    
    if to_plot == 'CO':
        CO_cal = LGR["[CO]d_ppm"]*1000
        CO_cal = CO_cal*1.08 - 3
        y = CO_cal[ix].values
    else:
        N2O_cal = LGR["[N2O]d_ppm"]*1000
        N2O_cal = N2O_cal*1.099 + 6.333
        y = N2O_cal[ix].values
    
    # examine
    #plt.plot(LGR_time,CO_cal,'.')
    #plt.plot(LGR_time,LGR["Peak0"],'.')
    #plt.plot(LGR_time,LGR["GasP_torr"],'.')

    
    # %% drift plot
    # handle figure axes
    if case == 1:
        fig, ax = plt.subplot_mosaic([['A', 'C'],
                                      ['B', 'C']],
                              figsize=(6.5, 3))
        ax_cur = ax["A"]
    else:
        ax_cur = ax["B"]

    # select data
    if case == 1:
        y_filter = pd.Series(y[30*60 : 8*60*60])
    elif case == 2:
        y_filter = pd.Series(y[30*60-502 : 8*60*60-502])
    
    # calculate rolling mean
    y_mean = y_filter.rolling(window=180,center=True).mean()
    
    # plot
    ax_cur.plot(y_filter.values,'b.',markersize=0.1)
    #ax_cur.plot(y_mean,'b-')
    #ax_cur.plot(y_filter.expanding().quantile(0.01),'k:')
    #ax_cur.plot(y_filter.expanding().quantile(0.99),'k:')
    ax_cur.grid('on')
    li = [x*3600 for x in [0,1,2,3,4,5,6,7,8]]
    ax_cur.set_xticks(li)
    ax_cur.tick_params(axis='both', which='major', labelsize=8)
    ax_cur.set_xticklabels(['0','1','2','3','4','5','6','7','8'])
    
    # %% Allan deviation plot
    # https://allantools.readthedocs.io/en/latest/   
    tau_in = [1,2,3,4,5,6,7,8,9,10,15,20,25,30,35,40,45,50,55,60,2*60,3*60,4*60,5*60,6*60,7*60,8*60,9*60,10*60,30*60,60*60,120*60,180*60,240*60]
    
    # Allan plot
    plt.sca(ax["C"]) # set current axis
    (tau_out, ad, aderr, adn) = allantools.oadev(np.asarray(y_filter),rate=1.0,taus=tau_in)
    plt.loglog(tau_out, ad)
            
    print(str(tau_out[0]) + ' s deviaton: ' + str(ad[0]))
    print(str(tau_out[19]) + ' s deviaton: ' + str(ad[19]))

# %% plot formatting
ax["B"].set_xlabel('Time, hours',fontsize=8)

ax["A"].set_xticklabels([])

ax["C"].tick_params(axis='both', which='major', labelsize=8)
ax["C"].grid('on',which='major')
ax["C"].set_xlabel('Averaging time, s',fontsize=8)
plt.legend(['Lab','EEL'])

if to_plot == 'CO':
    ax["A"].set_ylabel('CO, ppb')
    ax["B"].set_ylabel('CO, ppb')
    ax["C"].set_ylabel('CO, ppb')
else:
    ax["A"].set_ylabel(r'$N_2O, ppb$')
    ax["B"].set_ylabel(r'$N_2O, ppb$')
    ax["C"].set_ylabel(r'$N_2O, ppb$')      

"""
#ax.set_xscale("log", base=60)
#ax2.set_xscale("log", base=10)
#ax2.set_yscale("log", base=10)
#plt.loglog([1,1000],[1E-1,2*1E-4],':k') # add slope -1/2 line (check math)
"""

ax["A"].set_position([0.10, 0.59, 0.40, 0.38]) # left, bottom, width, height
ax["B"].set_position([0.10, 0.16, 0.40, 0.38])
ax["C"].set_position([0.60, 0.25, 0.39, 0.60])

#fig.savefig('fig2.png',dpi=300)
