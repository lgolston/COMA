# -*- coding: utf-8 -*-
"""
Plot spectra as a movie file

add
- get EPOCH_TIME working
- plot concentration time series
- match spectra ID
- label Slider (SpectraID and Time) and axes
"""

# %% read file
#filename_s = '../Data/2021-08-06/n2o-co_2021-08-06_s0002.txt'
#filename_f = '../Data/2021-08-06/n2o-co_2021-08-06_f0002.txt'

#filename_s = '../Data/2021-08-10/n2o-co_2021-08-10_s0003.txt'
#filename_f = '../Data/2021-08-10/n2o-co_2021-08-10_f0003.txt'

#filename_s = '../Data/2021-08-16/n2o-co_2021-08-16_s0002.txt'
#filename_f = '../Data/2021-08-16/n2o-co_2021-08-16_f0002.txt'

filename_s = '../Data/2021-08-17/n2o-co_2021-08-17_s0002.txt'
filename_f = '../Data/2021-08-17/n2o-co_2021-08-17_f0002.txt'

import pandas as pd
import matplotlib.pyplot as plt
from datetime import timedelta, datetime
import time
import matplotlib.animation as manimation

# load spectra file
f = open(filename_s, "r")
txt = f.read()
f.close()
spectra = txt.splitlines()

block_length = 1126
num_lines = int(len(spectra)/block_length)
ID = [spectra[2+x*block_length][12:] for x in range(num_lines)] # SPECTRA_ID

# load output file
LGR = pd.read_csv(filename_f,sep=',',header=1)

LGR_time = LGR["                     Time"]
LGR_time = [datetime.strptime(tstamp,"  %m/%d/%Y %H:%M:%S.%f") for tstamp in LGR_time]
LGR_time = pd.DataFrame(LGR_time)
LGR_time=LGR_time[0]

LGR_CO = LGR["      [CO]d_ppm"]*1000
#LGR_CO_median = pd.Series(LGR_CO)
#LGR_CO_median = LGR_CO_median.rolling(25).median()

LGR_N2O = LGR["     [N2O]d_ppm"]*1000
#LGR_N2O_median = pd.Series(LGR_N2O)
#LGR_N2O_median = LGR_N2O_median.rolling(25).median()

# open a movie output file
FFMpegWriter = manimation.writers['ffmpeg']
metadata = dict(title='Movie Test', artist='Matplotlib',
                comment='a red circle following a blue sine wave')
writer = FFMpegWriter(fps=15, metadata=metadata)

# %% plot
fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(10, 6))

ax[0,0].plot(LGR[" SpectraID"],LGR["     [N2O]d_ppm"]*1000)

ax[0,1].plot(LGR[" SpectraID"],LGR["      [CO]d_ppm"]*1000)

#ax1.set_position([0.12, 0.62, 0.85, 0.35]) #left, bottom, width, height
#ax2.set_position([0.12, 0.18, 0.85, 0.35])

floats = [float(x) for x in spectra[180:1123]]
l1, = ax[1,0].plot(floats,'.')
l2, = ax[1,1].plot(floats,'.')

with writer.saving(fig, "writer_test.mp4", 100):
    for ii in range(100,len(LGR_CO)-1):
        # N2O concentration time series
        ix = int(ID[ii])
        
        ax[0,0].set_xlim(ix-100,ix)
        ax[0,0].set_ylim(round(LGR_N2O[ix])-5,round(LGR_N2O[ix])+5)
        
        # CO concentration time series
        ax[0,1].set_xlim(ix-100,ix)
        ax[0,1].set_ylim(round(LGR_CO[ix])-5,round(LGR_CO[ix])+5)
        
        # N2O laser scan
        x0 = 180+ii*1126
        x1 = 1123+ii*1126
        floats = [float(x) for x in spectra[x0:x1]]
        l1.set_ydata(floats)
        ax[1,0].set_xlim(400,600)
        ax[1,0].set_ylim(-0.90,-0.60)
        
        # CO laser scan
        l2.set_ydata(floats)
        ax[1,1].set_xlim(700,900)
        ax[1,1].set_ylim(-0.75,-0.55)
                
        plt.title(ix)
        
        writer.grab_frame()