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
import matplotlib
import matplotlib.dates as mdates
from calculate_linear_cal_fun import calc_cal
from load_data_functions import read_COMA
from load_data_functions import return_filenames
import matplotlib.cm as cm

# set font size
plt.rcParams['axes.labelsize'] = 8
plt.rcParams['legend.fontsize'] = 8
plt.rcParams['xtick.labelsize'] = 7
plt.rcParams['ytick.labelsize'] = 7
plt.rcParams.update({'mathtext.default': 'regular' } ) # not italics

# %% define cases
case = 'RF03'

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

"""
# loop through multiple cases
# define file lists
filenames_2021 = ['FCF_2021','TF1_2021','TF2_2021','TF3_2021']

filenames_testing = ['../Data/2022-05-19/n2o-co_2022-05-19_f0000.txt',
                     '../Data/2022-05-20/n2o-co_2022-05-20_f0000_cut_timechange.txt'] # EEL Day 2
#'../Data/2022-04-22/n2o-co_2022-04-22_f0000.txt', # lab run cylinders

filenames_2022a = ['RF02','Transit1','Transit2','Transit3','Transit4','Transit5','RF03'] #...

filenames_2022b = ['']
"""

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

# %% load MMS data
# MMS = read_MMS(filename_MMS)

# %% load laser power
# ...

# %% handle filtering data
# [not complete]

# low cal
low_cal['valid'] = True
low_cal['ID'] = [pd.to_datetime(tmp).strftime("%Y-%m-%d_%H:%M:%S") for tmp in low_cal['time']]

low_cal.loc[low_cal['ID'].str.match("2022-07-21_16:27:14"),'valid']=False
low_cal.loc[low_cal['ID'].str.match("2022-07-21_17:12:15"),'valid']=False
low_cal.loc[low_cal['ID'].str.match("2022-07-21_17:57:14"),'valid']=False
low_cal.loc[low_cal['ID'].str.match("2022-08-02_04:41:13"),'valid']=False
low_cal.loc[low_cal['ID'].str.match("2022-08-02_05:26:13"),'valid']=False
low_cal.loc[low_cal['ID'].str.match("2022-08-02_06:11:13"),'valid']=False
low_cal.loc[low_cal['GasP_torr']<51,'valid'] = False

# high cal
high_cal['valid'] = True
high_cal['ID'] = [pd.to_datetime(tmp).strftime("%Y-%m-%d_%H:%M:%S") for tmp in high_cal['time']]

high_cal.loc[high_cal['ID'].str.match("2022-07-21_16:27:55"),'valid']=False
high_cal.loc[high_cal['ID'].str.match("2022-07-21_17:12:55"),'valid']=False
high_cal.loc[high_cal['ID'].str.match("2022-07-21_17:57:55"),'valid']=False
high_cal.loc[high_cal['ID'].str.match("2022-08-02_04:41:53"),'valid']=False
high_cal.loc[high_cal['ID'].str.match("2022-08-02_05:26:53"),'valid']=False
high_cal.loc[high_cal['ID'].str.match("2022-08-02_06:11:53"),'valid']=False
high_cal.loc[high_cal['GasP_torr']<51,'valid'] = False

# %% plot time series
fig2, ax2 = plt.subplots(1, 1, figsize=(8,5))

to_show = 'low_cal'

ax2.plot(COMA['[CO]d_ppm'][ix_high].values*1000,'.',markersize=1)
ax2_twin = ax2.twinx()
ax2_twin.plot(COMA['GasP_torr'][ix_high].values,'k.')

if cylinder == 'NOAA':
    ax2.set_ylim([140,180])

ax2.set_xlabel('Seconds')
ax2.set_ylabel('CO, ppbv')

# make horizontal lines for end values
for index, row in high_cal.iterrows():
    ax2.plot([row['start_ct'],row['end_ct']],[row['CO_val'],row['CO_val']],'b--')

# %% plot calibration results
cmap = plt.get_cmap("tab20")

fig, ax = plt.subplots(4, 1, figsize=(9,5),dpi=150)

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

# label ticks with time identifier
ax[3].set_xticks(range(0,len(low_cal)))
ax[3].tick_params(axis='x', labelrotation = 90)
xlabels = [pd.to_datetime(t).strftime('%m.%d %H:%M') for t in low_cal['time']]
ax[3].set_xticklabels(xlabels)

plt.tight_layout()
#plt.savefig('fig1.png',dpi=300)

# %% output results
print("CO:")
dat = high_cal

for ii in range(len(dat)):
    print("{:2d}".format(ii) +
          '  ' + dat['ID'][ii] + 
          '  ' + "{:6.2f}".format(dat['CO_val'][ii]) + 
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

# %% plot relationships
"""
ix_valid = low_cal['valid']

x = low_cal
y = low_cal['N2O_val']

fig3, ax3 = plt.subplots(3, 3, figsize=(8,5))
ax3[0,0].plot(x['GasP_torr'][ix_valid],y[ix_valid],'.')
ax3[0,1].plot(x['AIN5'][ix_valid],     y[ix_valid],'.')
ax3[0,2].plot(x['AIN6'][ix_valid],     y[ix_valid],'.')
ax3[1,0].plot(x['AmbT_C'][ix_valid],   y[ix_valid],'.')
ax3[1,1].plot(x['Peak0'][ix_valid],    y[ix_valid],'.')
ax3[1,2].plot(x['H2O'][ix_valid],      y[ix_valid],'.')
ax3[2,0].plot(x['SpectraID'][ix_valid],y[ix_valid],'.') # proxy for time COMA on

ax3[0,0].set_xlabel('GasP_torr')
ax3[0,1].set_xlabel('AIN5')
ax3[0,2].set_xlabel('AIN6')
ax3[1,0].set_xlabel('AmbT_C')
ax3[1,1].set_xlabel('Peak0')
ax3[1,2].set_xlabel('H2O')
ax3[2,0].set_xlabel('SpectraID')

fig3.tight_layout()
"""

# %% plot valid cycles (manuscript figure)
"""
fig4, ax4 = plt.subplots(4, 1, figsize=(6,5),sharex=True)

# low cal
ct = 0
for ii in range(len(low_cal)):
    if low_cal['valid'][ii]==True:
        ax4[0].plot(ct,low_cal['CO_val'][ii],'kx')
        ax4[1].plot(ct,low_cal['N2O_val'][ii]+7,'kx')
        ct += 1
ax4[0].axhline(low_tank_CO,linestyle = 'dashed')
ax4[1].axhline(low_tank_N2O,linestyle = 'dashed')

# high cal
ct = 0
for ii in range(len(high_cal)):
    if high_cal['valid'][ii]==True:
        ax4[2].plot(ct,high_cal['CO_val'][ii],'kx')
        ax4[3].plot(ct,high_cal['N2O_val'][ii]+7,'kx')
        ct += 1

ax4[2].axhline(high_tank_CO,linestyle = 'dashed')
ax4[3].axhline(high_tank_N2O,linestyle = 'dashed')

# label ticks with time identifier
ax4[3].set_xticks(range(0,ct))
xlabels = [t[5:-1] for t in low_cal[ix_valid]['ID'].values]
ax4[3].set_xticklabels(xlabels,rotation=90)

# format plot
ax4[0].set_ylabel('Low CO, ppb')
ax4[1].set_ylabel(r'Low $N_2O$, ppb')
ax4[2].set_ylabel('High CO, ppb')
ax4[3].set_ylabel(r'High $N_2O$, ppb')
ax4[3].set_xlabel('Cycle #')
fig4.tight_layout()
#fig4.savefig('fig4.png',dpi=300)
"""
