"""
read Dilution test
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# read LGR
LGR = pd.read_csv('2019-09-26 Dilution\co_co2_2019-09-26_f0000.txt',skiprows = 2,sep=',')

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

## plot dilution series zoomed in
times  = [datetime.strptime("2019-09-26 10:59:00","%Y-%m-%d %H:%M:%S"), #1. 15 ppb
          datetime.strptime("2019-09-26 11:14:00","%Y-%m-%d %H:%M:%S"), #2. 25 ppb
          datetime.strptime("2019-09-26 11:28:00","%Y-%m-%d %H:%M:%S"), #3. 35 ppb
          datetime.strptime("2019-09-26 11:41:00","%Y-%m-%d %H:%M:%S"), #4. 45 ppb
          datetime.strptime("2019-09-26 11:53:00","%Y-%m-%d %H:%M:%S"), #5. 55 ppb
          datetime.strptime("2019-09-26 12:06:00","%Y-%m-%d %H:%M:%S"), #6. 65 ppb
          datetime.strptime("2019-09-26 12:18:00","%Y-%m-%d %H:%M:%S"), #7. 75 ppb
          datetime.strptime("2019-09-26 12:31:00","%Y-%m-%d %H:%M:%S"), #8. 85 ppb
          datetime.strptime("2019-09-26 12:53:00","%Y-%m-%d %H:%M:%S"), #9. 95 ppb
          datetime.strptime("2019-09-26 13:05:00","%Y-%m-%d %H:%M:%S"), #10. 105 ppb
          datetime.strptime("2019-09-26 13:17:00","%Y-%m-%d %H:%M:%S"), #11. 115 ppb
          datetime.strptime("2019-09-26 13:28:00","%Y-%m-%d %H:%M:%S")] #12. 125 ppb

tmp = np.asarray(LGR_time) # can't directly index the datetime list


values_CO = np.empty(0) # store all elements
values_CO_orig = np.empty(0) # store all elements
values_CO_mix = np.empty(0)
values_CO_mean = np.empty(0)
values_CO2 = np.empty(0)
values_Gnd = np.empty(0)

for ii in range(12):
    # get indices
    x0 = times[ii]
    ix = np.where([ (time_i >= x0 and
                          (time_i <= (x0 + timedelta(minutes = 10)))) for time_i in LGR_time])
    ix = np.ravel(ix) # flatten array
    
    # plot
    plt.figure(figsize=(8,5)) # in inches
    mean_CO = np.mean(LGR_CO[ix])
    plt.plot(tmp[ix],LGR_CO[ix],'b.')
    plt.plot([tmp[ix[0]], tmp[ix[-1]]],[mean_CO, mean_CO], 'k')
    plt.plot([tmp[ix[0]], tmp[ix[-1]]],[mean_CO-5, mean_CO-5], 'k:')
    plt.plot([tmp[ix[0]], tmp[ix[-1]]],[mean_CO+5, mean_CO+5], 'k:')
    plt.ylim( mean_CO - 10, mean_CO + 10 )
    plt.show()
    
    values_CO_mix = np.hstack( (values_CO_mix, np.ones(len(ix))*(10*ii+15) ) ) # from flow mix setup
    values_CO_orig = np.hstack((values_CO_orig,LGR_CO[ix]))
    values_CO = np.hstack((values_CO,LGR_CO[ix]-mean_CO)) # subtract mean each 10 min segment
    values_CO_mean = np.hstack( (values_CO_mean, mean_CO) )
    
    mean_CO2 = np.mean(LGR_CO2[ix]) # for 10 min segment
    values_CO2 = np.hstack((values_CO2,LGR_CO2[ix]-mean_CO2))
    values_Gnd = np.hstack((values_Gnd,LGR_Gnd[ix]))
    # old content
    # plt.xlim( x0, x0 + timedelta(minutes = 10))


## plot possible relationship with ground
plt.figure(figsize=(20,8)) # in inches
plt.subplot(311)
plt.plot(values_CO,'.')
for ii in range(13):
    plt.plot([ii*585, ii*585], [-8, 8],'k:')
plt.ylabel('CO, ppb')
    
plt.subplot(312)
plt.plot(values_Gnd,'.')
plt.ylabel('Ground')

plt.subplot(313)
plt.plot(values_CO2,'.')
plt.ylabel('CO2, ppm')
plt.show()


""" plot cell pressure
plt.figure()
plt.plot(LGR_time,LGR_GasP)
plt.xlim( datetime.strptime("2019-09-26 10:57:00","%Y-%m-%d %H:%M:%S"), 
          datetime.strptime("2019-09-26 13:50:00","%Y-%m-%d %H:%M:%S"))
plt.ylim( 19.95, 20.10 )
"""


## plot overall time series
plt.figure(figsize=(15,8))
plt.subplot(211)
plt.plot(LGR_time,LGR_CO)
plt.xlim( datetime.strptime("2019-09-26 10:57:00","%Y-%m-%d %H:%M:%S"), 
          datetime.strptime("2019-09-26 13:50:00","%Y-%m-%d %H:%M:%S"))
plt.ylim( 0, 150 )
plt.ylabel('CO, ppb')

plt.subplot(212)
plt.plot(LGR_time,LGR_CO2)
plt.xlim( datetime.strptime("2019-09-26 10:57:00","%Y-%m-%d %H:%M:%S"), 
          datetime.strptime("2019-09-26 13:50:00","%Y-%m-%d %H:%M:%S"))
plt.ylim( 0, 400 )
plt.ylabel('CO2, ppm')
plt.show()

## plot modeled vs measured concentration
plt.figure(figsize=(5,3.5),dpi=300)
plt.plot(values_CO_mix,values_CO_orig,'.')
plt.plot([10, 130],[10, 130],'k:')
plt.plot(np.linspace(15,125,num=12),values_CO_mean,'kx')
plt.xlabel('CO delivered, ppb')
plt.ylabel('CO observed, ppb')
plt.xlim((5,140))
plt.ylim((5,140))
plt.grid('on')
plt.show()

#plt.plot(values_CO_orig,values_CO_mix,'.')
#plt.plot([10, 130],[10, 130],'k:')
#plt.plot(values_CO_mean,np.linspace(15,125,num=12),'kx')
#plt.xlabel('CO observed, ppb')
#plt.ylabel('CO delivered, ppb')
#plt.show()


"""
plt.subplot(212)
plt.plot(LGR_time,LGR_OCS)
plt.xlim( datetime.strptime("2019-09-26 10:57:00","%Y-%m-%d %H:%M:%S"), 
          datetime.strptime("2019-09-26 13:50:00","%Y-%m-%d %H:%M:%S"))
plt.ylabel('OCS')
plt.show()
"""