# -*- coding: utf-8 -*-
"""
Compare COMA and DLH

TODO:
1. Set time end to one hour after stat
2. Look at all cases
"""

# %% header
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.dates as mdates

from load_data_functions import read_COMA
from load_data_functions import return_filenames

case = 'RF15'

# set plot style
plt.rc('axes', labelsize=11) # xaxis and yaxis labels
plt.rc('xtick', labelsize=11) # xtick labels
plt.rc('ytick', labelsize=11) # ytick labels
plt.rc('legend', fontsize=11) # ytick labels

# %% list file names
filenames = return_filenames(case)
    
# %% create helper function (for loading ICARTT files, linear regression)
def read_DLH_ict(filename):
    # e.g. ACCLIP-DLH-H2O_WB57_20220816_RA.ict
    cur_day = datetime.strptime(filename[-15:-7],"%Y%m%d")
    DLH = pd.read_csv(filename,sep=',',header=35)
    DLH['time'] = [cur_day+timedelta(seconds=t) for t in DLH['Time_Start']]
    return DLH


# %% load COMA and DLH files
COMA, inlet_ix = read_COMA(filenames['COMA_raw'])

if case == 'RF13': # fix clock setting on this day
    COMA['time'] = COMA['time'] + timedelta(hours=6)

# load and plot DLH
DLH = read_DLH_ict(filenames['DLH'])
    

# %% Plot CO time series and DLH H2O
fig3, ax = plt.subplots(1, 1, figsize=(6,3))

# plot COMA
ax.plot(COMA['time'][inlet_ix],COMA["[H2O]_ppm"][inlet_ix],'b.',label='COMA')
ax.plot(DLH['time'],DLH['H2O_DLH'],'.k',label='DLH')
ax.set_ylabel('Water vapor mixing ratio, ppmv') 

ax.set_title(case)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
fig3.tight_layout()

# %%
""" regression
# load DLH
if filename_DLH:
    DLH = read_DLH_ict(filename_DLH)

    df_a = pd.DataFrame({'time': COMA['time'][inlet_ix], 'H2O_COMA': COMA["      [H2O]_ppm"][inlet_ix]})
    df_b = pd.DataFrame({'time': DLH['time'], 'H2O_DLH': DLH['H2O_DLH']})
    sync_data, results = sync_ab(df_a,df_b)
    ax[2].plot(sync_data['H2O_COMA'],sync_data['H2O_DLH'],'k.')
    ax[2].text(0.05,0.93,'y = ' + "{:.3f}".format(results.params[1]) + 'x + ' + "{:.3f}".format(results.params[0]),transform=ax[2].transAxes)
    ax[2].text(0.05,0.87,'R2 = ' + "{:.3f}".format(results.rsquared),transform=ax[2].transAxes)

ax[2].set_xlabel('COMA H2O, ppmv')
ax[2].set_ylabel('DLH H2O, ppmv')
ax[2].plot([0,30000],[0,30000],'k:')
"""    
