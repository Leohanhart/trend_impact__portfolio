# -*- coding: utf-8 -*-
"""
Created on Fri May  6 13:25:11 2022

@author: Gebruiker
"""

import schedule
import time
 
def function_test():
    print("test")
# Functions setup
def download_and_refresh():
    print("Get ready for Sudo Placement at Geeksforgeeks")
 

schedule.every(10).seconds.do(function_test)

schedule.every().friday
 
# Every tuesday at 18:00 sudo_placement() is called
schedule.every().monday.at("23:59").do(download_and_refresh)
 
# Loop so that the scheduling task
# keeps on running all time.
while True:
 
    # Checks whether a scheduled task
    # is pending to run or not
    schedule.run_pending()
    time.sleep(1)
    

