# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 15:59:43 2022

@author: madco
"""

# %% load libraries and files
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.dates as mdates

from load_flight_functions import read_COMA
from load_flight_functions import read_MMS

# EDIT THESE
case = 'RF10'

if case == 'RF10': # RF10 (instrument start before midnight; takeoff on 2022-08-19 UTC)
    filename_COMA = ['../Data/2022-08-18/n2o-co_2022-08-18_f0000.txt']
    filename_MMS_WB = '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20220819_RA.ict'
    filename_GV = '../Data/_OtherData_/ACCLIP-CORE_GV_20220818_RA.ict'

MMS = read_MMS(filename_MMS_WB)

def read_GV_ict(filename):
    cur_day = datetime.strptime(filename[-15:-7],"%Y%m%d") # get date from end of file name
    GV = pd.read_csv(filename,sep=',',header=158)
    GV['time'] = [cur_day+timedelta(seconds=t) for t in GV['Time_Start']]
    return GV

GV = read_GV_ict(filename_GV)

#ALT
#LATC and #LONC
#GGLAT and GGLON; GGALT
#PALT

# %% 3d plot
fig, ax = plt.subplots(3, 1, figsize=(10,8),sharex=True)

ax[0].plot(MMS['time'],MMS['LAT'],'.',label='MMS WB57')
ax[0].plot(GV['time'],GV['LATC'],'.',label='GV')
#ax[0].plot(GV['time'],GV['GGLAT'],'.')
ax[0].grid()
ax[0].set_ylim(30,40)
ax[0].set_ylabel('Latitude')
ax[0].legend(loc='lower left')

ax[1].plot(MMS['time'],MMS['LON'],'.')
ax[1].plot(GV['time'],GV['LONC'],'.')
ax[1].grid()
ax[1].set_ylabel('Longitude')
#ax[1].plot(GV['time'],GV['GGLON'],'.')

ax[2].plot(MMS['time'],MMS['ALT'],'.')
ax[2].plot(GV['time'],GV['ALT'],'.')
ax[2].grid()
ax[2].set_ylim(0,20000)
ax[2].set_ylabel('Altitude, m')

ax[0].set_xlim(datetime(2022,8,19,0),datetime(2022,8,19,7))
ax[0].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax[0].set_title('RF10 WB-57 and GV')
fig.tight_layout()

#fig.savefig('fig1.png',dpi=300)


# %% 3D
fig = plt.figure()
ax = fig.add_subplot(projection='3d')

#sm = plt.cm.ScalarMappable(cmap='viridis', 
#                           norm=plt.Normalize(vmin=datetime(2022,8,19,0),
#                                              vmax=datetime(2022,8,19,7)))

p1 = ax.scatter(GV['GGLON'],GV['GGLAT'],GV['GGALT']) #c=GV['time']
p2 = ax.scatter(MMS['LON'],MMS['LAT'],MMS['ALT'])#c=MMS['time']
#cb = plt.colorbar(p1)
#cb.ax.set_yticklabels(pd.to_datetime(cb.get_ticks()).strftime(date_format='%H:%M'))
#cb.set_label('Time, UTC')

