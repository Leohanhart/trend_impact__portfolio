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
from datetime import datetime

import threading
import multiprocessing
import time
import threading

from threading import Lock
from core_utils.core_initalization import initializer_tickers

import startup_support as support

import initializer_tickers_main
import update_stocks_main

import update_portfolios_trend_strat as update_trend_kalman
import update_trend_analyses
import portfolio_synchronization

import schedule
import time

import numpy as np
import os
from datetime import datetime

import support_class
import database_querys_main

#mutex = Lock()


def update_tickers_weekly():

    # mutex.acquire()

    # update tickers

    initializer_tickers_main.initiaze_tickers()

    # update analyses

    update_analyses(periode="W")

    # mutex.release()


def update_complex_operations():

    # updates archive.
    proces_background = threading.Thread(
        name='daemon_complex_operations', target=update_trend_analyses.update_kaufman_kalman_analyses.update_full_analyses()
    )

    proces_background.start()
    proces_background.join()
    update = update_trend_kalman.update_trend_kamal_portfolio_selection()
    return


def update_operation():
    """
    Updates every business day. 

    Returns
    -------
    None.

    """

    update_trend_analyses.update_kaufman_kalman_analyses.update_all()

    update = portfolio_synchronization.update_trading_portfolios.update_trading_portfolios()

    return


def update_tickers_daily():

    # mutex.acquire()

    # update tickers

    update_stocks_main.update_stocks.download_stockdata()

    # update analyses daily
    if support.check_if_today_is_businessday():

        # start operations
        proces_background = threading.Thread(
            name='daemon_operations', target=update_operation)

        proces_background.setDaemon(True)
        proces_background.start()

    # if today is first of the month.
    if support.check_if_today_is_first_the_month():

        proces_background = threading.Thread(
            name='daemon_complex_operations', target=update_operation)

        proces_background.setDaemon(True)
        proces_background.start()

    update_analyses(periode="D")

    # mutex.release()


def update_analyses(periode: str = "W"):
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

    # mutex.acquire()
    try:
        if periode == "W":

            # logs update
            data = database_querys_main.database_querys.log_item(
                1999, "Finnised weekly update")

        elif periode == "D":

            # logs update
            data = database_querys_main.database_querys.log_item(
                1003, "Finnised daily update")

    except:
        print("problem with update")
    # mutex.release()


def heartbeat():

    # if mutex.locked() == True:

    #   return

    # mutex.acquire()

    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    print(current_time, " trendimpact_core is active ")

    # mutex.release()


def update_scedual():

    print("Starting up.")
    # if mutex.locked() == True:
    #    return

    # mutex.acquire()

    schedule.every(1).seconds.do(heartbeat)

    schedule.every().day.at("18:55").do(update_tickers_daily)
    # Every friday tickers get initizalized and analyses are yodated after

    schedule.every().saturday.at("01:00").do(update_tickers_weekly)

    # schedule.every().friday.at("23:59").do(update_analyses)

    while True:

        try:

            schedule.run_pending()
            time.sleep(0.5)
        except Exception as e:
            print(e)
            pass

    # mutex.release()


def start_update_scedule():
    proces_background = threading.Thread(name='daemon', target=update_scedual)
    proces_background.setDaemon(True)
    proces_background.start()
    # proces_background.join()


if __name__ == "__main__":

    try:

        support_class.clear()
        time.sleep(5)

        name = input(
            "Starting up s Flowimpact.\n\npress (E)fficient for fast en efficient update, (A)dvanced for extended re-inializing stocks + update!\n\n")

        if name.lower() == "e":
            update_tickers_daily()
            update_analyses()
        else:
            update_tickers_weekly()
            update_analyses()

    except Exception as e:

        raise Exception("Error with tickers", e)
