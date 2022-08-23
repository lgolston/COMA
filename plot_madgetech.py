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
from load_flight_functions import read_MMS
from load_flight_functions import read_COMA
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# select files to analyze
case = 'RF11'

if case == 'RF04': #RF04 (first flight with MadgeTech installed)
    filename_MT = '../Data/2022-08-04/8.4.2022 flight Madgetech.xlsx'
    filename_MMS = '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20220804_RA.ict'
    filename_COMA = ['../Data/2022-08-04/n2o-co_2022-08-04_f0000.txt']
elif case == 'RF05': #RF05
    filename_MT = '../Data/2022-08-06/8.6.2022 flight Madgetech.xlsx'
    filename_MMS = '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20220804_RA.ict'
    filename_COMA = ['../Data/2022-08-06/n2o-co_2022-08-06_f0000.txt']    
elif case == 'RF06': #RF06
    filename_MT = '../Data/2022-08-12/8.12.2022 flight Madgetech.xlsx'
    filename_MMS = '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20220812_RA.ict'
    filename_COMA = ['../Data/2022-08-12/n2o-co_2022-08-12_f0000.txt']    
elif case == 'RF07': #RF07
    filename_MT = '../Data/2022-08-13/8.13.2022 flight Madgetech.xlsx'
    filename_MMS = '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20220813_RA.ict'
    filename_COMA = ['../Data/2022-08-13/n2o-co_2022-08-13_f0000.txt']    
elif case == 'RF08': #RF08
    filename_MT = '../Data/2022-08-15/8.15.2022 flight Madgetech.xlsx'
    filename_MMS = '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20220815_RA.ict'
    filename_COMA = ['../Data/2022-08-15/n2o-co_2022-08-15_f0000.txt',
                     '../Data/2022-08-15/n2o-co_2022-08-15_f0001.txt']    
elif case == 'RF09': #RF09
    filename_MT = '../Data/2022-08-16/8.16.2022 flight Madgetech.xlsx'
    filename_MMS = '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20220816_RA.ict'
    filename_COMA = ['../Data/2022-08-16/n2o-co_2022-08-16_f0000.txt']    
elif case == 'RF10': #RF10
    filename_MT = '../Data/2022-08-18/8.18.2022 flight Madgetech.xlsx'
    filename_MMS = '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20220819_RA.ict'
    filename_COMA = ['../Data/2022-08-18/n2o-co_2022-08-18_f0000.txt']    
elif case == 'RF11': #RF11
    filename_MT = '../Data/2022-08-21/8.21.2022 flight Madgetech.xlsx'
    filename_MMS = '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20220821_RA.ict'
    filename_COMA = ['../Data/2022-08-21/n2o-co_2022-08-21_f0000.txt']  
    
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

ix_8 = np.ravel(np.where(COMA["      MIU_VALVE"]==8)) # inlet
ix_7 = np.ravel(np.where(COMA["      MIU_VALVE"]==7)) # inlet (lab)
ix_3 = np.ravel(np.where(COMA["      MIU_VALVE"]==3)) # high cal
ix_2 = np.ravel(np.where(COMA["      MIU_VALVE"]==2)) # low cal
ix_1 = np.ravel(np.where(COMA["      MIU_VALVE"]==1)) # flush

# load MMS
MMS = read_MMS(filename_MMS)

# %% plot data
fig1, ax = plt.subplots(2, 1, figsize=(8,5.5),sharex=True)
#ax[0].plot(MT['Date'],MT['Thermocouple 5 (°C)'],'r.') # RF04 (before column given name)
ax[0].plot(MT['Date'],MT['InletSolen (°C)'],'r.') # RF05
#ax[0].plot(MT['Date'],MT['Ambient Temperature 1 (°C)'])
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

ax[1].plot(COMA['time'],COMA["      GasP_torr"],'k.')
ax[1].plot(COMA['time'][ix_8],COMA["      GasP_torr"][ix_8],'b.')
ax[1].plot(COMA['time'][ix_2],COMA["      GasP_torr"][ix_2],'y.')
ax[1].plot(COMA['time'][ix_3],COMA["      GasP_torr"][ix_3],'m.')
ax[1].grid('on')
ax[1].set_ylabel('Cell pressure, Torr')
fig1.tight_layout()

#fig1.savefig('fig1.png',dpi=300)