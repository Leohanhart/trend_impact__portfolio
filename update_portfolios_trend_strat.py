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
from datetime import datetime, timedelta

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
            #res = [list(ele) for ele in options]
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
            stock_ticker=ticker, simplyfied_load=True, periode_weekly=False)

       # stockdata
        sdata = power_object.stock_data

       # stock.data.change
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

    def __init__(self, list_of_stocks: list, amount_of_stocks: int):

        tickers_out = list_of_stocks
        # create function that creates all kind off ticker combinations
        # 5 - 10.

        tickers_out = xg = tickers_out[1:10]
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
        #res = [list(ele) for ele in options]
        res = [list(ele) for i, ele in enumerate(options)]
        list_of_options.extend(res)

        # create dataframes that can be tested.
        for i in range(0, len(list_of_options)):

            tickers_selected = list_of_options[i]

            data = self.create_data_frame_of_tickers(
                tickers_selected, ticker_options)

            portfolio = portfolio_constructor_manager(data)

            allowd_to_add = kko_portfolio_gardian(portfolio)

            if not allowd_to_add.allowd:

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

        tickers = portfolio.high_sharp_frame.ticker.to_list()
        serialized_list_of_tickers = json.dumps(tickers)

        model.list_of_tickers = serialized_list_of_tickers
        # create an

        # get sides.
        # get amount,


class create_kko_tickers_selection:

    selected_tickers: list

    def __init__(self, methode_one: bool = False, methode_two: bool = False):
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


class kko_portfolio_gardian:

    allowd: bool = False

    # allows portfolio's that have one stock that les than 50 of average.
    lower_boundery = 50

    def __init__(self, portfolio):
        """
        Criteria:
            - mainly build for max sharp.

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

        # implement logic here.
        amount_stocks = self.return_amount_of_stocks(portfolio)
        boundery_low = 100/amount_stocks * (self.lower_boundery / 100)

        min_shapr = portfolio.min_sharp * 100

        if min_shapr < self.lower_boundery:
            self.allowd = False
            return

        self.allowd = True

        return

    def return_amount_of_stocks(self, p):
        amount = len(p.portfolio_strat_high_sharp_stocks)
        return amount


class kko_portfolio_update_manager:

    def __init__(self):

        # get the tickers
        selection = create_kko_tickers_selection(methode_one=True)

        # this will be threaded, 5 for portfolio of 5
        insert = create_kko_portfolios(selection.selected_tickers, 5)
        # the rest one I guess.


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
        power_object = stock_object.power_stock_object(stock_ticker = "ACRX", simplyfied_load = True, periode_weekly = True)
        x = update_kaufman_support.return_kaufman_ma_frame(stock__data__frame=power_object.stock_data)   
        print(x)
        z = update_kaufman_support.add_kalman_filter_to_data(x)
        print(z)
        y = update_kaufman_support.return_profiles_data(z,10,False,power_object.stock_data)
        print(y)
        print("Finnished")
        print("END")
        """

        #tickers = ['ABM', 'PYCR', 'MBINP', 'TWIN', 'IDA', 'ICD', 'OHI', 'ADC', 'ALX', 'ESNT', 'ABNB', 'CWH', 'UTSI', 'QLYS', 'SEIC', 'VLYPP', 'VRAR', 'SNPS', 'AGTI', 'RYAN', 'HEQ', 'DSGN', 'MCHP', 'CNM', 'CD']
        #ding_ = create_correlation_matrix(tickers)
        # print(ding_.data)

        #obj = create_time_serie_with_kamalstrategie("IDA")
        # print(obj)
        x = kko_portfolio_update_manager()

        # update_kaufman_kalman_analyses.update_full_analyses()
       # update_kaufman_kalman_analyses.update_all()
       # update_trend_performance("AAPL", "D")

    except Exception as e:

        raise Exception("Error with tickers", e)
