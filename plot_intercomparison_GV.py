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
from functools import reduce
from load_data_functions import read_COMA
from load_data_functions import read_MMS_ict

# set plot style
plt.rcParams['axes.labelsize'] = 8
plt.rcParams['legend.fontsize'] = 8
plt.rcParams['xtick.labelsize'] = 7
plt.rcParams['ytick.labelsize'] = 7
plt.rcParams.update({'mathtext.default': 'regular' } ) # not italics

# EDIT THESE
case = 'RF13'

if case == 'RF10': # RF10 (instrument start before midnight; takeoff on 2022-08-19 UTC)
    filename_COMA = ['../Data/2022-08-18/n2o-co_2022-08-18_f0000.txt']
    filename_MMS_WB = '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20220819_RA.ict'
    filename_GV = '../Data/_OtherData_/ACCLIP-CORE_GV_20220818_RA.ict'
    fig_title = 'WB-RF10 and GV-RF08'
elif case == 'RF13': # RF13
    filename_COMA = ['../Data/2022-08-24/n2o-co_2022-08-24_f0002.txt']
    filename_MMS_WB = '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20220825_RA.ict'
    filename_GV = '../Data/_OtherData_/ACCLIP-CORE_GV_20220824_RA.ict'
    fig_title = 'WB-RF13 and GV-RF11'

# load files
COMA, inlet_ix = read_COMA(filename_COMA)
if case == 'RF13':  # correct six hour offset
    COMA['time'] = COMA['time'] + timedelta(hours=6)

MMS = read_MMS_ict(filename_MMS_WB)

def read_GV_ict(filename):
    cur_day = datetime.strptime(filename[-15:-7],"%Y%m%d") # get date from end of file name
    GV = pd.read_csv(filename,sep=',',header=158)
    GV['time'] = [cur_day+timedelta(seconds=t) for t in GV['Time_Start']]
    return GV

GV = read_GV_ict(filename_GV)

# sync COMA and MMS
MMS_sync = MMS.groupby(pd.Grouper(key="time", freq='1s')).mean()
COMA_sync = COMA.groupby(pd.Grouper(key="time", freq='1s')).mean()
df = [MMS_sync, COMA_sync]
sync_data = reduce(lambda  left,right: pd.merge(left,right,on=['time'],how='inner'), df).fillna(np.nan)


# %%  times series comparison of latitude, longitude, altitude
# relevant GV variables:
#ALT
#LATC and #LONC
#GGLAT and GGLON; GGALT
#PALT

fig1, ax = plt.subplots(3, 1, figsize=(6,4),sharex=True)

ax[0].plot(MMS['time'],MMS['LAT'],'.',label='WB57')
ax[0].plot(GV['time'],GV['LATC'],'.',label='GV')
#ax[0].plot(GV['time'],GV['GGLAT'],'.')
ax[0].grid()
ax[0].set_ylabel('Latitude')
ax[0].legend(loc='lower left')

ax[1].plot(MMS['time'],MMS['LON'],'.')
ax[1].plot(GV['time'],GV['LONC'],'.')
ax[1].grid()
ax[1].set_ylabel('Longitude')
#ax[1].plot(GV['time'],GV['GGLON'],'.')

ax[2].plot(MMS['time'],MMS['ALT'],'.')
ax[2].plot(GV['time'],GV['GGALT'],'.')
ax[2].grid()
ax[2].set_ylabel('Altitude, m')

# RF10 settings
if case == 'RF10':
    ax[0].set_ylim(30,40)
    ax[2].set_ylim(0,20000)
    ax[0].set_xlim(datetime(2022,8,19,0),datetime(2022,8,19,7))
elif case == 'RF13':
    ax[0].set_ylim(27,38)
    ax[0].set_xlim(datetime(2022,8,25,0),datetime(2022,8,25,7))

ax[0].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax[0].set_title(fig_title)
fig1.tight_layout()

# %% CO and N2O comparison
#COA_ARI
#CO_ARI
#CO_PIC2401
#N2OA_ARI
#N2O_ARI
#COCAL_ARI
#COCAL_PIC2401

fig2, ax = plt.subplots(2, 1, figsize=(6,4),sharex=True)
#ax[0].plot(COMA['time'][inlet_ix],COMA["      [CO]d_ppm"][inlet_ix]*1000,'b.',label='COMA')
#ax[0].plot(GV['time'],GV["CO_ARI"],'k.',label='GV ARI')
#ax[0].plot(GV['time'],GV['CO_PIC2401']*1000,'g.',label='GV PIC2401')#,markersize=1

#ix_timeWB = np.ravel(np.where((sync_data.index>datetime(2022,8,19,4,57)) & (sync_data.index<datetime(2022,8,19,5,30))))
#ix_timeGV = np.ravel(np.where((GV['time']>datetime(2022,8,19,4,55)) & (GV['time']<datetime(2022,8,19,5,22))))

ix_timeWB = np.ravel(np.where((sync_data.index>datetime(2022,8,25,2,12)) & (sync_data.index<datetime(2022,8,25,2,40))))
ix_timeGV = np.ravel(np.where((GV['time']>datetime(2022,8,25,2,10)) & (GV['time']<datetime(2022,8,25,2,30))))

ax[0].plot(sync_data["LAT"][ix_timeWB],sync_data["[CO]d_ppm"][ix_timeWB]*1000,'.',label='WB COMA')
ax[0].plot(GV['GGLAT'][ix_timeGV],GV["CO_ARI"][ix_timeGV],'k.',label='GV ARI')
ax[0].plot(GV['GGLAT'][ix_timeGV],GV['CO_PIC2401'][ix_timeGV]*1000,'g.',label='GV PIC2401')#,markersize=1

ax[0].set_ylabel('CO, ppb')
ax[0].legend()

#ax[1].plot(COMA['time'][inlet_ix],COMA["     [N2O]d_ppm"][inlet_ix]*1000,'b.',label='COMA')
#ax[1].plot(GV['time'],GV["N2O_ARI"],'k.',label='ARI')

ax[1].plot(sync_data["LAT"][ix_timeWB],sync_data["[N2O]d_ppm"][ix_timeWB]*1000,'.')
ax[1].plot(GV['GGLAT'][ix_timeGV],GV["N2O_ARI"][ix_timeGV],'k.',label='ARI')

ax[1].set_ylabel('N2O, ppb')
ax[1].set_xlabel('Latitude')
#ax[1].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

#RF10
if case == 'RF10':
    ax[0].set_ylim(140,320)
    ax[1].set_ylim(320,340)
    #ax[0].set_xlim(datetime(2022,8,19,4,57),datetime(2022,8,19,5,30))
    plt.suptitle(fig_title)

#RF13
if case == 'RF13':
    ax[0].set_ylim(65,180)
    ax[1].set_ylim(320,340)
    #ax[0].set_xlim(datetime(2022,8,25,2,10),datetime(2022,8,25,2,30))
    plt.suptitle(fig_title)
    
fig2.tight_layout()

#fig1.savefig('fig1.png',dpi=300)
#fig2.savefig('fig2.png',dpi=300)

# %% 3D flight tracks
"""
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
"""