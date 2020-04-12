"""Este módulo traz embarcadas algumas funcionalidades específicas das klines da binance, tais como:
    
    - Tratar do pedido de klines, cuidando para não estourar o limite de requests/período;
    - Verificar o peso das requests já efetuadas naquele minuto corrente;
    - Retornar o horário do servidor da binance, a fim de proceder a correção dos timestamps
    dos dados armazenados.

"""

from django.db import models
import requests
from datetime import datetime
import time

# Create your models here.
class FormatKlines:
    def __init__(self):
        pass

    def main_format(self, raw_klines, delta):
        
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

        def making_seconds_be_zero_on(self, klines_in):

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


    def replace_with_zero_where_data_is_missing(self, oldest_open_time, last_open_time, klines):

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

class BinanceKlines:    
    def __init__(self, asset_symbol:str, candle_interval:str, max_attempts:int):
        
        self.asset_symbol = asset_symbol
        self.candle_interval = candle_interval
        self.max_attempts = max_attempts

    
    def get_from(self, start_time: str) -> list:
        
        self.start_time = start_time
        
        raw_klines = []

        url = '''https://api.binance.com/api/v1/klines?symbol=\
''' + self.asset_symbol + '''&interval=''' + self.candle_interval +\
'''&startTime=''' + self.start_time

        for i in range(self.max_attempts):

            try:

                response = requests.get(url); response.raise_for_statufrom datetime import datetime

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
