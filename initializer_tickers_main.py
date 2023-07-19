# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 11:58:52 2022

@author: Gebruiker

USE initizalize_ticker (NOT THE ONE ABOVE.)
"""

import constants

import pandas as pd
import sqlalchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from core_scripts.stock_data_download import power_stock_object
from core_utils.database_tables.tabels import Ticker, MarketData
from yahooquery import Ticker as TTicker

import database_querys_main
import database_connection

from tqdm import tqdm
import os
import sys
import time
import uuid
import numpy as np
import os
from time import sleep
import finnhub


class InitializeTickers:
    """
    Logbook:
        14-07-22 We ended all the bullshit over that weird library.
    """

    @classmethod
    def initialize_all_tickers(cls):

        database_connection.test_postgresql_connection()

        db_connection = database_connection.get_db_connection()

        df = pd.read_excel("tickers.xlsx")

        # Specify the columns to change the data type
        columns_to_convert = ["id", "sector", "industry", "exchange"]

        # Change the data type of selected columns to string
        df[columns_to_convert] = df[columns_to_convert].astype(str)

        # Use the session as a context manager
        with db_connection as session:
            # Loop through the DataFrame and fill the Ticker class
            for _, row in df.iterrows():
                ticker = Ticker(
                    id=row["id"],
                    sector=row["sector"],
                    industry=row["industry"],
                    exchange=row["exchange"],
                    blacklist=row["blacklist"],
                    safe=row["safe"],
                    active=row["active"],
                )
                print(row["id"])
                session.add(ticker)
                session.commit()
            # Commit the session to persist the changes

        print("tickers are loaded in")

    @classmethod
    def initialize_all_market_data(cls):
        """
        In this function, there is checked if ticker is still active,
        update the market cap, update everything, if problems

        Kalman trend will be deleted, kalman performance will be delete,
        archive will stay intact.

        Returns
        -------
        None.

        """

        tickers = database_querys_main.database_querys.get_all_active_tickers()

        finnhub_client = finnhub.Client(api_key=constants.APIKEY_FINNHUB)

        db_connection = database_connection.get_db_connection()
        with db_connection as session:
            for ticker in tickers:

                sleep(1)

                data = finnhub_client.company_profile2(symbol=ticker)

                stocks_object = power_stock_object.power_stock_object(
                    stock_ticker=ticker
                )

                if data == {} or not data:

                    if stocks_object.stock_data.empty:
                        # Get the ticker with id "AAPL" from the database
                        ticker_aapl = (
                            session.query(Ticker).filter_by(id=ticker).first()
                        )

                        # Check if the ticker exists and update its active status
                        if ticker_aapl:

                            ticker_aapl.active = False  # Set active to False for the specified ticker

                            # Commit the changes to the database
                            session.commit()

                            database_querys_main.database_querys.delete_trend_kamal()

                    else:
                        database_querys_main.database_querys.add_log_to_logbook(
                            "MaketData API mallfunctioned on ticker {ticker}"
                        )

                print(data)
                if "shareOutstanding" not in data.keys():
                    # Check if a row with the matching index_column exists
                    existing_row = (
                        session.query(MarketData)
                        .filter_by(index_column=ticker)
                        .first()
                    )

                    if existing_row:
                        session.delete(existing_row)
                try:
                    market_cap = data["shareOutstanding"]
                except:
                    continue

                real_market_shares_out = round(market_cap * 1000000, 0)
                real_market_cap = (
                    stocks_object.stock_data.Close.tail(1).mean().round()
                    * real_market_shares_out
                )

                average_volume = (
                    stocks_object.stock_data.Volume.tail(10).mean()
                    * stocks_object.stock_data.Close.tail(1).mean()
                )

                # Check if a row with the matching index_column exists
                existing_row = (
                    session.query(MarketData)
                    .filter_by(index_column=ticker)
                    .first()
                )

                if existing_row:
                    # Row exists, update its data
                    existing_row.regularMarketVolume = round(real_market_cap)
                    existing_row.marketCap = round(average_volume)

                else:
                    # Row doesn't exist, create a new one
                    new_market_data = MarketData(
                        index_column=ticker,
                        regularMarketVolume=round(real_market_cap),
                        marketCap=round(average_volume),
                    )
                    session.add(new_market_data)

                # Commit the session to persist the changes
                session.commit()


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
            session = database_connection.get_db_connection()

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

    def add_ticker_to_db(self):
        """

        Adds ticker to database with tickers

        Returns
        -------
        None.

        """

        stock = self.main_ticker

        session = database_connection.get_db_connection()

        # try:
        stocks_object = power_stock_object.power_stock_object(
            stock_ticker=stock
        )

        if not self.check_if_ticker_exsist():

            ticker = Ticker(
                id=str(stock),
                sector="ETF",
                industry="ETF",
                exchange="ETF",
                blacklist=False,
                safe=True,
                active=True,
            )
            # ticker class is added
            session.add(ticker)
            session.commit

        data = session.query(Ticker).get(stock)

        # Check if DataFrame is empty
        if stocks_object.get("stock_data").empty:
            is_empty = True

        # Check if DataFrame type is an empty string
        if (
            isinstance(stocks_object.get("stock_data"), pd.DataFrame)
            and not stocks_object.get("stock_data").columns.tolist()
        ):
            is_empty = True
        else:
            is_empty = False

        data = session.query(Ticker).get(stock)

        if is_empty:
            data.active = False

            database_querys_main.database_querys.delete_trend_kamal(stock)

            session.commit()

            session.close()

        session.close()


if __name__ == "__main__":

    try:
        pass
        # NOT DELETE: DELISTED TICKER : FRTA
        # x = initiaze_tickers()
        #
        # infile_ = initiaze_singel_ticker("AAPL")
        # print(infile_.check_if_ticker_is_capable() , "this is false or good.")
        # infile_.add_ticker_to_db()
        InitializeTickers.initialize_all_market_data()
    except Exception as e:

        raise Exception("Error with tickers", e)
