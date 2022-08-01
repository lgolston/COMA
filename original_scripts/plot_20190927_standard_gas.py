"""
read standard gas test
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from sklearn.linear_model import LinearRegression
from scipy.signal import detrend

# read LGR
LGR = pd.read_csv('2019-09-27 Standard gas\co_co2_2019-09-27_f0000.txt',skiprows = 2,sep=',')

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


""" plot cell pressure
plt.figure()
plt.plot(LGR_time,LGR_GasP)
#plt.ylim( 19.95, 20.10 )
"""


## plot overall time series
plt.figure(figsize=(15,8))
plt.subplot(211)
plt.plot(LGR_time,LGR_CO,'b.')
plt.ylim( 100, 200 )
plt.ylabel('CO, ppb')

plt.subplot(212)
plt.plot(LGR_time,LGR_CO2,'b.')
plt.ylim( 370, 500 )
plt.ylabel('CO2, ppm')
plt.show()


## plot specific time series
x0 = datetime.strptime("2019-09-27 12:05:00","%Y-%m-%d %H:%M:%S")
x1 = datetime.strptime("2019-09-27 16:15:00","%Y-%m-%d %H:%M:%S")


plt.figure(figsize=(15,8))
plt.subplot(311)
plt.plot(LGR_time,LGR_CO,'b.')
df = pd.DataFrame(LGR_CO)
meanCO = df.rolling(10).mean()
plt.plot(LGR_time,meanCO,'k')
plt.ylim( 115, 145 )
plt.xlim( x0, x1)
plt.ylabel('CO, ppb')

plt.subplot(312)
plt.plot(LGR_time,LGR_CO2,'b.')
df = pd.DataFrame(LGR_CO2)
meanCO2 = df.rolling(10).mean()
plt.plot(LGR_time,meanCO2,'k')
plt.ylim( 375, 395 )
plt.xlim( x0, x1)
plt.ylabel('CO2, ppm')

plt.subplot(313)
plt.plot(LGR_time,LGR_Gnd,'b.')
df = pd.DataFrame(LGR_Gnd)
meanGnd = df.rolling(10).mean()
plt.plot(LGR_time,meanGnd,'k')
plt.ylim( -0.202, -0.198 )
plt.xlim( x0, x1 )
plt.ylabel('Ground, V')
plt.show()


## regression between Gnd and CO
x0 = datetime.strptime("2019-09-27 12:25:00","%Y-%m-%d %H:%M:%S")
x1 = datetime.strptime("2019-09-27 16:02:00","%Y-%m-%d %H:%M:%S")

tmp = np.asarray(LGR_time) # can't directly index the datetime list
ix = np.where([ (time_i >= x0 and time_i <= x1) for time_i in LGR_time])
ix = np.ravel(ix) # flatten array

#x = np.asarray(LGR_Gnd[ix]).reshape((-1,1))
#y = np.asarray(LGR_CO[ix])
x = np.asarray(meanGnd)[ix].reshape((-1,1))
y = np.asarray(meanCO)[ix]
model = LinearRegression()
model.fit(x,y)
x_0 = -0.2015
x_1 = -0.1985
y_0 = model.coef_[0]*x_0 + model.intercept_
y_1 = model.coef_[0]*x_1 + model.intercept_

plt.figure(figsize=(10,8))
#plt.plot(LGR_Gnd[ix],LGR_CO[ix],'.')
plt.plot(x,y,'.')
plt.plot([x_0, x_1],[y_0,y_1])
print('coefficient of determination:', model.score(x, y))
plt.xlabel('Ground, V')
plt.ylabel('CO, ppb')
plt.text(-0.2015,134,"R^2 = 0.82")
plt.show()


"""
plt.figure(figsize=(15,8))
plt.subplot(211)
plt.plot(LGR_time,LGR_GasT,'b.')
plt.xlim( datetime.strptime("2019-09-27 12:05:00","%Y-%m-%d %H:%M:%S"), 
          datetime.strptime("2019-09-27 16:15:00","%Y-%m-%d %H:%M:%S"))
plt.ylabel('Cell temperature, deg C')

plt.figure(figsize=(15,8))
plt.subplot(212)
plt.plot(LGR_time,LGR_GasP,'b.')
plt.ylim( 19.95, 20.06 )
plt.xlim( datetime.strptime("2019-09-27 12:05:00","%Y-%m-%d %H:%M:%S"), 
          datetime.strptime("2019-09-27 16:15:00","%Y-%m-%d %H:%M:%S"))
plt.ylabel('Cell pressure, torr')
"""


"""
plt.plot(LGR_time,LGR_OCS)
plt.ylabel('OCS')
plt.show()
"""

## Allan deviation plot
import allantools

t1 = np.linspace(start=1,stop=59,num=59) # by second
t2 = np.linspace(start=60,stop=3600,num=60) # then by minute
t = np.hstack((t1,t2))
(t2, ad, ade, adn) = allantools.oadev(np.asarray(LGR_CO[ix]),data_type="freq",taus=t)

fig = plt.loglog(t2, ad,'m')
plt.xlabel('Integration time, s')
plt.ylabel('Allan deviation, ppb')
plt.grid(b=True, which='both')
plt.ylim((0.4,2))
plt.tight_layout()
plt.savefig('output.png', dpi=300)
plt.show()

print("Min: " + "{:.3f}".format(ad[0]) + " ppb at: 1 s" )
print("Min: " + "{:.3f}".format(ad[9]) + " ppb at: 10 s" )
print("Min: " + "{:.3f}".format(min(ad)) + " ppb at: " + str(t[np.argmin(ad)]) )


## zoom in on 20-min segment
x0 = datetime.strptime("2019-09-27 12:25:00","%Y-%m-%d %H:%M:%S")
x1 = datetime.strptime("2019-09-27 12:45:04","%Y-%m-%d %H:%M:%S") # make length divisible by 10
tmp = np.asarray(LGR_time) # can't directly index the datetime list
ix = np.where([ (time_i >= x0 and time_i <= x1) for time_i in LGR_time])
ix = np.ravel(ix) # flatten array

plt.figure(figsize=(10,6))
plt.plot(tmp[ix],LGR_CO[ix],'b.')
df = pd.DataFrame(LGR_CO[ix])
meanCO = df.rolling(10).mean()
plt.plot(tmp[ix],meanCO,'k')
plt.ylim( 115, 145 )
plt.ylabel('CO, ppb')
plt.show()

resampled = np.mean(np.reshape(np.ravel(LGR_CO[ix]),(127,10)),axis=1) # average every 10 samples

(t2, ad, ade, adn) = allantools.oadev(np.asarray(LGR_CO[ix]),data_type="freq",taus=t)
print("Min: " + "{:.3f}".format(ad[0]) + " ppb at: 1 s" )
print("Min: " + "{:.3f}".format(ad[9]) + " ppb at: 10 s" )

print("Std: " + "{:.3f}".format(np.std(LGR_CO[ix])))
print("Std: " + "{:.3f}".format( np.std(detrend(LGR_CO[ix]))) ) # std with linear detrend

print("Std: " + "{:.3f}".format(np.std(resampled)))
print("Std: " + "{:.3f}".format( np.std(detrend(resampled))) ) # std with linear detrend, 10 s mean

print("{:.3f}".format(np.percentile(LGR_CO[ix],0.3)))
print("{:.3f}".format(np.percentile(LGR_CO[ix],5)))
print("{:.3f}".format(np.percentile(LGR_CO[ix],25)))
print("{:.3f}".format(np.percentile(LGR_CO[ix],50)))
print("{:.3f}".format(np.percentile(LGR_CO[ix],75)))
print("{:.3f}".format(np.percentile(LGR_CO[ix],95)))
print("{:.3f}".format(np.percentile(LGR_CO[ix],99.7)))