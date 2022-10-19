# -*- coding: utf-8 -*-
"""
Calculate linear calibration based on the cal cycles
Show results across multiple days, colored before flight; in-flight; post-flight (or by altitude, gas temperature, etc. to check for dependencies)

Handles tank values from original NOAA tanks; and newer Matheson gas values

"""

# %% load libraries and data
import numpy as np
import pandas as pd
import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
from calculate_linear_cal_fun import calc_cal
from load_data_functions import read_COMA
from load_data_functions import return_filenames
from load_data_functions import read_MMS_ict

# set font size
plt.rcParams['axes.labelsize'] = 8
plt.rcParams['legend.fontsize'] = 8
plt.rcParams['xtick.labelsize'] = 7
plt.rcParams['ytick.labelsize'] = 7
plt.rcParams.update({'mathtext.default': 'regular' } ) # not italics

cases = ['FCF_2021','TF1_2021','TF2_2021','TF3_2021','EEL_2022_Day1','EEL_2022_Day2',
         'RF02','Transit1','Transit2','Transit3','Transit4','Transit5',
         'RF03_lab','RF03','RF04_lab','RF04','RF05_lab','RF05','RF06_lab','RF06','RF07_lab','RF07',
         'RF08_lab','RF08','RF09_lab','RF09','RF10_lab','RF10','RF11_lab','RF11','RF12_lab','RF12',
         'RF13_lab','RF13','RF14_lab','RF14','RF15_lab','RF15','RF16_lab','RF16','RF17_lab','RF17',
         'Transit6','Transit7','Transit8','Transit9']

#cases = ['RF13']

header = "Case,Cycle#,ID,CO_val,CO_std,N2O_val,N2O_std,H2O,CellP,CellP_std,Alt,Time_on,Power,Peak0"
a = open('plots/table_low_cal.csv', 'w')
a.write(header)
a.write('\n')
b = open('plots/table_high_cal.csv', 'w')    
b.write(header)
b.write('\n')

# %% main loop
for case in cases:
    # %% define cases
    print('Processing case:' + case)
    
    filenames = {'COMA_raw':[],'MMS':[]}
    
    if case == 'RF03_lab':
        filenames['COMA_raw'] = ['../Data/2022-08-02/n2o-co_2022-08-02_f0001.txt'] #post-flight
        
    elif case == 'RF04_lab':
        filenames['COMA_raw'] = ['../Data/2022-08-04/n2o-co_2022-08-04_f0001.txt'] #post-flight
        
    elif case == 'RF05_lab':
        filenames['COMA_raw'] = ['../Data/2022-08-05/n2o-co_2022-08-05_f0000_no_10s_cal.txt', #pre-flight
                                 '../Data/2022-08-06/n2o-co_2022-08-06_f0001.txt'] # post-flight
    
    elif case == 'RF06_lab':
        filenames['COMA_raw'] = ['../Data/2022-08-11/n2o-co_2022-08-11_f0001.txt'] # pre-flight
        
    elif case == 'RF07_lab':
        filenames['COMA_raw'] = ['../Data/2022-08-12/n2o-co_2022-08-12_f0002.txt', # pre-flight
                                 '../Data/2022-08-13/n2o-co_2022-08-13_f0001.txt']  # post-flight
        
    elif case == 'RF08_lab':
        filenames['COMA_raw'] = ['../Data/2022-08-15/n2o-co_2022-08-15_f0002.txt'] # post-flight
    
    elif case == 'RF09_lab':
        filenames['COMA_raw'] = ['../Data/2022-08-15/n2o-co_2022-08-15_f0003.txt', # pre-flight
                                 '../Data/2022-08-16/n2o-co_2022-08-16_f0001.txt'] # post-flight
    
    elif case == 'RF10_lab':
        filenames['COMA_raw'] = ['../Data/2022-08-19/n2o-co_2022-08-19_f0000.txt'] # post-flight
    
    elif case == 'RF11_lab':
        filenames['COMA_raw'] = ['../Data/2022-08-20/n2o-co_2022-08-20_f0000.txt', # pre-flight
                                 '../Data/2022-08-21/n2o-co_2022-08-21_f0001.txt'] # post-flight
    
    elif case == 'RF12_lab':
        filenames['COMA_raw'] = ['../Data/2022-08-22/n2o-co_2022-08-22_f0000.txt', # pre-flight
                                 '../Data/2022-08-23/n2o-co_2022-08-23_f0001.txt']  # post-flight
      
    elif case == 'RF13_lab':
        filenames['COMA_raw'] = ['../Data/2022-08-25/n2o-co_2022-08-25_f0000.txt'] # post-flight
        
    elif case == 'RF14_lab':
        filenames['COMA_raw'] = ['../Data/2022-08-26/n2o-co_2022-08-26_f0001.txt'] # post-flight
    
    elif case == 'RF15_lab':
        filenames['COMA_raw'] = ['../Data/2022-08-28/n2o-co_2022-08-28_f0000.txt', # pre-flight
                                 '../Data/2022-08-29/n2o-co_2022-08-29_f0001.txt'] # post-flight
    
    elif case == 'RF16_lab':
        filenames['COMA_raw'] = ['../Data/2022-08-30/n2o-co_2022-08-30_f0000.txt', # pre-flight
                                 '../Data/2022-08-31/n2o-co_2022-08-31_f0001.txt'] # post-flight
        
    elif case == 'RF17_lab':
        filenames['COMA_raw'] = ['../Data/2022-08-31/n2o-co_2022-08-31_f0002.txt', # pre-flight
                                 '../Data/2022-09-01/n2o-co_2022-09-01_f0001.txt'] # post-flight
        
    else:
        filenames = return_filenames(case)
    
    # unused:
    #2022-08-18lab
    #2022-08-24_f0000
    #n2o-co_2022-09-01_f0002
    
    #'FCF_2021':        2021-08-06_f0002
    #'TF1_2021':        2021-08-10_f0003
    #'TF2_2021':        2021-08-16_f0002
    #'TF3_2021':        2021-08-17_f0002
    #'EEL_2022_Day1':   2022-05-19_f0000
    #'EEL_2022_Day2':   2022-05-20_f0000
    #'RF02':            2022-07-18_f0002, 2022-07-18_f0003
    #'Transit1':        2022-07-21_f0000, 2022-07-21_f0001 (Ellington to Seattle)
    #'Transit2':        2022-07-21_f0002 (Seattle to Anchorage)
    #'Transit3':        2022-07-24_f0000 (Anchorage to Adak)
    #'Transit4':        2022-07-25_f0000 (Adak to Misawa)
    #'Transit5':        2022-07-27_f0000 (Misawa to Osan)
    #'RF03':            2022-08-02_f0000
    #'RF04':            2022-08-04_f0000
    #'RF05':            2022-08-06_f0000_no_10s_cal
    #'RF06':            2022-08-12_f0000
    #'RF07':            2022-08-13_f0000
    #'RF08':            2022-08-15_f0000, 2022-08-15_f0001
    #'RF09':            2022-08-16_f0000
    #'RF10':            2022-08-18_f0000
    #'RF11':            2022-08-21_f0000
    #'RF12':            2022-08-23_f0000
    #'RF13':            2022-08-24_f0002
    #'RF14':            2022-08-26_f0000
    #'RF15':            2022-08-29_f0000
    #'RF16':            2022-08-31_f0000
    #'RF17':            2022-09-01_f0000
    #'Transit6':        2022-09-09_f0000 (Osan to Misawa)
    #'Transit7':        2022-09-12_f0000 (Misawa to Adak)
    #'Transit8':        2022-09-13_f0000 (Adak to Seattle)
    #'Transit9':        2022-09-14_f0000 (Seattle to Houston)
    
    # %% load COMA data
    COMA, inlet_ix = read_COMA(filenames['COMA_raw'])

    if case == 'RF13': # fix clock setting on this day
        COMA['time'] = COMA['time'] + timedelta(hours=6)
    
    # %% define cal gas cylinders
    start_time = COMA['time'][0]
    
    if start_time <= datetime.datetime(2022,8,11): # NOAA gas bottle
        cylinder = 'NOAA'
        
        #NOAA low (CC745344)
        #NOAA high (CC746190)
        #https://gml.noaa.gov/ccl/refgas.html
        low_tank_CO = 51.30 # 51.30 +/- 0.66
        high_tank_CO = 163.11 # 163.11 +/- 0.92
        low_tank_N2O = 265.90 # 265.90 +/- 0.04
        high_tank_N2O = 348.05 # 348.05 +/- 0.04
    else:
        cylinder = 'Matheson'
        
        #Matheson low: ~200 ppb CO and N2O
        #Matheson high: ~1000 ppb CO and N2O
        low_tank_CO = 200
        high_tank_CO = 1000
        low_tank_N2O = 200
        high_tank_N2O = 1000
        
    # %% calc data
    ix_low = np.ravel(np.where(COMA["MIU_VALVE"]==2)) # low cal
    ix_high = np.ravel(np.where(COMA["MIU_VALVE"]==3)) # high cal
    
    low_cal = calc_cal(COMA,ix_low)
    high_cal = calc_cal(COMA,ix_high)
    
    df_lowcal = pd.DataFrame({'time': COMA['time'][ix_low],
                              'CO_dry': COMA["[CO]d_ppm"][ix_low]*1000,
                              'N2O_dry': COMA["[N2O]d_ppm"][ix_low]*1000,
                              'H2O': COMA["[H2O]_ppm"][ix_low],
                              'GasP_torr': COMA['GasP_torr'][ix_low]})
    df_lowcal['groups'] = (df_lowcal.index.to_series().diff()>5).cumsum()
    
    df_highcal = pd.DataFrame({'time': COMA['time'][ix_high],
                               'CO_dry': COMA["[CO]d_ppm"][ix_high]*1000,
                               'N2O_dry': COMA["[N2O]d_ppm"][ix_high]*1000,
                               'H2O': COMA["[H2O]_ppm"][ix_high],
                               'GasP_torr': COMA['GasP_torr'][ix_high]})
    df_highcal['groups'] = (df_highcal.index.to_series().diff()>5).cumsum()
    
    low_cal['ID'] = [pd.to_datetime(tmp).strftime("%Y-%m-%d %H:%M:%S") for tmp in low_cal['time']]
    high_cal['ID'] = [pd.to_datetime(tmp).strftime("%Y-%m-%d %H:%M:%S") for tmp in high_cal['time']]
    
    # %% load MMS data
    if (len(filenames['MMS']) > 0):
        MMS = read_MMS_ict(filenames['MMS'])
        
        # match by time (add 35 s since time represents start of cal cycle)
        low_cal['alt'] = np.nan
        for index, row in low_cal.iterrows():
            time_distance = np.abs( MMS['time'] - (row['time']+np.timedelta64(35, 's')) )
            match_ix = np.argmin(time_distance)
            if time_distance[match_ix] < np.timedelta64(5, 's'):
                low_cal.loc[index,'alt'] = MMS.loc[match_ix,'ALT']
        
        high_cal['alt'] = np.nan
        for index, row in high_cal.iterrows():
            time_distance = np.abs( MMS['time'] - (row['time']+np.timedelta64(35, 's')) )
            match_ix = np.argmin(time_distance)
            if time_distance[match_ix] < np.timedelta64(5, 's'):
                high_cal.loc[index,'alt'] = MMS.loc[match_ix,'ALT']
        
    else:
        low_cal['alt']=0
        high_cal['alt']=0
    
    # %% load laser power
    # replace f with s in filenames
    f = lambda x: (x[0:42].replace("f", "s")+".txt") # handle no_10s_cal cropped cases
    spectra_fnames = map(f, filenames['COMA_raw'])
    
    # load spectra files and calculate laser power
    for count, fname in enumerate(spectra_fnames):
        print("Calculating laser power:")
        f = open(fname, "r")
        txt = f.read()
        f.close()
        spectra = txt.splitlines()
        
        block_length = 1126
        num_lines = int(len(spectra)/block_length)
        
        laser_power = np.zeros(num_lines)
    
        EPOCH_TIME = [int(spectra[4+x*1126][11:]) for x in range(num_lines)]
        x0 = datetime.datetime(1970,1,1)
        SPECTRA_TIME = [x0+timedelta(seconds=t/1000) for t in EPOCH_TIME]
        
        if case == 'RF13': # fix clock setting on this day
            SPECTRA_TIME = [x + timedelta(hours=6) for x in SPECTRA_TIME]
            
        for ii in range(num_lines):
            # select the laser scan (LR0)
            x0 = 180+ii*1126
            x1 = 1123+ii*1126
            raw_scan = np.ravel([float(x) for x in spectra[x0:x1]])
            
            # select the ringdown scan (RD0)
            x0 = 17+ii*1126
            x1 = 176+ii*1126
            ringdown = np.ravel([float(x) for x in spectra[x0:x1]])
            
            # calculate laser power
            laser_power[ii] = np.mean(raw_scan[-11:-1]) - np.mean(ringdown[-11:-1])

        if count == 0:
            laser_power_df = pd.DataFrame({'time':SPECTRA_TIME,'power':laser_power})
        else:
            tmp = pd.DataFrame({'time':SPECTRA_TIME,'power':laser_power})
            laser_power_df = pd.concat([laser_power_df,tmp],ignore_index=True)
    
        # match by time (add 35 s since time represents start of cal cycle)
        low_cal['power'] = np.nan
        for index, row in low_cal.iterrows():
            time_distance = np.abs( laser_power_df['time'] - (row['time']+np.timedelta64(35, 's')) )
            match_ix = np.argmin(time_distance)
            if time_distance[match_ix] < np.timedelta64(5, 's'):
                low_cal.loc[index,'power'] = laser_power_df.loc[match_ix,'power']
        
        high_cal['power'] = np.nan
        for index, row in high_cal.iterrows():
            time_distance = np.abs( laser_power_df['time'] - (row['time']+np.timedelta64(35, 's')) )
            match_ix = np.argmin(time_distance)
            if time_distance[match_ix] < np.timedelta64(5, 's'):
                high_cal.loc[index,'power'] = laser_power_df.loc[match_ix,'power']
        
    # %% plot time series (cal cycles overlapped)
    fig2, ax2 = plt.subplots(3, 2, figsize=(6,5))
    
    ms = 4
    
    for ct, data in df_lowcal.groupby('groups'):
        ax2[0,0].plot(data['CO_dry'].values,'-.',markersize=ms,alpha=0.6)
        ax2[1,0].plot(data['N2O_dry'].values,'-.',markersize=ms,alpha=0.6)
        ax2[2,0].plot(data['GasP_torr'].values,'-.',markersize=ms,alpha=0.6)
    
    for ct, data in df_highcal.groupby('groups'):
        ax2[0,1].plot(data['CO_dry'].values,'-.',markersize=ms,alpha=0.6)
        ax2[1,1].plot(data['N2O_dry'].values,'-.',markersize=ms,alpha=0.6)
        ax2[2,1].plot(data['GasP_torr'].values,'-.',markersize=ms,alpha=0.6)
    
    # NOAA gas bottle
    if cylinder == 'NOAA':
        ax2[0,0].set_ylim(0,200)
        ax2[0,1].set_ylim(20,220)
        ax2[1,0].set_ylim(220,360)
        ax2[1,1].set_ylim(220,360)
    else:
        # Matheson gas bottle
        ax2[0,0].set_ylim(170,220)
        ax2[0,1].set_ylim(500,1000)
        ax2[1,0].set_ylim(150,400)
        ax2[1,1].set_ylim(500,1000)
    
    ax2[0,0].set_ylabel('CO, ppb')
    ax2[0,0].grid()
    ax2[0,1].grid()
    
    ax2[1,0].set_ylabel('N2O, ppb')
    ax2[1,0].grid()
    ax2[1,1].grid()
    
    ax2[2,0].set_ylabel('Cell pressure, torr')
    ax2[2,0].grid()
    ax2[2,1].grid()
    
    ax2[2,0].set_xlabel('Seconds')
    ax2[2,1].set_xlabel('Seconds')
    ax2[0,0].set_title('Low cal')
    ax2[0,1].set_title('High cal')
    
    fig2.suptitle(t=case,x=0.15,y=0.98)
    fig2.tight_layout()
    
    ax2[0,1].legend(np.linspace(0,12,13,dtype='int'),ncol=2,bbox_to_anchor=(0, 1.6)) #framealpha=0
    
    fig2.savefig('plots/fig_'+case+'.png',dpi=300)
    #fig2.savefig('plots/fig_'+case+'.svg')
    plt.close(fig2)
    
    
    # %% output stats    
    for to_calc in [0,1]:
        if to_calc == 0:
            dat = low_cal
            file_handle = a
        else:
            dat = high_cal
            file_handle = b
        
        for ii in range(len(dat)):
            file_handle.write(
                case + ','                                        # Case name
                "{:2d}".format(ii) + ','                          #Cycle#
                '  ' + dat['ID'][ii] + ','                        #Unique identifier
                '  ' + "{:6.2f}".format(dat['CO_val'][ii]) + ','  #CO value
                '  ' + "{:6.2f}".format(dat['CO_std'][ii]) + ','  #CO std dev
                '  ' + "{:6.2f}".format(dat['N2O_val'][ii]) + ',' #N2O value
                '  ' + "{:6.2f}".format(dat['N2O_std'][ii]) + ',' #N2O std dev
                '  ' + "{:6.2f}".format(dat['H2O'][ii]) + ','     #H2O value
                '  ' + "{:5.2f}".format(dat['GasP_val'][ii]) + ','  #Cell pressure
                '  ' + "{:5.3f}".format(dat['GasP_std'][ii]) + ','  #Cell pressure std dev
                '  ' + "{:6.0f}".format(dat['alt'][ii]) + ','    #Altitude
                '  ' + "{:6.0f}".format(dat['SpectraID'][ii]) + ','  #SpectraID / seconds on
                '  ' + "{:6.4f}".format(dat['power'][ii]) + ','  # Laser power
                '  ' + "{:6.2f}".format(dat['Peak0'][ii]))          #Peak position
            file_handle.write('\n')
    
# %% close files
a.close()
b.close()
