# -*- coding: utf-8 -*-
"""
Compare COLD2, ACOS, and COMA CO measurements
"""

# %% header
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.dates as mdates
import numpy as np

from load_data_functions import read_COMA
from load_data_functions import read_ACOS_ict
from load_data_functions import read_COLD2_ict
from load_data_functions import return_filenames
from load_data_functions import linear_ab

case = 'RF15'

# set plot style
plt.rc('axes', labelsize=8) # xaxis and yaxis labels
plt.rc('xtick', labelsize=8) # xtick labels
plt.rc('ytick', labelsize=8) # ytick labels
plt.rcParams['legend.fontsize'] = 7
plt.rcParams['font.size']=8

# %% load data files names
filenames = return_filenames(case)

# COMA
COMA, inlet_ix = read_COMA(filenames['COMA_raw'])

if case == 'RF13': # fix clock setting on this day
    COMA['time'] = COMA['time'] + timedelta(hours=6)

ACOS = read_ACOS_ict(filenames['ACOS'])
ACOS[ACOS["ACOS_CO_PPB"]<-600] = np.nan

COLD2 = read_COLD2_ict(filenames['COLD2'])
COLD2[COLD2[' CO_COLD2_ppbv']<-600]=np.nan

# %% Plot CO time series from COMA, ACOS, COLD2
fig, ax = plt.subplot_mosaic([['A', 'A'],
                              ['B', 'C']],
                              figsize=(6, 4.5))

time_offset = timedelta(seconds=6)

# ict files for each are 1 Hz data
ax["A"].plot(ACOS['time'],ACOS['ACOS_CO_PPB'],'m',marker='.',label='ACOS',markersize=2)
ax["A"].plot(COMA['time'][inlet_ix],COMA["[CO]d_ppm"][inlet_ix]*1000,'b',marker='.',label='COMA',markersize=2)
ax["A"].plot(COLD2['time']+time_offset,COLD2[' CO_COLD2_ppbv'],'g',marker='.',label='COLD2',markersize=2)

ax["A"].set_ylabel('CO, ppb')
ax["A"].set_xlim(datetime(2022,8,29,1),datetime(2022,8,29,7))
ax["A"].set_ylim([-10,200])
ax["A"].grid('on')
ax["A"].legend(ncol=3,loc='upper left')
ax["A"].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

# %% correlation plots
# COMA CO vs ACOS
# COMA CO vs COLD2

# load ACOS
df_a = pd.DataFrame({'time': COMA['time'][inlet_ix], 'CO_COMA': COMA["[CO]d_ppm"][inlet_ix]*1000})
df_b = pd.DataFrame({'time': ACOS['time'], 'CO_ACOS': ACOS['ACOS_CO_PPB']})
sync_data, results = linear_ab(df_a,df_b,'5s')

# plot
ax["B"].plot(sync_data['CO_COMA'],sync_data['CO_ACOS'],'k.')
ax["B"].text(0.05,0.93,'y = ' + "{:.3f}".format(results.params[1]) + 'x + ' + "{:.3f}".format(results.params[0]),transform=ax["B"].transAxes)
ax["B"].text(0.05,0.87,'R2 = ' + "{:.3f}".format(results.rsquared),transform=ax["B"].transAxes)
   
df_a = pd.DataFrame({'time': COMA['time'][inlet_ix], 'CO_COMA': COMA["[CO]d_ppm"][inlet_ix]*1000})
df_b = pd.DataFrame({'time': COLD2['time'] + time_offset, 'CO_COLD2': COLD2[' CO_COLD2_ppbv']})
sync_data, results = linear_ab(df_a,df_b,'5s')

ax["C"].plot(sync_data['CO_COMA'],sync_data['CO_COLD2'],'k.')
ax["C"].text(0.05,0.93,'y = ' + "{:.3f}".format(results.params[1]) + 'x + ' + "{:.3f}".format(results.params[0]),transform=ax["C"].transAxes)
ax["C"].text(0.05,0.87,'R2 = ' + "{:.3f}".format(results.rsquared),transform=ax["C"].transAxes)

# format plots
ax["B"].set_xlabel('COMA CO, ppbv')
ax["B"].set_ylabel('ACOS CO, ppbv')
ax["C"].set_xlabel('COMA CO, ppbv')
ax["C"].set_ylabel('COLD2 CO, ppbv')

xlim = 200
ylim = 200
ax["B"].plot([0,xlim],[0,ylim],'k:')
ax["B"].set_xlim([0,xlim])
ax["B"].set_ylim([0,ylim])

ax["C"].plot([0,xlim],[0,ylim],'k:')
ax["C"].set_xlim([0,xlim])
ax["C"].set_ylim([0,ylim])

fig.tight_layout()

#fig.savefig('fig1.png',dpi=300)
