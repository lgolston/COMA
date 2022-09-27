# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 22:58:33 2022

"""

# %% headers
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from datetime import datetime, timedelta
import matplotlib.dates as mdates
from load_flight_functions import read_MMS

# %% loop to load the data
COMA = []

for ii in range(3,18):
    if ii == 3: #WB-RF03: 2022-08-02
        COMA_filename = './ict/acclip-COMA-CON2O_WB57_20220802_RA.ict'
        MMS_filename = '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20220802_RA.ict'
        cur_day = datetime(2022,8,2) # used by COMA reading below (not really necessary)
        
    elif ii == 4: #WB-RF04: 2022-08-04
        COMA_filename = './ict/acclip-COMA-CON2O_WB57_20220804_RA.ict'
        MMS_filename = '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20220804_RA.ict'
        cur_day = datetime(2022,8,4)
        
    elif ii == 5: #WB-RF05: 2022-08-06
        COMA_filename = './ict/acclip-COMA-CON2O_WB57_20220806_RA.ict'
        MMS_filename = '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20220806_RA.ict'
        cur_day = datetime(2022,8,6)
        
    elif ii == 6: #WB-RF06: 2022-08-12
        COMA_filename = './ict/acclip-COMA-CON2O_WB57_20220812_RA.ict'
        MMS_filename = '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20220812_RA.ict'
        cur_day = datetime(2022,8,12)
        
    elif ii == 7: #WB-RF07: 2022-08-13
        COMA_filename = './ict/acclip-COMA-CON2O_WB57_20220813_RA.ict'
        MMS_filename = '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20220813_RA.ict'
        cur_day = datetime(2022,8,13)
        
    elif ii == 8: #WB-RF08: 2022-08-15
        COMA_filename = []
        MMS_filename = '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20220815_RA.ict'
        cur_day = datetime(2022,8,15)
        
    elif ii == 9: #WB-RF09: 2022-08-16
        COMA_filename = './ict/acclip-COMA-CON2O_WB57_20220816_RA.ict'
        MMS_filename = '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20220816_RA.ict'
        cur_day = datetime(2022,8,16)
        
    elif ii == 10: #WB-RF10: 2022-08-19
        COMA_filename = './ict/acclip-COMA-CON2O_WB57_20220819_RA.ict'
        MMS_filename = '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20220819_RA.ict'
        cur_day = datetime(2022,8,19)
        
    elif ii == 11: #WB-RF11: 2022-08-21
        COMA_filename = './ict/acclip-COMA-CON2O_WB57_20220821_RA.ict'
        MMS_filename = '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20220821_RA.ict'
        cur_day = datetime(2022,8,21)
        
    elif ii == 12: #WB-RF12: 2022-08-23
        COMA_filename = './ict/acclip-COMA-CON2O_WB57_20220823_RA.ict'
        MMS_filename = '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20220823_RA.ict'
        cur_day = datetime(2022,8,23)
        
    elif ii == 13: #WB-RF13: 2022-08-25
        COMA_filename = './ict/acclip-COMA-CON2O_WB57_20220825_RA.ict'
        MMS_filename = '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20220825_RA.ict'
        cur_day = datetime(2022,8,25)
        
    elif ii == 14: #WB-RF14: 2022-08-26
        COMA_filename = './ict/acclip-COMA-CON2O_WB57_20220826_RA.ict'
        MMS_filename = '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20220826_RA.ict'
        cur_day = datetime(2022,8,26)
        
    elif ii == 15: #WB-RF15: 2022-08-29
        COMA_filename = './ict/acclip-COMA-CON2O_WB57_20220829_RA.ict'
        MMS_filename = '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20220829_RA.ict'
        cur_day = datetime(2022,8,29)
        
    elif ii == 16: #WR-RF16: 2022-08-31
        COMA_filename = './ict/acclip-COMA-CON2O_WB57_20220831_RA.ict'
        MMS_filename = '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20220831_RA.ict'
        cur_day = datetime(2022,8,31)
        
    elif ii == 17: #WB-RF17: 2022-09-01
        COMA_filename = './ict/acclip-COMA-CON2O_WB57_20220901_RA.ict'
        MMS_filename = '../Data/_OtherData_/ACCLIP-MMS-1HZ_WB57_20220901_RA.ict'
        cur_day = datetime(2022,9,1)

    if len(COMA_filename)>0:
        if len(COMA) == 0:
            COMA = pd.read_csv(COMA_filename,header=35)
            COMA['time'] = [cur_day+timedelta(seconds=t) for t in COMA['Time_Mid']]
            COMA['flightID'] = [ii for t in COMA['Time_Mid']]
            MMS = read_MMS(MMS_filename)
        else:
            COMA2 = pd.read_csv(COMA_filename,header=35)
            COMA2['time'] = [cur_day+timedelta(seconds=t) for t in COMA2['Time_Mid']]
            COMA2['flightID'] = [ii for t in COMA2['Time_Mid']]
            MMS2 = read_MMS(MMS_filename)
            
            COMA = pd.concat([COMA,COMA2],ignore_index=True)
            MMS = pd.concat([MMS,MMS2],ignore_index=True)

# %% sychronize data
COMA[COMA['CO'] == -9999] = np.nan

MMS_sync = MMS.groupby(pd.Grouper(key="time", freq="10s")).mean()
COMA_sync = COMA.groupby(pd.Grouper(key="time", freq="10s")).mean()
sync_data = pd.merge(MMS_sync, COMA_sync, how='inner', on=['time'])

# %% plot data
fig1, ax1 = plt.subplots(1, 1, figsize=(5,4))
#plt.plot(COMA['Time_Mid'],COMA['CO'],'.')
cmap = matplotlib.cm.terrain
bounds=[3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
norm = matplotlib.colors.BoundaryNorm(bounds, cmap.N)

sync_randomized = sync_data.sample(frac=1)

sc = ax1.scatter(sync_randomized['CO'],sync_randomized['ALT'],
                 c=sync_randomized['flightID'],s=2,alpha=1,cmap=cmap,norm=norm)
ax1.set_xlim(0,400)
ax1.grid('on')
ax1.set_xlabel('CO, ppbv')
ax1.set_ylabel('Altitude, m')
cb = plt.colorbar(sc)
cb.set_label('Flight ID')
cb.solids.set(alpha=1)
fig1.tight_layout()

#fig1.savefig('fig1.png',dpi=300)