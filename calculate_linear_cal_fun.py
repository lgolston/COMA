# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 13:08:19 2022

@author: madco
"""

# headers
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# function to calculate the average and standard deviation at end of cal cycle
def calc_mean(gas_vals):
    rolling_mean = gas_vals.rolling(10).mean()
    rolling_std = gas_vals.rolling(10).std()
    mean_val = rolling_mean.iloc[-1] # last value
    std_val = rolling_std.iloc[-1]  # last value
    return mean_val, std_val

def calc_cal(LGR_time,CO_raw,N2O_raw,ix_low,ix_high):    
    low_CO_mean = np.zeros(20)
    low_CO_std = np.zeros(20)
    high_CO_mean = np.zeros(20)
    high_CO_std = np.zeros(20)
    low_N2O_mean = np.zeros(20)
    low_N2O_std = np.zeros(20)
    high_N2O_mean = np.zeros(20)
    high_N2O_std = np.zeros(20)
    
    df_lowcal = pd.DataFrame({'time': LGR_time[ix_low], 'CO_dry': CO_raw[ix_low]*1000, 'N2O_dry': N2O_raw[ix_low]*1000})
    df_lowcal['groups'] = (df_lowcal.index.to_series().diff()>5).cumsum()
    df_highcal = pd.DataFrame({'time': LGR_time[ix_high], 'CO_dry': CO_raw[ix_high]*1000, 'N2O_dry': N2O_raw[ix_high]*1000})
    df_highcal['groups'] = (df_highcal.index.to_series().diff()>5).cumsum()
    
    ii = 0
    for ct, data in df_lowcal.groupby('groups'):
        CO_series = pd.Series(data['CO_dry'].values)
        low_CO_mean[ii], low_CO_std[ii] = calc_mean(CO_series)
        ii += 1

    ii = 0
    for ct, data in df_highcal.groupby('groups'):
        CO_series = pd.Series(data['CO_dry'].values)
        high_CO_mean[ii], high_CO_std[ii] = calc_mean(CO_series)
        ii += 1
        
    ii = 0
    for ct, data in df_lowcal.groupby('groups'):
        N2O_series = pd.Series(data['N2O_dry'].values)
        low_N2O_mean[ii], low_N2O_std[ii] = calc_mean(N2O_series)
        ii += 1

    ii = 0
    for ct, data in df_highcal.groupby('groups'):
        N2O_series = pd.Series(data['N2O_dry'].values)
        high_N2O_mean[ii], high_N2O_std[ii] = calc_mean(N2O_series)
        ii += 1
    
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
        x1=50.64 # low tank value
        x2=162.2 # high tank value
        y1=low_CO_mean[ii]
        y2=high_CO_mean[ii]
        m = (x2-x1)/(y2-y1) # original method that Emma showed
        b = x1-y1*m # same as x2-y2*m
        
        CO_low_ratio[ii] = x1/y1
        CO_high_ratio[ii] = x2/y2
        CO_slope[ii] = m
        CO_intercept[ii] = b

        x1=265.87 # low tank value
        x2=348.03 # high tank value
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

    # apply calibration factors
    CO_cal = CO_raw*1000
    N2O_cal = N2O_raw*1000
    
    for ii in rng:
        tmp = CO_raw[starting_index[ii]:starting_index[ii+1]]*1000
        CO_cal[starting_index[ii]:starting_index[ii+1]] = tmp*CO_slope[ii]+CO_intercept[ii]
    
        tmp = N2O_raw[starting_index[ii]:starting_index[ii+1]]*1000
        N2O_cal[starting_index[ii]:starting_index[ii+1]] = tmp*N2O_slope[ii]+N2O_intercept[ii]
    
    #breakpoint()
    
    # print averages
    """
    print('Average values:')
    print('CO low ratio ' + "{:.3f}".format(np.mean(CO_low_ratio)))
    print('CO high ratio ' + "{:.3f}".format(np.mean(CO_high_ratio)))
    print('CO equation ' + "{:.3f}".format(np.mean(CO_slope)) + 'x + ' 
                         + "{:.3f}".format(np.mean(CO_intercept)))

    print('N2O low ratio ' + "{:.3f}".format(np.mean(N2O_low_ratio)))
    print('N2O high ratio ' + "{:.3f}".format(np.mean(N2O_high_ratio)))
    print('N2O equation ' + "{:.3f}".format(np.mean(N2O_slope)) + 'x + ' 
                         + "{:.3f}".format(np.mean(N2O_intercept)))
    """
    
    # calibrated outputs
    return CO_cal, N2O_cal