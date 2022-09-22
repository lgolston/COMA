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
from datetime import datetime, timedelta
import matplotlib.dates as mdates
import allantools
import matplotlib.ticker
from calculate_linear_cal_fun import calc_cal

plt.rc('axes', labelsize=6) # xaxis and yaxis labels
plt.rc('xtick', labelsize=6) # xtick labels
plt.rc('ytick', labelsize=6) # ytick labels
    
for case in [1,2]:
    # select day
    if case == 1:
        filename_COMA = '../Data/2022-04-12/n2o-co_2022-04-12_f0000.txt' # scuba air run
    elif case == 2:
        filename_COMA = '../Data/2022-05-20/n2o-co_2022-05-20_f0000_cut_timechange.txt' # EEL Day 2
    else:
        filename_COMA = '../Data/2022-04-22/n2o-co_2022-04-22_f0000.txt'
    
    # read COMA data
    LGR = pd.read_csv(filename_COMA,sep=',',header=1)
    
    LGR_time = LGR["                     Time"]
    LGR_time = [datetime.strptime(tstamp,"  %m/%d/%Y %H:%M:%S.%f") for tstamp in LGR_time]
    LGR_time = pd.DataFrame(LGR_time)
    LGR_time=LGR_time[0]
    
    # index MIU valves
    if case == 1:
        ix_7 = np.ravel(np.where(LGR["      MIU_VALVE"]>-10)) # select all; MIU was not used
        ix = ix_7
    if case == 2:
        ix_8 = np.ravel(np.where(LGR["      MIU_VALVE"]==8)) # inlet
        #ix_7 = np.ravel(np.where(LGR["      MIU_VALVE"]==7)) # inlet (lab)
        ix_7 = np.ravel(np.where(LGR["      MIU_VALVE"].rolling(window=15).min()==7))
        ix_3 = np.ravel(np.where(LGR["      MIU_VALVE"]==3)) # high cal
        ix_2 = np.ravel(np.where(LGR["      MIU_VALVE"]==2)) # low cal
        ix_1 = np.ravel(np.where(LGR["      MIU_VALVE"]==1)) # flush
        
        # filter to peak position of 807 +/- 1
        # and not super volatile
        ix = np.ravel(np.where((LGR["          Peak0"]>800) &
                               (LGR["          Peak0"]<820) &
                               (LGR["          Peak0"].rolling(10,center=True).std() < 2) &
                               (LGR["      MIU_VALVE"].rolling(window=15).min()==7)))
        #ix = np.ravel(np.where((LGR["          Peak0"]>807) &
        #                       (LGR["          Peak0"]<812) &
        #                       (LGR["          Peak0"].rolling(10,center=True).std() < 2) &
        #                       (LGR["      MIU_VALVE"].rolling(window=15).min()==7)))
        
    # apply calibration
    CO_cal = LGR["      [CO]d_ppm"]*1000
    CO_cal = CO_cal*1.08 - 3
    N2O_cal = LGR["     [N2O]d_ppm"]*1000
    N2O_cal = N2O_cal*1.099 + 6.333
    
    # examine
    #plt.plot(LGR_time,CO_cal,'.')
    #plt.plot(LGR_time,LGR["          Peak0"],'.')
    #plt.plot(LGR_time,LGR["      GasP_torr"],'.')
    
    #if case == 2:
    #    CO_cal, N2O_cal = calc_cal(LGR_time,LGR["      [CO]d_ppm"],LGR["     [N2O]d_ppm"],ix_2,ix_3)
    
    # %% drift plot
    to_plot = 'CO'
    
    x = LGR_time[ix] # FILTER
    if to_plot == 'CO':
        y = CO_cal[ix]
    else:
        y = N2O_cal[ix]
    
    #y_filter =  y[(x>datetime(2022,4,12,16,34))]
    if case == 1:
        y_filter =  y[(x>datetime(2022,4,12,16,59))]
    else:
        y_filter =  y[(x>datetime(2022,5,20,8,45))]
      
    if case == 1:
        fig1, ax1 = plt.subplots(2, 1, figsize=(6,3),dpi=120)
    
    y_mean = y_filter.rolling(window=180,center=True).mean()
    
    ii = case-1
    ax1[ii].plot(y_filter,'b.',markersize=0.1)
    #ax1[ii].plot(y_mean,'b-')
    ax1[ii].plot(y_filter.expanding().quantile(0.01),'k:')
    ax1[ii].plot(y_filter.expanding().quantile(0.99),'k:')
    ax1[ii].grid('on')
    li = [x*3600 for x in [1,2,3,4,5,6,7,8]]
    ax1[ii].set_xticks(li)
    ax1[ii].tick_params(axis='both', which='major', labelsize=8)
    ax1[ii].set_xticklabels(['1','2','3','4','5','6','7','8'])
    
    if case == 2:
        ax1[0].set_ylabel('CO, ppb')
        ax1[1].set_ylabel('CO, ppb')
        ax1[1].set_xlabel('Time, hours',fontsize=8)
        fig1.tight_layout()
        
    # %% Allan deviation plot
    # https://allantools.readthedocs.io/en/latest/
    if case == 1:
        fig2, ax2 = plt.subplots(1, 1, figsize=(6,3),dpi=120)
    
    tau_in = [1,2,3,4,5,6,7,8,9,10,15,20,25,30,35,40,45,50,55,60,2*60,3*60,4*60,5*60,6*60,7*60,8*60,9*60,10*60,30*60,60*60,120*60,180*60,240*60]
    
    # Allan plot
    (tau_out, ad, aderr, adn) = allantools.oadev(np.asarray(y_filter),rate=1.0,taus=tau_in)
    plt.loglog(tau_out, ad)
    
    if case == 2:
        #ax.set_xscale("log", base=60)
        ax2.set_xscale("log", base=10)
        ax2.set_yscale("log", base=10)
        #plt.loglog([1,1000],[1E-1,2*1E-4],':k') # add slope -1/2 line (check math)
        ax2.set_xlabel('Averaging time, s',fontsize=8)
        ax2.tick_params(axis='both', which='major', labelsize=8)
        ax2.grid('on',which='major')
        plt.legend(['Lab','EEL'])
    
        if to_plot == 'CO':
            ax2.set_ylabel('CO (dry), ppb',fontsize=8)
            #ax[1].set_ylabel('CO (dry), ppb',fontsize=8)
        else:
            ax2.set_ylabel('N2O (dry), ppb',fontsize=8)
            #ax[1].set_ylabel('N2O (dry), ppb',fontsize=8)
    
        fig2.tight_layout()
        
    print(str(tau_out[0]) + ' s deviaton: ' + str(ad[0]))
    print(str(tau_out[19]) + ' s deviaton: ' + str(ad[19]))


#fig2.savefig('fig2.png',dpi=300)


# %% plot time series data (old)
"""
fig, ax = plt.subplots(2, 1, figsize=(6,3),dpi=200, sharex=True)

# 1. CO
ax[0].plot(LGR_time,CO_cal,'k.',markersize=2)
ax[0].set_ylabel('CO (dry), ppbv')
ax[0].set_ylim(0,200)

# 2. N2O
ax[1].plot(LGR_time,LGR["     [N2O]d_ppm"]*1000,'.',markersize=2)
ax[1].set_ylabel('$\mathregular{N_2O (dry), ppbv}$')
ax[1].set_ylim(200,350)

#fig.savefig('fig1.png',dpi=300)
"""