# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 15:04:20 2022

@author: Gebruiker
"""

import initializer_db as initializer_database



if __name__ == "__main__":          
   
    try: 
        
        initializer_database.initialization()
    
    except Exception as e:
        
        
        pass 
    
    # initalize the tables. 