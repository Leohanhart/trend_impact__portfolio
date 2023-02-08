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


class return_portfolios_options(object):

    @staticmethod
    def return_trading_portfolios(id_: str = ""):
        """
        Returns trading portfolio's these can be added with the add function.

        Returns
        -------
        None.

        """

        # get portfolio's
        data = database_querys_main.database_querys.get_trading_portfolio(id_)

        res_data = analyses_support().package_data(data)

        return res_data

    @staticmethod
    def return_portfolios(page_number: int = 1,
                          page_amount: int = 20,
                          min_amount_stocks: int = 5,
                          max_amount_stocks: int = 6):
        """


        Parameters
        ----------
        min_amount_stocks : int, optional
            DESCRIPTION. The default is 5.
        max_amount_stocks : int, optional
            DESCRIPTION. The default is 6.

        Returns
        -------
        None.

        """

        # get portfolio's
        data = database_querys_main.database_querys.get_portfolio()

        # filter portfolios
        data = portfolio_support().return_portfolio_selection_between_amounts(df=data,
                                                                              min_amount_stocks=min_amount_stocks,
                                                                              max_amount_stocks=max_amount_stocks
                                                                              )

        data = analyses_support().apply_pagination(
            data, page_amount=page_amount, page_number=page_number)

        data = analyses_support().package_data(data)

        return data

    @staticmethod
    def add_trading_portfolio(id_: str):
        """
        Add portfolio, after the portfio is added. The portfolio will not be deleted. 

        Parameters
        ----------
        id_ : str
            DESCRIPTION.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """

        try:

            data = database_querys_main.database_querys.subscribe_trading_portfolio(
                id_=id_)

            return data

        except Exception as e:

            return e

    @staticmethod
    def delete_trading_portfolio(id_: str):
        """
        Add portfolio, after the portfio is added. The portfolio will not be deleted. 

        Parameters
        ----------
        id_ : str
            DESCRIPTION.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """

        try:

            data = database_querys_main.database_querys.unsubscribe_trading_portfolio()

            return data

        except Exception as e:

            return e


class portfolio_support(object):

    @staticmethod
    def check_portfolio_id_is_avible(id_: str):
        """

        Check if portolio is avalible. 

        Parameters
        ----------
        id_ : str
            DESCRIPTION.

        Returns
        -------
        bool
            DESCRIPTION.

        """
        avalble_ids = portfolio_support().return_portfolio_ids()
        avable_trading_ids = portfolio_support.return_trading_portfolios()

        if id_ in avalble_ids:
            return True
        elif id_ in avable_trading_ids:
            return True
        else:
            return False

    @staticmethod
    def return_portfolio_ids():
        """

        returns the portfolio ids.

        Returns
        -------
        data : TYPE
            DESCRIPTION.

        """
        data = database_querys_main.database_querys.get_portfolio()
        data = list(data.portfolio_id.values)
        return data

    def return_trading_portfolios():
        """


        Returns
        -------
        None.

        """
        data = database_querys_main.database_querys.get_trading_portfolio()
        data = list(data.portfolio_id.values)
        return data

    @staticmethod
    def return_portfolio_selection_between_amounts(df, min_amount_stocks: int = 5, max_amount_stocks: int = 6, filter_on_sharp: bool = True):
        """


        Parameters
        ----------
        df : TYPE
            DESCRIPTION.
        min_amount_stocks : int, optional
            DESCRIPTION. The default is 5.
        max_amount_stocks : int, optional
            DESCRIPTION. The default is 6.
        filter_on_sharp : bool, optional
            DESCRIPTION. The default is True.

        Returns
        -------
        df : TYPE
            DESCRIPTION.

        """
        df = df.loc[(df["portfolio_amount"] <= max_amount_stocks) &
                    (df["portfolio_amount"] >= min_amount_stocks)]

        if filter_on_sharp:
            df = portfolio_support().sort_on_yield(df)

        return df

    @staticmethod
    def sort_on_yield(df):
        """
        Sort portfolio on 2 year sharp ration. 

        Parameters
        ----------
        df : TYPE
            DESCRIPTION.

        Returns
        -------
        df : TYPE
            DESCRIPTION.

        """

        df = df.sort_values(by='total_sharp_y2', ascending=False)
        return df


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
        long_trades = df.loc[(df['trend'] > 0) & (df['duration'] < 250)]
        short_trades = df.loc[(df['trend'] < 0) & (df['duration'] < 250)]

        long_trades_m1 = df.loc[(df['trend'] > 0) & (df['duration'] <= 21)]
        short_trades_m1 = df.loc[(df['trend'] < 0) & (df['duration'] <= 21)]

        trades_m1 = df.loc[df['duration'] <= 21]

        long_trades_d5 = df.loc[(df['trend'] > 0) & (df['duration'] <= 5)]
        short_trades_d5 = df.loc[(df['trend'] < 0) & (df['duration'] <= 5)]

        trades_d5 = df.loc[df['duration'] <= 5]

        data_res["percentage_average_yield_m1"] = trades_m1.current_yield.mean().round(
            2)
        data_res["percentage_average_yield_w1"] = trades_d5.current_yield.mean().round(
            2)

        data_res["stocks_trending_long"] = pct_markettrending = round(
            len(long_trades) / len(df)*100, 2)

        positive_trades = df.loc[df['current_yield'] > 0]

        positive_trades_m1 = trades_m1.loc[df['current_yield'] > 0]

        positive_trades_d5 = trades_d5.loc[df['current_yield'] > 0]

        negative_trades = df.loc[df['current_yield'] < 0]

        data_res["percentage_positive_trades_y1"] = pct_positive_signals = round(
            len(positive_trades) / len(df)*100, 2)
        pct_negative_signals = round(
            len(negative_trades) / len(df)*100, 2)

        data_res["percentage_positive_trades_m1"] = pct_positive_signals_ = round(
            len(positive_trades_m1) / len(trades_m1)*100, 2)

        data_res["percentage_positive_trades_w1"] = pct_positive_signals_ = round(
            len(positive_trades_d5) / len(trades_d5)*100, 2)

        data_res["amount_trades_m1"] = len(trades_m1)

        data_res["amount_trades_w1"] = len(trades_d5)

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

    @staticmethod
    def apply_pagination(data, page_amount: int = 20, page_number: int = 1):
        """
        Pagnation.

        Parameters
        ----------
        data : dataframe with data.

        pagination_filter : bool, optional
            DESCRIPTION. The default is False.
        page_amount : int, optional
            DESCRIPTION. The default is 20.
        page_number : int, optional
            DESCRIPTION. The default is 1.

        Returns
        -------
        None.



        """
        # setup to pervent idiotic pagination.
        if len(data) < page_amount:
            return data
        # gets starting number

        # define page number:
        end___number = page_amount * page_number
        start_number = end___number - page_amount
        data = data.iloc[start_number:end___number]

        return data

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


if __name__ == "__main__":

    try:

        x = return_portfolios_options.add_trading_portfolio(
            id_="fcd50532-8dd2-11ed-904b-001a7dda7110")

        print(x)
    except Exception as e:

        print(e)

   # print(data, "this is the data")
