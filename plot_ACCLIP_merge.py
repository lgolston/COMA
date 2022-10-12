# -*- coding: utf-8 -*-
"""
plot 1 Hz merge

Wait a little while for other fields to be added (model output, ozone, etc.)
"""

# %% header
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# %% select data
case = 'Transit8'

if case == 'Transit1':
    filename_merge = 1 #2022-07-21
elif case == 'Transit2':
    filename_merge = 1 #2022-07-21
elif case == 'Transit3':
    filename_merge = '../Data/_Merge_/ACCLIP-mrg01-WB57_merge_20220724_RA.ict' #2022-07-24
elif case == 'Transit4':
    filename_merge = 1 #2022-07-25
elif case == 'Transit5':
    filename_merge = 1 #2022-07-27
elif case == 'RF03':
    1
elif case == 'RF04':
    1
elif case == 'RF05':
    1
elif case == 'RF06':
    1
elif case == 'RF07':
    1
elif case == 'RF08':
    1
elif case == 'RF09':
    1
elif case == 'RF10':
    1
elif case == 'RF11':
    1
elif case == 'RF12':
    1
elif case == 'RF13':
    1
elif case == 'RF14':
    1
elif case == 'RF15':
    1
elif case == 'RF16':
    1
elif case == 'RF17':
    1
elif case == 'Transit6':
    1
elif case == 'Transit7':
    1
elif case == 'Transit8':
    filename_merge = '../Data/_Merge_/ACCLIP-mrg01-WB57_merge_20220913_RA.ict'
elif case == 'Transit9':
    1


# %% load data
cur_day = datetime.strptime(filename_merge[-15:-7],"%Y%m%d")
mergeData = pd.read_csv(filename_merge,sep=',',header=258)
mergeData['time'] = [cur_day+timedelta(seconds=t) for t in mergeData['Time_Start']]

# %% plot time vs pressure level; CO colorbar
fig, ax = plt.subplots(1, 1, figsize=(6,5))

ax.plot(mergeData['time'],mergeData[' CO_ACOS'])
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.xlabel('Time')
plt.tight_layout()
#plt.savefig('fig_output.png',dpi=200)