# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 16:57:39 2023

@author: Gebruiker
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
from loguru import logger
from multiprocessing import Process
import multiprocessing
import datetime


class update_data:

    kill_switch: bool = False

    update_allowd: bool = False

    def __init__(self):

        self.pre_startup()
        # self.start_update_scedule()

    def pre_startup(self):

        # get tickers
        tickers = database_querys.database_querys.get_all_active_tickers()

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

        # counter.
        i = 0
        # do archive update on the tickers
        while True:

            # add the tickers to a special list that updates every 24 hours.
            now = datetime.datetime.now()

            if now.hour >= 4 and now.hour < 24:

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

            else:

                update_tickers = total_items
                up_t = []
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
                        up_t.append(p)
                        p.start()

                    # wait for all threads to finish
                    for p in threads:
                        p.join()

                    upt_ = []

                    time.sleep(5)  # wait for 60 seconds before running again

            # exit criteria.
            if 0 >= len(tickers):
                break

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
