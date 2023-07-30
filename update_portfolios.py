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
import service_layer_data_service as service

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
from initializer_tickers_main import InitializeTickers
import subprocess
import os
import atexit


class update_data:

    test_module: bool = False

    kill_switch: bool = False

    update_allowd: bool = False

    def __init__(self, no_action: bool = False):

        if no_action:
            return

        self.lock_file_path = "process.lock"
        atexit.register(
            self._remove_lock_file
        )  # Register a function to remove the lock file on script termination

        database_querys.database_querys.add_log_to_logbook(
            "Started applcation"
        )
        #
        self.pre_startup()
        # self.afterhour_update_cycle()
        self.start_update_schedule()

    def pre_startup(self):

        database_querys.database_querys.add_log_to_logbook(
            "Started initalizing old archive dta data"
        )
        # update archive
        first_run = initalization_file.add_data_to_archive()

        database_querys.database_querys.add_log_to_logbook(
            "Started updating trend data ..."
        )
        if first_run:
            database_querys.database_querys.add_log_to_logbook(
                "Started initalizing tickers"
            )
            InitializeTickers.initialize_all_market_data()

            database_querys.database_querys.add_log_to_logbook(
                "Started start update cycle"
            )
            self.afterhour_update_cycle()

        return

    def afterhour_update_cycle(self):

        logger.info("starting daily update cycle")

        update_stats_trend_analyses.update_kaufman_support.sleep_until(
            17, 0, 35
        )

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
            "update-cycle: Update trend anlyses"
        )

        # update archive
        update_stats_trend_analyses.update_kaufman_support.update_all_analyse_multi()

        database_querys.database_querys.add_log_to_logbook(
            "update-cycle: Update timeserie analyses analyses"
        )

        # refresh timeseries.
        timeseries.update_trend_timeseries.update()

        # Save trend analyses. #
        service.return_trend_analyses.save_all_trend_analyses()

        database_querys.database_querys.add_log_to_logbook(
            f"Generating profiles for sector"
        )
        # refresh timeserie stats.
        sector_extended_analyses = timeseries.extent_trend_analsyes()

        database_querys.database_querys.add_log_to_logbook(
            "daily update cycle ended"
        )

        # update trading portfolio

        database_querys.database_querys.add_log_to_logbook(
            "Refreshing trading portfoios"
        )
        portfolio_synch.update_trading_portfolios.startup_update()

        database_querys.database_querys.update_last_update()

        database_querys.database_querys.add_log_to_logbook(
            "Initalizing ticker"
        )

        InitializeTickers.initialize_all_market_data()

    def task_1(self):

        database_querys.database_querys.add_log_to_logbook("Started task_1")

        logger.info("starting portfolio update system")
        i = 0
        # block for a moment
        while True:

            # report a message
            try:

                update = update_portfolio_trends.kko_portfolio_update_manager()
            except Exception as e:
                print("Error in thread = ", e)
                database_querys.database_querys.add_log_to_logbook(
                    f"Error thrown in portfolio_update, task 1, {e}"
                )
                sleep(60)

    def task_2(self):

        database_querys.database_querys.add_log_to_logbook("Started task_2")

        i = 0
        # block for a moment
        while True:

            # report a message

            try:

                self.afterhour_update_cycle()

            except Exception as e:
                print("Error in thread = ", e)
                database_querys.database_querys.add_log_to_logbook(
                    f"Error thrown in portfolio_update, task 2, {e}"
                )
                sleep(60)

    def startup_data_transformation(self):
        """ """
        # function with different parameters
        database_querys.database_querys.add_log_to_logbook(
            "System that initalizes CORE threads, task_1 and task_2 is started"
        )
        logger.info("starting trend update")

        # start regular trendupdate
        thread1 = Process(target=self.task_1)

        sleep(0.5)

        # starts update portfolii manager.
        thread2 = thread_2 = Process(target=self.task_2)

        sleep(0.5)

        threads = []
        # Start the threads
        thread1.start()
        sleep(0.5)
        thread2.start()
        sleep(0.5)

        logger.info("threads started.")
        threads.append(thread1)
        threads.append(thread2)
        database_querys.database_querys.add_log_to_logbook(
            "Starting process threads Executed"
        )
        # Join the threads before
        loop: bool = True
        while loop:
            for thread in threads:
                if not thread.is_alive():

                    logger.error("Thread of update cycle faild. ")
                    thread.join()
                    self.kill_switch = True
                    loop = False
                    database_querys.database_querys.add_log_to_logbook(
                        "Large Error in Threads, ALL THREADS ARE KILLED"
                    )
                    break

        # moving further
        thread1.join()
        thread2.join()

        self.startup_data_transformation()

    def start_update_schedule(self):

        database_querys.database_querys.add_log_to_logbook(
            "System passed: Startup scedual"
        )
        if self._check_lock_file():
            database_querys.database_querys.add_log_to_logbook(
                "LockFile blocked system going nuts."
            )
            print("Another process is already running. Exiting.")
            return

        try:
            self._create_lock_file()
            subprocess.Popen(
                [
                    "python",
                    "-c",
                    "from update_portfolios import update_data; update_data().startup_data_transformation()",
                ]
            )
        except Exception as e:
            print(f"Failed to start subprocess: {e}")
            self._remove_lock_file()

    def _check_lock_file(self):
        return os.path.exists(self.lock_file_path)

    def _create_lock_file(self):
        database_querys.database_querys.add_log_to_logbook("Lock Established")
        with open(self.lock_file_path, "w") as lock_file:
            lock_file.write("Lock file")

    def _remove_lock_file(self):
        database_querys.database_querys.add_log_to_logbook("Removed Lock")
        if self._check_lock_file():
            os.remove(self.lock_file_path)

    def __del__(self):
        self._remove_lock_file()


if __name__ == "__main__":

    # archive
    try:
        x = update_data(no_action=True)
        # x.start_update_scedule()
        x.afterhour_update_cycle()
        print("LEETS GOOO")
        sleep(432000)
        # x.pre_startup()
    except Exception as e:

        raise Exception("Error with tickers", e)
