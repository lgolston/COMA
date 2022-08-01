# -*- coding: utf-8 -*-
"""
Plot COMA vertical profile vs GEOS model

Also look at: 'GEOS_AsianFF_CO(ppb)' and 'GEOS_NAmericanFF_CO(ppb)' components
"""

# %% header
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from load_flight_functions import read_COMA
from load_flight_functions import read_MMS
from load_flight_functions import sync_data

# %% process data
fig, ax = plt.subplots(1, 3, figsize=(8,3), dpi=100)

to_plot = 'CO_series' # CO_vert, CO_series, CO_GEOS, or N2O_vert

for case in range(1, 4):   
    # choose files
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
        filename_GEOS = '../Data/_OtherData_/GEOSFP_CO_ACCLIP-20210810.txt'
    elif case == 2: # Test Flight 2
        filename_COMA = ['../Data/2021-08-16/n2o-co_2021-08-16_f0002.txt']
        filename_MMS = '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20210816_RA.ict'
        filename_WB57 = '../Data/_OtherData_/NP_WB57_20210816_R0.ict'
        cur_day = datetime(2021,8,16)
        filename_GEOS = '../Data/_OtherData_/GEOSFP_CO_ACCLIP-20210816.txt'
    elif case == 3: # Test Flight 3
        filename_COMA = ['../Data/2021-08-17/n2o-co_2021-08-17_f0002.txt']
        filename_MMS = '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20210817_RA.ict'
        filename_WB57 = '../Data/_OtherData_/NP_WB57_20210817_R0.ict'
        cur_day = datetime(2021,8,17)
        filename_GEOS = '../Data/_OtherData_/GEOSFP_CO_ACCLIP-20210817.txt'
    
    # load files
    COMA = read_COMA(filename_COMA)
    MMS = read_MMS(filename_MMS,cur_day)
    synced_data = sync_data(MMS,COMA)
    if case == 0:
        GEOS = pd.DataFrame(data={'Time(UTC_Sec)': [np.nan], 'GEOS_CO(ppb)': [np.nan]})
    else:
        GEOS = pd.read_csv(filename_GEOS,sep='\s+',header=0)
        GEOS_time = [cur_day + timedelta(seconds=tmp) for tmp in GEOS['Time(UTC_Sec)']]
    
    # filter to peak position of 807 +/- 1
    # and not super volatile
    ix = np.ravel(np.where((synced_data['Peak0']>806) &
                           (synced_data['Peak0']<808) &
                           (synced_data['Peak0'].rolling(10,center=True).std() < 2)))
    
    # apply calibration factor
    # Flight 1: CO equation 1.086x + -2.576
    # Flight 2: CO equation 1.076x + -3.717
    # Flight 3: CO equation 1.082x + -2.309
    # Flight 1: N2O equation 1.151x + -5.404
    # Flight 2: N2O equation 1.099x + 6.333
    # Flight 3: N2O equation 1.094x + 7.937
    CO_cal = synced_data['CO_dry']*1.08 - 3
    
    # subplot with each of the 3x flights
    if to_plot == 'CO_vert':
        # CO vertical profile vs GEOS-FP
        sc = ax[case-1].scatter(CO_cal[ix],synced_data['ALT'][ix],c=synced_data.index[ix],s=4)
        ax[case-1].plot(GEOS['GEOS_CO(ppb)'],GEOS['Altitude(M)'],'k--')
        ax[case-1].set_xlim(0,100)
        ax[case-1].set_xlabel('CO, ppb')
        
        if case == 3:
            cbar = plt.colorbar(sc)
            cbar.set_label('Time, UTC')
            cbar.set_ticklabels([pd.to_datetime(t).strftime("%H:%M") for t in cbar.ax.get_yticks()])
            #cbar.ax.set_yticklabels(synced_data.index[ix].strftime("%H:%M"))
    
    elif to_plot == 'CO_series':
        # CO time series vs GEOS-FP
        ax[case-1].plot(synced_data.index,CO_cal,'b.')
        #ax[case-1].plot(synced_data.index[ix],CO_cal[ix],'y.')
        #ax[case-1].plot(synced_data.index,synced_data['ALT']/100,'k:')
        ax[case-1].plot(GEOS_time,GEOS['GEOS_CO(ppb)'],'k--')
        ax[case-1].set_ylim(0,200)
        ax[case-1].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        ax[case-1].set_xlabel('Time, UTC')
        ax[case-1].tick_params(axis='x', labelrotation = 45)
    elif to_plot == 'CO_GEOS':
        # CO time series
        ax[case-1].plot(GEOS_time,GEOS['GEOS_CO(ppb)'],'k')
        ax[case-1].plot(GEOS_time,GEOS['GEOS_AsianFF_CO(ppb)'],'k--')
        ax[case-1].plot(GEOS_time,GEOS['GEOS_NAmericanFF_CO(ppb)'],'k:')
        ax[case-1].set_ylim(0,200)
        ax[case-1].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        ax[case-1].set_xlabel('Time, UTC')
        ax[case-1].tick_params(axis='x', labelrotation = 45)
    else:
        # N2O vertical profile
        ax[case-1].scatter(synced_data['N2O_dry'][ix],synced_data['ALT'][ix],c=synced_data.index)
        ax[case-1].set_xlim(230,330)
        #ax[case-1].set_ylim(8000,20000)
        ax[case-1].set_xlabel('N2O, ppb')

# plot 2 formatting
if to_plot == 'CO_vert':
    ax[0].set_ylabel('Altitude, m')
elif to_plot == 'CO_series':
    ax[0].set_ylabel('CO, ppb')
elif to_plot == 'CO_GEOS':
    ax[0].set_ylabel('CO, ppb')
else:
    ax[0].set_ylabel('Altitude, m')
#ax[1].yaxis.set_ticklabels([])
#ax[2].yaxis.set_ticklabels([])
fig.tight_layout()

#plt.savefig('fig_output.png',dpi=300)
#plt.savefig('fig_output.png',dpi=300)
#plt.savefig('fig_output.png',dpi=300)
