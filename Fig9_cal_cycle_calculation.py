# -*- coding: utf-8 -*-
"""
Calculate linear calibration based on the cal cycles
Show results across multiple days, colored before flight; in-flight; post-flight (or by altitude, gas temperature, etc. to check for dependencies)

Handles tank values from original NOAA tanks; and newer Matheson gas values

TODO
1. add all files
2. check calculation of rest of COMA outputs (like cell pressure)
3. flag [by ID (YYYY-MM-DD HH:MM:SS)]. use those to exclude incomplete cycles
4. calculate overall statistics
5. divide data into NOAA gas and Matheson gas
6. Add MMS pressure
7. Add back linear regression calculation
"""

# %% load libraries and data
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.dates as mdates
from calculate_linear_cal_fun import calc_cal
from load_data_functions import read_COMA
import matplotlib.cm as cm

filenames_2021 = ['../Data/2021-08-06/n2o-co_2021-08-06_f0002.txt', # FCF
                  '../Data/2021-08-10/n2o-co_2021-08-10_f0003.txt', # Test Flight 1
                  '../Data/2021-08-16/n2o-co_2021-08-16_f0002.txt', # Test Flight 2
                  '../Data/2021-08-17/n2o-co_2021-08-17_f0002.txt'] # Test Flight 3

#'../Data/2022-04-22/n2o-co_2022-04-22_f0000.txt', # lab run cylinders
#'../Data/2022-05-20/n2o-co_2022-05-20_f0000_cut_timechange.txt', # EEL Day 2

filenames_2022a = ['../Data/2022-07-18/n2o-co_2022-07-18_f0002.txt',
                   '../Data/2022-07-18/n2o-co_2022-07-18_f0003.txt',
                   '../Data/2022-07-21/n2o-co_2022-07-21_f0000.txt',
                   '../Data/2022-07-21/n2o-co_2022-07-21_f0001.txt',
                   '../Data/2022-07-21/n2o-co_2022-07-21_f0002.txt',
                   '../Data/2022-07-24/n2o-co_2022-07-24_f0000.txt',
                   '../Data/2022-07-25/n2o-co_2022-07-25_f0000.txt',
                   '../Data/2022-07-27/n2o-co_2022-07-27_f0000.txt',
                   '../Data/2022-08-02/n2o-co_2022-08-02_f0000.txt',  # RF03 - first flight in Osan
                   '../Data/2022-08-05/n2o-co_2022-08-05_f0000_no_10s_cal.txt',
                   '../Data/2022-08-04/n2o-co_2022-08-04_f0000.txt', # RF04
                   '../Data/2022-08-06/n2o-co_2022-08-06_f0000_no_10s_cal.txt', # RF05
                   '../Data/2022-08-06/n2o-co_2022-08-06_f0001.txt']

filenames_2022b = ['../Data/2022-08-11/n2o-co_2022-08-11_f0001.txt',
                  '../Data/2022-08-12/n2o-co_2022-08-12_f0000.txt', # RF06
                  '../Data/2022-08-15/n2o-co_2022-08-15_f0000.txt',
                  '../Data/2022-08-15/n2o-co_2022-08-15_f0001.txt',
                  '../Data/2022-08-15/n2o-co_2022-08-15_f0002.txt',
                  '../Data/2022-08-15/n2o-co_2022-08-15_f0003.txt',
                  '../Data/2022-08-16/n2o-co_2022-08-16_f0000.txt', # RF09
                  '../Data/2022-08-16/n2o-co_2022-08-16_f0001.txt']

# %% define cal gas cylinders
cylinder='NOAA'
# handle different gas tanks
if cylinder == 'NOAA':
    #NOAA low (CC745344)
    #NOAA high (CC746190)
    #https://gml.noaa.gov/ccl/refgas.html
    low_tank_CO = 51.30 # 51.30 +/- 0.66
    high_tank_CO = 163.11 # 163.11 +/- 0.92
    low_tank_N2O = 265.90 # 265.90 +/- 0.04
    high_tank_N2O = 348.05 # 348.05 +/- 0.04
elif cylinder == 'Matheson':
    #Matheson low: ~200 ppb CO and N2O
    #Matheson high: ~1000 ppb CO and N2O
    low_tank_CO = 200
    high_tank_CO = 1000
    low_tank_N2O = 200
    high_tank_N2O = 1000
else:
    print('Cylinder name not recognized.')
    
# %% load COMA data
filenames_COMA = filenames_2022a
COMA = []

# load COMA files      
for ii in range(len(filenames_COMA)):
    fname = filenames_COMA[ii]
    print(fname)
    
    if len(COMA) == 0:
        COMA, inlet_ix = read_COMA([fname])
    else:
        COMA2, inlet_ix = read_COMA([fname])             
        COMA = pd.concat([COMA,COMA2],ignore_index=True)

# calc
ix_low = np.ravel(np.where(COMA["MIU_VALVE"]==2)) # low cal
ix_high = np.ravel(np.where(COMA["MIU_VALVE"]==3)) # high cal

low_cal = calc_cal(COMA,ix_low)
high_cal = calc_cal(COMA,ix_high)

# %% handle filtering data
low_cal['valid']=True

# 2022-07-21_16:27:14
# 2022-07-21_17:12:15
# 2022-07-21_17:57:14
# 2022-08-02_04:41:13
# 2022-08-02_05:26:13
# 2022-08-02_06:11:13

# plus more...
# also need to handle high_cal

# %% load MMS data
#MMS = read_MMS(filename_MMS)

# %% plot time series
fig2, ax2 = plt.subplots(1, 1, figsize=(8,5))

ax2.plot(COMA['[CO]d_ppm'][ix_low].values*1000,'.',markersize=1)
ax2.set_ylim([40,65])
ax2_twin = ax2.twinx()
#ax2_twin.plot(COMA['GasP_torr'][ix_low].values,'k.')

ax2.axhline(51.30,linestyle = 'dashed')
ax2.set_xlabel('Seconds')
ax2.set_ylabel('CO, ppbv')

for index, row in low_cal.iterrows():
    ax2.plot([row['start_ct'],row['end_ct']],[row['CO_val'],row['CO_val']],'b--')

# %% plot calibration results
cmap = plt.get_cmap("tab20")

plt.rc('axes', labelsize=8) # xaxis and yaxis labels
plt.rc('xtick', labelsize=8) # xtick labels
plt.rc('ytick', labelsize=8) # ytick labels

fig, ax = plt.subplots(1, 4, figsize=(10,3))

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
print("CO:")
for ii in range(len(low_cal)):
    print(str(ii) +
          '  ' + pd.to_datetime(low_cal['time'][ii]).strftime("%Y-%m-%d_%H:%M:%S") + 
          '  ' + "{:.3f}".format(low_cal['CO_val'][ii]) + 
          '  ' + "{:.3f}".format(low_cal['N2O_val'][ii]))

#print()
#print("N2O:")
#for ii in range(len(CO_cal)):
#    print(pd.to_datetime(CO_cal['time'][ii]).strftime("%m/%d/%Y %H:%M:%S") + 
#          ' ' + "{:.3f}".format(N2O_cal.slope[ii]) + 
#          ' ' + "{:.3f}".format(N2O_cal.intercept[ii]) + 
#          '  ' + "{:.3f}".format(N2O_cal.low_mean[ii]) + 
#          '  ' + "{:.3f}".format(N2O_cal.high_mean[ii]))

# print averages

# %% plot relationships
fig3, ax3 = plt.subplots(1, 1, figsize=(7,4))
#plt.plot(low_cal['GasP_torr'],low_cal['CO_val'],'.')
#plt.plot(low_cal['AIN5'],low_cal['CO_val'],'.')
#plt.plot(low_cal['AIN6'],low_cal['CO_val'],'.')
#plt.plot(low_cal['AmbT_C'],low_cal['CO_val'],'.')
#plt.plot(low_cal['Peak0'],low_cal['CO_val'],'.')
#ax3.plot(low_cal['H2O'],low_cal['CO_val'],'.')
ax3.plot(low_cal['SpectraID'],low_cal['CO_val'],'.') #proxy for time COMA on
