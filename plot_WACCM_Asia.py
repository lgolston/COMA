# -*- coding: utf-8 -*-
"""
Downloaded data from
https://www.acom.ucar.edu/waccm/download.shtml, or
https://rda.ucar.edu/datasets/ds313.6/index.html#!cgi-bin/datasets/getSubset?dsnum=313.6&listAction=customize&_da=y&gindex=32021

TODO
1. Add range ring
https://stackoverflow.com/questions/52105543/drawing-circles-with-cartopy-in-orthographic-projection
https://arm-doe.github.io/pyart/source/auto_examples/plotting/plot_ppi_with_rings.html
2. Potential vorticity
3. Potential T
4. Altitude axis in km
5. Airplane profile
"""

# %% header
from scipy.io import netcdf_file as nc
import matplotlib.pyplot as plt

# %% load data
filename = '../Data/_OtherData_/WACCM_88/543020.CO.f.e22.beta02.FWSD.f09_f09_mg17.cesm2_2_beta02.forecast.001.cam.h3.2021-08-10-00000.nc'

tmp = nc(filename)
CO = tmp.variables['CO']
CO.dimensions #('time', 'lev', 'lat', 'lon')
CO.shape # (4, 88, 74, 71)

lon = tmp.variables['lon'].data
lat = tmp.variables['lat'].data
lev = tmp.variables['lev'].data

# %% plot map
import cartopy.crs as crs
import cartopy.feature as cfeature

fig1 = plt.figure(figsize=(8,6),dpi=100)

ax = fig1.add_subplot(1,1,1, projection=crs.PlateCarree())

ax.add_feature(cfeature.COASTLINE)

#cb = ax.pcolorfast(lon,lat,CO.data[1,87]) # 87 = near surface
cb = ax.pcolorfast(lon,lat,CO.data[1,56]) # 56 = 163 Pa
fig1.colorbar(cb, ax=ax)

ax.plot(lon[10],lat[40],'kx')
ax.plot(lon[40],lat[40],'kx')
ax.plot(lon[60],lat[40],'kx')

# %% plot vertical profile
fig2 = plt.figure()
plt.plot(CO.data[0,25:88,40,10],lev[25:88],'b-.')
plt.plot(CO.data[0,25:88,40,40],lev[25:88],'k-.')
plt.plot(CO.data[0,25:88,40,60],lev[25:88],'-.')
plt.gca().invert_yaxis()