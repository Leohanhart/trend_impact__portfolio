# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 11:39:08 2022

@author: Gebruiker
"""

import constants
from core_scripts.stock_data_download import power_stock_object as stock_object
import sector_analyse
import stock_analyses_main as stock_analyses 
      

class update_support_functions(object):
    
    @staticmethod            
    def get_stock_data_with_ticker( ticker : str = "", timeframe = "D"):
        """
        Loads stockdata. Returns pandas dataframe with the stockdata.

        Parameters
        ----------
        ticker : TYPE, optional
            DESCRIPTION. The default is None.
        timeframe : TYPE, optional
            DESCRIPTION. The default is None.

        Returns
        -------
        None.

        

        05-01-2022  : Today I add that D and W data are booted seperate 
        02-03 : coppied the function from the sector-analyses class. 
        """
        
        # boots powerstockobject with the selected ticker. 
        if timeframe == "D": 
            power_object = stock_object.power_stock_object(stock_ticker = ticker, simplyfied_load = True, periode_weekly = False)
        
        # boots power stock object with weekly data.
        elif timeframe == "W":
            power_object = stock_object.power_stock_object(stock_ticker = ticker, simplyfied_load = True, periode_weekly = True)
        
        # if no reply, there must be a linking error. 
        else:
            
            raise Exception("timeframe is not avalible for ticker = ", ticker , "class : sector support functions")
            
        return power_object.stock_data
    
    @staticmethod
    def get_stock_analyses_with_ticker(ticker = None, analyeses_name = "", periode = "W"):
        """
        
        returns dict with analyses. These are the options for now analyses_names  = [ "MONEYFLOWS", "LIQUIDTY"] 
            
        Parameters
        ----------
        ticker : TYPE, optional
            DESCRIPTION. The default is None.
        analyeses_name : TYPE, optional
            DESCRIPTION. The default is "".
        periode : TYPE, optional
            DESCRIPTION. The default is "".

        RaisesC
        ------
        Exception
            DESCRIPTION.

        Returns
        -------
        dictonary : TYPE
            DESCRIPTION.

        """
        
        #sector_analyses_support_funtions = sector_analyse.sector_analyses_support_funtions()
        
        

        # grote test
       
        # checks if analyses is exsisting
        if not sector_analyse.sector_analyses_support_funtions.check_if_analyses_exist(analyeses_name):

            raise Exception("Analayses is not avalible for ticker = ", ticker , "class : sector support functions")
        
        
        # check if timeframe is alowed - addiontional function
        elif not sector_analyse.sector_analyses_support_funtions.check_if_timeframe_is_allowed(periode):
            
            raise Exception("timeframe is not avalible for ticker = ", ticker , "class : sector support functions")
            
        else:
            
            
 

          
            # sets stockdata
            stock_data = sector_analyse.sector_analyses_support_funtions.get_stock_data_with_ticker(ticker ,periode)

            # sets analyeses object
            analyses = stock_analyses.main_analyeses(stock_ticker = ticker, stock_data = stock_data, synchronize=True, timeframe=periode)
     
            # loads analayes
            try: 
                analyses.load_analyese( title_analyses = analyeses_name)
            
            except ValueError:
                
                raise ValueError
                
            # extracts the dictonary
            dictonary =  analyses.analyeses_dictionary
            
            # returns the dictornaty
            return dictonary
            
        
if __name__ == "__main__":    
    
    try:
        
        x = update_support_functions.get_stock_analyses_with_ticker(ticker= "AACG", analyeses_name = "LIQUIDTY" , periode ="W")
        print(x)
        
        
    except Exception as e:
        
        raise Exception("Error with tickers", e)

