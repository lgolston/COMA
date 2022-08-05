# -*- coding: utf-8 -*-
"""
@author: madco
"""

# %% load data
# import libraries
import pandas as pd
from load_flight_functions import read_MMS
from load_flight_functions import read_COMA
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

filename_MT = '../Data/2022-08-04/8.4.2022 flight Madgetech.xlsx'
filename_MMS = '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20220804_RA.ict'
filename_COMA = ['../Data/2022-08-04/n2o-co_2022-08-04_f0000.txt']
cur_day = datetime(2022,8,4)

# set font sizes
plt.rc('axes', labelsize=12) # xaxis and yaxis labels
plt.rc('xtick', labelsize=12) # xtick labels
plt.rc('ytick', labelsize=12) # ytick labels

# load MadgeTech file
sheet = 'S06126 MultiChannel - Data'
MT = pd.read_excel(filename_MT,sheet_name=sheet,header=6)
#MT_time = [datetime.strptime(tstamp,"%Y-%m-%d %H:%M:%S") for tstamp in MT['Date']]

# load COMA file
COMA = read_COMA(filename_COMA)

# load MMS
MMS = read_MMS(filename_MMS,cur_day)

# %% plot data
fig1, ax = plt.subplots(2, 1, figsize=(8,5.5),sharex=True)
ax[0].plot(MT['Date'],MT['Thermocouple 5 (°C)'],'r.')
ax[0].grid('on')
ax0_twin = ax[0].twinx()
ax0_twin.plot(MMS['time'],MMS['ALT'],'k.')
ax[0].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax[0].set_ylabel('Temperature, C')
ax0_twin.set_ylabel('Altitude, m')
ax[0].set_xlabel('Time, UTC')

ax[1].plot(COMA['time'],COMA["      GasP_torr"],'k.')
ax[1].grid('on')
ax[1].set_ylabel('Cell pressure, Torr')
fig1.tight_layout()

#fig1.savefig('fig1.png',dpi=300)