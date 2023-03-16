# -*- coding: utf-8 -*-
"""
Created on Wed Jan  4 14:53:01 2023

@author: Gebruiker

all portfolio's have certain experation criteria, these need to be managed in this file']

so - load all portfolio's check the options and do the actions.'

"""
import constants
import database_querys_main as database_querys
import stock_analyses_with_ticker_main as stock_analyses_with_ticker
from core_scripts.stock_data_download import power_stock_object as stock_object
from core_update.update_analyses import update_support
from datetime import datetime, timedelta, date
import time
import numpy as np
import pandas as pd
import os
import datetime
from pykalman import KalmanFilter
from pykalman import KalmanFilter as KF
import math
from collections import Counter
from math import sqrt
from itertools import combinations
from finquant.portfolio import build_portfolio
from finquant.efficient_frontier import EfficientFrontier
from statsmodels.tsa.vector_ar.vecm import coint_johansen
from collections import ChainMap
import uuid
import json
from time import sleep
from threading import Thread, Event
import threading
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
from concurrent.futures import wait
from concurrent.futures import FIRST_EXCEPTION
from update_portfolios_trend_strat import create_kko_portfolios, portfolio_constructor_manager, create_time_serie_with_kamalstrategie


class update_trading_portfolios:

    @staticmethod
    def startup_update():

        # get the portfolio's
        # update the portfolio's

        portfolios = database_querys.database_querys.get_trading_portfolio()

        try:

            update_trading_portfolios.update_portfolios(portfolios)

        except Exception as e:

            raise e

    @staticmethod
    def update_portfolios(portfolios):
        # extract the portfolio ID's and tickers
        for i in range(0, len(portfolios)):

            slide = portfolios.iloc[i]

            tickers = json.loads(slide.list_of_tickers)

            ticker_options = {}

            #
            for i in tickers:

                ts_data = create_time_serie_with_kamalstrategie(i)

                if ts_data == 404:

                    print("portfolio should be deleted")

                ticker_options[i] = ts_data.data

            data = update_trading_portfolios.create_data_frame_of_tickers(
                tickers=tickers, data=ticker_options)

            portfolio = portfolio_constructor_manager(data)

            add_model = add_update_trading_portfolio(
                portfolio, slide.portfolio_id)

        print(portfolios)

    @staticmethod
    def create_data_frame_of_tickers(tickers: list, data: dict):
        """

        r_data.mean(axis=1).pct_change().cumsum().plot()

        r_data.pct_change().cumsum().plot()


        Parameters
        ----------
        tickers : list
            DESCRIPTION.
        data : dict
            DESCRIPTION.

        Returns
        -------
        None.

        """

        first: bool = True
        r_data = 0
        for i in tickers:

            #
            sdata = data[i]

            # select data from dict
            df = sdata

            df = df.tail(520)
            # first column selected
            first_column = df.iloc[:, 0]

            # set to frame
            xdf = first_column.to_frame()

            # rename to ticker
            xdf = xdf.rename(columns={xdf.columns[0]: str(i)})

            if first:

                r_data = xdf
                first = False

            else:

                r_data = pd.concat([r_data, xdf], axis=1)

        return r_data


class add_update_trading_portfolio:

    model = None

    def __init__(self, portfolio, portfolio_id: str):

        model = trading_portfolio_update_model()
        # create an UUID,

        model.portfolio_id = portfolio_id
        model.portfolio_amount = int(
            len(portfolio.high_sharp_frame.ticker.to_list()))

        tickers = portfolio.high_sharp_frame.ticker.to_list()
        serialized_list_of_tickers = json.dumps(tickers)

        # set tickers
        model.list_of_tickers = serialized_list_of_tickers

        balances = portfolio.high_sharp_frame.balance.to_list()
        balances = [round(num, 2) for num in balances]

        serialized_list_balances = json.dumps(balances)

        # set balances
        model.list_of_balances = serialized_list_balances

        sides_list = []
        # set sides.
        for i in tickers:

            data = database_querys.database_querys.get_trend_kalman(i)

            trend = int(data.trend)

            sides_list.append(trend)

        serialized_list_of_sides = json.dumps(sides_list)
        model.list_of_sides = serialized_list_of_sides

        # create an
        total_expected_return = round(
            portfolio.max_sharp_y2_expected_return, 2)
        model.total_expected_return = portfolio.Imax_sharp_expected_return

        total_sharp = round(portfolio.max_sharp_y2_return, 2)
        model.total_sharp_y2 = portfolio.Imax_sharp_sharp_ratio

        model.total_volatility_y2 = portfolio.Imax_sharp_volatility

        database_querys.database_querys.update_trading_portfolio(model)

        return


class trading_portfolio_update_model():

    portfolio_id: str
    list_of_tickers: str
    list_of_balances: str
    list_of_sides: str
    total_expected_return: str
    total_sharp_y2: str
    total_volatility_y2: str


if __name__ == "__main__":

    try:

        x = update_trading_portfolios()

    except Exception as e:

        raise Exception("Database could not be created", e)
