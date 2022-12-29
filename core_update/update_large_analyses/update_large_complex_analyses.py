# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 20:11:07 2022

@author: Gebruiker


- Sector analyses
- Industry analyses. 
- Exchange analyses. (Both liquidity and Money floww all 3 above)

- Overview of all last industry's inflows and impact. Including profiles idividual, sub profiels. Save as DF

Needs to be overthougt about a analyses object for sectors. ( For synching the profiles)


"""

from core_scripts.stock_sector_analyses import sector_analyse
from core_utils.save_temp_data import save_and_load_temp_data
import time
class update_large_analyses:
    
    # function how saves the analyses
    # function who loads the anylyses. 
    
    @staticmethod
    def update_all_sector_and_industry_analyses():
        
        # initialize class for analyses
        # start with industry
        
        # spawns analyses class object.
        sector_and_industy_analyesses = sector_analyse.sector_analyse()
        
        # loops true sectors and fixes the thing. 
        for industry in sector_and_industy_analyesses.industry:
            # loop true analsyes
            for analyses  in sector_and_industy_analyesses.analyeses: 
                
                # holds name for industry
                industry_name_holder = industry
                # holds name for analyses
                analyses_name_holder = analyses
                print("1 ", industry ," ", analyses )
                # creates analyses
                try: 
                    analyses_out = sector_and_industy_analyesses.create_industy_or_sector_analyses(name_industry_or_sector = industry,
                                                                                                   periode="W",
                                                                                                   name_anlyeses= analyses,
                                                                                                   sub_atribute_analyses="indicator_timeserie_raw",
                                                                                                   methode = "FIT"
                                                                                                   )
                except Exception as e:
                    
                    print(str(e))
                    continue
                    
                    
                print(analyses_out.Data)
                # creates analyses name
                name_placeholder = str(industry_name_holder + "." + analyses_name_holder )
                # saves analyses
                save_and_load_temp_data.save_and_load_temp_data_class.save_data(analyses_out, name_placeholder, "LARGE_ANALYSES")
                
                
        
if __name__ == "__main__":    
    
    try:
        
        
        print("START")
        update_large_analyses.update_all_sector_and_industry_analyses()
        print("END")
        
    except Exception as e:
        
        raise Exception("Error with tickers", e)

                
                
                
                
                
                
                
                