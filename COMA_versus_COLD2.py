# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 16:20:16 2022
"""

# %% header
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.dates as mdates

from load_flight_functions import read_COMA

case = 4

# %% load data
if case == 0: # Ellington to Seattle
     filename_COMA = ['../Data/2022-07-21/n2o-co_2022-07-21_f0000.txt',
                      '../Data/2022-07-21/n2o-co_2022-07-21_f0001.txt']
     filename_COLD2 = '../Data/_OtherData_/acclip-COLD2-CO_WB57_20220721_RA_L1.ict'
     cur_day = datetime(2022,7,21)
elif case == 1: # Seattle to Anchorage
     filename_COMA = ['../Data/2022-07-21/n2o-co_2022-07-21_f0002.txt']
     filename_COLD2 = '../Data/_OtherData_/acclip-COLD2-CO_WB57_20220721_RA_L2.ict'
     cur_day = datetime(2022,7,21)
elif case == 2: # Anchorage to Adak
     filename_COMA = ['../Data/2022-07-24/n2o-co_2022-07-24_f0000.txt']
     filename_COLD2 = '../Data/_OtherData_/acclip-COLD2-CO_WB57_20220724_RA.ict'
     cur_day = datetime(2022,7,24)
elif case == 3: # Adak to Misawa
     filename_COMA = ['../Data/2022-07-25/n2o-co_2022-07-25_f0000.txt']
     filename_COLD2 = '../Data/_OtherData_/acclip-COLD2-CO_WB57_20220725_RA.ict'
     cur_day = datetime(2022,7,25)
elif case == 4: # Misawa to Osan
     filename_COMA = ['../Data/2022-07-27/n2o-co_2022-07-27_f0000.txt']
     filename_COLD2 = '../Data/_OtherData_/acclip-COLD2-CO_WB57_20220727_RA.ict'
     cur_day = datetime(2022,7,27)
 
# load COMA
COMA = read_COMA(filename_COMA)
ix_8 = np.ravel(np.where(COMA["      MIU_VALVE"]==8)) # inlet

# load COLD2
COLD2 = pd.read_csv(filename_COLD2,sep=',',header=32)
COLD_time = [cur_day+timedelta(seconds=t) for t in COLD2['Time_Start']]

# %% plot data
plt.plot(COMA['time'][ix_8],COMA["      [CO]d_ppm"][ix_8]*1000,'b.',markersize=2)
plt.plot(COLD_time,COLD2[' CO_COLD2_ppbv'],'.g')
plt.ylim([0,1000])
