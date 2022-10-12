# -*- coding: utf-8 -*-
"""
Figure
"""

# %% header
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.dates as mdates

from load_data_functions import return_filenames
from load_data_functions import read_COMA
from load_data_functions import read_ACOS_ict
from load_data_functions import read_MMS_ict

# set plot style
plt.rc('axes', labelsize=8) # xaxis and yaxis labels
plt.rc('xtick', labelsize=8) # xtick labels
plt.rc('ytick', labelsize=8) # ytick labels

# load files
case = 'Transit8'

# load COMA    
filenames = return_filenames(case)
COMA, inlet_ix = read_COMA(filenames['COMA_raw'])

# load MMS
MMS = read_MMS_ict(filenames['MMS'])
MMS[MMS['T']<0] = np.nan

# load GEOS model
filename_GEOS = '../Data/_Model_/ACCLIP-GEOS_WB57_20220913_RA.ict'
cur_day = datetime.strptime(filename_GEOS[-15:-7],"%Y%m%d")
GEOS = pd.read_csv(filename_GEOS,sep=',',header=61)
GEOS['time'] = [cur_day+timedelta(seconds=t) for t in GEOS['Time_Start']]

# load ozone (preliminary MTS version)
filename_UASO3 = '../Data/_OtherData_/UASO3_telemetry-6320db6532c0bcdb35876e58.csv'
UASO3 = pd.read_csv(filename_UASO3,sep=',', header=0, skiprows=lambda x: (x != 0) and not x % 2)
UASO3['time'] = [datetime.strptime(tstamp,"%Y-%m-%dT%H:%M:%S.%fZ") for tstamp in UASO3['Timestamp']]


# %% create figure
fig, ax = plt.subplots(2, 1, figsize=(6,3.5),sharex=True)

ax[0].plot(COMA['time'][inlet_ix],COMA["[CO]d_ppm"][inlet_ix]*1000,'m',marker='.',label='COMA',markersize=0.1)
ax[0].set_ylim(10,50)
ax0_twin = ax[0].twinx()
ax0_twin.plot(COMA['time'][inlet_ix],COMA["[N2O]d_ppm"][inlet_ix]*1000,'k',marker='.',label='COMA',markersize=0.1)

ax[1].plot(UASO3['time'],UASO3['Ozone Mixing Ratio'])
ax[1].set_ylim(0,800)

#ax[0].plot(GEOS['time'],GEOS[' CO_GEOS']*1E9)
#ax0_twin.set_ylim(10,50)

#ax[1].plot(MMS['time'],MMS['POT'])
#ax[1].plot(GEOS['time'],GEOS[' POTT_GEOS'])
#ax[1].set_ylim(200,500)

#ax[1].plot(MMS['time'],MMS['P'])
#ax[1].plot(GEOS['time'],GEOS[' TROPPB_GEOS'])
#ax[1].set_ylim(0,600)

#ax[1].plot(GEOS['time'],GEOS[' EPV_GEOS'])
#ax[1].set_ylim(0,2E-5)

#ax_twin.plot(MMS['time'],MMS['T'])
#MMS['ALT']


#CO_GEOS
#QV_GEOS
