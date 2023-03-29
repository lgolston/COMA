# -*- coding: utf-8 -*-
"""
Merge file

"""

# %% load data
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.dates as mdates
import numpy as np
from scipy import signal

filenames_1s = \
[['acclip-mrg60_wb57_20220802_RA_20221111T194047.ict','20220802_RF03'], #0-RF03
 ['acclip-mrg60_wb57_20220804_RA_20221111T194048.ict','20220804_RF04'], #1-RF04
 ['acclip-mrg60_wb57_20220806_RA_20221111T194048.ict','20220806_RF05'], #2-RF05
 ['acclip-mrg60_wb57_20220812_RA_20221111T194049.ict','20220812_RF06'], #3-RF06
 ['acclip-mrg60_wb57_20220813_RA_20221111T194049.ict','20220813_RF07'], #4-RF07
 ['acclip-mrg60_wb57_20220815_RA_20221111T194049.ict','20220815_RF08'], #5-RF08
 ['acclip-mrg60_wb57_20220816_RA_20221111T194050.ict','20220816_RF09'], #6-RF09
 ['acclip-mrg60_wb57_20220819_RA_20221111T194050.ict','20220819_RF10'], #7-RF10
 ['acclip-mrg60_wb57_20220821_RA_20221111T194050.ict','20220821_RF11'], #8-RF11
 ['acclip-mrg60_wb57_20220823_RA_20221111T194051.ict','20220823_RF12'], #9-RF12
 ['acclip-mrg60_wb57_20220825_RA_20221111T194051.ict','20220825_RF13'], #10-RF13
 ['acclip-mrg60_wb57_20220826_RA_20221111T194052.ict','20220826_RF14'], #11-RF14
 ['acclip-mrg60_wb57_20220829_RA_20221111T194052.ict','20220829_RF15'], #12-RF15
 ['acclip-mrg60_wb57_20220831_RA_20221111T194052.ict','20220831_RF16'], #13-RF16
 ['acclip-mrg60_wb57_20220901_RA_20221111T194053.ict','20220901_RF17']] #14-RF17

# set plot style
plt.rcParams['axes.labelsize'] = 8
plt.rcParams['xtick.labelsize'] = 7
plt.rcParams['ytick.labelsize'] = 7
plt.rcParams['legend.fontsize'] = 7
plt.rcParams['font.size']=8
plt.rcParams.update({'mathtext.default': 'regular' } ) # not italics

# %% load and plot
for case in range(0,15):
    # %% load and prepare data
    filename = '../Data/_Merge_/'+filenames_1s[case][0]
    case_name = filenames_1s[case][1]
    
    Data = pd.read_csv(filename,sep=',',header=88,skipinitialspace=True,low_memory=False)
    
    Data[Data==-999999] = np.nan
    
    alt_km = Data['G_ALT_MMS_BUI']/1000
    
    x = Data['CO_PODOLSKE'] 
    y = Data['ACOS_CO_PPB_GURGANUS']
    #y = Data['CO_COLD2_ppbv_VICIANI']
    
    plt.plot(x)
    plt.plot(y)
    
    ix = np.ravel(np.where((x>0) & (y>0))) # inlet
    
    correlation = signal.correlate(x[ix]-np.mean(x[ix]), y[ix] - np.mean(y[ix]), mode="full")
    lags = signal.correlation_lags(len(x[ix]), len(y[ix]), mode="full")
    lag = lags[np.argmax(abs(correlation))]
    
    print(lag)
    #plt.plot(lags,correlation,'.')
    
# %% test
#https://stackoverflow.com/questions/69117617/how-to-find-the-lag-between-two-time-series-using-cross-correlation
#x = [4,4,4,4,6,8,10,8,6,4,4,4,4,4,4,4,4,4,4,4,4,4,4]
#y = [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,6,8,10,8,6,4,4]
#correlation = signal.correlate(x-np.mean(x), y - np.mean(y), mode="full")
#lags = signal.correlation_lags(len(x), len(y), mode="full")
#lag = lags[np.argmax(abs(correlation))]
