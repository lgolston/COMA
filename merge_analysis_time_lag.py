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
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.dates as mdates
import numpy as np
from scipy import signal
from load_data_functions import read_COMA
from load_data_functions import read_ACOS_ict
from load_data_functions import read_COLD2_ict
from load_data_functions import return_filenames
import scipy.stats

filenames_1s = \
[['acclip-mrg1_wb57_20220721_RA_20221111T194215.ict','Transit1'], # 0
 ['acclip-mrg1_wb57_20220721_RA_20221111T194215.ict','Transit2'], # 1
 ['acclip-mrg1_wb57_20220724_RA_20221111T194216.ict','Transit3'], # 2
 ['acclip-mrg1_wb57_20220725_RA_20221111T194217.ict','Transit4'], # 3
 ['acclip-mrg1_wb57_20220727_RA_20221111T194218.ict','Transit5'], # 4
 ['acclip-mrg1_wb57_20220802_RA_20221111T194220.ict','RF03'], #5-RF03
 ['acclip-mrg1_wb57_20220804_RA_20221111T194221.ict','RF04'], #6-RF04
 ['acclip-mrg1_wb57_20220806_RA_20221111T194223.ict','RF05'], #7-RF05
 ['acclip-mrg1_wb57_20220812_RA_20221111T194225.ict','RF06'], #8-RF06
 ['acclip-mrg1_wb57_20220813_RA_20221111T194226.ict','RF07'], #9-RF07
 ['acclip-mrg1_wb57_20220815_RA_20221111T194228.ict','RF08'], #10-RF08
 ['acclip-mrg1_wb57_20220816_RA_20221111T194230.ict','RF09'], #11-RF09
 ['acclip-mrg1_wb57_20220819_RA_20221111T194231.ict','RF10'], #12-RF10
 ['acclip-mrg1_wb57_20220821_RA_20221111T194233.ict','RF11'], #13-RF11
 ['acclip-mrg1_wb57_20220823_RA_20221111T194235.ict','RF12'], #14-RF12
 ['acclip-mrg1_wb57_20220825_RA_20221111T194237.ict','RF13'], #15-RF13
 ['acclip-mrg1_wb57_20220826_RA_20221111T194239.ict','RF14'], #16-RF14
 ['acclip-mrg1_wb57_20220829_RA_20221111T194241.ict','RF15'], #17-RF15
 ['acclip-mrg1_wb57_20220831_RA_20221111T194242.ict','RF16'], #18-RF16
 ['acclip-mrg1_wb57_20220901_RA_20221111T194244.ict','RF17'], #19-RF17
 ['acclip-mrg1_wb57_20220721_RA_20221111T194215.ict','Transit6'], # 20
 ['acclip-mrg1_wb57_20220721_RA_20221111T194215.ict','Transit7'], # 21
 ['acclip-mrg1_wb57_20220721_RA_20221111T194215.ict','Transit8'], # 22
 ['acclip-mrg1_wb57_20220721_RA_20221111T194215.ict','Transit9']] # 23
 
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
        cur_day = datetime.strptime(filename[-15:-7],"%Y%m%d")
        DLH = pd.read_csv(filename,sep=',',header=35)
        DLH['time'] = [cur_day+timedelta(seconds=t) for t in DLH['Time_Start']]
        DLH[DLH['H2O_DLH']<-800] = np.nan
    return DLH


# %% load and plot
for case in range(0,3):
    # %% load merge data
    filename = '../Data/_Merge_/'+filenames_1s[case][0]
    case_name = filenames_1s[case][1]
    
    cur_day = datetime.strptime(filename[-31:-23],"%Y%m%d")
    
    Data = pd.read_csv(filename,sep=',',header=88,skipinitialspace=True,low_memory=False)
    Data[Data==-999999] = np.nan
    Data_time = pd.Series([cur_day+timedelta(seconds=ts) for ts in Data['Time_Start']])
    
    alt_km = Data['G_ALT_MMS_BUI']/1000
    
    # %% load individual ict data
    filenames = return_filenames(case_name)

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

    ACOS = read_ACOS_ict(filenames['ACOS'])
    ACOS[ACOS["ACOS_CO_PPB"]<-600] = np.nan

    COLD2 = read_COLD2_ict(filenames['COLD2'])
    COLD2[COLD2[' CO_COLD2_ppbv']<-600]=np.nan
    
    DLH = read_DLH_ict(filenames['DLH'])
        
    COMA_raw, inlet_ix = read_COMA(filenames['COMA_raw'])
    
    # %% time lag COMA vs COLD2 data
    merge_CO_COMA = Data['CO_PODOLSKE']
    merge_CO_ACOS = Data['ACOS_CO_PPB_GURGANUS']
    merge_CO_COLD2 = Data['CO_COLD2_ppbv_VICIANI']
        
    # wiht some smoothing:
    #merge_CO_COMA = Data['CO_PODOLSKE'].rolling(10,min_periods=8,center=True).median()
    #merge_CO_ACOS = Data['ACOS_CO_PPB_GURGANUS'].rolling(10,min_periods=8,center=True).median()
    #merge_CO_COLD2 = Data['CO_COLD2_ppbv_VICIANI'].rolling(10,min_periods=8,center=True).median()

    x = merge_CO_COMA
    y = merge_CO_COLD2
    
    fig1, ax = plt.subplots()
    plt.plot(Data_time,x)
    plt.plot(Data_time,y)
    #plt.plot(Data_time,merge_CO_ACOS)
    #plt.plot(COMA['time'],COMA['CO'])
    
    time_step = 500
    iterator = range(20,len(Data_time)-500-20,time_step)
    
    bin_time = np.zeros(len(iterator),dtype=pd.Timestamp)
    bin_lag = np.zeros_like(bin_time)
    bin_corr = np.zeros_like(bin_time)
    bin_alt = np.zeros_like(bin_time)
    
    for jj, time_index in enumerate(iterator):
        
        vals = np.zeros(len(range(-20,21)))
        counter = 0
        
        # slide window by +/- 20 seconds
        for ss in range(-20,21):
            x_temp = x.values[(time_index+ss):(time_index+ss+time_step)]
            y_temp = y.values[time_index:(time_index+time_step)]
            ix = np.ravel(np.where((x_temp>0) & (y_temp>0))) # remove NaN
            
            if len(ix)>100:
                res = scipy.stats.pearsonr(x_temp[ix], y_temp[ix])
                vals[counter]=res.statistic
                #print(jj,ss,res.statistic)
                
            counter+=1
        
        bin_time[jj] = Data_time[time_index]
        bin_lag[jj] = np.argmax(vals)-20
        bin_corr[jj] = np.max(vals)
        bin_alt[jj] = Data['G_ALT_MMS_BUI'][time_index]
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
        COMA_1s_avg = COMA_raw.groupby(pd.Grouper(key="time", freq="1s")).mean()
        DLH_1s_avg = DLH.groupby(pd.Grouper(key="time", freq="1s")).mean()
        sync_data = pd.merge(COMA_1s_avg, DLH_1s_avg, how='inner', on=['time'])
    
        x = sync_data['[H2O]_ppm']
        y = sync_data['H2O_DLH']
        ID = sync_data['SpectraID'] 
     
        time_step = 500
        iterator = range(20,len(sync_data)-500-20,time_step)
            
        bin_time_DLH = np.zeros(len(iterator),dtype=pd.Timestamp)
        bin_lag_DLH = np.zeros_like(bin_time)
        bin_corr_DLH = np.zeros_like(bin_time)
        bin_alt_DLH = np.zeros_like(bin_time)
    
        for jj, time_index in enumerate(iterator):
            
            vals = np.zeros(len(range(-20,21)))
            counter = 0
                
            # slide window by +/- 20 seconds
            for ss in range(-20,21):
                x_temp = x.values[(time_index+ss):(time_index+ss+time_step)]
                y_temp = y.values[time_index:(time_index+time_step)]
                ix = np.ravel(np.where((x_temp>100) & (y_temp>100))) # remove NaN and below COMA LOD
                  
                if len(ix)>100:
                    res = scipy.stats.pearsonr(x_temp[ix], y_temp[ix])
                    vals[counter]=res.statistic
                    #print(jj,ss,res.statistic)
                            
                counter+=1
                
            bin_time_DLH[jj] = sync_data.index[time_index]
            bin_lag_DLH[jj] = np.argmax(vals)-20
            bin_corr_DLH[jj] = np.max(vals)
            #print(bin_time_DLH[jj],bin_lag_DLH[jj],f'{bin_corr_DLH[jj]:.2}')
        
    
    # %% plot
    ix = np.ravel(np.where(bin_corr>0.95))
    if len(DLH)>0:
        ix_DLH = np.ravel(np.where(bin_corr_DLH>0.95))
    
    fig2, ax1 = plt.subplots()
    ax1.plot(bin_time[ix],bin_lag[ix],'--.')
    if len(DLH)>0:
        ax1.plot(bin_time_DLH[ix_DLH],bin_lag_DLH[ix_DLH],'yx')
    ax1.set_ylabel('Lag, s')
    ax2 = ax1.twinx()
    ax2.plot(bin_time[ix],bin_alt[ix],'k.')
    ax2.plot(Data_time,Data['G_ALT_MMS_BUI'],'k')
    ax2.set_ylabel('MMS altitude, m')
    ax1.set_ylim(-1,9)
    
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