# -*- coding: utf-8 -*-
"""
Calculate linear calibration based on the cal cycles
Show results across multiple days, colored before flight; in-flight; post-flight (or by altitude, gas temperature, etc. to check for dependencies)

Handles tank values from original NOAA tanks; and newer Matheson gas values

TODO
1. add all files
2. calculate rest of COMA outputs (like cell pressure)
3. additional plot with raw data
4. flag [by ID (YYYY-MM-DD HH:MM:SS)]. use those to exclude incomplete cycles
5. calculate overall statistics
6. divide data into NOAA gas and Matheson gas
7. Add MMS pressure
8. Add back linear regression calculation
"""

# %% load libraries and data
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib
import matplotlib.dates as mdates
from calculate_linear_cal_fun import calc_cal
from load_data_functions import read_COMA, read_MMS_ict
from functools import reduce
import matplotlib.cm as cm

filenames_2021 = ['../Data/2021-08-06/n2o-co_2021-08-06_f0002.txt', # FCF
                  '../Data/2021-08-10/n2o-co_2021-08-10_f0003.txt', # Test Flight 1
                  '../Data/2021-08-16/n2o-co_2021-08-16_f0002.txt', # Test Flight 2
                  '../Data/2021-08-17/n2o-co_2021-08-17_f0002.txt'] # Test Flight 3

filenames_2022 = ['../Data/2022-04-22/n2o-co_2022-04-22_f0000.txt',
                  '../Data/2022-05-20/n2o-co_2022-05-20_f0000_cut_timechange.txt', # EEL Day 2
                  '../Data/2022-08-02/n2o-co_2022-08-02_f0000.txt',  # RF03 - first flight in Osan
                  '../Data/2022-08-05/n2o-co_2022-08-05_f0000_no_10s_cal.txt',
                  '../Data/2022-08-06/n2o-co_2022-08-06_f0000_no_10s_cal.txt', # RF05
                  '../Data/2022-08-06/n2o-co_2022-08-06_f0001.txt',
                  '../Data/2022-08-11/n2o-co_2022-08-11_f0001.txt',
                  '../Data/2022-08-12/n2o-co_2022-08-12_f0000.txt', # RF06
                  '../Data/2022-08-15/n2o-co_2022-08-15_f0000.txt',
                  '../Data/2022-08-15/n2o-co_2022-08-15_f0001.txt',
                  '../Data/2022-08-15/n2o-co_2022-08-15_f0002.txt',
                  '../Data/2022-08-15/n2o-co_2022-08-15_f0003.txt',
                  '../Data/2022-08-16/n2o-co_2022-08-16_f0000.txt', # RF09
                  '../Data/2022-08-16/n2o-co_2022-08-16_f0001.txt']

# %% load COMA data
filenames_COMA = filenames_2022
COMA = []

# load COMA files      
for ii in range(len(filenames_COMA)):
    if len(COMA) == 0:
        COMA, inlet_ix = read_COMA([filenames_COMA[ii]])
    else:
        COMA2, inlet_ix = read_COMA([filenames_COMA[ii]])             
        COMA = pd.concat([COMA,COMA2],ignore_index=True)

# calc
ix_low = np.ravel(np.where(COMA["MIU_VALVE"]==2)) # low cal
ix_high = np.ravel(np.where(COMA["MIU_VALVE"]==3)) # high cal
    
low_cal = calc_cal(COMA,ix_low,'Matheson')
high_cal = calc_cal(COMA,ix_high,'Matheson')

# %% load MMS data
#MMS = read_MMS(filename_MMS)

# %% plot calibration results
cmap = plt.get_cmap("tab20")

plt.rc('axes', labelsize=6) # xaxis and yaxis labels
plt.rc('xtick', labelsize=6) # xtick labels
plt.rc('ytick', labelsize=6) # ytick labels

fig, ax = plt.subplots(1, 4, figsize=(7,2),dpi=200)

x_low=list(range(len(low_cal)))
x_high=list(range(len(high_cal)))

norm = matplotlib.colors.Normalize(vmin=0, vmax=30, clip=True)
mapper = cm.ScalarMappable(norm=norm, cmap=cm.viridis)

# low cal CO
for ii in range(len(low_cal)):
    c = mapper.to_rgba(low_cal['AmbT_C'][ii])
    ax[0].errorbar(x_low[ii], y=low_cal['CO_val'][ii], yerr=2 * low_cal['CO_std'][ii],ls='none',fmt='x',markersize=3,color=c)

ax[0].set_xlabel('Cycle #')
ax[0].set_ylabel('CO, ppb')

# high cal CO
ax[1].errorbar(x=x_high, y=high_cal['CO_val'], yerr=2 * high_cal['CO_std'],ls='none',fmt='kx',markersize=3)
ax[1].set_xlabel('Cycle #')
ax[1].set_ylabel('CO, ppb')

# low cal N2O
ax[2].errorbar(x=x_low, y=low_cal['N2O_val'], yerr=2 * low_cal['N2O_std'],ls='none',fmt='kx',markersize=3)
ax[2].set_xlabel('Cycle #')
ax[2].set_ylabel('N2O, ppb')

# high cal N2O
ax[3].errorbar(x=x_high, y=high_cal['N2O_val'], yerr=2 * high_cal['N2O_std'],ls='none',fmt='kx',markersize=3)
ax[3].set_xlabel('Cycle #')
ax[3].set_ylabel('N2O, ppb')

#ax[0].set_ylim([46,52])
#ax[1].set_ylim([46,52])
#ax[2].set_ylim([46,52])
#ax[3].set_ylim([46,52])

ax[0].grid()
ax[1].grid()
ax[2].grid()
ax[3].grid()

plt.tight_layout()
#plt.savefig('fig1.png',dpi=300)

# %% output results
"""
print("CO:")
for ii in range(len(CO_cal)):
    print(pd.to_datetime(CO_cal['time'][ii]).strftime("%m/%d/%Y %H:%M:%S") + 
          '  ' + "{:.3f}".format(CO_cal.slope[ii]) + 
          '  ' + "{:.3f}".format(CO_cal.intercept[ii]) + 
          '  ' + "{:.3f}".format(CO_cal.low_mean[ii]) + 
          '  ' + "{:.3f}".format(CO_cal.high_mean[ii]))
"""

#print()
#print("N2O:")
#for ii in range(len(CO_cal)):
#    print(pd.to_datetime(CO_cal['time'][ii]).strftime("%m/%d/%Y %H:%M:%S") + 
#          ' ' + "{:.3f}".format(N2O_cal.slope[ii]) + 
#          ' ' + "{:.3f}".format(N2O_cal.intercept[ii]) + 
#          '  ' + "{:.3f}".format(N2O_cal.low_mean[ii]) + 
#          '  ' + "{:.3f}".format(N2O_cal.high_mean[ii]))

# print averages
"""
print('Average values:')
print('CO low ratio ' + "{:.3f}".format(np.mean(CO_low_ratio)))
print('CO high ratio ' + "{:.3f}".format(np.mean(CO_high_ratio)))
print('CO equation ' + "{:.3f}".format(np.mean(CO_slope)) + 'x + ' 
                         + "{:.3f}".format(np.mean(CO_intercept)))

print('N2O low ratio ' + "{:.3f}".format(np.mean(N2O_low_ratio)))
print('N2O high ratio ' + "{:.3f}".format(np.mean(N2O_high_ratio)))
print('N2O equation ' + "{:.3f}".format(np.mean(N2O_slope)) + 'x + ' 
                      + "{:.3f}".format(np.mean(N2O_intercept)))
"""