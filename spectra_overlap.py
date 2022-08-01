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
from matplotlib.colors import Normalize

filename_s = '../Data/2022-07-21/n2o-co_2022-07-21_s0001.txt'
filename_f = '../Data/2022-07-21/n2o-co_2022-07-21_f0001.txt'

# %% read file
# load spectra file
f = open(filename_s, "r")
txt = f.read()
f.close()
spectra = txt.splitlines()

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
LGR_time=LGR_time[0]

LGR_CO = LGR["      [CO]d_ppm"]*1000
LGR_N2O = LGR["     [N2O]d_ppm"]*1000


# %% plot
fig = plt.figure(constrained_layout=True,figsize=(10,8))
ax = fig.subplot_mosaic(
    [
        ["A"],
        ["B"],
        ["B"]
    ])

c0 = min(SPECTRA_TIME).timestamp()
c1 = max(SPECTRA_TIME).timestamp()
LGR_time_epoch = [x.timestamp() for x in LGR_time]

# define colormap used by both subplots
cmap = cm.viridis
norm = Normalize(vmin=c0, vmax=c1)

ax["A"].scatter(x=LGR[" SpectraID"],y=LGR_N2O,c=norm(LGR_time_epoch),s = 10)

for ii in range(1000,max(SPECTRA_ID),2000):#start,stop,step
    x0 = 180+ii*1126
    x1 = 1123+ii*1126   
    floats = [float(x) for x in spectra[x0:x1]]
    c = cmap(norm(SPECTRA_TIME[ii].timestamp()))
    l2, = ax["B"].plot(floats,color=c,label=SPECTRA_TIME[ii].strftime("%Y-%m-%d %H:%M:%S"))

ax["A"].set_ylim(300,350)
ax["B"].set_ylim(-1.0,-0.7)
ax["B"].legend()
fig.tight_layout()
