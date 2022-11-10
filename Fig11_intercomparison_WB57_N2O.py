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

filename = filenames['COLD2'] = '../Data/_OtherData_/acclip-COLD2-N2O_WB57_20220829_RB.ict'
cur_day = datetime.strptime(filename[-15:-7],"%Y%m%d")
COLD2 = pd.read_csv(filename,sep=',',header=32) # for RB version
COLD2['time'] = [cur_day+timedelta(seconds=t) for t in COLD2['Time_Start']]
COLD2[COLD2[' N2O_COLD2_ppbv']<-600]=np.nan

# %% Plot CO time series from COMA, ACOS, COLD2
fig, ax = plt.subplot_mosaic([['A', 'B']], figsize=(6, 3))

time_offset = timedelta(seconds=6)

# ict files for each are 1 Hz data
ax["A"].plot(COMA['time'][inlet_ix],COMA["[N2O]d_ppm"][inlet_ix]*1000,'b',marker='.',label='COMA',markersize=2)
ax["A"].plot(COLD2['time']+time_offset,COLD2[' N2O_COLD2_ppbv'],'g',marker='.',label='COLD2',markersize=2)

ax["A"].set_ylabel('N2O, ppb')
#ax["A"].set_ylim([-10,200])
ax["A"].grid('on')
ax["A"].legend(ncol=3,loc='upper left')
ax["A"].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

# %% correlation plots
# COMA N2O vs COLD2

# load ACOS
df_a = pd.DataFrame({'time': COMA['time'][inlet_ix], 'N2O_COMA': COMA["[N2O]d_ppm"][inlet_ix]*1000})
df_b = pd.DataFrame({'time': COLD2['time'], 'N2O_ACOS': COLD2[' N2O_COLD2_ppbv']})
sync_data, results = linear_ab(df_a,df_b,'5s')

# plot
ax["B"].plot(sync_data['N2O_COMA'],sync_data['N2O_ACOS'],'k.')
ax["B"].text(0.05,0.93,'y = ' + "{:.3f}".format(results.params[1]) + 'x + ' + "{:.3f}".format(results.params[0]),transform=ax["B"].transAxes)
ax["B"].text(0.05,0.87,'R2 = ' + "{:.3f}".format(results.rsquared),transform=ax["B"].transAxes)
   
# format plots
ax["B"].set_xlabel('COMA N2O, ppbv')
ax["B"].set_ylabel('COMA N20, ppbv')

ax["B"].plot([280,350],[280,350],'k:')
ax["B"].set_xlim([280,350])
ax["B"].set_ylim([280,350])

fig.tight_layout()

#fig.savefig('fig1.png',dpi=300)
