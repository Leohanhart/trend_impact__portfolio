# -*- coding: utf-8 -*-
"""
Created on Fri May  6 13:52:54 2022

@author: Gebruiker

To do. 
- Set stockdownloading in this file. 
- set sqeduler in this file. 
- run this file in main. 
- test if this works. 
- If it works, be happy. You have created the core of this app. 
after that you add the analyses en you have won this battle.







"""

import threading
import multiprocessing
import time 
import threading

from threading import Lock
from core_utils.core_initalization import initializer_tickers


import initializer_tickers_main
import update_flows_analyses
import update_liquidity_analyses
import update_large_complex_analyses
import update_stocks_main
import update_archive

import schedule
import time

import numpy as np
import os
from datetime import datetime
import support_class
import database_querys_main

#mutex = Lock()

        
def update_tickers_weekly():
    
    #mutex.acquire()
    
    # update tickers
    
    initializer_tickers_main.initiaze_tickers()
    
    # update analyses
    
    
    update_analyses(periode="W")
    
    
    
    #mutex.release()

def update_tickers_daily():
    
    #mutex.acquire()
    
    # update tickers
    
    update_stocks_main.update_stocks.download_stockdata()
    
    # update analyses
    
    update_analyses(periode="D")
    
    #mutex.release()
    
def update_analyses(periode : str = "W"):
    """
    Updates the analsyses, 

    Parameters
    ----------
    periode : str, optional : W or D
        DESCRIPTION. The default is "W".

    Returns
    -------
    None.

    """
    
    #mutex.acquire()
    try: 
        if periode == "W":
            
            # tested, weekly/daily update works
            update_liquidity_analyses.update_liquidity_impact_analyses.update_analyses(periode=periode)
            
            # tested, weekly/daily update works
            update_flows_analyses.update_money_flow_analyses.update_analyses(periode = periode)
            
            # tested, weekly/daily update works
            update_large_complex_analyses.update_large_analyses.update_all_sector_and_industry_analyses()
            
            # updates archive, NOT tested. 
            update_archive.update_all_archives()
        
            # logs update
            data = database_querys_main.database_querys.log_item(1999, "Finnised weekly update")
            
        elif periode == "D":
            
            # checked, all paths should work.
            update_liquidity_analyses.update_liquidity_impact_analyses.update_analyses(periode=periode)
            
            # tested, weekly/daily update works
            update_flows_analyses.update_money_flow_analyses.update_analyses(periode = periode)
            
            # logs update
            data = database_querys_main.database_querys.log_item(1003, "Finnised daily update")
            
            pass
    except:
        print("problem with update")
    #mutex.release()
    
    
def heartbeat():
    
    #if mutex.locked() == True:
        
     #   return
    
    #mutex.acquire()

    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    print(current_time, " flow_impact_core is active ")
    
    data = database_querys_main.database_querys.log_item(1010, "last heartbeat")
    
    #mutex.release()
    

def update_scedual(): 
    
    print("Starting up. ")
    #if mutex.locked() == True:
    #    return
    
    #mutex.acquire()
    
    schedule.every(1).seconds.do(heartbeat)
    
    schedule.every().day.at("18:55").do(update_tickers_daily)
    # Every friday tickers get initizalized and analyses are yodated after
    schedule.every().saturday.at("01:00").do(update_tickers_weekly)   
    #schedule.every().friday.at("23:59").do(update_analyses)  
    
    
    while True:
        
        try:

             
            schedule.run_pending()
            time.sleep(0.5)
        except Exception as e:
            print(e)
            pass
            
    #mutex.release()
    
    
def start_update_scedule():
    proces_background = threading.Thread(name='daemon',target=update_scedual)
    proces_background.setDaemon(True)
    proces_background.start()
    #proces_background.join()
    

    
if __name__ == "__main__":    
    
    try:
        
        support_class.clear()
        time.sleep(5)
        

        
        name = input("Starting up Flowimpact.\n\npress (E)fficient for fast en efficient update, (A)dvanced for extended re-inializing stocks + update!\n\n")
        
        
        if name.lower() == "e":
            update_tickers_daily()
            update_analyses()
        else:
            update_tickers_weekly()
            update_analyses()
        
    except Exception as e:
        
        raise Exception("Error with tickers", e)

        