# -*- coding: utf-8 -*-
"""
Calculate linear calibration based on the cal cycles
Show results across multiple days, colored before flight; in-flight; post-flight (or by altitude, gas temperature, etc. to check for dependencies)

Handles tank values from original NOAA tanks; and newer Matheson gas values

TODO
1. List NOAA files
2. List Matheson files
3. Add MMS pressure
4. Add laser power and CO line center
5. Add back linear regression calculation
6. Label or vertical lines for each flight
7. Add pre-ACCLIP NOAA files
"""

# %% load libraries and data
import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from calculate_linear_cal_fun import calc_cal
from load_data_functions import read_COMA
from load_data_functions import return_filenames
from load_data_functions import read_MMS_ict

# set font size
plt.rcParams['axes.labelsize'] = 8
plt.rcParams['legend.fontsize'] = 8
plt.rcParams['xtick.labelsize'] = 7
plt.rcParams['ytick.labelsize'] = 7
plt.rcParams.update({'mathtext.default': 'regular' } ) # not italics

# %% define cases
case = 'FCF_2021'

filenames = return_filenames(case)

if case == 'FCF_2021':
    1
elif case == 'TF1_2021':
    1
elif case == 'TF2_2021':
    1
elif case == 'TF3_2021':
    1
elif case == 'EEL_2022_Day1':
    1
elif case == 'EEL_2022_Day2':
    1
elif case == 'RF02':
    1
elif case == 'Transit1': # Ellington to Seattle
    1
elif case == 'Transit2': # Seattle to Anchorage
    1
elif case == 'Transit3': # Anchorage to Adak
    1
elif case == 'Transit4': # Adak to Misawa
    1
elif case == 'Transit5': # Misawa to Osan
    1
elif case == 'RF03':
    1
elif case == 'RF04':
    1
elif case == 'RF05':
    1
elif case == 'RF06':
    1
elif case == 'RF07':
    1
elif case == 'RF08':
    1
elif case == 'RF09':
    1
elif case == 'RF10':
    1
elif case == 'RF11':
    1
elif case == 'RF12':
    1
elif case == 'RF13':
    1
elif case == 'RF14':
    1
elif case == 'RF15':
    1
elif case == 'RF16':
    1
elif case == 'RF17':
    1
elif case == 'Transit6': # Osan to Misawa
    1
elif case == 'Transit7': # Misawa to Adak
    1
elif case == 'Transit8': # Adak to Seattle
    1
elif case == 'Transit9': # Seattle to Houston
    1

# %% define cal gas cylinders
cylinder = 'NOAA'

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
COMA = []

filenames_COMA = filenames['COMA_raw']

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

df_lowcal = pd.DataFrame({'time': COMA['time'][ix_low],
                          'CO_dry': COMA["[CO]d_ppm"][ix_low]*1000,
                          'N2O_dry': COMA["[N2O]d_ppm"][ix_low]*1000,
                          'H2O': COMA["[H2O]_ppm"][ix_low],
                          'GasP_torr': COMA['GasP_torr'][ix_low]})
df_lowcal['groups'] = (df_lowcal.index.to_series().diff()>5).cumsum()

df_highcal = pd.DataFrame({'time': COMA['time'][ix_high],
                           'CO_dry': COMA["[CO]d_ppm"][ix_high]*1000,
                           'N2O_dry': COMA["[N2O]d_ppm"][ix_high]*1000,
                           'H2O': COMA["[H2O]_ppm"][ix_high],
                           'GasP_torr': COMA['GasP_torr'][ix_high]})
df_highcal['groups'] = (df_highcal.index.to_series().diff()>5).cumsum()

# %% load MMS data
MMS = read_MMS_ict(filenames['MMS'])

# %% load laser power
# ...

# %% plot time series (slower changing variables)
fig1, ax1 = plt.subplots(3, 1, figsize=(6,5))
# 
# altitude and laser power
# peak position


# %% plot time series (cal cycles overlapped)
fig2, ax2 = plt.subplots(3, 2, figsize=(6,5))

for ct, data in df_lowcal.groupby('groups'):
    ax2[0,0].plot(data['CO_dry'].values,'.')
    ax2[1,0].plot(data['N2O_dry'].values,'.')
    ax2[2,0].plot(data['GasP_torr'].values,'.')

for ct, data in df_highcal.groupby('groups'):
    ax2[0,1].plot(data['CO_dry'].values,'.')
    ax2[1,1].plot(data['N2O_dry'].values,'.')
    ax2[2,1].plot(data['GasP_torr'].values,'.')
    
# NOAA gas bottle
if cylinder == 'NOAA':
    ax2[0,0].set_ylim(20,200)
    ax2[0,1].set_ylim(20,200)
else:
    # Matheson gas bottle
    ax2[0,0].set_ylim(170,220)
    ax2[0,1].set_ylim(800,1000)

ax2[0,0].set_ylabel('CO, ppb')
ax2[0,0].grid()
ax2[0,1].grid()

ax2[1,0].set_ylabel('N2O, ppb')
ax2[1,0].grid()
ax2[1,1].grid()

ax2[2,0].set_ylabel('Cell pressure, torr')
ax2[2,0].grid()
ax2[2,1].grid()

ax2[2,0].set_xlabel('Seconds')
ax2[2,1].set_xlabel('Seconds')
ax2[0,0].set_title('Low cal')
ax2[0,1].set_title('High cal')

ax2[0,1].legend(np.linspace(1,13,13,dtype='int'),ncol=2)

fig2.suptitle(case)
fig2.tight_layout()
#fig2.savefig('fig2.png',dpi=300)


# %% output stats
print("CO:")
low_cal['ID'] = [pd.to_datetime(tmp).strftime("%Y-%m-%d_%H:%M:%S") for tmp in low_cal['time']]
high_cal['ID'] = [pd.to_datetime(tmp).strftime("%Y-%m-%d_%H:%M:%S") for tmp in high_cal['time']]

dat = high_cal

for ii in range(len(dat)):
    print("{:2d}".format(ii) +                          #Cycle#
          '  ' + dat['ID'][ii] +                        #Unique identifier
          '  ' + "{:6.2f}".format(dat['CO_val'][ii]) +  #CO mean
          '  ' + "{:6.2f}".format(dat['CO_std'][ii]) +
          '  ' + "{:6.2f}".format(dat['N2O_val'][ii]))

#print()
#print("N2O:")
#for ii in range(len(CO_cal)):
#    print(pd.to_datetime(CO_cal['time'][ii]).strftime("%m/%d/%Y %H:%M:%S") + 
#          ' ' + "{:.3f}".format(N2O_cal.slope[ii]) + 
#          ' ' + "{:.3f}".format(N2O_cal.intercept[ii]) + 
#          '  ' + "{:.3f}".format(N2O_cal.low_mean[ii]) + 
#          '  ' + "{:.3f}".format(N2O_cal.high_mean[ii]))

# print averages

# %% holding
# label ticks with time identifier
#xlabels = [pd.to_datetime(t).strftime('%m.%d %H:%M') for t in low_cal['time']]
#plt.tight_layout()
#plt.savefig('fig1.png',dpi=300)
