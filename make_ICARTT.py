# -*- coding: utf-8 -*-
"""
Output data to archive format for NASA DAAC

Before adding to DAAC:
- apply calibration factor to CO, N2O
- verify format of ICARTT header
"""

# %% set up
# import libraries
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime
from load_flight_functions import read_COMA

# select file to export
case = '2022-08-06'

if case == '2022-08-02':
    filename_COMA = ['../Data/2022-08-02/n2o-co_2022-08-02_f0000.txt']
    output_name = 'COMA_WB57_20220802_R_alpha.ict'
    t0 = datetime(2022,8,2,1,10)
    t1 = datetime(2022,8,2,6,33)
elif case == '2022-08-04':
    filename_COMA = ['../Data/2022-08-04/n2o-co_2022-08-04_f0000.txt']
    output_name = 'COMA_WB57_20220804_R_alpha.ict'
    t0 = datetime(2022,8,4,1,12)
    t1 = datetime(2022,8,4,6,18)
elif case == '2022-08-06':
    filename_COMA = ['../Data/2022-08-06/n2o-co_2022-08-06_f0000.txt']
    output_name = 'COMA_WB57_20220806_R_alpha.ict'
    t0 = datetime(2022,8,6,1,0)
    t1 = datetime(2022,8,6,7,9)

# read COMA data
COMA = read_COMA(filename_COMA)

# filter to inlet air (valve 8), between takeoff (t0) and landing (t1)
ix_flight = np.ravel( np.where((COMA["      MIU_VALVE"]==8) & 
                               (COMA["time"]>t0) & 
                               (COMA["time"]<t1)) )

# %% output data
# convert timestamp to seconds after midnight
time_midnight = [(t.hour * 3600) + (t.minute * 60) + t.second + (t.microsecond / 1000000.0) for t in COMA['time']]
time_midnight = np.array(time_midnight)

# select mixing ratios to output
CO = COMA["      [CO]d_ppm"]*1000
N2O = COMA["     [N2O]d_ppm"]*1000
H2O = COMA["      [H2O]_ppm"]

# create DataFrame with desired variables
df = pd.DataFrame({'time': time_midnight[ix_flight],
                    'CO_ppbv': CO[ix_flight],
                    'N2O_ppbv': N2O[ix_flight], 
                    'H2O_ppmv': H2O[ix_flight]})

# loop that saves string formatted (commas, decimal places) data
# create new file; overwrites if needed
with open(output_name,"w") as ofile:
     fmt = '%.1f, %6.2f, %6.2f, %6.0f'
     np.savetxt(ofile, df.values, fmt=fmt)

# %% create file header
# refer to ICARTT 2.0 specifications for more details
header = '39,1001\n' # number of lines in header, file format index
header += 'Podolske, James\n' # PI name
header += 'NASA Ames Research Center\n' # PI affiliation
header += 'In-situ gas-phase CO/N2O Analyzer (Los Gatos Research)\n' # data source description
header += 'ACCLIP 2022\n' # mission name
header += '1,1\n' # file volume number, total number of file volumes
header += '2022, 08, 02, 2022, 08, 05\n' # date of data collection, date of most recent revision
header += '-1\n' # data interval code
header += 'Start_Time,Seconds after midnight\n' # name of independent variable, units of variable
header += '3\n' # number of dependent variables
header += '1,1,1\n' # scale factors of dependent variables
header += '-9999.00,-9999.00,-9999.00\n' # missing data flags of dependent variables
header += 'CO_ppbv, ppbv, CO dry air volume mixing ratio\n' # dependent variable short name, units, standard name
header += 'N2O_ppbv, ppmv, N2O2 dry air volume mixing ratio\n' # (repeat as necessary)
header += 'H2O_ppmv, ppmv, H2O volume mixing ratio\n' # (repeat as necessary)
header += '0\n' # number of special comment lines (not including this line)
header += '22\n' # number of normal comment lines (not including this line)
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
header += 'Time_Start,CO_ppbv,N2O_ppbv,H2O_ppmv\n'

# append the defined header to the already created data file
with open(output_name, 'r+') as f:
    content = f.read()
    f.seek(0, 0)
    f.write(header + content)        
