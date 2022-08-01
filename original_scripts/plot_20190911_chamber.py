"""
read Dilution test
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import allantools

# read LGR
LGR = pd.read_csv('2019-09-11 Chamber2\co_co2_2019-09-11_f0000_noPGP.txt',skiprows = 2,sep=',')

LGR_spectraID = LGR.iloc[:,0]
LGR_tstamp = LGR.iloc[:,1]
LGR_H2O = LGR.iloc[:,2]
LGR_CO = LGR.iloc[:,4] * 1000
LGR_CO2 = LGR.iloc[:,8]
LGR_GasP = LGR.iloc[:,12]
LGR_GasT = LGR.iloc[:,14]
LGR_AmbT = LGR.iloc[:,16]
LGR_LTC0 = LGR.iloc[:,20]
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
plt.plot(LGR_time,LGR_DetOff)
plt.ylabel('Detector offset')

#plt.subplot(413)
#plt.plot(LGR_time,LGR_GasP)
#plt.ylabel('Cell pressure, torr')
#plt.ylim( 18, 20.2 )

plt.subplot(414)
plt.plot(LGR_time,LGR_GasT)
plt.ylabel('Cell temperature, °C')
plt.show()


## plot Gnd
x0 = datetime.strptime("2019-09-11 12:00:00","%Y-%m-%d %H:%M:%S")
x1 = datetime.strptime("2019-09-11 12:45:00","%Y-%m-%d %H:%M:%S")

fig, ax1 = plt.subplots(figsize=(15, 10))
ax1.plot(LGR_time,LGR_CO,'b.')
ax1.set_ylim(100,150)

ax2 = ax1.twinx()

ax2.plot(LGR_time,LGR_Gnd,'k.')
ax2.set_xlim(x0,x1)
ax2.set_ylim(-0.22,-0.19)