# -*- coding: utf-8 -*-
"""
Plot interesting aspects of WB-57 return transit
"""

# %% header
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.dates as mdates

from load_data_functions import return_filenames
from load_data_functions import read_COMA
from load_data_functions import read_MMS_ict

# set plot style
plt.rc('axes', labelsize=8) # xaxis and yaxis labels
plt.rc('xtick', labelsize=8) # xtick labels
plt.rc('ytick', labelsize=8) # ytick labels
plt.rcParams.update({'mathtext.default': 'regular' } ) # not italics

# load files
case = 'Transit8'

# load COMA    
filenames = return_filenames(case)
COMA, inlet_ix = read_COMA(filenames['COMA_raw'])

# load MMS
MMS = read_MMS_ict(filenames['MMS'])
MMS[MMS['T']<0] = np.nan

# additional filenames
if case == 'Transit7': # Misawa to Adak
    #filename_UASO3 = '../Data/_OtherData_/UASO3_telemetry-631fa94e32c0bcdb3575ece4.csv'
    filename_UASO3 = '../Data/_OtherData_/ACCLIP-UASO3_WB57_20220912_RA.ict'
    filename_GEOS = '../Data/_Model_/ACCLIP-GEOS_WB57_20220912_RC.ict'
elif case == 'Transit8': # Adak to Seattle
    #filename_UASO3 = '../Data/_OtherData_/UASO3_telemetry-6320db6532c0bcdb35876e58.csv'
    filename_UASO3 = '../Data/_OtherData_/ACCLIP-UASO3_WB57_20220913_RA.ict'
    filename_GEOS = '../Data/_Model_/ACCLIP-GEOS_WB57_20220913_RC.ict'

# load GEOS
cur_day = datetime.strptime(filename_GEOS[-15:-7],"%Y%m%d")
GEOS = pd.read_csv(filename_GEOS,sep=',',header=61)
GEOS['time'] = [cur_day+timedelta(seconds=t) for t in GEOS['Time_Start']]

# load ozone
# (preliminary MTS version)
#UASO3 = pd.read_csv(filename_UASO3,sep=',', header=0, skiprows=lambda x: (x != 0) and not x % 2)
#UASO3['time'] = [datetime.strptime(tstamp,"%Y-%m-%dT%H:%M:%S.%fZ") for tstamp in UASO3['Timestamp']]

# (ict version)
cur_day = datetime.strptime(filename_UASO3[-15:-7],"%Y%m%d") # get date from end of file name
UASO3 = pd.read_csv(filename_UASO3,header=32)
UASO3['time'] = [cur_day+timedelta(seconds=t) for t in UASO3['Time_Start']]
UASO3[UASO3[' O3_ppb '] == -9999] = np.nan

# %% create figure
fig, ax = plt.subplots(2, 1, figsize=(6,3.5),sharex=True)

ax[0].plot(COMA['time'][inlet_ix],COMA["[CO]d_ppm"][inlet_ix]*1000,'m',label='CO',linewidth=1,alpha=0.9)
ax[0].set_ylim(0,90)
ax[0].plot(COMA['time'][inlet_ix],COMA["[N2O]d_ppm"][inlet_ix]*1000 - 270,'k',label='N2O',linewidth=1,alpha=0.9)
ax[0].grid('on')
ax[0].set_ylabel(r'$N_2O - 270, ppb$',color='k')
ax[0].text(-0.13,0.4,'CO, ppb',transform=ax[0].transAxes,rotation='vertical',fontsize=8,color='m')

ax0_twin = ax[0].twinx()
ax0_twin.plot(UASO3['time'],UASO3[' O3_ppb '],'b',linewidth=1,alpha=0.9,label='O3')
ax0_twin.set_ylim(0,1200)
ax0_twin.set_ylabel('Ozone, ppb',color='b')

fig.legend(ncol=3,loc='upper center')
ax[1].plot(MMS['time'],MMS['P'],'k')
ax[1].plot(GEOS['time'],GEOS[' TROPPB_GEOS'],'k:')
ax[1].set_ylim(0,400)
ax[1].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

ax[0].set_position([0.12, 0.40, 0.78, 0.55]) # left, bottom, width, height
ax[1].set_position([0.12, 0.10, 0.78, 0.20])
ax[1].set_ylabel('Pressure, hPa')

#(GEOS['time'],GEOS[' CO_GEOS']*1E9)
#(MMS['time'],MMS['POT'])
#(GEOS['time'],GEOS[' POTT_GEOS'])
#(MMS['time'],MMS['P'])
#(GEOS['time'],GEOS[' EPV_GEOS'])
#(MMS['time'],MMS['T'])
#MMS['ALT']
#CO_GEOS
#QV_GEOS

#fig.savefig('fig1.png',dpi=300)
