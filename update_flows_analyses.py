# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 11:50:35 2022

@author: Gebruiker
"""

import constants 
import database_querys_main as database_querys
import stock_analyses_with_ticker_main as stock_analyses_with_ticker

from core_update.update_analyses import update_support
import support_class
from tqdm import tqdm
import time

class update_money_flow_analyses(object):
    
    @staticmethod 
    def update_analyses(periode = "W"):
        """
        Update moneyflow analayses

        Returns
        -------
        None.

        """
        
        # get tickers
        tickers = database_querys.database_querys.get_all_active_tickers()
        
        # clear console.
        support_class.clear()
        
        print("Update moneyflow analyses")
        
        # loops true tickers. 
       
        for ticker in tickers:   
            
            try:

                update_money_flow_analyses.update_moneyflow_weekly_analyses(ticker, periode)
                    
            except Exception as e:
                print("this is the error.")
                print(e) 

    @staticmethod
    def update_moneyflow_weekly_analyses(ticker : str = "", periode : str = "W"):
        
        periode : str = periode
        ticker_in : str = ticker
        analyses : str = "MONEYFLOWS"
        
        try:
            # get data
            analyses = stock_analyses_with_ticker.update_support_functions.get_stock_analyses_with_ticker(ticker, analyses , periode )
            
        except Exception as e:
            print(e)
             
       
        # does query.
        database_querys.database_querys.update_analyses_moneyflow(ticker_id =ticker_in, 
                                                                  periode = periode, 
                                                                  profile = analyses["last_calculation_profile_indicator_number"], 
                                                                  profile_rate_of_change = analyses['last_calculation_profile_change_number'], 
                                                                  rate_of_change = 0, 
                                                                  last = int(analyses["indicator_timeserie_raw"]["Data"].tail(1)),
                                                                  last_signal = update_support.update_support_functions.get_last_signal(analyses),
                                                                  periode_since_signal= update_support.update_support_functions.get_last_signal(analyses,True) 
                                                                  )


if __name__ == "__main__":    
    
    try:
        
        
        
         
        update_money_flow_analyses.update_analyses(periode="D")
        
        #support_class.clear()

        #name = input("Updating moneyflow analyses, press (W)eekly or (D)daily")

        #if name.upper() == "W":
            
        #    update_money_flow_analyses.update_analyses(periode="W")
        #else:
        
         #   update_money_flow_analyses.update_analyses(periode="D")
            

        
        # additional commands
        
        #update_liquidity_impact_analyses.update_liquidity_weekly_analyses("AAIO")
    
        #database_querys.database_querys.update_analyses_liquidity(ticker_id ="BABA", periode = "W", profile= 0, profile_rate_of_change = 0, rate_of_change = 0, last = 100 )
        
        #power_stock_object.power_stock_object(stock_ticker="AAIO")

        
    except Exception as e:
        
        raise Exception("Error with tickers", e)