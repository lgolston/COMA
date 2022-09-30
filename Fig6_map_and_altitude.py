# -*- coding: utf-8 -*-
"""
Figure
"""

# header
import pandas as pd
import matplotlib.pyplot as plt
from datetime import timedelta
import matplotlib.dates as mdates

import cartopy.crs as ccrs
import cartopy.feature as cf
    
from load_data_functions import read_COMA
from load_data_functions import read_MMS
from load_data_functions import return_filenames

# EDIT THESE
case = 'RF10'
focus = 'flight_CO' # lab, flight_CO, flight_N2O

# %% data
# read COMA data, combining multiple files if needed
filenames = return_filenames(case)

COMA, inlet_ix = read_COMA(filenames['COMA_raw'])

if case == 'RF13': # fix clock setting on this day
    COMA['time'] = COMA['time'] + timedelta(hours=6)

# %% plot data
plt.rc('axes', labelsize=8) # xaxis and yaxis labels
plt.rc('xtick', labelsize=8) # xtick labels
plt.rc('ytick', labelsize=8) # ytick labels

# %% load MMS and WB57 data
MMS = read_MMS(filenames['MMS'])
MMS_sync = MMS.groupby(pd.Grouper(key="time", freq="1s")).mean()
    
# handle COMA data
indices = inlet_ix # use only inlet data
#indices = np.union1d(ix_1,ix_8) # use both inlet and flush data here
COMA_df = pd.DataFrame({'time': COMA['time'][indices], 'CO_dry': COMA["[CO]d_ppm"][indices]*1000, 
                        'N2O_dry': COMA["[N2O]d_ppm"][indices]*1000, 'amb_T': COMA["AmbT_C"]})
COMA_df_sync = COMA_df.groupby(pd.Grouper(key="time", freq="1s")).mean()
    
# time-sync the data with COMA
sync_data = pd.merge(MMS_sync, COMA_df_sync, how='inner', on=['time'])

# %% create figure
fig = plt.figure(figsize=(6.5, 2.5))
ax1 = plt.subplot(121, projection=ccrs.Mercator())
ax2 = plt.subplot(122)
cmap = 'viridis'

# %% lat/lon map (colored by time)
plate = ccrs.PlateCarree()

ax1.add_feature(cf.COASTLINE)
ax1.add_feature(cf.BORDERS)

# OPTION 1: color by CO
sc1 = ax1.scatter(sync_data['LON'].values,sync_data['LAT'].values,c=sync_data['CO_dry'], 
                  vmin=20, vmax=250, cmap=cmap, s = 15, transform=plate)


# %% altitude vs time scatterplot
sc = ax2.scatter(sync_data.index,sync_data['ALT']/1000,c=sync_data['CO_dry'],vmin=20, vmax=250, s = 15, cmap=cmap) # color by CO

cb_position=fig.add_axes([0.91,0.1,0.01,0.85])  ## the parameters are the specified position you set 
cb = plt.colorbar(sc,cax=cb_position)
cb.set_label('CO, ppb')

ax2.grid()
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax2.set_xlabel('Time (UTC)')
ax2.set_ylabel('Altitude, km')

ax1.set_position([0.02, 0.10, 0.397, 0.85]) # left, right, width, height
ax2.set_position([0.49, 0.20, 0.4, 0.75])

  
# %% save figure
#fig.savefig('fig1.png',dpi=300)
