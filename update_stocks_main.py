# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 10:57:30 2022

@author: Gebruiker

Wat hebben we hiervoor nodig? 
1. Het script wat de data ophaalt. 
2. Een module die de data in de DB zet. 

Belangijk:
    1. Data moet in gitignore.
    2. data moet gecheckt worden 
    
proces: 
    in de initalizatie moeten de aandelen in de DB komen. 
    in de update_module moeten de aandelen gecontrolleerd en geupdate worden. 
    s
"""
import constants 
from core_scripts.stock_data_download import power_stock_object
import database_querys_main as database_querys
from core_utils.core_initalization.initializer_tickers import initialization_support

# added these so string with data can be saved. 
from core_utils.save_temp_data import save_and_load_temp_data

import support_class

import time
import os, sys
from datetime import datetime


class update_stocks: 
    
    @staticmethod
    def download_stockdata():
        """
        
        
        Downloads all active tickers.


        
        Raises
        ------
        Exception
            DESCRIPTION.

        Returns
        -------
        None.

        """
        # 
        try:
            
            # retreives the active tickers. Tickers are maintained with the initialize ticker file.
            tickers = database_querys.database_querys.get_all_active_tickers()
        
        except Exception as e:
            
            print(e)
            
            raise Exception("EEROR")
        
        # declairs startime and end time vars
        start_time = 0 
        end_time = 0 
        
        support_class.clear()
        time.sleep(3)
        print("\nupdating stockdata\n")
        
        # loops true the tickers, and updates the tickers. 
        #for i in tqdm(range(0,len(tickers))):
            
        for ticker in tickers:
            
            #with HiddenPrints():
                
                #ticker = tickers[i]
                
                end_time = time.time()
                
                time_to_sleep = initialization_support.speed_limiter(start_time,end_time,2.6)
                time.sleep(time_to_sleep)
                start_time = time.time()
                
                initialization_support.speed_limiter()
                stocks_object = power_stock_object.power_stock_object(stock_ticker = ticker)
                  
        
        # save the date for the daily update. 
        update_stocks_support.saving_last_daily_update()
        
        
        
class update_stocks_support:
    
    @staticmethod
    def saving_last_daily_update(name_ticker : str = ""):

        now = datetime.now() 
        data = date_time = now.strftime("%d-%m-%Y, %H:%M:%S")
        data = save_and_load_temp_data.save_and_load_temp_data_class.save_data(data, "LAST_DAILY_UPDATE", "system_info")
        
        return 
    
class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


if __name__ == "__main__":    
    
    try:
        #update_stocks_support.saving_last_daily_update()
        
        the_update_class = update_stocks()
        the_update_class.download_stockdata()
        #tickers = database_querys.database_querys.get_all_active_tickers()
        #print(tickers)
        
        #stocks_object = power_stock_object.power_stock_object(stock_ticker = "AFBI")
        
    except Exception as e:
        
        raise Exception("Error with tickers", e)