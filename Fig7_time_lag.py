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
from load_data_functions import linear_ab
from load_data_functions import return_filenames

case = 'RF09'

# set plot style
plt.rcParams['axes.labelsize'] = 8
plt.rcParams['legend.fontsize'] = 8
plt.rcParams['xtick.labelsize'] = 7
plt.rcParams['ytick.labelsize'] = 7

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

#RF04, RF06, RF09, RF11, RF14, RF16, RF17 worked on descent
# no DLH on RF03

if case in ['RF04']:
    COMA['time'] = COMA['time'] - timedelta(seconds = 4.5)
elif case in ['RF03','RF05','RF06', 'RF07', 'RF08','RF09', 'RF10', 'RF11', 'RF12', 'RF14', 'RF15','RF16','RF17']:
    COMA['time'] = COMA['time'] - timedelta(seconds = 6)
elif case == 'RF13': # fix clock setting on this day
    COMA['time'] = COMA['time'] + timedelta(hours=6) - timedelta(seconds = 6)


# load and plot DLH
DLH = read_DLH_ict(filenames['DLH'])
    

# %% Plot CO time series and DLH H2O
fig, ax = plt.subplots(1, 2, figsize=(6.5,3))

ix_COMA = np.ravel(np.where( (COMA['time'] > datetime(2022,8,16,3,5)) & (COMA['time'] < datetime(2022,8,16,3,28))  ))
ix_DLH = np.ravel(np.where(DLH['time'] < datetime(2022,8,16,3,28)))

# plot COMA
ax[0].plot(COMA['time'][ix_COMA],COMA["[H2O]_ppm"][ix_COMA],'b.-',label='COMA')
ax[0].plot(DLH['time'][ix_DLH],DLH['H2O_DLH'][ix_DLH],'k.-',label='DLH')
ax[0].set_xlabel('Time')
ax[0].set_ylabel('Water vapor mixing ratio, ppmv') 

ax[0].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax[0].legend()
ax[0].set_ylim(-1000,10000)

# %% regression
# correlate before 03:40 on RF09

df_a = pd.DataFrame({'time': COMA['time'][ix_COMA], 'H2O_COMA': COMA["[H2O]_ppm"][ix_COMA]})
df_b = pd.DataFrame({'time': DLH['time'][ix_DLH], 'H2O_DLH': DLH['H2O_DLH'][ix_DLH]})
sync_data, results = linear_ab(df_a,df_b,'5s')
ax[1].plot(sync_data['H2O_COMA'],sync_data['H2O_DLH'],'k.')
ax[1].text(0.05,0.93,'y = ' + "{:.3f}".format(results.params[1]) + 'x + ' + "{:.3f}".format(results.params[0]),transform=ax[1].transAxes)
ax[1].text(0.05,0.87,'R2 = ' + "{:.3f}".format(results.rsquared),transform=ax[1].transAxes)

ax[1].set_xlabel('COMA H2O, ppmv')
ax[1].set_ylabel('DLH H2O, ppmv')
ax[1].plot([0,25000],[0,25000],'k:')
ax[1].set_xlim([0,25000])
ax[1].set_ylim([0,25000])

fig.tight_layout()

#plt.savefig('fig_output.png',dpi=300)
