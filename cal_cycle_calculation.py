# -*- coding: utf-8 -*-
"""
Calculate linear calibration based on the cal cycles
"""

# %% EDIT THESE
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates
from calculate_linear_cal_fun import calc_cal
from load_flight_functions import read_COMA

case = '2022-08-06'

if case == '2021-08-06': # FCF
    filename_COMA = '../Data/2021-08-06/n2o-co_2021-08-06_f0002.txt'
elif case == '2021-08-10': # Test Flight 1
    filename_COMA = '../Data/2021-08-10/n2o-co_2021-08-10_f0003.txt'
elif case == '2021-08-16': # Test Flight 2
    filename_COMA = '../Data/2021-08-16/n2o-co_2021-08-16_f0002.txt'
elif case == '2021-08-17': # Test Flight 3
    filename_COMA = '../Data/2021-08-17/n2o-co_2021-08-17_f0002.txt'
"""
elif case == 4: # lab breathing air
    filename_COMA = '../Data/2021-08-06/n2o-co_2021-08-06_f0000.txt' # chop 3am part
elif case == 5:
    filename_COMA = '../Data/2021-08-10/n2o-co_2021-08-10_f0000.txt'
elif case == 6:
    filename_COMA = '../Data/2021-08-16/n2o-co_2021-08-16_f0000.txt'
elif case == 7:
    filename_COMA = '../Data/2021-08-17/n2o-co_2021-08-17_f0000.txt'
"""
if case == '2022-04-22': # cal gases
    filename_COMA = '../Data/2022-04-22/n2o-co_2022-04-22_f0000.txt'
elif case == '2022-05-20': # EEL Day 2
    filename_COMA = '../Data/2022-05-20/n2o-co_2022-05-20_f0000_cut_timechange.txt'
elif case == '2022-08-02': # RF03 - first flight in Osan
    filename_COMA = '../Data/2022-08-02/n2o-co_2022-08-02_f0000.txt'
elif case == '2022-08-04': # RF04
    filename_COMA = 1
elif case == '2022-08-06': # RF05
    filename_COMA = ['../Data/2022-08-05/n2o-co_2022-08-05_f0000_no_10s_cal.txt',
                     '../Data/2022-08-06/n2o-co_2022-08-06_f0000_no_10s_cal.txt',
                     '../Data/2022-08-06/n2o-co_2022-08-06_f0001.txt']

# %% data
# read COMA data
#LGR = pd.read_csv(filename_COMA,sep=',',header=1)
#LGR_time = LGR["                     Time"]
#LGR_time = [datetime.strptime(tstamp,"  %m/%d/%Y %H:%M:%S.%f") for tstamp in LGR_time]
#LGR_time = pd.DataFrame(LGR_time)
#LGR_time=LGR_time[0]
LGR = read_COMA(filename_COMA)
LGR_time = LGR['time']

# index MIU valves
#ix_8 = np.ravel(np.where( (LGR["      MIU_VALVE"]==8) & (LGR["      GasP_torr"]>52.45) & (LGR["      GasP_torr"]<52.65)) ) # Inlet
ix_8 = np.ravel(np.where(LGR["      MIU_VALVE"]==8)) # inlet
ix_7 = np.ravel(np.where(LGR["      MIU_VALVE"]==7)) # inlet (lab)
ix_3 = np.ravel(np.where(LGR["      MIU_VALVE"]==3)) # high cal
ix_2 = np.ravel(np.where(LGR["      MIU_VALVE"]==2)) # low cal
ix_1 = np.ravel(np.where(LGR["      MIU_VALVE"]==1)) # flush

# %% plot calibration data
plt.rc('axes', labelsize=6) # xaxis and yaxis labels
plt.rc('xtick', labelsize=6) # xtick labels
plt.rc('ytick', labelsize=6) # ytick labels

CO_raw = LGR["      [CO]d_ppm"]
N2O_raw = LGR["     [N2O]d_ppm"]
ix_low = ix_2
ix_high = ix_3
CO_cal, N2O_cal = calc_cal(LGR_time,CO_raw,N2O_raw,ix_low,ix_high)

# each cycle only takes a fixed amount of time
# therefore robust method is to check for large jumps in time (here > 5s) between occurences

"""
CO_slope = [1.07804824, 1.0712675 , 1.06404031, 1.05718497, 1.06851158,
       1.08508687, 1.07853471, 1.08321566, 1.0779714 , 1.07885479,
       1.07784337, 1.08879334, 1.07627126]
CO_intercept = [-3.25823985, -2.81917073, -3.42491811, -1.73777896, -3.77446838,
       -4.98576847, -4.31965464, -4.00183064, -3.63125074, -3.90676217,
       -3.95032122, -4.32512746, -3.40961519]
"""

cmap = plt.get_cmap("tab20")

#ax2[0].set_xlabel('Seconds')
#ax2[0].set_title('Low cal')
#ax2[1].set_xlabel('Seconds')
#ax2[1].set_title('High cal')
#ax[3].legend(np.linspace(1,13,13,dtype='int'),fontsize=5)

#fig.savefig('fig1.png',dpi=300)

# %% plot calibration results
fig, ax = plt.subplots(1, 4, figsize=(7,2),dpi=200)

x=list(range(len(CO_cal)))

ax[0].errorbar(x, y=CO_cal['low_mean'], yerr=2 * CO_cal['low_std'],ls='none',fmt='kx',markersize=3)

ax[0].set_xlabel('Cycle #')
ax[0].set_ylabel('CO, ppb')
#ax[0].set_ylim([46,52])

ax[1].errorbar(x=x, y=CO_cal['high_mean'], yerr=2 * CO_cal['high_std'],ls='none',fmt='kx',markersize=3)
ax[1].set_xlabel('Cycle #')
ax[1].set_ylabel('CO, ppb')
#ax[1].set_ylim([46,52])

ax[2].errorbar(x=x, y=N2O_cal['low_mean'], yerr=2 * N2O_cal['low_std'],ls='none',fmt='kx',markersize=3)
ax[2].set_xlabel('Cycle #')
ax[2].set_ylabel('N2O, ppb')
#ax[2].set_ylim([46,52])

ax[3].errorbar(x=x, y=N2O_cal['high_mean'], yerr=2 * N2O_cal['high_std'],ls='none',fmt='kx',markersize=3)
ax[3].set_xlabel('Cycle #')
ax[3].set_ylabel('N2O, ppb')
#ax[3].set_ylim([46,52])

ax[0].grid()
ax[1].grid()
ax[2].grid()
ax[3].grid()

plt.tight_layout()
#plt.savefig('fig1.png',dpi=300)

# %% output results
print("CO:")
for ii in range(len(CO_cal)):
    print(pd.to_datetime(CO_cal['time'][ii]).strftime("%m/%d/%Y %H:%M:%S") + 
          ' ' + "{:.3f}".format(CO_cal.slope[ii]) + 
          ' ' + "{:.3f}".format(CO_cal.intercept[ii]))

print()
print("N2O:")
for ii in range(len(CO_cal)):
    print(pd.to_datetime(CO_cal['time'][ii]).strftime("%m/%d/%Y %H:%M:%S") + 
          ' ' + "{:.3f}".format(N2O_cal.slope[ii]) + 
          ' ' + "{:.3f}".format(N2O_cal.intercept[ii]))
    
# %% test curve fit
# Exponential fit to determine flush rate and steady state concentration
# (skip first several points where concentration seems to overshoot)
# probably difficult in general; need to look at cases one by one
# https://stackoverflow.com/questions/3938042/fitting-exponential-decay-with-no-initial-guessing

"""
from scipy.optimize import curve_fit
def func(x, a, b, c):
    return a*np.exp(-b*x) + c

x = np.linspace(3,60,58)
y = 200-data['CO_dry'].values[3:] # make curve descending

popt, pcov = curve_fit(func, x, y)

plt.plot(200-data['CO_dry'].values,'.')
plt.plot(x,func(x,popt[0],popt[1],popt[2]),'.')
"""