# -*- coding: utf-8 -*-
"""
Plot maps of 2021 test flights from Houston
"""

# %% header
from datetime import datetime
import matplotlib.pyplot as plt
from load_data_functions import read_COMA
from load_data_functions import read_MMS_ict
from load_data_functions import sync_data
from load_data_functions import return_filenames
import cartopy.crs as crs
import cartopy.feature as cfeature

# %% plot settings
plt.rcParams['axes.labelsize'] = 8
plt.rcParams['legend.fontsize'] = 8
plt.rcParams['xtick.labelsize'] = 7
plt.rcParams['ytick.labelsize'] = 7
plt.rcParams.update({'mathtext.default': 'regular' } ) # not italics

# %% start cartopy map
fig = plt.figure(figsize=(6,3),dpi=100)

projection = crs.Mercator(central_longitude=180)
plate = crs.PlateCarree()

ax = fig.add_subplot(1,1,1, projection=projection)

ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.STATES)

# %% process data
#for case in range(0, 4):
#for case in ['Transit6','Transit7','Transit8','Transit9']:
to_plot = 'CO'
    
for case in ['RF10']: #
    # load files
    filenames = return_filenames(case)
    
    COMA, inlet_ix = read_COMA(filenames['COMA_raw'])
    MMS = read_MMS_ict(filenames['MMS'])
    synced_data = sync_data(MMS,COMA,inlet_ix)

    print(min(synced_data['CO_dry']))
    print(max(synced_data['CO_dry']))
    print(min(synced_data['N2O_dry']))
    print(max(synced_data['N2O_dry']))
    print()
    
    # plot map    
    if to_plot == 'CO':
        sc1 = ax.scatter(synced_data['LON'],synced_data['LAT'],c=synced_data['CO_dry'],vmin=20, vmax=100, s = 15, transform=plate)
    else:
        sc1 = ax.scatter(synced_data['LON'],synced_data['LAT'],c=synced_data['N2O_dry'],vmin=280, vmax=340, s = 15, transform=plate)

# %% format
# for outbound transit
ax.set_position([0.025, 0.3, 0.95, 0.652])
cbar_ax = fig.add_axes([0.06, 0.17, 0.90, 0.04])

# for return transit
#ax.set_position([0.05, 0.27, 0.92, 0.44])
#cbar_ax = fig.add_axes([0.06, 0.17, 0.90, 0.04])

# plot
cb1 = plt.colorbar(sc1,orientation='horizontal',cax=cbar_ax)

if to_plot == 'CO':
    cb1.set_label('CO, ppb')
elif to_plot == 'N2O':
    cb1.set_label('$N_2O$, ppb')
    
#fig.savefig('COMA_transit.png',dpi=300)
