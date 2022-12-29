# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 11:50:15 2022

@author: Gebruiker
"""

import constants
from core_utils.database_querys import database_querys
from core_scripts.stock_data_download import power_stock_object
from core_scripts.stock_analyses import stock_analyses_with_ticker
from core_update.update_analyses import update_support

class update_liquidity_impact_analyses:
    
    @staticmethod
    def update_analyses():
        
        
        # get tickers
        tickers = database_querys.database_querys.get_all_active_tickers()
        
        # loops true tickers. 
        for ticker in tickers:
            try: 
                update_liquidity_impact_analyses.update_liquidity_weekly_analyses(ticker)
            except Exception as e:
                print("Error1 ", e )
                continue 
            
            
            
    
    @staticmethod
    def update_liquidity_weekly_analyses(ticker : str = ""):
        
        periode : str = "W"
        ticker_in : str = ticker
        analyses : str = "LIQUIDTY"
        
        try:
            
            # get data
            analyses = stock_analyses_with_ticker.update_support_functions.get_stock_analyses_with_ticker(ticker, analyses , periode )

        except Exception as e:
            
            print("Error 2", e )
            return 
        
        
        # does query.
        database_querys.database_querys.update_analyses_liquidity(ticker_id =ticker_in, 
                                                                  periode = periode, 
                                                                  profile = analyses["last_calculation_profile_indicator_number"], 
                                                                  profile_rate_of_change = analyses['last_calculation_profile_change_number'], 
                                                                  rate_of_change = 0, 
                                                                  last = int(analyses["indicator_timeserie_raw"]["Data"].tail(1)),
                                                                  last_signal = update_support.update_support_functions.get_last_signal(analyses),
                                                                  periode_since_signal= update_support.update_support_functions.get_last_signal(analyses,True) 

                                                                  
                                                                  )
        
        #ticker_id ="AAPL", periode = "W", profile= 0, profile_rate_of_change = 0, rate_of_change = 0, last = -10
        
        

if __name__ == "__main__":    
    
    try:
        
        print("START")
        update_liquidity_impact_analyses.update_analyses()
        #update_liquidity_impact_analyses.update_liquidity_weekly_analyses("AAIO")
        #database_querys.database_querys.update_analyses_liquidity(ticker_id ="BABA", periode = "W", profile= 0, profile_rate_of_change = 0, rate_of_change = 0, last = 100 )
        #power_stock_object.power_stock_object(stock_ticker="AAIO")
        print("END")
        
    except Exception as e:
        
        raise Exception("Error with tickers", e)