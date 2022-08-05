# -*- coding: utf-8 -*-
"""
Output data to archive format for NASA DAAC
"""

# %% header
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime
from load_flight_functions import read_COMA

filename_COMA = ['../Data/2022-08-02/n2o-co_2022-08-02_f0000.txt']
output_name = 'COMA_WB57_20220802_R_alpha.ict'
t0 = datetime(2022,8,2,1,10)
t1 = datetime(2022,8,2,6,33)

#filename_COMA = ['../Data/2022-08-04/n2o-co_2022-08-04_f0000.txt']
#output_name = 'COMA_WB57_20220804_R_alpha.ict'
#t0 = datetime(2022,8,4,1,12)
#t1 = datetime(2022,8,4,6,18)

# read COMA data
COMA = read_COMA(filename_COMA)
ix_flight = np.ravel( np.where((COMA["      MIU_VALVE"]==8) & 
                               (COMA["time"]>t0) & 
                               (COMA["time"]<t1)) )

# %% output data
time_midnight = [(t.hour * 3600) + (t.minute * 60) + t.second + (t.microsecond / 1000000.0) for t in COMA['time']]
time_midnight = np.array(time_midnight)

CO = COMA["      [CO]d_ppm"]*1000
N2O = COMA["     [N2O]d_ppm"]*1000
H2O = COMA["      [H2O]_ppm"]

# filter between takeoff and landing
ix_8 = np.ravel(np.where(COMA["      MIU_VALVE"]==8)) # inlet

df = pd.DataFrame({'time': time_midnight[ix_flight],
                    'CO_ppbv': CO[ix_flight],
                    'N2O_ppbv': N2O[ix_flight], 
                    'H2O_ppmv': H2O[ix_flight]})

with open(output_name,"w") as ofile:
     fmt = '%.1f, %6.2f, %6.2f, %6.0f'
     np.savetxt(ofile, df.values, fmt=fmt)

# %% add header
header = '39,1001\n'
header += 'Podolske, James\n'
header += 'NASA Ames Research Center\n'
header += 'In-situ gas-phase CO/N2O Analyzer (Los Gatos Research)\n'
header += 'ACCLIP 2022\n'
header += '1,1\n'
header += '2022, 08, 02, 2022, 08, 05\n'
header += '-1\n'
header += 'Start_Time,Seconds after midnight\n'
header += '3\n'
header += '1,1,1\n'
header += '-9999.00,-9999.00,-9999.00\n'
header += 'CO_ppbv, ppbv, CO dry air volume mixing ratio\n'
header += 'N2O_ppmv, ppmv, N2O2 dry air volume mixing ratio\n'
header += 'H2O_ppmv, ppmv, H2O volume mixing ratio\n'
header += '0\n'
header += '24\n'
header += '******************************************************************************************************************\n'
header += 'NASA Ames Trace Gas Data (2022 ACCLIP) field campaign\n'
header += '\n'
header += 'PI_CONTACT_INFO: James.R.Podolske@nasa.gov\n'
header += 'PLATFORM: NASA WB-57 aircraft\n'
header += 'LOCATION: Data in Housekeeping files for associated flight\n'
header += 'ASSOCIATED_DATA: N/A\n'
header += 'INSTRUMENT_INFO: ABB/Los Gatos Research CO/N2O/H2O Analyzer\n'
header += 'DATA_INFO: None\n'
header += 'UNCERTAINTY: to be specified in RA release\n'
header += 'ULOD_FLAG: -7777\n'
header += 'ULOD_VALUE: N/A\n'
header += 'LLOD_FLAG: -8888\n'
header += 'LLOD_VALUE: 50 ppmv for H2O\n'
header += 'DM_CONTACT_INFO: James Podolske (James.R.Podolske@nasa.gov) and Levi Golston (levi.m.golston@nasa.gov)\n'
header += 'PROJECT_INFO: ACCLIP 2022\n'
header += 'STIPULATIONS_ON_USE: This is a pre-release of the ACCLIP 2022 data set. We strongly recommend that you consult the PI, both for updates to the data set, and for the proper and most recent interpretation of the data for specific science use.\n'
header += 'OTHER_COMMENTS: none\n'
header += 'REVISION: R_alpha\n'
header += 'R0: preliminary field data, subject to corrections due to calibrations, time lags, and future analysis results\n'
header += '******************************************************************************************************************\n'
header += 'Time_Start,CO_ppbv,N2O_ppmv,H2O_ppmv\n'

with open(output_name, 'r+') as f:
    content = f.read()
    f.seek(0, 0)
    f.write(header + content)        
