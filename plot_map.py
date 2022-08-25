# -*- coding: utf-8 -*-
"""
Plot maps of 2021 test flights from Houston
"""

# %% header
from datetime import datetime
import matplotlib.pyplot as plt
from load_flight_functions import read_COMA
from load_flight_functions import read_MMS
from load_flight_functions import sync_data
import cartopy.crs as crs
import cartopy.feature as cfeature

# %% start cartopy map
fig = plt.figure(figsize=(8,6),dpi=200)

ax = fig.add_subplot(1,1,1, projection=crs.PlateCarree())

ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.STATES)

# %% process data
#for case in range(0, 4):
for case in ['RF10']:
    # load files
    if case == 0: # FCF
        filename_COMA = ['../Data/2021-08-06/n2o-co_2021-08-06_f0002.txt']
        filename_MMS = '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20210806_RA.ict'
        filename_WB57 = '../Data/_OtherData_/NP_WB57_20210806_R0.ict'
        cur_day = datetime(2021,8,6)
    elif case == 1: # Test Flight 1
        filename_COMA = ['../Data/2021-08-10/n2o-co_2021-08-10_f0003.txt']
        filename_MMS = '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20210810_RA.ict'
        filename_WB57 = '../Data/_OtherData_/NP_WB57_20210810_R0.ict'
        cur_day = datetime(2021,8,10)
    elif case == 2: # Test Flight 2
        filename_COMA = ['../Data/2021-08-16/n2o-co_2021-08-16_f0002.txt']
        filename_MMS = '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20210816_RA.ict'
        filename_WB57 = '../Data/_OtherData_/NP_WB57_20210816_R0.ict'
        cur_day = datetime(2021,8,16)
    elif case == 3: # Test Flight 3
        filename_COMA = ['../Data/2021-08-17/n2o-co_2021-08-17_f0002.txt']
        filename_MMS = '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20210817_RA.ict'
        filename_WB57 = '../Data/_OtherData_/NP_WB57_20210817_R0.ict'
        cur_day = datetime(2021,8,17)
    elif case == 'RF10': # RF10
        filename_COMA = ['../Data/2022-08-18/n2o-co_2022-08-18_f0000.txt']
        filename_MMS = '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20220819_RA.ict'


    COMA = read_COMA(filename_COMA)
    MMS = read_MMS(filename_MMS)
    synced_data = sync_data(MMS,COMA)

    # plot map
    #sc1 = ax.scatter(synced_data['LON'],synced_data['LAT'],c=synced_data['CO_dry'],vmin=20, vmax=80, s = 15)
    sc1 = ax.scatter(synced_data['LON'],synced_data['LAT'],c=synced_data['CO_dry'],vmin=30, vmax=250, s = 15)
    
    #sc2 = ax2.scatter(synced_data['LON'],synced_data['LAT'],c=synced_data['N2O_dry'],vmin=250, vmax=300, s = 15)

#fig.savefig('fig1.png',dpi=300)

# %% format
cb1 = plt.colorbar(sc1)
cb1.set_label('CO, ppb')
#ax.set_xlabel('Longitude')
#ax.set_ylabel('Latitude')
plt.show()