"""
Created on Thu Mar 31 14:48:20 2022

@author: Gebruiker
"""
import database_querys_main
import json
from core_scripts.stock_data_download import power_stock_object
import stock_analyses_with_ticker_main as stock_analyses_with_ticker
import datetime
import constants
from collections import ChainMap

import pandas as pd

# Define a class to hold the row data
class TrendData:
    def __init__(
        self,
        id,
        ticker,
        year_start,
        month_start,
        date_start,
        weeknr_start,
        year_end,
        month_end,
        date_end,
        weeknr_end,
        periode,
        trend,
        duration,
        profile,
        profile_std,
        volatility,
        current_yield,
        max_drawdown,
        exp_return,
        max_yield,
    ):
        self.id = id
        self.ticker = ticker
        self.year_start = year_start
        self.month_start = month_start
        self.date_start = date_start
        self.weeknr_start = weeknr_start
        self.year_end = year_end
        self.month_end = month_end
        self.date_end = date_end
        self.weeknr_end = weeknr_end
        self.periode = periode
        self.trend = trend
        self.duration = duration
        self.profile = profile
        self.profile_std = profile_std
        self.volatility = volatility
        self.current_yield = current_yield
        self.max_drawdown = max_drawdown
        self.exp_return = exp_return
        self.max_yield = max_yield
        self.start_date = self.get_date(year_start, month_start, date_start)
        self.end_date = self.get_date(year_end, month_end, date_end)

    def get_date(self, year, month, day):
        return datetime.date(year=year, month=month, day=day)


def add_data_to_archive():
    # Load the CSV file into a Pandas DataFrame
    df = pd.read_csv("trend_archive.csv")

    # Do any necessary data cleaning or manipulation here

    # Print the first few rows of the DataFrame to verify it was loaded correctly
    print(df.head())

    # Define the column names
    column_names = [
        "id",
        "ticker",
        "year_start",
        "month_start",
        "date_start",
        "weeknr_start",
        "year_end",
        "month_end",
        "date_end",
        "weeknr_end",
        "periode",
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

    # Assign the column names to the DataFrame
    df.columns = column_names

    if 0 == 0:
        pass
    # Loop through each row of the DataFrame
    for index, row in df.iterrows():
        # Create a dictionary from the row data
        data_dict = row.to_dict()
        # Create a new instance of the TrendData class using the dictionary
        trend_data = TrendData(**data_dict)
        # Do something with the TrendData object
        database_querys_main.database_querys.update_analyses_trend_kamal_archive(
            model=trend_data
        )

    return "Done"


def add_trend_timeserie_data():
    # Load the CSV file into a Pandas DataFrame
    print("starting up the program")
    df = pd.read_csv("timeserietrenddata.csv", encoding="latin-1")

    # Remove the first column by column index
    column_index = 0

    df = df.drop(df.columns[column_index], axis=1)

    column_names = [
        "date",
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

    df.columns = column_names

    print("Data loaded, database insertion started.")
    database_querys_main.database_querys.add_trend_timeserie(df)


if __name__ == "__main__":

    try:

        global x

        x = "Epmty"

        add_trend_timeserie_data()

    except Exception as e:

        print(e)
