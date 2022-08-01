# -*- coding: utf-8 -*-
"""
output data to archive format for NASA DAAC
"""

# %% header
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta

filename_COMA = '../Data/2022-05-20/n2o-co_2022-05-20_f0000.txt'
output_name = 'COMA_WB57_20220520_R0.ict'

# %% data
# read COMA data
LGR = pd.read_csv(filename_COMA,sep=',',header=1)

LGR_time = LGR["                     Time"]
LGR_time = [datetime.strptime(tstamp,"  %m/%d/%Y %H:%M:%S.%f") for tstamp in LGR_time]
LGR_time = pd.DataFrame(LGR_time)
LGR_time = LGR_time[0]

# %% open file and create header
# example:
#40375.647, 40376.593, 40376.120,  73.80,408.74,21165.63


# %% output data
CO = LGR["      [CO]d_ppm"]*1000
N2O = LGR["     [N2O]d_ppm"]*1000
H2O = LGR["      [H2O]_ppm"]

df = pd.DataFrame({'time': LGR_time,
                    'CO_ppbv': CO,
                    'N2O_ppbv': N2O, 
                    'H2O_ppmv': H2O})

df.to_csv(output_name,index=False,header='test')

# %% add header
header = '43,1001\n'
header += 'Podolske, James\n'
header += 'NASA Ames Research Center\n'
header += 'In-situ gas-phase CO/N2O Analyzer (Los Gatos Research)\n'
header += 'ACCLIP 2021 Test Flights\n'
header += '1,1\n'
header += '2017, 08, 21, 2019, 08, 12\n'
header += '0\n'
header += 'Start_UTC,Seconds after midnight\n'
header += '5\n'
header += '1,1,1,1,1\n'
header += '-9999.00,-9999.00,-9999.00,-9999.00,-9999.00\n'
header += 'End_UTC, seconds\n'
header += 'Mid_UTC, seconds\n'
header += 'CO_ppbv, ppbv, CO dry air volume mixing ratio\n'
header += 'N2O_ppmv, ppmv, N2O2 dry air volume mixing ratio\n'
header += 'H2O_ppmv, ppmv, H2O volume mixing ratio\n'
header += '0\n'
header += '24\n'
header += '******************************************************************************************************************\n'
header += 'NASA Ames Trace Gas Data (2017 ORACLES) field campaign\n'
header += '\n'
header += 'PI_CONTACT_INFO: James.R.Podolske@nasa.gov\n'
header += 'PLATFORM: NASA WB-57 aircraft\n'
header += 'LOCATION: Data in Housekeeping files for associated flight\n'
header += 'ASSOCIATED_DATA: N/A\n'
header += 'INSTRUMENT_INFO: ABB/Los Gatos Research CO/N2O/H2O Analyzer\n'
header += 'DATA_INFO: None\n'
header += 'UNCERTAINTY: all data are 1%\n'
header += 'ULOD_FLAG: -7777\n'
header += 'ULOD_VALUE: N/A\n'
header += 'LLOD_FLAG: -8888\n'
header += 'LLOD_VALUE: 50 ppmv for H2O\n'
header += 'DM_CONTACT_INFO: James Podolske (James.R.Podolske@nasa.gov) and Levi Golston (levi.m.golston@nasa.gov)\n'
header += 'PROJECT_INFO: ACCLIP 2017\n'
header += 'STIPULATIONS_ON_USE: This is the initial public release of the ACCLIP 2021 data set. We strongly recommend that you consult the PI, both for updates to the data set, and for the proper and most recent interpretation of the data for specific science use.\n'
header += 'OTHER_COMMENTS: none\n'
header += 'REVISION: R0\n'
header += 'R0: preliminary field data, subject to corrections due to calibrations, time lags, and future analysis results\n'
header += '******************************************************************************************************************\n'

with open(output_name, 'r+') as f:
    content = f.read()
    f.seek(0, 0)
    f.write(header + content)        
