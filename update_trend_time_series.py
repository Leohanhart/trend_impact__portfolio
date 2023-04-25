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


class update_trend_timeseries:
    @staticmethod
    def update():

        manager = create_timeseries_manager()

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
        start_date = pd.Timestamp("2022-10-01")
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

        # load all sectors
        self.update_all()

    def update_all(self):
        """
        Updates all avalible updates.

        Returns
        -------
        None.

        """

        self.update_main_analyses()
        self.update_all_sectors()
        self.update_all_industrys()

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


atexit.register(get_trend_ts_support.cleanup)

if __name__ == "__main__":

    try:

        x = update_trend_timeseries()

    except Exception as e:

        raise Exception("Error with tickers", e)
