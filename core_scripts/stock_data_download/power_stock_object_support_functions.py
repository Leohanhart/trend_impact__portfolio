# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 17:29:20 2021

@author: Gebruiker
"""
import yfinance as yf

from datetime import datetime
from core_scripts.synchronization import synch_class
from dateutil.parser import parse
import pandas as pd

from core_scripts.stock_data_download import (
    power_stock_object_support_functions as support_functions,
)
from core_scripts.stock_data_download import (
    stockobject_supporting_functions as old_supporting_functions,
)
from core_scripts.stock_analyses import old_stock_analyses as stock_analyses
import os
import constants
import pandas as pd


class load_stock_data_rf:

    """

    Taken
    1. Cash per share moet worden toegevoegd.
    2. Dividend forward return moet worden toegevoegd.
    3. Minimaal de dividend discount methode,
    4. Minimaal de close / (book + cash + forward dividend in value) discount methode.





    Extreem belangrijk:

        Deze library werkt alleen als je de verzie van "pip install git+https://github.com/rodrigobercini/yfinance.git"
        verzie installeerd.

    This object is mainly depending on the following.
    Just check if the stock is only donwloaded one time a day. If not than canecel..


    """


class handle_data_synch:

    synch_object = None

    def __init__(self, synch_object=""):

        self.synch_object = synch_object

    def load_data_varible(self, data_extention=None):
        """

        This is function is used to load a certain type of data with an data extention

        Parameters
        ----------
        data_extention : TYPE, optional
            DESCRIPTION. The default is None.

        Returns
        -------
        data : TYPE
            DESCRIPTION.

        """

        if data_extention != None:

            dsb = data_synch_object = self.synch_object

            dsb.data_extention = data_extention
            dsb.refresh_object()

            dsb.load_data()

            data = dsb.retreived_data

            return data

    def save_data_varible(self, data=None, data_extention=None):
        """
        This function is made to save and load data more easy,

        Parameters
        ----------
        data : TYPE, optional
            DESCRIPTION. The default is None.
        data_extention : TYPE, optional
            DESCRIPTION. The default is None.

        Returns
        -------
        None.

        """

        dsb = data_synch_object = self.synch_object
        dsb.new_data = data
        dsb.data_extention = data_extention
        dsb.refresh_object()

        dsb.overwrite_data()


class load_company_data_yahoo:

    # ticker object
    __ticker_object = ""
    data_object = ""

    all_details_dict: dict = None

    # company info
    company_ticker = None
    sector = None
    industry = None

    # financials
    free_float = None
    market_cap = None
    dividends = None
    book_value = None
    short_ratio = None
    cash_per_share = None

    # pricingmodels
    future_fair_value_including_dividends = None  # this calculation is (total bookvalue per share + cashper share + dividend discount. )
    future_price_discount = None

    #

    # errors
    error_code = None

    def __init__(self, ticker="AAPL"):

        self.company_ticker = ticker

        self.ticker = ticker.upper()

        self.__ticker_object = yf.Ticker(self.company_ticker)
        self.het_ticker_object = yf.Ticker(self.company_ticker)

        try:

            self.data_object = self.__ticker_object.get_info()
            # self.all_details_dict = self.data_object

            self.load_data()

        except:

            self.error_code = 1

    def load_data(self):

        # load dividends for dividend analyses
        self.load_dividends()

        # load sector
        self.sector = self.data_object["sector"]

        # load industy
        self.industry = self.data_object["industry"]

        # load bookvalue per share
        self.book_value = self.data_object["bookValue"]

        # load market capitalization ( for liq impact and so on )
        self.market_cap = self.data_object["marketCap"]

        # load free float.
        self.free_float = self.data_object["floatShares"]

        # loads all data into var
        self.all_details_dict = self.data_object
        # load cash per share (Own creation )

        try:

            self.cash_per_share = self.load_cash_per_share()

        except:

            self.cash_per_share = 0

        try:

            self.future_fair_value_including_dividends = (
                self.load_future_fairvalue_price_including_dividends()
            )

        except:

            self.future_fair_value_including_dividends = 0

        self.load_discount_on_future_fair()

    def load_dividends(self):

        try:
            self.dividends = self.__ticker_object.dividends
        except:
            self.dividends = 0

    def load_cash_per_share(self):
        """
        This function loads cash per share: (Bookvalue ps + cash ps + discounted dividend yield.)

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        #
        data = self.__ticker_object.quarterly_balancesheet
        #
        # rett
        data_cash = data.loc["Cash"]
        #
        # retreives the amount of shares
        last_reported_cash = data_cash.iloc[0]

        self.cash_per_share = last_reported_cash / self.free_float

        return self.cash_per_share

    def load_dividend_discount(self):
        """

        Loads dividend discount this calcation is based on the book coporate finanace.

        Returns
        -------
        b : TYPE
            DESCRIPTION.

        """

        # get the dividend yield.
        dividend_yield = self.data_object["dividendYield"]

        # a is 100% min dvidend
        a = 1 - dividend_yield

        # b is the sigma
        b = (1 - a) / a

        return b

    def load_future_fairvalue_price_including_dividends(self):
        """

        This function loads the future fair value including divindends.

        this funtcion is calculating this by adding the bookvalue and the fairvalue
        and multipling this with the dividend discount ration.

        Returns
        -------
        None.

        """

        # retreive book price per share
        bookprice_ps = self.book_value
        #
        # retreive the cash per share
        cash_ps = self.cash_per_share
        #
        # retreives the dividend discount
        dividend_discount = self.load_dividend_discount()
        #
        # sum of the total value
        total_value = bookprice_ps + cash_ps
        #
        # totalvalue times the discounted dividend
        sigma = total_value * (1 + dividend_discount)

        return sigma

    def load_discount_on_future_fair(self):
        """

        Returns discount on the current price.

        Returns
        -------
        None.

        """
        # loads the future fair value
        future_fair_value = self.future_fair_value_including_dividends
        #
        # get last close
        previousclose = self.data_object["currentPrice"]
        #
        # adding calculating the difference from the currentprice
        discount = ((future_fair_value - previousclose) / previousclose) * 100

        self.future_price_discount = discount

        return round(discount, 2)


global load_ding
load_ding = load_company_data_yahoo("AAPL")


class experation_manager:
    """
    Class die gebruikt kan worden voor datum verificatie.
    """

    def days_between(self, date_1):
        """
        This function is to check the last days inbetween the dates.
        """
        today = self.return_last_date_object()

        d1 = datetime.strptime(date_1, "%Y-%m-%d")
        d2 = datetime.strptime(today, "%Y-%m-%d")

        return int(abs((d2 - d1).days))

    def return_last_date_object(self):
        return datetime.today().strftime("%Y-%m-%d")

    def return_true_if_weekly_expired(self, date_1, return_amound=True):

        today = self.return_last_date_object()

        d1 = datetime.strptime(date_1, "%Y-%m-%d")
        d2 = datetime.strptime(today, "%Y-%m-%d")

        weeknr_1 = d1.isocalendar()[1]
        weeknr_2 = d2.isocalendar()[1]

        if weeknr_1 != weeknr_2 and not return_amound:
            return True
        else:
            if not return_amound:
                return False

        if return_amound:

            weeksbetween = weeknr_2 - weeknr_1

            return weeksbetween


class time_conversion:

    # https://tcoil.info/aggregate-daily-ohlc-stock-price-data-to-weekly-python-and-pandas/

    weekly_stock_data = None
    montly_stock_data = None

    time_frames = {}

    def __init__(self, stock_data=""):
        """
        Insert stock data

        Parameters
        ----------
        stock_data : TYPE, optional
            DESCRIPTION. The default is "".

        Returns
        -------
        None.

        """

        df = stock_data

        self.time_frames["Daily"] = stock_data

        if "Change" in df.columns:

            agg_dict = {
                "Open": "first",
                "High": "max",
                "Low": "min",
                "Close": "last",
                "Adj Close": "last",
                "Volume": "sum",
                "Change": "mean",
            }

            # resampled dataframe
            # 'W' means weekly aggregation
            self.weekly_stock_data = df.resample("W-Fri").agg(agg_dict)

            self.time_frames["Weekly"] = self.weekly_stock_data

            agg_dict = {
                "Open": "first",
                "High": "max",
                "Low": "min",
                "Close": "last",
                "Adj Close": "last",
                "Volume": "sum",
                "Change": "mean",
            }

            # resampled dataframe
            # 'W' means weekly aggregation

            self.montly_stock_data = df.resample("M").agg(agg_dict)
            self.time_frames["Monthly"] = self.montly_stock_data
        else:
            agg_dict = {
                "Open": "first",
                "High": "max",
                "Low": "min",
                "Close": "last",
                "Adj Close": "last",
                "Volume": "mean",
            }

            # resampled dataframe
            # 'W' means weekly aggregation
            r_df = df.resample("W").agg(agg_dict)

            self.time_frames["Weekly"] = r_df

            agg_dict = {
                "Open": "first",
                "High": "max",
                "Low": "min",
                "Close": "last",
                "Adj Close": "last",
                "Volume": "sum",
            }

            # het zou kunnen dat volume mean vervangen moet worden door np.sum - test dit.

            # resampled dataframe
            # 'W' means weekly aggregation

            r_df = df.resample("M").agg(agg_dict)
            self.time_frames["Monthly"] = r_df


class load_tickers:

    tickers_list: list() = []
    tickers_dict: dict = {}

    def __init__(self):

        stocks = {}

        # load the list of stocks

        with open("stocks.txt") as f:
            contents = f.readlines()
            # print(contents)

        # create a dictonary for the stocks.
        for i in range(0, len(contents)):
            x = contents[i].replace("\n", "")
            stocks[x] = ""

        self.tickers_dict = stocks


class error_checker:
    def is_date(self, string, fuzzy=False):
        """
        Return whether the string can be interpreted as a date.

        :param string: str, string to check for date
        :param fuzzy: bool, ignore unknown tokens in string if True
        """

        try:
            parse(string, fuzzy=fuzzy)
            return True

        except ValueError:
            return False

    def date_error_synch(self, value):
        pass


"""             OLD FUNCTIONS

    def load_data_varible(self,  data_extention = None, synch_object = None):
        
        
        This is function is used to load a certain type of data with an data extention

        Parameters
        ----------
        data_extention : TYPE, optional
            DESCRIPTION. The default is None.

        Returns
        -------
        data : TYPE
            DESCRIPTION.


        if  data_extention != None:
            
            dsb = data_synch_object = self.synch_object
            
            dsb.data_extention = data_extention
            dsb.refresh_object()
            
            dsb.load_data()
            
            data = dsb.retreived_data
            
            return data
            
   



"""


class data_modifications:
    def convert_nested_analeses_dict_data_to_list(self, data=None) -> list:
        """
        Converts all kinds of dictonary, they need to contain "Data"

        Parameters
        ----------
        data : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        #
        # check if type is correct
        # print(type(data))

        if not isinstance(data, pd.core.frame.DataFrame):
            #
            # else raise error, wrong formate
            raise Exception(
                "Wrong formate, no match to dict",
                "convert_nested_analeses_dict_data_to_list",
            )
        #
        # raises error of data is missing
        elif not "Data" in data.columns:
            #
            # raises the missing colums name error
            raise Exception(
                'Data column - named "Data" is missing in dict dict',
                "convert_nested_analeses_dict_data_to_list",
            )
        #
        # else, just execute the normal convertino
        else:
            #
            # extract values
            value_data = data.values
            #
            # list the values
            nested_values = value_data.tolist()
            #
            # de-nest the values
            unnested_values = [
                item for sublist in nested_values for item in sublist
            ]
            #
            # return the values
            return unnested_values


if __name__ == "__main__":

    try:

        synch_object = synch_class.data_synch(
            path=constants.CORE_DATA_____PATH,
            subfolder="stock_data",
            ticker="AACG",
            data_extention="last_download_company_data_refresh",
        )

        synch_handler = support_functions.handle_data_synch(synch_object)

        # power_stock_apple.twitter_module(full_test_function=True)

    except Exception as e:

        raise Exception("Problem with the stockticker", e)
