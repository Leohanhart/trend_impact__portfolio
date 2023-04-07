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

# system
from time import sleep
from threading import Thread, Event
import threading
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
from concurrent.futures import wait
from concurrent.futures import FIRST_EXCEPTION
from loguru import logger

class update_data:

    kill_switch: bool = False

    update_allowd: bool = False

    def __init__(self):

        Thread()
        self.start_update_scedule()

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
                    last_update_first=True)
            except Exception as e:
                print("Error in thread = ", e)
                sleep(60)

           


    def startup_data_transformation(self):
        """
       

        """
        # function with different parameters
        
        logger.info("starting trend update")
        # start regular trendupdate
        thread1 = threading.Thread(target=self.task,
                                   args=())
        
        logger.info("starting portfolio creation")
        # starts update portfolii manager. 
        thread2 = thread_2 = Thread(target=self.task_2)
        
        logger.info("starting up archive")
        # starts archive kaufman
        thread3 = threading.Thread(target=self.task_3,
                                   args=())
        
        logger.info("starting hourly update trading portfolio")
        # start update trading portfolio.
        thread4 = threading.Thread(target=self.task_4,
                                   args=())
        
        logger.info("starting up trendupdate revers.")
        # start regulare trend update reverse. 
        thread5 = threading.Thread(target=self.task_5,
                                   args=())
        threads = []
        # Start the threads
        thread1.start()
        thread2.start()
        thread3.start()
        thread4.start()
        thread5.start()
        
        logger.info("threads started.")
        threads.append(thread1)
        threads.append(thread2)
        threads.append(thread3)
        threads.append(thread4)
        threads.append(thread5)

        # Join the threads before
        loop:  bool = True
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

        self.startup_data_transformation()

    def start_update_scedule(self):

        print(0.1)

        database_querys.database_querys.add_log_to_logbook(
            "Started update data_transformation.")

        proces_background = threading.Thread(
            name='daemon_dtf', target=self.startup_data_transformation)
        proces_background.setDaemon(True)
        proces_background.start()
        # proces_background.join()


if __name__ == "__main__":

    # archive
    try:
        x = update_data()
        x.start_update_scedule()
        sleep(2000)

    except Exception as e:

        raise Exception("Error with tickers", e)
