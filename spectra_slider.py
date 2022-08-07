# -*- coding: utf-8 -*-
"""
Plot spectra below concentration time series

add
- get EPOCH_TIME working
- match spectra ID
- label Slider (SpectraID and Time) and axes

fitting
- scipy.optimize
- common to use Levenberg–Marquardt algorithm
"""

# %% header
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.widgets import Slider
import hapi
hapi.db_begin('HAPI')

case = 'RF05'

if case == 'RF05':
    filename_f = '../Data/2022-08-06/n2o-co_2022-08-06_f0000.txt'
    filename_s = '../Data/2022-08-06/n2o-co_2022-08-06_s0000.txt'
    cur_day = datetime(2022,8,6)

# %% set up HITRAN Application Programming Interface (HAPI)
# Download spectral data using the Python library HAPI
# Can also refer to Los Gatos information used in peaks_000.ini file
# working in range 4.565-4.567 (2189-2191)
#hapi.fetch('H2O',1,1,2189,2191)
#hapi.fetch('CO',5,1,2189,2191)
#hapi.fetch('N2O',4,1,2189,2191)

# %% load files
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
LGR_N2O = LGR["     [N2O]d_ppm"]*1000

# %% plot time series and spectra
plt.rc('xtick', labelsize=10) 
plt.rc('ytick', labelsize=10) 

# set up plot with slider
fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(15, 7))

ax1.plot(LGR[" SpectraID"],LGR["     [N2O]d_ppm"]*1000,linewidth=2)
l1, = ax1.plot([50,50],[0,1000])
ax1.grid('on')

raw_scan = np.ravel([float(x) for x in spectra[180:1123]])
l2, = ax2.plot(raw_scan,'.')
#ax2.set_xlim(300,900)
ax2.set_xlim(300,875)
ax2.set_ylim(-0.05,0.25)
ax2.grid('on')

x_fit = np.concatenate( ( list(range(175,300)), list(range(600,675)) ) )
x_plot = list(range(0,943))
l3, = ax2.plot(x_plot,raw_scan[x_plot],'k:')

axcolor = 'lightgoldenrodyellow'
axfreq = plt.axes([0.15, 0.05, 0.76, 0.03], facecolor=axcolor)
sfreq = Slider(axfreq, 'Freq', 0, len(ID), valinit=1, valstep=1)

ax1.set_position([0.07, 0.62, 0.90, 0.35]) #left, bottom, width, height
ax2.set_position([0.07, 0.18, 0.90, 0.35])

# create class (allows data to be accessed outside of the callback function)
class Spectral:
    # key variables
    raw_scan = None
    baseline = None
    ringdown = None
    
    # spectral parameters
    H2O_center = 340
    N2O_center_a = 425
    N2O_center_a = 458
    N2O_center = 542
    CO_center = 806
    
    nu_CO,coef_CO = hapi.absorptionCoefficient_Voigt(SourceTables='CO',
                                                 Diluent={'air':1.0},
                                                 WavenumberRange = [2189, 2191],
                                                 WavenumberStep=0.001,
                                                 Environment={'p':0.1,'T':296})

    nu_N2O,coef_N2O = hapi.absorptionCoefficient_Voigt(SourceTables='N2O',
                                                 Diluent={'air':1.0},
                                                 WavenumberRange = [2189, 2191],
                                                 WavenumberStep=0.001,
                                                 Environment={'p':0.1,'T':296})

    nu_H2O,coef_H2O = hapi.absorptionCoefficient_Voigt(SourceTables='H2O',
                                                 Diluent={'air':1.0},
                                                 WavenumberRange = [2189, 2191],
                                                 WavenumberStep=0.001,
                                                 Environment={'p':0.1,'T':296})
    
    # function called when slider is moved
    def update(self, event):
        # get value of slider
        ii = sfreq.val
                
        # plot vertical line on concentration time series (top plot)
        l1.set_data([ii,ii],[0,1000])
        
        # set axes limits (top plot)
        ix = int(ID[ii])
        ax1.set_xlim(ix-50,ix+50)
        ax1.set_ylim(LGR_N2O[ix]-5,LGR_N2O[ix]+5)
        
        # select the laser scan
        x0 = 180+ii*1126
        x1 = 1123+ii*1126
        self.raw_scan = np.ravel([float(x) for x in spectra[x0:x1]])
        
        # select the ringdown scan
        x0 = 17+ii*1126
        x1 = 176+ii*1126
        self.ringdown = np.ravel([float(x) for x in spectra[x0:x1]])
        
        # calculate spectral baseline
        combined = self.raw_scan[x_fit]
        z1 = np.polyfit(x_fit, combined, 2)
        self.baseline = np.polyval(z1,x_plot)
        
        # plot the scan (bottom plot)
        #l3.set_data(x_plot,baseline)
        #l2.set_ydata(floats)
        l2.set_ydata(self.baseline-self.raw_scan)
        
        # perform spectral fitting
        # ...
        #plt.plot(nu_CO,coef_CO*100E-9,'b')
        #plt.plot(nu_N2O,coef_N2O*300E-9,'g')
        #plt.plot(nu_H2O,coef_H2O*1E-2,'m')
        #plt.xlim(2189.8,2190.7)
        
        # update figure
        fig.canvas.draw_idle()

    def voigt():
        return 1

# set up callback
callback = Spectral()   
sfreq.on_changed(callback.update)
plt.show()