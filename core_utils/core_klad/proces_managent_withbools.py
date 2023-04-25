# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 11:01:06 2023

@author: Gebruiker
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 16:57:39 2023

@author: Gebruiker



goals, create sequence, if three is not finnished wait. Possibly good with states. 

pre-started-stoped-finnished,


"""

# other objects.
import update_portfolios_trend_strat as update_portfolio_trends
import update_trend_analyses as update_stats_trend_analyses
import database_querys_main as database_querys
import portfolio_synchronization as portfolio_synch

# system
from time import sleep
from threading import Thread, Event
from multiprocessing import Process
import threading

from loguru import logger
from multiprocessing import Process


class update_data:

    kill_switch: bool = False

    update_allowd: bool = False

    proces_stage_1_finnised: bool = False
    proces_stage_2_finnised: bool = False

    def __init__(self):

        self.start_update_scedule()

    def task(self):

        i = 0
        print("started task")
        # block for a moment
        while True:

            try:

                print("task 1")
            except Exception as e:
                print("Error in thread = ", e)

            finally:

                i += 1
                sleep(5)

            print(i, "we are here ")
            if i > 3:
                print("increment I ")
                self.proces_stage_1_finnised = True

    def task_2(self):

        i = 0
        sleep(49)
        # block for a moment
        while True:

            while self.proces_stage_1_finnised == False:
                print("Waiting for thread to free")
                sleep(3)

            try:

                print("task 2")
            except Exception as e:
                print("Error in thread = ", e)

                sleep(60)

    def task_3(self):

        i = 0
        # block for a moment
        while True:

            try:

                print("task 3")
            except Exception as e:
                print("Error in thread = ", e)

                sleep(60)

    def task_4(self):

        i = 0
        # block for a moment
        while True:

            try:

                print("task 4")
            except Exception as e:
                print("Error in thread =  ", e)

                sleep(60)

    def task_5(self):

        i = 0
        # block for a moment
        while True:

            try:

                print("task 5")
            except Exception as e:
                print("Error in thread = ", e)

                sleep(60)

    def task_6(self):

        i = 0
        # block for a moment
        while True:

            try:

                print("task 6")
            except Exception as e:
                print("Error in thread = ", e)

                sleep(60)

    def startup_data_transformation(self):
        """ """
        # function with different parameters

        logger.info("starting test")

        # start regular trendupdate
        thread1 = Process(target=self.task_3)

        # starts update portfolii manager.
        thread2 = thread_2 = Process(target=self.task_3)

        # starts archive kaufman
        thread3 = Process(target=self.task_3, args=())

        # start update trading portfolio.
        thread4 = Process(target=self.task_4, args=())

        # start regulare trend update reverse.
        thread5 = Process(target=self.task_5, args=())

        # start regulare trend update reverse.
        thread6 = Process(target=self.task_6, args=())

        threads = []
        # Start the threads
        thread1.start()
        sleep(2.5)
        thread2.start()
        sleep(0.5)

        logger.info("threads started.")
        threads.append(thread1)
        threads.append(thread2)

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
        x.start_update_scedule()
        sleep(2000)

    except Exception as e:

        raise Exception("Error with tickers", e)
