# -*- coding: utf-8 -*-
"""
plot data -during- a WB-57 flight
using COMA and IWG1 from MTS
"""

# %% EDIT THESE
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates

from load_flight_functions import V_to_T

filename_COMA_MTS = '../Data/2022-08-02/telemetry-62e876f99f75ebc8abffaf51.csv'
filename_IWG1_MTS = '../Data/2022-08-02/telemetry-62e876539f75ebc8abffa3ed.csv'
cur_day = datetime(2022,8,2)

# %% data
# read COMA data (obtained over MTS)
LGR = pd.read_csv(filename_COMA_MTS,sep=',',header=0)

LGR_time = LGR["Timestamp"]
LGR_time = [datetime.strptime(tstamp,"%Y-%m-%dT%H:%M:%S.%fZ") for tstamp in LGR_time]
LGR_time = pd.DataFrame(LGR_time)
LGR['time'] = LGR_time[0]

# load WB-57 IWG1 data (obtained over MTS)
IWG1 = pd.read_csv(filename_IWG1_MTS,sep=',',header=0)

IWG1_time = IWG1["TimeStamp"]
IWG1_time = [datetime.strptime(tstamp,"%Y-%m-%dT%H:%M:%S.%fZ") for tstamp in IWG1_time]
IWG1_time = pd.DataFrame(IWG1_time)
IWG1['time'] = IWG1_time[0]

# %% plot data
plt.rc('axes', labelsize=6) # xaxis and yaxis labels
plt.rc('xtick', labelsize=6) # xtick labels
plt.rc('ytick', labelsize=6) # ytick labels
fig, ax = plt.subplots(3, 2, figsize=(9,3.5),dpi=200,sharex=True)

# 1. CO
ax[0,0].plot(LGR['time'],LGR["CO_ppm"]*1000,'k.',markersize=2)
ax[0,0].set_ylabel('CO (dry), ppbv')
ax[0,0].set_ylim(0,300)

# 2. altitude
ax[1,0].plot(IWG1['time'],IWG1["Pressure Altitude"],'k.',markersize=2)
ax[1,0].set_ylabel('Pressure altitude, ft')
#ax[0,0].set_ylim(0,300)

# 3. MIU
ax[2,0].plot(LGR['time'],LGR["MIU_Valve"],'k.',markersize=2)
ax[2,0].set_ylabel('MUI #')
#ax[0,0].set_ylim(0,300)

# 4. N2O
ax[0,1].plot(LGR['time'],LGR["N2O_ppm"]*1000,'.',markersize=2)
ax[0,1].set_ylabel('$\mathregular{N_2O (dry), ppbv}$')
ax[0,1].set_ylim(200,350)

# 5. laser temperature
laserT = V_to_T(LGR["AIN6"])
ax[1,1].plot(LGR['time'],laserT,'.',markersize=2) # laser temp
ax[1,1].set_ylabel('Laser T, C')

# 6. supercool temperature
supercoolT = V_to_T(LGR["AIN5"])
ax[2,1].plot(LGR['time'],supercoolT,'.',markersize=2)
ax[2,1].set_ylabel('Supercool T, C')

# other. H2O
#ax[2,0].plot(LGR_time,LGR["H2O_ppm"],'.',markersize=2)
#ax[2,0].set_ylabel('$\mathregular{H_2O, ppmv}$')
#ax[2,0].set_yscale('log')

# other. gas and ambient temperatures
#ax[2,2].plot(LGR_time,LGR["         GasT_C"],'-',markersize=2)
#ax[2,1].plot(LGR_time,LGR["Amb_T"],'.',markersize=2)
#ax[2,1].legend(['Amb_T'],edgecolor='none',facecolor='none',fontsize='xx-small')
#ax[2,1].set_ylabel('Temperatures, C')

# other. cell pressure
#ax[0,3].plot(LGR_time,LGR["      GasP_torr"],'.',markersize=2)
#ax[0,3].set_ylabel('$\mathregular{Gas P, torr}$')

# formatting
ax[2,0].set_xticklabels(ax[2,0].get_xticks(), rotation = 45)
ax[2,1].set_xticklabels(ax[2,1].get_xticks(), rotation = 45)
ax[2,0].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.tight_layout()
plt.show()

#fig.savefig('fig1.png',dpi=300)

# %% plot correlations
# sync data
COMA_1s = LGR.groupby(pd.Grouper(key="time", freq="1s")).mean()
IWG1_1s = IWG1.groupby(pd.Grouper(key="time", freq="1s")).mean()
sync_data = pd.merge(COMA_1s, IWG1_1s, how='inner', on=['time'])
ix_8 = np.ravel(np.where(LGR["MIU_Valve"]==8))

# vertical profile
#fig, ax = plt.subplots(1, 1, figsize=(6,5),dpi=200)
#plt.plot(sync_data["Pressure Altitude"][ix_8],sync_data["CO_ppm"][ix_8]*1000,'.')

# N-S profile
fig, ax = plt.subplots(1, 1, figsize=(6,5),dpi=200)
plt.plot(sync_data["Latitude"][ix_8],sync_data["CO_ppm"][ix_8]*1000,'.')
plt.grid()
plt.ylim([40,100])

