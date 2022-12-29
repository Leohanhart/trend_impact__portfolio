# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 11:50:15 2022

@author: Gebruiker
there is a ghost in the system. Dont know where it is but when you dont add pararmeters to function underhere the system chokes.

"""

import constants
import database_querys_main as database_querys
from core_scripts.stock_data_download import power_stock_object
import stock_analyses_with_ticker_main as stock_analyses_with_ticker
from core_update.update_analyses import update_support
import support_class
from tqdm import tqdm

class update_liquidity_impact_analyses:
    
    @staticmethod
    def update_analyses(periode = "W"):
        """
        

        Parameters
        ----------
        periode : TYPE, optional D or W
            DESCRIPTION. The default is "W".

        Returns
        -------
        None.

        """
        

        # get tickers
        tickers = database_querys.database_querys.get_all_active_tickers()
                
        # clear console.
        support_class.clear()
        
        # shows update
        print("Update liquidity analyses")
        
        # loops true tickers. 
        for ticker in tickers:
            try: 
                #with support_class.HiddenPrints():
                    
                update_liquidity_impact_analyses.update_liquidity_analyses(ticker, periode)
                
            except Exception as e:
                
                print("Error1 ", e )
                continue 
            

        
            
            
    
    @staticmethod
    def update_liquidity_analyses(ticker : str = "", periode : str = "W"):
        
        periode : str = periode
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
        
        update_liquidity_impact_analyses.update_analyses(periode="D")
        #support_class.clear()

        #name = input("Updating liquidity analyses, press (W)eekly or (D)daily")

        #if name.upper() == "W":
        #    update_liquidity_impact_analyses.update_analyses(periode="W")
        #else:
        #    update_liquidity_impact_analyses.update_analyses(periode="D")
            
            
        # overige commandos
        
        #update_liquidity_impact_analyses.update_liquidity_analyses("AAIO")
    
        #database_querys.database_querys.update_analyses_liquidity(ticker_id ="BABA", periode = "W", profile= 0, profile_rate_of_change = 0, rate_of_change = 0, last = 100 )
       
        #power_stock_object.power_stock_object(stock_ticker="AAIO")

        
    except Exception as e:
        
        raise Exception("Error with tickers", e)