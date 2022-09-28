# -*- coding: utf-8 -*-
"""
Load different file types ACCLIP:
- COMA (from analyzer)
- MMS (from NASA LaRC archive)
- IWG1 (from Mission Tools Suite)

# add return transit flights
"""

# %% load libraries
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# %% convert laser and supercool voltage to temperature [values from Ian]
def V_to_T(voltage):
    a = 1.1279*10**-3
    b = 2.3429*10**-4
    c = 8.7298*10**-8
    R = voltage/(100*10**-6) # 100 microAmp
    return 1/(a+b*np.log(R)+c*np.log(R)**3) - 273.15            

# %% read COMA/LGR data
def read_COMA(filename_COMA):
    """
   Function to read the COMA/LGR data
    """
    # read file, combining multiple if necessary
    for count, fname in enumerate(filename_COMA):
        if count == 0:
            COMA = pd.read_csv(filename_COMA[0],sep=',',header=1,skipinitialspace=True)
        else:
            COMA2 = pd.read_csv(fname,sep=',',header=1,skipinitialspace=True)
            COMA = pd.concat([COMA,COMA2],ignore_index=True)

    # parse timestamp
    COMA_time = COMA["Time"]
    COMA_time = [datetime.strptime(tstamp,"%m/%d/%Y %H:%M:%S.%f") for tstamp in COMA_time]
    COMA_time = pd.DataFrame(COMA_time)
    COMA_time = COMA_time[0]
    COMA['time'] = COMA_time
    
    # basic quality control
    #ix_8 = np.ravel(np.where( (LGR["      MIU_VALVE"]==8) & (LGR["      GasP_torr"]>52.45) & (LGR["      GasP_torr"]<52.65)) ) # Inlet
    #indices = np.union1d(ix_1,ix_8) # use both inlet and flush data here
    MIU = COMA["MIU_VALVE"]
    cellP = COMA["GasP_torr"]
    
    # handle purge air settings
    if COMA_time[0] <= datetime(2022,8,15):
        # use only inlet data
        inlet_ix = np.ravel( np.where((MIU==8) & (cellP>50)) )
    else:
        # starting 2022-08-16, MIU sequence no longer set to cycle through purge
        # account for this by excluding 20 s of data after the high cal
        inlet_ix = np.ravel( np.where((MIU==8) & (MIU.shift(30)==8) & (cellP>50)) )
    
    # return files
    return COMA, inlet_ix


# %% read MMS data
def read_MMS(filename):
    """
   Function to read the MMS data
    """
    
    # parse variables
    MMS = pd.read_csv(filename,sep=',',header=52)
    MMS_P = MMS[' P_MMS']*0.01 # static pressure (hPa)
    MMS_T = MMS[' T_MMS']*0.01 # static temperature (K)
    MMS_TAS = MMS[' TAS_MMS']*0.01 # platform true air speed (m/s)
    MMS_U = MMS[' U_MMS']*0.01
    MMS_V = MMS[' V_MMS']*0.01
    MMS_W = MMS[' W_MMS']*0.001
    MMS_TEDR = MMS[' TEDR_MMS']*0.01
    MMS_REYN = MMS[' REYN_MMS']*0.01
    MMS_LAT = MMS[' G_LAT_MMS']*0.00001
    MMS_LON = MMS[' G_LONG_MMS']*0.00001
    MMS_ALT = MMS[' G_ALT_MMS']*0.1
    MMS_POT = MMS[' POT_MMS']*0.01 # potential temperature (K)
    MMS_ROLL = MMS[' ROLL_MMS']*0.01
    MMS_HDG = MMS[' HDG_MMS']*0.01
    MMS_PITCH = MMS[' PITCH_MMS']*0.01
    #MMS_YAW = MMS[' YAW_MMS']*0.01 # has **** to filter out
    
    # AOA is last columm in file
    # may be ' AOA_MMS                                   ' or ' AOA_MMS     '
    # let number of spaces at end be flexible:
    AOA_col = MMS.columns[MMS.columns.str.startswith(' AOA')]
    MMS_AOA = MMS[AOA_col[0]]*0.01
    
    # clean up
    MMS_LAT[MMS_LAT<-500] = np.nan # clean up
    MMS_LON[MMS_LON<-500] = np.nan
    MMS_ALT[MMS_ALT<-500] = np.nan
    
    # create timestamp
    cur_day = datetime.strptime(filename[-15:-7],"%Y%m%d") # get date from end of file name
    MMS_time = [cur_day+timedelta(seconds=t) for t in MMS['TIME_START']]
    
    # save to DataFrame
    MMS = pd.DataFrame({'time': MMS_time, 'P': MMS_P, 'T': MMS_T, 'TAS': MMS_TAS, 'U': MMS_U,
                        'V': MMS_V, 'W': MMS_W, 'TEDR': MMS_TEDR, 'REYN': MMS_REYN, 'LAT': MMS_LAT,
                        'LON': MMS_LON, 'ALT': MMS_ALT, 'POT': MMS_POT, 'ROLL': MMS_ROLL, 'HDG': MMS_HDG,
                         'PITCH': MMS_PITCH, 'AOA': MMS_AOA})

    return MMS
    

# %% load WB57 data
def read_IWG1(filename_IWG1,cur_day):
    """
   Function to read the WB57 IWG1 data
    """
    
    IWG1 = pd.read_csv(filename_IWG1,sep=',',header=47)
    IWG1_lat = IWG1[' iLat']
    IWG1_lon = IWG1[' iLon']
    IWG1_alt_GPS = IWG1[' gAlt']
    IWG1_alt_baro = IWG1[' alt204']
    return IWG1 
    
    # IWG1['Ground Speed']
    # IWG1['True Airspeed']
    # IWG1['Indicated Airspeed']
    
    
# %% time-sync the data with COMA
def sync_data(MMS,COMA,inlet_ix):
    """
   Time sync the data
    """
    # MMS
    MMS_1s_avg = MMS.groupby(pd.Grouper(key="time", freq="1s")).mean()
    
    # COMA    
    COMA_subset = pd.DataFrame({'time': COMA['time'],
                                'CO_dry': COMA["      [CO]d_ppm"][inlet_ix]*1000, 
                                'N2O_dry': COMA["     [N2O]d_ppm"][inlet_ix]*1000,
                                'AmbT_C': COMA["         AmbT_C"],
                                'GasT_C': COMA["         GasT_C"],
                                'GasP_torr': COMA["      GasP_torr"],
                                'Peak0': COMA["          Peak0"],
                                '12COa_0000_CT': COMA["  12COa_0000_CT"],
                                'AIN5': COMA["           AIN5"],
                                'AIN6': COMA["           AIN6"],
                                'AIN7': COMA["           AIN7"],
                                'Gnd': COMA["            Gnd"],
                                'LTC0_v': COMA["         LTC0_v"],
                                'CHISQ0': COMA["         CHISQ0"]})
    
    COMA_1s_avg = COMA_subset.groupby(pd.Grouper(key="time", freq="1s")).mean()
    
    sync_data = pd.merge(MMS_1s_avg, COMA_1s_avg, how='inner', on=['time'])
    
    return sync_data

# %%
filenames = {'COMA_raw':[],
             'COMA_ict':[],
             'EEL':[],
             'MadgeTech':[],
             'MMS':[],
             'ACOS':[],
             'DLH':[],
             'COLD2':[]}

def return_filenames(case):
    if case == 'FCF_2021': # FCF
        filenames['COMA_raw'] = ['../Data/2021-08-06/n2o-co_2021-08-06_f0002.txt']
        filenames['MMS'] = '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20210806_RA.ict'
        filename_WB57 = '../Data/_OtherData_/NP_WB57_20210806_R0.ict'
    
    elif case == 'TF1_2021': # Test Flight 1
        filenames['COMA_raw'] = ['../Data/2021-08-10/n2o-co_2021-08-10_f0003.txt']
        filenames['MMS'] = '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20210810_RA.ict'
        filename_WB57 = '../Data/_OtherData_/NP_WB57_20210810_R0.ict'
        
    elif case == 'TF2_2021': # Test Flight 2
        filenames['COMA_raw'] = ['../Data/2021-08-16/n2o-co_2021-08-16_f0002.txt']
        filenames['MMS'] = '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20210816_RA.ict'
        filename_WB57 = '../Data/_OtherData_/NP_WB57_20210816_R0.ict'
        
    elif case == 'TF3_2021': # Test Flight 3
        filenames['COMA_raw'] = ['../Data/2021-08-17/n2o-co_2021-08-17_f0002.txt']
        filenames['MMS'] = '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20210817_RA.ict'
        filename_WB57 = '../Data/_OtherData_/NP_WB57_20210817_R0.ict'
        
    elif case == '2021-08-17': # lab breathing air
        #filename_COMA = '../Data/2021-08-06/n2o-co_2021-08-06_f0000.txt' # chop 3am part
        #filename_COMA = '../Data/2021-08-10/n2o-co_2021-08-10_f0000.txt'
        #filename_COMA = '../Data/2021-08-16/n2o-co_2021-08-16_f0000.txt'
        filenames['COMA_raw'] = ['../Data/2021-08-17/n2o-co_2021-08-17_f0000.txt']
        
    elif case == 'EEL_2022_Day2': # second day of chamber test
        filenames['COMA_raw'] = ['../Data/2022-05-20/n2o-co_2022-05-20_f0000.txt']
        
    elif case == 'FCF_2022': # FCF Houston integration 2022
        filenames['COMA_raw'] = ['../Data/2022-07-14/n2o-co_2022-07-14_f0002.txt']
        
    elif case == 'RF01': # science flight 1 Houston
        filenames['COMA_raw'] = ['../Data/2022-07-16/n2o-co_2022-07-16_f0002.txt']
        
    elif case == 'RF02': # science flight 2 Houston
        filenames['COMA_raw'] = ['../Data/2022-07-18/n2o-co_2022-07-18_f0002.txt',
                                 '../Data/2022-07-18/n2o-co_2022-07-18_f0003.txt']
        filenames['MMS'] = '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20220718_RA.ict'
        
    elif case == 'Transit1': # Ellington to Seattle
        filenames['COMA_raw'] = ['../Data/2022-07-21/n2o-co_2022-07-21_f0000.txt',
                         '../Data/2022-07-21/n2o-co_2022-07-21_f0001.txt']
        filenames['MMS'] =   '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20220721_RA_1.ict'
        filenames['ACOS'] =  '../Data/_OtherData_/ACCLIP-ACOS-1Hz_WB57_20220721_RA_1.ict'
        filenames['COLD2'] = '../Data/_OtherData_/acclip-COLD2-CO_WB57_20220721_RA_L1.ict'
        filenames['DLH'] = None
        
    elif case == 'Transit2': # Seattle to Anchorage
        filenames['COMA_raw'] = ['../Data/2022-07-21/n2o-co_2022-07-21_f0002.txt']
        filenames['MMS'] = '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20220721_RA_2.ict'
        filenames['ACOS'] = '../Data/_OtherData_/ACCLIP-ACOS-1Hz_WB57_20220721_RA_2.ict'
        filenames['COLD2'] = '../Data/_OtherData_/acclip-COLD2-CO_WB57_20220721_RA_L2.ict'
        filenames['DLH'] = None
    
    elif case == 'Transit3': # Anchorage to Adak
        filenames['COMA_raw'] = ['../Data/2022-07-24/n2o-co_2022-07-24_f0000.txt']
        filenames['MMS'] = '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20220724_RA.ict'
        filenames['ACOS'] = '../Data/_OtherData_/ACCLIP-ACOS-1Hz_WB57_20220724_RA.ict'
        filenames['COLD2'] = '../Data/_OtherData_/acclip-COLD2-CO_WB57_20220724_RA.ict'
        filenames['DLH'] = None
            
    elif case == 'Transit4': # Adak to Misawa
        filenames['COMA_raw'] = ['../Data/2022-07-25/n2o-co_2022-07-25_f0000.txt']
        filenames['MMS'] = '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20220725_RA.ict'
        filenames['ACOS'] = '../Data/_OtherData_/ACCLIP-ACOS-1Hz_WB57_20220725_RA.ict'
        filenames['COLD2'] = '../Data/_OtherData_/acclip-COLD2-CO_WB57_20220725_RA.ict'
        filenames['DLH'] = None
        
    elif case == 'Transit5': # Misawa to Osan
        filenames['COMA_raw'] = ['../Data/2022-07-27/n2o-co_2022-07-27_f0000.txt']
        filenames['MMS'] =   '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20220727_RA.ict'
        filenames['ACOS'] =  '../Data/_OtherData_/ACCLIP-ACOS-1Hz_WB57_20220727_RA.ict'
        filenames['COLD2'] = '../Data/_OtherData_/acclip-COLD2-CO_WB57_20220727_RA.ict'
        filenames['DLH'] = None
    
    elif case == 'RF03': # RF03
        filenames['COMA_raw'] = ['../Data/2022-08-02/n2o-co_2022-08-02_f0000.txt']
        filenames['MMS'] =   '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20220802_RA.ict'
        filenames['ACOS'] =  '../Data/_OtherData_/ACCLIP-ACOS-1Hz_WB57_20220802_RA.ict'
        filenames['COLD2'] = '../Data/_OtherData_/acclip-COLD2-CO_WB57_20220802_RA.ict'
        filenames['DLH'] = None
        
    elif case == 'RF04': # RF04 (first flight with MadgeTech installed)
        filenames['COMA_raw'] = ['../Data/2022-08-04/n2o-co_2022-08-04_f0000.txt']
        filenames['MMS'] =   '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20220804_RA.ict'
        filenames['ACOS'] =  '../Data/_OtherData_/ACCLIP-ACOS-1Hz_WB57_20220804_RA.ict'
        filenames['COLD2'] = '../Data/_OtherData_/acclip-COLD2-CO_WB57_20220804_RA.ict'
        filenames['DLH'] =   '../Data/_OtherData_/ACCLIP-DLH-H2O_WB57_20220804_RA.ict'
        filenames['MadgeTech'] = '../Data/2022-08-04/8.4.2022 flight Madgetech.xlsx'
        
    elif case == 'RF05': # RF05
        filenames['COMA_raw'] = ['../Data/2022-08-06/n2o-co_2022-08-06_f0000_no_10s_cal.txt']
        filenames['MMS'] =   '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20220806_RA.ict'
        filenames['ACOS'] =  '../Data/_OtherData_/ACCLIP-ACOS-1Hz_WB57_20220806_RA.ict'
        filenames['COLD2'] = '../Data/_OtherData_/acclip-COLD2-CO_WB57_20220806_RA.ict'
        filenames['DLH'] =   '../Data/_OtherData_/ACCLIP-DLH-H2O_WB57_20220806_RA.ict'
        filenames['MadgeTech'] = '../Data/2022-08-06/8.6.2022 flight Madgetech.xlsx'    
        
    elif case == 'RF06': # RF06
        filenames['COMA_raw'] = ['../Data/2022-08-12/n2o-co_2022-08-12_f0000.txt']
        filenames['MMS'] =   '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20220812_RA.ict'
        filenames['ACOS'] =  '../Data/_OtherData_/ACCLIP-ACOS-1Hz_WB57_20220812_RA.ict'
        filenames['COLD2'] = '../Data/_OtherData_/acclip-COLD2-CO_WB57_20220812_RA.ict'
        filenames['DLH'] =   '../Data/_OtherData_/ACCLIP-DLH-H2O_WB57_20220812_RA.ict'    
        filenames['MadgeTech'] = '../Data/2022-08-12/8.12.2022 flight Madgetech.xlsx' 
    
    elif case == 'RF07': # RF07
        filenames['COMA_raw'] = ['../Data/2022-08-13/n2o-co_2022-08-13_f0000.txt']
        filenames['MMS'] =   '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20220813_RA.ict'
        filenames['ACOS'] =  '../Data/_OtherData_/ACCLIP-ACOS-1Hz_WB57_20220813_RA.ict'
        filenames['COLD2'] = '../Data/_OtherData_/acclip-COLD2-CO_WB57_20220813_RA.ict'
        filenames['DLH'] =   '../Data/_OtherData_/ACCLIP-DLH-H2O_WB57_20220813_RA.ict'
        filenames['MadgeTech'] = '../Data/2022-08-13/8.13.2022 flight Madgetech.xlsx'
        
    elif case == 'RF08': # RF08
        filenames['COMA_raw'] = ['../Data/2022-08-15/n2o-co_2022-08-15_f0000.txt',
                         '../Data/2022-08-15/n2o-co_2022-08-15_f0001.txt']
        filenames['MMS'] =   '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20220815_RA.ict'
        filenames['ACOS'] =  '../Data/_OtherData_/ACCLIP-ACOS-1Hz_WB57_20220815_RA.ict'
        filenames['COLD2'] = '../Data/_OtherData_/acclip-COLD2-CO_WB57_20220815_RA.ict'
        filenames['DLH'] =   '../Data/_OtherData_/ACCLIP-DLH-H2O_WB57_20220815_RA.ict'
        filenames['MadgeTech'] = '../Data/2022-08-15/8.15.2022 flight Madgetech.xlsx'
        
    elif case == 'RF09': # RF09
        filenames['COMA_raw'] = ['../Data/2022-08-16/n2o-co_2022-08-16_f0000.txt']
        filenames['MMS'] =   '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20220816_RA.ict'
        filenames['ACOS'] =  '../Data/_OtherData_/ACCLIP-ACOS-1Hz_WB57_20220816_RA.ict'
        filenames['COLD2'] = '../Data/_OtherData_/acclip-COLD2-CO_WB57_20220816_RA.ict'
        filenames['DLH'] =   '../Data/_OtherData_/ACCLIP-DLH-H2O_WB57_20220816_RA.ict'
        filenames['MadgeTech'] = '../Data/2022-08-16/8.16.2022 flight Madgetech.xlsx'  
        
    elif case == 'RF10': # RF10 (instrument start before midnight; takeoff on 2022-08-19 UTC)
        filenames['COMA_raw'] = ['../Data/2022-08-18/n2o-co_2022-08-18_f0000.txt']
        filenames['MMS'] =   '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20220819_RA.ict'
        filenames['ACOS'] =  '../Data/_OtherData_/ACCLIP-ACOS-1Hz_WB57_20220819_RB.ict'
        filenames['COLD2'] = '../Data/_OtherData_/acclip-COLD2-CO_WB57_20220819_RA.ict'
        filenames['DLH'] =   '../Data/_OtherData_/ACCLIP-DLH-H2O_WB57_20220819_RA.ict'
        filenames['MadgeTech'] = '../Data/2022-08-18/8.18.2022 flight Madgetech.xlsx'
    
    elif case == 'RF11': # RF11
        filenames['COMA_raw'] = ['../Data/2022-08-21/n2o-co_2022-08-21_f0000.txt']
        filenames['MMS'] =   '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20220821_RA.ict'
        filenames['ACOS'] =  '../Data/_OtherData_/ACCLIP-ACOS-1Hz_WB57_20220821_RB.ict'
        filenames['COLD2'] = '../Data/_OtherData_/acclip-COLD2-CO_WB57_20220821_RA.ict'
        filenames['DLH'] =   '../Data/_OtherData_/ACCLIP-DLH-H2O_WB57_20220821_RA.ict'
        filenames['MadgeTech'] = '../Data/2022-08-21/8.21.2022 flight Madgetech.xlsx'
        
    elif case == 'RF12': # RF12 [need to fix time offset in MadgeTech file]
        filenames['COMA_raw'] = ['../Data/2022-08-23/n2o-co_2022-08-23_f0000.txt']
        filenames['MMS'] =   '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20220823_RA.ict'
        filenames['ACOS'] =  '../Data/_OtherData_/ACCLIP-ACOS-1Hz_WB57_20220823_RC.ict'
        filenames['COLD2'] = '../Data/_OtherData_/acclip-COLD2-CO_WB57_20220823_RA.ict'
        filenames['DLH'] =   '../Data/_OtherData_/ACCLIP-DLH-H2O_WB57_20220823_RA.ict'
        filenames['MadgeTech'] = '../Data/2022-08-23/8.23.2022 flight Madgetech.xlsx'
        
    elif case == 'RF13': # RF13
        filenames['COMA_raw'] = ['../Data/2022-08-24/n2o-co_2022-08-24_f0002.txt'] # six hour offset
        filenames['MMS'] =   '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20220825_RA.ict'
        filenames['ACOS'] =  '../Data/_OtherData_/ACCLIP-ACOS-1Hz_WB57_20220825_RA.ict'
        filenames['COLD2'] = '../Data/_OtherData_/acclip-COLD2-CO_WB57_20220825_RA.ict'
        filenames['DLH'] =   '../Data/_OtherData_/ACCLIP-DLH-H2O_WB57_20220825_RA.ict'
        filenames['MadgeTech'] = '../Data/2022-08-25/8.25.2022 flight Madgetech.xlsx'
        
    elif case == 'RF14': # RF14
        filenames['COMA_raw'] = ['../Data/2022-08-26/n2o-co_2022-08-26_f0000.txt']
        filenames['MMS'] =   '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20220826_RA.ict'
        filenames['ACOS'] =  '../Data/_OtherData_/ACCLIP-ACOS-1Hz_WB57_20220826_RA.ict'
        filenames['COLD2'] = '../Data/_OtherData_/acclip-COLD2-CO_WB57_20220826_RA.ict'
        filenames['DLH'] =   '../Data/_OtherData_/ACCLIP-DLH-H2O_WB57_20220826_RA.ict'
        filenames['MadgeTech'] = '../Data/2022-08-26/8.26.2022 flight Madgetech.xlsx'
        
    elif case == 'RF15': # RF15
        filenames['COMA_raw'] = ['../Data/2022-08-29/n2o-co_2022-08-29_f0000.txt']
        filenames['MMS'] =   '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20220829_RA.ict'
        filenames['ACOS'] =  '../Data/_OtherData_/ACCLIP-ACOS-1Hz_WB57_20220829_RA.ict'
        filenames['COLD2'] = '../Data/_OtherData_/acclip-COLD2-CO_WB57_20220829_RA.ict'
        filenames['DLH'] =   '../Data/_OtherData_/ACCLIP-DLH-H2O_WB57_20220829_RA.ict'
        filenames['MadgeTech'] = '../Data/2022-08-29/8.29.2022 flight Madgetech.xlsx'
    
    elif case == 'RF16': # RF16
        filenames['COMA_raw'] = ['../Data/2022-08-31/n2o-co_2022-08-31_f0000.txt']
        filenames['MMS'] =   '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20220831_RA.ict'
        filenames['ACOS'] =  '../Data/_OtherData_/ACCLIP-ACOS-1Hz_WB57_20220831_RA.ict'
        filenames['COLD2'] = '../Data/_OtherData_/acclip-COLD2-CO_WB57_20220831_RA.ict'
        filenames['DLH'] =   '../Data/_OtherData_/ACCLIP-DLH-H2O_WB57_20220831_RA.ict'
        filenames['MadgeTech'] = '../Data/2022-08-31/8.31.2022 flight Madgetech.xlsx'
    
    elif case == 'RF17': # RF17
        filenames['COMA_raw'] = ['../Data/2022-09-01/n2o-co_2022-09-01_f0000.txt']
        filenames['MMS'] =   '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20220901_RA.ict'
        filenames['ACOS'] =  '../Data/_OtherData_/ACCLIP-ACOS-1Hz_WB57_20220901_RA.ict'
        filenames['COLD2'] = '../Data/_OtherData_/acclip-COLD2-CO_WB57_20220901_RA.ict'
        filenames['DLH'] =   '../Data/_OtherData_/ACCLIP-DLH-H2O_WB57_20220901_RA.ict'
        filenames['MadgeTech'] = '../Data/2022-09-01/9.01.2022 flight Madgetech.xlsx'
        
    else:
        print('case not recognized')
    
    return filenames
