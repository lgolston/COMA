# -*- coding: utf-8 -*-
"""
calculate and plot Allan deviation
uses allantools package
"""

# %% EDIT THESE
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.dates as mdates
import allantools
import matplotlib.ticker

case = 8

if case == 0: # FCF
    filename_COMA = '../Data/2021-08-06/n2o-co_2021-08-06_f0002.txt'
elif case == 1: # Test Flight 1
    filename_COMA = '../Data/2021-08-10/n2o-co_2021-08-10_f0003.txt'
elif case == 2: # Test Flight 2
    filename_COMA = '../Data/2021-08-16/n2o-co_2021-08-16_f0002.txt'
elif case == 3: # Test Flight 3
    filename_COMA = '../Data/2021-08-17/n2o-co_2021-08-17_f0002.txt'
elif case == 4: # lab breathing air
    filename_COMA = '../Data/2021-08-06/n2o-co_2021-08-06_f0000.txt' # chop 3am part
elif case == 5:
    filename_COMA = '../Data/2021-08-10/n2o-co_2021-08-10_f0000.txt'
elif case == 6:
    filename_COMA = '../Data/2021-08-16/n2o-co_2021-08-16_f0000.txt'
elif case == 7:
    filename_COMA = '../Data/2021-08-17/n2o-co_2021-08-17_f0000.txt'
elif case == 8:
    filename_COMA = '../Data/2022-04-12/n2o-co_2022-04-12_f0000.txt'
    y_start = datetime(2022,4,12)
    y_end = datetime(2022,4,12,17,0)
    # (note timestamp in first five minutes must have been manually set)
else:
    print('not a valid case')
    
# %% data
# read COMA data
LGR = pd.read_csv(filename_COMA,sep=',',header=1)

LGR_time = LGR["                     Time"]
LGR_time = [datetime.strptime(tstamp,"  %m/%d/%Y %H:%M:%S.%f") for tstamp in LGR_time]
LGR_time = pd.DataFrame(LGR_time)
LGR_time=LGR_time[0]

# index MIU valves
ix_8 = np.ravel(np.where(LGR["      MIU_VALVE"]==8)) # inlet
ix_7 = np.ravel(np.where(LGR["      MIU_VALVE"]==7)) # inlet (lab)
ix_3 = np.ravel(np.where(LGR["      MIU_VALVE"]==3)) # high cal
ix_2 = np.ravel(np.where(LGR["      MIU_VALVE"]==2)) # low cal
ix_1 = np.ravel(np.where(LGR["      MIU_VALVE"]==1)) # flush


# %% plot time series data
plt.rc('axes', labelsize=6) # xaxis and yaxis labels
plt.rc('xtick', labelsize=6) # xtick labels
plt.rc('ytick', labelsize=6) # ytick labels

# each cycle only takes a fixed amount of time
# therefore robust method is to check for large jumps in time (here > 5s) between occurences

fig, ax = plt.subplots(5, 1, figsize=(6,3),dpi=200, sharex=True)

# apply calibration
CO_cal = LGR["      [CO]d_ppm"]*1000
CO_cal = CO_cal*1.08 - 3
N2O_cal = LGR["     [N2O]d_ppm"]*1000
N2O_cal = N2O_cal*1.099 + 6.333

# 1. CO
ax[0].plot(LGR_time,CO_cal,'k.',markersize=2)
ax[0].set_ylabel('CO (dry), ppbv')
ax[0].set_ylim(0,200)

# 2. N2O
#ax[0].plot(LGR_time,LGR["     [N2O]d_ppm"]*1000,'.',markersize=2)
#ax[1].set_ylabel('$\mathregular{N_2O (dry), ppbv}$')
#ax[0].set_ylim(200,350)

# 3. laser temperature
ax[1].plot(LGR_time,LGR["           AIN6"],'.',markersize=2) # laser temp
#ax[2].set_ylabel('Laser T, C')

# 4. supercool temperature
ax[2].plot(LGR_time,LGR["           AIN5"],'.',markersize=2)
#ax[3].set_ylabel('Supercool T, C')

# 5. laser control voltage
ax[3].plot(LGR_time,LGR["         LTC0_v"],'.',markersize=2)
#ax[4].set_ylabel('LTC0_v')

# 6. Peak0
ax[4].plot(LGR_time,LGR["          Peak0"],'.',markersize=2)
#ax[5].set_ylabel('Peak0')
ax[4].set_ylim(790,820)

# 7. line centers
#ax[6].plot(LGR_time,LGR["  12COa_0000_CT"],'.',markersize=2)
#ax[6].set_ylim(-11,-9.5)
##ax[6].set_ylabel('12COa_0000_CT')

ax[4].xaxis.set_major_formatter(mdates.DateFormatter('%D:%H:%M'))
plt.tight_layout()

#fig.savefig('fig1.png',dpi=300)


# %% Allan deviation plot
# https://allantools.readthedocs.io/en/latest/
fig2, ax = plt.subplots(2, 1, figsize=(6,6),dpi=120)

to_plot = 'CO'

# case 3 (Test Flight 3)
# filter from 18:00 to 19:20 UTC
x = LGR_time[ix_8] # FILTER
x = LGR_time
if to_plot == 'CO':
    y = CO_cal[ix_8]
else:
    y = N2O_cal[ix_8]
#y_filter = y[(x>datetime(2021,8,17,18)) & (x<datetime(2021,8,17,19,20))] # before ER-2 intercomparison
#y_filter = y[(x>datetime(2021,8,17,19,40)) & (x<datetime(2021,8,17,20,35))] # ER-2 intercomparison

#x = LGR_time
#if to_plot == 'CO':
#    y = CO_cal
#else:
#    y = N2O_cal

tau_in = [1,2,3,4,5,6,7,8,9,10,15,20,25,30,35,40,45,50,55,60,2*60,3*60,4*60,5*60,6*60,7*60,8*60,9*60,10*60,30*60,60*60,120*60,180*60,240*60]

# case 7 (lab)
y_filter =  y[(x>datetime(2021,8,17))]

# case 8 (lab)
#y_filter =  y[(x>datetime(2022,4,12,17,0))]

# time series plot
ax[0].plot(y_filter,'b.',markersize=0.1)
ax[0].set_xlabel('Time, hours',fontsize=8)
ax[0].grid('on')
li = [x*3600 for x in [1,2,3,4,5,6,7,8]]
ax[0].set_xticks(li)
ax[0].tick_params(axis='both', which='major', labelsize=8)
ax[0].set_xticklabels(['1','2','3','4','5','6','7','8'])

# Allan plot
(tau_out, ad, aderr, adn) = allantools.oadev(np.asarray(y_filter),rate=1.0,taus=tau_in)
plt.loglog(tau_out, ad)
ax[1].set_xscale("log", base=60)
ax[1].set_yscale("log", base=10)
#plt.loglog([1,1000],[1E-1,2*1E-4],':k') # add slope -1/2 line (check math)
ax[1].set_xlabel('Averaging time, s',fontsize=8)
ax[1].tick_params(axis='both', which='major', labelsize=8)
ax[1].grid('on',which='major')


if to_plot == 'CO':
    ax[0].set_ylabel('CO (dry), ppb',fontsize=8)
    ax[1].set_ylabel('CO (dry), ppb',fontsize=8)
else:
    ax[0].set_ylabel('N2O (dry), ppb',fontsize=8)
    ax[1].set_ylabel('N2O (dry), ppb',fontsize=8)

print('1 Hz deviaton: ' + str(ad[0]))
fig2.tight_layout()

#fig2.savefig('fig2.png',dpi=300)