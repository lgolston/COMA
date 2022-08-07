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

case = 'RF05'

# %% load data
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
elif case == 'RF03': # RF03, Osan
    filename_ACOS = '../Data/_OtherData_/ACCLIP-ACOS-1Hz_WB57_20220802_RA.ict'
    filename_COLD2 = '../Data/_OtherData_/acclip-COLD2-CO_WB57_20220802_RA.ict'
    filename_COMA = ['../Data/2022-08-02/n2o-co_2022-08-02_f0000.txt']
    cur_day = datetime(2022,8,2)
elif case == 'RF04': # RF04, Osan
    filename_ACOS = '../Data/_OtherData_/ACCLIP-ACOS-1Hz_WB57_20220804_RA.ict'
    filename_COLD2 = '../Data/_OtherData_/acclip-COLD2-CO_WB57_20220804_RA.ict'
    filename_COMA = ['../Data/2022-08-04/n2o-co_2022-08-04_f0000.txt']
    cur_day = datetime(2022,8,4)
elif case == 'RF05': # RF05, Osan
    filename_ACOS = '../Data/_OtherData_/ACCLIP-ACOS-1Hz_WB57_20220806_RA.ict'
    filename_COLD2 = None
    filename_COMA = ['../Data/2022-08-06/n2o-co_2022-08-06_f0000.txt']
    cur_day = datetime(2022,8,6)

# %% load and plot data
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