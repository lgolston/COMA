# -*- coding: utf-8 -*-
"""
plot netcdf (2D) data
"""

# %% header
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import netCDF4 as nc4

# %% select data
case = 2

if case == 1: # Test Flight 1
    filename_GEOS_nc = '../Data/_OtherData_/GEOSFP_CO_ACCLIP-20210810.nc'
    filename_GEOS_txt = '../Data/_OtherData_/GEOSFP_CO_ACCLIP-20210810.txt'
    cur_day = datetime(2021,8,10)
elif case == 2: # Test Flight 2
    filename_GEOS_nc = '../Data/_OtherData_/GEOSFP_CO_ACCLIP-20210816.nc'
    filename_GEOS_txt = '../Data/_OtherData_/GEOSFP_CO_ACCLIP-20210816.txt'
    cur_day = datetime(2021,8,16)
elif case == 3: # Test Flight 3
    filename_GEOS_nc = '../Data/_OtherData_/GEOSFP_CO_ACCLIP-20210817.nc'
    filename_GEOS_txt = '../Data/_OtherData_/GEOSFP_CO_ACCLIP-20210817.txt'
    cur_day = datetime(2021,8,17)

# %% load data
# netcdf file (2D)
GEOS_nc = nc4.Dataset(filename_GEOS_nc,'r')

GEOS_nc_CO = GEOS_nc.variables['GEOS_CO'][:] # (lev,time)
GEOS_nc_lon = GEOS_nc.variables['lon'][:]
GEOS_nc_lat = GEOS_nc.variables['lat'][:]
GEOS_nc_lev = GEOS_nc.variables['lev'][:]
GEOS_nc_time = [cur_day + timedelta(seconds=float(tmp)) for tmp in GEOS_nc.variables['time'][:]]

# txt file (subsetted along flight track)
GEOS_txt = pd.read_csv(filename_GEOS_txt,sep='\s+',header=0)
GEOS_txt_time = [cur_day + timedelta(seconds=tmp) for tmp in GEOS_txt['Time(UTC_Sec)']]

# %% plot time vs pressure level; CO colorbar
fig, ax = plt.subplots(1, 1, figsize=(6,5))

im = plt.pcolormesh(GEOS_nc_time,GEOS_nc_lev,GEOS_nc_CO,vmax=150)
plt.plot(GEOS_txt_time,GEOS_txt['Pressure(hPa)'],'k')

ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.xlabel('Time')
ax0 = plt.gca()
ax0.invert_yaxis()
plt.ylabel('Pressure, hPa')
cbar = fig.colorbar(im,ax=ax0)
cbar.set_label('CO, ppb')
plt.tight_layout()
#plt.savefig('fig_output.png',dpi=200)