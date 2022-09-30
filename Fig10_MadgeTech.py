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

from load_data_functions import read_MMS_ict
from load_data_functions import read_COMA
from load_data_functions import return_filenames

# select files to analyze
case = 'RF17'

filenames = return_filenames(case)

# set font sizes
plt.rcParams['axes.labelsize'] = 8
plt.rcParams['legend.fontsize'] = 7
plt.rcParams['xtick.labelsize'] = 7
plt.rcParams['ytick.labelsize'] = 7
plt.rcParams['font.size']=8
plt.rcParams.update({'mathtext.default': 'regular' } ) # not italics

# load MadgeTech file
sheet = 'S06126 MultiChannel - Data'
MT = pd.read_excel(filenames['MadgeTech'],sheet_name=sheet,header=6)
#MT_time = [datetime.strptime(tstamp,"%Y-%m-%d %H:%M:%S") for tstamp in MT['Date']]

# load COMA file
COMA, inlet_ix = read_COMA(filenames['COMA_raw'])

if case == 'RF13': # fix clock setting on this day
    COMA['time'] = COMA['time'] + timedelta(hours=6)
    
# load MMS
MMS = read_MMS_ict(filenames['MMS'])

# %% plot data
fig1, ax = plt.subplots(1, 1, figsize=(6,3))
#ax[0].plot(MT['Date'],MT['Thermocouple 5 (°C)'],'r.') # RF04 (before column given name)
ax.plot(MT['Date'],MT['InletSolen (°C)'],'r',label='Solenoid') # RF05
ax.plot(MT['Date'],MT['Ambient Temperature 1 (°C)'],label='Ambient')
ax.plot(MT['Date'],MT['PowrSupply (°C)'],label='Powr supply')
ax.plot(MT['Date'],MT['Ext Front (°C)'],label='Ext front')
ax.plot(MT['Date'],MT['Lsr_I_tran (°C)'],label='Lsr transistor')
ax.plot(MT['Date'],MT['Lasr_I_res (°C)'],label='Lsr resistor')
ax.plot(MT['Date'],MT['LaserBack (°C)'],label='Lsr back')
#ax.plot(MT['Date'],MT['CPU (°C)'])
#ax.plot(MT['Date'],MT['BoxFanFlow (°C)'])

ax_twin = ax.twinx()
ax_twin.plot(MMS['time'],MMS['ALT']/1000,'k.')

ax.grid('on')
ax.legend()
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax.set_ylabel('Temperature, °C')
ax_twin.set_ylabel('Altitude, km')
ax.set_xlabel('Time, UTC')

ax.set_xlim(datetime(2022,9,1,1),datetime(2022,9,1,9))

fig1.tight_layout()
#fig1.savefig('fig1.png',dpi=300)

#ix_8 = np.ravel(np.where(COMA["MIU_VALVE"]==8)) # inlet
#ix_7 = np.ravel(np.where(COMA["MIU_VALVE"]==7)) # inlet (lab)
#ix_3 = np.ravel(np.where(COMA["MIU_VALVE"]==3)) # high cal
#ix_2 = np.ravel(np.where(COMA["MIU_VALVE"]==2)) # low cal
#ix_1 = np.ravel(np.where(COMA["MIU_VALVE"]==1)) # flush
#ax[1].plot(COMA['time'],COMA["GasP_torr"],'k.')
#ax[1].plot(COMA['time'][ix_8],COMA["GasP_torr"][ix_8],'b.')
#ax[1].plot(COMA['time'][ix_2],COMA["GasP_torr"][ix_2],'y.')
#ax[1].plot(COMA['time'][ix_3],COMA["GasP_torr"][ix_3],'m.')
#ax[1].grid('on')
#ax[1].set_ylabel('Cell pressure, Torr')

