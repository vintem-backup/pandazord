#TODO: Docstrings and type annotations

from datetime import datetime
import requests
import os
from copy import deepcopy
import psutil


def utc_time_func():
    
    try:
    
        url = 'http://worldclockapi.com/api/json/utc/now'

        time_utc_now = requests.get(url).json

        year = int(time_utc_now()['currentDateTime'].split('T')[0].split('-')[0])
        month = int(time_utc_now()['currentDateTime'].split('T')[0].split('-')[1])
        day = int(time_utc_now()['currentDateTime'].split('T')[0].split('-')[2])

        hour = int(time_utc_now()['currentDateTime'].split('T')[1].split(':')[0])
        minute = int(time_utc_now()['currentDateTime'].split('T')[1].split(':')[1].split('Z')[0])
    
        utc_now = datetime(year, month, day, hour, minute)
    
    except (Exception) as error: #TODO: Tratar exceção
        
        utc_now = datetime.utcnow()

    return utc_now


def delta_time_in_seconds_rounded_from_integers_hours_between_utc_and(this_time):

    utc_time = utc_time_func()
    
    delta_time = utc_time - this_time

    delta_hour = round(delta_time.total_seconds()/3600)
    
    delta = delta_hour*3600
    
    return delta


def format_klines(raw_klines, delta):
    
    def clear_columns_and_adjust_time_and_prices_and_volume_on(raw_klines, delta):

        klines_out = []

        for i in range (len(raw_klines)):

            data = [datetime.fromtimestamp(int(raw_klines[i][0]/1000) + delta), #open_time
                    float(raw_klines[i][1]), #Open
                    float(raw_klines[i][2]), #High
                    float(raw_klines[i][3]), #Low
                    float(raw_klines[i][4]), #Close
                    float(raw_klines[i][5]) #volume
                    ]

            klines_out.append(data)

        return klines_out

    def making_seconds_be_zero_on(klines_in):

        klines_out = deepcopy(klines_in)

        for i in range(len(klines_in)):

            entry = klines_in[i][0]

            if (entry.second != 0):

                out = datetime.fromtimestamp((datetime.timestamp(entry) - entry.second))

                klines_out[i][0] = out

        return klines_out

    klines_adjusted = clear_columns_and_adjust_time_and_prices_and_volume_on(raw_klines, delta)

    klines = making_seconds_be_zero_on(klines_adjusted)

    return klines


def replace_with_zero_where_data_is_missing(oldest_open_time, last_open_time, klines):

    #This indicates the first call, so the adjust must be bypassed
    if (last_open_time == oldest_open_time): klines_out = klines
    
    else:
        
        auxiliary_list = []
    
        auxiliary_list.append(int(last_open_time + 60000))

        for i in range(0, len(klines)-1):

            auxiliary_list.append(auxiliary_list[i] + 60000)
    
        klines_out = deepcopy(klines)

        for i in range (len(klines)):

            compatibility = bool(int(klines_out[i][0]) == auxiliary_list[i])

            if (compatibility): pass

            else:

                klines_out[i][0] = auxiliary_list[i] #Open_time
                klines_out[i][1] = 0.0 #Open
                klines_out[i][2] = 0.0 #High
                klines_out[i][3] = 0.0 #Low
                klines_out[i][4] = 0.0 #Close
                klines_out[i][5] = 0.0 #volume

    return klines_out


def running_this_subprocess(pid):
    
    if pid == None: return False
    
    elif isinstance(pid, int):
        
        if (psutil.pid_exists(pid)):
            
            process = psutil.Process(pid)
            
            if (process.status() == 'zombie'): 
                
                process.kill()
                
                return False
            
            else: return True
        
        else: return False
        
    else: raise TypeError('Not a valid type. Should be integer or None.')