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

case = 'RF09'
to_plot = 'CO' # CO, CO-H2O, corr

# %% list file names
filename_DLH = None

if case == 'Transit1': # Ellington to Seattle
    filename_ACOS = '../Data/_OtherData_/ACCLIP-ACOS-1Hz_WB57_20220721_RA_1.ict'
    filename_COLD2 = '../Data/_OtherData_/acclip-COLD2-CO_WB57_20220721_RA_L1.ict'
    filename_COMA = ['../Data/2022-07-21/n2o-co_2022-07-21_f0000.txt',
                     '../Data/2022-07-21/n2o-co_2022-07-21_f0001.txt']
    cur_day = datetime(2022,7,21)
elif case == 'Transit2': # Seattle to Anchorage
    filename_ACOS = '../Data/_OtherData_/ACCLIP-ACOS-1Hz_WB57_20220721_RA_2.ict'
    filename_COLD2 = '../Data/_OtherData_/acclip-COLD2-CO_WB57_20220721_RA_L2.ict'
    filename_COMA = ['../Data/2022-07-21/n2o-co_2022-07-21_f0002.txt']
    cur_day = datetime(2022,7,21)
elif case == 'Transit3': # Anchorage to Adak
    filename_ACOS = '../Data/_OtherData_/ACCLIP-ACOS-1Hz_WB57_20220724_RA.ict'
    filename_COLD2 = '../Data/_OtherData_/acclip-COLD2-CO_WB57_20220724_RA.ict'
    filename_COMA = ['../Data/2022-07-24/n2o-co_2022-07-24_f0000.txt']
    cur_day = datetime(2022,7,24)
elif case == 'Transit4': # Adak to Misawa
    filename_ACOS = '../Data/_OtherData_/ACCLIP-ACOS-1Hz_WB57_20220725_RA.ict'
    filename_COLD2 = '../Data/_OtherData_/acclip-COLD2-CO_WB57_20220725_RA.ict'
    filename_COMA = ['../Data/2022-07-25/n2o-co_2022-07-25_f0000.txt']
    cur_day = datetime(2022,7,25)
elif case == 'Transit5': # Misawa to Osan
    filename_ACOS = '../Data/_OtherData_/ACCLIP-ACOS-1Hz_WB57_20220727_RA.ict'
    filename_COLD2 = '../Data/_OtherData_/acclip-COLD2-CO_WB57_20220727_RA.ict'
    filename_COMA = ['../Data/2022-07-27/n2o-co_2022-07-27_f0000.txt']
    cur_day = datetime(2022,7,27)
elif case == 'RF03': # Osan
    filename_ACOS = '../Data/_OtherData_/ACCLIP-ACOS-1Hz_WB57_20220802_RA.ict'
    filename_COLD2 = '../Data/_OtherData_/acclip-COLD2-CO_WB57_20220802_RA.ict'
    filename_COMA = ['../Data/2022-08-02/n2o-co_2022-08-02_f0000.txt']
    cur_day = datetime(2022,8,2)
elif case == 'RF04': # Osan
    filename_ACOS = '../Data/_OtherData_/ACCLIP-ACOS-1Hz_WB57_20220804_RA.ict'
    filename_COLD2 = '../Data/_OtherData_/acclip-COLD2-CO_WB57_20220804_RA.ict'
    filename_COMA = ['../Data/2022-08-04/n2o-co_2022-08-04_f0000.txt']
    filename_DLH = '../Data/_OtherData_/ACCLIP-DLH-H2O_WB57_20220804_RA.ict'
    cur_day = datetime(2022,8,4)
elif case == 'RF05': # Osan
    filename_ACOS = '../Data/_OtherData_/ACCLIP-ACOS-1Hz_WB57_20220806_RA.ict'
    filename_COLD2 = '../Data/_OtherData_/acclip-COLD2-CO_WB57_20220806_RA.ict'
    filename_COMA = ['../Data/2022-08-06/n2o-co_2022-08-06_f0000.txt']
    filename_DLH = '../Data/_OtherData_/ACCLIP-DLH-H2O_WB57_20220806_RA.ict'
    cur_day = datetime(2022,8,6)
elif case == 'RF06': # Osan
    filename_ACOS = '../Data/_OtherData_/ACCLIP-ACOS-1Hz_WB57_20220812_RA.ict'
    filename_COLD2 = '../Data/_OtherData_/acclip-COLD2-CO_WB57_20220812_RA.ict'
    filename_COMA = ['../Data/2022-08-12/n2o-co_2022-08-12_f0000.txt']
    filename_DLH = '../Data/_OtherData_/ACCLIP-DLH-H2O_WB57_20220812_RA.ict'
    cur_day = datetime(2022,8,12)
elif case == 'RF07': # Osan
    filename_ACOS = '../Data/_OtherData_/ACCLIP-ACOS-1Hz_WB57_20220813_RA.ict'
    filename_COLD2 = '../Data/_OtherData_/acclip-COLD2-CO_WB57_20220813_RA.ict'
    filename_COMA = ['../Data/2022-08-13/n2o-co_2022-08-13_f0000.txt']
    filename_DLH = '../Data/_OtherData_/ACCLIP-DLH-H2O_WB57_20220813_RA.ict'
    cur_day = datetime(2022,8,13)
elif case == 'RF08': # Osan
    filename_ACOS = '../Data/_OtherData_/ACCLIP-ACOS-1Hz_WB57_20220815_RA.ict'
    filename_COLD2 = '../Data/_OtherData_/acclip-COLD2-CO_WB57_20220815_RA.ict'
    filename_COMA = ['../Data/2022-08-15/n2o-co_2022-08-15_f0000.txt',
                     '../Data/2022-08-15/n2o-co_2022-08-15_f0001.txt']
    filename_DLH = '../Data/_OtherData_/ACCLIP-DLH-H2O_WB57_20220815_RA.ict'
    cur_day = datetime(2022,8,15)
elif case == 'RF09': # Osan
    filename_ACOS = '../Data/_OtherData_/ACCLIP-ACOS-1Hz_WB57_20220816_RA.ict'
    filename_COLD2 = '../Data/_OtherData_/acclip-COLD2-CO_WB57_20220816_RA.ict'
    filename_COMA = ['../Data/2022-08-16/n2o-co_2022-08-16_f0000.txt']
    filename_DLH = '../Data/_OtherData_/ACCLIP-DLH-H2O_WB57_20220816_RA.ict'
    cur_day = datetime(2022,8,16)
    
# %% Plot CO time series from COMA, ACOS, COLD2
if to_plot == 'CO':
    fig, ax = plt.subplots(1, 1, figsize=(8,4))
    
    # load ACOS
    if filename_ACOS:
        ACOS = pd.read_csv(filename_ACOS,sep=',',header=37)
        ACOS_time = [cur_day+timedelta(seconds=t) for t in ACOS['TIME_START']]
        plt.plot(ACOS_time,ACOS['ACOS_CO_PPB'],'.m',label='ACOS')
        
    # load COLD2
    if filename_COLD2:
        COLD2 = pd.read_csv(filename_COLD2,sep=',',header=32)
        COLD_time = [cur_day+timedelta(seconds=t) for t in COLD2['Time_Start']]
        plt.plot(COLD_time,COLD2[' CO_COLD2_ppbv'],'.g',label='COLD2')
        
    # load COMA
    if filename_COMA:
        COMA = read_COMA(filename_COMA)
        ix_8 = np.ravel(np.where(COMA["      MIU_VALVE"]==8)) # inlet
        plt.plot(COMA['time'][ix_8],COMA["      [CO]d_ppm"][ix_8]*1000,'b.',label='COMA')
    
    ax.set_ylabel('CO, ppb')
    ax.set_ylim([-10,300])
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
        DLH = pd.read_csv(filename_DLH,sep=',',header=35)
        DLH_time = [cur_day+timedelta(seconds=t) for t in DLH['Time_Start']]
        ax_twin.plot(DLH_time,DLH['H2O_DLH'],'.k',label='DLH')
        #ax_twin.plot(DLH_time,DLH['RHw_DLH'],'.k',label='DLH')
    
    # load COMA
    if filename_COMA:
        COMA = read_COMA(filename_COMA)
        ix_8 = np.ravel(np.where(COMA["      MIU_VALVE"]==8)) # inlet
        ax.plot(COMA['time'][ix_8],COMA["      [CO]d_ppm"][ix_8]*1000,'b.',label='COMA')
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
    a_1Hz = df_a.groupby(pd.Grouper(key="time", freq="1s")).mean()
    b_1Hz = df_b.groupby(pd.Grouper(key="time", freq="1s")).mean()
    sync_data = pd.merge(a_1Hz, b_1Hz, how='inner', on=['time'])
    sync_data = sync_data.dropna()

    # linear regression
    col_names = sync_data.columns
    model = sm.OLS(sync_data[col_names[1]],sm.add_constant(sync_data[col_names[0]]))
    results = model.fit()
    return sync_data, results

if to_plot == 'corr':
    fig, ax = plt.subplots(1, 3, figsize=(12,4))
    
    COMA = read_COMA(filename_COMA)
    ix_8 = np.ravel(np.where(COMA["      MIU_VALVE"]==8)) # inlet
    
    # load ACOS
    if filename_ACOS:
        ACOS = pd.read_csv(filename_ACOS,sep=',',header=37)
        ACOS['time'] = [cur_day+timedelta(seconds=t) for t in ACOS['TIME_START']]
        
        df_a = pd.DataFrame({'time': COMA['time'][ix_8], 'CO_COMA': COMA["      [CO]d_ppm"][ix_8]*1000})
        df_b = pd.DataFrame({'time': ACOS['time'], 'CO_ACOS': ACOS['ACOS_CO_PPB']})
        sync_data, results = sync_ab(df_a,df_b)
        ax[0].plot(sync_data['CO_COMA'],sync_data['CO_ACOS'],'k.')
        ax[0].text(0.05,0.93,'y = ' + "{:.3f}".format(results.params[1]) + 'x + ' + "{:.3f}".format(results.params[0]),transform=ax[0].transAxes)
        ax[0].text(0.05,0.87,'R2 = ' + "{:.3f}".format(results.rsquared),transform=ax[0].transAxes)
        
    # load COLD2
    if filename_COLD2:
        COLD2 = pd.read_csv(filename_COLD2,sep=',',header=32)
        COLD2['time'] = [cur_day+timedelta(seconds=t) for t in COLD2['Time_Start']]
        
        df_a = pd.DataFrame({'time': COMA['time'][ix_8], 'CO_COMA': COMA["      [CO]d_ppm"][ix_8]*1000})
        df_b = pd.DataFrame({'time': COLD2['time'], 'CO_COLD2': COLD2[' CO_COLD2_ppbv']})
        sync_data, results = sync_ab(df_a,df_b)
        ax[1].plot(sync_data['CO_COMA'],sync_data['CO_COLD2'],'k.')
        ax[1].text(0.05,0.93,'y = ' + "{:.3f}".format(results.params[1]) + 'x + ' + "{:.3f}".format(results.params[0]),transform=ax[1].transAxes)
        ax[1].text(0.05,0.87,'R2 = ' + "{:.3f}".format(results.rsquared),transform=ax[1].transAxes)
        
    # load DLH
    if filename_DLH:
        DLH = pd.read_csv(filename_DLH,sep=',',header=35)
        DLH['time'] = [cur_day+timedelta(seconds=t) for t in DLH['Time_Start']]

        df_a = pd.DataFrame({'time': COMA['time'][ix_8], 'H2O_COMA': COMA["      [H2O]_ppm"][ix_8]})
        df_b = pd.DataFrame({'time': DLH['time'], 'H2O_DLH': DLH['H2O_DLH']})
        sync_data, results = sync_ab(df_a,df_b)
        ax[2].plot(sync_data['H2O_COMA'],sync_data['H2O_DLH'],'k.')
        ax[2].text(0.05,0.93,'y = ' + "{:.3f}".format(results.params[1]) + 'x + ' + "{:.3f}".format(results.params[0]),transform=ax[2].transAxes)
        ax[2].text(0.05,0.87,'R2 = ' + "{:.3f}".format(results.rsquared),transform=ax[2].transAxes)
        
    ax[0].set_xlabel('COMA CO, ppbv')
    ax[0].set_ylabel('ACOS CO, ppbv')
    
    ax[1].set_xlabel('COMA CO, ppbv')
    ax[1].set_ylabel('COLD2 CO, ppbv')
    
    ax[2].set_xlabel('COMA H2O, ppmv')
    ax[2].set_ylabel('DLH H2O, ppmv')
    
    ax[0].plot([0,200],[0,200],'k:')
    ax[0].set_xlim([0,200])
    ax[0].set_ylim([0,200])
    
    ax[1].plot([0,200],[0,200],'k:')
    ax[1].set_xlim([0,200])
    ax[1].set_ylim([0,200])
    
    ax[2].plot([0,30000],[0,30000],'k:')
    
    fig.tight_layout()