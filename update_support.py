# -*- coding: utf-8 -*-
"""
Created on Tue May  3 11:11:41 2022

@author: Gebruiker
"""


class update_support_functions(object):
    
    # find last profile.
    
    @staticmethod
    def get_last_signal(incomming_data : dict = [], periode = False):
        
        # retreive the data
        data = incomming_data["indicator_timeserie_profile"]
        
        # values extracten, flippen ( of andersom eerste waarde vinden)
        # flip 
        data = data.iloc[::-1]
        
        # vars get them 
        data_vars = data.Data.values
        
        last_value = 0
        itterations = 0 
        
        # loop true 
        for data in data_vars:
            
            # add itteration
            itterations = itterations + 1
            
            # if data is not equal to 0 than that's first datapoint
            if data != 0:
                
                # sets last value
                last_value = data
                
                break
            
        # if periode is true return amount of ittterations
        if periode:
            
            return int(itterations)
        
        # else return last value        
        else:
            
            return int(last_value)
        
        

    # with option return amount of days.