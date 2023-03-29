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

"""
filenames_1s = \
['acclip-mrg1_wb57_20220716_RA_20221111T194210.ict', #
 'acclip-mrg1_wb57_20220718_RA_20221111T194212.ict', # 
 'acclip-mrg1_wb57_20220721_RA_20221111T194215.ict', # 
 'acclip-mrg1_wb57_20220724_RA_20221111T194216.ict', # 
 'acclip-mrg1_wb57_20220725_RA_20221111T194217.ict', #
 'acclip-mrg1_wb57_20220727_RA_20221111T194218.ict', # 
 'acclip-mrg1_wb57_20220802_RA_20221111T194220.ict', #
 'acclip-mrg1_wb57_20220804_RA_20221111T194221.ict', #
 'acclip-mrg1_wb57_20220806_RA_20221111T194223.ict', #
 'acclip-mrg1_wb57_20220812_RA_20221111T194225.ict', #
 'acclip-mrg1_wb57_20220813_RA_20221111T194226.ict', #
 'acclip-mrg1_wb57_20220815_RA_20221111T194228.ict', #
 'acclip-mrg1_wb57_20220816_RA_20221111T194230.ict', #
 'acclip-mrg1_wb57_20220819_RA_20221111T194231.ict', #
 'acclip-mrg1_wb57_20220821_RA_20221111T194233.ict', #
 'acclip-mrg1_wb57_20220823_RA_20221111T194235.ict', #
 'acclip-mrg1_wb57_20220825_RA_20221111T194237.ict', #
 'acclip-mrg1_wb57_20220826_RA_20221111T194239.ict', #
 'acclip-mrg1_wb57_20220829_RA_20221111T194241.ict', #
 'acclip-mrg1_wb57_20220831_RA_20221111T194242.ict', #
 'acclip-mrg1_wb57_20220901_RA_20221111T194244.ict', #
 'acclip-mrg1_wb57_20220909_RA_20221111T194245.ict', #
 'acclip-mrg1_wb57_20220912_RA_20221111T194246.ict', #
 'acclip-mrg1_wb57_20220913_RA_20221111T194248.ict', # 
 'acclip-mrg1_wb57_20220914_RA_20221111T194249.ict'] # 
"""

filenames_60s = \
[['acclip-mrg60_wb57_20220716_RA_20221111T194045.ict','20220716_RF01'], #0-RF1 (Houston)
 ['acclip-mrg60_wb57_20220718_RA_20221111T194046.ict','20220718_RF02'], #1-RF2 (Houston)
 ['acclip-mrg60_wb57_20220721_RA_20221111T194046.ict','20220721_Transit'], #2-Transit1 and (Transit2?)
 ['acclip-mrg60_wb57_20220724_RA_20221111T194047.ict','20220724_Transit'], #3-Transit3
 ['acclip-mrg60_wb57_20220725_RA_20221111T194047.ict','20220725_Transit'], #4-Transit4
 ['acclip-mrg60_wb57_20220727_RA_20221111T194047.ict','20220727_Transit'], #5-Transit5
 ['acclip-mrg60_wb57_20220802_RA_20221111T194047.ict','20220802_RF03'], #6-RF03
 ['acclip-mrg60_wb57_20220804_RA_20221111T194048.ict','20220804_RF04'], #7-RF04
 ['acclip-mrg60_wb57_20220806_RA_20221111T194048.ict','20220806_RF05'], #8-RF05
 ['acclip-mrg60_wb57_20220812_RA_20221111T194049.ict','20220812_RF06'], #9-RF06
 ['acclip-mrg60_wb57_20220813_RA_20221111T194049.ict','20220813_RF07'], #10-RF07
 ['acclip-mrg60_wb57_20220815_RA_20221111T194049.ict','20220815_RF08'], #11-RF08
 ['acclip-mrg60_wb57_20220816_RA_20221111T194050.ict','20220816_RF09'], #12-RF09
 ['acclip-mrg60_wb57_20220819_RA_20221111T194050.ict','20220819_RF10'], #13-RF10
 ['acclip-mrg60_wb57_20220821_RA_20221111T194050.ict','20220821_RF11'], #14-RF11
 ['acclip-mrg60_wb57_20220823_RA_20221111T194051.ict','20220823_RF12'], #15-RF12
 ['acclip-mrg60_wb57_20220825_RA_20221111T194051.ict','20220825_RF13'], #16-RF13
 ['acclip-mrg60_wb57_20220826_RA_20221111T194052.ict','20220826_RF14'], #17-RF14
 ['acclip-mrg60_wb57_20220829_RA_20221111T194052.ict','20220829_RF15'], #18-RF15
 ['acclip-mrg60_wb57_20220831_RA_20221111T194052.ict','20220831_RF16'], #19-RF16
 ['acclip-mrg60_wb57_20220901_RA_20221111T194053.ict','20220901_RF17'], #20-RF17
 ['acclip-mrg60_wb57_20220909_RA_20221111T194053.ict','20220909_Transit'], #21-Transit6
 ['acclip-mrg60_wb57_20220912_RA_20221111T194053.ict','20220912_Transit'], #22-Transit7
 ['acclip-mrg60_wb57_20220913_RA_20221111T194054.ict','20220913_Transit'], #23-Transit8
 ['acclip-mrg60_wb57_20220914_RA_20221111T194054.ict','20220914_Transit']] #24-Transit9

# set plot style
plt.rcParams['axes.labelsize'] = 8
plt.rcParams['xtick.labelsize'] = 7
plt.rcParams['ytick.labelsize'] = 7
plt.rcParams['legend.fontsize'] = 7
plt.rcParams['font.size']=8
plt.rcParams.update({'mathtext.default': 'regular' } ) # not italics

# %% load and plot
for case in range(8,9):
    # %% load and prepare data
    filename = '../Data/_Merge_/'+filenames_60s[case][0]
    case_name = filenames_60s[case][1]
    
    Data = pd.read_csv(filename,sep=',',header=88,skipinitialspace=True,low_memory=False)
    
    Data[Data==-999999] = np.nan
    
    alt_km = Data['G_ALT_MMS_BUI']/1000
    
    # find maxima
    from scipy.signal import find_peaks
    maxima, _ = find_peaks(Data['G_ALT_MMS_BUI'], prominence=1000)
    
    #minima, _ = find_peaks(-Data['G_ALT_MMS_BUI'], prominence=1000)
    #minima = np.union1d(0,minima)
    #minima = np.union1d(minima,len(Data))
    
    #generate list of indices
    ix_list = []
    if 'Transit' in case_name:
        ix_list.append(np.ravel(np.where(alt_km>10)))
    else:
        ix_list.append(np.ravel(np.where((alt_km.index<maxima[0]) & (alt_km>10)))) # ascent
        for ii in range(len(maxima)-1):
            ix_list.append(range(maxima[ii],maxima[ii+1]))
        ix_list.append(np.ravel(np.where((alt_km.index>maxima[-1]) & (alt_km>10)))) # descent
    
    # convert GEOS trop pressure to altitude
    # (common barometric formula not accurate in UTLS)
    xp = Data['P_MMS_BUI']
    yp = Data['G_ALT_MMS_BUI']
    idx = np.isfinite(xp) & np.isfinite(yp)
    poly = np.polyfit(xp[idx], yp[idx], 2)
    trop_height = np.polyval(poly,Data['TROPPB_GEOS_NEWMAN'])/1000
    
    # timestamp
    merge_time = pd.Series([datetime(2022,8,6)+timedelta(seconds=ts) for ts in Data['Time_Start']])
    
    # %% plot time series of altitude
    fig1, ax1 = plt.subplot_mosaic([['A', 'A'],
                                    ['B', 'C']],
                                  figsize=(6, 4.5))
    
    ax1["A"].plot(merge_time,trop_height,'k:',label='GEOS TROP')
    
    msize = 3
    
    for ii, ix in enumerate(ix_list):
        ax1["A"].plot(merge_time[ix],alt_km[ix],label=('prof'+str(ii)))
        ax1["B"].plot(Data['CO_PODOLSKE'][ix],Data['N2O_PODOLSKE'][ix],'.',markersize=msize)
        if 'O3_ppb_THORNBERRY' in Data:
            ax1["C"].plot(Data['CO_PODOLSKE'][ix],Data['O3_ppb_THORNBERRY'][ix],'.',markersize=msize)
        
    ax1["A"].legend(ncol=3)
    ax1["A"].set_ylim([10,20])
    ax1["A"].set_ylabel('Altitude, km')
    
    ax1["B"].invert_yaxis()
    ax1["B"].set_xlabel("CO (COMA), ppb")
    ax1["B"].set_ylabel("$N_2O$ (COMA), ppb")
    
    ax1["C"].set_xlabel("CO (COMA), ppb")
    ax1["C"].set_ylabel("$O_3$ (UASO3), ppb")
    
    ax1["A"].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    fig1.suptitle(case_name)
    fig1.tight_layout()
    #fig1.savefig('./plots/' + case_name + '_div_scatterplots.png',dpi=300)
    #plt.close(fig1)
    
    # %% plot vertical profiles
    fig2, ax2 = plt.subplots(3, 2, figsize=(6,5),sharey=True)
    
    vert_coord = 'alt' # alt or theta

    for ix in ix_list:
        if vert_coord == 'alt':
            ydata = Data['G_ALT_MMS_BUI'][ix]/1000
        else:
            #ydata = Data['EPV_GEOS_NEWMAN'][ix]*1E6
            #ydata = Data['POT_MMS_BUI'][ix]
            ydata = Data['POTT_GEOS_NEWMAN'][ix]
        
        p0 = ax2[0,0].plot(Data['EPV_GEOS_NEWMAN'][ix]*1E6,ydata,'.',markersize=msize)
        ax2[0,1].plot(Data['POT_MMS_BUI'][ix],ydata,'.',markersize=msize)
        ax2[1,0].plot(Data['CO_PODOLSKE'][ix],ydata,'.',markersize=msize)
        ax2[1,1].plot(Data['N2O_PODOLSKE'][ix],ydata,'.',markersize=msize)
        if 'O3_ppb_THORNBERRY' in Data:
            ax2[2,0].plot(Data['O3_ppb_THORNBERRY'][ix],ydata,'.',markersize=msize)
        if 'H2O_DLH_DISKIN' in Data:
            ax2[2,1].plot(Data['H2O_DLH_DISKIN'][ix],ydata,'.',markersize=msize)
            
        if vert_coord == 'alt':
            ax2[0,0].axhline(np.mean(trop_height[ix]),linestyle=':',color=p0[0].get_color(),markersize=msize)
    
    ax2[0,0].set_xlabel('EPV, $10^{-6}$ $m^{2}$ $s^{-1}$ K $kg^{-1}$')
    ax2[0,1].set_xlabel('Pot T, K')  
    ax2[1,0].set_xlabel('CO, ppb')
    ax2[1,1].set_xlabel('$N_2O$, ppb')
    ax2[2,0].set_xlabel('$O_3$, ppb')
    ax2[2,1].set_xlabel('$H_2O$, ppm')
    
    if vert_coord == 'alt':
        ax2[0,0].set_ylim(10,20)
        ax2[0,0].set_ylabel('Altitude, km')
        ax2[0,1].set_ylabel('Altitude, km')
        ax2[1,0].set_ylabel('Altitude, km')
        ax2[1,1].set_ylabel('Altitude, km')
        ax2[2,0].set_ylabel('Altitude, km')
        ax2[2,1].set_ylabel('Altitude, km')
    else:
        1
        #ax2[0,0].set_ylim(330,450)
    
    fig2.suptitle(case_name)
    fig2.tight_layout()
    #fig2.savefig('./plots/' + case_name + '_profile.png',dpi=300)
    #plt.close(fig2)
