# -*- coding: utf-8 -*-
"""
Merge file

look at time sychronization
- Divide data into 5 min windows
- cross-correlate DLH and COMA
- cross compare COMA, ACOS, COLD2
- other species such as ozone

"""

# %% load data
import numpy as np
import pandas as pd
from functools import reduce
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from scipy import signal
import scipy.stats
from load_data_functions import read_COMA
from load_data_functions import read_ACOS_ict
from load_data_functions import read_MMS_ict
from load_data_functions import read_COLD2_ict
from load_data_functions import return_filenames

cases = ['Transit1','Transit2','Transit3','Transit4','Transit5','RF03','RF04','RF05','RF06',
         'RF07','RF08','RF09','RF10','RF11','RF12','RF13','RF14','RF15','RF16','RF17','Transit6',
         'Transit7','Transit8','Transit9']
 
# set plot style
plt.rcParams['axes.labelsize'] = 8
plt.rcParams['xtick.labelsize'] = 7
plt.rcParams['ytick.labelsize'] = 7
plt.rcParams['legend.fontsize'] = 7
plt.rcParams['font.size']=8
plt.rcParams.update({'mathtext.default': 'regular' } ) # not italics

# %% create helper function (for loading ICARTT files, linear regression)
def read_DLH_ict(filename):
    # e.g. ACCLIP-DLH-H2O_WB57_20220816_RA.ict
    if filename==None:
        DLH = []
    else:
        if len(filename)==58:
            cur_day = datetime.strptime(filename[-18:-10],"%Y%m%d")
        else:
            cur_day = datetime.strptime(filename[-15:-7],"%Y%m%d")
        DLH = pd.read_csv(filename,sep=',',header=35)
        DLH['time'] = [cur_day+timedelta(seconds=t) for t in DLH['Time_Start']]
        DLH[DLH['H2O_DLH']<-800] = np.nan
    return DLH


# %% load and plot
for case_name in cases: #['RF04']:
    # %% load individual ict data
    filenames = return_filenames(case_name)

    # load COMA ict data
    if case_name == 'Transit1':
        cur_day = datetime(2022,7,21)
    elif case_name == 'Transit2':
        cur_day = datetime(2022,7,21)
    else:
        cur_day = datetime.strptime(filenames['COMA_ict'][-15:-7],"%Y%m%d") # get date from end of file name
    COMA = pd.read_csv(filenames['COMA_ict'],header=35)
    COMA['time'] = [cur_day+timedelta(seconds=t) for t in COMA['Time_Mid']]
    COMA[COMA['CO'] == -9999] = np.nan
    COMA[COMA['N2O'] == -9999] = np.nan

    # load ACOS
    ACOS = read_ACOS_ict(filenames['ACOS'])
    ACOS[ACOS["ACOS_CO_PPB"]<-600] = np.nan

    # load COLD2
    COLD2 = read_COLD2_ict(filenames['COLD2'])
    COLD2[COLD2[' CO_COLD2_ppbv']<-600]=np.nan
    
    # load DLH (not always available)
    DLH = read_DLH_ict(filenames['DLH'])
    
    # load MMS data
    MMS = read_MMS_ict(filenames['MMS'])
    #MMS[ACOS["ACOS_CO_PPB"]<-600] = np.nan
    
    # load COMA raw data
    COMA_raw, inlet_ix = read_COMA(filenames['COMA_raw'])
    if case_name == 'RF13': # fix clock setting on this day
        COMA_raw['time'] = COMA_raw['time'] + timedelta(hours=6)
        
    # filter COMA data that is not from inlet
    tmp=np.array(COMA_raw.index)
    mask=np.full(len(COMA_raw.index),True,dtype=bool)
    mask[inlet_ix]=False
    non_inlet_ix = tmp[mask]
    COMA_raw['[CO]d_ppm'][non_inlet_ix] = np.nan
    COMA_raw['[H2O]_ppm'][non_inlet_ix] = np.nan
    
    # %% merge data
    COMA_1s_avg = COMA_raw.groupby(pd.Grouper(key="time", freq="1s")).mean()
    COLD2_1s_avg = COLD2.groupby(pd.Grouper(key="time", freq="1s")).mean()
    MMS_1s_avg = MMS.groupby(pd.Grouper(key="time", freq="1s")).mean()
    
    if len(DLH)>0:
        DLH_1s_avg = DLH.groupby(pd.Grouper(key="time", freq="1s")).mean()
        data_frames = [COMA_1s_avg, COLD2_1s_avg, DLH_1s_avg, MMS_1s_avg]
        suffixes = ['_COMA','_COLD2','_DLH', '_MMS']
    else:
        data_frames = [COMA_1s_avg, COLD2_1s_avg, MMS_1s_avg]
        suffixes = ['_COMA','_COLD2','_MMS']
    # add suffixes to each df
    data_frames = [data_frames[i].add_suffix(suffixes[i]) for i in range(len(data_frames))]

    sync_data = reduce(lambda  left,right: pd.merge(left,right,on=['time'],
                                            how='outer'), data_frames)

    #sync_data = pd.merge(COMA_1s_avg, COLD2_1s_avg, how='inner', on=['time'])
    
    # %% time lag COMA vs COLD2 data        
    # wiht some smoothing:
    #merge_CO_COMA = Data['CO_PODOLSKE'].rolling(10,min_periods=8,center=True).median()
    #merge_CO_ACOS = Data['ACOS_CO_PPB_GURGANUS'].rolling(10,min_periods=8,center=True).median()
    #merge_CO_COLD2 = Data['CO_COLD2_ppbv_VICIANI'].rolling(10,min_periods=8,center=True).median()

    x = sync_data['[CO]d_ppm_COMA']*1000
    y = sync_data[' CO_COLD2_ppbv_COLD2']
    
    fig1, ax = plt.subplots()
    plt.plot(sync_data.index,x)
    plt.plot(sync_data.index,y)
    #plt.plot(Data_time,merge_CO_ACOS)
    #plt.plot(COMA['time'],COMA['CO'])
    
    time_step = 500
    time_distance = 50
    iterator = range(time_distance,len(sync_data.index)-time_step-time_distance,time_step)
    
    bin_time = np.zeros(len(iterator),dtype=pd.Timestamp)
    bin_lag = np.zeros_like(bin_time)
    bin_corr = np.zeros_like(bin_time)
    bin_alt = np.zeros_like(bin_time)
    
    for jj, time_index in enumerate(iterator):
        
        vals = np.zeros(len(range(-time_distance,time_distance+1)))
        counter = 0
        
        # slide window by +/- 20 seconds
        for ss in range(-time_distance,time_distance+1):
            x_temp = x.values[(time_index+ss):(time_index+ss+time_step)]
            y_temp = y.values[time_index:(time_index+time_step)]
            ix = np.ravel(np.where((x_temp>0) & (y_temp>0))) # remove NaN
            
            # require a certain number of data points
            if len(ix)>100:
                res = scipy.stats.pearsonr(x_temp[ix], y_temp[ix])
                vals[counter]=res.statistic
                #print(jj,ss,res.statistic)
                
            counter+=1
        
        bin_time[jj] = sync_data.index[time_index]
        bin_lag[jj] = np.argmax(vals)-time_distance
        bin_corr[jj] = np.max(vals)
        bin_alt[jj] = sync_data['ALT_MMS'][time_index]
        #print(bin_time[jj],bin_lag[jj],f'{bin_corr[jj]:.2}',f"{bin_alt[jj]:.0f}")
        
    
    # %% original method using signal correlate
    """
    for jj in range(0,20500,1000):
        ix = np.ravel( np.where((x>0) & (y>0) 
                                & (x.index>jj)  & (y.index<(jj+1000))) ) # exclude nan
        
        if len(ix)>100:
            correlation = signal.correlate(x[ix]-np.mean(x[ix]), y[ix] - np.mean(y[ix]), mode="same")
            lags = signal.correlation_lags(len(x[ix]), len(y[ix]), mode="same")
            lag = lags[np.argmax(abs(correlation))]
            
            print(Data_time[jj],lag)
    #plt.plot(lags,correlation,'.'),plt.axvline(0,color='black',linestyle=':')
    #plt.plot(merge_CO_COMA[ix]),plt.plot(merge_CO_COLD2[ix])
    """
    
    # %% COMA v. DLH time lag
    if len(DLH)>0:
    
        x = sync_data['[H2O]_ppm_COMA']
        y = sync_data['H2O_DLH_DLH']
        #ID = sync_data['SpectraID'] 
     
        time_step = 500
        time_distance = 50
        iterator = range(time_distance,len(sync_data)-time_step-time_distance,time_step)
        
        bin_time_DLH = np.zeros(len(iterator),dtype=pd.Timestamp)
        bin_lag_DLH = np.zeros_like(bin_time)
        bin_corr_DLH = np.zeros_like(bin_time)
        bin_alt_DLH = np.zeros_like(bin_time)
    
        for jj, time_index in enumerate(iterator):
            
            vals = np.zeros(len(range(-time_distance,time_distance+1)))
            counter = 0
                
            # slide window by +/- 20 seconds
            for ss in range(-time_distance,time_distance):
                x_temp = x.values[(time_index+ss):(time_index+ss+time_step)]
                y_temp = y.values[time_index:(time_index+time_step)]
                ix = np.ravel(np.where((x_temp>500) & (y_temp>0))) # remove NaN and below COMA LOD
                
                # require a certain number of data points
                if len(ix)>100:
                    res = scipy.stats.pearsonr(x_temp[ix], y_temp[ix])
                    vals[counter]=res.statistic
                    #print(jj,ss,res.statistic)
                            
                counter+=1
            
            bin_time_DLH[jj] = sync_data.index[time_index]
            bin_lag_DLH[jj] = np.argmax(vals)-time_distance
            bin_corr_DLH[jj] = np.max(vals)
            #print(bin_time_DLH[jj],bin_lag_DLH[jj],f'{bin_corr_DLH[jj]:.2}')
        
    
    # %% plot
    ix = np.ravel(np.where(bin_corr>0.95))
    if len(DLH)>0:
        ix_DLH = np.ravel(np.where(bin_corr_DLH>0.95))
    
    fig2, ax1 = plt.subplots()
    ax1.plot(bin_time[ix],bin_lag[ix],'--.',label='COMA : COLD2')
    if len(DLH)>0:
        ax1.plot(bin_time_DLH[ix_DLH],bin_lag_DLH[ix_DLH],'yx',label='COMA : DLH')
    ax1.set_ylabel('Lag, s')
    ax1.legend()
    ax2 = ax1.twinx()
    ax2.plot(bin_time[ix],bin_alt[ix],'k.')
    ax2.plot(sync_data.index,sync_data['ALT_MMS'],'k')
    ax2.set_ylabel('MMS altitude, m')
    ax1.set_ylim(-10,25)
    ax1.grid('on')
    
    print(case_name)
    print('min/max COLD2 lag:', min(bin_lag[ix]), max(bin_lag[ix]))
    if len(DLH)>0:
        print('min/max DLH lag:', min(bin_lag_DLH[ix_DLH]), max(bin_lag_DLH[ix_DLH]))
    else:
        print('empty')
    
    ax1.set_title(case_name)
    ax2.set_ylim([0,19000])
    fig2.tight_layout()
    fig2.savefig('COMA_' + case_name + '.png',dpi=300)
    
    plt.close('all')