# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 10:50:48 2022

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


"""

We create two databases: ONE for the current state of the measure ment. 
                        : TWO. we build this one where we connect date archive varibles
                        so that we can build an archive, cluster the data and create a 
                        time serie of the archive. The only thing we need is to 
                        - Create a system that wins specefic data if lost( missing days mainly)
                        - Create a stock_analyses class that load this data, into a pickle file
                        so it can be load quickly. 
                        
                        We can use these dataframes for statiscical analsyes in many ways. 
                        We can cluster these analyses with other archives if possible. 
                        


"""


class update_all_trend_analyses(object):
    pass


class update_kaufman_kalman_analyses(object):

    def update_all():
        """


        Parameters
        ----------
        object : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """

        # load periodes
        periodes = ["D"]

        # load tickers
        tickers = database_querys.database_querys.get_all_active_tickers()

        trade_data = None

        for periode_in in periodes:
            for ticker in tickers:

                if periode_in == "D":

                    try:
                        power_object = stock_object.power_stock_object(
                            stock_ticker=ticker, simplyfied_load=True, periode_weekly=False)

                        model = update_kaufman_support.return_full_analyses_dict(
                            stock_data=power_object.stock_data, ticker_name=power_object.stock_ticker, max_levels=10, periode="D")

                        print(model.__dict__)
                        database_querys.database_querys.update_analyses_trend_kamal(
                            model)

                        del power_object
                        del model

                    except Exception as e:
                        continue

                elif periode_in == "W":

                    try:

                        power_object = stock_object.power_stock_object(
                            stock_ticker=ticker, simplyfied_load=True, periode_weekly=True)

                        model = update_kaufman_support.return_full_analyses_dict(
                            stock_data=power_object.stock_data, ticker_name=power_object.stock_ticker, max_levels=10, periode="W")

                        database_querys.database_querys.update_analyses_trend_kamal(
                            model)

                        del power_object
                        del model

                    except Exception as e:
                        continue

                else:
                    continue

    @staticmethod
    def update_full_analyses():
        """

        updates all tickers in analyses_trend_kamal_archive and analyses_trend_kamal_performance. 



        Parameters
        ----------
        object : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        # load periodes
        periodes = ["D"]

        # load tickers
        tickers = database_querys.database_querys.get_all_active_tickers()

        trade_data = None

        for periode_in in periodes:
            for ticker in tickers:

                #
                if periode_in == "D":

                    try:

                        power_object = stock_object.power_stock_object(
                            stock_ticker=ticker, simplyfied_load=True, periode_weekly=False)

                        archive_data = update_archive_kaufmal(stock_data=power_object.stock_data, periode=periode_in,
                                                              min_range=30, ticker=ticker)

                        performance_specs = update_trend_performance(
                            ticker, periode_in)

                    except Exception as e:

                        print(e)

                else:
                    continue


class update_kaufman_support(object):

    @staticmethod
    def return_full_analyses_dict(stock_data,
                                  ticker_name: str = "",
                                  max_levels: int = 10,
                                  periode: str = None
                                  ):
        """
        returns full dict with ['profile', 'profile_std', 'trend', 'duration', 'current_yield', 'max_drawdown', 'exp_return', 'max_yield']

        Parameters
        ----------
        stock_data : TYPE
            DESCRIPTION.

        Returns
        -------
        dict_info : TYPE
            DESCRIPTION.

        """

        kaufman_ma = update_kaufman_support.return_kaufman_ma_frame(
            stock__data__frame=stock_data)

        kaufman_and_kamal = update_kaufman_support.add_kalman_filter_to_data(
            kaufman_ma)

        dict_info = update_kaufman_support.return_profiles_data(dataframe_input=kaufman_and_kamal,
                                                                max_levels=max_levels,
                                                                std_based_levels=False,
                                                                stock__data__frame=stock_data
                                                                )

        dict_info["ticker"] = ticker_name
        dict_info["periode"] = periode
        # Turns a dictionary into a class
        dict_info = update_kaufman_support.package_dict_in_class(dict_info)

        return dict_info

    @staticmethod
    def package_dict_in_class(my_dict):
        """
        creates class with dict. 

        Parameters
        ----------
        my_dict : TYPE
            DESCRIPTION.

        Returns
        -------
        class_object : TYPE
            DESCRIPTION.

        """

        class Dict2Class(object):

            def __init__(self, my_dict):

                for key in my_dict:
                    setattr(self, key, my_dict[key])

        class_object = Dict2Class(my_dict)

        return class_object

    @staticmethod
    def KAMA(price, n=10, pow1=2, pow2=30):
        ''' kama indicator '''
        ''' accepts pandas dataframe of prices '''

        absDiffx = abs(price - price.shift(1))

        ER_num = abs(price - price.shift(n))
        ER_den = ER_num.rolling(n).sum()
        ER = ER_num / ER_den

        sc = (ER*(2.0/(pow1+1)-2.0/(pow2+1.0))+2/(pow2+1.0)) ** 2.0

        answer = np.zeros(sc.size)
        N = len(answer)
        first_value = True

        for i in range(N):
            if sc[i] != sc[i]:
                answer[i] = np.nan
            else:
                if first_value:
                    answer[i] = price[i]
                    first_value = False
                else:
                    answer[i] = answer[i-1] + sc[i] * (price[i] - answer[i-1])
        return answer

    @staticmethod
    def return_kaufman_ma_frame(stock__data__frame=None, return_as_list: bool = True):
        """


        Parameters
        ----------
        stock__data__frame : TYPE, optional
            DESCRIPTION. The default is None.

        Returns
        -------
        None.

        """
        # dit organiseert een lijst met
        kama = update_kaufman_support.KAMA(
            stock__data__frame.Close, n=10, pow1=2, pow2=30)
        data = kama.tolist()
        if return_as_list:
            # remove Na's
            data = [x for x in data if math.isnan(x) == False]
            return data
        else:
            df = pd.DataFrame(data)
            return df

    @staticmethod
    def add_kalman_filter_to_data(input_data=None):
        """


        Parameters
        ----------
        input_data : TYPE, optional
            DESCRIPTION. The default is None.

        Returns
        -------
        None.

        """

        # created dataframe with index of lengt
        x = pd.DataFrame(input_data, index=np.arange(0, len(input_data), 1))

        # setup data in Dataframe with fitting length.

        kf = KF(initial_state_mean=1, n_dim_obs=1)

        #kf = kf.em(x.dropna().values, n_iter=5)

        state_means, _ = kf.filter(x.dropna().values)

        d = {'a': np.asarray(x), 'b': np.asarray(state_means)}

        sm = pd.DataFrame(state_means, index=x.index, columns=['state'])

        sma = x.rolling(window=10).mean()

        x['Data'] = sm  # kalman filter.

        x['rolling'] = sma

        return x

    def retrun_volatiltiy(stock_data_frame=None):
        """
        source : https://stackoverflow.com/questions/43284304/how-to-compute-volatility-standard-deviation-in-rolling-window-in-pandas

        returns bullshit.

        Parameters
        ----------
        stock_data_frame : TYPE, optional
            DESCRIPTION. The default is None.

        Returns
        -------
        None.

        """

        # set var
        df = stock_data_frame
        df.tail(252)

        window = 21  # trading days in rolling window
        days_per_year = 252  # trading days per year
        ann_factor = days_per_year / window

        df['log_rtn'] = np.log(df['Close']).diff()

        # Var Swap (returns are not demeaned)
        df['real_var'] = np.square(df['log_rtn']).rolling(
            window).sum() * ann_factor
        df['real_vol'] = np.sqrt(df['real_var'])

        # Classical (returns are demeaned, dof=1)
        df['real_var'] = df['log_rtn'].rolling(window).var() * ann_factor
        df['real_vol'] = np.sqrt(df['real_var'])

        volatility = round(float(df.real_vol.tail(1))*100, 2)

        return volatility

    def return_max_drawdown(stock__data__frame=None, position_side: int = 1, return_time_serie: bool = False):
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

    @staticmethod
    def return_profiles_data(dataframe_input, max_levels: int = 5, std_based_levels: bool = False, stock__data__frame: type = None):
        """


        Parameters
        ----------
        dataframe_input : TYPE
            DESCRIPTION.
        max_levels : int, optional
            DESCRIPTION. The default is 5.
        std_based_levels : bool, optional
            DESCRIPTION. The default is False.
        stock__data__frame : type, optional
            DESCRIPTION. The default is None.

        Returns
        -------
        output_data : TYPE
            DESCRIPTION.

        """

        # sets dict
        output_data = {}

        # sets varible
        x = dataframe_input

        # create data exctractions
        y = x.Data.pct_change()
        z = x.Data.diff()

        # tails data so begin error is deleted
        y = y.tail(len(y)-5)

        # sets last profile
        last_dp = float(y.tail(1))

        # detirmen trend level.
        # if positive
        if last_dp > 0:

            # sets to the max
            max_dp = y.max()
            # Extracts levels
            levels = max_dp / max_levels
            # extracts profile.
            profile = round(last_dp / levels)
            # saves data
            output_data["profile"] = profile

            # also pics std profile
            op = pd.DataFrame(y)
            # filters data to positive datapoints
            xp = op[op.Data > 0]
            # sts std profile.
            output_data["profile_std"] = round(
                last_dp / (float(xp.std()) * 3 / max_levels))

        else:

            # same as above
            max_dp = y.min()
            levels = max_dp / max_levels

            profile = round(last_dp / levels)
            output_data["profile"] = profile

            op = pd.DataFrame(y)
            xp = op[op.Data < 0]
            output_data["profile_std"] = round(
                last_dp / (float(xp.std()) * 3 / max_levels))

        ###
        # determen trend direction
        last_dp_trend = float(z.tail(1))
        if last_dp_trend > 0:
            output_data["trend"] = 1
        else:
            output_data["trend"] = -1

        ###
        # durretation of a trend.
        for i in range(1, len(z)):
            if last_dp_trend > 0:
                if float(z.tail(i).min()) < 0:
                    output_data["duration"] = i
                    break
            if last_dp_trend < 0:
                if float(z.tail(i).max()) > 0:
                    output_data["duration"] = i
                    break

        # if stock data is not 0 :?

        # tails data to valide point
        sdata = stock__data__frame.tail(len(z))

        # takes periode of duration
        data_total = sdata.tail(output_data["duration"])

        # positive signal, extract high
        if last_dp_trend > 0:

            # sets prices, max = max price, cur_price = currentprice
            max_price = round(data_total.High.max(), 2)
            startprice = round(float(data_total.Open.head(1)), 2)
            min_price = round(data_total.High.min(), 2)
            cur_price = round(float(data_total.Close.tail(1)), 2)
            max_yield = round(((max_price/startprice)-1)*100, 2)
            current_yield = round(((cur_price/startprice)-1)*100, 2)
            max_drawdown = round(update_kaufman_support.return_max_drawdown(
                stock__data__frame=data_total, position_side=1, return_time_serie=False), 2)
            exp_return = round(current_yield / output_data["duration"], 2)

            output_data["current_yield"] = current_yield
            output_data["max_drawdown"] = max_drawdown
            output_data["exp_return"] = exp_return
            output_data["max_yield"] = max_yield

        else:
            # sets prices, max = max price, cur_price = currentprice
            min_price = round(data_total.High.min(), 2)
            startprice = round(float(data_total.Open.head(1)), 2)
            cur_price = round(float(data_total.Close.tail(1)), 2)
            max_yield = round((((min_price/startprice)-1)*100)*-1, 2)
            current_yield = round((((cur_price/startprice)-1)*100)*-1, 2)
            max_drawdown = round(update_kaufman_support.return_max_drawdown(
                stock__data__frame=data_total, position_side=-1, return_time_serie=False), 2)
            exp_return = round(current_yield / output_data["duration"], 2)

            output_data["current_yield"] = current_yield
            output_data["max_drawdown"] = max_drawdown
            output_data["exp_return"] = exp_return
            output_data["max_yield"] = max_yield

        output_data["volatility"] = update_kaufman_support.retrun_volatiltiy(
            stock_data_frame=stock__data__frame)

        # start date
        date = data_total.tail(1).index[0]

        #
        output_data["date_end"] = date.day

        #
        output_data["month_end"] = date.month

        #
        output_data["year_end"] = date.year

        #
        output_data["weeknr_end"] = date.weekofyear

        # does the same for the startdate of the stock.
        date = data_total.head(1).index[0]

        #
        output_data["date_start"] = date.day

        #
        output_data["month_start"] = date.month

        #
        output_data["year_start"] = date.year

        #
        output_data["weeknr_start"] = date.weekofyear

        """
        We want - max yields, sinds then, 
        We want - avg. yield_per_periode(W and D seperated)
        We want - current yield. 
        """

        return output_data


class update_archive_kaufmal():
    """
    TEST: if old datapoint gets refershed
            if next itteration matches database if exsits, so no fill errror loop occures.
    """

    data_slides: list = []

    # error handling
    # turend on in the start to prevent malicues stocks to be procesed.
    error_check: bool = True
    errors_total: int = 0
    error_exsits: int = 0

    # last date
    last_date_use_year: int = 0
    last_date_use_month: int = 0
    last_date_use_date: int = 0
    last_durration: int = -1

    def __init__(self, stock_data, periode: str = "D", min_range: int = 30, ticker: str = ""):

        # if problems, delete all data.
        #

        stock_data = stock_data

        # fix lengt, used for loop true right data.
        i = len(stock_data)

        # if lenght is not good, return.
        if len(stock_data) < 30:

            raise Exception("DATA_ERROR", "Data is not long enough")

        # set vars
        first_it: bool = True

        # loops true archive manager
        while True:

            # add data
            work_data = stock_data.head(i)

            model = update_kaufman_support.return_full_analyses_dict(stock_data=work_data, ticker_name=ticker, max_levels=10,
                                                                     periode=periode
                                                                     )

            # stockdata frame
            self.data_slides.append(model)

            # check error.
            try:

                self.process_errors(model)

            except:
                break
                self.delete_all_stocks_inserted()

            # check if refresh is neaded.
            # get last model.
            try:

                old_model = self.get_last_model(ticker=ticker, periode=periode)

                if self.check_if_need_overwrite(old_model, model):
                    # delete old model.

                    database_querys.database_querys.update_analyses_trend_kamal_archive(
                        model)

                    i = i - model.duration

                    continue

            except:
                print("No archive found")

            report = database_querys.database_querys.update_analyses_trend_kamal_archive(
                model)

            if report["status"] == "EXISTS":
                break

           # print(self.__dict__)
            # reset lengt
            i = i - model.duration

            continue

        return

    def __incomming_error_check(self, data):
        if len(data) < 30:
            raise Exception("DATA_ERROR", "Data is not long enough")
        else:
            return

    def delete_all_stocks_inserted(self):
        """
        Deletes all inserted stocks.

        Returns
        -------
        None.

        """
        for i in range(0, len(self.data_slides)):
            database_querys.database_querys.delete_analyses_trend_kamal_archive(
                self.data_slides[i])

    def check_if_need_overwrite(self, model_old, model_new):

        if(model_old.year_start == model_new.year_start and
           model_old.month_start == model_new.month_start and
           model_old.date_start == model_new.date_start):
            return True
        else:
            return False

    def process_errors(self, model):

        # set duration or add error
        self.process_durration_error(model)

        if self.check_for_failure():
            raise Exception("ERRORS_OCCURED")

    def check_for_failure(self):
        if self.errors_total > 5:
            return True

    def process_durration_error(self, model):
        if self.last_durration == -1:
            self.last_durration = model.duration
        else:
            if self.last_durration == model.duration:
                self.errors_total += 1
            else:
                self.errors_total = 0
                self.last_durration = model.duration

        return

    def get_last_model(self, ticker: str, periode: str):

        # get data.
        report = database_querys.database_querys.get_trend_kalman_data(
            ticker=ticker, periode=periode)

        # tails data.
        report = report.tail(1)

        # unpacks the data.
        new_raport = report.to_dict(orient="records")

        # create model of data.
        raport_class = update_kaufman_support.package_dict_in_class(
            new_raport[0])

        return raport_class


class update_trend_performance:
    """
    - AVG return / volatility. We need that for later. 
    - 2 years, 5 years. 

    IMPRORTANT, create empty field for score, after analyses, a score 
    will be added on behaf of profitibly, focussing for seperation. 
    Score from on to 10. 

    """

    def __init__(self, ticker, periode):

        # get the data
        df = database_querys.database_querys.get_trend_kalman_data(
            ticker=ticker, periode=periode)

        # error check.
        if len(df) < 10 and len(df) > 2:
            return

        # start with two year parrameters
        df2 = df_last_two_years = self.filter_pandas_years(df, 2)

        details_two_years = self.create_performance_details(df2, "y2")

        df5 = df_last_two_years = self.filter_pandas_years(df, 5)

        details_five_years = self.create_performance_details(df5, "y5")

        overall_performance = self.create_performance_details(df, "all")

        all_data = {**details_two_years, **
                    details_five_years, **overall_performance}

        all_data["ticker"] = ticker
        all_data["periode"] = periode
        all_data["profible_profile"] = 0

        model = all_data

        model = update_kaufman_support().package_dict_in_class(model)

        database_querys.database_querys.update_analyses_trend_kamal_performance(
            model)

    def create_performance_details(self, dataframe, name=""):
        df = dataframe

        data = {}

        # strips the dataframe lenght
        data["amount_of_trades_" + name] = ty_amount_of_trades = len(df)

        # sets total return
        data["total_return_" +
             name] = ty_total_return = round(df.current_yield.sum(), 2)

        # total mean
        data["total_average_return_" +
             name] = ty_total_mean_return = round(df.current_yield.mean(), 2)

        # sets
        ty_amount_positive_trades = len(df.loc[df['current_yield'] > 0])

        # sets amoutn negative trades.
        ty_amount_negative_trades = len(df.loc[df['current_yield'] < 0])

        # set percentage -- needed for volatility returns.

        try:
            ty_perctage_positive_trades = round(
                ty_amount_positive_trades / ty_amount_of_trades, 2)*100
        except:
            ty_perctage_positive_trades = 0

        data["total_profitible_trades_" + name] = ty_perctage_positive_trades = round(
            ty_amount_positive_trades / ty_amount_of_trades, 2)*100

        try:
            # sets percentage negative trades.

            ty_perctage_negative_trades = round(
                ty_amount_negative_trades / ty_amount_of_trades, 2)*100

        except:

            ty_perctage_negative_trades = 0

        try:
            # sets mean, lost trades.
            ty_average_negative_trades = round(
                df.loc[df['current_yield'] < 0].exp_return.mean())

        except:
            ty_average_negative_trades = 0

        try:
            # sets mean, winning trades.
            ty_average_positive_trades = round(
                df.loc[df['current_yield'] > 0].exp_return.mean())

        except:

            ty_average_positive_trades = 0
        # set trades long
        ty_trades_long = len(df.loc[df['trend'] > 0])

        ty_trades_short = len(df.loc[df['trend'] < 0])

        ty_expected_return = df.exp_return.mean()

        try:

            ty_exp_return_volatility = round(self.get_expected_return_volatility(ty_perctage_positive_trades,
                                                                                 ty_perctage_negative_trades,
                                                                                 ty_average_positive_trades,
                                                                                 ty_average_negative_trades), 2)
        except:

            ty_exp_return_volatility = 0

        data["total_exp_volatility_" + name] = ty_exp_return_volatility

        data["total_volatility_" +
             name] = ty_volatility = round(df.volatility.mean())

        data["total_sharp_" +
             name] = ty_sharp = round(ty_total_mean_return / ty_volatility, 2)

        return data

    def get_expected_return_volatility(self,
                                       chance_a: float,
                                       chance_b: float,
                                       exp_return_a: float,
                                       exp_return_b: float
                                       ):
        """

        https://www.youtube.com/watch?v=bE1Uq-sUFh8
        Parameters
        ----------
        chance_a : float
            DESCRIPTION.
        change_b : float
            DESCRIPTION.
        exp_return_a : float
            DESCRIPTION.
        exp_return_b : float
            DESCRIPTION.

        Returns
        -------
        None.

        """
        outcome_a = chance_a * (exp_return_a - exp_return_b)
        outcome_b = chance_b * (exp_return_b - exp_return_a)
        variance = outcome_a + outcome_b
        volatility = sqrt(variance) * 100

        return volatility

    def filter_pandas_years(self, df, amount_of_years=2):

        last_row = df.tail(1)

        start_year = int(last_row.year_end) - amount_of_years

        df = df.loc[df['year_end'] > start_year]

        return df


"""

For portfolio selection we will create a correlation matrix for all stocks 
with the higher returns. So level of profitbilty need to be add. 

After that we will look at the Expected return and the volatility of expected return (https://www.google.com/search?q=expected+return+volatility&oq=expected+return+volatility&aqs=chrome..69i57.8799j0j7&sourceid=chrome&ie=UTF-8#kpvalbx=_hfN4Y_X_DtWI9u8PrJCb-AE_29)

                                                                                      
"""


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
            df = df.head(25)
            #
            tickers_for_portfolio = list(df.id.values)

            # create correlation matrix
            correlations_tickers = create_correlation_matrix(
                tickers=tickers_for_portfolio)

            # one way to create a dataframe
            df = pd.DataFrame(correlations_tickers.data)

            df = df.sort_values(by=["correlation"])

            # this one creates tickers

            tickers_out = correlations_tickers.ticker

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
        #x = update_kaufman_kalman_analyses.update_full_analyses()

        # update_kaufman_kalman_analyses.update_full_analyses()
        update_kaufman_kalman_analyses.update_all()
       # update_trend_performance("AAPL", "D")

    except Exception as e:

        raise Exception("Error with tickers", e)
