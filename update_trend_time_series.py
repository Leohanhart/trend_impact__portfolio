# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 12:29:13 2023

@author: Gebruiker
"""

import database_querys_main as database_querys
import stock_analyses_with_ticker_main as stock_analyses_with_ticker
from core_scripts.stock_data_download import power_stock_object as stock_object
from core_update.update_analyses import update_support
from datetime import datetime, timedelta, date
import pandas as pd
from datetime import timedelta
import atexit
import multiprocessing
import yfinance as yf

# import torch
# import torch.nn as nn
# import torch.optim as optim
import numpy as np


class update_trend_timeseries:
    @staticmethod
    def update():
        try:
            manager = create_timeseries_manager()
        except Exception as e:
            database_querys.database_querys.add_log_to_logbook(
                "Update Trend timeseries faild, or prevent blocking ", e
            )
        # aggergate the timeseries (Ceprated functions)
        return


class update_trend_support:
    @staticmethod
    def get_dict_dates_name(date_str: str = "2000-01-01"):
        """
        returns dict with businessdates form a certain date.

        Parameters
        ----------
        date_str : str, optional
            DESCRIPTION. The default is "2000-01-01".

        Returns
        -------
        None.

        """
        # Convert string date to pandas Timestamp object
        start_date = pd.Timestamp(date_str)

        # Get today's date as a pandas Timestamp object
        end_date = pd.Timestamp(date.today())

        # Create an array of business days between start and end dates (inclusive)
        business_days = pd.date_range(start=start_date, end=end_date, freq="B")

        # Use the update_trend_support module to create a dictionary of dates
        # with boolean values indicating whether each date is a business day
        dates = update_trend_support.return_dict_of_dates(business_days)

        # Return the dictionary of dates
        return dates

    @staticmethod
    def get_dates():
        """
        returns df with business days from 1980 till now

        Returns
        -------
        business_days : TYPE
            DESCRIPTION.

        """

        # get business days from 1980 till now.
        start_date = pd.Timestamp("2000-01-01")
        end_date = pd.Timestamp(date.today())

        # get frame
        business_days = pd.date_range(start=start_date, end=end_date, freq="B")

        return business_days

    @staticmethod
    def return_dict_of_dates(frame):
        """
        returns

        Parameters
        ----------
        frame : TYPE
            DESCRIPTION.

        Returns
        -------
        dict_of_dates_list : TYPE
            DESCRIPTION.

        """

        dict_of_dates_list = [
            {"year": d.year, "month": d.month, "date": d.day} for d in frame
        ]

        return dict_of_dates_list


class create_timeseries_manager:
    def __init__(self):
        # load industry's

        self.industrys = (
            database_querys.database_querys.get_all_active_industrys()
        )

        self.sectors = database_querys.database_querys.get_all_active_sectors()

        self.remove_bullshit()

        # load all sectors
        self.update_all()

    def remove_bullshit(self):
        self.sectors = [item for item in self.sectors if item != "Unkown"]
        self.industrys = [item for item in self.industrys if item != "Unkown"]

        self.sectors = [item for item in self.sectors if item != "nan"]
        self.industrys = [item for item in self.industrys if item != "nan"]

        self.sectors = [item for item in self.sectors if item != "ETF"]
        self.industrys = [item for item in self.industrys if item != "ETF"]

    def update_all(self):
        """
        Updates all avalible updates.

        Returns
        -------
        None.

        """

        self.update_main_analyses()
        self.update_all_sectors()
        # self.update_all_industrys()

    def update_main_analyses(self):
        # recovers last date
        date = self.recover_last_date("ALL")

        # generates date
        dates = update_trend_support.get_dict_dates_name(date_str=date)

        # creates data.
        data = get_trend_analyses_timeseries.get_analyses_ts(
            tickers=[], dates=dates, name_of_analyses="ALL"
        )

        self.save_the_tts_dataframe(data)

    def update_all_industrys(self):
        # first need to add data before fetch.

        for name in self.industrys:
            # get all tickers
            tickers = (
                database_querys.database_querys.get_all_stocks_with_industry(
                    name_industry=name
                )
            )

            # recovers last date
            date = self.recover_last_date(name)

            # generates date
            dates = update_trend_support.get_dict_dates_name(date_str=date)

            # creates data.
            data = get_trend_analyses_timeseries.get_analyses_ts(
                tickers=tickers, dates=dates, name_of_analyses=name
            )

            self.save_the_tts_dataframe(data)

    def update_all_sectors(self):
        # first need to add data before fetch.

        for name in self.sectors:
            # get all tickers
            tickers = (
                database_querys.database_querys.get_all_stocks_with_sector(
                    name_sector=name
                )
            )

            # recovers last date
            date = self.recover_last_date(name)

            # generates date
            dates = update_trend_support.get_dict_dates_name(date_str=date)

            # creates data.
            data = get_trend_analyses_timeseries.get_analyses_ts(
                tickers=tickers, dates=dates, name_of_analyses=name
            )

            self.save_the_tts_dataframe(data)

            continue

    def save_the_tts_dataframe(self, df):
        """
        Saves a dataframe to a timeserie

        Parameters
        ----------
        df : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        try:
            database_querys.database_querys.add_trend_timeserie(df)

        except AttributeError:
            pass

        return

    def retreive_last_update(self, name: str):
        try:
            df = database_querys.database_querys.get_trend_timeseries_data(
                name
            )

        except UnboundLocalError:
            print("troubles")

        return df

    def recover_last_date(self, name):
        """
        recovers the last date of analyse

        Parameters
        ----------
        name : TYPE
            DESCRIPTION.

        Returns
        -------
        date : TYPE
            DESCRIPTION.

        """
        # retreive last date
        data = self.retreive_last_update(name)

        if data.empty:
            return "2000-01-01"

        data = data.sort_values(by="date", ascending=False)

        data = data.date.values[0]

        # check if the variable is a datetime object, if so return it in string with right format
        # if not, check if it can be converted(to see if format matches) otherwise just return startformat.
        try:
            data = datetime.datetime.strptime(data, "%Y-%m-%d")
        except ValueError:
            return "2000-01-01"
        finally:
            return data

        if isinstance(data, datetime.datetime):
            # convert the datetime object to a string with year-month-day format
            data = data.strftime("%Y-%m-%d")
            return data


class get_trend_analyses_timeseries:
    """
    Should it save?
    Should it do all the work?
    """

    @staticmethod
    def get_analyses_ts(
        tickers: list = [], dates: list = [], name_of_analyses: str = ""
    ):
        tickers_all = []

        data_frame = None
        for date in dates:
            # get the date items
            year, month, date = get_trend_ts_support.extract_date_info(date)

            # get the database function
            func = get_trend_ts_support.return_query_function()

            # get dateframe with data
            frame = func(tickers, year, month, date)

            # potentially get tickers that are missing.

            # aggegrate dataframe
            slide = get_trend_ts_support.aggegrate_the_ts_date(
                frame, name_of_analyses
            )

            # create a dataframe/
            df = get_trend_ts_support.create__dataframe__from__series(slide)

            # rename the df
            df = get_trend_ts_support.rename_columns(df)

            # create index with date
            df = get_trend_ts_support.add_index_date(df, year, month, date)

            if data_frame is None:
                # if it is, assign the second DataFrame to the variable
                data_frame = df
            else:
                # if it isn't, append the second DataFrame to the bottom of the first DataFrame
                data_frame = pd.concat([data_frame, df])

        data_frame = data_frame.head(len(data_frame) - 1)

        return data_frame


class get_trend_ts_support:
    @staticmethod
    def add_index_date(df, year, month, date):
        """
        addes a date to the index of the dataframe

        Parameters
        ----------
        df : TYPE
            DESCRIPTION.
        year : TYPE
            DESCRIPTION.
        month : TYPE
            DESCRIPTION.
        date : TYPE
            DESCRIPTION.

        Returns
        -------
        df : TYPE
            DESCRIPTION.

        """
        dt_object = datetime(year, month, date)

        # create a DataFrame from the series with the datetime object as index
        date_ = pd.to_datetime(dt_object)

        # add a date column
        # date = pd.to_datetime('2022-04-15')
        df["date"] = date_

        # set the date column as the index
        df.set_index("date", inplace=True)

        return df

    @staticmethod
    def create__dataframe__from__series(df):
        """


        Parameters
        ----------
        df : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        df = df.to_frame().T
        return df

    @staticmethod
    def rename_columns(df):
        """

        Renames the colums from the dataframe

        Parameters
        ----------
        df : TYPE
            DESCRIPTION.

        Returns
        -------
        df : TYPE
            DESCRIPTION.

        """
        new_cols = [
            "name",
            "trend",
            "duration",
            "profile",
            "profile_std",
            "volatility",
            "current_yield",
            "max_drawdown",
            "exp_return",
            "max_yield",
            "longs",
            "shorts",
            "total",
        ]

        # Rename the columns of the dataframe
        df = df.reindex(columns=new_cols)

        return df

    @staticmethod
    def aggegrate_the_ts_date(df, name):
        # drop unnecessary columns
        df = df.drop(
            columns=[
                "date_start",
                "weeknr_start",
                "year_end",
                "month_end",
                "date_end",
                "weeknr_end",
                "periode",
            ]
        )

        # compute mean of certain columns
        mean_cols = [
            "trend",
            "duration",
            "profile",
            "profile_std",
            "volatility",
            "current_yield",
            "max_drawdown",
            "exp_return",
            "max_yield",
        ]

        # aggegrate the
        df_mean = df[mean_cols].mean()

        # compute conditional sums of 'trend' column
        df_longs = df.loc[df["trend"] == 1, "trend"].sum()
        df_shorts = df.loc[df["trend"] == -1, "trend"].sum()

        # create new columns for conditional sums
        df_mean["longs"] = (
            df["trend"].apply(lambda x: x if x == 1 else 0).sum()
        )
        df_mean["shorts"] = (
            df["trend"].apply(lambda x: x if x == -1 else 0).sum()
        )
        df_mean["total"] = int(len(df))

        df_mean["name"] = name

        # print resulting dataframe
        return df_mean

    @staticmethod
    def extract_date_info(date_dict):
        """
        returns itmes of date dict

        Parameters
        ----------
        date_dict : TYPE
            DESCRIPTION.

        Returns
        -------
        year : TYPE
            DESCRIPTION.
        month : TYPE
            DESCRIPTION.
        date : TYPE
            DESCRIPTION.

        """
        year = date_dict["year"]
        month = date_dict["month"]
        date = date_dict["date"]
        return year, month, date

    @staticmethod
    def return_query_function():
        """
        returns a function that does query

        Returns
        -------
        func : TYPE
            DESCRIPTION.

        """

        func = (
            database_querys.database_querys.get_trend_archive_with_tickers_and_date
        )
        return func

    # cleanup function to terminate any remaining processes
    @staticmethod
    def cleanup():
        for process in multiprocessing.active_children():
            process.terminate()


class extent_trend_analsyes:
    """
    what do you get in this class?

    Everything you need is in this class

    Timeseries that can be used in machine learning are found in :
        # creating df's off all performance
        self.df_performance_combined

        # creating trends.
        self.df_trend_combined

    if you need profile calculation you can do ("ALL" is where the sector name is) :

        # create "all" dataframe
        ts_all = self.retreive_trend_timeserie("ALL")

        # first does it for all, then loop true all sectors.
        df = self.create_clean_trend_based_timeserie(ts_all)

        # get performance
        df_perforamnce_all = self.add_perofmance_indicator(df, "ALL")



    """

    sector_tickers = {
        "ALL": "^GSPC",
        "Technology": "XLK",
        "Healthcare": "XLV",
        "Consumer Cyclical": "XLY",
        "Consumer Defensive": "XLP",
        "Energy": "XLE",
        "Financial Services": "XLF",
        "Industrials": "XLI",
        "Basic Materials": "XLB",
        "Real Estate": "XLRE",
        "Utilities": "XLU",
        "Communication Services": "XLC",
    }

    def __init__(self, analyses_name: str = ""):
        """


        Parameters
        ----------
        analyses_name : str, optional
            DESCRIPTION. The default is "".

        Returns
        -------
        None.

        """
        # get sector data.
        self.sectors = database_querys.database_querys.get_all_active_sectors()

        # get all industry data.
        self.industrys = (
            database_querys.database_querys.get_all_active_industrys()
        )

        # create all dataframes

        # does trend analyses.
        self.get_do_trend_analyses()

        # create timeserie for columns.

    def get_do_trend_analyses(self):
        # create "all" dataframe
        ts_all = self.retreive_trend_timeserie("ALL")

        # first does it for all, then loop true all sectors.
        df = self.create_clean_trend_based_timeserie(ts_all)

        # get performance
        df_perforamnce_all = self.add_perofmance_indicator(df, "ALL")

        # get performance indicators.
        df_performance_stats_all = self.add_performance_stats(
            df_perforamnce_all
        )

        performance_all = {}
        trend_all = {}

        performance_all["ALL"] = df_perforamnce_all.performance
        trend_all["ALL"] = df_perforamnce_all.trend

        df = df_perforamnce_all

        trades = self.create_trades_aggergration(df, "ALL")

        database_querys.database_querys.add_sector_trade_stats(trades)

        # create slide for db
        slide = self.create_slide(df, df_performance_stats_all, "ALL")

        # add to db
        database_querys.database_querys.add_sector_trends(slide)

        for sector in self.sectors:
            print(sector)

            # check if exsist
            if not extent_trend_support.check_if_exsts(
                sector, self.sector_tickers
            ):
                continue

            # set timeserie.
            ts_sector = self.retreive_trend_timeserie(sector)

            # first does it for all, then loop true all sectors.
            df = self.create_clean_trend_based_timeserie(ts_sector)

            # get performance
            df_perforamnce = self.add_perofmance_indicator(df, sector)

            # get performance indicators.
            df_performance_stats = self.add_performance_stats(df_perforamnce)

            trades = self.create_trades_aggergration(df_perforamnce, sector)

            database_querys.database_querys.add_sector_trade_stats(trades)

            # create slide for db
            slide = self.create_slide(df, df_performance_stats_all, sector)

            # add to db
            database_querys.database_querys.add_sector_trends(slide)

            # only for performance differences.
            performance_all[sector] = df_perforamnce.performance
            trend_all[sector] = df_perforamnce.trend

        # creating df's off all performance
        self.df_performance_combined = pd.concat(
            performance_all, axis=0, keys=performance_all.keys()
        )

        # creating trends.
        self.df_trend_combined = pd.concat(
            trend_all, axis=0, keys=performance_all.keys()
        )

    def create_slide(self, df, stats, sector):
        """
        Generates a slide.

        Parameters
        ----------
        df : TYPE
            DESCRIPTION.
        stats : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        #
        row = df.tail(1)

        # get slide
        slide = dict(row.iloc[0].to_dict())
        # get date of slide
        dates = row.index[0]

        slide["date"] = dates.strftime("%Y-%m-%d")

        slide["sector"] = sector

        slide["stats"] = str(stats)

        return slide

    def create_trades_aggergration(self, df, ticker):
        """


        Parameters
        ----------
        df : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """

        # convert index to datetime and set it as the index
        df["index_datetime"] = pd.to_datetime(df.index)
        df.set_index("index_datetime", inplace=True)

        # create a new column for the switch in side, where 0 indicates no switch, and 1 indicates a switch
        df["side_switch"] = df["side"].diff().ne(0).astype(int)

        # create a new column for the group, which is the cumulative sum of the side_switch column
        df["group"] = df["side_switch"].cumsum()

        # group the dataframe by the group column, and aggregate the columns by taking the mean of all columns except for 'performance', which is summed
        df_agg = df.groupby("group").agg(
            {
                "trend": "mean",
                "profile_std": "mean",
                "trend_profile": "last",
                "std_profile": "last",
                "side": "last",
                "performance": "sum",
            }
        )

        # set the index as the last date of each group
        df_agg.index = df[df["side_switch"].ne(0)].index

        df = df_agg

        # Rows of the last 2 years
        two_years_ago = datetime.now() - timedelta(days=2 * 365)
        last_two_years = df.loc[df.index >= two_years_ago]

        # amount trades last 2 years
        amount_2_years = len(last_two_years)

        # Percentage of rows with performance above 0
        positive_percent_y2 = (
            len(last_two_years[last_two_years["performance"] > 0])
            / len(last_two_years)
        ) * 100

        # Mean of performance
        mean_performance_y2 = last_two_years["performance"].mean()

        # Rows of the last 5 years
        five_years_ago = datetime.now() - timedelta(days=5 * 365)
        last_five_years = df.loc[df.index >= five_years_ago]

        # amount trades last 5 years
        amount_5_years = len(last_five_years)

        # Percentage of rows with performance above 0
        positive_percent_y5 = (
            len(last_five_years[last_five_years["performance"] > 0])
            / len(last_five_years)
        ) * 100

        # amount trades last 5 years
        amount_all_years = len(df)

        # Percentage of rows with performance above 0
        positive_all_percent = (len(df[df["performance"] > 0]) / len(df)) * 100

        # Mean of performance
        mean_all_performance_ = df["performance"].mean()

        trade_stats = {
            "sector": ticker,
            "amount_2_years": amount_2_years,
            "positive_percent_y2": positive_percent_y2,
            "mean_performance_y2": mean_performance_y2,
            "amount_5_years": amount_5_years,
            "positive_percent_y5": positive_percent_y5,
            "amount_all_years": amount_all_years,
            "positive_all_percent": positive_all_percent,
            "mean_all_performance_": mean_all_performance_,
        }

        return trade_stats

    def add_perofmance_indicator(self, df, ticker):
        stock_ticker_performance = self.sector_tickers[ticker]

        # load the stock data using yfinance
        stock_data = yf.download(
            stock_ticker_performance,
            start="2000-01-01",
            end=pd.Timestamp.today(),
        )

        # prepairs data, adds performance colums, shifts one row.
        sdata = extent_trend_support.prepair_data_ts_yf(stock_data)

        # Merge the dataframes based on their index
        merged_data = pd.merge(
            df,
            stock_data[["Change"]],
            how="left",
            left_index=True,
            right_index=True,
        )

        # Rename the 'Change' column to 'performance'
        merged_data = merged_data.rename(columns={"Change": "performance"})

        # sets varible
        df = merged_data

        # filters data.
        df = df.fillna(0)

        # clearefy's performance, positive results will turn positive, negative will be negative. (side * performance)
        df["performance"] = df["performance"] * df["side"]

        return df

    def add_performance_stats(self, df):
        stats = {}
        stats["overall_accuracy"] = (
            len(df[df["performance"] > 0]) / len(df)
        ) * 100

        stats["overall_avg_return"] = df.performance.mean()

        df["trend_profile"] = df["trend_profile"].round()
        # Calculate the percentage of positive numbers in the performance column where the trend_underscore column is within a certain range
        for i in range(1, 10):
            i_pos = i
            i_neg = i * -1

            positive_percent = (
                len(
                    df[
                        (df["performance"] > 0)
                        & (
                            (df["trend_profile"] > i_pos)
                            | (df["trend_profile"] < i_neg)
                        )
                    ]
                )
                / len(
                    df[
                        (
                            (df["trend_profile"] > i_pos)
                            | (df["trend_profile"] < i_neg)
                        )
                    ]
                )
            ) * 100

            sstr = "prc_accurate_above_profile_" + str(i)
            stats[sstr] = round(positive_percent, 2)

        # Calculate the percentage of positive numbers in the performance column where the trend_underscore column is within a certain range
        for i in range(1, 10):
            i_pos = i
            i_neg = i * -1

            positive_percent = (
                len(
                    df[
                        (df["performance"] > 0)
                        & (
                            (df["trend_profile"] == i_pos)
                            | (df["trend_profile"] == i_neg)
                        )
                    ]
                )
                / len(
                    df[
                        (
                            (df["trend_profile"] == i_pos)
                            | (df["trend_profile"] == i_neg)
                        )
                    ]
                )
            ) * 100

            sstr = "prc_accurate_on_profile_" + str(i)
            stats[sstr] = round(positive_percent, 2)

        # gadders average return.
        for i in range(1, 10):
            i_pos = i
            i_neg = i * -1
            # assuming i_pos and i_neg are defined
            mean_perf_i_pos = df.loc[
                df["trend_profile"] == i_pos, "performance"
            ].mean()
            mean_perf_i_neg = df.loc[
                df["trend_profile"] == i_neg, "performance"
            ].mean()
            sstr_ = "avg_return_profile_pos_" + str(i)
            sstr = "avg_return_profile_neg_" + str(i)
            stats[sstr_] = round(mean_perf_i_pos, 2)
            stats[sstr] = round(mean_perf_i_neg, 2)

        return stats

    def retreive_trend_timeserie(self, name: str):
        try:
            df = database_querys.database_querys.get_trend_timeseries_data(
                name
            )

        except UnboundLocalError:
            print("troubles")

        return df

    def create_clean_time_serie_df(self, df):
        df = self.set_index_and_remove_id(df)

        # renames and removes name data column.
        df, analyses_name = self.rename_columns(df)

        return df, analyses_name

    def create_clean_trend_based_timeserie(self, df):
        """
        Returns very good dataframe for predicting trends.

        FOR all, every + 3 signal is a winner, + 5,6,7 are all in.

        Parameters
        ----------
        df : TYPE
            DESCRIPTION.

        Returns
        -------
        df : TYPE
            DESCRIPTION.

        """
        df = self.set_index_and_remove_id(df)

        df = self.drop_columns(
            df=df,
            columns_to_drop=[
                "name",
                "duration",
                "profile",
                "volatility",
                "current_yield",
                "max_drawdown",
                "exp_return",
                "max_yield",
                "longs",
                "shorts",
                "total",
            ],
        )

        # calculate the difference of 'trend'
        df["trend_diff"] = df["trend"].diff()

        # renames and removes name data column.
        # calculate the difference of 'trend'
        df["profile_std_diff"] = df["profile_std"].diff()

        df["trend_mean"] = df["trend_diff"].mean()

        df["profile_std_mean"] = df["profile_std_diff"].mean()

        df["trend_std_level"] = df["trend_diff"].std() * 3 / 10

        df["profile_std_std_level"] = df["profile_std_diff"].std() * 3 / 10

        df["trend_profile"] = df["trend_diff"] / df["trend_std_level"]

        df["std_profile"] = (
            df["profile_std_diff"] / df["profile_std_std_level"]
        )

        df = df.round(2)

        df = df.fillna(0)

        self.drop_columns(
            df=df,
            columns_to_drop=[
                "trend_diff",
                "profile_std_diff",
                "trend_mean",
                "profile_std_mean",
                "trend_std_level",
                "profile_std_std_level",
            ],
        )

        # add the trend signals toghetter.
        # calculate the difference between the rows
        df["diff"] = df["trend"].diff()

        # create the trend column based on the difference
        df["side"] = df["diff"].apply(lambda x: 1 if x > 0 else -1)

        # drop the diff column
        df.drop(columns=["diff"], inplace=True)

        return df

    def set_index_and_remove_id(self, df):
        # convert date column to datetime format
        df["date"] = pd.to_datetime(df["date"])

        # set date column as index
        df.set_index("date", inplace=True)

        # drop id column
        df.drop("id", axis=1, inplace=True)

        df = df.round(3)

        return df

    def drop_columns(self, df, columns_to_drop):
        df.drop(columns=columns_to_drop, inplace=True)

        return df

    def rename_columns(self, df):
        new_columns = []

        df_name = df["name"][0]

        df = self.drop_columns(df=df, columns_to_drop=[df_name])

        suggested_name = df_name

        for column in df.columns:
            new_column = f"{suggested_name}_{column}"

            new_columns.append(new_column)

        df.columns = new_columns

        return df, df_name


class extent_trend_support:
    @staticmethod
    def prepair_data_ts_yf(df):
        """
        Creates a column named change that is used to create % of change
        and shift them one line on the side so the performance of today is the score of towmorrow.

        Parameters
        ----------
        df : TYPE
            DESCRIPTION.

        Returns
        -------
        df : TYPE
            DESCRIPTION.

        """
        stock_data = df
        # Compute percentage change and shift values
        stock_data["Change"] = stock_data["Close"].pct_change() * 100
        stock_data["Change"] = stock_data["Change"].shift(-1)

        stock_data = stock_data.fillna(0, inplace=True)

        df = stock_data

        return df

    @staticmethod
    def check_if_exsts(sector, sectors):
        if sector in sectors:
            return True
        else:
            return False


class overall_trend_analyses:
    def __init__(self):
        # load all sectors
        self.sectors = database_querys.database_querys.get_all_active_sectors()

        # filter list
        self.filter_sectors()

        self.data = df = self.create_trend_dataframe()

        # x = self.create_model("ALL", "ALLPTG", data)

    def create_trend_dataframe(self):
        frame = None
        ts_all = self.retreive_trend_timeserie("ALL")

        ts_all.set_index("date", inplace=True)

        ts_all.rename(columns={"trend": "ALL"}, inplace=True)

        ts_data = ts_all[["ALL"]]

        main_frame = ts_data

        for i in self.sectors:
            ts_all = self.retreive_trend_timeserie(i)

            ts_all.set_index("date", inplace=True)

            ts_all.rename(columns={"trend": i}, inplace=True)

            ts_data = ts_all[[i]]

            main_frame = pd.merge(
                main_frame, ts_data, left_index=True, right_index=True
            )

        return main_frame

    def create_model(
        self, name: str = "ALL", name_mode_for_save: str = "test", df=None
    ):
        # Separate the features and target variable
        features = df.drop(columns=["ALL"])
        target = df["ALL"]
        """
        # Convert the features and target to numpy arrays
        X = features.values
        y = target.values

        X_tensor_5 = torch.Tensor(y)

        # Convert the numpy arrays to PyTorch tensors
        X_tensor = torch.Tensor(X)
        y_tensor = torch.Tensor(y)

        # Define the train-test split ratio (e.g., 80% train, 20% test)
        train_ratio = 0.8

        # Calculate the number of samples for the training set
        train_samples = int(train_ratio * len(X))

        # Split the data into training and testing sets
        X_train, y_train = X_tensor[:train_samples], y_tensor[:train_samples]
        X_test, y_test = X_tensor[train_samples:], y_tensor[train_samples:]

        class ComplexTimeSeriesModel(nn.Module):
            def __init__(self, input_size, hidden_size, output_size):
                super(ComplexTimeSeriesModel, self).__init__()

                self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
                self.fc = nn.Linear(
                    hidden_size, output_size
                )  # Adjust the output size

            def forward(self, x):
                _, (hidden, _) = self.lstm(x)
                output = self.fc(hidden[-1])
                return output

        # Example usage
        input_size = 16  # Number of input features
        hidden_size = 64  # Number of hidden units in the LSTM layer
        output_size = 1  # Number of output units

        model = ComplexTimeSeriesModel(input_size, hidden_size, output_size)

        # Print the model architecture
        print(model)

        # Define the loss function
        criterion = nn.MSELoss()

        # Define the optimizer
        optimizer = optim.Adam(model.parameters(), lr=0.001)

        # Train the model
        num_epochs = 50
        batch_size = 32
        num_batches = len(X_train) // batch_size

        for epoch in range(num_epochs):
            epoch_loss = 0.0

            # Mini-batch training
            for i in range(num_batches):
                start = i * batch_size
                end = (i + 1) * batch_size

                # Forward pass
                outputs = model(X_train[start:end])
                loss = criterion(outputs, y_train[start:end].unsqueeze(1))

                # Backward pass and optimization
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

                epoch_loss += loss.item()

            # Print average loss for the epoch
            print(
                f"Epoch {epoch+1}/{num_epochs}, Loss: {epoch_loss / num_batches:.4f}"
            )

        # Evaluate the model on the testing set
        with torch.no_grad():
            y_pred = model(X_tensor)
            mse = criterion(y_pred, y_test.unsqueeze(1))
            rmse = torch.sqrt(mse)
            forecast = model(X_tensor_5)

        # Convert the forecast tensor to a NumPy array
        forecast = forecast.numpy().flatten()
        # Extract the next 5 points from the forecast
        next_5_points = forecast[:5]
        print("Next 5 points:", next_5_points, len(forecast))

        last_5_values = forecast[-5:]
        print("Last 5 values:", last_5_values)
        # Print the forecast
        print(forecast)

        print("Mean Squared Error:", mse.item())
        print("Root Mean Squared Error:", rmse.item())
        """

    def retreive_trend_timeserie(self, name: str):
        try:
            df = database_querys.database_querys.get_trend_timeseries_data(
                name
            )

        except UnboundLocalError:
            print("troubles")

        return df

    def filter_sectors(self):
        strings_to_remove = ["", "ETF", "Unkown"]
        self.sectors = [
            string
            for string in self.sectors
            if string not in strings_to_remove
        ]


atexit.register(get_trend_ts_support.cleanup)

if __name__ == "__main__":
    try:
        x = update_trend_timeseries.update()
        # x = overall_trend_analyses()

    except Exception as e:
        raise Exception("Error with tickers", e)
