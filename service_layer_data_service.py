# -*- coding: utf-8 -*-
"""
Created on Fri May  6 17:16:04 2022

@author: Gebruiker

IMPORTANT NOTES:
    
    IF YOU EVER WANT AN OTHER TYPE OF STOCK_ANALYSES_PACKAGE, REMOVE NAME FROM 
    
"""

import database_querys_main
import json
from core_scripts.stock_data_download import power_stock_object
import datetime
import constants
import service_layer_support
from core_utils.save_temp_data import save_and_load_temp_data
import pandas
import numpy as np


class return_trend_analyses(object):

    @staticmethod
    def get_trend_analyses(ticker: str):
        """
        returns trend data. 

        Parameters
        ----------
        ticker : str
            DESCRIPTION.

        Returns
        -------
        res : TYPE
            DESCRIPTION.

        """
        data = database_querys_main.database_querys.get_trend_kalman(ticker)

        res = trend_analyse_support.package_data(data)

        return res

    @staticmethod
    def get_trend_archive_analyses(ticker: str):
        """
        returns trend data. 

        Parameters
        ----------
        ticker : str
            DESCRIPTION.

        Returns
        -------
        res : TYPE
            DESCRIPTION.

        """

        data = database_querys_main.database_querys.get_trend_kalman_performance(
            ticker)

        res_data = trend_analyse_support.package_data(data)

        return res_data

    @staticmethod
    def get_all_trend_specs():

        data = database_querys_main.database_querys.get_all_trend_kalman()

        res_data = analyses_support.return_market_stats(data)

        return res_data

    @staticmethod
    def get_all_tickers():

        data = database_querys_main.database_querys.get_all_trend_kalman()

        res_data = analyses_support.extract_all_tickers(data)

        res_data = trend_analyse_support().package_data(res_data)

        return res_data


class trend_analyse_support(object):

    @staticmethod
    def set_ticker(ticker):
        """
        Prevents that ticker will be set in wrong format.

        Parameters
        ----------
        ticker : TYPE
            DESCRIPTION.

        Returns
        -------
        ticker : TYPE
            DESCRIPTION.

        """
        ticker = str(ticker)
        ticker = ticker.upper()
        return ticker

    @staticmethod
    def package_data(data):
        """
        Packages data in JSON 

        Parameters
        ----------
        data : TYPE
            DESCRIPTION.

        Returns
        -------
        resp : TYPE
            DESCRIPTION.

        """
        # transform data to json

        try:

            data = data.to_dict(orient='records')

        # if packaging already done, dump and return.
        except AttributeError:

            resp = json.dumps(data)

            return resp

        # else dump and return.

        resp = json.dumps(data)

        return resp


class analyses_support(object):

    @staticmethod
    def extract_all_tickers(data):
        df = data
        tickers = df.id.values.tolist()
        return tickers

    @staticmethod
    def return_market_stats(data):
        """
        Returns all strategy stats, including trending market.

        Parameters
        ----------
        data : TYPE
            DESCRIPTION.

        Returns
        -------
        resp : TYPE
            DESCRIPTION.

        """
        data_res = {}
        # set dataframe
        df = data

        # get amount of positive data.
        long_trades = df.loc[df['trend'] > 0]
        short_trades = df.loc[df['trend'] < 0]

        data_res["stocks_trending_long"] = pct_markettrending = round(
            len(long_trades) / len(df)*100, 2)

        positive_trades = df.loc[df['current_yield'] > 0]

        negative_trades = df.loc[df['current_yield'] < 0]

        data_res["percentage_positive_trades"] = pct_positive_signals = round(
            len(positive_trades) / len(df)*100, 2)
        pct_negative_signals = round(
            len(negative_trades) / len(df)*100, 2)

        average_yield_positive = positive_trades.current_yield.mean(
        ).round(2)

        average_yield_negative = negative_trades.current_yield.mean().round(2)

        data_res["average_strategy_net_yield"] = average_net_yield = round(((((pct_positive_signals/100) * average_yield_positive) +
                                                                             ((pct_negative_signals/100) * average_yield_negative))), 2)

        data_res["average_durration_trade"] = average_durration_long_durration = df.duration.mean(
        ).round(2)

        # else dump and return.
        resp = json.dumps(data_res)
        return resp


if __name__ == "__main__":

    try:

        x = return_trend_analyses.get_all_tickers()

        print(x)
    except Exception as e:

        print(e)

   # print(data, "this is the data")
