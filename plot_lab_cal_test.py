# -*- coding: utf-8 -*-
"""
simpler plotting script aimed at the lab runs
"""

# %% EDIT THESE
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.dates as mdates

case = 'Nov2'

if case == 'Nov1': # room air (24 hr)
    filename_COMA = '../Data/2022-11-01/n2o-co_2022-11-01_f0001.txt'
elif case == 'Nov2': # room air (last hr)
    filename_COMA = '../Data/2022-11-02/n2o-co_2022-11-02_f0000.txt'
elif case == 'Nov8': # scuba air
    filename_COMA = '../Data/2022-11-08/n2o-co_2022-11-08_f0000.txt'
else:
    print('not a valid case')
    
# %% data
# read COMA data
LGR = pd.read_csv(filename_COMA,sep=',',header=1)

LGR_time = LGR["                     Time"]
LGR_time = [datetime.strptime(tstamp,"  %m/%d/%Y %H:%M:%S.%f") for tstamp in LGR_time]
LGR_time = pd.DataFrame(LGR_time)
LGR_time=LGR_time[0]

td = -7 # timezone offset
LGR_time = LGR_time+timedelta(hours=td)

# %% quick plot
fig, ax = plt.subplots(3, 3, figsize=(12,6),sharex=True)

ax[0,0].plot(LGR_time,LGR["         GasT_C"],'.',markersize=2)
ax[0,0].set_ylabel('GasT_C')

ax[0,1].plot(LGR_time,LGR["           AIN6"],'k.',markersize=2) # supercool?
ax_twin = ax[0,1].twinx()
ax_twin.plot(LGR_time,LGR["           AIN5"],'g.',markersize=2) # laser temp?
ax[0,1].set_ylabel('Laser')
ax_twin.set_ylabel('Supercool')

ax[0,2].plot(LGR_time,LGR["      GasP_torr"],'.',markersize=2)
ax[0,2].set_ylabel('$\mathregular{Gas P, torr}$')

ax[1,0].plot(LGR_time,LGR["      [CO]d_ppm"]*1000,'.',markersize=2)
ax[1,0].set_ylabel('CO, ppbv')
ax[1,0].set_ylim(0,400)

ax[1,1].plot(LGR_time,LGR["     [N2O]d_ppm"]*1000,'.',markersize=2)
ax[1,1].set_ylabel('$\mathregular{N_2O, ppbv}$')

ax[1,2].plot(LGR_time,LGR["      [H2O]_ppm"],'.',markersize=2)
ax[1,2].set_ylabel('$\mathregular{H_2O, ppmv}$')

ax[2,0].plot(LGR_time,LGR["         AmbT_C"],'.',markersize=2)
ax[2,0].set_ylabel('AmbT_C')

ax[2,1].plot(LGR_time,LGR["            Gnd"],'.',markersize=2)
ax[2,1].set_ylabel('Gnd')

ax[2,2].plot(LGR_time,LGR["          Peak0"],'.',markersize=2)
ax[2,2].set_ylabel('Peak0')

# formatting
ax[2,0].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.tight_layout()
plt.show()

# plt.savefig('fig_output.png',dpi=200)

# %% plot CO and N2O
ix_2 = np.ravel(np.where(LGR["      MIU_VALVE"]==2))
ix_3 = np.ravel(np.where(LGR["      MIU_VALVE"]==3))
ix_7 = np.ravel(np.where(LGR["      MIU_VALVE"]==7))

fig, ax = plt.subplots(2, 1, figsize=(8,6),sharex=True)
ax[0].plot(LGR_time[ix_7],LGR["      [CO]d_ppm"][ix_7]*1000,'b.',markersize=2)
ax[0].plot(LGR_time[ix_2],LGR["      [CO]d_ppm"][ix_2]*1000,'k.',markersize=2)
ax[0].plot(LGR_time[ix_3],LGR["      [CO]d_ppm"][ix_3]*1000,'r.',markersize=2)
ax[0].set_ylabel('CO, ppbv')
#ax[0].set_ylim(225,242)

ax[1].plot(LGR_time[ix_7],LGR["     [N2O]d_ppm"][ix_7]*1000,'b.',markersize=2)
ax[1].plot(LGR_time[ix_2],LGR["     [N2O]d_ppm"][ix_2]*1000,'k.',markersize=2)
ax[1].plot(LGR_time[ix_3],LGR["     [N2O]d_ppm"][ix_3]*1000,'r.',markersize=2)
ax[1].set_ylabel('$\mathregular{N_2O, ppbv}$')
#ax[1].set_ylim(315,340)

ax[0].grid()
ax[1].grid()
ax[0].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax[1].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax[1].set_xlabel('Local time')

#if case == 3:
#    ax[0].set_xlim([datetime(2022,5,19,12)],[datetime(2022,5,19,17)])

# plt.savefig('fig1_output.png',dpi=200)

# %% plot time series
fig, ax = plt.subplots(2, 1, figsize=(8,6),sharex=True)
ix = np.ravel( np.where( (LGR_time>datetime(2022,11,1,10,48))&(LGR_time<datetime(2022,11,1,10,49))) )
ax[0].plot(LGR["      [CO]d_ppm"][ix].values*1000,'b',markersize=2)
ax[1].plot(LGR["     [N2O]d_ppm"][ix].values*1000,'b',markersize=2)
ix = np.ravel( np.where( (LGR_time>datetime(2022,11,1,10,52))&(LGR_time<datetime(2022,11,1,10,53))) )
ax[0].plot(LGR["      [CO]d_ppm"][ix].values*1000,'b',markersize=2)
ax[1].plot(LGR["     [N2O]d_ppm"][ix].values*1000,'b',markersize=2)
ix = np.ravel( np.where( (LGR_time>datetime(2022,11,1,11,3,30))&(LGR_time<datetime(2022,11,1,11,4,30))) )
ax[0].plot(LGR["      [CO]d_ppm"][ix].values*1000,'b',markersize=2)
ax[1].plot(LGR["     [N2O]d_ppm"][ix].values*1000,'b',markersize=2)

ix = np.ravel( np.where( (LGR_time>datetime(2022,11,1,11,15))&(LGR_time<datetime(2022,11,1,11,16))) )
ax[0].plot(LGR["      [CO]d_ppm"][ix].values*1000,'y',markersize=2)
ax[1].plot(LGR["     [N2O]d_ppm"][ix].values*1000,'y',markersize=2)

ix = np.ravel( np.where( (LGR_time>datetime(2022,11,1,10,55,20))&(LGR_time<datetime(2022,11,1,10,57))) )
ax[0].plot(LGR["      [CO]d_ppm"][ix].values*1000,'g',markersize=2)
ax[1].plot(LGR["     [N2O]d_ppm"][ix].values*1000,'g',markersize=2)
ix = np.ravel( np.where( (LGR_time>datetime(2022,11,1,10,59,0))&(LGR_time<datetime(2022,11,1,11,1))) )
ax[0].plot(LGR["      [CO]d_ppm"][ix].values*1000,'g',markersize=2)
ax[1].plot(LGR["     [N2O]d_ppm"][ix].values*1000,'g',markersize=2)

ax[0].set_ylim(45,55)
ax[1].set_ylim(250,270)

# %% plot cal gas
"""
# select MIU data
ix_3 = np.ravel(np.where(LGR["      MIU_VALVE"]==3)) # high cal
ix_2 = np.ravel(np.where(LGR["      MIU_VALVE"]==2)) # low cal

df_lowcal = pd.DataFrame({'time': LGR_time[ix_2], 'CO_dry': LGR["      [CO]d_ppm"][ix_2]*1000, 'N2O_dry': LGR["     [N2O]d_ppm"][ix_2]*1000})
df_lowcal['groups'] = (df_lowcal.index.to_series().diff()>5).cumsum()
df_highcal = pd.DataFrame({'time': LGR_time[ix_3], 'CO_dry': LGR["      [CO]d_ppm"][ix_3]*1000, 'N2O_dry': LGR["     [N2O]d_ppm"][ix_3]*1000})
df_highcal['groups'] = (df_highcal.index.to_series().diff()>5).cumsum()

fig2, ax2 = plt.subplots(1, 2, figsize=(6,2.5),dpi=200)

for ct, data in df_lowcal.groupby('groups'):
    ax2[0].plot(data['CO_dry'].values,marker='.')
    #ax2[0].set_ylim(68,78)
        
for ct, data in df_highcal.groupby('groups'):
    ax2[1].plot(data['CO_dry'].values,marker='.')
    #ax2[1].set_ylim(170,200)

ax2[0].grid()
ax2[0].set_ylabel('CO, ppb')
ax2[0].set_xlabel('Seconds')
ax2[1].grid()
ax2[1].set_ylabel('N2O, ppb')
ax2[1].set_xlabel('Seconds')

plt.tight_layout()

# plt.savefig('fig2_output.png',dpi=200)
"""
