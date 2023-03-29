# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 11:44:42 2022

@author: L Golston
"""

# %% read data
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from load_data_functions import read_COMA
from load_data_functions import return_filenames

case = 'Transit8'
filenames = return_filenames(case)

#filename = 'acclip-COMA-CON2O_WB57_20220913_RB.ict'
filename = filenames['COMA_ict']
cur_day = datetime.strptime(filename[-15:-7],"%Y%m%d")
COMA_ict = pd.read_csv(filename,sep=',',header=35)
COMA_ict['time'] = [cur_day+timedelta(seconds=t) for t in COMA_ict['Time_Mid']]

COMA, inlet_ix = read_COMA(filenames['COMA_raw'])

# %% plot data
fig, ax = plt.subplots(3, 1, figsize=(8,4),sharex=True)
#ax_twin = ax.twinx()

ax[0].plot(COMA['time'],COMA['[CO]d_ppm']*1000,'k.',label='CO-orig')
ax[0].plot(COMA['time'],COMA['[N2O]d_ppm']*1000-250,'y.',label='CO-orig')

ax[0].plot(COMA_ict['time'],COMA_ict['CO'],'.',label='CO')
ax[0].plot(COMA_ict['time'],COMA_ict['N2O']-250,'g.',label='N2O - 250')


ax[0].legend()
ax[0].set_ylim([0,200])

ax[1].plot(COMA['time'], COMA["GasP_torr"],'.')
ax[1].axhline(52.8,color='black')
ax[1].axhline(52.8-52.8*0.0025,color='black',linestyle='--')
ax[1].axhline(52.8+52.8*0.0025,color='black',linestyle='--')
ax[1].set_ylim([52.4,53.2])

ax[2].plot(COMA['time'], COMA["MIU_VALVE"],'.')

ax[0].set_ylabel('Mixing ratio, ppb')
ax[1].set_ylabel('Cell pressure, Torr')
ax[0].set_title('Transit8 COMA RB')
fig.tight_layout()

#ax_twin.set_ylim([200,400])
