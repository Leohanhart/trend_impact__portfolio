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
    
"""
import constants 
from core_scripts.stock_data_download import power_stock_object
from core_utils.database_querys import database_querys
from core_utils.core_initalization.initializer_tickers import initialization_support
import time

class update_stocks: 
    
    @staticmethod
    def download_stockdata():
        try:
            
            tickers = database_querys.database_querys.get_all_active_tickers()
        
        except Exception as e:
            
            print(e)
            
            raise Exception("EEROR")
            
        start_time = 0 
        end_time = 0 
        
        for ticker in tickers:
            
            end_time = time.time()
            
            time_to_sleep = initialization_support.speed_limiter(start_time,end_time,2.6)
            time.sleep(time_to_sleep)
            start_time = time.time()
            
            initialization_support.speed_limiter()
            stocks_object = power_stock_object.power_stock_object(stock_ticker = ticker)
              
        
        
        
class update_stocks_support:
    
    @staticmethod
    def check_if_ticker_is_new(name_ticker : str = ""):
        """
        
        Checks if the ticker exsists in DB

        Parameters
        ----------
        name_ticker : str, optional
            DESCRIPTION. The default is "".

        Returns
        -------
        None.

        """
        pass 

if __name__ == "__main__":    
    
    try:
        
        the_update_class = update_stocks()
        the_update_class.download_stockdata()
        #tickers = database_querys.database_querys.get_all_active_tickers()
        #print(tickers)
        
        #stocks_object = power_stock_object.power_stock_object(stock_ticker = "AFBI")
        
    except Exception as e:
        
        raise Exception("Error with tickers", e)