"""Este módulo contém classes e funções que são necessãrias ao funcionamento de mais de um app do sistema.

"""

#from django.db import models
from datetime import datetime
import requests
import os
from copy import deepcopy
#import psutil

#Market stuff
class PriceSeriesFrom:
    def __init__(self, market_df):
        
        super().__init__()
        self.market_df = market_df
    
    def open_(self):
        return self.market_df['open']
    
    def high_(self):
        return self.market_df['high']
    
    def low_(self):
        return self.market_df['low']
    
    def close_(self):
        return self.market_df['close']
    
    def ohlc4_(self):
        
        price = (self.market_df['open'] +
                self.market_df['high'] +
                self.market_df['low'] +
                self.market_df['close'])/4
        
        return price
    
    def hl2_(self):
        
        price = (self.market_df['high'] +
                self.market_df['low'])/2
        
        return price
    
    def hlc3_(self):
        
        price = (self.market_df['high'] +
                self.market_df['low'] +
                self.market_df['close'])/3
        
        return price

# Time handlers
class TimeHandler:
    def __init__(self):
        pass
    
    def utc_time_func(self):
        
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


    def delta_time_in_seconds_rounded_from_integers_hours_between_utc_and(self, this_time):

        utc_time = utc_time_func()
        
        delta_time = utc_time - this_time

        delta_hour = round(delta_time.total_seconds()/3600)
        
        delta = delta_hour*3600
        
        return delta

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
