# -*- coding: utf-8 -*-
"""
Figure
"""

# header
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.dates as mdates
from load_flight_functions import read_COMA
from load_flight_functions import read_MMS

# read data
#COMA, inlet_ix= read_COMA(filename_COMA)

# create figure
#fig, ax = plt.subplots(3, 4, figsize=(9,3.5),dpi=200,sharex=True)