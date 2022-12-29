# -*- coding: utf-8 -*-
"""
Created on Wed May  4 12:39:52 2022

@author: Gebruiker
"""

import sector_analyse

  
if __name__ == "__main__":    
    
    try:
        
        
        print("START")
        global test_class
        test_class = sector_analyse.sector_analyse()
        global analyses_out
        analyses_out = test_class.create_industy_or_sector_analyses(test_class.industry[7])
        print("END")
        # check if sector works. 
        # check if other analsyes works.
        
    except Exception as e:
        
        raise Exception("Error with sector analyses", e)