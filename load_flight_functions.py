# -*- coding: utf-8 -*-
"""
Load different file types ACCLIP:
- COMA (from analyzer)
- MMS (from NASA LaRC archive)
- IWG1 (from Mission Tools Suite)
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
    for count, fname in enumerate(filename_COMA):
        if count == 0:
            COMA = pd.read_csv(filename_COMA[0],sep=',',header=1)
        else:
            COMA2 = pd.read_csv(fname,sep=',',header=1)
            COMA = pd.concat([COMA,COMA2],ignore_index=True)

    COMA_time = COMA["                     Time"]
    COMA_time = [datetime.strptime(tstamp,"  %m/%d/%Y %H:%M:%S.%f") for tstamp in COMA_time]
    COMA_time = pd.DataFrame(COMA_time)
    COMA_time = COMA_time[0]
    
    COMA['time'] = COMA_time
    
    return COMA


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
    
    # IWG1['Ground Speed']
    # IWG1['True Airspeed']
    # IWG1['Indicated Airspeed']
    
    
# %% time-sync the data with COMA
def sync_data(MMS,COMA):
    """
   Time sync the data
    """
    
    MMS_1s_avg = MMS.groupby(pd.Grouper(key="time", freq="1s")).mean()
    
    # index MIU valves
    #ix_8 = np.ravel(np.where( (LGR["      MIU_VALVE"]==8) & (LGR["      GasP_torr"]>52.45) & (LGR["      GasP_torr"]<52.65)) ) # Inlet
    MIU = COMA["      MIU_VALVE"]   
    COMA_time = COMA['time']
    
    # handle purge air settings
    if COMA_time[0] <= datetime(2022,8,15):
        # use only inlet data
        indices = np.ravel(np.where(MIU==8))
    else:
        # starting 2022-08-16, MIU sequence no longer set to cycle through purge
        # account for this by excluding 20 s of data after the high cal
        # [NOTE: the command below also excludes 20 s data before the low cal.
        # revise to handle this]
        indices = np.ravel(np.where((MIU==8) & (MIU.shift(20)==8)))
    
    #indices = np.union1d(ix_1,ix_8) # use both inlet and flush data here
    COMA_subset = pd.DataFrame({'time': COMA_time,
                                'CO_dry': COMA["      [CO]d_ppm"][indices]*1000, 
                                'N2O_dry': COMA["     [N2O]d_ppm"][indices]*1000,
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