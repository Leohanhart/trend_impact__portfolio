
"""
Created on Thu Mar 31 14:48:20 2022

@author: Gebruiker
"""
import database_querys_main
import json
from core_scripts.stock_data_download import power_stock_object
import stock_analyses_with_ticker_main as stock_analyses_with_ticker
import datetime
import constants
from collections import ChainMap


if __name__ == "__main__":

    try:

        global x

        x = "Epmty"

    except Exception as e:

        print(e)
