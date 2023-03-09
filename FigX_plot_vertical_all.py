# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 22:58:33 2022

"""

# %% headers
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from datetime import datetime, timedelta
from load_data_functions import read_MMS_ict
from load_data_functions import return_filenames

plt.rcParams['axes.labelsize'] = 8
plt.rcParams['legend.fontsize'] = 8
plt.rcParams['xtick.labelsize'] = 7
plt.rcParams['ytick.labelsize'] = 7

# %% loop to load the data
fig1, ax1 = plt.subplots(1, 1, figsize=(3.5,3.5))

for ii in [10,5,3]:  #range(3,18):
    # load data
    case_name = "RF" + "{:02d}".format(ii)

    filenames = return_filenames(case_name)
    
    filename_COMA = filenames['COMA_ict']
    filename_MMS = filenames['MMS']

    cur_day = datetime.strptime(filename_COMA[-15:-7],"%Y%m%d") # get date from end of file name
    COMA = pd.read_csv(filename_COMA,header=35)
    COMA['time'] = [cur_day+timedelta(seconds=t) for t in COMA['Time_Mid']]
    #COMA['flightID'] = [ii for t in COMA['Time_Mid']]
    
    MMS = read_MMS_ict(filename_MMS)          

    # sychronize data
    COMA[COMA['CO'] == -9999] = np.nan
    
    MMS_sync = MMS.groupby(pd.Grouper(key="time", freq="10s")).mean()
    COMA_sync = COMA.groupby(pd.Grouper(key="time", freq="10s")).mean()
    sync_data = pd.merge(MMS_sync, COMA_sync, how='inner', on=['time'])

    # plot
    ax1.plot(sync_data['CO'],sync_data['ALT']/1000,'.',label=case_name)

# %% format plot
ax1.legend(ncol=3)
ax1.set_xlim(0,350)
ax1.grid('on')
ax1.set_xlabel('CO, ppbv')
ax1.set_ylabel('Altitude, km')
fig1.tight_layout()
#fig1.savefig('fig1.png',dpi=300)
