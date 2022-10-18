# -*- coding: utf-8 -*-
"""
Calculate linear calibration based on the cal cycles
Show results across multiple days, colored before flight; in-flight; post-flight (or by altitude, gas temperature, etc. to check for dependencies)

Handles tank values from original NOAA tanks; and newer Matheson gas values

"""

# %% load libraries and data
import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# set font size
plt.rcParams['axes.labelsize'] = 8
plt.rcParams['legend.fontsize'] = 8
plt.rcParams['xtick.labelsize'] = 7
plt.rcParams['ytick.labelsize'] = 7
plt.rcParams.update({'mathtext.default': 'regular' } ) # not italics

# %% define cases

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


# %% load spreadsheet



# %% remove for now: linear regression
    """
    # number of cycles
    n = sum(low_CO_mean>0)
    rng = range(0,n)
    
    # linear slope and intercept: CO and N2O
    CO_low_ratio = np.zeros(len(rng))
    CO_high_ratio = np.zeros(len(rng))
    CO_slope = np.zeros(len(rng))
    CO_intercept = np.zeros(len(rng))
    
    N2O_low_ratio = np.zeros(len(rng))
    N2O_high_ratio = np.zeros(len(rng))
    N2O_slope = np.zeros(len(rng))
    N2O_intercept = np.zeros(len(rng))
    
    starting_index = np.zeros(len(rng),dtype=int)
    
    # loop through and calculate slope/intercepts         
    for ii in rng:
        # CO
        x1=low_tank_CO # low tank value
        x2=high_tank_CO # high tank value
        y1=low_CO_mean[ii]
        y2=high_CO_mean[ii]
        m = (x2-x1)/(y2-y1) # original method that Emma showed
        b = x1-y1*m # same as x2-y2*m
        
        CO_low_ratio[ii] = x1/y1
        CO_high_ratio[ii] = x2/y2
        CO_slope[ii] = m
        CO_intercept[ii] = b

        x1=low_tank_N2O # low tank value
        x2=high_tank_N2O # high tank value
        y1=low_N2O_mean[ii]
        y2=high_N2O_mean[ii]
        m = (x2-x1)/(y2-y1)
        b = x1-y1*m # same as x2-y2*m
        
        N2O_low_ratio[ii] = x1/y1
        N2O_high_ratio[ii] = x2/y2
        N2O_slope[ii] = m
        N2O_intercept[ii] = b
        
        tmp = np.argmax(df_lowcal['groups']==ii)
        starting_index[ii] = df_lowcal.index[tmp]

    starting_index = np.append(starting_index,len(CO_raw))
    
    # apply calibration factors to data
    CO_calibrated = CO_raw*1000
    N2O_calibrated = N2O_raw*1000
    
    for ii in rng:
        tmp = CO_raw[starting_index[ii]:starting_index[ii+1]]*1000
        CO_calibrated[starting_index[ii]:starting_index[ii+1]] = tmp*CO_slope[ii]+CO_intercept[ii]
    
        tmp = N2O_raw[starting_index[ii]:starting_index[ii+1]]*1000
        N2O_calibrated[starting_index[ii]:starting_index[ii+1]] = tmp*N2O_slope[ii]+N2O_intercept[ii]
    
    # calibration outputs
    CO_cal = pd.DataFrame({'low_mean': low_CO_mean[rng],
                           'low_std': low_CO_std[rng],
                           'high_mean': high_CO_mean[rng],
                           'high_std': high_CO_std[rng],
                           'low_ratio': CO_low_ratio,
                           'high_ratio': CO_high_ratio, 
                           'slope': CO_slope,
                           'intercept': CO_intercept,
                           'time':CO_time[rng],
                           'cell_T':cell_T[rng]})
    N2O_cal = pd.DataFrame({'low_mean': low_N2O_mean[rng],
                            'low_std': low_N2O_std[rng],
                            'high_mean': high_N2O_mean[rng],
                            'high_std': high_N2O_std[rng],
                            'low_ratio': N2O_low_ratio,
                            'high_ratio': N2O_high_ratio, 
                            'slope': N2O_slope,
                            'intercept': N2O_intercept})
    return CO_cal, N2O_cal
    """


# %% holding
# label ticks with time identifier
#xlabels = [pd.to_datetime(t).strftime('%m.%d %H:%M') for t in low_cal['time']]
#plt.tight_layout()
#plt.savefig('fig1.png',dpi=300)


# -*- coding: utf-8 -*-


# %% handle filtering data
"""
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
"""

# %% plot calibration results
"""
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
"""


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

