# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 11:58:52 2022

@author: Gebruiker

USE initizalize_ticker (NOT THE ONE ABOVE.)
"""

import constants


import sqlalchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from core_scripts.stock_data_download import power_stock_object
from core_utils.database_tables.tabels import Ticker
from yahooquery import Ticker as TTicker

import database_querys_main

from tqdm import tqdm
import os
import sys
import time
import uuid
import numpy as np
import os
from time import sleep

db_dir = "core_data/flowimpact_api_db.db"
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.abspath(db_dir)

db_path = SQLALCHEMY_DATABASE_URI
engine = create_engine(db_path, echo=False)
Session = sessionmaker(bind=engine)
session = Session()


class initialization:

    # the list for the tickers.
    tickers: list = []

    def __init__(self, load_tickers_only: bool = False):
        """

        /Dont use this function

        Parameters
        ----------
        load_tickers_only : bool, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        #
        pass

        stocks = initialization_support.load_tickers_txt()

        # check tickers
        if load_tickers_only:

            self.tickers = stocks

            return self.tickers

        # setting up db stream

        db_dir = "core_data/flowimpact_api_db.db"
        SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.abspath(db_dir)

        db_path = SQLALCHEMY_DATABASE_URI
        engine = create_engine(db_path, echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()

        # loop true the tickers, add to DB
        for i in range(0, len(stocks)):

            db_dir = "core_data/flowimpact_api_db.db"
            SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.abspath(db_dir)

            db_path = SQLALCHEMY_DATABASE_URI
            engine = create_engine(db_path, echo=False)
            Session = sessionmaker(bind=engine)
            session = Session()

            #
            stock_ticker_in = list(stocks.keys())[i]

            print(stock_ticker_in)

            # getting the stock object
            stocks_object = power_stock_object.power_stock_object(
                stock_ticker=stock_ticker_in
            )

            # testing if stock is: A, valide. B, still active. C, delisted
            status_stock = initialization_support.check_if_ticker_valide(
                stocks_object
            )

            # query for DB
            data = session.query(Ticker).get(stock_ticker_in)

            #
            # checks if the location exsists, if yes, action.
            if data == None:

                if stocks_object.sector == None or stocks_object:
                    continue
                # option 1, Ticker is active

                ticker = Ticker(
                    id=stock_ticker_in,
                    sector=stocks_object.sector,
                    industry=stocks_object.industry,
                    exchange=stocks_object.all_stock_data["exchange"],
                    active=True,
                )

                session.add(ticker)
                session.commit()

            else:

                if stocks_object.sector == None:

                    # Ticker = unit_tests_and_errors(id = location, error = error, error_code = message)

                    data.active = False

                    session.commit()

            session.close()


class initialization_support:
    @staticmethod
    def check_if_ticker_valide(stocks_object: object = None):
        """
        Checks if ticker is valide, meaning: workable data, sector and industy and that stock is not delisted

        first check are based on invalide/mallefide, if error occures it will be because dataframe is loaded
        correctly, that's why if the exception is thrown this will result in a positive signal(return tru).

        Parameters
        ----------
        stocks_object : object, optional
            DESCRIPTION. The default is None.

        Returns
        -------
        bool
            DESCRIPTION.

        """
        return True
        try:

            if (
                not stocks_object.sector
                or stocks_object.stock_data == None
                or type(stocks_object.stock_data) == None
                or stocks_object.stock_data is None
            ):
                return False
            else:
                return True

        except Exception as e:

            return True

    @staticmethod
    def load_tickers_txt():
        """

        Loads stocks from the txt file.

        Returns
        -------
        stocks : DICT

            DESCRIPTION.

        """
        stocks = {}

        path_tickers = constants.TICKER_DATA___PATH

        path_file = os.path.join(path_tickers, "stocks.txt")

        with open(path_file) as f:
            contents = f.readlines()
            # print(contents)

            # create a dictonary for the stocks.
        for i in range(0, len(contents)):
            x = contents[i].replace("\n", "")
            stocks[x] = ""

        return stocks

    @staticmethod
    def speed_limiter(
        start_time: float = 0, end_time: float = 0, limiter: float = 2.6
    ):
        """
        Speedlimiter calculates additional time and sleeps in the meanwhile.

        Used when a function needs to be speedlimit doe to api restrictions.

        what happens is that the function calclulatse the passet time and sleeps the additional time so

        te speedlimiter will not be upset.

        Parameters
        ----------
        start_time : float, optional
            DESCRIPTION. The default is 0.
        end_time : float, optional
            DESCRIPTION. The default is 0.
        limiter : TYPE, optional
            DESCRIPTION. The default is 2.6.

        Returns
        -------
        None.

        """

        # print(start_time, end_time)

        # sets seconds past
        time_past = end_time - start_time

        # print(time_past)

        # subtracts the limit time
        additional_time = limiter - time_past

        # if additional time is larger than
        if additional_time > 0:

            # print("this is the total sleep time", additional_time )

            # time.sleep(additional_time)

            return additional_time

        else:

            print("No time to sleep")

            return 0.0001

    @staticmethod
    def load_malfunctioning_ticker():
        pass


class initiaze_tickers:
    """
    Logbook:
        14-07-22 We ended all the bullshit over that wird library.
    """

    def __init__(self):

        stocks_object = 0

        stocks = initialization_support.load_tickers_txt()

        stocks = list(stocks)

        start_time = time.time()
        end_time = time.time()

        for stock in stocks:

            sleep(1)

            try:

                initiaze_singel_ticker(stock_ticker=stock, auto_modus=True)

            except Exception as e:

                print("Error ")

                pass


class initiaze_singel_ticker:
    """
        Usage: add the ticker with initaliation.

    if you want more checks. Add in check if ticker is capble.

    """

    # main ticker
    main_ticker: str = None
    # main error
    main_error_status: str = None

    def __init__(self, stock_ticker: str = None, auto_modus: bool = True):
        """


        Parameters
        ----------
        stock_ticker : str, optional
            DESCRIPTION. The default is None.
        auto_modus : bool, optional

            DESCRIPTION. If you turn on auto modus. Ticker is inizalized. If new and oke, its added, if exsists conaining error
            it will be removed.

        Returns
        -------
        None.

        """

        self.main_ticker = stock_ticker

        if auto_modus:

            try:
                self.add_ticker_to_db()
            except:
                self.delete_ticker_from_db()

    def check_if_ticker_is_capable(self):
        """

        Function created to add stock, create stock or check if the stock is valide/ and in case if not, delete the stock from the system.

        Parameters
        ----------
        ticker_name : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """

        # sets the ticker.
        stock = self.main_ticker

        try:

            # global stocks_object

            # try:
            stocks_object = power_stock_object.power_stock_object(
                stock_ticker=stock
            )

            # addiitional checks if exsists.
            if len(stocks_object.stock_data.index) == 0:
                return False

            # testing if stock is: A, valide. B, still active. C, delisted
            status_stock = initialization_support.check_if_ticker_valide(
                stocks_object
            )

            # tries to run all functions.
            """
            
            3 types of stocks.
            1. Has sector, industry, timeseries, exchange
            2. Has industry, timeseries,
            3. is totally invlaide. 
            
            - Invalides have no timeserie. 
            
            There must be a check that or assigns the db vars with the value, otherwise NA. 
            
            
            
            """
            # check if sector is legid
            if not stocks_object.sector:

                sector_in = "NA"

            else:

                sector_in = stocks_object.sector

            # check if industry is legid
            if not stocks_object.industry:

                industry_in = "NA"

            else:

                industry_in = stocks_object.industry

            # check if stockexchange is legid.
            if not stocks_object.all_stock_data == False:

                exchange_in = "NA"

            else:

                exchange_in = stocks_object.all_stock_data["exchange"]

            # tries manipulation on time serie, if fails, problem with time serie, stock is inactive.
            if sector_in != "NA":

                return True
            else:

                return False

        except:

            raise ValueError

    def check_if_ticker_exsist(self):
        """
        Check if ticker exsists in system.

        Returns
        -------
        True if ticker exsists.
        False if ticker is new.

        """
        try:
            # setting up the database
            db_dir = "core_data/flowimpact_api_db.db"
            SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.abspath(db_dir)

            db_path = SQLALCHEMY_DATABASE_URI
            engine = create_engine(db_path, echo=False)
            Session = sessionmaker(bind=engine)
            session = Session()

            stock = self.main_ticker
            data = session.query(Ticker).get(stock)

            session.close()

            # check if data is new.
            if data == None:

                return False

            else:

                return True

        except Exception as e:

            print("Error ")

            pass

    def delete_ticker_from_db(self):
        """

        Deletes ticker from db.

        Returns
        -------
        None.

        """

    def add_ticker_to_db(self):
        """

        Adds ticker to database with tickers

        Returns
        -------
        None.

        """

        stock = self.main_ticker
        try:

            # setting up the database
            db_dir = "core_data/flowimpact_api_db.db"
            SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.abspath(db_dir)

            db_path = SQLALCHEMY_DATABASE_URI
            engine = create_engine(db_path, echo=False)

            Session = sessionmaker(bind=engine)
            session = Session()

            # try:
            stocks_object = power_stock_object.power_stock_object(
                stock_ticker=stock
            )

            # testing if stock is: A, valide. B, still active. C, delisted
            # status_stock = initialization_support.check_if_ticker_valide(
            #    stocks_object)

            data = session.query(Ticker).get(stock)

            stock_ = TTicker(stock)

            if type(stock_.asset_profile[stock]) == str:

                data.active = False

                database_querys_main.database_querys.delete_trend_kamal(stock)

                session.commit()

                session.close()

                return

            NotEquiy: bool = False

            if stock_.quote_type[stock]["quoteType"] != "EQUITY":
                # check if data is new.
                if data == None:
                    # print("stock is added")
                    # if data is new, ticker is added, in_ data is inserted. if single var fails, rest is added anyway.
                    ticker = Ticker(
                        id=str(stock),
                        sector="ETF",
                        industry="ETF",
                        exchange="ETF",
                        active=True,
                    )
                    # ticker class is added
                    session.add(ticker)
                    # ticker class is commited.
                    session.commit()

                    session.close()

                    return

                # if ticker already exsist there is only one var that's need to be maintained. The active var.
                else:
                    # print("stock is re-added")

                    # sets bool
                    data.active = True

                    # commits.
                    session.commit()

                    session.close()

                    return

            # tries to run all functions.
            """
            
            3 types of stocks.
            1. Has sector, industry, timeseries, exchange
            2. Has industry, timeseries,
            3. is totally invlaide. 
            
            - Invalides have no timeserie. 
            
            There must be a check that or assigns the db vars with the value, otherwise NA. 
            
            
            
            """
            # check if sector is legid
            if not stocks_object.sector:

                sector_in = stock_.asset_profile[stock]["sector"]

            else:

                sector_in = stocks_object.sector

            # check if industry is legid
            if not stocks_object.industry:

                industry_in = stock_.asset_profile[stock]["industry"]

            else:

                industry_in = stocks_object.industry

            # check if stockexchange is legid.
            if not stocks_object.all_stock_data == False:

                try:
                    exchange_in = stock_.quote_type[stock]["exchange"]
                except:
                    exchange_in = "NA"
            else:

                exchange_in = stocks_object.all_stock_data["exchange"]

            # tries manipulation on time serie, if fails, problem with time serie, stock is inactive.
            if self.check_if_ticker_is_capable():
                active_in = True
            else:

                active_in = False

                database_querys_main.database_querys.delete_trend_kamal(stock)

            # check if data is new.
            if data == None:

                # if data is new, ticker is added, in_ data is inserted. if single var fails, rest is added anyway.
                ticker = Ticker(
                    id=str(stock),
                    sector=sector_in,
                    industry=industry_in,
                    exchange=exchange_in,
                    active=active_in,
                )
                # ticker class is added
                session.add(ticker)
                # ticker class is commited.
                session.commit()

                session.close()
                return

            # if ticker already exsist there is only one var that's need to be maintained. The active var.
            else:
                # print("stock is added")

                # sets bool
                data.active = active_in
                data.sector = stock_.asset_profile[stock]["sector"]
                data.industry = stock_.asset_profile[stock]["industry"]
                data.exchange_in = stock_.asset_profile[stock]["exchange"]
                # commits.
                session.commit()

            session.close()

        except Exception as e:

            return
            print("Error in inizaliation", e)


if __name__ == "__main__":

    try:
        # NOT DELETE: DELISTED TICKER : FRTA
        # x = initiaze_tickers()
        #
        infile_ = initiaze_singel_ticker("XLF")
        # print(infile_.check_if_ticker_is_capable() , "this is false or good.")
        # infile_.add_ticker_to_db()

    except Exception as e:

        raise Exception("Error with tickers", e)
