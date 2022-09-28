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

from load_data_functions import read_COMA
from load_data_functions import return_filenames

import statsmodels.api as sm

case = 'RF15'

# set plot style
plt.rc('axes', labelsize=11) # xaxis and yaxis labels
plt.rc('xtick', labelsize=11) # xtick labels
plt.rc('ytick', labelsize=11) # ytick labels
plt.rc('legend', fontsize=11) # ytick labels

# %% list file names
filenames = return_filenames(case)
    
# %% create helper function (for loading ICARTT files, linear regression)
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

# %% load COMA file (used in all plot types below)
COMA, inlet_ix = read_COMA(filenames['COMA_raw'])

if case == 'RF13': # fix clock setting on this day
    COMA['time'] = COMA['time'] + timedelta(hours=6)
    
# %% Plot CO time series from COMA, ACOS, COLD2
fig1, ax = plt.subplots(1, 1, figsize=(8,4))

# ict files for each are 1 Hz data
# load and plot ACOS
if len(filenames['ACOS'])>0:
    ACOS = read_ACOS_ict(filenames['ACOS'])
    plt.plot(ACOS['time'],ACOS['ACOS_CO_PPB'],'.m',label='ACOS',markersize=2)
    
# plot COMA
plt.plot(COMA['time'][inlet_ix],COMA["[CO]d_ppm"][inlet_ix]*1000,'b.',label='COMA',markersize=2)
     
# load and plot COLD2
if len(filenames['COLD2'])>0:
    COLD2 = read_COLD2_ict(filenames['COLD2'])
    plt.plot(COLD2['time'],COLD2[' CO_COLD2_ppbv'],'.g',label='COLD2',markersize=2)
    
ax.set_ylabel('CO, ppb')
ax.set_ylim([-10,200])
#ax.set_ylim([-10,300])
ax.grid('on')
ax.legend()
ax.set_title(case)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
fig1.tight_layout()

# %% correlation plots
# COMA CO vs ACOS
# COMA CO vs COLD2
fig2, ax = plt.subplots(1, 2, figsize=(9,4))
        
# load ACOS
if len(filenames['ACOS'])>0:
    ACOS = read_ACOS_ict(filenames['ACOS'])
        
    df_a = pd.DataFrame({'time': COMA['time'][inlet_ix], 'CO_COMA': COMA["[CO]d_ppm"][inlet_ix]*1000})
    df_b = pd.DataFrame({'time': ACOS['time'], 'CO_ACOS': ACOS['ACOS_CO_PPB']})
    sync_data, results = sync_ab(df_a,df_b)
    ax[0].plot(sync_data['CO_COMA'],sync_data['CO_ACOS'],'k.')
    ax[0].text(0.05,0.93,'y = ' + "{:.3f}".format(results.params[1]) + 'x + ' + "{:.3f}".format(results.params[0]),transform=ax[0].transAxes)
    ax[0].text(0.05,0.87,'R2 = ' + "{:.3f}".format(results.rsquared),transform=ax[0].transAxes)
    
# load COLD2
if len(filenames['COLD2'])>0:
    COLD2 = read_COLD2_ict(filenames['COLD2'])
        
    df_a = pd.DataFrame({'time': COMA['time'][inlet_ix], 'CO_COMA': COMA["[CO]d_ppm"][inlet_ix]*1000})
    df_b = pd.DataFrame({'time': COLD2['time'], 'CO_COLD2': COLD2[' CO_COLD2_ppbv']})
    sync_data, results = sync_ab(df_a,df_b)
    ax[1].plot(sync_data['CO_COMA'],sync_data['CO_COLD2'],'k.')
    ax[1].text(0.05,0.93,'y = ' + "{:.3f}".format(results.params[1]) + 'x + ' + "{:.3f}".format(results.params[0]),transform=ax[1].transAxes)
    ax[1].text(0.05,0.87,'R2 = ' + "{:.3f}".format(results.rsquared),transform=ax[1].transAxes)
    
# format plots
ax[0].set_xlabel('COMA CO, ppbv')
ax[0].set_ylabel('ACOS CO, ppbv')
    
ax[1].set_xlabel('COMA CO, ppbv')
ax[1].set_ylabel('COLD2 CO, ppbv')

xlim = 200
ylim = 200
ax[0].plot([0,xlim],[0,ylim],'k:')
ax[0].set_xlim([0,xlim])
ax[0].set_ylim([0,ylim])

ax[1].plot([0,xlim],[0,ylim],'k:')
ax[1].set_xlim([0,xlim])
ax[1].set_ylim([0,ylim])

fig2.tight_layout()

#fig.savefig('fig1.png',dpi=300)
