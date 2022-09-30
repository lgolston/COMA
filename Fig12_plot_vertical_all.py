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

# %% loop to load the data
COMA = []

for ii in [3,5,10]:  #range(3,18):
    case_name = "RF" + "{:02d}".format(ii)

    filenames = return_filenames(case_name)
    
    filename_COMA = filenames['COMA_ict']
    filename_MMS = filenames['MMS']

    cur_day = datetime.strptime(filename_COMA[-15:-7],"%Y%m%d") # get date from end of file name

    if len(filename_COMA)>0:
        if len(COMA) == 0:
            COMA = pd.read_csv(filename_COMA,header=35)
            COMA['time'] = [cur_day+timedelta(seconds=t) for t in COMA['Time_Mid']]
            COMA['flightID'] = [ii for t in COMA['Time_Mid']]
            MMS = read_MMS_ict(filename_MMS)
        else:
            COMA2 = pd.read_csv(filename_COMA,header=35)
            COMA2['time'] = [cur_day+timedelta(seconds=t) for t in COMA2['Time_Mid']]
            COMA2['flightID'] = [ii for t in COMA2['Time_Mid']]
            MMS2 = read_MMS_ict(filename_MMS)
            
            COMA = pd.concat([COMA,COMA2],ignore_index=True)
            MMS = pd.concat([MMS,MMS2],ignore_index=True)

# %% sychronize data
COMA[COMA['CO'] == -9999] = np.nan

MMS_sync = MMS.groupby(pd.Grouper(key="time", freq="10s")).mean()
COMA_sync = COMA.groupby(pd.Grouper(key="time", freq="10s")).mean()
sync_data = pd.merge(MMS_sync, COMA_sync, how='inner', on=['time'])

# %% plot data
fig1, ax1 = plt.subplots(1, 1, figsize=(5,4))
#plt.plot(COMA['Time_Mid'],COMA['CO'],'.')
cmap = matplotlib.cm.terrain
bounds=[3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
norm = matplotlib.colors.BoundaryNorm(bounds, cmap.N)

sync_randomized = sync_data.sample(frac=1)

sc = ax1.scatter(sync_randomized['CO'],sync_randomized['ALT'],
                 c=sync_randomized['flightID'],s=2,alpha=1,cmap=cmap,norm=norm)
ax1.set_xlim(0,400)
ax1.grid('on')
ax1.set_xlabel('CO, ppbv')
ax1.set_ylabel('Altitude, m')
cb = plt.colorbar(sc)
cb.set_label('Flight ID')
cb.solids.set(alpha=1)
fig1.tight_layout()

#fig1.savefig('fig1.png',dpi=300)