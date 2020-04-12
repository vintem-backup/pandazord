#TODO: Docstrings and Type annotations
#TODO: Se for reaproveitar este programa, substituir "binance_assets" e simiçares por apenas "assets"

import sys
import os
import subprocess
import time
import psutil
from datetime import datetime
from iteration_utilities import duplicates, unique_everseen
from modules.postgres_handler import PostgresHandler as PG
from modules.useful_functions import *

DB_HOST = os.environ['DB_HOST']
POSTGRES_USER = os.environ['POSTGRES_USER']
POSTGRES_DB = os.environ['POSTGRES_DB']
POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']

candle_interval = '1m'

DB_HOST='postgres_dev'

pg = PG(DB_HOST, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD)

def listen_to_asset_table(control_assets_table_name):

    control_assets_table_name = '"' + control_assets_table_name + '"'
    
    while True:

        try:

            binance_assets = pg.read_entries_from_table(control_assets_table_name)

            if (len(binance_assets) == 0): time.sleep(1)

            else:
                
                pid_list = []

                for binance_asset in binance_assets:

                    pid = binance_asset['last_updated_by_pid']
                    
                    pid_list.append(pid)
                    
                    oldest_open_time = (int(datetime.timestamp(
                        binance_asset['collect_data_since'])))*1000 #milisseconds

                    if (binance_asset['auto_update'] == 'ON'):

                        if not (running_this_subprocess(pid)):

                            complete_data_subprocess = subprocess.Popen([sys.executable,
                            # This program on a isolated subprocess...
                            'complete_oldest_data_so_far.py',
                            
                            # ... running with this args:
                            control_assets_table_name,
                            str(binance_asset['asset_symbol']),
                            candle_interval,
                            str(oldest_open_time)])

                            was_entry_updated_pid = pg.update_entry(control_assets_table_name, 
                                                        'asset_symbol', 
                                                        str(binance_asset['asset_symbol']),
                                                        'last_updated_by_pid',
                                                        int(complete_data_subprocess.pid))

                            if not (was_entry_updated_pid): pass #TODO: Tratar exceção

                    else:

                        if(running_this_subprocess(pid)): psutil.Process(pid).kill()

                #Killing duplicated PIDs
                duplicated_pid_list = list(unique_everseen(duplicates(pid_list)))
                
                if (len(duplicated_pid_list) > 0):

                    for duplicated_pid in duplicated_pid_list:

                        if(running_this_subprocess(duplicated_pid)): psutil.Process(duplicated_pid).kill()
                
                time.sleep(60 - int(datetime.now().second))

        except (Exception) as error: 
            print(error)
            time.sleep(1)

if __name__ == "__main__":
    control_assets_table_name = str(sys.argv[1])
    listen_to_asset_table(control_assets_table_name)