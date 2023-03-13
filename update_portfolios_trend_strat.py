# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 20:20:32 2022

@author: Gebruiker
"""
import constants
import database_querys_main as database_querys
import stock_analyses_with_ticker_main as stock_analyses_with_ticker
from core_scripts.stock_data_download import power_stock_object as stock_object
from core_update.update_analyses import update_support
from datetime import datetime, timedelta, date
import time
import numpy as np
import numpy
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
import random
from datetime import datetime
import statistics
import startup_support as support
# custom target function


import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)


class update_trend_kamal_portfolio_selection:

    def __init__(self, methode_one: bool = True):

        if methode_one:

            """
            Methode one is basicly filterd on winrate, cutted and
            """
            # gets data
            df = database_querys.database_querys.get_trend_kalman_performance(
                periode="D")

            # first select half of amount of trades.
            df = df.loc[df['amount_of_trades_y2'] >
                        df["amount_of_trades_y2"].median()]

            # high winrates, takes higest BEST 82,5%
            p = df.total_profitible_trades_y2.max() - round((df.total_profitible_trades_y2.max() -
                                                             df.total_profitible_trades_y2.mean()) / 4)

            #
            df = df.loc[df['total_profitible_trades_y2'] > p]

            df = df.sort_values(
                by=["total_sharp_y2",  "total_sharp_y5", "total_sharp_all"], ascending=False)

            # opoinaly remove. if there are more than 25 the system chrashs haha
            # it takes ages for the correlation matrix.

            # removed because tail values
            # df = df.head(25)
            #
            tickers_for_portfolio = list(df.id.values)

            """
            # create correlation matrix
            correlations_tickers = create_correlation_matrix(
                tickers=tickers_for_portfolio)

            # one way to create a dataframe
            df = pd.DataFrame(correlations_tickers.data)

            df = df.sort_values(by=["correlation"])

            # this one creates tickers

            tickers_out = correlations_tickers.ticker
            """
            tickers_out = tickers_for_portfolio
            # create function that creates all kind off ticker combinations
            # 5 - 10.
            list_of_options = []

            # gets all posible moves. 5 IS 42k
            options = list(combinations(tickers_out, 5))

            # adds those to list.
            # this options out commanded is fuckt because of wrong python version.
            # res = [list(ele) for ele in options]
            res = [list(ele) for i, ele in enumerate(options)]
            list_of_options.extend(res)

            # optionally there needs to be a efficiency impementation here.
            # that could be a loop that gets all data and puts it in a dict
            # and gets it out, so it will work way faster.
            ticker_options = {}

            # loops true
            for i in tickers_out:

                ts_data = create_time_serie_with_kamalstrategie(i)

                ticker_options[i] = ts_data.data

            # create dataframes that can be tested.
            for i in range(0, len(list_of_options)):

                tickers_selected = list_of_options[i]

                data = self.create_data_frame_of_tickers(
                    tickers_selected, ticker_options)

                portfolio = portfolio_constructor_manager(data)

    # first, take the correlation of the two stocks. then get the details of archive.
    # mainly profitiblity score, and LEO-sharp, Expected return and VOL are importand.
    # then add them to the database. you get the archive and the active portfolio:
    # filter selection : first filter on profitibliy-score (10), Then on correlation.
    # then take create lists. of the portfolio's.

    def create_data_frame_of_tickers(self, tickers: list, data: dict):
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


class create_correlation_matrix:

    data = None

    def __init__(self, tickers):

        data = []
        #
        for tickerA in tickers:

            #
            for tickerB in tickers:

                #
                if tickerA == tickerB:
                    continue

                #
                try:

                    #
                    new_data = {}

                    # sort data
                    tickers_in = [tickerA, tickerB]
                    tickers_in.sort()

                    #
                    new_data["stock_a"] = tickers_in[0]
                    new_data["stock_b"] = tickers_in[1]

                    #
                    power_objectA = stock_object.power_stock_object(
                        stock_ticker=tickerA, simplyfied_load=True, periode_weekly=False)
                    power_objectB = stock_object.power_stock_object(
                        stock_ticker=tickerB, simplyfied_load=True, periode_weekly=False)

                    #
                    correlation = power_objectA.stock_data.Change.corr(
                        power_objectB.stock_data.Change)

                    new_core = round(correlation, 2)

                    new_data["correlation"] = new_core

                    data.append(new_data)

                    self.data = data

                except Exception as e:
                    continue

        df = pd.DataFrame(data)

        df = df.sort_values(by=["correlation"])

        df.drop_duplicates()

        # create loss value tickers.
        tickers = [df.stock_a.values, df.stock_b.values]
        ticker = tickers[0]
        ticker = list(dict.fromkeys(ticker))

        self.data = df
        self.ticker = ticker


class portfolio_constructor_manager:

    # low vol strats
    portfolio_strat_low_vol_stocks = None
    portfolio_strat_low_vol_details = None

    # high sharp.
    portfolio_strat_high_sharp_stocks = None
    portfolio_strat_high_sharp_details = None

    # potfolio items.
    std_vol: float = None
    min_vol: float = None
    max_vol: float = None
    avg_vol: float = None

    std_sharp: float = None
    min_sharp: float = None
    max_sharp: float = None
    avg_sharp: float = None

    # min vol
    # 2 year return
    min_vol_y2_return: float = None
    # 2 year max drawdown
    min_vol_y2_max_drawdown: float = None
    # 2 year expected return
    min_vol_y2_expected_return: float = None

    # max sharp
    # 2 year return
    max_sharp_y2_return: float = None
    # 2 year max drawdown
    max_sharp_y2_max_drawdown: float = None
    # 2 year expected return
    max_sharp_y2_expected_return: float = None

    # amount of stocks

    def __init__(self, data, name_strategie: str = "undefined", periode=500, days_untill_ex: int = 21):
        """
        Insert data in the format needed for financial quant.

        Parameters
        ----------
        data : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        # sets name strategie.
        self.name_strategie = name_strategie

        # sets days untill ex
        self.days_untill_ex = days_untill_ex

        # transform data =
        data = data.tail(periode)

        # fills data profolems
        data = data.fillna(0)

        # sets pf to class object.
        self.pf = pf = build_portfolio(data=data)

        # set optimalization
        opt_w, opt_res = pf.mc_optimisation(num_trials=500)

        # gets ID's
        self.the_id_low_vol = uuid.uuid4().hex
        self.the_id_sharp__ = uuid.uuid4().hex

        # creates frames of porfolios
        self.portfolio_strat_low_vol_stocks = self.process__stocks__to__df(
            opt_w.iloc[0], self.the_id_low_vol)
        self.portfolio_strat_high_sharp_stocks = self.process__stocks__to__df(
            opt_w.iloc[1], self.the_id_sharp__)

        # create specs
        self.portfolio_strat_low_vol_details = self.process__portfolio_specs__to__df(
            opt_res.iloc[:1, ::], self.the_id_low_vol)
        self.portfolio_strat_high_sharp_details = self.process__portfolio_specs__to__df(
            opt_res.iloc[1:2, ::], self.the_id_sharp__)

        # set matrix
        self.set_matrix()

        # sets high sharp to data
        x_data = opt_res[1:2]
        sharp_dict = x_data.to_dict(orient="records")
        self.Imax_sharp_volatility = round(sharp_dict[0]["Volatility"], 2)
        self.Imax_sharp_expected_return = round(
            sharp_dict[0]['Expected Return'], 2)
        self.Imax_sharp_sharp_ratio = round(sharp_dict[0]['Sharpe Ratio'], 2)
        ####

        # create stock_data details for low vol.
        balances_low_vol = list(self.low_vol_frame.balance.to_dict().values())
        # sets data balanced
        low_volatile_data = data * balances_low_vol
        low_volatile_summed = low_volatile_data.sum(axis=1)

        # create 2 year frame low/high
        ts_low_vol = low_volatile_data.sum(axis=1).pct_change().cumsum()

        # setting up dataframe for drawdown functions
        ts_low_df = pd.DataFrame(low_volatile_summed)
        ts_low_df.rename(
            columns={ts_low_df.columns[0]: 'Adj Close'}, inplace=True)

        low_vol_max_drawdown = self.return_max_drawdown(ts_low_df)
        low_vol_expected_return = low_volatile_summed.pct_change().mean() * 100

        self.min_vol_y2_expected_return = low_vol_expected_return
        self.min_vol_y2_max_drawdown = low_vol_max_drawdown
        self.min_vol_y2_return = round(((float(low_volatile_summed.tail(
            1)) - float(low_volatile_summed.head(1))) / float(low_volatile_summed.tail(1)))*100, 2)
        #####

        # create stock_data details for high sharp.
        balances_high_sharp = list(
            self.high_sharp_frame.balance.to_dict().values())
        # round the values
        balances_high_sharp = [round(num, 2) for num in balances_high_sharp]
        # sets data balanced
        high_sharp_data = data * balances_high_sharp
        high_sharp_summed = high_sharp_data.sum(axis=1)

        """
        the rest of the names is unchanged for purpose chill.
        """
        # create 2 year frame low/high
        ts_low_vol = high_sharp_data.sum(axis=1).pct_change().cumsum()

        # setting up dataframe for drawdown functions
        ts_low_df = pd.DataFrame(high_sharp_summed)
        ts_low_df.rename(
            columns={ts_low_df.columns[0]: 'Adj Close'}, inplace=True)

        low_vol_max_drawdown = self.return_max_drawdown(ts_low_df)
        low_vol_expected_return = low_volatile_summed.pct_change().mean() * 100

        self.max_sharp_y2_expected_return = low_vol_expected_return
        self.max_sharp_y2_max_drawdown = low_vol_max_drawdown
        self.max_sharp_y2_return = round(((float(high_sharp_summed.tail(
            1)) - float(high_sharp_summed.head(1))) / float(high_sharp_summed.tail(1)))*100, 2)

        return

    def return_max_drawdown(self, stock__data__frame=None, position_side: int = 1, return_time_serie: bool = False):
        """
        source: https://quant.stackexchange.com/questions/18094/how-can-i-calculate-the-maximum-drawdown-mdd-in-python

        Parameters
        ----------
        data_input_stock_data : TYPE, optional
            DESCRIPTION. The default is None.
        filterd_data : TYPE, optional
            DESCRIPTION. The default is None.

        Returns
        -------
        None.

        """

        window = len(stock__data__frame)

        if position_side == 1:

            # Calculate the max drawdown in the past window days for each day in the series.
            # Use min_periods=1 if you want to let the first 252 days data have an expanding window
            Roll_Max = stock__data__frame['Adj Close'].rolling(
                window, min_periods=1).max()
            Daily_Drawdown = stock__data__frame['Adj Close']/Roll_Max - 1.0

            # Next we calculate the minimum (negative) daily drawdown in that window.
            # Again, use min_periods=1 if you want to allow the expanding window
            Max_Daily_Drawdown = Daily_Drawdown.rolling(
                window, min_periods=1).min()

            # return in right format,
            if not return_time_serie:
                return round(float(Max_Daily_Drawdown.min()*100), 3)
            else:
                return Max_Daily_Drawdown

        else:
            Roll_Max = stock__data__frame['Adj Close'].rolling(
                window, min_periods=1).min()
            Daily_Drawdown = stock__data__frame['Adj Close']/Roll_Max - 1.0
            Dd_test = Daily_Drawdown * -1

            # Next we calculate the minimum (negative) daily drawdown in that window.
            # Again, use min_periods=1 if you want to allow the expanding window
            Max_Daily_Drawdown = Dd_test.rolling(window, min_periods=1).min()
            # return in right format,
            if not return_time_serie:
                return round(float(Max_Daily_Drawdown.min()*100), 3)
            else:
                return Max_Daily_Drawdown

    def set_matrix(self):

        # sets vars
        self.low_vol_frame = self.portfolio_strat_low_vol_stocks
        self.high_sharp_frame = self.portfolio_strat_high_sharp_stocks

        # potfolio items.
        self.std_vol: float = float(self.low_vol_frame.balance.std())
        self.min_vol: float = float(self.low_vol_frame.balance.min())
        self.max_vol: float = float(self.low_vol_frame.balance.max())
        self.avg_vol: float = float(self.low_vol_frame.balance.mean())

        #
        self.std_sharp: float = float(self.high_sharp_frame.balance.std())
        self.min_sharp: float = float(self.high_sharp_frame.balance.min())
        self.max_sharp: float = float(self.high_sharp_frame.balance.max())
        self.avg_sharp: float = float(self.high_sharp_frame.balance.mean())

    def process__portfolio_specs__to__df(self, df: dict, UUid: str):

        df = df.reset_index()

        # sets uuID
        df['id'] = UUid

        # sets the mame of the strategie
        df['selection strategie'] = self.name_strategie

        # sets created AT datestring - so you can see when constructed
        df['createdAt'] = self.get_date_string()

        # sets experation -- so when it can not longer be used.
        df['expiresAt'] = self.get_date_string(self.days_untill_ex)

        # sets bool for trading
        df['Traded'] = False

        # sets status, if portolio trade is over, just make in-active.
        df['Trade_active'] = True

        # sets total lengt of stocks
        df['total_amount_stocks'] = len(self.portfolio_strat_low_vol_stocks)

        df['user_id'] = "0"

        df['pnl'] = 0.00

        # renames the frame.
        df = df.rename(columns={df.columns[0]: "optimization strategie",



                                })

        # re organizes index.
        columns_titles = ['id', 'selection strategie', 'optimization strategie', 'Expected Return', 'Volatility',
                          'Sharpe Ratio',   'createdAt', 'expiresAt']

        # reindex dataframe
        df = df.reindex(columns=columns_titles)

        return df

    def process__stocks__to__df(self, df_stocks, UUid):

        # set df to var.
        df = df_stocks

        # reset index.
        df = df.reset_index()

        # sets id column.
        df['id'] = UUid

        # renames the frame.
        df = df.rename(
            columns={df.columns[0]: "ticker", df.columns[1]: 'balance'})

        # re organizes index.
        columns_titles = ["id", "ticker", "balance"]

        # reindex dataframe
        df = df.reindex(columns=columns_titles)

        return df

    def get_date_string(self, amount_of_days: int = 0):
        """
        returns date string

        Parameters
        ----------
        amount_of_days : int, optional
            DESCRIPTION. The default is 0.

        Raises
        ------
        ImportError
            DESCRIPTION.

        Returns
        -------
        date_string : TYPE
            DESCRIPTION.

        """

        try:
            from datetime import datetime, timedelta
        except:
            raise ImportError

        date_ = datetime.today()

        if amount_of_days != 0:

            date_ = date_ + timedelta(days=amount_of_days)

        # sets datestring.
        date_string = date_.strftime("%d-%m-%Y")

        return date_string
        #


class create_time_serie_with_kamalstrategie:

    def __init__(self, ticker):
        """
        https://stackoverflow.com/questions/29370057/select-dataframe-rows-between-two-dates


        Parameters
        ----------
        ticker : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
       # return signals
        power_object = stock_object.power_stock_object(
            stock_ticker=ticker)

       # stockdata
        sdata = power_object.stock_data

        if sdata.empty:
            return 404

        itms = list(sdata.columns.to_list())
       # stock.data.change
        if 'Change' not in itms:

            cdata = power_object.stock_data.Close

        else:

            cdata = power_object.stock_data.Change

        # set openprice
        open_price_stock = float(sdata.Close.head(1))

        cdata = self.filter_pandas_stock_years(cdata, 35)

       # gets the data
        data = database_querys.database_querys.get_trend_kalman_data(
            ticker=ticker)

       # filter last 2years
        data = self.filter_pandas_years(data, 35)

       # selects the right columns
        data = data[['year_start', 'month_start', 'date_start',
                     'year_end', 'month_end', 'date_end', 'trend']]

       # create date objects
        data_obj = data.to_dict(orient='records')

        df = dfu = cdata

       # select mask = changevalue, df.update, finished
        for i in data_obj:

            if i["trend"] == 1:
                continue

            # creates startdate
            date_start = str(i["year_start"]) + "-" + \
                str(i["month_start"]) + "-" + str(i["date_start"])

            # create enddates
            date_end = str(i["year_end"]) + "-" + \
                str(i["month_end"]) + "-" + str(i["date_end"])

            # creates mask
            mask = (df.index > date_start) & (df.index <= date_end)

            # creates data
            work_data = df.loc[mask]

            work_data = work_data * -1

            df.update(work_data)

        # set dataframe
        x = df.cumsum()

        # set
        y = df
        y[0:] = open_price_stock

        # set percentage
        p = x + 100

        # dataframe with total price.
        o = (y * p) / 100

        # create dataframe
        df_data = o.to_frame()

        # create
        df_data["returns"] = x

        # create ticker
        name_ticker = str(ticker) + "_"

        df_data.add_prefix(name_ticker)

        self.data = df_data

    def filter_pandas_years(self, df, amount_of_years=2):

        last_row = df.tail(1)

        start_year = int(last_row.year_end) - amount_of_years

        df = df.loc[df['year_end'] > start_year]

        return df

    def filter_pandas_stock_years(self, df, amount_of_years=2):

        last_row = df.tail(1)

        start_year = int(df.tail(1).index.year[0]) - amount_of_years

        df = df.loc[df.index > str(start_year)]

        return df


class create_kko_portfolios:
    """
    On 06-01 this class is not longer be maintained anymore,
    main function is

    """

    def __init__(self):
        return

    def create_all_options(self, list_of_stocks: list, amount_of_stocks: int):

        tickers_out = list_of_stocks
        # create function that creates all kind off ticker combinations
        # 5 - 10.

        list_of_options = []

        # optionally there needs to be a efficiency impementation here.
        # that could be a loop that gets all data and puts it in a dict
        # and gets it out, so it will work way faster.
        ticker_options = {}

        # loops true
        for i in tickers_out:

            try:

                ts_data = create_time_serie_with_kamalstrategie(i)

                ticker_options[i] = ts_data.data
            except:

                tickers_out.remove(i)

        # get the keys so only good stocks will stay ther
        tickers_out = list(ticker_options.keys())

        # gets all posible moves. 5 IS 42k
        options = list(combinations(tickers_out, 5))

        # adds those to list.
        # this options out commanded is fuckt because of wrong python version.
        # res = [list(ele) for ele in options]
        res = [list(ele) for i, ele in enumerate(options)]
        list_of_options.extend(res)

        round_ = 0
        # create dataframes that can be tested.
        for i in range(0, len(list_of_options)):

            round_ += 1

            tickers_selected = list_of_options[i]

            data = self.create_data_frame_of_tickers(
                tickers_selected, ticker_options)

            portfolio = portfolio_constructor_manager(data)

            allowd_to_add = kko_portfolio_gardian(portfolio)

            if allowd_to_add.allowd:

                execute = add_kko_portfolio(portfolio)

        return

    def create_data_frame_of_tickers(self, tickers: list, data: dict):
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


class add_kko_portfolio:

    model = None

    def __init__(self, portfolio):

        model = kko_strat_model()
        # create an UUID,
        model.portfolio_id = str(uuid.uuid1())

        model.portfolio_strategy = "TREND_STRAT_KKO_HS"
        # create amount
        model.portfolio_amount = int(
            len(portfolio.high_sharp_frame.ticker.to_list()))

        tickers = portfolio.high_sharp_frame.ticker.to_list()
        serialized_list_of_tickers = json.dumps(tickers)

        # set tickers
        model.list_of_tickers = serialized_list_of_tickers

        balances = portfolio.high_sharp_frame.balance.to_list()
        balances = [round(num, 3) for num in balances]

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

        # perfomnace data =
        performance_data = {trend: "Leo_Was_Here"}
        serialized_list_of_perfomance_data = json.dumps(performance_data)
        model.list_of_performance = serialized_list_of_perfomance_data

        # create an
        total_expected_return = round(
            portfolio.max_sharp_y2_expected_return, 2)
        model.total_expected_return = portfolio.Imax_sharp_expected_return

        total_sharp = round(portfolio.max_sharp_y2_return, 2)
        model.total_sharp_y2 = portfolio.Imax_sharp_sharp_ratio

        model.total_volatility_y2 = portfolio.Imax_sharp_volatility

        today = date.today()
        d1 = today.strftime("%d-%m-%Y")

        model.createdAt = d1

        database_querys.database_querys.update_portfolio(model)
        return


class create_kko_tickers_selection:

    selected_tickers: list

    def __init__(self, methode_one: bool = False, methode_two: bool = False, methode_test: bool = False):
        """
        VERY important
        - First method is kind of created to make small lists of stocks.
        -second method is more pragmatish without caring about rest.

        Parameters
        ----------
        methode_one : bool, optional
            DESCRIPTION. The default is True.

        Returns
        -------
        None.

        """

        if methode_one:

            """
            Methode one is basicly filterd on winrate, cutted and

            its very hard to say why this method is chosen, because it takes the median of the



            """
            # gets data

            df = database_querys.database_querys.get_trend_kalman_performance(
                periode="D")

            # first select half of amount of trades.
            df = df.loc[df['amount_of_trades_y2'] >
                        df["amount_of_trades_y2"].median()]

            # high winrates, takes higest BEST 82,5%

            p = df.total_profitible_trades_y2.max() - round((df.total_profitible_trades_y2.max() -
                                                             df.total_profitible_trades_y2.mean()) / 4)

            #
            df = df.loc[df['total_profitible_trades_y2'] > p]

            df = df.sort_values(
                by=["total_sharp_y2",  "total_sharp_y5", "total_sharp_all"], ascending=False)

            # opoinaly remove. if there are more than 25 the system chrashs haha
            # it takes ages for the correlation matrix.

            # removed because tail values
            # df = df.head(25)
            #
            tickers_for_portfolio = list(df.id.values)

            self.selected_tickers = tickers_for_portfolio
            return

        if methode_two:

            """
            Methode one is basicly filterd on winrate, cutted and

            its very hard to say why this method is chosen, because it takes the median of the



            """
            # gets data
            df = database_querys.database_querys.get_trend_kalman_performance(
                periode="D")

            # first select half of amount of trades.
            df = df.loc[df['amount_of_trades_y2'] > 13]

            df = df.loc[df['total_profitible_trades_y2'] > 95]

            df = df.sort_values(
                by=["total_sharp_y2",  "total_sharp_y5", "total_sharp_all"], ascending=False)

            # opoinaly remove. if there are more than 25 the system chrashs haha
            # it takes ages for the correlation matrix.

            # removed because tail values
            # df = df.head(25)
            #
            tickers_for_portfolio = list(df.id.values)

            self.selected_tickers = tickers_for_portfolio
            return

        if methode_test:
            """
            Methode one is basicly filterd on winrate, cutted and

            its very hard to say why this method is chosen, because it takes the median of the



            """
            # gets data
            df = database_querys.database_querys.get_trend_kalman_performance(
                periode="D")

            # first select half of amount of trades.
            df = df.loc[df['amount_of_trades_y2'] > 13]

            df = df.loc[df['total_profitible_trades_y2'] > 95]

            df = df.sort_values(
                by=["total_sharp_y2",  "total_sharp_y5", "total_sharp_all"], ascending=False)

            # opoinaly remove. if there are more than 25 the system chrashs haha
            # it takes ages for the correlation matrix.

            # removed because tail values
            df = df.head(30)
            #
            tickers_for_portfolio = list(df.id.values)

            self.selected_tickers = tickers_for_portfolio
            return


class kko_portfolio_gardian:

    allowd: bool = False

    # allows portfolio's that have one stock that les than 50 of average.
    lower_boundery = 50

    def __init__(self, portfolio):
        """

        stocks for only 5 stocks have hardcore criteria.
        for above 10, there are different criteria.
        - no more sharpratio blockers -- this will be done automatic
        for above 20
        - there will be a 1% minimum portfolio balance.
        - for

        Criteria:
            - mainly build for max sharp, correlation balance in portfolio, and high expected return

        checks
        - 1 if the stocks are equal balanced.

        Parameters
        ----------
        portfolio : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """

        allowd = False
        # sets portfolio_parameters -- if needed check them here -- for example long short.
        self.set_parameters(portfolio)

        # route for 5 stocks
        if self.amount_stocks == 5:

            self.amount_5_stocks_criteria()
            return

        # route for 5 - 10 stocks
        if self.amount_stocks >= 5 and self.amount_stocks <= 10:

            self.amount_5_stocks_criteria()
            return

        # route for 10 and 20.
        if self.amount_stocks > 11 and self.amount_stocks <= 20:

            self.amount_20_stocks_criteria()
            return
        if self.amount_stocks > 21 and self.amount_stocks < 50:

            self.amount_50_stocks_criteria()
            return

        if self.amount_stocks > 51 and self.amount_stocks < 500:

            self.amount_100_stocks_criteria()
            return

    def amount_5_stocks_criteria(self):

        if self.min_balance > ((100 / (self.amount_stocks * 2))/100):
            if self.portfolio.Imax_sharp_sharp_ratio > 2.99:
                if self.portfolio.Imax_sharp_expected_return > 0.15:
                    self.allowd = True

    def amount_20_stocks_criteria(self):
        if self.min_balance > 0.025:
            if self.portfolio.Imax_sharp_sharp_ratio > 2.99:
                if self.portfolio.Imax_sharp_expected_return > 0.14:
                    self.allowd = True

    def amount_50_stocks_criteria(self):
        if self.min_balance > 0.0005:
            if self.portfolio.Imax_sharp_sharp_ratio > 2.00:
                if self.portfolio.Imax_sharp_expected_return > 0.10:
                    self.allowd = True

    def amount_100_stocks_criteria(self):
        if self.min_balance > 0.00005:
            if self.portfolio.Imax_sharp_sharp_ratio > 2.00:
                if self.portfolio.Imax_sharp_expected_return > 0.10:
                    self.allowd = True

    def return_amount_of_stocks(self, p):
        amount = len(p.portfolio_strat_high_sharp_stocks)
        return amount

    def set_parameters(self, portfolio):
        """
        Sets parrameters for analyses.

        amount of stocks,
        calculations,
        ect

        Parameters
        ----------
        porfolfio : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        self.portfolio = portfolio
        self.amount_stocks = self.return_amount_of_stocks(portfolio)
        self.boundery_low = 100/self.amount_stocks * \
            (self.lower_boundery / 100)
        self.min_balance = round((portfolio.min_sharp * 100), 2)
        self.min_shapr = portfolio.min_sharp * 100


class kko_portfolio_update_manager:

    kill_switch: bool = False

    def __init__(self):

        self.startup_new()

    def startup_new(self):
        """


        System functions
        1. Deletes all old options when a cycle is finished, removes all options if restarted. So there is always a clean database.

        """

        delete_old_portfolios: bool = False

        min_amount_tickers: int = 5
        max_rotations: int = 10000
        max_stocks: int = 50
        min_sharp_ratio: int = 0

        # find last amount and sharp.
        details = self.get_last_details()
        # remove methode test befor deployment
        min_amount_tickers, min_sharp_ratio = details

        #
        if min_amount_tickers == 5:
            #
            self.remove_all_portfolios()

        # retreives the list with old portoflio's that will be deleted in the end.
        old_portfolios = self.return_all_old_portfolios()

        # get the tickers
        selection = create_kko_tickers_selection(methode_two=True)

        tickers_selected = selection.selected_tickers

        # shuffel selection.
        for i in range(0, 10):
            random.shuffle(tickers_selected)

        items = self.create_data_of_tickers(
            selection.selected_tickers)

        tickers = list(items.keys())

        # self.create_single_options(items[1], lists_[0], "thread Leo")
        # self.create_all_options(selection.selected_tickers, 5)

        self.continues_portfolio_creation(
            items, tickers, 'thread 0', min_amount_tickers, max_rotations, max_stocks, min_sharp_ratio)

        self.delete_list_portrfolios(old_portfolios)

        return
        """
        threads = []
        thread0.start()
        thread6.start()

        threads.append(thread0)
        threads.append(thread6)

        print('threads have started')
        # Join the threads before
        loop:  bool = True
        while loop:

            if not thread6.is_alive():

                print("Doden threads in portfolio managment")

                thread6.join()
                self.kill_switch = True
                loop = False
                break

            if not thread0.is_alive():

                print("Doden threads in portfolio managment")

                print(thread)

                thread.join()
                self.kill_switch = True
                loop = False
                break

    
        thread1.join()
        thread2.join()
        thread3.join()
        thread4.join()
        thread5.join()
 
        thread7.join()
        thread8.join()
        thread9.join()
        

        thread10.join()
        thread11.join()

        thread12.join()
        thread13.join()
        thread14.join()
        thread15.join()
        thread16.join()


        # the rest one I guess.
        # function with different parameters
        thread1 = threading.Thread(target=self.print_squares,
                                   args=("thread1", [1, 2, 3, 4, 5]))

        thread2 = thread_2 = Thread(target=self.task_2)

        thread3 = threading.Thread(target=self.task_3,
                                   args=())
        threads = []
        # Start the threads
        thread1.start()
        thread2.start()
        thread3.start()

        threads.append(thread1)
        threads.append(thread2)
        threads.append(thread3)

        # Join the threads before
        loop:  bool = True
        while loop:
            for thread in threads:
                if not thread.is_alive():
                    print("Doden threads")

                    thread.join()
                    self.kill_switch = True
                    loop = False
                    break

        # moving further
        thread1.join()
        thread2.join()
        thread3.join()
  
        """

    def starting_up(self):
        """


        first split the list of options so that the data unit doesent overload. 

        befor split randomise the list. 


        """

        min_amount_tickers: int = 5
        min_sharp_ratio: int = 0
        max_rotations: int = 10000
        max_stocks: int = 50

        if support.check_if_today_is_first_the_month():

            database_querys.database_querys.add_log_to_logbook(
                "Deleted all portfolio's and re-newd cycle")
            self.remove_all_portfolios()

        else:

            # find last amount and sharp.
            details = self.get_last_details()
            # remove methode test befor deployment
            min_amount_tickers, min_sharp_ratio = details

        # get the tickers
        selection = create_kko_tickers_selection(methode_test=True)

        tickers_selected = selection.selected_tickers

        # shuffel selection.
        for i in range(0, 10):
            random.shuffle(tickers_selected)

        items = self.create_data_of_tickers(
            selection.selected_tickers)

        tickers = list(items.keys())

        """
        list_portfolios_big = self.create_lists_with_limit(
            items[1].keys(), 10, 1000)

        items_10 = self.create_data_and_filter_tickers(
            selection.selected_tickers, 10)

        items_20 = self.create_data_and_filter_tickers(
            selection.selected_tickers, 20)
        """
        # this function is realy danagerouse, remove fast as posible.
        # this will be threaded, 5 for portfolio of 5
        # lists_ = self.return_equal_lists(
        #    items[0], amount_of_lists=5)

        """
        # this will be threaded, 5 for portfolio of 5
        lists_ten = self.return_equal_lists(
            items_10[0], amount_of_lists=6)


        items_20 = items_20[0:100000]

        lists_twen = self.return_equal_lists(
            items_20[0], amount_of_lists=6)
        
        self.continues_portfolio_creation(
            items[1], selection, "thread 1", 10, 10000, 15)
        

        thread1 = threading.Thread(target=self.create_single_options,
                                   args=(items[1], lists_[0], "thread 2"))

        # self.create_single_options(items[1], lists_[0], "thread Leo")
        # self.create_all_options(selection.selected_tickers, 5)
        
        """

        thread0 = threading.Thread(target=self.the_kill_switch,
                                   args=(2, False))
        """
        thread1 = threading.Thread(target=self.create_single_options,
                                   args=(items[1], lists_[0], "thread 1"))

        thread2 = threading.Thread(target=self.create_single_options,
                                   args=(items[1], lists_[1], "thread 2"))

        thread3 = threading.Thread(target=self.create_single_options,
                                   args=(items[1], lists_[2], "thread 3"))
        thread4 = threading.Thread(target=self.create_single_options,
                                   args=(items[1], lists_[3], "thread 4"))
        thread5 = threading.Thread(target=self.create_single_options,
                                   args=(items[1], lists_[4], "thread 5"))
        """

        thread6 = threading.Thread(target=self.continues_portfolio_creation,
                                   args=(items, tickers, "thread 6",
                                         min_amount_tickers,
                                         max_rotations,
                                         max_stocks,
                                         min_sharp_ratio))

        """
        random.shuffle(tickers)

        thread7 = threading.Thread(target=self.continues_portfolio_creation,
                                   args=(items, tickers, "thread 7", 5, 100000, 50))

        random.shuffle(tickers)

        thread8 = threading.Thread(target=self.continues_portfolio_creation,
                                   args=(items, tickers, "thread 8", 5, 100000, 50))

        random.shuffle(tickers)

        thread9 = threading.Thread(target=self.continues_portfolio_creation,
                                   args=(items, tickers, "thread 9", 5, 100000, 50))
        
        print("threads are about to start.")

        
        thread7 = threading.Thread(target=self.create_single_options,
                                   args=(items[1], lists_ten[1], "thread 7"))
        thread8 = threading.Thread(target=self.create_single_options,
                                   args=(items[1], lists_ten[2], "thread 8"))
        thread9 = threading.Thread(target=self.create_single_options,
                                   args=(items[1], lists_ten[3], "thread 9"))
        thread10 = threading.Thread(target=self.create_single_options,
                                    args=(items[1], lists_ten[4], "thread 10"))
        thread11 = threading.Thread(target=self.create_single_options,
                                    args=(items[1], lists_ten[5], "thread 11"))


        thread12 = threading.Thread(target=self.create_single_options,
                                    args=(items[1], lists_twen[0], "thread 12"))
        thread13 = threading.Thread(target=self.create_single_options,
                                    args=(items[1], lists_twen[1], "thread 13"))
        thread14 = threading.Thread(target=self.create_single_options,
                                    args=(items[1], lists_twen[2], "thread 14"))
        thread15 = threading.Thread(target=self.create_single_options,
                                    args=(items[1], lists_twen[3], "thread 15"))
        thread16 = threading.Thread(target=self.create_single_options,
                                    args=(items[1], lists_twen[4], "thread 16"))
        thread17 = threading.Thread(target=self.create_single_options,
                                    args=(items[1], lists_twen[5], "thread 17"))

        """
        threads = []
        # thread0.start()
        """
        thread1.start()
        thread2.start()
        thread3.start()
        thread4.start()
        thread5.start()
        """
        thread6.start()

        """
        thread7.start()
        thread8.start()
        thread9.start()

        
         
        thread10.start()
        thread11.start()

        thread12.start()
        thread13.start()
        thread14.start()
        thread15.start()
        thread16.start()
        thread17.start()

        """
        """
        threads.append(thread1)
        threads.append(thread2)
        threads.append(thread3)
        threads.append(thread4)
        threads.append(thread5)
        """

        threads.append(thread6)
        """
        threads.append(thread7)
        threads.append(thread8)
        threads.append(thread9)
        
        
        threads.append(thread10)
        threads.append(thread11)

        threads.append(thread12)
        threads.append(thread13)
        threads.append(thread14)
        threads.append(thread15)
        threads.append(thread16)
        """
        print('threads have started')
        # Join the threads before
        loop:  bool = True
        while loop:

            for thread in threads:

                if not thread.is_alive():
                    print("Doden threads in portfolio managment")

                    print(thread)

                    thread.join()
                    self.kill_switch = True
                    loop = False
                    break
            continue
        """
        thread1.join()
        thread2.join()
        thread3.join()
        thread4.join()
        thread5.join()
        """

        thread6.join()

        """
        thread7.join()
        thread8.join()
        thread9.join()
        
        """
        return

        """
        thread10.join()
        thread11.join()

        thread12.join()
        thread13.join()
        thread14.join()
        thread15.join()
        thread16.join()

        """
        """
        # the rest one I guess.
        # function with different parameters
        thread1 = threading.Thread(target=self.print_squares,
                                   args=("thread1", [1, 2, 3, 4, 5]))

        thread2 = thread_2 = Thread(target=self.task_2)

        thread3 = threading.Thread(target=self.task_3,
                                   args=())
        threads = []
        # Start the threads
        thread1.start()
        thread2.start()
        thread3.start()

        threads.append(thread1)
        threads.append(thread2)
        threads.append(thread3)

        # Join the threads before
        loop:  bool = True
        while loop:
            for thread in threads:
                if not thread.is_alive():
                    print("Doden threads")

                    thread.join()
                    self.kill_switch = True
                    loop = False
                    break

        # moving further
        thread1.join()
        thread2.join()
        thread3.join()
        """

    def create_all_options(self, list_of_stocks: list, amount_of_stocks: int):

        tickers_out = list_of_stocks
        # create function that creates all kind off ticker combinations
        # 5 - 10.

        list_of_options = []

        # optionally there needs to be a efficiency impementation here.
        # that could be a loop that gets all data and puts it in a dict
        # and gets it out, so it will work way faster.
        ticker_options = {}

        # loops true
        for i in tickers_out:

            try:

                ts_data = create_time_serie_with_kamalstrategie(i)

                ticker_options[i] = ts_data.data
            except:

                tickers_out.remove(i)

        # get the keys so only good stocks will stay ther
        tickers_out = list(ticker_options.keys())

        # gets all posible moves. 5 IS 42k
        options = list(combinations(tickers_out, 5))

        # adds those to list.
        # this options out commanded is fuckt because of wrong python version.
        # res = [list(ele) for ele in options]
        res = [list(ele) for i, ele in enumerate(options)]
        list_of_options.extend(res)

        round_ = 0
        # create dataframes that can be tested.
        for i in range(0, len(list_of_options)):

            round_ += 1

            tickers_selected = list_of_options[i]

            data = self.create_data_frame_of_tickers(
                tickers_selected, ticker_options)

            portfolio = portfolio_constructor_manager(data)

            allowd_to_add = kko_portfolio_gardian(portfolio)

            if allowd_to_add.allowd:

                execute = add_kko_portfolio(portfolio)

        return

    def create_single_options(self, data_service, list_of_options: list, thread_name="thread 1 "):
        """


        Parameters
        ----------
        data_service : TYPE
            DESCRIPTION.
        list_of_options : list
            DESCRIPTION.
        thread_name : TYPE, optional
            DESCRIPTION. The default is "thread 1 ".

        Returns
        -------
        None.

        """

        total_len = len(list_of_options)
        round_ = 0
        # create dataframes that can be tested.
        for i in range(0, len(list_of_options)):

            round_ += 1
            prc_ = round((round_ / total_len) * 100, 2)
            # print("we are running itteration ", round_)

            tickers_selected = list_of_options[i]

            data = self.create_data_frame_of_tickers(
                tickers_selected, data_service)

            portfolio = portfolio_constructor_manager(data)

            allowd_to_add = kko_portfolio_gardian(portfolio)

            if allowd_to_add.allowd:

                execute = add_kko_portfolio(portfolio)

            if self.kill_switch:
                break

        return

    def continues_portfolio_creation(self, data_service,
                                     tickers_in: list,
                                     thread_name="thread 1 ",
                                     amount_per_portfolio: int = 5,
                                     amount_if_itterations_before_next_step=10000,
                                     max_amount_per_portfolio=50,
                                     minimum_sharp_last=0):
        """


        Parameters
        ----------
        data_service : TYPE
            DESCRIPTION.
        tickers_in : list
            DESCRIPTION.
        thread_name : TYPE, optional
            DESCRIPTION. The default is "thread 1 ".
        amount_per_portfolio : int, optional
            DESCRIPTION. The default is 10.
        amount_if_itterations_before_next_step : TYPE, optional
            DESCRIPTION. The default is 10000.
        max_amount_per_portfolio : TYPE, optional
            DESCRIPTION. The default is 50.

        minumim_shrp is set to create default minimum/
        Returns
        -------
        None.

        """
        """

        explaination:
            this script loops 10000 times over an amount of stock, everytime the sharp ratio will
            be added to a list, and when the sharp ratio is 2 stds above the average the count will be
            resetted, so that only the best portfolio's will be added'

            - what if the average go's down? this can result in a infinit loop,, only if score is higher than average will be added.'
            - what if dubble portfolio's come in? that is no problem' on


        """

        amount_per_portfolio = amount_per_portfolio

        # creates list where pseudo portfolio' will be added in.
        pseudo_portfo = []

        start_amount = 5

        # stats.
        itterations_count = []

        # sharp ratio's
        sharp_ratios = [5, 5]

        # var for suggested portfolio.
        suggested_portfolio = None
        max_nr = (len(tickers_in)-1)
        rng = numpy.random.RandomState(2)

        # while killswitch is off: run for ever.
        while not self.kill_switch:

            print("Looking for a portfolio")
            # add itteration
            itterations_count.append(1)

            # if 10000 itterations have been and no sharp is updated
            if len(itterations_count) > amount_if_itterations_before_next_step:

                itterations_count = []
                sharp_ratios = []
                amount_per_portfolio += 1

                if amount_per_portfolio > max_amount_per_portfolio:
                    break

            data = None
            pseudo_portfo = []

            # loop runs untill the portfolio is full.
            while True:

                # creates random number
                number = rng.randint(0, max_nr)

                # selects ticker based on the random number
                ticker = tickers_in[number]

                # if ticker is not in the portfolio' add.
                if ticker not in pseudo_portfo:

                    # add stock to list of portfolio
                    pseudo_portfo.append(ticker)

                    # if the length is equal to max amount, break
                    if len(pseudo_portfo) >= amount_per_portfolio:

                        # set to selected portfolio and break.
                        suggested_portfolio = pseudo_portfo

                        break

                # if there is a kill in the thread. Exit.
                if self.kill_switch:

                    break

            # if there is a kill in the thread, kill it.
            if self.kill_switch:

                break

            # /|\ CREATES PSUEDO PORTFOLIO || \|/ CREATES OPTIONAL PORTFOLIO
            ############################################################################

            # creates data with the portfolio
            data = self.create_data_frame_of_tickers(
                suggested_portfolio, data_service)

            # Remove NA's
            data = data.tail(len(data)-1)

            # check if is contains error's
            if data.isna().values.any():

                # amount of signals
                amount_of_nas = data.isna().sum().sum()
                amount_of_values = data.count().sum()

                # if error rate is higher then 1%, let it go.
                if amount_of_nas / amount_of_values > 0.01:
                    continue

            # creates portfolio
            portfolio = portfolio_constructor_manager(data)

            # checks for sharp ratio managment, if list is empty or not full, fill, if sharp is not above average, remove.
            if not sharp_ratios or len(sharp_ratios) < 100 and minimum_sharp_last == 0:

                sharp_ratios.append(portfolio.Imax_sharp_sharp_ratio)

                if len(sharp_ratios) <= 100:

                    start_amount = statistics.mean(sharp_ratios)

                itterations_count = []

            else:
                start_amount = minimum_sharp_last

            if portfolio.Imax_sharp_sharp_ratio < start_amount:

                continue

            # add sharp ratio
            sharp_ratios.append(portfolio.Imax_sharp_sharp_ratio)

            # checks needed if portfolio is alowed to trade.
            allowd_to_add = kko_portfolio_gardian(portfolio)

            # if alowed
            if allowd_to_add.allowd:

                # add portfolio to the database.
                execute = add_kko_portfolio(portfolio)

                start_amount += 0.05

                itterations_count = []

            if self.kill_switch:
                break

        return

    def create_data_of_tickers(self, list_of_stocks: list):
        tickers_out = list_of_stocks
        # create function that creates all kind off ticker combinations
        # 5 - 10.

        list_of_options = []

        # optionally there needs to be a efficiency impementation here.
        # that could be a loop that gets all data and puts it in a dict
        # and gets it out, so it will work way faster.
        ticker_options = {}

        # loops true
        for i in tickers_out:

            try:

                nr = tickers_out.index(i)
                #prc = nr / len(tickers_out)

                ts_data = create_time_serie_with_kamalstrategie(i)

                ticker_options[i] = ts_data.data

            except:

                tickers_out.remove(i)

        # get the keys so only good stocks will stay ther
        tickers_out = list(ticker_options.keys())

        return ticker_options

    def create_data_and_filter_tickers(self, list_of_stocks: list, amount_of_stocks: int):
        tickers_out = list_of_stocks
        # create function that creates all kind off ticker combinations
        # 5 - 10.

        list_of_options = []

        # optionally there needs to be a efficiency impementation here.
        # that could be a loop that gets all data and puts it in a dict
        # and gets it out, so it will work way faster.
        ticker_options = {}

        # loops true
        for i in tickers_out:

            try:

                nr = tickers_out.index(i)
                #prc = nr / len(tickers_out)

                print(i, " is added to data, we are at =",
                      str(nr), " of ", str(len(tickers_out)))

                ts_data = create_time_serie_with_kamalstrategie(i)

                ticker_options[i] = ts_data.data

            except:

                tickers_out.remove(i)

        # get the keys so only good stocks will stay ther
        tickers_out = list(ticker_options.keys())

        # gets all posible moves. 5 IS 42k
        options = list(combinations(tickers_out, amount_of_stocks))
        res = [list(ele) for i, ele in enumerate(options)]
        list_of_options.extend(res)

        return[list_of_options, ticker_options]

    def create_data_frame_of_tickers(self, tickers: list, data: dict):
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

    def return_equal_lists(self, data, amount_of_lists=3):

        amount_per_list = int(round(len(data)/amount_of_lists))

        chunks = [data[x:x+amount_per_list]
                  for x in range(0, len(data), amount_per_list)]

        return chunks

    def create_lists_with_limit(self, tickers_in: list, mode: str = "random", amount_per_portfolio: int = 10,
                                amount_portfoio: int = 1000):
        """


        Parameters
        ----------
        tickers_in : list
            DESCRIPTION.
        mode : str, optional
            DESCRIPTION. The default is "random".
        amount_per_portfolio : int, optional
            DESCRIPTION. The default is 10.
        amount_portfoio : int, optional
            DESCRIPTION. The default is 1000.

        Returns
        -------
        None.

        """

        list_of_portfolios = []
        pseudo_portfo = []

        while len(list_of_portfolios) < amount_portfoio:

            number = random.randint(0, (len(tickers_in)-1))

            ticker = tickers_in[number]

            if ticker not in pseudo_portfo:
                pseudo_portfo.append(ticker)
                if len(pseudo_portfo) >= amount_per_portfolio:
                    list_of_portfolios.append(pseudo_portfo)
                    pseudo_portfo = []

            if len(list_of_portfolios) >= amount_portfoio:

                break

    def get_last_details(self):
        """
        returns amount of minimaal number, and sharp. 

        Returns
        -------
        int
            DESCRIPTION.
        int
            DESCRIPTION.

        """

        portfolios = database_querys.database_querys.get_portfolio()

        # if there are no portfolios, return 5 and 0
        if portfolios.empty:
            return (5, 0)

        high_amount = portfolios.sort_values(
            ['portfolio_amount', 'total_sharp_y2'], ascending=False)

        height_sharpr = high_amount.total_sharp_y2.to_list()[0]
        height_amount = high_amount.portfolio_amount.to_list()[0]

        return (height_amount, height_sharpr)

    def the_kill_switch(self, days_untill_reset=1, test_modus: bool = False):
        """
        destroys thread after certain time so that the system can reset. 

        Parameters
        ----------
        days_untill_reset : TYPE, optional
            DESCRIPTION. The default is 31.

        Returns
        -------
        None.

        """
        if not test_modus:
            amount_of_sleep = days_untill_reset * 86400

            time.sleep(amount_of_sleep)

            return
        else:

            amount_of_sleep = 10

            time.sleep(amount_of_sleep)

            print("Wakie wakie")

            self.kill_switch = True

            print("hit the switch.")

            return

    def return_all_old_portfolios(self):
        """

        returns a list of portfolios. 

        Returns
        -------
        portfolio_ids : TYPE
            DESCRIPTION.

        """
        portfolios = database_querys.database_querys.get_portfolio()

        portfolio_ids = list(portfolios.portfolio_id)

        return portfolio_ids

    def delete_list_portrfolios(self, list_of_portfolios: list):
        """
        returns list of portfolios

        Parameters
        ----------
        list_of_portfolios : list
            DESCRIPTION.

        Returns
        -------
        None.

        """

        if not list_of_portfolios:
            return

        for i in list_of_portfolios:

            database_querys.database_querys.delete_portfolio_with_id(i)

        return

    def remove_all_portfolios(self):

        portfolios = database_querys.database_querys.get_portfolio()

        portfolio_ids = list(portfolios.portfolio_id)

        for i in portfolio_ids:

            database_querys.database_querys.delete_portfolio_with_id(i)
            print("deleted portfolio : ", i)


class kk_manager(object):

    @staticmethod
    def run_the_portfolio_update_system():

        while True:

            # start portfolio program, will take days before finish.
            portfolio_creator = kko_portfolio_update_manager()


class create_stats(object):

    @staticmethod
    def return_backtest(tickers: list = []):

        tickers_out = tickers
        # create function that creates all kind off ticker combinations
        # 5 - 10.

        list_of_options = []

        # optionally there needs to be a efficiency impementation here.
        # that could be a loop that gets all data and puts it in a dict
        # and gets it out, so it will work way faster.
        ticker_options = {}

        # loops true
        for i in tickers_out:

            try:

                ts_data = create_time_serie_with_kamalstrategie(i)

                ticker_options[i] = ts_data.data
            except:

                raise ValueError

        # get the keys so only good stocks will stay ther
        tickers_out = list(ticker_options.keys())

        tickers_selected = tickers_out

        data = create_stats.create_data_frame_of_tickers(
            tickers_selected, ticker_options)

        portfolio = portfolio_constructor_manager(data)

        balanced_portfolio = data * portfolio.high_sharp_frame.balance.values

        ts_portfolio = balanced_portfolio.mean(axis=1).pct_change().cumsum()

        ts_portfolio = ts_portfolio * 100

        ts_portfolio = ts_portfolio.fillna(0)

        return ts_portfolio

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


class portfolio_kamal:

    tickers: list
    volatiltiy: float
    sharp_ratio_max: float

    perforamnce_y1: float
    perforamnce_y5: float
    perforamnce_y10: float

    drawdown_max_sharp: float
    drawdown_min_vol: float

    balances_low_vol: dict
    balances_high_sharp: dict

    minimum_value: float

    minimum_vol_weight: float
    maximum_vol_weight: float
    minimum_sharp_weight: float
    maximum_sharp_weight: float


class kko_strat_model:
    """
    k stands for kaufman.
    k stands for kamal.
    o stands for optimzed

    """
    portfolio_id: str
    portfolio_strategy: str
    portfolio_amount: int
    list_of_tickers: str
    list_of_balances: str
    list_of_sides: str
    list_of_performance: str
    total_expected_return: float
    total_sharp_y2: float
    total_volatility_y2: float
    createdAt: str


if __name__ == "__main__":

    # archive
    try:

        """
        print("Starting up ...")
        power_object = stock_object.power_stock_object(
            stock_ticker = "ACRX", simplyfied_load = True, periode_weekly = True)
        x = update_kaufman_support.return_kaufman_ma_frame(
            stock__data__frame=power_object.stock_data)
        print(x)
        z = update_kaufman_support.add_kalman_filter_to_data(x)
        print(z)
        y = update_kaufman_support.return_profiles_data(
            z,10,False,power_object.stock_data)
        print(y)
        print("Finnished")
        print("END")
        """

        # tickers = ['ABM', 'PYCR', 'MBINP', 'TWIN', 'IDA', 'ICD', 'OHI', 'ADC', 'ALX', 'ESNT', 'ABNB', 'CWH', 'UTSI', 'QLYS', 'SEIC', 'VLYPP', 'VRAR', 'SNPS', 'AGTI', 'RYAN', 'HEQ', 'DSGN', 'MCHP', 'CNM', 'CD']
        # ding_ = create_correlation_matrix(tickers)
        # print(ding_.data)

        # obj = create_time_serie_with_kamalstrategie("IDA")
        # print(obj)
        # x = create_stats.return_backtest(
        #    tickers=["ADMA", "ALT", "AFYA", "AEPPZ", "ACET"])
        startup_ = kko_portfolio_update_manager()
        # update_kaufman_kalman_analyses.update_full_analyses()
       # update_kaufman_kalman_analyses.update_all()
       # update_trend_performance("AAPL", "D")

    except Exception as e:

        raise Exception("Error with tickers", e)
