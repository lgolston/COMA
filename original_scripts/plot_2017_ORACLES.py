"""
read Dilution test
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import allantools

# read LGR
LGR = pd.read_csv('2017-08-24 ORACLES\co_co2_2017-08-24_f0001.txt',skiprows = 2,sep=',')

LGR_tstamp = LGR.iloc[:,0]
LGR_H2O = LGR.iloc[:,1]
LGR_CO = LGR.iloc[:,3] * 1000
LGR_CO2 = LGR.iloc[:,7]
LGR_GasP = LGR.iloc[:,11]
LGR_GasT = LGR.iloc[:,13]
LGR_AmbT = LGR.iloc[:,15]
LGR_DetOff = LGR.iloc[:,27]
LGR_time = [datetime.strptime(tstamp,"  %m/%d/%Y %H:%M:%S.%f") for tstamp in LGR_tstamp]


# get indices
#x0 = times[ii]
#ix = np.where([ (time_i >= x0 and
#                (time_i <= (x0 + timedelta(minutes = 10)))) for time_i in LGR_time])
#ix = np.ravel(ix) # flatten array
    


""" plot cell pressure
plt.figure()
plt.plot(LGR_time,LGR_GasP)
#plt.ylim( 19.95, 20.10 )
"""


## plot overall time series
plt.figure(figsize=(15,8))
plt.subplot(211)
plt.plot(LGR_time,LGR_CO,'b.')
#plt.ylim( 50, 500 )
plt.xlim( datetime.strptime("2017-08-24 08:30:00","%Y-%m-%d %H:%M:%S"), 
          datetime.strptime("2017-08-24 11:00:00","%Y-%m-%d %H:%M:%S"))
plt.ylim(70, 160)
plt.ylabel('CO, ppb')

plt.subplot(212)
plt.plot(LGR_time,LGR_CO2,'b.')
#plt.ylim( 370, 500 )
plt.xlim( datetime.strptime("2017-08-24 08:30:00","%Y-%m-%d %H:%M:%S"), 
          datetime.strptime("2017-08-24 11:00:00","%Y-%m-%d %H:%M:%S"))
plt.ylim(420, 480)
plt.ylabel('CO2, ppm')
plt.show()


"""
plt.figure(figsize=(15,8))
plt.subplot(211)
plt.plot(LGR_time,LGR_GasT,'b.')
plt.xlim( datetime.strptime("2019-09-27 12:05:00","%Y-%m-%d %H:%M:%S"), 
          datetime.strptime("2019-09-27 16:15:00","%Y-%m-%d %H:%M:%S"))
plt.ylabel('Cell temperature, deg C')
"""


"""
plt.plot(LGR_time,LGR_OCS)
plt.ylabel('OCS')
plt.show()
"""