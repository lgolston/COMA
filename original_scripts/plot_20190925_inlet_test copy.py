"""
read Dilution test
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import allantools

# read LGR
LGR = pd.read_csv('2019-09-25 Inlet_pressure\co_co2_2019-09-25_f0003.txt',skiprows = 2,sep=',')

LGR_spectraID = LGR.iloc[:,0]
LGR_tstamp = LGR.iloc[:,1]
LGR_H2O = LGR.iloc[:,2]
LGR_CO = LGR.iloc[:,4] * 1000
LGR_CO2 = LGR.iloc[:,8]
LGR_GasP = LGR.iloc[:,12]
LGR_GasT = LGR.iloc[:,14]
LGR_AmbT = LGR.iloc[:,16]
LGR_DetOff = LGR.iloc[:,28]
LGR_Gnd = LGR.iloc[:,30]
LGR_Peak0 = LGR.iloc[:,32]
LGR_OCS = LGR.iloc[:,46]
LGR_FitFlag = LGR.iloc[:,92]
LGR_time = [datetime.strptime(tstamp,"  %m/%d/%Y %H:%M:%S.%f") for tstamp in LGR_tstamp]
tmp = np.asarray(LGR_time) # can't directly index the datetime list


## plot overall time series
plt.figure(figsize=(15,10))
plt.subplot(411)
plt.plot(LGR_time,LGR_CO)
plt.ylim( 100, 350 )
plt.ylabel('CO, ppb')

plt.subplot(412)
plt.plot(LGR_time,LGR_CO2)
plt.ylim( 350, 600 )
plt.ylabel('CO2, ppm')

plt.subplot(413)
plt.plot(LGR_time,LGR_GasP)
plt.ylabel('Cell pressure, torr')
plt.ylim( 18, 20.2 )

plt.subplot(414)
plt.plot(LGR_time,LGR_GasT)
plt.ylabel('Cell temperature, °C')
plt.show()


## zoom in 13:30 to 14:50 for CO
x0 = datetime.strptime("2019-09-25 13:30:00","%Y-%m-%d %H:%M:%S")
x1 = datetime.strptime("2019-09-25 14:50:00","%Y-%m-%d %H:%M:%S")
ix = np.where([ (time_i >= x0 and time_i <= x1) for time_i in LGR_time])
ix = np.ravel(ix) # flatten array
plt.figure(figsize=(15,5))
plt.plot(tmp[ix],LGR_CO[ix],'b.',markersize=2)
plt.ylim(120, 140)
df = pd.DataFrame(LGR_CO[ix])
plt.plot(tmp[ix],df.rolling(10).mean(),'k')
plt.ylabel('CO, ppb')
plt.show()


## also zoom in for CO2
plt.figure(figsize=(15,5))
plt.plot(tmp[ix],LGR_CO2[ix],'b.',markersize=2)
plt.ylim(370, 390)
df = pd.DataFrame(LGR_CO2[ix])
plt.ylabel('CO2, ppm')
plt.grid(True)
plt.show()


## plot possible relationship with ground
plt.figure(figsize=(15,8)) # in inches
plt.subplot(211)
plt.plot(tmp[ix],LGR_CO[ix],'.')
plt.ylim( 120, 140 )
plt.ylabel('CO, ppb')
    
plt.subplot(212)
plt.plot(tmp[ix],LGR_Gnd[ix],'.')
plt.ylim(-0.21, -0.19)
plt.ylabel('Ground')
plt.show()


## Allan deviation plot
(t2, ad, ade, adn) = allantools.oadev(np.asarray(LGR_CO[ix]))
fig = plt.loglog(t2, ad)
plt.show()