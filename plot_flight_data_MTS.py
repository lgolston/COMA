# -*- coding: utf-8 -*-
"""
plot data after a WB-57 flight
using COMA and IWG1 from MTS
"""

# %% EDIT THESE
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.dates as mdates

case = 2

if case == 0: # transit Houston to Seattle
    filename_COMA = '../Data/2022-07-21/telemetry-62d94e74c5950a96da9a1f8e.csv'
    cur_day = datetime(2022,7,21)
if case == 1: #no COMA data Seattle to Anchorage
    1
elif case == 2: # transit Anchorage to Adak
     filename_COMA = '../Data/2022-07-24/telemetry-62ddbb1d9f75ebc8ab741691.csv'
     #filename_MMS = '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20220718_RA.ict'
     cur_day = datetime(2022,7,24)

# %% data
# read COMA data
LGR = pd.read_csv(filename_COMA,sep=',',header=0)
#LGR = pd.concat([LGR1,LGR2],ignore_index=True)

LGR_time = LGR["Timestamp"]
LGR_time = [datetime.strptime(tstamp,"%Y-%m-%dT%H:%M:%S.%fZ") for tstamp in LGR_time]
LGR_time = pd.DataFrame(LGR_time)
LGR_time=LGR_time[0]

# index MIU valves
#ix_8 = np.ravel(np.where( (LGR["      MIU_VALVE"]==8) & (LGR["      GasP_torr"]>52.45) & (LGR["      GasP_torr"]<52.65)) ) # Inlet
#ix_8 = np.ravel(np.where(LGR["      MIU_VALVE"]==8)) # inlet
#ix_7 = np.ravel(np.where(LGR["      MIU_VALVE"]==7)) # inlet (lab)
#ix_3 = np.ravel(np.where(LGR["      MIU_VALVE"]==3)) # high cal
#ix_2 = np.ravel(np.where(LGR["      MIU_VALVE"]==2)) # low cal
#ix_1 = np.ravel(np.where(LGR["      MIU_VALVE"]==1)) # flush

# convert laser and supercool voltage to temperature [values from Ian]
def V_to_T(voltage):
    a = 1.1279*10**-3
    b = 2.3429*10**-4
    c = 8.7298*10**-8
    R = voltage/(100*10**-6) # 100 microAmp
    return 1/(a+b*np.log(R)+c*np.log(R)**3) - 273.15


# %% plot data
plt.rc('axes', labelsize=6) # xaxis and yaxis labels
plt.rc('xtick', labelsize=6) # xtick labels
plt.rc('ytick', labelsize=6) # ytick labels
fig, ax = plt.subplots(3, 2, figsize=(9,3.5),dpi=200,sharex=True)

# 1. CO
ax[0,0].plot(LGR_time,LGR["CO_ppm"]*1000,'k.',markersize=2)
ax[0,0].set_ylabel('CO (dry), ppbv')
ax[0,0].set_ylim(0,300)

# 2. N2O
ax[1,0].plot(LGR_time,LGR["N2O_ppm"]*1000,'.',markersize=2)
ax[1,0].set_ylabel('$\mathregular{N_2O (dry), ppbv}$')
ax[1,0].set_ylim(200,350)

# 3. H2O
ax[2,0].plot(LGR_time,LGR["H2O_ppm"],'.',markersize=2)
ax[2,0].set_ylabel('$\mathregular{H_2O, ppmv}$')
ax[2,0].set_yscale('log')

# 4. laser temperature
laserT = V_to_T(LGR["AIN6"])
ax[0,1].plot(LGR_time,laserT,'.',markersize=2) # laser temp
ax[0,1].set_ylabel('Laser T, C')

# 5. supercool temperature
supercoolT = V_to_T(LGR["AIN5"])
ax[1,1].plot(LGR_time,supercoolT,'.',markersize=2)
ax[1,1].set_ylabel('Supercool T, C')

# 9. gas and ambient temperatures
#ax[2,2].plot(LGR_time,LGR["         GasT_C"],'-',markersize=2)
ax[2,1].plot(LGR_time,LGR["Amb_T"],'-',markersize=2)
ax[2,1].legend(['Amb_T'],edgecolor='none',facecolor='none',fontsize='xx-small')
ax[2,1].set_ylabel('Temperatures, C')

# 10. cell pressure
#ax[0,3].plot(LGR_time,LGR["      GasP_torr"],'.',markersize=2)
#ax[0,3].set_ylabel('$\mathregular{Gas P, torr}$')

# formatting
ax[2,0].set_xticklabels(ax[2,0].get_xticks(), rotation = 45)
ax[2,1].set_xticklabels(ax[2,1].get_xticks(), rotation = 45)
ax[2,0].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.tight_layout()
plt.show()

#fig.savefig('fig1.png',dpi=300)