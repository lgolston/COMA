# -*- coding: utf-8 -*-
"""
Load data file from MadgeTech temperature logger
Slow loading .xlsx files converted to csv
In-pallet temperature vs. altitude

TODO
1. add time colorbar
2. also test labeling by time since takeoff
3. calculate statistics in UTLS
"""

# %% header
# import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from load_data_functions import read_MMS_ict
from dateutil import parser

# set font sizes
plt.rcParams['axes.labelsize'] = 8
plt.rcParams['legend.fontsize'] = 7
plt.rcParams['xtick.labelsize'] = 7
plt.rcParams['ytick.labelsize'] = 7
plt.rcParams['font.size']=8
plt.rcParams.update({'mathtext.default': 'regular' } ) # not italics
cmap = 'viridis'

# %% load files files
# load MadgeTech file
# skip ['8.21.2022 flight Madgetech.csv','ACCLIP-MMS-1HZ_WB57_20220821_RA.ict'], which has no amb temp
fname = [['8.4.2022 flight Madgetech_wAmbTemp.csv','ACCLIP-MMS-1HZ_WB57_20220804_RA.ict'],
         ['8.6.2022 flight Madgetech.csv','ACCLIP-MMS-1HZ_WB57_20220806_RA.ict'],
         ['8.12.2022 flight Madgetech.csv','ACCLIP-MMS-1HZ_WB57_20220812_RA.ict'],
         ['8.15.2022 flight Madgetech.csv','ACCLIP-MMS-1HZ_WB57_20220815_RA.ict'],
         ['8.16.2022 flight Madgetech.csv','ACCLIP-MMS-1HZ_WB57_20220816_RA.ict'],
         ['8.18.2022 flight Madgetech.csv','ACCLIP-MMS-1HZ_WB57_20220819_RA.ict'],
         ['8.23.2022 flight Madgetech.csv','ACCLIP-MMS-1HZ_WB57_20220823_RA.ict'],
         ['8.25.2022 flight Madgetech.csv','ACCLIP-MMS-1HZ_WB57_20220825_RA.ict'],
         ['8.26.2022 flight Madgetech.csv','ACCLIP-MMS-1HZ_WB57_20220826_RA.ict'],
         ['8.29.2022 flight Madgetech.csv','ACCLIP-MMS-1HZ_WB57_20220829_RA.ict'],
         ['8.31.2022 flight Madgetech.csv','ACCLIP-MMS-1HZ_WB57_20220831_RA.ict'],
         ['9.01.2022 flight Madgetech.csv','ACCLIP-MMS-1HZ_WB57_20220901_RA.ict']]

for ii in range(0,12):
    # load MadgeTech csv file
    MT = pd.read_csv('../Data/MadgeTech_csv/'+fname[ii][0],sep=',',header=6,encoding='latin1')
    MT['time'] = [parser.parse(tstamp) for tstamp in (MT['Date']+' '+MT['Time'])]
    
    # load MMS
    MMS = read_MMS_ict('../Data/_OtherData_/' + fname[ii][1])
    
    # sync data
    MT_1s_avg = MT.groupby(pd.Grouper(key="time", freq="1s")).mean()
    MMS_1s_avg = MMS.groupby(pd.Grouper(key="time", freq="1s")).mean()

    # merge
    if ii == 0:
        sync_data = pd.merge(MMS_1s_avg, MT_1s_avg, how='inner', on=['time'])
    else:
        sync_data2 = pd.merge(MMS_1s_avg, MT_1s_avg, how='inner', on=['time'])
        sync_data = pd.concat([sync_data,sync_data2],ignore_index=True)

# %% plot data
fig1, ax = plt.subplots(1, 1, figsize=(5,2.7))

# vertical profile
sc = ax.scatter(sync_data.index,sync_data['P'],c=sync_data['Ambient Temperature 1 (°C)'],
                s = 5, cmap=cmap, vmin=-1, vmax=10) # color by CO

# ?
#sc = ax.scatter(sync_data['Ambient Temperature 1 (°C)'],c=sync_data['P'], s = 5, cmap=cmap) # color by CO

#ax.plot(sync_data['Ambient Temperature 1 (°C)'],sync_data['P'],'.')

#ax[0].plot(MT['Date'],MT['Thermocouple 5 (°C)'],'r.') # RF04 (before column given name)
#ax.plot(MT_time,MT['InletSolen (°C)'],'r',label='Solenoid') # RF05
#ax.plot(MT['time'],MT['Ambient Temperature 1 (°C)'],label='Ambient')
#ax.plot(MT_time,MT['PowrSupply (°C)'],label='Powr supply')
#ax.plot(MT_time,MT['Ext Front (°C)'],label='Ext front')
#ax.plot(MT_time,MT['Lsr_I_tran (°C)'],label='Lsr transistor')
#ax.plot(MT_time,MT['Lasr_I_res (°C)'],label='Lsr resistor')
#ax.plot(MT_time,MT['LaserBack (°C)'],label='Lsr back')
#ax.plot(MT_time,MT['CPU (°C)'])
#ax.plot(MT_time,MT['BoxFanFlow (°C)'])
    
fig1.tight_layout()
ax.set_xlabel('Temperature, C')
ax.set_ylabel('Pressure, hPa')
#fig1.savefig('fig1.png',dpi=300)
