# -*- coding: utf-8 -*-
"""
Figure
"""

# %% header
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.dates as mdates

from load_data_functions import return_filenames
from load_data_functions import read_COMA
from load_data_functions import read_MMS_ict

case = 'RF11'

# set plot style
plt.rcParams['axes.labelsize'] = 8
plt.rcParams['legend.fontsize'] = 8
plt.rcParams['xtick.labelsize'] = 7
plt.rcParams['ytick.labelsize'] = 7
plt.rcParams['font.size']=8
plt.rcParams.update({'mathtext.default': 'regular' } ) # not italics

filenames = return_filenames(case)

COMA, inlet_ix = read_COMA(filenames['COMA_raw'])

# index MIU valves
ix_8 = np.ravel(np.where(COMA["MIU_VALVE"]==8)) # inlet
ix_7 = np.ravel(np.where(COMA["MIU_VALVE"]==7)) # inlet (lab)
ix_3 = np.ravel(np.where(COMA["MIU_VALVE"]==3)) # high cal
ix_2 = np.ravel(np.where(COMA["MIU_VALVE"]==2)) # low cal
ix_1 = np.ravel(np.where(COMA["MIU_VALVE"]==1)) # flush

# %% plot
fig2, ax2 = plt.subplots(1, 2, figsize=(6,3))

df_lowcal = pd.DataFrame({'time': COMA['time'][ix_2],
                          'CO_dry': COMA["[CO]d_ppm"][ix_2]*1000,
                          'N2O_dry': COMA["[N2O]d_ppm"][ix_2]*1000,
                          'H2O': COMA["[H2O]_ppm"][ix_2]})
df_lowcal['groups'] = (df_lowcal.index.to_series().diff()>5).cumsum()
df_highcal = pd.DataFrame({'time': COMA['time'][ix_3],
                           'CO_dry': COMA["[CO]d_ppm"][ix_3]*1000,
                           'N2O_dry': COMA["[N2O]d_ppm"][ix_3]*1000,
                           'H2O': COMA["[H2O]_ppm"][ix_3]})
df_highcal['groups'] = (df_highcal.index.to_series().diff()>5).cumsum()
#df_flush = pd.DataFrame({'time': LGR_time[ix_1], 'CO_dry': LGR["      [CO]d_ppm"][ix_1]*1000})
#df_flush['groups'] = (df_flush.index.to_series().diff()>5).cumsum()
    
start_time = COMA['time'][0]
    
for ct, data in df_lowcal.groupby('groups'):
    ax2[0].plot(data['CO_dry'].values,'.')
            
for ct, data in df_highcal.groupby('groups'):
    ax2[1].plot(data['CO_dry'].values,'.')

# NOAA gas bottle
ax2[0].set_ylim(40,70)
ax2[1].set_ylim(140,170)

# Matheson gas bottle
ax2[0].set_ylim(170,220)
ax2[1].set_ylim(800,1000)

ax2[0].set_ylabel('CO, ppb')

ax2[0].grid()
ax2[1].grid()
ax2[0].set_xlabel('Seconds')
ax2[0].set_title('Low cal')
ax2[1].set_xlabel('Seconds')
ax2[1].set_title('High cal')
ax2[1].legend(np.linspace(1,13,13,dtype='int'),ncol=2)

fig2.tight_layout()
#fig2.savefig('fig2.png',dpi=300)
