# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 16:01:06 2022

@author: Gebruiker
"""

from core_scripts.stock_data_download import power_stock_object

# malisious stock
stock__A = power_stock_object.power_stock_object(stock_ticker="FRTA")

stock__B = power_stock_object.power_stock_object(stock_ticker="AAPL")

