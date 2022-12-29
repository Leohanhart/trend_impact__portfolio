# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 15:07:15 2022

@author: Gebruiker
"""
import pickle
from pathlib import Path
import constants
import os

class save_and_load_temp_data_class:
    
    @staticmethod
    def save_data(data, name, extention):
        
        name_file = str(name) + "."+ extention
        full_name = os.path.join(constants.DATA_TEMP_PATH,  name_file)
        
        

        with open(full_name, 'wb') as handle:
            pickle.dump(data, handle, protocol=pickle.DEFAULT_PROTOCOL)
            
        return
    
    @staticmethod
    def load_data( name, extention):   
        name_file = str(name) + "."+ extention
        full_name = os.path.join(constants.DATA_TEMP_PATH,  name_file)
        
        try:
            
            with open(full_name, 'rb') as handle:
                data = pickle.load(handle)
                
        except ValueError:
            
            raise Exception("PICKLE_ERROR")
            
        return data
    
if __name__ == "__main__":          
    
    x = "TEST"
    print(constants.DATA_TEMP_PATH)
    save_and_load_temp_data_class.save_data(x, "DEe", "TEST")
    
    p = save_and_load_temp_data_class.load_data("DEe", "TEST")
    print(p)