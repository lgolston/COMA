# -*- coding: utf-8 -*-
"""
Load data file from MadgeTech temperature logger
Slow loading .xlsx files converted to csv
In-pallet temperature vs. altitude

TODO
1. load all files
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

fig1, ax = plt.subplots(1, 1, figsize=(5,2.7))

for ii in range(0,12):
    MT = pd.read_csv('../Data/MadgeTech_csv/'+fname[ii][0],sep=',',header=6,encoding='latin1')
    MT['time'] = [parser.parse(tstamp) for tstamp in (MT['Date']+' '+MT['Time'])]
    
    # load MMS
    MMS = read_MMS_ict('../Data/_OtherData_/' + fname[ii][1])
    
    # sync data
    MT_1s_avg = MT.groupby(pd.Grouper(key="time", freq="1s")).mean()
    MMS_1s_avg = MMS.groupby(pd.Grouper(key="time", freq="1s")).mean()
    sync_data = pd.merge(MMS_1s_avg, MT_1s_avg, how='inner', on=['time'])

    # %% plot data
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
    
    ax.plot(sync_data['Ambient Temperature 1 (°C)'],sync_data['P'],'.')

fig1.tight_layout()
#fig1.savefig('fig1.png',dpi=300)
