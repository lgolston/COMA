# -*- coding: utf-8 -*-
"""
Plot spectra

add
- match time window to selected data in time series
- filter data to ix_8
"""

# %% header
import pandas as pd
import matplotlib.pyplot as plt
from datetime import timedelta, datetime
import matplotlib.cm as cm
import numpy as np
from matplotlib.colors import Normalize
import matplotlib.dates as mdates

# set font size
plt.rcParams['axes.labelsize'] = 8
plt.rcParams['legend.fontsize'] = 8
plt.rcParams['xtick.labelsize'] = 7
plt.rcParams['ytick.labelsize'] = 7
plt.rcParams.update({'mathtext.default': 'regular' } ) # not italics

# %% filenames
#filename_f = '../Data/2022-05-19/n2o-co_2022-05-19_f0000.txt' # EEL Day 1
#filename_s = '../Data/2022-05-19/n2o-co_2022-05-19_s0000.txt' # EEL Day 1

#filename_f = '../Data/2022-05-20/n2o-co_2022-05-20_f0000.txt' # EEL Day 2
#filename_s = '../Data/2022-05-20/n2o-co_2022-05-20_s0000.txt' # EEL Day 2

#filename_f = '../Data/2022-07-21/n2o-co_2022-07-21_f0001.txt' # Transit 2
#filename_s = '../Data/2022-07-21/n2o-co_2022-07-21_s0001.txt' 

filename_f = '../Data/2022-08-18/n2o-co_2022-08-18_f0000.txt'
filename_s = '../Data/2022-08-18/n2o-co_2022-08-18_s0000.txt'


# %% read file
# load spectra file
print("Loading files")

f = open(filename_s, "r")
txt = f.read()
f.close()
spectra = txt.splitlines()

# parse SPECTRA_ID
block_length = 1126
num_lines = int(len(spectra)/block_length)
SPECTRA_ID = [int(spectra[2+x*block_length][12:]) for x in range(num_lines)]

# H:MM:SS.FFF time
#SPECTRA_TIME = [(spectra[3+x*block_length][6:]) for x in range(num_lines)]

# EPOCH TIME
EPOCH_TIME = [int(spectra[4+x*1126][11:]) for x in range(num_lines)]
x0 = datetime(1970,1,1)
SPECTRA_TIME = [x0+timedelta(seconds=t/1000) for t in EPOCH_TIME]

# load output file
LGR = pd.read_csv(filename_f,sep=',',header=1)

LGR_time = LGR["                     Time"]
LGR_time = [datetime.strptime(tstamp,"  %m/%d/%Y %H:%M:%S.%f") for tstamp in LGR_time]
LGR_time = pd.DataFrame(LGR_time)
LGR_time = LGR_time[0]

LGR_CO = LGR["      [CO]d_ppm"]*1000
LGR_N2O = LGR["     [N2O]d_ppm"]*1000

# %% calculate laser power
laser_power = np.zeros(num_lines)

print("Calculating laser power:")

for ii in range(num_lines):
    # select the laser scan (LR0)
    x0 = 180+ii*1126
    x1 = 1123+ii*1126
    raw_scan = np.ravel([float(x) for x in spectra[x0:x1]])
    
    # select the ringdown scan (RD0)
    x0 = 17+ii*1126
    x1 = 176+ii*1126
    ringdown = np.ravel([float(x) for x in spectra[x0:x1]])
    
    # calculate laser power
    laser_power[ii] = np.mean(raw_scan[-11:-1]) - np.mean(ringdown[-11:-1])

# %% plot
print("Plotting")

# set up figure
fig = plt.figure(constrained_layout=True,figsize=(10,8))
ax = fig.subplot_mosaic(
    [
        ["A"],
        ["B"],
        ["B"]
    ])

# define colormap used by both subplots
c0 = min(SPECTRA_TIME).timestamp()
c1 = max(SPECTRA_TIME).timestamp()
LGR_time_epoch = [x.timestamp() for x in LGR_time]
cmap = cm.viridis
norm = Normalize(vmin=c0, vmax=c1)

# plot time series
ax["A"].scatter(x=LGR_time,y=LGR_CO,c=norm(LGR_time_epoch),s = 10)
ax["A"].set_xlabel('SpectraID')
ax["A"].set_ylim(0,150)
#ax["A"].set_ylim(300,350)
#ax["A"].set_ylim(220,250)

ax_twin = ax["A"].twinx()
ax_twin.plot(SPECTRA_TIME,laser_power,'k')
ax_twin.set_ylim(0.40,0.47)

# plot spectra
for ii in range(1000,max(SPECTRA_ID),2000):#start,stop,step
    x0 = 180+ii*1126
    x1 = 1123+ii*1126   
    floats = [float(x) for x in spectra[x0:x1]]
    c = cmap(norm(SPECTRA_TIME[ii].timestamp()))
    l2, = ax["B"].plot(floats,color=c,label=SPECTRA_TIME[ii].strftime("%Y-%m-%d %H:%M:%S"))

ax["B"].set_ylim(-1.0,-0.7)
ax["B"].legend()
fig.tight_layout()

#fig.savefig('fig_output.png',dpi=300)

# %% chamber test specific
"""
day = 1

if day == 1:
    # read chamber temperature file (2022-05-19)
    CHAMBER = pd.read_csv('../Data/2022-05-19/COMA_2022_05_19',skiprows = 10,sep='\t',header=None)
    CHAMBER.columns = ['PRESSURE','CHAMBER','CUR S REST','CPU','LASER CUR T','PWR SPLY','LASER BAKING','MID-RIB','EXT SIDE','SECONDS','DATETIME']	
    CHAMBER_TIME = [datetime.strptime(tstamp,"%H:%M:%S %d %b %Y") for tstamp in CHAMBER['DATETIME']]

elif day == 2:
    # read chamber temperature file (2022-05-20)
    CHAMBER1 = pd.read_csv('../Data/2022-05-20/COMA_2022_05_20',skiprows = 10,sep='\t',header=None)
    CHAMBER1.columns = ['PRESSURE','CHAMBER','CUR S REST','CPU','LASER CUR T','PWR SPLY','LASER BAKING','MID-RIB','EXT SIDE','SECONDS','DATETIME']	
    CHAMBER1_TIME = [datetime.strptime(tstamp,"%H:%M:%S %d %b %Y") for tstamp in CHAMBER1['DATETIME']]
    
    CHAMBER2 = pd.read_csv('../Data/2022-05-20/COMA_2022_05_20-02',skiprows = 10,sep='\t',header=None)
    CHAMBER2.columns = ['PRESSURE','CHAMBER','CUR S REST','CPU','LASER CUR T','PWR SPLY','LASER BAKING','MID-RIB','EXT SIDE','SECONDS','DATETIME']	
    CHAMBER2_TIME = [datetime.strptime(tstamp,"%H:%M:%S %d %b %Y") for tstamp in CHAMBER2['DATETIME']]
    
    CHAMBER = pd.concat([CHAMBER1,CHAMBER2])
    CHAMBER_TIME = CHAMBER1_TIME + CHAMBER2_TIME

fig, ax = plt.subplots(ncols=1,nrows=3,figsize=(6,6),sharex=True)
ax[0].plot(CHAMBER_TIME,CHAMBER['CHAMBER'],label='CHAMBER')
ax[0].grid()
ax[0].set_ylim([-20,40])
ax0_twin = ax[0].twinx()
ax0_twin.plot(CHAMBER_TIME,CHAMBER['PRESSURE']/3280.84,'k',label='PRESSURE') # ft to km
ax[0].legend(loc='upper left',ncol=2)
ax[0].set_ylabel('Temperatures, °C')
ax0_twin.set_ylabel('Chamber altitude, km')
ax[0].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax[0].set_xlabel('Time')

ax[1].scatter(x=LGR_time[600:-1]-timedelta(hours=7),y=LGR_CO[600:-1],c=norm(LGR_time_epoch[600:-1]),s = 6)
ax[1].set_ylim(225,240)
ax[1].set_ylabel('CO, ppb')
ax1_twin = ax[1].twinx()
ax1_twin.plot(LGR_time[600:-1]-timedelta(hours=7),laser_power[600:-1],'k')
ax1_twin.set_ylim(0.40,0.47)

ax[2].scatter(x=LGR_time[600:-1]-timedelta(hours=7),y=LGR_N2O[600:-1],c=norm(LGR_time_epoch[600:-1]),s = 6)
ax[2].set_ylim(300,350)
ax[2].set_ylabel(r'$N_2O, ppb$')
ax2_twin = ax[2].twinx()
ax2_twin.plot(LGR_time[600:-1]-timedelta(hours=7),laser_power[600:-1],'k')
ax2_twin.set_ylim(0.40,0.47)

ax1_twin.set_ylabel('Laser power')
ax2_twin.set_ylabel('Laser power')
ax[0].set_title('EEL Day 1 - May 19, 2022',fontsize=8)
fig.tight_layout()

#plt.savefig('fig_output.png',dpi=300)
"""
