# -*- coding: utf-8 -*-
"""
plot 2D GEOS data
"""

# %% header
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from load_data_functions import return_filenames, read_MMS_ict

# %% select data
case = 'RF05'

if case == 'RF05':
    filename_GEOS = '../Data/_Model_/ACCLIP-GEOS_WB57_20220806_R0.ict'
    filename_GEOS_2D = '../Data/_Model_/ACCLIP-GEOS-2D_WB57_20220806_R0.ict'
    cur_day = datetime(2022,8,6)
if case == 'RF10':
    filename_GEOS = '../Data/_Model_/ACCLIP-GEOS_WB57_20220819_R0.ict'
    filename_GEOS_2D = '../Data/_Model_/ACCLIP-GEOS-2D_WB57_20220819_R0.ict'
    cur_day = datetime(2022,8,19)
elif case == 'Transit7': # Misawa to Adak
    filename_GEOS = '../Data/_Model_/ACCLIP-GEOS_WB57_20220912_R0.ict'
    filename_GEOS_2D = '../Data/_Model_/ACCLIP-GEOS-2D_WB57_20220912_R0.ict'
    cur_day = datetime(2022,9,12)
elif case == 'Transit8': # Adak to Seattle
    filename_GEOS = '../Data/_Model_/ACCLIP-GEOS_WB57_20220913_R0.ict'
    filename_GEOS_2D = '../Data/_Model_/ACCLIP-GEOS-2D_WB57_20220913_R0.ict'
    cur_day = datetime(2022,9,13)

# %% load data
# main model file
#cur_day = datetime.strptime(filename_GEOS[-15:-7],"%Y%m%d")
#GEOS = pd.read_csv(filename_GEOS,sep=',',header=61)
#GEOS['time'] = [cur_day+timedelta(seconds=t) for t in GEOS['Time_Start']]
#GEOS[GEOS[' SLP_GEOS'] < 0] = np.nan

# load MMS file
filenames = return_filenames(case)
MMS = read_MMS_ict(filenames['MMS'])
MMS[MMS['T']<0] = np.nan

# 2D model file
header_lines = 65
dat = open(filename_GEOS_2D).readlines()
dat = dat[header_lines:len(dat)]
num_chunks = int(len(dat)/32) # one set of data (31 P levels + 1 header line)
num_P_levels = 31
num_variables = 23
GEOS_2D = np.zeros(shape=(num_chunks,num_P_levels,num_variables))
GEOS_2D_time = np.zeros(num_chunks, dtype='datetime64[s]')

for ii in range(num_chunks):
    tmp = dat[ii*32]
    GEOS_2D_time[ii] = cur_day + timedelta(seconds = float(tmp[0:7]))
    
    for jj in range(1,32):
        GEOS_2D[ii,jj-1,:] = np.array(dat[ii*32+jj].split(','),dtype='float')

# %% plot time vs pressure level; CO colorbar
fig, ax = plt.subplots(1, 1, figsize=(6,5))

GEOS_levels = [1000,975,950,925,900,875,850,825,800,775,
               750,725,700,650,600,550,500,450,400,350,
               300,250,200,150,100,70,50,40,30,20,10]

GEOS_2D_CO = GEOS_2D[:,:,10]
GEOS_2D_CO[GEOS_2D_CO<=-99] = np.nan

im = plt.pcolormesh(GEOS_2D_time,GEOS_levels,GEOS_2D_CO.T*1E9,vmax=150)
plt.plot(MMS['time'],MMS['P'])

ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.xlabel('Time')
ax0 = plt.gca()
ax0.invert_yaxis()
plt.ylabel('Pressure, hPa')
cbar = fig.colorbar(im,ax=ax0)
cbar.set_label('CO, ppb')
plt.tight_layout()
#plt.savefig('fig_output.png',dpi=200)