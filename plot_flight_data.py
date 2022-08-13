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
from datetime import datetime
import matplotlib.dates as mdates

from load_flight_functions import V_to_T
from load_flight_functions import read_COMA
from load_flight_functions import read_MMS

# EDIT THESE
case = '2022-08-13'
focus = 'flight_N2O' # lab, flight_CO, flight_N2O

if case == '2021-08-06': # FCF
    filename_COMA = ['../Data/2021-08-06/n2o-co_2021-08-06_f0002.txt']
    filename_MMS = '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20210806_RA.ict'
    filename_WB57 = '../Data/_OtherData_/NP_WB57_20210806_R0.ict'
    cur_day = datetime(2021,8,6)
elif case == '2021-08-10': # Test Flight 1
    filename_COMA = ['../Data/2021-08-10/n2o-co_2021-08-10_f0003.txt']
    filename_MMS = '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20210810_RA.ict'
    filename_WB57 = '../Data/_OtherData_/NP_WB57_20210810_R0.ict'
    cur_day = datetime(2021,8,10)
elif case == '2021-08-16': # Test Flight 2
    filename_COMA = ['../Data/2021-08-16/n2o-co_2021-08-16_f0002.txt']
    filename_MMS = '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20210816_RA.ict'
    filename_WB57 = '../Data/_OtherData_/NP_WB57_20210816_R0.ict'
    cur_day = datetime(2021,8,16)
elif case == '2021-08-17': # Test Flight 3
    filename_COMA = ['../Data/2021-08-17/n2o-co_2021-08-17_f0002.txt']
    filename_MMS = '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20210817_RA.ict'
    filename_WB57 = '../Data/_OtherData_/NP_WB57_20210817_R0.ict'
    cur_day = datetime(2021,8,17)
elif case == '2021-08-17': # lab breathing air
    #filename_COMA = '../Data/2021-08-06/n2o-co_2021-08-06_f0000.txt' # chop 3am part
    #filename_COMA = '../Data/2021-08-10/n2o-co_2021-08-10_f0000.txt'
    #filename_COMA = '../Data/2021-08-16/n2o-co_2021-08-16_f0000.txt'
    filename_COMA = ['../Data/2021-08-17/n2o-co_2021-08-17_f0000.txt']
elif case == '2022-05-20':
    filename_COMA = ['../Data/2022-05-20/n2o-co_2022-05-20_f0000.txt']
elif case == '2022-07-14': # FCF Houston integration 2022
    filename_COMA = ['../Data/2022-07-14/n2o-co_2022-07-14_f0002.txt']
elif case == '2022-07-16': # science flight 1 Houston
    filename_COMA = ['../Data/2022-07-16/n2o-co_2022-07-16_f0002.txt']
elif case == '2022-07-18': # science flight 2 Houston
    filename_COMA = ['../Data/2022-07-18/n2o-co_2022-07-18_f0002.txt',
                     '../Data/2022-07-18/n2o-co_2022-07-18_f0003.txt']
    filename_MMS = '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20220718_RA.ict'
    cur_day = datetime(2022,7,18)
elif case == '2022-07-21-A': # Ellington to Seattle
    filename_COMA = ['../Data/2022-07-21/n2o-co_2022-07-21_f0000.txt',
                     '../Data/2022-07-21/n2o-co_2022-07-21_f0001.txt']
    filename_MMS = '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20220721_RA_1.ict'
    cur_day = datetime(2022,7,21)
elif case == '2022-07-21-B': # Seattle to Anchorage
    filename_COMA = ['../Data/2022-07-21/n2o-co_2022-07-21_f0002.txt']
    filename_MMS = '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20220721_RA_2.ict'
    cur_day = datetime(2022,7,21)
elif case == '2022-07-24': # Anchorage to Adak
    filename_COMA = ['../Data/2022-07-24/n2o-co_2022-07-24_f0000.txt']
    filename_MMS = '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20220724_RA.ict'
    cur_day = datetime(2022,7,24)
elif case == '2022-07-25': # Adak to Misawa
    filename_COMA = ['../Data/2022-07-25/n2o-co_2022-07-25_f0000.txt']
    filename_MMS = '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20220725_RA.ict'
    cur_day = datetime(2022,7,25)
elif case == '2022-07-27': # Misawa to Osan
    filename_COMA = ['../Data/2022-07-27/n2o-co_2022-07-27_f0000.txt']
    filename_MMS = '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20220727_RA.ict'
    cur_day = datetime(2022,7,27)
elif case == '2022-08-02': # RF03
    filename_COMA = ['../Data/2022-08-02/n2o-co_2022-08-02_f0000.txt']
    filename_MMS = '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20220802_RA.ict'
    cur_day = datetime(2022,8,2)
elif case == '2022-08-04': # RF04
    filename_COMA = ['../Data/2022-08-04/n2o-co_2022-08-04_f0000.txt']
    filename_MMS = '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20220804_RA.ict'
    cur_day = datetime(2022,8,4)
elif case == '2022-08-06': # RF05
    filename_COMA = ['../Data/2022-08-06/n2o-co_2022-08-06_f0000_no_10s_cal.txt']
    filename_MMS = '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20220806_RA.ict'
    cur_day = datetime(2022,8,6)
elif case == '2022-08-12': # RF06
    filename_COMA = ['../Data/2022-08-12/n2o-co_2022-08-12_f0000.txt']
    filename_MMS = '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20220812_RA.ict'
    cur_day = datetime(2022,8,12)
elif case == '2022-08-13': # RF07
    filename_COMA = ['../Data/2022-08-13/n2o-co_2022-08-13_f0000.txt']
    filename_MMS = '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20220813_RA.ict'
    cur_day = datetime(2022,8,13)
    
# %% data
# read COMA data, combining multiple files if needed
COMA = read_COMA(filename_COMA)

# index MIU valves
#ix_8 = np.ravel(np.where( (LGR["      MIU_VALVE"]==8) & (LGR["      GasP_torr"]>52.45) & (LGR["      GasP_torr"]<52.65)) ) # Inlet
ix_8 = np.ravel(np.where(COMA["      MIU_VALVE"]==8)) # inlet
ix_7 = np.ravel(np.where(COMA["      MIU_VALVE"]==7)) # inlet (lab)
ix_3 = np.ravel(np.where(COMA["      MIU_VALVE"]==3)) # high cal
ix_2 = np.ravel(np.where(COMA["      MIU_VALVE"]==2)) # low cal
ix_1 = np.ravel(np.where(COMA["      MIU_VALVE"]==1)) # flush

# %% plot data
plt.rc('axes', labelsize=6) # xaxis and yaxis labels
plt.rc('xtick', labelsize=6) # xtick labels
plt.rc('ytick', labelsize=6) # ytick labels
fig, ax = plt.subplots(3, 4, figsize=(9,3.5),dpi=200,sharex=True)

# choose index
#ix = ix_8
#ix = LGR_time.index
#ix = np.concatenate((ix_2,ix_3))

# 1. CO
ax[0,0].plot(COMA['time'][ix_8],COMA["      [CO]d_ppm"][ix_8]*1000,'b.',markersize=2)
ax[0,0].plot(COMA['time'][ix_2],COMA["      [CO]d_ppm"][ix_2]*1000,'y.',markersize=2)
ax[0,0].plot(COMA['time'][ix_3],COMA["      [CO]d_ppm"][ix_3]*1000,'m.',markersize=2)
ax[0,0].set_ylabel('CO (dry), ppbv')
ax[0,0].set_ylim(0,200)

# 2. N2O
ax[1,0].plot(COMA['time'][ix_8],COMA["     [N2O]d_ppm"][ix_8]*1000,'b.',markersize=2)
ax[1,0].plot(COMA['time'][ix_2],COMA["     [N2O]d_ppm"][ix_2]*1000,'y.',markersize=2)
ax[1,0].plot(COMA['time'][ix_3],COMA["     [N2O]d_ppm"][ix_3]*1000,'m.',markersize=2)
ax[1,0].set_ylim(0,200)
ax[1,0].set_ylabel('$\mathregular{N_2O (dry), ppbv}$')
ax[1,0].set_ylim(200,350)

# 3. H2O
ax[2,0].plot(COMA['time'],COMA["      [H2O]_ppm"],'k.',markersize=2)
ax[2,0].set_ylabel('$\mathregular{H_2O, ppmv}$')
ax[2,0].set_yscale('log')

# 4. laser temperature
laserT = V_to_T(COMA["           AIN6"])
ax[0,1].plot(COMA['time'],laserT,'k.',markersize=2) # laser temp
ax[0,1].set_ylabel('Laser T, C')

# 5. supercool temperature
supercoolT = V_to_T(COMA["           AIN5"])
ax[1,1].plot(COMA['time'],supercoolT,'k.',markersize=2)
ax[1,1].set_ylabel('Supercool T, C')

# 6. laser control voltage
ax[2,1].plot(COMA['time'],COMA["         LTC0_v"],'k.',markersize=2)
ax[2,1].set_ylabel('LTC0_v')

# 7. Peak0
ax[0,2].plot(COMA['time'],COMA["          Peak0"],'k.',markersize=2)
ax[0,2].set_ylabel('Peak0')
ax[0,2].set_ylim(790,820)

# 8. line centers
ax[1,2].plot(COMA['time'],COMA["  12COa_0000_CT"],'k.',markersize=2)
ax[1,2].set_ylim(-11,-9.5)
ax[1,2].set_ylabel('12COa_0000_CT')

# 9. gas and ambient temperatures
ax[2,2].plot(COMA['time'],COMA["         GasT_C"],'-',markersize=2)
ax[2,2].plot(COMA['time'],COMA["         AmbT_C"],'-',markersize=2)
ax[2,2].legend(['Gas_T','Amb_T'],edgecolor='none',facecolor='none',fontsize='xx-small')
ax[2,2].set_ylabel('Temperatures, C')

# 10. cell pressure
ax[0,3].plot(COMA['time'][ix_8],COMA["      GasP_torr"][ix_8],'b.',markersize=2)
ax[0,3].plot(COMA['time'][ix_2],COMA["      GasP_torr"][ix_2],'y.',markersize=2)
ax[0,3].plot(COMA['time'][ix_3],COMA["      GasP_torr"][ix_3],'m.',markersize=2)
ax[0,3].plot(COMA['time'][ix_1],COMA["      GasP_torr"][ix_1],'g.',markersize=2)
#x[0,3].plot(COMA['time'],COMA["      GasP_torr"],'k.',markersize=2)
ax[0,3].set_ylabel('$\mathregular{Gas P, torr}$')

# 11. Gnd
ax[1,3].plot(COMA['time'],COMA["            Gnd"],'k.',markersize=2)
ax[1,3].set_ylabel('Gnd')

# 12. chi-squared
ax[2,3].plot(COMA['time'],COMA["         CHISQ0"],'k.',markersize=2)
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
    
    fig2, ax2 = plt.subplots(1, 2, figsize=(6,3),dpi=200)
    
    df_lowcal = pd.DataFrame({'time': COMA['time'][ix_2],
                              'CO_dry': COMA["      [CO]d_ppm"][ix_2]*1000,
                              'N2O_dry': COMA["     [N2O]d_ppm"][ix_2]*1000,
                              'H2O': COMA["      [H2O]_ppm"][ix_2]})
    df_lowcal['groups'] = (df_lowcal.index.to_series().diff()>5).cumsum()
    df_highcal = pd.DataFrame({'time': COMA['time'][ix_3],
                               'CO_dry': COMA["      [CO]d_ppm"][ix_3]*1000,
                               'N2O_dry': COMA["     [N2O]d_ppm"][ix_3]*1000,
                               'H2O': COMA["      [H2O]_ppm"][ix_3]})
    df_highcal['groups'] = (df_highcal.index.to_series().diff()>5).cumsum()
    #df_flush = pd.DataFrame({'time': LGR_time[ix_1], 'CO_dry': LGR["      [CO]d_ppm"][ix_1]*1000})
    #df_flush['groups'] = (df_flush.index.to_series().diff()>5).cumsum()
    
    if focus == 'flight_CO':
        for ct, data in df_lowcal.groupby('groups'):
            ax2[0].plot(data['CO_dry'].values,'.')
            
        for ct, data in df_highcal.groupby('groups'):
            ax2[1].plot(data['CO_dry'].values,'.')
        
        if cur_day <= datetime(2022,8,11): # NOAA gas bottle
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
        
        if cur_day <= datetime(2022,8,11): # NOAA gas bottle
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
    MMS = read_MMS(filename_MMS,cur_day)
    MMS_sync = MMS.groupby(pd.Grouper(key="time", freq="1s")).mean()
    
    # handle COMA data
    indices = ix_8 # use only inlet data
    #indices = np.union1d(ix_1,ix_8) # use both inlet and flush data here
    COMA_df = pd.DataFrame({'time': COMA['time'][indices], 'CO_dry': COMA["      [CO]d_ppm"][indices]*1000, 
                            'N2O_dry': COMA["     [N2O]d_ppm"][indices]*1000, 'amb_T': COMA["         AmbT_C"]})
    COMA_df_sync = COMA_df.groupby(pd.Grouper(key="time", freq="1s")).mean()
    
    # time-sync the data with COMA
    sync_data = pd.merge(MMS_sync, COMA_df_sync, how='inner', on=['time'])

    # %% altitude vs time scatterplot
    fig3, ax3 = plt.subplots(1, 1, figsize=(6,3.5),dpi=200)
    #ax3[0].scatter(sync_data.index,sync_data['alt'],c=sync_data['CO_dry'],vmin=20, vmax=80, s = 15)
    ax3.scatter(sync_data.index,sync_data['ALT'],c=sync_data.index, s = 15)
    ax3.grid()
    ax3.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax3.set_xlabel('Time (UTC)')
    ax3.set_ylabel('Altitude, m')
    
    # %% lat/lon map (colored by time)
    fig4 = plt.figure(4)
    if case in [11,12]: # Transit 3-4
        projection = ccrs.Mercator(central_longitude=180)
    else:  # Transit 1-2 and 5 (and default)
        projection = ccrs.Mercator() 
            
    ax4 = plt.axes(projection = projection)
    ax4.add_feature(cf.COASTLINE)
    ax4.add_feature(cf.BORDERS)

    plate = ccrs.PlateCarree()
    
    sc1 = ax4.scatter(sync_data['LON'].values,sync_data['LAT'].values,c=sync_data.index, s = 15, transform=plate)
    
    if case == '2022-07-21-A':
        ax4.set_extent([-125, -90, 23, 53], crs=plate) # Transit 1
    elif case == '2022-07-21-B':
        ax4.set_extent([-155, -115, 40, 65], crs=plate) # Transit 2
    elif case == '2022-07-24':
        ax4.set_extent([170, 220, 40, 65], crs=plate) # Transit 3 (trick for international date line)
    elif case == '2022-07-25':
        ax4.set_extent([130, 190, 30, 65], crs=plate) # Transit 4 (trick for international date line)
    elif case == '2022-07-27':
        ax4.set_extent([122, 144, 30, 45], crs=plate) # Transit 5
    elif case == '2022-08-02':
        ax4.set_extent([110, 145, 15, 44], crs=plate) # RF03 (first flight Osan)
    
    cb1 = plt.colorbar(sc1)
    cb1.ax.set_yticklabels(pd.to_datetime(cb1.get_ticks()).strftime(date_format='%H:%M'))
    cb1.set_label('Time, UTC', fontsize=10)
    cb1.ax.tick_params(labelsize=10)
    fig4.tight_layout()
    
    # %% vertical profile
    fig5, ax5 = plt.subplots(1, figsize=(5,4),dpi=200)
    
    if focus == 'flight_CO':
            sc2 = plt.scatter(sync_data['CO_dry'],sync_data['ALT'],c=sync_data.index,s=8)
            plt.xlim(15,200)
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