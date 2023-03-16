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

            sleep(4)
            database_querys.database_querys.add_log_to_logbook(
                "started trend_update in portfolio construction")
            try:

                update_stats_trend_analyses.update_kaufman_kalman_analyses.update_all()
            except:
                sleep(60)
            database_querys.database_querys.add_log_to_logbook(
                "ended trend_update in portfolio construction")

    def task_2(self):

        i = 0
        # block for a moment
        while True:
            i += 1
            sleep(.10)

            # report a message

            database_querys.database_querys.add_log_to_logbook(
                "started portfolio creation system")
            try:

                update = update_portfolio_trends.kko_portfolio_update_manager()
            except:

                sleep(60)

            database_querys.database_querys.add_log_to_logbook(
                "ended portfolio creation system")

            if self.kill_switch:
                print("GET OUT ")
                break

    def task_3(self):

        i = 0
        # block for a moment
        while True:
            i += 1
            sleep(3)
            # report a message

            database_querys.database_querys.add_log_to_logbook(
                "started trendperformance archive")
            try:
                update_stats_trend_analyses.update_kaufman_kalman_analyses.update_full_analyses()
            except:

                sleep(60)

            database_querys.database_querys.add_log_to_logbook(
                "eneded trendperformance archive")

            if self.kill_switch:
                print("GET OUT ")
                break

    def task_4(self):

        i = 0
        # block for a moment
        while True:

            print("start trading portfolio")

            sleep(8)

            try:

                portfolio_synch.update_trading_portfolios.startup_update()

            except:

                sleep(3600)

            print("Updaded trading portfolios")

    def task_5(self):

        i = 0
        # block for a moment
        while True:

            print("start trading portfolio")

            sleep(4)
            try:
                update_stats_trend_analyses.update_kaufman_kalman_analyses.update_all(
                    last_update_first=True)
            except:
                sleep(60)

            print("Updaded trading portfolios")

    def print_squares(self, thread_name, numbers):

        for number in numbers:
            print("Startup check, ", number**2)

            # Produce some delay to see the output
            sleep(1)

    def startup_data_transformation(self):
        """
        # create a new thread
        threads = []

        thread2 = threading.Thread(target=self.task_3())
        thread1 = threading.Thread(target=self.task_2())

        thread2.start()
        thread1.start()

        thread2.join()
        thread1.join()

        threads.append(thread2)
        threads.append(thread1)

        i: int = 0
        loop:  bool = True
        while loop:

            i = i + 1
            print(i, "this is Leo")
            for thread in threads:
                if not thread.is_alive():
                    print("Doden threads")

                    thread.join()
                    loop = False
                    break

            if i > 10:
                self.kill_switch = True

        """
        for i in range(0, 10):
            print("startup")
        # function with different parameters
        thread1 = threading.Thread(target=self.task,
                                   args=())

        thread2 = thread_2 = Thread(target=self.task_2)

        thread3 = threading.Thread(target=self.task_3,
                                   args=())

        thread4 = threading.Thread(target=self.task_4,
                                   args=())

        thread5 = threading.Thread(target=self.task_5,
                                   args=())
        threads = []
        # Start the threads
        thread1.start()
        thread2.start()
        thread3.start()
        thread4.start()
        thread5.start()

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

                    database_querys.database_querys.add_log_to_logbook(
                        "Thead is killed, portfolio managment has stopt.")

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

    except Exception as e:

        raise Exception("Error with tickers", e)
