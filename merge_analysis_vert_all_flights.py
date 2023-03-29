# -*- coding: utf-8 -*-
"""
Look at mean profiles across all flights during ACCLIP

"""

# %% load data
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.dates as mdates
import numpy as np

filenames_60s = \
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
fig, ax = plt.subplots(1, 1, figsize=(4,4))

for case in range(0,15):
    # %% load and prepare data
    filename = '../Data/_Merge_/'+filenames_60s[case][0]
    case_name = filenames_60s[case][1]
    
    Data = pd.read_csv(filename,sep=',',header=88,skipinitialspace=True,low_memory=False)
    Data[Data==-999999] = np.nan
    merge_time = pd.Series([datetime(2022,8,6)+timedelta(seconds=ts) for ts in Data['Time_Start']])
        
    # %% plot vertical profiles
    #xdata = Data['N2O_PODOLSKE']
    #xdata = Data['N2O_COLD2_ppbv_VICIANI']
    xdata = Data['N2O_PODOLSKE'] - Data['N2O_COLD2_ppbv_VICIANI']
    
    ydata = Data['G_ALT_MMS_BUI']/1000
    bins = np.arange(0,19.5,step=0.5)
    bins_plot = np.arange(0.25,19.25,step=0.5)
    
    #ydata = Data['P_MMS_BUI']
    #bins = np.arange(60,300,step=20)
    #bins_plot = np.arange(70,290,step=20)
    
    from scipy.stats import binned_statistic
    
    mean_stat = binned_statistic(ydata, xdata, statistic=np.nanmean, bins=bins)
    
    msize=3
    plt.plot(mean_stat.statistic,bins_plot)
    #ax.plot(xdata,ydata,'-',markersize=msize)
    ax.set_xlabel('$N_2O$ (COMA-COLD2) ppb')
    
    ax.set_ylabel('Altitude, km')
    ax.set_ylim(10,19.5)
    
    #ax.set_ylabel('Pressure, mb')
    #ax.invert_yaxis()

    ax.grid()
    
    #fig.suptitle(case_name)
    fig.tight_layout()
    #fig2.savefig('./plots/' + case_name + '_profile.png',dpi=300)
    #plt.close(fig2)
