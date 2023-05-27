# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 16:57:39 2023

@author: Gebruiker

Tasks,
- fill in the github act.

Note, we have added a startup_task. This one will (verymuch depending on how much data is already in the 
                                                   database)
take 9 hours, untill probably 4 weeks or so. I will target it on 9 hours. 
Not there are many tasks, for example 
- archive 
- update portfolios 
- update trading portfolios
- update trends 
- update portfolio revers. 
- update timeseries. 

We have upgraded trends so it will always update archive aswell, this still needs to be tested. 
So potentally this thead ( including the archive and reverse archive can be stoped. and put on a time slot)
# 
IDEAL we have 1 thead proces that starts at market close, updates all trends (this can also be done in reverse)
-- we could also implement that archive updates always updates the trend but this might confuse
-- also updating trends can be done in the loop done in the startup_thread, this goes very fast. 
this will take up to 6-9 hours. We need to create a function that downloads all stocks for the next hit while we are waiting. 

Afther that the update_timeseries needs to run, its unclear howmuch this will take when this whole 
sytem already ren on time but It will take up some hours ( I think about 4-12 but im not sure 6.5)
otherwise its about 1 minut. Then we need to update the trading portfolio's

Afther that, the system needs to sleep untill 6 oclock in the evening and the whole cycle restarts. 
- We need a DB -table that keeps track of the stages.
- We need a DB -table that keeps track of the last update. 
If this runs we 

So mainly, if we would take this chance, we only need two threads and the server is stable on its own. 




"""

# other objects.
import update_portfolios_trend_strat as update_portfolio_trends
import update_trend_analyses as update_stats_trend_analyses
import database_querys_main as database_querys
import portfolio_synchronization as portfolio_synch
import update_trend_time_series as timeseries

# system
from time import sleep
from threading import Thread, Event
from multiprocessing import Process
import threading
import time
import concurrent.futures
import datetime
import time
from loguru import logger
import multiprocessing
import datetime
import initalization_file


class update_data:

    kill_switch: bool = False

    update_allowd: bool = False

    def __init__(self):

        self.afterhour_update_cycle()
        # self.pre_startup()
        # self.start_update_scedule()

    def pre_startup(self):

        # update archive
        initalization_file.add_data_to_archive()

        # get tickers
        tickers = database_querys.database_querys.get_all_active_tickers()

        #
        tickers.reverse()

        # list for updated tickers
        tickers_that_are_updated = []

        # update function
        update_function = (
            update_stats_trend_analyses.update_kaufman_support.update_all_analyses_with_ticker
        )

        update_trend = (
            update_stats_trend_analyses.update_kaufman_support.update_all_trends_with_ticker
        )

        # lists
        total_items = []

        daily_procedure_run_q = False

        # counter.
        i = 0
        # do archive update on the tickers
        while True:

            # add the tickers to a special list that updates every 24 hours.
            now = datetime.datetime.now()

            """            
            if datetime.time(23, 0) <= now <= datetime.time(23, 15):
                # Do phase 1 for 15 minutes starting at 11pm
                print("Phase 1: starting at 11pm...")
                time.sleep(15 * 60)  # Sleep for 15 minutes
            elif datetime.time(23, 15) < now <= datetime.time(0, 15):
                # Do phase 2 for 60 minutes after phase 1
                print("Phase 2: starting after phase 1...")
                time.sleep(60 * 60)  # Sleep for 60 minutes
            else:
                # Do phas
            """
            if datetime.time(23, 0) <= now <= datetime.time(23, 15):
                # Do phase 1 for 15 minutes starting at 11pm
                daily_procedure_run_q = False
                time.sleep(60)  # Sleep for 15 minutes

            elif datetime.time(23, 15) < now <= datetime.time(0, 15):
                # Do phase 2 for 60 minutes after phase 1
                if not daily_procedure_run_q:

                    update_tickers = total_items.copy()
                    up_t = []
                    threads = []
                    while True:
                        try:
                            for i in range(5):
                                item = update_tickers.pop()
                                up_t.append(item)

                        except IndexError:
                            break

                        # start each thread with the function and its argument
                        for ticker in up_t:
                            p = Process(target=update_function, args=(ticker,))
                            threads.append(p)
                            p.start()

                        # wait for all threads to finish
                        for p in threads:
                            p.join()

                        threads = []
                        up_t = []

                        time.sleep(
                            5
                        )  # wait for 60 seconds before running again

                        daily_procedure_run_q = True
                else:
                    sleep(60)

            else:

                tickers_for_loop = []

                # Remove 5 items from the original list and append them to the new list
                try:
                    for i in range(10):
                        item = tickers.pop()
                        tickers_for_loop.append(item)
                        total_items.append(item)
                except IndexError:
                    break

                # create a list to hold the threads
                threads = []

                # start each thread with the function and its argument
                for ticker in tickers_for_loop:
                    print(f"update {ticker}")
                    p = Process(target=update_function, args=(ticker,))
                    threads.append(p)
                    p.start()

                # wait for all threads to finish
                for p in threads:
                    p.join()

                threads = []

                time.sleep(5)  # wait for 60 seconds before running again

                tickers_for_loop = []

            # exit criteria.
            if 0 >= len(tickers):
                break

        self.start_update_scedule()

    def afterhour_update_cycle(self):

        # started
        database_querys.database_querys.add_log_to_logbook(
            "daily update cycle started"
        )

        database_querys.database_querys.add_log_to_logbook(
            "update-cycle: Update tickers"
        )

        # download en maintenance
        # update_stats_trend_analyses.update_kaufman_support.update_all_tickers()

        database_querys.database_querys.add_log_to_logbook(
            "update-cycle: Update update anlyses"
        )

        # update archive
        update_stats_trend_analyses.update_kaufman_support.update_all_analyse_multi()

        database_querys.database_querys.add_log_to_logbook(
            "update-cycle: Update analyses"
        )

        # refresh timeseries.
        timeseries.update_trend_timeseries.update()

        # refresh timeserie stats.
        sector_extended_analyses = timeseries.extent_trend_analsyes()

        database_querys.database_querys.add_log_to_logbook(
            "daily update cycle ended"
        )

        # update trading portfolio
        portfolio_synch.update_trading_portfolios.startup_update()

        update_stats_trend_analyses.update_kaufman_support.sleep_until_time(
            17, 0, 10
        )

    def task(self):

        i = 0
        # block for a moment
        while True:

            try:

                update_stats_trend_analyses.update_kaufman_kalman_analyses.update_all()
            except Exception as e:
                print("Error in thread = ", e)

                sleep(60)

    def task_2(self):

        i = 0
        # block for a moment
        while True:

            # report a message
            try:

                update = update_portfolio_trends.kko_portfolio_update_manager()
            except Exception as e:
                print("Error in thread = ", e)
                sleep(60)

    def task_3(self):

        i = 0
        # block for a moment
        while True:

            # report a message

            try:

                update_stats_trend_analyses.update_kaufman_kalman_analyses.update_full_analyses()
                sleep(5)
            except Exception as e:
                print("Error in thread = ", e)

                sleep(60)

    def task_4(self):

        i = 0
        # block for a moment
        while True:

            try:

                portfolio_synch.update_trading_portfolios.startup_update()

            except Exception as e:

                print("Error in thread = ", e)

                sleep(3600)

    def task_5(self):

        i = 0

        # block for a moment
        while True:

            try:

                update_stats_trend_analyses.update_kaufman_kalman_analyses.update_all(
                    last_update_first=True
                )
            except Exception as e:
                print("Error in thread = ", e)
                sleep(60)

    def task_6(self):

        logger.info("starting task 6")
        i = 0
        # funtion always sleeps one day before the start.
        sleep(86000)
        # block for a moment
        while True:

            now = datetime.datetime.now()

            # Set the target date to tomorrow at midnight
            target_date = datetime.datetime(now.year, now.month, now.day + 1)

            # Loop until the target date is reached
            while datetime.datetime.now() < target_date:
                # Sleep for one second
                time.sleep(10)

            try:

                timeseries.update_trend_timeseries.update()

            except Exception as e:
                print("Error in thread = ", e)
                sleep(60)

    def startup_data_transformation(self):
        """ """
        # function with different parameters

        logger.info("starting trend update")

        # start regular trendupdate
        thread1 = Process(target=self.task, args=())

        sleep(0.5)

        logger.info("starting portfolio creation")
        # starts update portfolii manager.
        thread2 = thread_2 = Process(target=self.task_2)

        sleep(0.5)

        logger.info("starting up archive")
        # starts archive kaufman
        thread3 = Process(target=self.task_3, args=())

        sleep(0.5)

        logger.info("starting hourly update trading portfolio")
        # start update trading portfolio.
        thread4 = Process(target=self.task_4, args=())
        sleep(0.5)

        logger.info("starting up trendupdate revers.")
        # start regulare trend update reverse.
        thread5 = Process(target=self.task_5, args=())

        logger.info("starting up date timeseries..")
        # start regulare trend update reverse.
        thread6 = Process(target=self.task_6, args=())

        threads = []
        # Start the threads
        thread1.start()
        sleep(0.5)
        thread2.start()
        sleep(0.5)
        thread3.start()
        sleep(0.5)
        thread4.start()
        sleep(0.5)
        thread5.start()
        sleep(0.5)
        thread6.start()

        logger.info("threads started.")
        threads.append(thread1)
        threads.append(thread2)
        threads.append(thread3)
        threads.append(thread4)
        threads.append(thread5)
        threads.append(thread6)

        # Join the threads before
        loop: bool = True
        while loop:
            for thread in threads:
                if not thread.is_alive():

                    logger.error("Thread of update cycle faild. ")
                    thread.join()
                    self.kill_switch = True
                    loop = False
                    break

        # moving further
        thread1.join()
        thread2.join()
        thread3.join()
        thread4.join()
        thread5.join()
        thread6.join()

        self.startup_data_transformation()

    def start_update_scedule(self):

        print(0.1)

        database_querys.database_querys.add_log_to_logbook(
            "Started update data_transformation."
        )

        proces_background = threading.Thread(
            name="daemon_dtf", target=self.startup_data_transformation
        )
        proces_background.setDaemon(True)
        proces_background.start()
        # proces_background.join()


if __name__ == "__main__":

    # archive
    try:
        x = update_data()
        # x.start_update_scedule()
        # sleep(86000)
        x.pre_startup()
    except Exception as e:

        raise Exception("Error with tickers", e)
