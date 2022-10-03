# -*- coding: utf-8 -*-
"""
Main function used by Fig9_cal_cycle_calculation
"""

# headers
import numpy as np
import pandas as pd

# function to calculate the average and standard deviation at end of cal cycle
def calc_mean(gas_vals):
    rolling_mean = gas_vals.rolling(10).mean()
    rolling_std = gas_vals.rolling(10).std()
    mean_val = rolling_mean.iloc[-1] # last value
    std_val = rolling_std.iloc[-1]  # last value
    return mean_val, std_val

def calc_cal(COMA,ix):    
    # make DataFrame
    df_cal = pd.DataFrame({'time': COMA['time'][ix],
                           '[CO]d_ppb': COMA["[CO]d_ppm"][ix]*1000,
                           '[N2O]d_ppb': COMA["[N2O]d_ppm"][ix]*1000,
                           '[H2O]_ppm': COMA['[H2O]_ppm'][ix],
                           'AmbT_C': COMA['AmbT_C'][ix],
                           'Peak0': COMA['Peak0'][ix],
                           'AIN5': COMA['AIN5'][ix],
                           'AIN6': COMA['AIN6'][ix],
                           'GasP_torr': COMA['GasP_torr'][ix],
                           'SpectraID': COMA['SpectraID'][ix]
                           })
    
    # group data
    df_cal['groups'] = (df_cal.index.to_series().diff()>5).cumsum()
    df_grouped = df_cal.groupby('groups')
    
    # set up output variables
    feature_list = ['time','CO_val','CO_std','N2O_val','N2O_std',
                    'H2O','AmbT_C','Peak0','AIN5','AIN6',
                    'start','end','start_ct','end_ct','time_on']
    zero_data = np.zeros( shape = (len(df_grouped), len(feature_list)) )
    res = pd.DataFrame(zero_data, columns=feature_list)
    
    # look through cal cycles
    for ct, data in df_grouped:
        CO_series = pd.Series(data['[CO]d_ppb'].values)
        N2O_series = pd.Series(data['[N2O]d_ppb'].values)
        H2O_series = pd.Series(data['[H2O]_ppm'].values)
        
        res.loc[ct,'time'] = data['time'].values[0] #start of sequence
        res.loc[ct,'CO_val'], res.loc[ct,'CO_std'] = calc_mean(CO_series)        
        res.loc[ct,'N2O_val'], res.loc[ct,'N2O_std'] = calc_mean(N2O_series)
        
        res.loc[ct,'AmbT_C'] = np.mean(data['AmbT_C'].values)
        res.loc[ct,'Peak0'] = np.mean(data['Peak0'].values)
        res.loc[ct,'AIN5'] = np.mean(data['AIN5'].values)
        res.loc[ct,'AIN6'] = np.mean(data['AIN6'].values)
        res.loc[ct,'GasP_torr'] = np.mean(data['GasP_torr'].values)
        
        res.loc[ct,'SpectraID'] = data['SpectraID'].values[-1]
        res.loc[ct,'H2O'] = data['[H2O]_ppm'].values[-1]
        
        res.loc[ct,'start'] = min(data.index)
        res.loc[ct,'end'] = max(data.index)
        
        if ct == 0:
            res.loc[ct,'start_ct'] = 0
            res.loc[ct,'end_ct'] = len(data)-1
        else:
            res.loc[ct,'start_ct'] = res.loc[ct-1,'end_ct'] + 1
            res.loc[ct,'end_ct'] = res.loc[ct,'start_ct'] + len(data)-1
            
    return res

# %% remove for now: linear regression
    """
    # number of cycles
    n = sum(low_CO_mean>0)
    rng = range(0,n)
    
    # linear slope and intercept: CO and N2O
    CO_low_ratio = np.zeros(len(rng))
    CO_high_ratio = np.zeros(len(rng))
    CO_slope = np.zeros(len(rng))
    CO_intercept = np.zeros(len(rng))
    
    N2O_low_ratio = np.zeros(len(rng))
    N2O_high_ratio = np.zeros(len(rng))
    N2O_slope = np.zeros(len(rng))
    N2O_intercept = np.zeros(len(rng))
    
    starting_index = np.zeros(len(rng),dtype=int)
    
    # loop through and calculate slope/intercepts         
    for ii in rng:
        # CO
        x1=low_tank_CO # low tank value
        x2=high_tank_CO # high tank value
        y1=low_CO_mean[ii]
        y2=high_CO_mean[ii]
        m = (x2-x1)/(y2-y1) # original method that Emma showed
        b = x1-y1*m # same as x2-y2*m
        
        CO_low_ratio[ii] = x1/y1
        CO_high_ratio[ii] = x2/y2
        CO_slope[ii] = m
        CO_intercept[ii] = b

        x1=low_tank_N2O # low tank value
        x2=high_tank_N2O # high tank value
        y1=low_N2O_mean[ii]
        y2=high_N2O_mean[ii]
        m = (x2-x1)/(y2-y1)
        b = x1-y1*m # same as x2-y2*m
        
        N2O_low_ratio[ii] = x1/y1
        N2O_high_ratio[ii] = x2/y2
        N2O_slope[ii] = m
        N2O_intercept[ii] = b
        
        tmp = np.argmax(df_lowcal['groups']==ii)
        starting_index[ii] = df_lowcal.index[tmp]

    starting_index = np.append(starting_index,len(CO_raw))
    
    # apply calibration factors to data
    CO_calibrated = CO_raw*1000
    N2O_calibrated = N2O_raw*1000
    
    for ii in rng:
        tmp = CO_raw[starting_index[ii]:starting_index[ii+1]]*1000
        CO_calibrated[starting_index[ii]:starting_index[ii+1]] = tmp*CO_slope[ii]+CO_intercept[ii]
    
        tmp = N2O_raw[starting_index[ii]:starting_index[ii+1]]*1000
        N2O_calibrated[starting_index[ii]:starting_index[ii+1]] = tmp*N2O_slope[ii]+N2O_intercept[ii]
    
    # calibration outputs
    CO_cal = pd.DataFrame({'low_mean': low_CO_mean[rng],
                           'low_std': low_CO_std[rng],
                           'high_mean': high_CO_mean[rng],
                           'high_std': high_CO_std[rng],
                           'low_ratio': CO_low_ratio,
                           'high_ratio': CO_high_ratio, 
                           'slope': CO_slope,
                           'intercept': CO_intercept,
                           'time':CO_time[rng],
                           'cell_T':cell_T[rng]})
    N2O_cal = pd.DataFrame({'low_mean': low_N2O_mean[rng],
                            'low_std': low_N2O_std[rng],
                            'high_mean': high_N2O_mean[rng],
                            'high_std': high_N2O_std[rng],
                            'low_ratio': N2O_low_ratio,
                            'high_ratio': N2O_high_ratio, 
                            'slope': N2O_slope,
                            'intercept': N2O_intercept})
    return CO_cal, N2O_cal
    """

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