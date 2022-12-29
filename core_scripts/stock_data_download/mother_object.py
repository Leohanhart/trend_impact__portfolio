# -*- coding: utf-8 -*-
"""
Created on Sat Aug 14 15:37:56 2021

@author: Gebruiker
"""

from core_scripts.stock_data_download import power_stock_object,mother_object
import synch_class
from timeit import default_timer as timer
import numpy as np

# timer start. 
start= timer()

# times stocks 
times = []

# counter for the stocks. 
counter = 0

# list for stocks. 


global stocks
stocks = {}

# load the list of stocks 
global contents

with open("stocks.txt") as f:
    contents = f.readlines()
    #print(contents)

# create a dictonary for the stocks.     
for i in range(0,len(contents)):
    x = contents[i].replace("\n", "")
    stocks[x] = ""
    
print("There are" , len(stocks), " added")


    
synch_object = synch_class.data_synch(subfolder="Main_Data",ticker = "stock_tickers", data_extention = ".mother_data")


# create a synch object that saves the stocks. 
synch_object.new_data = stocks
synch_object.save_data()

global test
test = {}
test["industry"] = {}
test["sector"] = {}

for i in range(0,len(stocks)):
    

    
    # sets timer
    start_in_stock= timer()
        
    # 
    stock_ticker_in =  list(stocks.keys())[i]
    stocks_object = power_stock_object.power_stock_object(stock_ticker = stock_ticker_in, simplyfied_load = True )
    
    stocks_object.sector
    
   
    
    # checked = GOOD
    # adding the details of the ticker 
    test[stock_ticker_in] = {}
    test[stock_ticker_in]["sector"] = stocks_object.sector
    test[stock_ticker_in]["industry"] = stocks_object.industry
    
    
    # check if stock ticker alreay exsists
    if stocks_object.industry not in test.keys():
        
        test[stocks_object.industry] = {}
        test[stocks_object.industry][stock_ticker_in] = None
        #test["industry"] = {}
        test["industry"][stocks_object.industry] = None
        
    elif stocks_object.industry in test.keys():
        test[stocks_object.industry][stock_ticker_in] = None
    
    # check if stock ticker alreay exsists
    if stocks_object.sector not in test.keys():
        
        test[stocks_object.sector] = {}
        test[stocks_object.sector][stock_ticker_in] = None
        #test["sector"] = {}
        test["sector"][stocks_object.sector] = None
        
    elif stocks_object.sector in test.keys():
        test[stocks_object.sector][stock_ticker_in] = None

    #print(test)
    
    #
    # counts the stocks
    counter = counter + 1 
    
    #
    # ends main timer
    end = timer()
    # 
    # in stock timer 
    end_in_stock= timer()
    
    # time this round
    time_total = end-start
    
    amount_of_secs_per_stock = time_total/counter
    elapsted_time_this_round = end_in_stock - start_in_stock
    
    
    
    stocks_to_go = len(stocks) - counter
    percentage = round((counter/len(stocks))*100,2)
    
    print("there are ", counter, " stocks added, we have ",stocks_to_go," to go, so we are at",percentage,
          "%,\n\n", "Time that it has taken:", end-start, "the average time per stock = ", elapsted_time_this_round)
    
    print()
    synch_object = synch_class.data_synch(subfolder="Main_Data",ticker = "mother_object", data_extention = ".mother_data")

    mother_dictonary = test
    # create a synch object that saves the stocks. 
    synch_object.new_data = mother_dictonary
    synch_object.synchronized_data = mother_dictonary
    synch_object.save_data()
        
mother_dictonary = test

synch_object = synch_class.data_synch(subfolder="Main_Data",ticker = "mother_object", data_extention = ".mother_data")


# create a synch object that saves the stocks. 
synch_object.new_data = mother_dictonary
synch_object.synchronized_data = mother_dictonary
synch_object.save_data()


# stocks per sector, stocks lose with sector and things

