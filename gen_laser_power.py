# -*- coding: utf-8 -*-
"""
Create file with laser power information
"""

# %% load libraries and data
import numpy as np
import pandas as pd
import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
import os
import re

# %% load all filenames
# walk through directory
root = "G:/My Drive/3_COMA/Data/"

filenames = []

for r, d, f in os.walk(root):
    for file in f:
        # add $ add end to exclude .zip (or otherwise)
        m = re.search("2022(.*)s.{4}\.txt", file)
            
        # read data
        # note above: limit file length to exclude modified _no_10s_cal 'f' files
        if bool(m and len(file)==27):
            filename_COMA = os.path.join(r, file)
            print(filename_COMA)
            filenames.append(filename_COMA)

# %% main loop
#filenames = [filename_COMA] # do one file for now

for fname in filenames:
    print('Processing case:' + fname)
    
    # %% calculate laser power from spectra    
    # load spectra file
    print("Calculating laser power:")
    f = open(fname, "r")
    txt = f.read()
    f.close()
    spectra = txt.splitlines()
    
    # calculate number of spectra in file
    block_length = 1126 # 160 RD0; 944 LR0; + other text
    num_lines = int(len(spectra)/block_length)
    
    # parse header
    # known data flags = JUNK, BOOTSTRAP, MEASURE
    # exclude JUNK (first row) to match 'f' file
    SPECTRA_ID = np.array([int(spectra[2+x*block_length][12:]) for x in range(num_lines)])
    DATA_FLAG = [str(spectra[9+x*block_length][11:]) for x in range(num_lines)]
    ix = np.ravel([i for i, x in enumerate(DATA_FLAG) if x != "JUNK"])
    
    # calculate laser power
    laser_power = np.zeros(num_lines)
    for ii in range(num_lines):
       # select the laser scan (LR0)
       x0 = 180+ii*block_length
       x1 = 1123+ii*block_length
       raw_scan = np.ravel([float(x) for x in spectra[x0:x1]])
       
       # select the ringdown scan (RD0)
       x0 = 17+ii*block_length
       x1 = 176+ii*block_length
       ringdown = np.ravel([float(x) for x in spectra[x0:x1]])
            
       # calculate laser power
       laser_power[ii] = np.mean(raw_scan[-11:-1]) - np.mean(ringdown[-11:-1])

    # write file
    outpath = fname.replace('s00','p00')
    
    df = pd.DataFrame({'SpectraID':SPECTRA_ID[ix],'LaserPower':laser_power[ix]})
    df = df.round({'LaserPower':5})
    df.to_csv(outpath,index=False)
    