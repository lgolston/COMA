"""
read Dilution test
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from sklearn.linear_model import LinearRegression


# read LGR
LGR = pd.read_csv('2019-09-25 Inlet_pressure\co_co2_2019-09-25_f0003.txt',skiprows = 2,sep=',')
LGR_tstamp = LGR.iloc[:,1]
LGR_CO_day1 = LGR.iloc[:,4] * 1000
LGR_time1 = [datetime.strptime(tstamp,"  %m/%d/%Y %H:%M:%S.%f") for tstamp in LGR_tstamp]


LGR = pd.read_csv('2019-09-27 Standard gas\co_co2_2019-09-27_f0000.txt',skiprows = 2,sep=',')

LGR_spectraID = LGR.iloc[:,0]
LGR_tstamp = LGR.iloc[:,1]
LGR_H2O = LGR.iloc[:,2]
LGR_CO_day2 = LGR.iloc[:,4] * 1000
LGR_CO2 = LGR.iloc[:,8]
LGR_GasP = LGR.iloc[:,12]
LGR_GasT = LGR.iloc[:,14]
LGR_AmbT = LGR.iloc[:,16]
LGR_DetOff = LGR.iloc[:,28]
LGR_Gnd = LGR.iloc[:,30]
LGR_Peak0 = LGR.iloc[:,32]
LGR_OCS = LGR.iloc[:,46]
LGR_FitFlag = LGR.iloc[:,92]
LGR_time2 = [datetime.strptime(tstamp,"  %m/%d/%Y %H:%M:%S.%f") for tstamp in LGR_tstamp]

# get indices
#x0 = times[ii]
#ix = np.where([ (time_i >= x0 and
#                (time_i <= (x0 + timedelta(minutes = 10)))) for time_i in LGR_time])
#ix = np.ravel(ix) # flatten array
    

## plot specific time series
x0 = datetime.strptime("2019-09-27 12:00:00","%Y-%m-%d %H:%M:%S")
x1 = datetime.strptime("2019-09-27 16:15:00","%Y-%m-%d %H:%M:%S")


plt.figure(figsize=(15,10))
plt.subplot(411)
plt.plot(LGR_time2,LGR_CO_day2,'b.')
df = pd.DataFrame(LGR_CO_day2)
meanCO = df.rolling(10).mean()
plt.plot(LGR_time2,meanCO,'k')
plt.ylim( 115, 145 )
plt.xlim( x0, x1)
plt.ylabel('CO, ppb')
plt.title("2019-09-27")

plt.subplot(412)
plt.plot(LGR_time2,LGR_Gnd,'b.')
df = pd.DataFrame(LGR_Gnd)
meanGnd = df.rolling(10).mean()
plt.plot(LGR_time2,meanGnd,'k')
plt.ylim( -0.202, -0.198 )
plt.xlim( x0, x1 )
plt.ylabel('Ground, V')

plt.subplot(413)
plt.plot(LGR_time2,LGR_GasT,'b.')
plt.xlim( x0, x1 )
plt.ylabel('Cell temperature, deg C')

plt.subplot(414)
plt.plot(LGR_time2,LGR_GasP,'b.')
plt.xlim( x0, x1 )
plt.ylim( 19.95, 20.06 )
plt.ylabel('Cell pressure, torr')
plt.show()


## plot time series from the two days
plt.figure(figsize=(15,10))

df = pd.DataFrame(LGR_CO_day1)
meanCO1 = df.rolling(10).mean()
df = pd.DataFrame(LGR_CO_day2)
meanCO2 = df.rolling(10).mean()

plt.subplot(311)
x0 = datetime.strptime("2019-09-25 13:30:00","%Y-%m-%d %H:%M:%S")
x1 = datetime.strptime("2019-09-25 15:15:00","%Y-%m-%d %H:%M:%S")
plt.plot(LGR_time1,LGR_CO_day1,'b.')
plt.plot(LGR_time1,meanCO1,'k')
plt.xlim(x0, x1)
plt.ylim(120, 140)
plt.text(datetime.strptime("2019-09-25 15:06:00","%Y-%m-%d %H:%M:%S"),
         138,
         "2019-09-25",weight = "bold")
#plt.title("2019-09-25")
plt.ylabel('CO, ppb')

# 105 minutes
plt.subplot(312)
x0 = datetime.strptime("2019-09-27 12:30:00","%Y-%m-%d %H:%M:%S")
x1 = datetime.strptime("2019-09-27 14:15:00","%Y-%m-%d %H:%M:%S")
plt.plot(LGR_time2,LGR_CO_day2,'b.')
plt.plot(LGR_time2,meanCO2,'k')
plt.xlim(x0, x1)
plt.ylim(120, 140)
plt.text(datetime.strptime("2019-09-27 14:01:00","%Y-%m-%d %H:%M:%S"),
         138,
         "2019-09-27 part 1",weight = "bold")
#plt.title("2019-09-27 part 1")
plt.ylabel('CO, ppb')

plt.subplot(313)
x0 = datetime.strptime("2019-09-27 14:15:00","%Y-%m-%d %H:%M:%S")
x1 = datetime.strptime("2019-09-27 16:00:00","%Y-%m-%d %H:%M:%S")
plt.plot(LGR_time2,LGR_CO_day2,'b.')
plt.plot(LGR_time2,meanCO2,'k')
plt.xlim(x0, x1)
plt.ylim(120, 140)
plt.text(datetime.strptime("2019-09-27 15:46:00","%Y-%m-%d %H:%M:%S"),
         138,
         "2019-09-27 part 2",weight = "bold")
#plt.title("2019-09-27 part 2")
plt.ylabel('CO, ppb')