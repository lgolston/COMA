# -*- coding: utf-8 -*-
"""
plot calibration cycles
was in the process of moving parts of code into calculate_linear_cal_fun

"""

# %% EDIT THESE
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.dates as mdates

case = 3

if case == 0: # FCF
    filename_COMA = '../Data/2021-08-06/n2o-co_2021-08-06_f0002.txt'
elif case == 1: # Test Flight 1
    filename_COMA = '../Data/2021-08-10/n2o-co_2021-08-10_f0003.txt'
elif case == 2: # Test Flight 2
    filename_COMA = '../Data/2021-08-16/n2o-co_2021-08-16_f0002.txt'
elif case == 3: # Test Flight 3
    filename_COMA = '../Data/2021-08-17/n2o-co_2021-08-17_f0002.txt'
elif case == 4: # lab breathing air
    filename_COMA = '../Data/2021-08-06/n2o-co_2021-08-06_f0000.txt' # chop 3am part
elif case == 5:
    filename_COMA = '../Data/2021-08-10/n2o-co_2021-08-10_f0000.txt'
elif case == 6:
    filename_COMA = '../Data/2021-08-16/n2o-co_2021-08-16_f0000.txt'
elif case == 7:
    filename_COMA = '../Data/2021-08-17/n2o-co_2021-08-17_f0000.txt'
elif case == 8: # cal gases
    filename_COMA = '../Data/2022-04-22/n2o-co_2022-04-22_f0000.txt'
elif case == 9: # EEL Day 2
    filename_COMA = '../Data/2022-05-20/n2o-co_2022-05-20_f0000_cut_timechange.txt'
else:
    print('not a valid case')

# %% data
# read COMA data
LGR = pd.read_csv(filename_COMA,sep=',',header=1)

LGR_time = LGR["                     Time"]
LGR_time = [datetime.strptime(tstamp,"  %m/%d/%Y %H:%M:%S.%f") for tstamp in LGR_time]
LGR_time = pd.DataFrame(LGR_time)
LGR_time=LGR_time[0]

# index MIU valves
#ix_8 = np.ravel(np.where( (LGR["      MIU_VALVE"]==8) & (LGR["      GasP_torr"]>52.45) & (LGR["      GasP_torr"]<52.65)) ) # Inlet
ix_8 = np.ravel(np.where(LGR["      MIU_VALVE"]==8)) # inlet
ix_7 = np.ravel(np.where(LGR["      MIU_VALVE"]==7)) # inlet (lab)
ix_3 = np.ravel(np.where(LGR["      MIU_VALVE"]==3)) # high cal
ix_2 = np.ravel(np.where(LGR["      MIU_VALVE"]==2)) # low cal
ix_1 = np.ravel(np.where(LGR["      MIU_VALVE"]==1)) # flush

# %% plot calibration data
plt.rc('axes', labelsize=6) # xaxis and yaxis labels
plt.rc('xtick', labelsize=6) # xtick labels
plt.rc('ytick', labelsize=6) # ytick labels

# each cycle only takes a fixed amount of time
# therefore robust method is to check for large jumps in time (here > 5s) between occurences

fig, ax = plt.subplots(1, 4, figsize=(8,2.5),dpi=200)

df_lowcal = pd.DataFrame({'time': LGR_time[ix_2], 'CO_dry': LGR["      [CO]d_ppm"][ix_2]*1000, 'N2O_dry': LGR["     [N2O]d_ppm"][ix_2]*1000})
df_lowcal['groups'] = (df_lowcal.index.to_series().diff()>5).cumsum()
df_highcal = pd.DataFrame({'time': LGR_time[ix_3], 'CO_dry': LGR["      [CO]d_ppm"][ix_3]*1000, 'N2O_dry': LGR["     [N2O]d_ppm"][ix_3]*1000})
df_highcal['groups'] = (df_highcal.index.to_series().diff()>5).cumsum()
#df_flush = pd.DataFrame({'time': LGR_time[ix_1], 'CO_dry': LGR["      [CO]d_ppm"][ix_1]*1000})
#df_flush['groups'] = (df_flush.index.to_series().diff()>5).cumsum()

# function to calculate the average and standard deviation at end of cal cycle
def calc_mean(gas_vals):
    rolling_mean = gas_vals.rolling(10).mean()
    rolling_std = gas_vals.rolling(10).std()
    mean_val = rolling_mean.iloc[-1] # last value
    std_val = rolling_std.iloc[-1]  # last value
    return mean_val, std_val

low_CO_mean = np.zeros(20)
low_CO_std = np.zeros(20)
high_CO_mean = np.zeros(20)
high_CO_std = np.zeros(20)
low_N2O_mean = np.zeros(20)
low_N2O_std = np.zeros(20)
high_N2O_mean = np.zeros(20)
high_N2O_std = np.zeros(20)

CO_slope = [1.07804824, 1.0712675 , 1.06404031, 1.05718497, 1.06851158,
       1.08508687, 1.07853471, 1.08321566, 1.0779714 , 1.07885479,
       1.07784337, 1.08879334, 1.07627126]
CO_intercept = [-3.25823985, -2.81917073, -3.42491811, -1.73777896, -3.77446838,
       -4.98576847, -4.31965464, -4.00183064, -3.63125074, -3.90676217,
       -3.95032122, -4.32512746, -3.40961519]

cmap = plt.get_cmap("tab20")

ii = 0
for ct, data in df_lowcal.groupby('groups'):
    CO_series = pd.Series(data['CO_dry'].values)
    #CO_series = CO_series*CO_slope[ii] + CO_intercept[ii]
    low_CO_mean[ii], low_CO_std[ii] = calc_mean(CO_series)
    #x=np.linspace(0,len(CO_series)-1,num=len(CO_series))+ii*60 # make sequential
    ln1 = ax[0].plot(CO_series,'-',color=cmap(ii))
    #ax[0].plot(CO_series_mean,':',color=ln1[0].get_color())
    ii += 1

ii = 0
for ct, data in df_highcal.groupby('groups'):
    CO_series = pd.Series(data['CO_dry'].values)
    #CO_series = CO_series*CO_slope[ii] + CO_intercept[ii]
    high_CO_mean[ii], high_CO_std[ii] = calc_mean(CO_series)
    ax[1].plot(CO_series,'-')
    ii += 1
    
ii = 0
for ct, data in df_lowcal.groupby('groups'):
    N2O_series = pd.Series(data['N2O_dry'].values)
    low_N2O_mean[ii], low_N2O_std[ii] = calc_mean(N2O_series)
    ax[2].plot(data['N2O_dry'].values,'-')
    ii += 1

ii = 0
for ct, data in df_highcal.groupby('groups'):
    N2O_series = pd.Series(data['N2O_dry'].values)
    high_N2O_mean[ii], high_N2O_std[ii] = calc_mean(N2O_series)
    ax[3].plot(data['N2O_dry'].values,'-')
    ii += 1

# format plot
#ax[0].set_xlim(0,60)
ax[0].set_ylim(47,52)
ax[0].grid('on')
ax[0].set_ylabel('CO low, ppb')
ax[1].set_xlim(0,60)
#ax[1].set_ylim(148,158)
ax[1].grid('on')
ax[1].set_ylabel('CO high, ppb')
ax[2].set_xlim(0,60)
#ax[2].set_ylim(230,242)
ax[2].grid('on')
ax[2].set_ylabel('N2O low, ppb')
ax[3].set_xlim(0,60)
#ax[3].set_ylim(300,318)
ax[3].grid('on')
ax[3].set_ylabel('N2O high, ppb')

#
#ax2[0].set_xlabel('Seconds')
#ax2[0].set_title('Low cal')
#ax2[1].set_xlabel('Seconds')
#ax2[1].set_title('High cal')
#ax[3].legend(np.linspace(1,13,13,dtype='int'),fontsize=5)

plt.tight_layout()

#fig.savefig('fig1.png',dpi=300)

# %% plot calibration results
fig, ax = plt.subplots(1, 4, figsize=(7,2),dpi=200)

# (maybe replace below with sum(low_CO_mean>0))

if case == 0: # FCF
    x = np.linspace(0,8,9)
    rng = range(0,9)
elif case == 1: #Test Flight #1
    x = np.linspace(0,13,14)
    rng = range(0,14)
elif case == 2: #Test Flight #2
    x = np.linspace(0,12,13)
    rng = range(0,13)
elif case == 3: #Test Flight #3
    x = np.linspace(0,13,14)
    rng = range(0,14)
elif case == 8: #Cal gases in lab [didn't verify # of cycles below]
    x = np.linspace(0,13,14)
    rng = range(0,14)
elif case == 9:
    x = np.linspace(0,7,8)
    rng = range(0,8)
else:
    x = np.nan

for ii in x:
    ii = int(ii)
    ax[0].errorbar(x=ii, y=low_CO_mean[ii], yerr=2 * low_CO_std[ii],ls='none',fmt='kx',markersize=3,color=cmap(ii))
ax[0].set_xlabel('Cycle #')
ax[0].set_ylabel('CO, ppb')
#ax[0].set_ylim([46,52])

ax[1].errorbar(x=x, y=high_CO_mean[rng], yerr=2 * high_CO_std[rng],ls='none',fmt='kx',markersize=3)
ax[1].set_xlabel('Cycle #')
ax[1].set_ylabel('CO, ppb')
#ax[1].set_ylim([46,52])

ax[2].errorbar(x=x, y=low_N2O_mean[rng], yerr=2 * low_N2O_std[rng],ls='none',fmt='kx',markersize=3)
ax[2].set_xlabel('Cycle #')
ax[2].set_ylabel('N2O, ppb')
#ax[2].set_ylim([46,52])

ax[3].errorbar(x=x, y=high_N2O_mean[rng], yerr=2 * high_N2O_std[rng],ls='none',fmt='kx',markersize=3)
ax[3].set_xlabel('Cycle #')
ax[3].set_ylabel('N2O, ppb')
#ax[3].set_ylim([46,52])

plt.tight_layout()

# linear slope and intercept: CO
print('Case number:' + str(case))
print("CO stats")
CO_low_ratio = np.zeros(len(rng))
CO_high_ratio = np.zeros(len(rng))
CO_slope = np.zeros(len(rng))
CO_intercept = np.zeros(len(rng))

for ii in rng:
    # CO
    x1=50.64 # tank value
    x2=162.2 # tank value
    y1=low_CO_mean[ii]
    y2=high_CO_mean[ii]
    m = (x2-x1)/(y2-y1) # original method that Emma showed
    b = x1-y1*m # same as x2-y2*m
    print("{:.3f}".format(x1/y1) + ", ",end="")
    print("{:.3f}".format(x2/y2) + ", ",end="")
    print("{:.3f}".format(m) + '*x + ' + "{:.3f}".format(b))
    
    CO_low_ratio[ii] = x1/y1
    CO_high_ratio[ii] = x2/y2
    CO_slope[ii] = m
    CO_intercept[ii] = b

# linear slope and intercept: N2O
print("N2O stats")
N2O_low_ratio = np.zeros(len(rng))
N2O_high_ratio = np.zeros(len(rng))
N2O_slope = np.zeros(len(rng))
N2O_intercept = np.zeros(len(rng))

for ii in rng:
    x1=265.87 # tank value
    x2=348.03 # tank value
    y1=low_N2O_mean[ii]
    y2=high_N2O_mean[ii]
    m = (x2-x1)/(y2-y1)
    b = x1-y1*m # same as x2-y2*m
    print("{:.3f}".format(x1/y1) + ", ",end="")
    print("{:.3f}".format(x2/y2) + ", ",end="")
    print("{:.3f}".format(m) + '*x + ' + "{:.3f}".format(b))
    
    N2O_low_ratio[ii] = x1/y1
    N2O_high_ratio[ii] = x2/y2
    N2O_slope[ii] = m
    N2O_intercept[ii] = b

#plt.savefig('fig1.png',dpi=300)

# print averages
print('Average values:')
print('CO low ratio ' + "{:.3f}".format(np.mean(CO_low_ratio)))
print('CO high ratio ' + "{:.3f}".format(np.mean(CO_high_ratio)))
print('CO equation ' + "{:.3f}".format(np.mean(CO_slope)) + 'x + ' 
                     + "{:.3f}".format(np.mean(CO_intercept)))

print('N2O low ratio ' + "{:.3f}".format(np.mean(N2O_low_ratio)))
print('N2O high ratio ' + "{:.3f}".format(np.mean(N2O_high_ratio)))
print('N2O equation ' + "{:.3f}".format(np.mean(N2O_slope)) + 'x + ' 
                     + "{:.3f}".format(np.mean(N2O_intercept)))

# %% test curve fit
# Exponential fit to determine flush rate and steady state concentration
# (skip first several points where concentration seems to overshoot)
# probably difficult in general; need to look at cases one by one
# https://stackoverflow.com/questions/3938042/fitting-exponential-decay-with-no-initial-guessing

"""
from scipy.optimize import curve_fit
def func(x, a, b, c):
    return a*np.exp(-b*x) + c

x = np.linspace(3,60,58)
y = 200-data['CO_dry'].values[3:] # make curve descending

popt, pcov = curve_fit(func, x, y)

plt.plot(200-data['CO_dry'].values,'.')
plt.plot(x,func(x,popt[0],popt[1],popt[2]),'.')
"""