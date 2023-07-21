# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 14:25:08 2022

@author: Gebruiker

FIX TO DO
- There is a problem with (Flow and liquidity) function, loads tickers that are positive and negative same instance.
fix this with multiple statments appeard to be very hard, SQLalchemy dont likes turnekey functions, mabey turn.

FIX = add, postive only, netagive onle and add these to the querty function for execeturion.

TASKS TO DO:

    AFTER NEW DATABASE MIGRATION
    - create get _ analyseses (Liq / Mon) For daily tables and also update.

#





"""

import constants

from core_utils.database_tables.tabels import (
    Ticker,
    log,
    Analyses_trend_kamal,
    TradingPortfolio,
    Analyses_archive_kamal,
    Analyses_trend_kamal_performance,
    Portfolio,
    PortfolioArchive,
    Logbook,
    User_trades,
    TrendArchiveArchive,
    Trend_Analysis_Time_series,
    Sector_Trade_Archive,
    Sector_Trend,
    Portfolio_Strategy,
    MarketData,
)

import pandas as pd

from datetime import datetime, timedelta, date
import json
from datetime import datetime
import sqlalchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine
from sqlalchemy import and_, or_, not_
import time
from multiprocessing import Lock
from datetime import datetime, timedelta


class database_querys:
    def get_last_update():

        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()
        # Retrieve data from the "last_update" table
        df = pd.read_sql_table("last_update", con=engine)

        # Convert DataFrame to JSON
        json_data = df.to_json(orient="records")

        return json_data

    def update_last_update():

        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()

        # Get the current date and time
        current_datetime = datetime.now()

        # Create a DataFrame
        df = pd.DataFrame({"DateTime": [current_datetime]})
        # Write DataFrame to the "last_update" table
        df.to_sql(
            name="last_update",
            con=engine,
            if_exists="replace",
            index=False,
        )

        return df

    def get_darwin():

        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()

        query_string = session.query(
            Analyses_trend_kamal_performance
        ).statement.compile()

        try:
            df = pd.read_sql_query(query_string, session.bind)
        except Exception as e:
            print("rerror")
            print(e)

        # close session
        session.close()

        filtered_df = df[
            (df["total_profitible_trades_all"] >= 98)
            & (df["amount_of_trades_y2"] != 1)
            & (df["total_return_y2"] > 0.8)
            & (df["total_average_return_y2"] > 6)
        ]
        tickers = filtered_df.id.to_list()
        return tickers

    def get_liquid_tickers():

        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()

        # Query to select all rows from the table
        query = "SELECT * FROM market_data"

        # Load the table into a DataFrame
        df = pd.read_sql(query, engine)

        # Create the filter
        filter_condition = (df["regularMarketVolume"]) > 200000000

        # Apply the filter to the DataFrame
        filtered_df = df[filter_condition]

        tickers = filtered_df.index_column.to_list()

        return tickers

    def get_mid_and_large_cap_tickers():

        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()

        # Query to select all rows from the table
        query = "SELECT * FROM stock_market_data"

        # Load the table into a DataFrame
        df = pd.read_sql(query, engine)

        mid_cap_threshold = 2000000000  # $2 billion

        # Select rows with marketCap higher than the mid-cap threshold
        mid_cap_stocks = df[df["marketCap"] > mid_cap_threshold]

        tickers = mid_cap_stocks.index_column.to_list()

        return tickers

    def get_mid_and_large_cap():

        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()

        # Query to select all rows from the table
        query = "SELECT * FROM stock_market_data"

        # Load the table into a DataFrame
        df = pd.read_sql(query, engine)

        mid_cap_threshold = 2000000000  # $2 billion

        # Select rows with marketCap higher than the mid-cap threshold
        mid_cap_stocks = df[df["marketCap"] > mid_cap_threshold]

        tickers = mid_cap_stocks.index_column.to_list()

        return tickers

    def check_if_ticker_is_allowd(
        ticker_name: str,
        exclude_blacklisted: bool = True,
        excluded_non_safe: bool = False,
        excluded_own_recomanded: bool = False,
    ):

        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()

        query_string = (
            session.query(Ticker)
            .filter(Ticker.id == ticker_name)
            .statement.compile()
        )

        df = pd.read_sql_query(query_string, session.bind)

        session.close()
        try:
            if df.empty:
                return False
        except:
            return False

        data = df.to_dict(orient="records")
        try:

            if data[0]["active"] != True:
                return False

            if exclude_blacklisted:
                if data[0]["blacklist"] == True:
                    return False

            if excluded_non_safe:

                if data[0]["safe"] != True:
                    return False

        except KeyError:

            return False

        except NameError:

            if data[0]["active"] != True:
                return False
            else:
                return True

        return True

    def update_ticker(
        ticker_name: str = "",
        apply_to_blacklist: bool = False,
        remove_from_blacklist: bool = False,
        apply_to_safe: bool = False,
        remove_from_safe: bool = False,
    ):

        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()

        data = session.query(Ticker).get(ticker_name)

        if apply_to_blacklist:
            data.blacklist = True
        elif remove_from_blacklist:
            data.blacklist = False
        elif apply_to_safe:
            data.safe = True
        elif remove_from_safe:
            data.safe = False

        session.commit()

        session.close()
        return

    def add_tickers_to_list(name_list: str = "", name_ticker: str = ""):
        """


        Parameters
        ----------
        name_list : str, optional
            DESCRIPTION. The default is "".
        name_ticker : str, optional
            DESCRIPTION. The default is "".

        Returns
        -------
        TYPE
            DESCRIPTION.

        """

        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()

        # Check if the strategy already exists in the database
        existing_strategy = (
            session.query(Portfolio_Strategy)
            .filter_by(strategy=name_list)
            .first()
        )
        if not existing_strategy:
            return "Strategy not found{name_list}"

        if not database_querys.check_if_ticker_is_allowd(name_ticker):
            return (
                f"Ticker = {name_ticker} is not allowd, add ticker before add"
            )

        # Create a new Portfolio_Strategy object with the provided strategy and ticker
        new_strategy = Portfolio_Strategy(
            strategy=name_list, ticker=name_ticker
        )

        # Add the new strategy to the session and commit the changes
        session.add(new_strategy)
        try:
            session.commit()
        except IntegrityError:
            return 409

        # Close the session
        session.close()

        return 200

    def add_list_portfolio_strategys(name_list: str = ""):
        """
        Adds list to portfolio

        Parameters
        ----------
        name_list : str, optional
            DESCRIPTION. The default is "".

        Returns
        -------
        None.

        """

        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()

        # Load data from table into DataFrame
        query = session.query(Portfolio_Strategy)
        df = pd.read_sql(query.statement, query.session.bind)

        # Check if variable exists in strategy column
        incoming_variable = name_list
        if incoming_variable in df["strategy"].values:
            return 409
        else:
            # Add the variable to the table
            new_strategy = Portfolio_Strategy(strategy=name_list)
            session.add(new_strategy)
            session.commit()
            return 200

    def return_list_portfolio_strategys(
        name_list: str = "", ticker_name: str = "", return_all: bool = False
    ):
        """

        Returns list of strategy's if exstist

        Parameters
        ----------
        name_list : str, optional
            DESCRIPTION. The default is "".

        Returns
        -------
        TYPE
            DESCRIPTION.
        int
            DESCRIPTION.

        """

        # Create the SQLAlchemy engine and session
        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()

        # Check if name_list is provided
        if name_list:
            # Check if strategy exists in the data
            rows = (
                session.query(Portfolio_Strategy)
                .filter_by(strategy=name_list)
                .all()
            )

            data = []
            for row in rows:
                data.append({"strategy": row.strategy, "ticker": row.ticker})

            return json.dumps(data)

            if not row:
                return json.dumps({"error": "Strategy not found"}), 404

        elif return_all:
            rows = session.query(Portfolio_Strategy).all()

        elif ticker_name:
            rows = (
                session.query(Portfolio_Strategy)
                .filter_by(ticker=ticker_name)
                .all()
            )

            if not rows:
                return (
                    json.dumps(
                        {"error": "No rows found with the specified ticker"}
                    ),
                    404,
                )

            data = []
            for row in rows:
                data.append({"strategy": row.strategy, "ticker": row.ticker})

            return json.dumps(data)

        else:
            # Load available strategy values from the data
            available_strategies = (
                session.query(Portfolio_Strategy.strategy).distinct().all()
            )
            unpacked_values = [value for (value,) in available_strategies]
            return json.dumps(unpacked_values)

        # Load data from table into a list of dictionaries
        data = []
        for row in session.query(Portfolio_Strategy).all():
            data.append(
                {
                    "id": row.id,
                    "strategy": row.strategy,
                    "ticker": row.ticker,
                }
            )

        # Close the session
        session.close()

        # Return the data as JSON
        return json.dumps(data)

    def remove_list_portfolio_strategys(
        name_list: str = "", ticker_name: str = ""
    ):

        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()

        # Filter rows based on name_list and ticker_name
        query = session.query(Portfolio_Strategy)
        if name_list and ticker_name:
            query = query.filter_by(strategy=name_list, ticker=ticker_name)
        elif name_list:
            query = query.filter_by(strategy=name_list)
        elif ticker_name:
            query = query.filter_by(ticker=ticker_name)
        else:
            return 404
        # Delete the filtered rows
        rows_to_delete = query.all()
        for row in rows_to_delete:
            session.delete(row)
        session.commit()

        # Close the session
        session.close()

        return 204

    def get_trend_archive_with_tickers_and_date(
        tickers: list = [], year: int = 0, month: int = 0, date: int = 0
    ):
        """


        Parameters
        ----------
        tickers : list, optional
            DESCRIPTION. The default is [].
        year : int, optional
            DESCRIPTION. The default is 0.
        month : int, optional
            DESCRIPTION. The default is 0.
        date : int, optional
            DESCRIPTION. The default is 0.

        Returns
        -------
        df : TYPE
            DESCRIPTION.

        """

        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()

        dt_object = datetime(year, month, date)

        # convert the datetime object to a date object
        hit_date = dt_object.date()

        if tickers:
            query_string = session.query(Analyses_archive_kamal).filter(
                and_(
                    Analyses_archive_kamal.ticker.in_(tickers),
                    Analyses_archive_kamal.start_date <= hit_date,
                    Analyses_archive_kamal.end_date >= hit_date,
                )
            )
        else:
            query_string = session.query(Analyses_archive_kamal).filter(
                and_(
                    Analyses_archive_kamal.start_date <= hit_date,
                    Analyses_archive_kamal.end_date >= hit_date,
                )
            )

        sql_statement = str(
            query_string.statement.compile(
                compile_kwargs={"literal_binds": True}
            )
        )
        # load SQL statement into pandas dataframe
        df = pd.read_sql(sql_statement, engine)

        return df

    @staticmethod
    def get_expired_portfolio_archives(amount_of_days: int = 62):
        """


        Parameters
        ----------
        amount_of_days : int, optional
            DESCRIPTION. The default is 62.

        Returns
        -------
        None.

        """

        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()

        # Number of days before expiration date to filter by
        n_days = amount_of_days

        # Subtract n days from current date and time
        cutoff_date = datetime.now() - timedelta(days=n_days)

        # Query for orders that have expired within the last n days
        session = Session()

        first_row = session.query(PortfolioArchive).first()
        if first_row is None:

            return

        query_string = (
            session.query(PortfolioArchive)
            .filter(PortfolioArchive.created <= cutoff_date)
            .statement.compile()
        )
        df = pd.read_sql_query(query_string, session.bind)

        session.close()

        df.portfolio_id

        list_expired_tickers = df.portfolio_id.to_list()

        return list_expired_tickers

    @staticmethod
    def get_all_active_tickers():
        """
        Returns

        Returns
        -------
        data : List
            DESCRIPTION.
            list with all tickers:
                ['ADTN',
             'ADTX',
             'ADUS',
             'ADV',
             'ADVM',
             'ADXN',
             'ADXS',
             'AEAC']

        """

        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()

        query = session.query(Ticker).filter(and_(Ticker.active == True))

        df = pd.read_sql_query(query.statement, session.bind)
        session.close()

        data = df[df.active == True]
        data = data.id.to_list()

        return data

    @staticmethod
    def get_all_active_industrys():
        """
        Returns all active industry's

        Returns
        -------
        data : TYPE
            DESCRIPTION.

        """
        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()

        data = session.query(Ticker).filter(Ticker.active == True).all()
        data = database_querys_support.unpack_all_industrys(data)

        if "NA" in data:

            data.remove("NA")

        session.close()

        return data

    @staticmethod
    def get_all_active_sectors():
        """
        Returns all active sectors

        Returns
        -------
        data : TYPE
            DESCRIPTION.

        """
        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()

        data = session.query(Ticker).filter(Ticker.active == True).all()
        data = database_querys_support.unpack_all_sectors(data)

        if "NA" in data:

            data.remove("NA")

        session.close()

        return data

    @staticmethod
    def get_all_stocks_with_industry(name_industry: str = ""):
        """

        returns all industry name tickers

        Parameters
        ----------
        name_industry : str, optional
            DESCRIPTION. The default is "".

        Returns
        -------
        data : TYPE
            DESCRIPTION.

        """

        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()

        data = (
            session.query(Ticker)
            .filter(Ticker.industry == name_industry, Ticker.active == True)
            .all()
        )
        data = database_querys_support.unpack_all_tickers(data)

        session.close()

        if "NA" in data:

            data.remove("NA")

        return data

    @staticmethod
    def get_all_stocks_with_sector(name_sector: str = ""):
        """

        returns all secotrs with the name of an industry.

        Parameters
        ----------
        name_sector : str, optional
            DESCRIPTION. The default is "".

        Returns
        -------
        data : TYPE
            DESCRIPTION.

        """

        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()

        data = (
            session.query(Ticker)
            .filter(Ticker.sector == name_sector, Ticker.active == True)
            .all()
        )
        data = database_querys_support.unpack_all_tickers(data)

        session.close()

        if "NA" in data:

            data.remove("NA")

        return data

    @staticmethod
    def get_sector_with_ticker(ticker: str = ""):
        """
        Returns sector with ticker

        Parameters
        ----------
        ticker : str, optional
            DESCRIPTION. The default is "".

        Returns
        -------
        ticker : TYPE
            DESCRIPTION.

        """
        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()

        query = session.query(Ticker).filter(Ticker.id == ticker).all()
        data = (
            session.query(Ticker)
            .filter(Ticker.sector == query[0].__dict__["sector"])
            .all()
        )
        ticker = database_querys_support.unpack_all_tickers(data)

        session.close()

        if "NA" in data:

            data.remove("NA")

        return ticker

    @staticmethod
    def get_industry_with_ticker(ticker: str = ""):
        """
        Returns industry with ticker.

        Parameters
        ----------
        ticker : str, optional
            DESCRIPTION. The default is "".

        Returns
        -------
        ticker : TYPE
            DESCRIPTION.

        """
        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()

        query = session.query(Ticker).filter(Ticker.id == ticker).all()
        data = (
            session.query(Ticker)
            .filter(Ticker.industry == query[0].__dict__["industry"])
            .all()
        )
        ticker = database_querys_support.unpack_all_tickers(data)

        session.close()

        if "NA" in data:

            data.remove("NA")

        return ticker

    def get_trend_kalman(ticker: str = None):

        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()

        query_string = (
            session.query(Analyses_trend_kamal)
            .filter(
                Analyses_trend_kamal.id == ticker,
            )
            .statement.compile()
        )

        df = pd.read_sql_query(query_string, session.bind)

        # close session
        session.close()

        # return frame.
        return df

    def get_all_trend_kalman():

        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()

        query_string = session.query(Analyses_trend_kamal).statement.compile()

        df = pd.read_sql_query(query_string, session.bind)

        # close session
        session.close()

        # return frame.
        return df

    def get_trend_kalman_data(
        ticker: str = None,
        periode: str = "D",
        year: int = None,
        month: int = None,
        day: int = None,
        weeknr: int = None,
        as_pandas=True,
    ):
        """


        Returns archive data, not up to date.
        -------
        None.

        """

        # creates database engine.
        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()

        query_string = (
            session.query(Analyses_archive_kamal)
            .filter(
                Analyses_archive_kamal.ticker == ticker,
                Analyses_archive_kamal.periode == periode,
            )
            .statement.compile()
        )

        df = pd.read_sql_query(query_string, session.bind)

        # close session
        session.close()

        # return frame.
        return df

        if type(ticker) == str:

            # if pandas, return all.
            if as_pandas:

                if periode == "D" or periode == "W":

                    query_string = (
                        session.query(Analyses_archive_kamal)
                        .filter(
                            Analyses_archive_kamal.ticker == ticker,
                            Analyses_archive_kamal.periode == periode,
                        )
                        .statement.compile()
                    )  # .all()
                    # load dataframe with query

                    df = pd.read_sql_query(query_string, session.bind)

                    # close session
                    session.close()

                    # return frame.
                    return df

                elif periode != None:

                    # generate query
                    query_string = (
                        session.query(Analyses_archive_kamal)
                        .filter(
                            Analyses_archive_kamal.ticker == ticker,
                            Analyses_archive_kamal.periode == "D",
                        )
                        .statement.compile()
                    )  # .all()
                    # load dataframe with query

                    df = pd.read_sql_query(query_string, session.bind)

                    # close session
                    session.close()

                    # return frame.
                    return df

    def try_trend_kalman_performance(
        ticker: str = "", periode: str = "D", as_pandas: bool = True
    ):

        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()

        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()

        print("BINRGO")
        query_string = session.query(
            Analyses_trend_kamal_performance
        ).statement.compile()
        print("HIIIIIII")
        try:
            df = pd.read_sql_query(query_string, session.bind)
        except Exception as e:
            print("rerror")
            print(e)
        print("HAAAAAAAAA")
        # close session
        session.close()

        # return frame.
        return df

    def get_trend_kalman_performance(
        ticker: str = "", periode: str = "D", as_pandas: bool = True
    ):

        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()

        if periode == "D" and ticker != "":

            print(8.1)
            query_string = (
                session.query(Analyses_trend_kamal_performance)
                .filter(
                    Analyses_trend_kamal_performance.id == ticker,
                    Analyses_trend_kamal_performance.periode == periode,
                )
                .statement.compile()
            )  # .all()
            # load dataframe with query
            print(8.2)
            df = pd.read_sql_query(query_string, session.bind)

            print(8.3)
            # close session
            session.close()

            # return frame.
            return df

        elif periode == "D" and ticker == "":
            print(9.3)

            db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
            engine = create_engine(db_path, echo=False)
            Session = sessionmaker(bind=engine)
            session = Session()

            query_string = session.query(
                Analyses_trend_kamal_performance
            ).statement.compile()  # .all()
            # load dataframe with query
            print(9.4)
            df = pd.read_sql_query(query_string, session.bind)
            print(9.5)
            # close session
            session.close()
            print(9.6)
            # return frame.
            return df

        elif periode != None:

            print(10.1)
            # generate query
            query_string = session.query(
                Analyses_trend_kamal_performance
            ).statement.compile()  # .all()
            # load dataframe with query
            print(10.2)
            df = pd.read_sql_query(query_string, session.bind)
            print(10.3)
            # close session
            session.close()

            # return frame.
            return df

    def get_trend_and_performance_kamal():

        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()

        query_string = (
            session.query(
                Analyses_trend_kamal, Analyses_trend_kamal_performance
            )
            .filter(
                Analyses_trend_kamal.id == Analyses_trend_kamal_performance.id
            )
            .statement.compile()
        )

        df = pd.read_sql_query(query_string, session.bind)

        # close session
        session.close()

        # return frame.
        return df

    def get_trends_and_sector():

        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()

        query_string = (
            session.query(Analyses_trend_kamal, Ticker)
            .filter(Analyses_trend_kamal.id == Ticker.id)
            .statement.compile()
        )

        df = pd.read_sql_query(query_string, session.bind)

        # close session
        session.close()

        # return frame.
        return df

    def subscribe_trading_portfolio(id_: str):

        data = database_querys.get_portfolio(id_=id_)

        if type(data) == None:
            raise Exception("No portfolio matching ID")

        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=False)  # , check_same_thread=True
        Session = sessionmaker(bind=engine)
        session = Session()

        # check if portfolio already exsits
        data_exp = (
            session.query(TradingPortfolio)
            .filter(
                TradingPortfolio.portfolio_id == id_,
            )
            .first()
        )

        if data_exp != None:
            raise Exception("Portfolio already exists.")

        # get date
        today = date.today()
        d1 = today.strftime("%d-%m-%Y")

        # lists
        tickers = data.list_of_tickers.to_list()[0]
        balances = data.list_of_balances.to_list()[0]
        sides = data.list_of_sides.to_list()[0]
        performance = data.list_of_performance.to_list()[0]

        object_ = TradingPortfolio(
            portfolio_id=str(data.portfolio_id.to_list()[0]),
            portfolio_strategy=str(data.portfolio_strategy.to_list()[0]),
            list_of_tickers=tickers,
            list_of_balances=balances,
            list_of_sides=sides,
            list_of_performance=performance,
            total_expected_return=float(data.total_expected_return),
            total_sharp_y2=float(data.total_sharp_y2),
            total_volatility_y2=float(data.total_volatility_y2),
            createdAt=d1,
            updatedAt=d1,
        )

        session.add(object_)
        session.commit()
        session.close()

        return 200

    def get_trading_portfolio(id_: str = None):

        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=False)  # , check_same_thread=True
        Session = sessionmaker(bind=engine)
        session = Session()

        query_string: str

        if id_:

            query_string = (
                session.query(TradingPortfolio)
                .filter(
                    TradingPortfolio.portfolio_id == id_,
                )
                .statement.compile()
            )

        elif not id_:
            query_string = session.query(TradingPortfolio).statement.compile()

        df = pd.read_sql_query(query_string, session.bind)

        # close session
        session.close()

        # return frame.
        return df

    def update_trading_portfolio(model):

        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=False)  # , check_same_thread=True
        Session = sessionmaker(bind=engine)
        session = Session()

        x = (
            session.query(TradingPortfolio)
            .filter(
                TradingPortfolio.portfolio_id == model.portfolio_id,
            )
            .first()
        )

        if x == None:
            Analyses = TradingPortfolio(
                portfolio_id=model.portfolio_id,
                portfolio_strategy=model.portfolio_strategy,
                portfolio_amount=model.portfolio_amount,
                list_of_tickers=model.list_of_tickers,
                list_of_balances=model.list_of_balances,
                list_of_sides=model.list_of_sides,
                list_of_performance=model.list_of_performance,
                total_expected_return=model.total_expected_return,
                total_sharp_y2=model.total_sharp_y2,
                total_volatility_y2=model.total_volatility_y2,
                createdAt=model.createdAt,
            )

            session.add(Analyses)
            session.commit()
            session.close()

        else:

            if x.list_of_tickers != model.list_of_tickers:
                x.list_of_tickers = model.list_of_tickers

            if x.list_of_balances != model.list_of_balances:
                x.list_of_balances = model.list_of_balances

            if x.list_of_sides != model.list_of_sides:
                x.list_of_sides = model.list_of_sides

            if x.total_expected_return != model.total_expected_return:
                x.total_expected_return = model.total_expected_return

            if x.total_sharp_y2 != model.total_sharp_y2:
                x.total_sharp_y2 = model.total_sharp_y2

            if x.total_volatility_y2 != model.total_volatility_y2:
                x.total_volatility_y2 = model.total_volatility_y2

            # update date
            today = date.today()
            d1 = today.strftime("%d-%m-%Y")

            # update date.
            x.updatedAt = d1

            session.commit()
            session.close()

        session.close()
        return

    def unsubscribe_trading_portfolio(id_: str):

        data = database_querys.get_portfolio(id_=id_)

        if type(data) == None:
            raise Exception("No portfolio matching ID")

        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=False)  # , check_same_thread=True
        Session = sessionmaker(bind=engine)
        session = Session()

        x = (
            session.query(TradingPortfolio)
            .filter(
                TradingPortfolio.portfolio_id == id_,
            )
            .first()
        )

        if x == None:

            return False

        # else work with it.
        else:

            session.delete(x)
            session.commit()

        session.close()

        return 200

    def get_logs():

        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()

        query_string = session.query(Logbook).statement.compile()  # .all()

        df = pd.read_sql_query(query_string, session.bind)

        # close session
        session.close()

        # return frame.
        return df

    def get_trend_timeseries_data(name_of_timeserie: str):

        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()

        query = f"SELECT * FROM trend_analyses_timeseries WHERE name='{name_of_timeserie}'"
        df = pd.read_sql(query, con=engine)

        return df

    def get_sector_trade_stats():

        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=False)
        conn = engine.connect()

        query = "SELECT * FROM sector_trades_archive"
        result = conn.execute(query)

        trade_stats = []
        for row in result:
            (
                sector,
                amount_2_years,
                positive_percent_y2,
                mean_performance_y2,
                amount_5_years,
                positive_percent_y5,
                amount_all_years,
                positive_all_percent,
                mean_all_performance_,
            ) = row
            trade_stats.append(
                {
                    "sector": sector,
                    "amount_2_years": amount_2_years,
                    "positive_percent_y2": positive_percent_y2,
                    "mean_performance_y2": mean_performance_y2,
                    "amount_5_years": amount_5_years,
                    "positive_percent_y5": positive_percent_y5,
                    "amount_all_years": amount_all_years,
                    "positive_all_percent": positive_all_percent,
                    "mean_all_performance_": mean_all_performance_,
                }
            )

        conn.close()

        return json.dumps(trade_stats)

    def get_sector_trends():

        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()

        sector_trends = session.query(Sector_Trend).all()

        result = []
        for sector_trend in sector_trends:
            data = {
                "id": sector_trend.id,
                "trend": sector_trend.trend,
                "profile_std": sector_trend.profile_std,
                "trend_profile": sector_trend.trend_profile,
                "std_profile": sector_trend.std_profile,
                "side": sector_trend.side,
                "stats": sector_trend.stats,
                "updatedAt": sector_trend.updatedAt,
            }
            result.append(data)

        session.close()

        return json.dumps(result)

    def add_sector_trends(data: dict):

        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()

        try:
            # Check if data already exists in the table
            existing_data = (
                session.query(Sector_Trend)
                .filter_by(id=data["sector"])
                .first()
            )

            if existing_data:
                # Update existing data if it exists
                existing_data.trend = data["trend"]
                existing_data.profile_std = data["profile_std"]
                existing_data.trend_profile = data["trend_profile"]
                existing_data.std_profile = data["std_profile"]
                existing_data.side = data["side"]
                existing_data.stats = data["stats"]
                existing_data.updatedAt = datetime.utcnow().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                session.commit()
                return "Data updated"
            else:
                # Add new data if it doesn't exist
                new_data = Sector_Trend(
                    id=data["sector"],
                    trend=data["trend"],
                    profile_std=data["profile_std"],
                    trend_profile=data["trend_profile"],
                    std_profile=data["std_profile"],
                    side=data["side"],
                    stats=data["stats"],
                    updatedAt=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                )
                session.add(new_data)
                session.commit()
                return "Data added"

        except IntegrityError as e:
            session.rollback()
            return f"IntegrityError: {str(e)}"
        except Exception as e:
            session.rollback()
            return f"Error: {str(e)}"
        finally:
            session.close

    def add_sector_trade_stats(trade_stats_dict: dict):

        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()

        sector = trade_stats_dict["sector"]
        amount_2_years = trade_stats_dict["amount_2_years"]
        positive_percent_y2 = trade_stats_dict["positive_percent_y2"]
        mean_performance_y2 = trade_stats_dict["mean_performance_y2"]
        amount_5_years = trade_stats_dict["amount_5_years"]
        positive_percent_y5 = trade_stats_dict["positive_percent_y5"]
        amount_all_years = trade_stats_dict["amount_all_years"]
        positive_all_percent = trade_stats_dict["positive_all_percent"]
        mean_all_performance_ = trade_stats_dict["mean_all_performance_"]

        # Check if sector already exists in the table
        trade_stats = (
            session.query(Sector_Trade_Archive)
            .filter(Sector_Trade_Archive.id == sector)
            .first()
        )

        if trade_stats is None:
            # Add new row to table
            trade_stats = Sector_Trade_Archive(
                id=sector,
                amount_2_years=amount_2_years,
                positive_percent_y2=positive_percent_y2,
                mean_performance_y2=mean_performance_y2,
                amount_5_years=amount_5_years,
                positive_percent_y5=positive_percent_y5,
                amount_all_years=amount_all_years,
                positive_all_percent=positive_all_percent,
                mean_all_performance_=mean_all_performance_,
            )
            session.add(trade_stats)
        else:
            # Update existing row in table
            trade_stats.amount_2_years = amount_2_years
            trade_stats.positive_percent_y2 = positive_percent_y2
            trade_stats.mean_performance_y2 = mean_performance_y2
            trade_stats.amount_5_years = amount_5_years
            trade_stats.positive_percent_y5 = positive_percent_y5
            trade_stats.amount_all_years = amount_all_years
            trade_stats.positive_all_percent = positive_all_percent
            trade_stats.mean_all_performance_ = mean_all_performance_

        session.commit()

    def add_trend_timeserie(df):

        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=True)
        Session = sessionmaker(bind=engine)
        session = Session()
        for row in df.itertuples():
            try:
                new_data = Trend_Analysis_Time_series(
                    date=row.Index,
                    name=row.name,
                    trend=row.trend,
                    duration=row.duration,
                    profile=row.profile,
                    profile_std=row.profile_std,
                    volatility=row.volatility,
                    current_yield=row.current_yield,
                    max_drawdown=row.max_drawdown,
                    exp_return=row.exp_return,
                    max_yield=row.max_yield,
                    longs=row.longs,
                    shorts=row.shorts,
                    total=row.total,
                )

                session.add(new_data)
                session.commit()
            except IntegrityError:
                session.rollback()

        session.close()

    def add_log_to_logbook(text: str = ""):

        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=True)  # , check_same_thread=True
        Session = sessionmaker(bind=engine)
        session = Session()

        log = Logbook(message=str(text))

        session.add(log)
        session.commit()
        session.close()

    def add_portfolio_to_archive(id_portfolio: str):

        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=False)  # , check_same_thread=True
        Session = sessionmaker(bind=engine)
        session = Session()

        archive = PortfolioArchive(portfolio_id=id_portfolio)
        session.add(archive)
        session.commit()
        session.close()

    def add_user_trade(user_id: str, user_ticker):

        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=False)  # , check_same_thread=True
        Session = sessionmaker(bind=engine)
        session = Session()

        x = (
            session.query(User_trades)
            .filter(
                User_trades.user_id == user_id,
                User_trades.ticker == user_ticker,
            )
            .first()
        )

        if x == None:

            trade = User_trades(user_id=str(user_id), ticker=str(user_ticker))

            session.add(trade)
            session.commit()
            session.close()

            return

    def get_user_trade(user_id: str):

        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=False)  # , check_same_thread=True
        Session = sessionmaker(bind=engine)
        session = Session()

        query_string: str

        query_string = (
            session.query(User_trades)
            .filter(User_trades.user_id == user_id)
            .statement.compile()
        )

        df = pd.read_sql_query(query_string, session.bind)

        # close session
        session.close()

        # return frame.
        return df

    def add_or_update_archive_of_trend_archive(ticker_id: str):

        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=False)  # , check_same_thread=True
        Session = sessionmaker(bind=engine)
        session = Session()

        query_string: str

        x = (
            session.query(TrendArchiveArchive)
            .filter(TrendArchiveArchive.archive_id == ticker_id)
            .first()
        )

        if x == None:

            today = date.today()

            archive = TrendArchiveArchive(
                archive_id=str(ticker_id), updated_at=datetime.now()
            )

            session.add(archive)
            session.commit()
            session.close()

            return
        else:

            x.updated_at = datetime.now()
            session.commit()
            session.close()

            session.close()

            return

    def get_archive_of_trend_archive():

        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=False)  # , check_same_thread=True
        Session = sessionmaker(bind=engine)
        session = Session()

        query_string = session.query(TrendArchiveArchive).statement.compile()

        df = pd.read_sql_query(query_string, session.bind)

        df = df.sort_values("updated_at", ascending=True)

        data = df.archive_id.to_list()

        return data

    def delete_user_trade(user_id: str, user_ticker):

        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=False)  # , check_same_thread=True
        Session = sessionmaker(bind=engine)
        session = Session()

        x = (
            session.query(User_trades)
            .filter(
                User_trades.user_id == user_id,
                User_trades.ticker == user_ticker,
            )
            .first()
        )

        # check if ticker exsists
        if x == None:

            return False

        # else work with it.
        else:

            session.delete(x)
            session.commit()

        session.close()

    def get_portfolio(id_: str = "", strategy: str = ""):

        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=False)  # , check_same_thread=True
        Session = sessionmaker(bind=engine)
        session = Session()

        x = (
            session.query(Portfolio)
            .filter(
                Portfolio.portfolio_id == id_,
            )
            .first()
        )

        query_string: str

        if id_:

            query_string = (
                session.query(Portfolio)
                .filter(
                    Portfolio.portfolio_id == id_,
                )
                .statement.compile()
            )

        elif strategy:

            query_string = (
                session.query(Portfolio)
                .filter(Portfolio.portfolio_strategy == strategy)
                .statement.compile()
            )

        elif id_ and strategy:
            query_string = (
                session.query(Portfolio)
                .filter(
                    Portfolio.portfolio_strategy == strategy,
                    Portfolio.portfolio_id == id_,
                )
                .statement.compile()
            )

        else:

            query_string = session.query(Portfolio).statement.compile()

        df = pd.read_sql_query(query_string, session.bind)

        # close session
        session.close()

        # return frame.
        return df

    def get_portfolio_archive():

        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()

        query_string = session.query(
            PortfolioArchive
        ).statement.compile()  # .all()

        df = pd.read_sql_query(query_string, session.bind)

        session.close()

        data = df[df.active == True]

        data = data.id.to_list()

        return data

    def update_portfolio(model):

        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=False)  # , check_same_thread=True
        Session = sessionmaker(bind=engine)
        session = Session()

        x = (
            session.query(Portfolio)
            .filter(
                Portfolio.portfolio_id == model.portfolio_id,
            )
            .first()
        )

        if x == None:
            Analyses = Portfolio(
                portfolio_id=model.portfolio_id,
                portfolio_strategy=model.portfolio_strategy,
                portfolio_amount=model.portfolio_amount,
                list_of_tickers=model.list_of_tickers,
                list_of_balances=model.list_of_balances,
                list_of_sides=model.list_of_sides,
                list_of_performance=model.list_of_performance,
                total_expected_return=model.total_expected_return,
                total_sharp_y2=model.total_sharp_y2,
                total_volatility_y2=model.total_volatility_y2,
                createdAt=model.createdAt,
            )

            session.add(Analyses)
            session.commit()
            session.close()

            database_querys.add_portfolio_to_archive(
                id_portfolio=model.portfolio_id
            )

        else:

            if x.portfolio_id != model.portfolio_id:
                x.portfolio_id = model.portfolio_id

            if x.portfolio_strategy != model.portfolio_strategy:
                x.portfolio_strategy = model.portfolio_strategy

            if x.list_of_tickers != model.list_of_tickers:
                x.list_of_tickers = model.list_of_tickers

            if x.list_of_balances != model.list_of_balances:
                x.list_of_balances = model.list_of_balances

            if x.list_of_sides != model.list_of_sides:
                x.list_of_sides = model.list_of_sides

            if x.list_of_performance != model.list_of_performance:
                x.list_of_performance = model.list_of_performance

            if x.total_expected_return != model.total_expected_return:
                x.total_expected_return = model.total_expected_return

            if x.total_sharp_y2 != model.total_sharp_y2:
                x.total_sharp_y2 = model.total_sharp_y2

            if x.total_volatility_y2 != model.total_volatility_y2:
                x.total_volatility_y2 = model.total_volatility_y2

            session.commit()
            session.close()

        session.close()
        return

    def delete_portfolio_archive(id_portfolio: str):

        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=False)  # , check_same_thread=True
        Session = sessionmaker(bind=engine)
        session = Session()

        x = (
            session.query(Portfolio)
            .filter(
                PortfolioArchive.portfolio_id == id_portfolio,
            )
            .first()
        )

        # check if ticker exsists
        if x == None:

            return False

        # else work with it.
        else:

            session.delete(x)
            session.commit()

        session.close()

    def delete_portfolio(portfio_id: str = ""):

        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=False)  # , check_same_thread=True
        Session = sessionmaker(bind=engine)
        session = Session()

        x = (
            session.query(Portfolio)
            .filter(
                Portfolio.portfolio_id == portfio_id,
            )
            .first()
        )

        # check if ticker exsists
        if x == None:

            return False

        # else work with it.
        else:

            session.delete(x)
            session.commit()

        session.close()

    def update_analyses_trend_kamal(model):

        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=False)  # , check_same_thread=True
        Session = sessionmaker(bind=engine)
        session = Session()

        x = (
            session.query(Analyses_trend_kamal)
            .filter(
                Analyses_trend_kamal.id == model.ticker,
                Analyses_trend_kamal.periode == model.periode,
            )
            .first()
        )

        now = datetime.now()  # current date and time

        date_time = now.strftime("%d-%m-%Y, %H:%M:%S")

        # check if ticker exsists
        if x == None:

            Analyses = Analyses_trend_kamal(
                # id = 1,
                id=model.ticker,
                periode=model.periode,
                trend=model.trend,
                duration=model.duration,
                profile=model.profile,
                profile_std=model.profile_std,
                volatility=model.volatility,
                current_yield=model.current_yield,
                max_drawdown=model.max_drawdown,
                exp_return=model.exp_return,
                max_yield=float(model.max_yield),
                last_update=now,
            )

            session.add(Analyses)
            #   session.flush()
            session.commit()
            session.close()

        # else work with it.
        else:

            if x.trend != model.trend:
                x.trend = model.trend

            if x.duration != model.duration:

                x.duration = model.duration

            if x.profile != model.profile:

                x.profile = model.profile

            if x.profile_std != model.profile_std:

                x.profile_std = model.profile_std

            if x.volatility != model.volatility:

                x.volatility = model.volatility

            if x.current_yield != model.current_yield:

                x.current_yield = model.current_yield

            if x.max_drawdown != model.max_drawdown:

                x.max_drawdown = model.max_drawdown

            if x.exp_return != model.exp_return:

                x.exp_return = model.exp_return

            if x.max_yield != model.max_yield:

                x.max_yield = model.max_yield

            x.last_update = now

            session.commit()
            session.close()

        session.close()
        return

    def update_analyses_trend_kamal_archive(
        model, check_if_exsits: bool = False
    ):

        add_report = {}

        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=False)  # , check_same_thread=True
        Session = sessionmaker(bind=engine)
        session = Session()

        x = (
            session.query(Analyses_archive_kamal)
            .filter(
                Analyses_archive_kamal.ticker == model.ticker,
                Analyses_archive_kamal.year_start == model.year_start,
                Analyses_archive_kamal.month_start == model.month_start,
                Analyses_archive_kamal.date_start == model.date_start,
                Analyses_archive_kamal.periode == model.periode,
            )
            .first()
        )

        # check if ticker exsists
        if x == None:

            add_report["status"] = "NEW"

            Analyses = Analyses_archive_kamal(
                # id = 1,
                # id = model.ticker,
                ticker=model.ticker,
                start_date=model.start_date,
                end_date=model.end_date,
                year_start=model.year_start,
                month_start=model.month_start,
                date_start=model.date_start,
                weeknr_start=model.weeknr_start,
                year_end=model.year_end,
                month_end=model.month_end,
                date_end=model.date_end,
                weeknr_end=model.weeknr_end,
                periode=model.periode,
                trend=model.trend,
                duration=model.duration,
                profile=model.profile,
                profile_std=model.profile_std,
                volatility=model.volatility,
                current_yield=model.current_yield,
                max_drawdown=model.max_drawdown,
                exp_return=model.exp_return,
                max_yield=float(model.max_yield),
            )

            session.add(Analyses)
            #   session.flush()
            session.commit()
            session.close()

        # else work with it.
        else:

            add_report["status"] = "EXISTS"

            if x.end_date != model.end_date:
                add_report["status"] = "MODIFIED"
                x.end_date = model.end_date

            if x.start_date != model.start_date:
                add_report["status"] = "MODIFIED"
                x.start_date = model.start_date

            if x.year_end != model.year_end:
                add_report["status"] = "MODIFIED"
                x.year_end = int(model.year_end)

            if x.month_end != model.month_end:
                add_report["status"] = "MODIFIED"
                x.month_end = int(model.month_end)

            if x.date_end != model.date_end:
                add_report["status"] = "MODIFIED"

                x.date_end = int(model.date_end)

            if x.trend != model.trend:
                add_report["status"] = "MODIFIED"
                x.trend = int(model.trend)

            if x.duration != model.duration:
                add_report["status"] = "MODIFIED"

                x.duration = int(model.duration)

            if x.profile != model.profile:
                add_report["status"] = "MODIFIED"

                x.profile = int(model.profile)

            if x.profile_std != model.profile_std:
                add_report["status"] = "MODIFIED"

                x.profile_std = int(model.profile_std)

            if x.volatility != model.volatility:
                add_report["status"] = "MODIFIED"

                x.volatility = model.volatility

            if x.current_yield != model.current_yield:
                add_report["status"] = "MODIFIED"

                x.current_yield = model.current_yield

            if x.max_drawdown != model.max_drawdown:
                add_report["status"] = "MODIFIED"

                x.max_drawdown = model.max_drawdown

            if x.exp_return != model.exp_return:
                add_report["status"] = "MODIFIED"

                x.exp_return = model.exp_return

            if x.max_yield != model.max_yield:
                add_report["status"] = "MODIFIED"

                x.max_yield = model.max_yield

            session.commit()
            session.close()

        session.close()

        return add_report

    def update_analyses_trend_kamal_performance(model):

        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=False)  # , check_same_thread=True
        Session = sessionmaker(bind=engine)
        session = Session()

        x = (
            session.query(Analyses_trend_kamal_performance)
            .filter(
                Analyses_trend_kamal_performance.id == model.ticker,
                Analyses_trend_kamal_performance.periode == model.periode,
            )
            .first()
        )

        # check if ticker exsists
        if x == None:

            Analyses = Analyses_trend_kamal_performance(
                # id = 1,
                id=model.ticker,
                periode=model.periode,
                amount_of_trades_y2=model.amount_of_trades_y2,
                total_return_y2=model.total_return_y2,
                total_average_return_y2=model.total_average_return_y2,
                total_profitible_trades_y2=model.total_profitible_trades_y2,
                total_exp_volatility_y2=model.total_exp_volatility_y2,
                total_volatility_y2=model.total_volatility_y2,
                total_return_all=model.total_return_all,
                total_profitible_trades_all=model.total_profitible_trades_all,
                total_average_return_all=model.total_average_return_all,
                total_sharp_y2=model.total_sharp_y2,
                total_sharp_y5=model.total_sharp_y5,
                total_sharp_all=model.total_sharp_all,
                profible_profile=model.profible_profile,
            )

            session.add(Analyses)
            #   session.flush()
            session.commit()
            session.close()

        # else work with it.
        else:

            if x.amount_of_trades_y2 != model.amount_of_trades_y2:
                x.trend = model.amount_of_trades_y2

            if x.total_return_y2 != model.total_return_y2:
                x.trend = model.total_return_y2

            if x.total_average_return_y2 != model.total_average_return_y2:
                x.trend = model.total_average_return_y2

            if (
                x.total_profitible_trades_y2
                != model.total_profitible_trades_y2
            ):
                x.trend = model.total_profitible_trades_y2

            if x.total_exp_volatility_y2 != model.total_exp_volatility_y2:
                x.trend = model.total_exp_volatility_y2

            if x.total_volatility_y2 != model.total_volatility_y2:
                x.trend = model.total_volatility_y2

            if x.total_return_all != model.total_return_all:
                x.trend = model.total_return_all

            if (
                x.total_profitible_trades_all
                != model.total_profitible_trades_all
            ):
                x.trend = model.total_profitible_trades_all

            if (
                x.total_profitible_trades_all
                != model.total_profitible_trades_all
            ):
                x.trend = model.total_profitible_trades_all

            if x.total_average_return_all != model.total_average_return_all:
                x.trend = model.total_average_return_all

            if x.total_sharp_y2 != model.total_sharp_y2:
                x.trend = model.total_sharp_y2

            if x.total_sharp_y5 != model.total_sharp_y5:
                x.trend = model.amount_of_trades_y2

            if x.total_sharp_all != model.total_sharp_all:
                x.trend = model.total_sharp_all

            session.commit()
            session.close()

        session.close()
        return

    def delete_portfolio_with_id(id_: str):

        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=False)  # , check_same_thread=True
        Session = sessionmaker(bind=engine)
        session = Session()

        x = (
            session.query(Portfolio)
            .filter(
                Portfolio.portfolio_id == id_,
            )
            .first()
        )

        # check if ticker exsists
        if x == None:

            return False

        # else work with it.
        else:

            database_querys.delete_portfolio_archive(id_portfolio=id_)

            session.delete(x)

            session.commit()

        session.close()

    def delete_trend_kamal(ticker: str):

        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()

        x = (
            session.query(Analyses_trend_kamal)
            .filter(
                Analyses_trend_kamal.id == ticker,
            )
            .first()
        )

        # check if ticker exsists
        if x == None:

            return False

        # else work with it.
        else:

            session.delete(x)
            session.commit()

        x = (
            session.query(Analyses_trend_kamal_performance)
            .filter(
                Analyses_trend_kamal_performance.id == ticker,
            )
            .first()
        )

        # check if ticker exsists
        if x == None:

            return False

        # else work with it.
        else:

            session.delete(x)
            session.commit()

        session.close()

    def delete_analyses_trend_kamal_archive(model):
        """


        Parameters
        ----------
        model : TYPE
            DESCRIPTION.

        Returns
        -------
        bool
            DESCRIPTION.

        """

        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=False)  # , check_same_thread=True
        Session = sessionmaker(bind=engine)
        session = Session()

        x = (
            session.query(Analyses_archive_kamal)
            .filter(
                Analyses_archive_kamal.ticker == model.ticker,
                Analyses_archive_kamal.year_start == model.year_start,
                Analyses_archive_kamal.month_start == model.month_start,
                Analyses_archive_kamal.date_start == model.date_start,
                Analyses_archive_kamal.periode == model.periode,
            )
            .first()
        )

        # check if ticker exsists
        if x == None:

            return False

        # else work with it.
        else:

            session.delete(x)
            session.commit()

        session.close()

        return True

    def return_portoflolios():
        pass

    def add_portolio_at_overview():
        pass

    def remove_portolio_at_overview():
        pass

    def trade_open_portfolio():
        pass

    def trade_close_portfolio():
        pass

    def trade_delete_portolio():
        pass

    def log_item(id_int: int, message: str):
        """
        adds log item.

        Parameters
        ----------
        id_int : int
            DESCRIPTION.
        message : str
            DESCRIPTION.

        Returns
        -------
        None.

        """

        #
        now = datetime.now()  # current date and time

        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()

        date_time = now.strftime("%d-%m-%Y, %H:%M:%S")
        x = session.query(log).filter(log.id == id_int).first()

        if x == None:

            Log = log(id=id_int, message=message + " " + date_time)

            session.add(Log)
            session.commit()

        else:

            x.message = message + " " + date_time

            session.commit()

        session.close()
        return

    def log_item_get(as_pandas: bool = True, as_json: bool = True):

        # if not as pandas return as query.
        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()

        if not as_pandas:

            query = session.query(log).all()

            session.close()

            return query

        # if panda's is wanted.
        else:

            query_string = session.query(log).statement.compile()

            data = pd.read_sql_query(query_string, session.bind)

            data.drop(["time_created", "time_updated"], axis=1, inplace=True)

            session.close()

            if not as_json:
                return data
            else:
                # transform data to json
                try:

                    data = data.to_dict(orient="records")

                # if packaging already done, dump and return.
                except AttributeError:

                    resp = json.dumps(data)

                    return resp

                # else dump and return.
                resp = json.dumps(data)
                return resp


class database_querys_support:
    @staticmethod
    def check_incomming_vars():
        pass

    @staticmethod
    def unpack_all_tickers(tickers):

        tickers_list = []

        for i in tickers:
            tickers_list.append(i.id)

        return tickers_list

    @staticmethod
    def unpack_all_sectors(tickers):

        sector_list = []

        for i in tickers:

            if type(i.sector) == None:
                continue

            if i.sector == None:
                continue

            if i.sector is None:
                continue

            if i.sector not in sector_list:
                sector_list.append(i.sector)

        return sector_list

    @staticmethod
    def unpack_all_industrys(tickers):

        industry_list = []

        for i in tickers:
            if i.industry:
                if i.industry not in industry_list:
                    industry_list.append(i.industry)

        return industry_list


if __name__ == "__main__":

    try:
        """
        # end

        print("START")

        class kko_strat_model:

            k stands for kaufman.
            k stands for kamal.
            o stands for optimzed


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

        model = kko_strat_model()

        model.portfolio_id = "POA123"
        model.portfolio_strategy = "LEOSBALSOFSTEAL"

        list_tickers = ["AAPL", "BABA", "META"]
        list_of_balances = [25, 33, 33]
        list_of_sides = [1, 1, 1]
        list_of_performance = {}

        serialized_list_of_tickers = json.dumps(list_tickers)
        serialized_list_of_balances = json.dumps(list_of_balances)
        serialized_list_of_sides = json.dumps(list_of_sides)
        serialized_list_of_performance = json.dumps(list_of_performance)

        model.portfolio_amount = 3
        model.list_of_tickers = serialized_list_of_tickers
        model.list_of_balances = serialized_list_of_balances
        model.list_of_sides = serialized_list_of_sides
        model.list_of_performance = serialized_list_of_performance
        model.total_expected_return = 10
        model.total_sharp_y2 = 5
        model.total_volatility_y2 = 20
        model.createdAt = "14-01-2023"

        # global x
        # x = database_querys.get_trading_portfolio(
        #    id_="e0eeaa4b-8e14-11ed-b2b9-001a7dda7110")
        # print(x)
        # x = database_querys.delete_portfolio_with_id(model.portfolio_id)
        global x
        x = database_querys.get_trading_portfolio()

        x = database_querys.subscribe_trading_portfolio(
            "3f8d8199-8dd5-11ed-84f2-001a7dda7110")

        class test:

            ticker = str
            periode = str
            trend = int
            duration = int
            profile = int
            profile_std = int
            volatility = float
            current_yield = float
            max_drawdown = float
            exp_return = float
            max_yield = float

        model = test()

        # id = 1,
        model.ticker = "AAL"
        model.periode = "D"
        model.trend = int(1)
        model.duration = int(12)
        model.profile = int(1)
        model.profile_std = int(1)
        model.volatility = float(4.1)
        model.current_yield = float(6.4)
        model.max_drawdown = float(12.1)
        model.exp_return = float(1.19)
        model.max_yield = float(1.10)
        """
        # x = database_querys.get_trends_and_sector()
        # x = database_querys.get_sector_trends()
        #### test
        x = database_querys.get_all_active_tickers()

        print(x)
        print("END")

    except Exception as e:

        raise Exception("Error with tickers", e)
