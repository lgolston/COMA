# -*- coding: utf-8 -*-
"""
Compare COLD2, ACOS, and COMA CO measurements
"""

# %% header
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.dates as mdates
from load_flight_functions import read_COMA
import statsmodels.api as sm

case = 'RF14'
to_plot = 'CO' # CO, CO-H2O, or corr

# %% list file names
if case == 'Transit1': # Ellington to Seattle
    filename_ACOS = '../Data/_OtherData_/ACCLIP-ACOS-1Hz_WB57_20220721_RA_1.ict'
    filename_COLD2 = '../Data/_OtherData_/acclip-COLD2-CO_WB57_20220721_RA_L1.ict'
    filename_COMA = ['../Data/2022-07-21/n2o-co_2022-07-21_f0000.txt',
                     '../Data/2022-07-21/n2o-co_2022-07-21_f0001.txt']
    filename_DLH = None
    
elif case == 'Transit2': # Seattle to Anchorage
    filename_ACOS = '../Data/_OtherData_/ACCLIP-ACOS-1Hz_WB57_20220721_RA_2.ict'
    filename_COLD2 = '../Data/_OtherData_/acclip-COLD2-CO_WB57_20220721_RA_L2.ict'
    filename_COMA = ['../Data/2022-07-21/n2o-co_2022-07-21_f0002.txt']
    filename_DLH = None
    
elif case == 'Transit3': # Anchorage to Adak
    filename_ACOS = '../Data/_OtherData_/ACCLIP-ACOS-1Hz_WB57_20220724_RA.ict'
    filename_COLD2 = '../Data/_OtherData_/acclip-COLD2-CO_WB57_20220724_RA.ict'
    filename_COMA = ['../Data/2022-07-24/n2o-co_2022-07-24_f0000.txt']
    filename_DLH = None
    
elif case == 'Transit4': # Adak to Misawa
    filename_ACOS = '../Data/_OtherData_/ACCLIP-ACOS-1Hz_WB57_20220725_RA.ict'
    filename_COLD2 = '../Data/_OtherData_/acclip-COLD2-CO_WB57_20220725_RA.ict'
    filename_COMA = ['../Data/2022-07-25/n2o-co_2022-07-25_f0000.txt']
    filename_DLH = None
    
elif case == 'Transit5': # Misawa to Osan
    filename_ACOS = '../Data/_OtherData_/ACCLIP-ACOS-1Hz_WB57_20220727_RA.ict'
    filename_COLD2 = '../Data/_OtherData_/acclip-COLD2-CO_WB57_20220727_RA.ict'
    filename_COMA = ['../Data/2022-07-27/n2o-co_2022-07-27_f0000.txt']
    filename_DLH = None
    
elif case == 'RF03': # Osan
    filename_ACOS = '../Data/_OtherData_/ACCLIP-ACOS-1Hz_WB57_20220802_RA.ict'
    filename_COLD2 = '../Data/_OtherData_/acclip-COLD2-CO_WB57_20220802_RA.ict'
    filename_COMA = ['../Data/2022-08-02/n2o-co_2022-08-02_f0000.txt']
    filename_DLH = None
    
elif case == 'RF04': # Osan
    filename_ACOS = '../Data/_OtherData_/ACCLIP-ACOS-1Hz_WB57_20220804_RA.ict'
    filename_COLD2 = '../Data/_OtherData_/acclip-COLD2-CO_WB57_20220804_RA.ict'
    filename_COMA = ['../Data/2022-08-04/n2o-co_2022-08-04_f0000.txt']
    filename_DLH = '../Data/_OtherData_/ACCLIP-DLH-H2O_WB57_20220804_RA.ict'
    
elif case == 'RF05': # Osan
    filename_ACOS = '../Data/_OtherData_/ACCLIP-ACOS-1Hz_WB57_20220806_RA.ict'
    filename_COLD2 = '../Data/_OtherData_/acclip-COLD2-CO_WB57_20220806_RA.ict'
    filename_COMA = ['../Data/2022-08-06/n2o-co_2022-08-06_f0000.txt']
    filename_DLH = '../Data/_OtherData_/ACCLIP-DLH-H2O_WB57_20220806_RA.ict'
    
elif case == 'RF06': # Osan
    filename_ACOS = '../Data/_OtherData_/ACCLIP-ACOS-1Hz_WB57_20220812_RA.ict'
    filename_COLD2 = '../Data/_OtherData_/acclip-COLD2-CO_WB57_20220812_RA.ict'
    filename_COMA = ['../Data/2022-08-12/n2o-co_2022-08-12_f0000.txt']
    filename_DLH = '../Data/_OtherData_/ACCLIP-DLH-H2O_WB57_20220812_RA.ict'
    
elif case == 'RF07': # Osan
    filename_ACOS = '../Data/_OtherData_/ACCLIP-ACOS-1Hz_WB57_20220813_RA.ict'
    filename_COLD2 = '../Data/_OtherData_/acclip-COLD2-CO_WB57_20220813_RA.ict'
    filename_COMA = ['../Data/2022-08-13/n2o-co_2022-08-13_f0000.txt']
    filename_DLH = '../Data/_OtherData_/ACCLIP-DLH-H2O_WB57_20220813_RA.ict'
    
elif case == 'RF08': # Osan
    filename_ACOS = '../Data/_OtherData_/ACCLIP-ACOS-1Hz_WB57_20220815_RA.ict'
    filename_COLD2 = '../Data/_OtherData_/acclip-COLD2-CO_WB57_20220815_RA.ict'
    filename_COMA = ['../Data/2022-08-15/n2o-co_2022-08-15_f0000.txt',
                     '../Data/2022-08-15/n2o-co_2022-08-15_f0001.txt']
    filename_DLH = '../Data/_OtherData_/ACCLIP-DLH-H2O_WB57_20220815_RA.ict'
    
elif case == 'RF09': # Osan
    filename_ACOS = '../Data/_OtherData_/ACCLIP-ACOS-1Hz_WB57_20220816_RA.ict'
    filename_COLD2 = '../Data/_OtherData_/acclip-COLD2-CO_WB57_20220816_RA.ict'
    filename_COMA = ['../Data/2022-08-16/n2o-co_2022-08-16_f0000.txt']
    filename_DLH = '../Data/_OtherData_/ACCLIP-DLH-H2O_WB57_20220816_RA.ict'
    
elif case == 'RF10': # Osan
    filename_ACOS = '../Data/_OtherData_/ACCLIP-ACOS-1Hz_WB57_20220819_RB.ict'
    filename_COLD2 = '../Data/_OtherData_/acclip-COLD2-CO_WB57_20220819_RA.ict'
    filename_COMA = ['../Data/2022-08-18/n2o-co_2022-08-18_f0000.txt']
    filename_DLH = '../Data/_OtherData_/ACCLIP-DLH-H2O_WB57_20220819_RA.ict'

elif case == 'RF11': # Osan
    filename_ACOS = '../Data/_OtherData_/ACCLIP-ACOS-1Hz_WB57_20220821_RB.ict'
    filename_COLD2 = '../Data/_OtherData_/acclip-COLD2-CO_WB57_20220821_RA.ict'
    filename_COMA = ['../Data/2022-08-21/n2o-co_2022-08-21_f0000.txt']
    filename_DLH = '../Data/_OtherData_/ACCLIP-DLH-H2O_WB57_20220821_RA.ict'

elif case == 'RF12': # Osan
    filename_ACOS = '../Data/_OtherData_/ACCLIP-ACOS-1Hz_WB57_20220823_RC.ict'
    filename_COLD2 = '../Data/_OtherData_/acclip-COLD2-CO_WB57_20220823_RA.ict'
    filename_COMA = ['../Data/2022-08-23/n2o-co_2022-08-23_f0000.txt']
    filename_DLH = '../Data/_OtherData_/ACCLIP-DLH-H2O_WB57_20220823_RA.ict'

elif case == 'RF13': # Osan
    filename_ACOS = '../Data/_OtherData_/ACCLIP-ACOS-1Hz_WB57_20220825_RA.ict'
    filename_COLD2 = '../Data/_OtherData_/acclip-COLD2-CO_WB57_20220825_RA.ict'
    filename_COMA = ['../Data/2022-08-24/n2o-co_2022-08-24_f0002.txt']
    filename_DLH = '../Data/_OtherData_/ACCLIP-DLH-H2O_WB57_20220825_RA.ict'

elif case == 'RF14': # Osan
    filename_ACOS = '../Data/_OtherData_/ACCLIP-ACOS-1Hz_WB57_20220826_RA.ict'
    filename_COLD2 = '../Data/_OtherData_/acclip-COLD2-CO_WB57_20220826_RA.ict'
    filename_COMA = ['../Data/2022-08-26/n2o-co_2022-08-26_f0000.txt']
    filename_DLH = '../Data/_OtherData_/ACCLIP-DLH-H2O_WB57_20220826_RA.ict'
    
# %% ICARTT file loading functions
def read_ACOS_ict(filename):
    # e.g. ACCLIP-ACOS-1Hz_WB57_20220816_RA.ict
    cur_day = datetime.strptime(filename[-15:-7],"%Y%m%d") # get date from end of file name
    ACOS = pd.read_csv(filename,sep=',',header=37)
    ACOS['time'] = [cur_day+timedelta(seconds=t) for t in ACOS['TIME_START']]
    return ACOS

def read_COLD2_ict(filename):
    # e.g. acclip-COLD2-CO_WB57_20220816_RA.ict
    cur_day = datetime.strptime(filename[-15:-7],"%Y%m%d")
    COLD2 = pd.read_csv(filename,sep=',',header=32)
    COLD2['time'] = [cur_day+timedelta(seconds=t) for t in COLD2['Time_Start']]
    return COLD2

def read_DLH_ict(filename):
    # e.g. ACCLIP-DLH-H2O_WB57_20220816_RA.ict
    cur_day = datetime.strptime(filename[-15:-7],"%Y%m%d")
    DLH = pd.read_csv(filename,sep=',',header=35)
    DLH['time'] = [cur_day+timedelta(seconds=t) for t in DLH['Time_Start']]
    return DLH

# load COMA file
COMA, inlet_ix = read_COMA(filename_COMA)

if case == 'RF13': # fix clock setting on this day
    COMA['time'] = COMA['time'] + timedelta(hours=6)
    
# set plot style
plt.rc('axes', labelsize=11) # xaxis and yaxis labels
plt.rc('xtick', labelsize=11) # xtick labels
plt.rc('ytick', labelsize=11) # ytick labels
plt.rc('legend', fontsize=11) # ytick labels

# %% Plot CO time series from COMA, ACOS, COLD2
if to_plot == 'CO':
    fig, ax = plt.subplots(1, 1, figsize=(8,4))
    
    # ict files for each are 1 Hz data
    
    # load and plot ACOS
    if filename_ACOS:
        ACOS = read_ACOS_ict(filename_ACOS)
        plt.plot(ACOS['time'],ACOS['ACOS_CO_PPB'],'.m',label='ACOS',markersize=2)
    
    # plot COMA
    plt.plot(COMA['time'][inlet_ix],COMA["      [CO]d_ppm"][inlet_ix]*1000,'b.',label='COMA',markersize=2)
     
    # load and plot COLD2
    if filename_COLD2:
        COLD2 = read_COLD2_ict(filename_COLD2)
        plt.plot(COLD2['time'],COLD2[' CO_COLD2_ppbv'],'.g',label='COLD2',markersize=2)
    
    ax.set_ylabel('CO, ppb')
    ax.set_ylim([-10,400])
    #ax.set_ylim([-10,300])
    ax.grid('on')
    ax.legend()
    ax.set_title(case)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    fig.tight_layout()
    
# %% Plot CO time series and DLH H2O
if to_plot == 'CO-H2O':
    fig, ax = plt.subplots(1, 1, figsize=(8,4))
    ax_twin = ax.twinx()
    
    # load DLH
    if filename_DLH:
        DLH = read_DLH_ict(filename_DLH)
        ax_twin.plot(DLH['time'],DLH['H2O_DLH'],'.k',label='DLH')
        #ax_twin.plot(DLH_time,DLH['RHw_DLH'],'.k',label='DLH')
    
    # plot COMA
    ax.plot(COMA['time'][inlet_ix],COMA["      [CO]d_ppm"][inlet_ix]*1000,'b.',label='COMA')
    #ax_twin.plot(COMA['time'][ix_8],COMA["      [H2O]_ppm"][ix_8]*1000,'y.',label='COMA-H2O')

    ax_twin.set_ylabel('DLH water vapor mixing ratio, ppmv') 
    ax_twin.set_yscale('log')

    ax.set_ylim(0,500)
    ax.set_ylabel('CO, ppb',color='b')
    ax.tick_params(axis='y', colors='blue')
    ax.grid('on')
    ax.set_title(case)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    fig.tight_layout()
   
# %% correlation plots
# COMA CO vs ACOS
# COMA CO vs COLD2
# COMA H2O vs DLH H2O

def sync_ab(df_a,df_b):   
    # clear missing, ULOD, and LLOD flagged values
    # (not relevant for non-ICARTT COMA data file = df_a)
    tmp = df_b.iloc[:,1]
    tmp[tmp<-600] = np.nan
    df_b.iloc[:,1] = tmp
    
    # create common timestamp
    a_1Hz = df_a.groupby(pd.Grouper(key="time", freq="5s")).mean()
    b_1Hz = df_b.groupby(pd.Grouper(key="time", freq="5s")).mean()
    sync_data = pd.merge(a_1Hz, b_1Hz, how='inner', on=['time'])
    sync_data = sync_data.dropna()

    # linear regression
    col_names = sync_data.columns
    model = sm.OLS(sync_data[col_names[1]],sm.add_constant(sync_data[col_names[0]]))
    results = model.fit()
    return sync_data, results

if to_plot == 'corr':
    fig, ax = plt.subplots(1, 3, figsize=(12,4))
        
    # load ACOS
    if filename_ACOS:
        ACOS = read_ACOS_ict(filename_ACOS)
        
        df_a = pd.DataFrame({'time': COMA['time'][inlet_ix], 'CO_COMA': COMA["      [CO]d_ppm"][inlet_ix]*1000})
        df_b = pd.DataFrame({'time': ACOS['time'], 'CO_ACOS': ACOS['ACOS_CO_PPB']})
        sync_data, results = sync_ab(df_a,df_b)
        ax[0].plot(sync_data['CO_COMA'],sync_data['CO_ACOS'],'k.')
        ax[0].text(0.05,0.93,'y = ' + "{:.3f}".format(results.params[1]) + 'x + ' + "{:.3f}".format(results.params[0]),transform=ax[0].transAxes)
        ax[0].text(0.05,0.87,'R2 = ' + "{:.3f}".format(results.rsquared),transform=ax[0].transAxes)
        
    # load COLD2
    if filename_COLD2:
        COLD2 = read_COLD2_ict(filename_COLD2)
        
        df_a = pd.DataFrame({'time': COMA['time'][inlet_ix], 'CO_COMA': COMA["      [CO]d_ppm"][inlet_ix]*1000})
        df_b = pd.DataFrame({'time': COLD2['time'], 'CO_COLD2': COLD2[' CO_COLD2_ppbv']})
        sync_data, results = sync_ab(df_a,df_b)
        ax[1].plot(sync_data['CO_COMA'],sync_data['CO_COLD2'],'k.')
        ax[1].text(0.05,0.93,'y = ' + "{:.3f}".format(results.params[1]) + 'x + ' + "{:.3f}".format(results.params[0]),transform=ax[1].transAxes)
        ax[1].text(0.05,0.87,'R2 = ' + "{:.3f}".format(results.rsquared),transform=ax[1].transAxes)
        
    # load DLH
    if filename_DLH:
        DLH = read_DLH_ict(filename_DLH)

        df_a = pd.DataFrame({'time': COMA['time'][inlet_ix], 'H2O_COMA': COMA["      [H2O]_ppm"][inlet_ix]})
        df_b = pd.DataFrame({'time': DLH['time'], 'H2O_DLH': DLH['H2O_DLH']})
        sync_data, results = sync_ab(df_a,df_b)
        ax[2].plot(sync_data['H2O_COMA'],sync_data['H2O_DLH'],'k.')
        ax[2].text(0.05,0.93,'y = ' + "{:.3f}".format(results.params[1]) + 'x + ' + "{:.3f}".format(results.params[0]),transform=ax[2].transAxes)
        ax[2].text(0.05,0.87,'R2 = ' + "{:.3f}".format(results.rsquared),transform=ax[2].transAxes)
    
    # format plots
    ax[0].set_xlabel('COMA CO, ppbv')
    ax[0].set_ylabel('ACOS CO, ppbv')
    
    ax[1].set_xlabel('COMA CO, ppbv')
    ax[1].set_ylabel('COLD2 CO, ppbv')
    
    ax[2].set_xlabel('COMA H2O, ppmv')
    ax[2].set_ylabel('DLH H2O, ppmv')
    
    ax[0].plot([0,350],[0,350],'k:')
    ax[0].set_xlim([0,350])
    ax[0].set_ylim([0,350])
    
    ax[1].plot([0,350],[0,350],'k:')
    ax[1].set_xlim([0,350])
    ax[1].set_ylim([0,350])
    
    ax[2].plot([0,30000],[0,30000],'k:')
    
    fig.tight_layout()
    
    #fig.savefig('fig1.png',dpi=300)

# %% debugging
"""
MIU = COMA["      MIU_VALVE"]
fig, ax = plt.subplots(1, 1, figsize=(8,4))
ax_twin = ax.twinx()
ax.plot(MIU,'b.')
ax_twin.plot( ((MIU==8) & (MIU.shift(30)==8)) ,'k.')
ax_twin.set_ylim(-0.5,1.5) # shift to prevent dots from overlapping
"""