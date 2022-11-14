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

# %% linear regression
def regress(xp,yp):
    idx = np.isfinite(xp) & np.isfinite(yp)
    p = np.polyfit(xp[idx], yp[idx], 1)
    return p
    
# %% load and plot
for case in range(0,25):
    # %%
    # load file
    filename = '../Data/_Merge_/'+filenames_60s[case][0]
    case_name = filenames_60s[case][1]
    
    Data = pd.read_csv(filename,sep=',',header=88,skipinitialspace=True,low_memory=False)
    
    Data[Data==-999999] = np.nan
    
    # timestamp
    merge_time = pd.Series([datetime(2022,8,6)+timedelta(seconds=ts) for ts in Data['Time_Start']])
    
    # %% plot time series    
    fig1, ax1 = plt.subplot_mosaic([['A', 'A', 'C'],
                                    ['B', 'B', 'D']],
                                  figsize=(6, 4))
        
    # time series
    ax1["A"].plot(merge_time,Data['CO_COLD2_ppbv_VICIANI'],'m',label='COLD2')
    ax1["A"].plot(merge_time,Data['CO_GEOS_NEWMAN']*1E9,'g',label='GEOS')
    ax1["A"].plot(merge_time,Data['ACOS_CO_PPB_GURGANUS'],'b',label='ACOS')
    ax1["A"].plot(merge_time,Data['CO_PODOLSKE'],'c--',label='COMA')
    ax1["A"].set_ylabel('CO, ppb')
    ax1["A"].legend(ncols=2)
    ax1["A"].grid()
    
    ax1["B"].plot(merge_time,Data['N2O_COLD2_ppbv_VICIANI'],'m',label='COLD2')
    ax1["B"].plot(merge_time,Data['N2O_PODOLSKE'],'c--',label='COMA')
    ax1["B"].set_ylabel("$N_2O$, ppb")
    ax1["B"].legend()
    ax1["A"].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax1["B"].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax1["B"].grid()
    
    # correlations
    msize = 1.5
    
    ax1["C"].plot(Data['CO_PODOLSKE'],Data['CO_COLD2_ppbv_VICIANI'],'m.',markersize=msize)
    ax1["C"].plot(Data['CO_PODOLSKE'],Data['CO_GEOS_NEWMAN']*1E9,'g.',markersize=msize)
    ax1["C"].plot(Data['CO_PODOLSKE'],Data['ACOS_CO_PPB_GURGANUS'],'b.',markersize=msize)
    min_val = np.min((np.min(Data['CO_PODOLSKE']),np.min(Data['CO_COLD2_ppbv_VICIANI']),np.min(Data['CO_GEOS_NEWMAN']*1E9)))
    max_val = np.max((np.max(Data['CO_PODOLSKE']),np.max(Data['CO_COLD2_ppbv_VICIANI']),np.max(Data['CO_GEOS_NEWMAN']*1E9)))
    ax1["C"].plot([min_val,max_val],[min_val,max_val],'k:')
    
    ax1["C"].set_xlabel('CO (COMA), ppb')
    ax1["C"].set_ylabel('CO (COLD2/GEOS), ppb')
    ax1["C"].grid()
        
    ax1["D"].plot(Data['N2O_PODOLSKE'],Data['N2O_COLD2_ppbv_VICIANI'],'m.',markersize=msize)
    min_val = np.min((np.min(Data['N2O_PODOLSKE']),np.min(Data['N2O_COLD2_ppbv_VICIANI'])))
    max_val = np.max((np.max(Data['N2O_PODOLSKE']),np.max(Data['N2O_COLD2_ppbv_VICIANI'])))
    ax1["D"].plot([min_val,max_val],[min_val,max_val],'k:')
    
    ax1["D"].set_xlabel('$N_2O$ (COMA), ppb')
    ax1["D"].set_ylabel('$N_2O$ (COLD2), ppb')
    ax1["D"].grid()
    
    # add linear regressions
    p = regress(Data['CO_PODOLSKE'],Data['CO_COLD2_ppbv_VICIANI'])
    ax1["C"].text(0.05,0.91,"{:.3f}".format(p[0])+"x + {:.1f}".format(p[1]),transform=ax1["C"].transAxes,fontsize=5,color='m')
    p = regress(Data['CO_PODOLSKE'],Data['CO_GEOS_NEWMAN']*1E9)
    ax1["C"].text(0.05,0.83,"{:.3f}".format(p[0])+"x + {:.1f}".format(p[1]),transform=ax1["C"].transAxes,fontsize=5,color='g')
    p = regress(Data['CO_PODOLSKE'],Data['ACOS_CO_PPB_GURGANUS'])
    ax1["C"].text(0.05,0.75,"{:.3f}".format(p[0])+"x + {:.1f}".format(p[1]),transform=ax1["C"].transAxes,fontsize=5,color='b')
    
    p = regress(Data['N2O_PODOLSKE'],Data['N2O_COLD2_ppbv_VICIANI'])
    ax1["D"].text(0.05,0.87,"{:.3f}".format(p[0])+"x + {:.1f}".format(p[1]),transform=ax1["D"].transAxes,fontsize=5,color='m')
    
    # final formatting of plots    
    fig1.suptitle(case_name)
    fig1.tight_layout()
    fig1.savefig('./plots/' + case_name + '_comparison.png',dpi=300)
    plt.close(fig1)
