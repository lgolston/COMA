# -*- coding: utf-8 -*-
"""
List 2022 files

"""

# %% load libraries and data
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from load_data_functions import read_COMA, read_MMS_ict
import os
import re

# %% read all COMA data
# walk through directory
root = "G:/My Drive/3_COMA/Data/"

for r, d, f in os.walk(root):
    for file in f:
        #m = re.search("f(.*).txt$", file)
        m = re.search("2022(.*)f.{4}.txt$", file)
        
        # read data
        if bool(m):
            filename_COMA = os.path.join(r, file)
            print(filename_COMA)
        
            #COMA, inlet_ix = read_COMA(filename_COMA)

# %% read all MMS data    
#MMS = read_MMS(filename_MMS)

# %% process
# sync the data (outer sync)
