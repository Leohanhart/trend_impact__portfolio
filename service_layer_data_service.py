# -*- coding: utf-8 -*-
"""
Created on Fri May  6 17:16:04 2022

@author: Gebruiker

IMPORTANT NOTES:
    
    IF YOU EVER WANT AN OTHER TYPE OF STOCK_ANALYSES_PACKAGE, REMOVE NAME FROM 
    
"""

import database_querys_main
import json
from core_scripts.stock_data_download import power_stock_object
import datetime
import constants
import service_layer_support
from core_utils.save_temp_data import save_and_load_temp_data
import sector_analyse
import pandas
import numpy as np


if __name__ == "__main__":

    # end
    #global data
    #data = support__industry__and__sector().return_all_analyses_large(string_incomming_name="Personal Services")

    try:
        global x

        x = "you are here"
        print(x)
    except Exception as e:

        print(e)

   # print(data, "this is the data")
