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
from load_data_functions import read_ACOS_ict
from load_data_functions import read_COLD2_ict
from load_data_functions import return_filenames
import scipy.stats

filenames_1s = \
[['acclip-mrg1_wb57_20220802_RA_20221111T194220.ict','RF03'], #0-RF03
 ['acclip-mrg1_wb57_20220804_RA_20221111T194221.ict','RF04'], #1-RF04
 ['acclip-mrg1_wb57_20220806_RA_20221111T194223.ict','RF05'], #2-RF05
 ['acclip-mrg1_wb57_20220812_RA_20221111T194225.ict','RF06'], #3-RF06
 ['acclip-mrg1_wb57_20220813_RA_20221111T194226.ict','RF07'], #4-RF07
 ['acclip-mrg1_wb57_20220815_RA_20221111T194228.ict','RF08'], #5-RF08
 ['acclip-mrg1_wb57_20220816_RA_20221111T194230.ict','RF09'], #6-RF09
 ['acclip-mrg1_wb57_20220819_RA_20221111T194231.ict','RF10'], #7-RF10
 ['acclip-mrg1_wb57_20220821_RA_20221111T194233.ict','RF11'], #8-RF11
 ['acclip-mrg1_wb57_20220823_RA_20221111T194235.ict','RF12'], #9-RF12
 ['acclip-mrg1_wb57_20220825_RA_20221111T194237.ict','RF13'], #10-RF13
 ['acclip-mrg1_wb57_20220826_RA_20221111T194239.ict','RF14'], #11-RF14
 ['acclip-mrg1_wb57_20220829_RA_20221111T194241.ict','RF15'], #12-RF15
 ['acclip-mrg1_wb57_20220831_RA_20221111T194242.ict','RF16'], #13-RF16
 ['acclip-mrg1_wb57_20220901_RA_20221111T194244.ict','RF17']] #14-RF17

# set plot style
plt.rcParams['axes.labelsize'] = 8
plt.rcParams['xtick.labelsize'] = 7
plt.rcParams['ytick.labelsize'] = 7
plt.rcParams['legend.fontsize'] = 7
plt.rcParams['font.size']=8
plt.rcParams.update({'mathtext.default': 'regular' } ) # not italics

# %% load and plot
for case in range(11,12):
    # %% load merge data
    filename = '../Data/_Merge_/'+filenames_1s[case][0]
    case_name = filenames_1s[case][1]
    
    Data = pd.read_csv(filename,sep=',',header=88,skipinitialspace=True,low_memory=False)
    Data[Data==-999999] = np.nan
    Data_time = pd.Series([datetime(2022,8,23)+timedelta(seconds=ts) for ts in Data['Time_Start']])
    
    alt_km = Data['G_ALT_MMS_BUI']/1000
    
    # %% load individual ict data
    filenames = return_filenames(case_name)

    cur_day = datetime.strptime(filenames['COMA_ict'][-15:-7],"%Y%m%d") # get date from end of file name
    COMA = pd.read_csv(filenames['COMA_ict'],header=35)
    COMA['time'] = [cur_day+timedelta(seconds=t) for t in COMA['Time_Mid']]
    COMA[COMA['CO'] == -9999] = np.nan
    COMA[COMA['N2O'] == -9999] = np.nan

    ACOS = read_ACOS_ict(filenames['ACOS'])
    ACOS[ACOS["ACOS_CO_PPB"]<-600] = np.nan

    COLD2 = read_COLD2_ict(filenames['COLD2'])
    COLD2[COLD2[' CO_COLD2_ppbv']<-600]=np.nan
        
    # %% plot
    merge_CO_COMA = Data['CO_PODOLSKE']
    merge_CO_ACOS = Data['ACOS_CO_PPB_GURGANUS']
    merge_CO_COLD2 = Data['CO_COLD2_ppbv_VICIANI']
    
    # wiht some smoothing:
    #merge_CO_COMA = Data['CO_PODOLSKE'].rolling(10,min_periods=8,center=True).median()
    #merge_CO_ACOS = Data['ACOS_CO_PPB_GURGANUS'].rolling(10,min_periods=8,center=True).median()
    #merge_CO_COLD2 = Data['CO_COLD2_ppbv_VICIANI'].rolling(10,min_periods=8,center=True).median()
    
    x = merge_CO_COMA
    y = merge_CO_COLD2
    
    plt.plot(Data_time,x)
    plt.plot(Data_time,y)
    #plt.plot(Data_time,merge_CO_ACOS)
    #plt.plot(COMA['time'],COMA['CO'])
    
    time_step = 500
    for jj in range(20,20000,time_step):
        
        vals = np.zeros(41)
        counter=0
        
        for ss in range (-20,21):
            x_temp = x.values[(jj+ss):(jj+ss+time_step)]
            y_temp = y.values[jj:(jj+time_step)]
            ix = np.ravel(np.where((x_temp>0) & (y_temp>0))) # remove NaN
            
            if len(ix)>100:
                res = scipy.stats.pearsonr(x_temp[ix], y_temp[ix])
                vals[counter]=res.statistic
                #print(jj,ss,res.statistic)
                
            counter+=1
        
        print(Data_time[jj],np.argmax(vals)-20,f'{np.max(vals):.2}',f"{Data['G_ALT_MMS_BUI'][jj]:.0f}")
        
    
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
    
# %% test
#https://stackoverflow.com/questions/69117617/how-to-find-the-lag-between-two-time-series-using-cross-correlation
#x = [4,4,4,4,6,8,10,8,6,4,4,4,4,4,4,4,4,4,4,4,4,4,4]
#y = [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,6,8,10,8,6,4,4]
#correlation = signal.correlate(x-np.mean(x), y - np.mean(y), mode="full")
#lags = signal.correlation_lags(len(x), len(y), mode="full")
#lag = lags[np.argmax(abs(correlation))]
