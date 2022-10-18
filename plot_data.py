# -*- coding: utf-8 -*-
"""
plot data after a WB-57 flight
Use COMA data files from instrument
MMS from data archive (https://www-air.larc.nasa.gov/cgi-bin/ArcView/acclip)
"""

# %% load libraries and files
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.dates as mdates

from load_data_functions import V_to_T
from load_data_functions import read_COMA
from load_data_functions import read_MMS_ict
from load_data_functions import return_filenames

# EDIT THESE
case = 'RF15'
focus = 'flight_CO' # lab, flight_CO, flight_N2O

# %% plot settings
plt.rcParams['axes.labelsize'] = 8
plt.rcParams['legend.fontsize'] = 8
plt.rcParams['xtick.labelsize'] = 7
plt.rcParams['ytick.labelsize'] = 7
plt.rcParams.update({'mathtext.default': 'regular' } ) # not italics

# %% data
# read COMA data, combining multiple files if needed
filenames = return_filenames(case)

COMA, inlet_ix = read_COMA(filenames['COMA_raw'])

if case == 'RF13': # fix clock setting on this day
    COMA['time'] = COMA['time'] + timedelta(hours=6)

# index MIU valves
ix_8 = np.ravel(np.where(COMA["MIU_VALVE"]==8)) # inlet
ix_7 = np.ravel(np.where(COMA["MIU_VALVE"]==7)) # inlet (lab)
ix_3 = np.ravel(np.where(COMA["MIU_VALVE"]==3)) # high cal
ix_2 = np.ravel(np.where(COMA["MIU_VALVE"]==2)) # low cal
ix_1 = np.ravel(np.where(COMA["MIU_VALVE"]==1)) # flush

# %% plot data
plt.rc('axes', labelsize=8) # xaxis and yaxis labels
plt.rc('xtick', labelsize=8) # xtick labels
plt.rc('ytick', labelsize=8) # ytick labels
fig, ax = plt.subplots(3, 4, figsize=(9,3.5),sharex=True)

# 1. CO
ax[0,0].plot(COMA['time'][ix_8],COMA["[CO]d_ppm"][ix_8]*1000,'b.',markersize=2)
ax[0,0].plot(COMA['time'][ix_2],COMA["[CO]d_ppm"][ix_2]*1000,'y.',markersize=2)
ax[0,0].plot(COMA['time'][ix_3],COMA["[CO]d_ppm"][ix_3]*1000,'m.',markersize=2)
ax[0,0].set_ylabel('CO (dry), ppbv')
ax[0,0].set_ylim(0,200)

# 2. N2O
ax[1,0].plot(COMA['time'][ix_8],COMA["[N2O]d_ppm"][ix_8]*1000,'b.',markersize=2)
ax[1,0].plot(COMA['time'][ix_2],COMA["[N2O]d_ppm"][ix_2]*1000,'y.',markersize=2)
ax[1,0].plot(COMA['time'][ix_3],COMA["[N2O]d_ppm"][ix_3]*1000,'m.',markersize=2)
ax[1,0].set_ylim(0,200)
ax[1,0].set_ylabel('$\mathregular{N_2O (dry), ppbv}$')
ax[1,0].set_ylim(200,350)

# 3. H2O
ax[2,0].plot(COMA['time'],COMA["[H2O]_ppm"],'k.',markersize=2)
ax[2,0].set_ylabel('$\mathregular{H_2O, ppmv}$')
ax[2,0].set_yscale('log')

# 4. laser temperature
laserT = V_to_T(COMA["AIN6"])
ax[0,1].plot(COMA['time'],laserT,'k.',markersize=2) # laser temp
ax[0,1].set_ylabel('Laser T, C')

# 5. supercool temperature
supercoolT = V_to_T(COMA["AIN5"])
ax[1,1].plot(COMA['time'],supercoolT,'k.',markersize=2)
ax[1,1].set_ylabel('Supercool T, C')

# 6. laser control voltage
ax[2,1].plot(COMA['time'],COMA["LTC0_v"],'k.',markersize=2)
ax[2,1].set_ylabel('LTC0_v')

# 7. Peak0
ax[0,2].plot(COMA['time'],COMA["Peak0"],'k.',markersize=2)
ax[0,2].set_ylabel('Peak0')
ax[0,2].set_ylim(790,820)

# 8. line centers
ax[1,2].plot(COMA['time'],COMA["12COa_0000_CT"],'k.',markersize=2)
ax[1,2].set_ylim(-11,-9.5)
ax[1,2].set_ylabel('12COa_0000_CT')

# 9. gas and ambient temperatures
ax[2,2].plot(COMA['time'],COMA["GasT_C"],'-',markersize=2)
ax[2,2].plot(COMA['time'],COMA["AmbT_C"],'-',markersize=2)
ax[2,2].legend(['Gas_T','Amb_T'],edgecolor='none',facecolor='none',fontsize='xx-small')
ax[2,2].set_ylabel('Temperatures, C')

# 10. cell pressure
ax[0,3].plot(COMA['time'][ix_8],COMA["GasP_torr"][ix_8],'b.',markersize=2)
ax[0,3].plot(COMA['time'][ix_2],COMA["GasP_torr"][ix_2],'y.',markersize=2)
ax[0,3].plot(COMA['time'][ix_3],COMA["GasP_torr"][ix_3],'m.',markersize=2)
ax[0,3].plot(COMA['time'][ix_1],COMA["GasP_torr"][ix_1],'g.',markersize=2)
#x[0,3].plot(COMA['time'],COMA["GasP_torr"],'k.',markersize=2)
ax[0,3].set_ylabel('$\mathregular{Gas P, torr}$')

# 11. Gnd
ax[1,3].plot(COMA['time'],COMA["Gnd"],'k.',markersize=2)
ax[1,3].set_ylabel('Gnd')

# 12. chi-squared
ax[2,3].plot(COMA['time'],COMA["CHISQ0"],'k.',markersize=2)
ax[2,3].set_ylabel('CHISQ0')
ax[2,3].set_yscale('log')

# formatting
plt.tight_layout()
ax[2,0].tick_params(axis='x', labelrotation = 45)
ax[2,1].tick_params(axis='x', labelrotation = 45)
ax[2,2].tick_params(axis='x', labelrotation = 45)
ax[2,3].tick_params(axis='x', labelrotation = 45)
ax[2,0].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.show()


# %% plot cal gas
if focus != 'lab':
    # each cycle only takes a fixed amount of time
    # therefore robust method is to check for large jumps in time (here > 5s) between occurences
    
    fig2, ax2 = plt.subplots(1, 2, figsize=(6,3))
    
    df_lowcal = pd.DataFrame({'time': COMA['time'][ix_2],
                              'CO_dry': COMA["[CO]d_ppm"][ix_2]*1000,
                              'N2O_dry': COMA["[N2O]d_ppm"][ix_2]*1000,
                              'H2O': COMA["[H2O]_ppm"][ix_2]})
    df_lowcal['groups'] = (df_lowcal.index.to_series().diff()>5).cumsum()
    df_highcal = pd.DataFrame({'time': COMA['time'][ix_3],
                               'CO_dry': COMA["[CO]d_ppm"][ix_3]*1000,
                               'N2O_dry': COMA["[N2O]d_ppm"][ix_3]*1000,
                               'H2O': COMA["[H2O]_ppm"][ix_3]})
    df_highcal['groups'] = (df_highcal.index.to_series().diff()>5).cumsum()
    #df_flush = pd.DataFrame({'time': LGR_time[ix_1], 'CO_dry': LGR["      [CO]d_ppm"][ix_1]*1000})
    #df_flush['groups'] = (df_flush.index.to_series().diff()>5).cumsum()
    
    start_time = COMA['time'][0]
    
    if focus == 'flight_CO':
        for ct, data in df_lowcal.groupby('groups'):
            ax2[0].plot(data['CO_dry'].values,'.')
            
        for ct, data in df_highcal.groupby('groups'):
            ax2[1].plot(data['CO_dry'].values,'.')
        
        if start_time <= datetime(2022,8,11): # NOAA gas bottle
            ax2[0].set_ylim(40,70)
            ax2[1].set_ylim(140,170)
        else:                              # Matheson gas bottle
            ax2[0].set_ylim(170,220)
            ax2[1].set_ylim(800,1000)
        ax2[0].set_ylabel('CO, ppb')  
        
    elif focus == 'flight_N2O':
        for ct, data in df_lowcal.groupby('groups'):
            ax2[0].plot(data['N2O_dry'].values,'.')
        
        for ct, data in df_highcal.groupby('groups'):
            ax2[1].plot(data['N2O_dry'].values,'.')
        
        if start_time <= datetime(2022,8,11): # NOAA gas bottle
            ax2[0].set_ylim(250,270)
            ax2[1].set_ylim(320,350)
        else:                              # Matheson gas bottle
            ax2[0].set_ylim(170,220)
            ax2[1].set_ylim(800,1000)
        ax2[0].set_ylabel('N2O, ppb')        
    
    elif focus == 'flight_H2O':
        for ct, data in df_lowcal.groupby('groups'):
            ax2[0].plot(data['H2O'].values,'.')
            #ax2[0].set_ylim(250,270)
            
        for ct, data in df_highcal.groupby('groups'):
            ax2[1].plot(data['H2O'].values,'.')
            #ax2[1].set_ylim(320,350)
        
        ax2[0].set_yscale('log')
        ax2[1].set_yscale('log')
        ax2[0].set_ylabel('H2O, ppb')        
    
    ax2[0].grid()
    ax2[1].grid()
    ax2[0].set_xlabel('Seconds')
    ax2[0].set_title('Low cal')
    ax2[1].set_xlabel('Seconds')
    ax2[1].set_title('High cal')
    ax2[1].legend(np.linspace(1,13,13,dtype='int'),fontsize=5)

# plots involving aicraft position
if focus != 'lab':
    # import mapping library
    import cartopy.crs as ccrs
    import cartopy.feature as cf
    
    # %% load MMS and WB57 data
    MMS = read_MMS_ict(filenames['MMS'])
    MMS_sync = MMS.groupby(pd.Grouper(key="time", freq="1s")).mean()
    
    # handle COMA data
    indices = inlet_ix # use only inlet data
    #indices = np.union1d(ix_1,ix_8) # use both inlet and flush data here
    COMA_df = pd.DataFrame({'time': COMA['time'][indices], 'CO_dry': COMA["[CO]d_ppm"][indices]*1000, 
                            'N2O_dry': COMA["[N2O]d_ppm"][indices]*1000, 'amb_T': COMA["AmbT_C"]})
    COMA_df_sync = COMA_df.groupby(pd.Grouper(key="time", freq="1s")).mean()
    
    # time-sync the data with COMA
    sync_data = pd.merge(MMS_sync, COMA_df_sync, how='inner', on=['time'])

    # %% altitude vs time scatterplot
    fig3, ax3 = plt.subplots(1, 1, figsize=(6,3.5))
    
    # OPTION 1: color by CO
    sc = ax3.scatter(sync_data.index,sync_data['ALT'],c=sync_data['CO_dry'],vmin=20, vmax=250, s = 15, cmap='rainbow') # color by CO
    cb = plt.colorbar(sc)
    cb.set_label('CO, ppb')
    
    # OPTION 2: color by time
    #ax3.scatter(sync_data.index,sync_data['ALT'],c=sync_data.index, s = 15)
    
    ax3.grid()
    ax3.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax3.set_xlabel('Time (UTC)')
    ax3.set_ylabel('Altitude, m')
    
    # %% lat/lon map (colored by time)
    fig4 = plt.figure(4)
    if case in ['Transit3','Transit4','Transit7','Transit8']: # Transit 3-4
        projection = ccrs.Mercator(central_longitude=180)
    else:  # Transit 1-2 and 5 (and default)
        projection = ccrs.Mercator() 
    
    ax4 = plt.axes(projection = projection)
    ax4.add_feature(cf.COASTLINE)
    ax4.add_feature(cf.BORDERS)
    plate = ccrs.PlateCarree()
    
    # OPTION 1: color by CO
    sc1 = ax4.scatter(sync_data['LON'].values,sync_data['LAT'].values,c=sync_data['CO_dry'], 
                      vmin=20, vmax=250, cmap='rainbow', s = 15, transform=plate)
    
    # OPTION 2: color by time
    #sc1 = ax4.scatter(sync_data['LON'].values,sync_data['LAT'].values,c=sync_data.index, s = 15, transform=plate)
    #cb1 = plt.colorbar(sc1)
    #cb1.ax.set_yticklabels(pd.to_datetime(cb1.get_ticks()).strftime(date_format='%H:%M'))
    #cb1.set_label('Time, UTC', fontsize=10)
    #cb1.ax.tick_params(labelsize=10)
    
    # handle transit flights
    if case == 'Transit1':
        ax4.set_extent([-125, -90, 23, 53], crs=plate) # Houston to Seattle
    elif case == 'Transit2':
        ax4.set_extent([-155, -115, 40, 65], crs=plate) # Seattle to Anchorage
    elif case == 'Transit3':
        ax4.set_extent([170, 220, 40, 65], crs=plate) # Anchorage to Adak (trick for international date line)
    elif case == 'Transit4':
        ax4.set_extent([130, 190, 30, 65], crs=plate) # Adak to Misawa (trick for international date line)
    elif case == 'Transit5':
        ax4.set_extent([122, 144, 30, 45], crs=plate) # Misawa to Osan
    elif case == 'RF03':
        ax4.set_extent([110, 145, 15, 44], crs=plate) # RF03 (first flight Osan)
    elif case == 'Transit6':
        ax4.set_extent([122, 144, 30, 45], crs=plate) # Osan to Misawa
    elif case == 'Transit7':
        ax4.set_extent([130, 190, 30, 65], crs=plate) # Misawa to Adak
    elif case == 'Transit8':
        ax4.set_extent([170, 245, 40, 65], crs=plate) # Adak to Seattle
    elif case == 'Transit9':
        ax4.set_extent([-125, -90, 23, 53], crs=plate) # Seattle to Houston
    fig4.tight_layout()
    
    # %% vertical profile
    fig5, ax5 = plt.subplots(1, figsize=(5,4))
    
    if focus == 'flight_CO':
            sc2 = plt.scatter(sync_data['CO_dry'],sync_data['ALT'],c=sync_data.index,s=8)
            plt.xlim(15,300)
            plt.xlabel('CO, ppb')
    elif focus == 'flight_N2O':
            sc2 = plt.scatter(sync_data['N2O_dry'],sync_data['ALT'],c=sync_data.index,s=8)
            plt.xlim(280,350)
            plt.xlabel('N2O, ppb')
    
    ax5.grid()
    cb2 = plt.colorbar(sc2)
    cb2.ax.set_yticklabels(pd.to_datetime(cb2.get_ticks()).strftime(date_format='%H:%M'))
    cb2.set_label('Time, UTC')
    plt.ylabel('Altitude, m')
    
# %% save all
"""
fig.savefig('fig1.png',dpi=300)
fig2.savefig('fig2_CO.png',dpi=300)
fig2.savefig('fig2_N2O.png',dpi=300)
fig3.savefig('fig3.png',dpi=300)
fig4.savefig('fig4.png',dpi=300)
fig5.savefig('fig5.png',dpi=300)
plt.close('all')
"""