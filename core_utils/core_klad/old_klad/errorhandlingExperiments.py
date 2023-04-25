# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 14:51:28 2022

@author: Gebruiker
"""

def raise_value_error():
    raise Exception("We are fuckt")
    
    

try:
    
    raise_value_error()
    
except ValueError:
    
    print("Value error")

except Exception as e:
    
    print("just trouble")