# -*- coding: utf-8 -*-
"""
Calculate linear calibration based on the cal cycles

TODO
- handle tank values from original NOAA tanks; and newer Matheson gas values
- output raw data from cal_fun and plot
- have results plot work across multiple days, colored before flight; in-flight; post-flight (or by altitude, gas temperature, etc. to check for dependencies)

Eventually
- delete cal_cycle_calculation and calculate_linear_cal_fun

"""

# %% load libraries and data
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib
import matplotlib.dates as mdates
from load_flight_functions import read_COMA, read_MMS
from functools import reduce
import matplotlib.cm as cm

# EDIT THESE


# %% data
# read COMA and MMS data
#COMA, inlet_ix = read_COMA(filename_COMA)
#MMS = read_MMS(filename_MMS)

import sys, os

root = "G:/My Drive/3_COMA/COMA/"
path = os.path.join(root, "../Data")

#plt.plot(COMA["      GasP_torr"])

for r, d, f in os.walk(path):
    for file in f:
        print(os.path.join(root, file))
