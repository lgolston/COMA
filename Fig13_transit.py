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
from load_data_functions import read_ACOS_ict
from load_data_functions import read_MMS_ict

# set plot style
plt.rc('axes', labelsize=8) # xaxis and yaxis labels
plt.rc('xtick', labelsize=8) # xtick labels
plt.rc('ytick', labelsize=8) # ytick labels

# load files
case = 'Transit6'

filenames = return_filenames(case)
ACOS = read_ACOS_ict(filenames['ACOS'])
MMS = read_MMS_ict(filenames['MMS'])
   
ACOS[ACOS['ACOS_CO_PPB']<-600] = np.nan
MMS[MMS['T']<0] = np.nan

# %% create figure
fig, ax = plt.subplots(1, 1, figsize=(6,3.5))
ax_twin = ax.twinx()

ax.plot(ACOS['time'],ACOS['ACOS_CO_PPB'],'m',marker='.',label='ACOS',markersize=2)
#ax_twin.plot(MMS['time'],MMS['T'])
ax_twin.plot(MMS['time'],MMS['POT'])
