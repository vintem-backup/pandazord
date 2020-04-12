import requests
from datetime import datetime
import time

class BinanceKlines:
    
    def __init__(self, asset_symbol, candle_interval, max_attempts):
        
        self.asset_symbol = asset_symbol
        self.candle_interval = candle_interval
        self.max_attempts = max_attempts

    
    def get_from(self, start_time):
        
        self.start_time = start_time
        
        raw_klines = []

        url = '''https://api.binance.com/api/v1/klines?symbol=\
''' + self.asset_symbol + '''&interval=''' + self.candle_interval +\
'''&startTime=''' + self.start_time

        for i in range(self.max_attempts):

            try:

                response = requests.get(url); response.raise_for_status()
                
                if (int(response.status_code) == 200): raw_klines = response.json(); break

            except (Exception, requests.exceptions.RequestException, 
            requests.exceptions.ConnectionError) as error: time.sleep(5) #TODO: TRATAR EXCEÇÃO AQUI
            
        return raw_klines

    
    def get_from_to(self):
        pass


def binance_server_time():

    binance_time = datetime.now()

    url = 'https://api.binance.com/api/v1/time'

    for i in range(5):

        try:

            response = requests.get(url); response.raise_for_status()

            if (int(response.status_code) == 200):

                binance_time = datetime.fromtimestamp(int((response).json()['serverTime'])/1000)

            break

        except (Exception, requests.exceptions.RequestException, 
        requests.exceptions.ConnectionError) as error: time.sleep(2) #TODO: TRATAR EXCEÇÃO AQUI

    return binance_time


def test_binance_request_limit():
    
    requests_limit_reached = True #Default
    
    for i in range(5):
        
        try:

            response_ping = requests.get('https://api.binance.com/api/v1/ping')
            
            #False if X-MBX-USED-WEIGHT < 1100
            requests_limit_reached = bool(int(response_ping.headers['X-MBX-USED-WEIGHT']) >= 1100)
            
            if not (requests_limit_reached): break
        
        except (Exception, requests.exceptions.RequestException, 
        requests.exceptions.ConnectionError) as error: time.sleep(2) #TODO: TRATAR EXCEÇÃO AQUI

    return requests_limit_reached