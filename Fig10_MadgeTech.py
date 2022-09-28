# -*- coding: utf-8 -*-
"""
Load data file from MadgeTech temperature logger
Plot against MMS and COMA data

Note that loading .xlsx file takes 5-10 seconds
"""

# %% load data
# import libraries
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from load_data_functions import read_MMS
from load_data_functions import read_COMA
from load_data_functions import return_filenames

# select files to analyze
case = 'RF17'

filenames = return_filenames(case)

# set font sizes
plt.rc('axes', labelsize=12) # xaxis and yaxis labels
plt.rc('xtick', labelsize=12) # xtick labels
plt.rc('ytick', labelsize=12) # ytick labels

# load MadgeTech file
sheet = 'S06126 MultiChannel - Data'
MT = pd.read_excel(filenames['MadgeTech'],sheet_name=sheet,header=6)
#MT_time = [datetime.strptime(tstamp,"%Y-%m-%d %H:%M:%S") for tstamp in MT['Date']]

# load COMA file
COMA, inlet_ix = read_COMA(filenames['COMA_raw'])

ix_8 = np.ravel(np.where(COMA["MIU_VALVE"]==8)) # inlet
ix_7 = np.ravel(np.where(COMA["MIU_VALVE"]==7)) # inlet (lab)
ix_3 = np.ravel(np.where(COMA["MIU_VALVE"]==3)) # high cal
ix_2 = np.ravel(np.where(COMA["MIU_VALVE"]==2)) # low cal
ix_1 = np.ravel(np.where(COMA["MIU_VALVE"]==1)) # flush

if case == 'RF13': # fix clock setting on this day
    COMA['time'] = COMA['time'] + timedelta(hours=6)
    
# load MMS
MMS = read_MMS(filenames['MMS'])

# %% plot data
fig1, ax = plt.subplots(2, 1, figsize=(8,5.5),sharex=True)
#ax[0].plot(MT['Date'],MT['Thermocouple 5 (°C)'],'r.') # RF04 (before column given name)
ax[0].plot(MT['Date'],MT['InletSolen (°C)'],'r.') # RF05
ax[0].plot(MT['Date'],MT['Ambient Temperature 1 (°C)'])
#ax[0].plot(MT['Date'],MT['PowrSupply (°C)'])
#ax[0].plot(MT['Date'],MT['Ext Front (°C)'])
#ax[0].plot(MT['Date'],MT['Lsr_I_tran (°C)'])
#ax[0].plot(MT['Date'],MT['Lasr_I_res (°C)'])
#ax[0].plot(MT['Date'],MT['LaserBack (°C)'])
#ax[0].plot(MT['Date'],MT['CPU (°C)'])
#ax[0].plot(MT['Date'],MT['BoxFanFlow (°C)'])

ax[0].grid('on')
ax0_twin = ax[0].twinx()
ax0_twin.plot(MMS['time'],MMS['ALT'],'k.')
ax[0].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax[0].set_ylabel('Temperature, C')
ax0_twin.set_ylabel('Altitude, m')
ax[0].set_xlabel('Time, UTC')

ax[1].plot(COMA['time'],COMA["GasP_torr"],'k.')
ax[1].plot(COMA['time'][ix_8],COMA["GasP_torr"][ix_8],'b.')
ax[1].plot(COMA['time'][ix_2],COMA["GasP_torr"][ix_2],'y.')
ax[1].plot(COMA['time'][ix_3],COMA["GasP_torr"][ix_3],'m.')
ax[1].grid('on')
ax[1].set_ylabel('Cell pressure, Torr')
fig1.tight_layout()

#fig1.savefig('fig1.png',dpi=300)