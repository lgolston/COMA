# -*- coding: utf-8 -*-
"""
Plot temperature readings during EEL chamber run
"""

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates

# set font size
plt.rcParams['axes.labelsize'] = 8
plt.rcParams['legend.fontsize'] = 8
plt.rcParams['xtick.labelsize'] = 7
plt.rcParams['ytick.labelsize'] = 7

# read chamber temperature file (2022-05-19)
CHAMBER = pd.read_csv('../Data/2022-05-19/COMA_2022_05_19',skiprows = 10,sep='\t',header=None)
CHAMBER.columns = ['PRESSURE','CHAMBER','CUR S REST','CPU','LASER CUR T','PWR SPLY','LASER BAKING','MID-RIB','EXT SIDE','SECONDS','DATETIME']	
CHAMBER_TIME = [datetime.strptime(tstamp,"%H:%M:%S %d %b %Y") for tstamp in CHAMBER['DATETIME']]

"""
# read chamber temperature file (2022-05-20)
CHAMBER1 = pd.read_csv('../Data/2022-05-20/COMA_2022_05_20',skiprows = 10,sep='\t',header=None)
CHAMBER1.columns = ['PRESSURE','CHAMBER','CUR S REST','CPU','LASER CUR T','PWR SPLY','LASER BAKING','MID-RIB','EXT SIDE','SECONDS','DATETIME']	
CHAMBER1_TIME = [datetime.strptime(tstamp,"%H:%M:%S %d %b %Y") for tstamp in CHAMBER1['DATETIME']]

CHAMBER2 = pd.read_csv('../Data/2022-05-20/COMA_2022_05_20-02',skiprows = 10,sep='\t',header=None)
CHAMBER2.columns = ['PRESSURE','CHAMBER','CUR S REST','CPU','LASER CUR T','PWR SPLY','LASER BAKING','MID-RIB','EXT SIDE','SECONDS','DATETIME']	
CHAMBER2_TIME = [datetime.strptime(tstamp,"%H:%M:%S %d %b %Y") for tstamp in CHAMBER2['DATETIME']]

CHAMBER = pd.concat([CHAMBER1,CHAMBER2])
CHAMBER_TIME = CHAMBER1_TIME + CHAMBER2_TIME
"""

# %% plot
fig, ax1 = plt.subplots(figsize=(6.5,3.7))
ax1.plot(CHAMBER_TIME,CHAMBER['CHAMBER'],label='CHAMBER')
ax1.plot(CHAMBER_TIME,CHAMBER['CUR S REST'],label='CUR S REST')
ax1.plot(CHAMBER_TIME,CHAMBER['CPU'],label='CPU')
ax1.plot(CHAMBER_TIME,CHAMBER['LASER CUR T'],label='LASER CUR T')
ax1.plot(CHAMBER_TIME,CHAMBER['PWR SPLY'],label='PWR SPLY')
ax1.plot(CHAMBER_TIME,CHAMBER['LASER BAKING'],label='LASER BACKING')
ax1.plot(CHAMBER_TIME,CHAMBER['MID-RIB'],label='MID-RIB')
ax1.plot(CHAMBER_TIME,CHAMBER['EXT SIDE'],label='EXT SIDE')
ax1.grid()
ax1.set_ylim([-20,120])
ax2 = ax1.twinx()
ax2.plot(CHAMBER_TIME,CHAMBER['PRESSURE']/3280.84,'k',label='PRESSURE') # ft to km
ax1.legend(loc='upper left',ncol=2)
ax1.set_ylabel('Temperatures, °C')
ax2.set_ylabel('Chamber altitude, km')
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax1.set_xlabel('Time')
plt.tight_layout()

#plt.savefig('fig_output.png',dpi=200)