#TODO: Docstrings and type annotations

import sys
from modules.useful_functions import *
from modules.binance_handler import *
from modules.postgres_handler import PostgresHandler as PG

DB_HOST = os.environ['DB_HOST']
POSTGRES_USER = os.environ['POSTGRES_USER']
POSTGRES_DB = os.environ['POSTGRES_DB']
POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']

#TODO: Encontrar um jeito prático de mudar esta variável
DB_HOST='postgres_dev'

pg = PG(DB_HOST, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD)

def return_last_open_time_from_db_or_create_table_if_doesnt_exist(oldest_open_time, table_name, keys_dict):
    last_open_time = oldest_open_time
    
    try:
        last_open_time_datetime_format = pg.read_entries_from_table(table_name, 
                                                    field_key = 'open_time', 
                                                    sort_type = 'DESC', 
                                                    limit = 1)[0][0]

        delta = delta_time_in_seconds_rounded_from_integers_hours_between_utc_and(binance_server_time())
        last_open_time = int(1000*(datetime.timestamp(last_open_time_datetime_format) - delta))

    except:
        table_was_created = pg.create_table(table_name, keys_dict, pk='open_time')
    
        if not (table_was_created): pass #TODO: tratar exceção
    
    return last_open_time

def complete_until_now(control_assets_table_name, asset_symbol, candle_interval, oldest_open_time):
    table_name = 'binance_BT_klines_' + asset_symbol + '_' + candle_interval
    table_name = '"' + table_name + '"'

    keys_dict = {'open_time': 'timestamp', 'open': 'numeric', 'high': 'numeric', 'low': 'numeric', 'close': 'numeric',
    'volume': 'numeric'}

    max_attempts = 10 #TODO: Pode vir de um parâmetro depois
    was_entry_updated_to_building = pg.update_entry(control_assets_table_name, 
                                                    'asset_symbol', asset_symbol, 'status', 'building')

    if not (was_entry_updated_to_building): pass #TODO: Tratar exceção

    while True:
        klines = []

        last_open_time = return_last_open_time_from_db_or_create_table_if_doesnt_exist(
            oldest_open_time, table_name, keys_dict)
        
        start_time = str(last_open_time + 30000)  #Um passo de 30s (30000 milissegundos)
        klines = BinanceKlines(asset_symbol, candle_interval, max_attempts).get_from(start_time)
        
        if (len(klines) > 0):
            
            if (len(klines) < 500): #Chegou na kline mais recente
                klines = klines[:(len(klines)-1)] #Apaga o último resgistro (candle não fechado)
                
                if (len(klines) == 0): break

            treated_missing_data_klines = replace_with_zero_where_data_is_missing(
                oldest_open_time, last_open_time, klines)
            
            delta = delta_time_in_seconds_rounded_from_integers_hours_between_utc_and(binance_server_time())
            
            formated_klines = format_klines(treated_missing_data_klines, delta)
            save_in_table_job_status = pg.save_data_in_table(table_name, keys_dict, formated_klines)

            if (len(klines) > 500): break #TODO: Isto é uma anomalia, deve ser tratada
                
        else: pass #TODO: Tratar exceção (Falha de comunicação com a binance, klines nulas)

        requests_limit_reached = test_binance_request_limit()
        
        if(requests_limit_reached): time.sleep(65)

    was_entry_updated_to_full = pg.update_entry(control_assets_table_name, 'asset_symbol', asset_symbol, 'status', 'full')

    if not (was_entry_updated_to_full): pass #TODO: Tratar exceção

if __name__ == "__main__":
    control_assets_table_name = str(sys.argv[1])
    asset_symbol = str(sys.argv[2])
    candle_interval = str(sys.argv[3])
    oldest_open_time = int(sys.argv[4])    
    
    complete_until_now(control_assets_table_name, asset_symbol, candle_interval, oldest_open_time)