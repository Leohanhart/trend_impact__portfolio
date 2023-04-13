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
)

import pandas as pd

from datetime import datetime, timedelta, date
import json
from datetime import datetime
import sqlalchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import and_, or_, not_

from threading import Thread
from threading import Lock
from datetime import datetime, timedelta


class database_querys:
    def check_if_ticker_is_allowd(
        ticker_name: str,
        exclude_blacklisted: bool = True,
        excluded_non_safe: bool = False,
        excluded_own_recomanded: bool = False,
    ):

        lock = Lock()
        with lock:
            db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
            engine = create_engine(db_path, echo=True)
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

                if excluded_non_safe:

                    if data[0]["safe"] != True:
                        return False

                if excluded_own_recomanded:
                    if data[0]["recommanded"] != True:
                        return False

            except KeyError:

                return False

            return True

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
        lock = Lock()
        with lock:
            db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
            engine = create_engine(db_path, echo=True)
            Session = sessionmaker(bind=engine)
            session = Session()

            # Number of days before expiration date to filter by
            n_days = amount_of_days

            # Subtract n days from current date and time
            cutoff_date = datetime.now() - timedelta(days=n_days)

            # Query for orders that have expired within the last n days
            session = Session()
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
        lock = Lock()
        with lock:
            db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
            engine = create_engine(db_path, echo=True)
            Session = sessionmaker(bind=engine)
            session = Session()

            query_string = (
                session.query(Ticker)
                .filter(Ticker.active == True)
                .statement.compile()
            )  # .all()

            df = pd.read_sql_query(query_string, session.bind)

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
        engine = create_engine(db_path, echo=True)
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
        engine = create_engine(db_path, echo=True)
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
        engine = create_engine(db_path, echo=True)
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
        engine = create_engine(db_path, echo=True)
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
        engine = create_engine(db_path, echo=True)
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
        engine = create_engine(db_path, echo=True)
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

        lock = Lock()
        with lock:
            db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
            engine = create_engine(db_path, echo=True)
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
        engine = create_engine(db_path, echo=True)
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
        lock = Lock()
        with lock:
            # creates database engine.
            db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
            engine = create_engine(db_path, echo=True)
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
        engine = create_engine(db_path, echo=True)
        Session = sessionmaker(bind=engine)
        session = Session()

        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=True)
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
        lock = Lock()
        with lock:
            db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
            engine = create_engine(db_path, echo=True)
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
                engine = create_engine(db_path, echo=True)
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
        engine = create_engine(db_path, echo=True)
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
        engine = create_engine(db_path, echo=True)
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
        engine = create_engine(db_path, echo=True)  # , check_same_thread=True
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
        engine = create_engine(db_path, echo=True)  # , check_same_thread=True
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
        engine = create_engine(db_path, echo=True)  # , check_same_thread=True
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
        engine = create_engine(db_path, echo=True)  # , check_same_thread=True
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
        engine = create_engine(db_path, echo=True)
        Session = sessionmaker(bind=engine)
        session = Session()

        query_string = session.query(Logbook).statement.compile()  # .all()

        df = pd.read_sql_query(query_string, session.bind)

        # close session
        session.close()

        # return frame.
        return df

    def add_log_to_logbook(text: str = ""):
        """
        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=True  # , check_same_thread=True
                               )
        Session = sessionmaker(bind=engine)
        session = Session()

        log = Logbook(
            message=str(text)
        )

        session.add(log)
        session.commit()
        session.close()
        """

        print(text)

    def add_portfolio_to_archive(id_portfolio: str):
        lock = Lock()
        with lock:
            db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
            engine = create_engine(
                db_path, echo=True
            )  # , check_same_thread=True
            Session = sessionmaker(bind=engine)
            session = Session()

            archive = PortfolioArchive(portfolio_id=id_portfolio)
            session.add(archive)
            session.commit()
            session.close()

    def add_user_trade(user_id: str, user_ticker):

        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=True)  # , check_same_thread=True
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
        engine = create_engine(db_path, echo=True)  # , check_same_thread=True
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
        lock = Lock()
        with lock:
            db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
            engine = create_engine(
                db_path, echo=True
            )  # , check_same_thread=True
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
        lock = Lock()
        with lock:
            db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
            engine = create_engine(
                db_path, echo=True
            )  # , check_same_thread=True
            Session = sessionmaker(bind=engine)
            session = Session()

            query_string = session.query(
                TrendArchiveArchive
            ).statement.compile()

            df = pd.read_sql_query(query_string, session.bind)

            df = df.sort_values("updated_at", ascending=True)

            data = df.archive_id.to_list()

            return data

    def delete_user_trade(user_id: str, user_ticker):

        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo=True)  # , check_same_thread=True
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
        lock = Lock()
        with lock:

            db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
            engine = create_engine(
                db_path, echo=True  # , check_same_thread=True
            )
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

        lock = Lock()
        with lock:
            db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
            engine = create_engine(db_path, echo=True)
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
        engine = create_engine(db_path, echo=True)  # , check_same_thread=True
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

        lock = Lock()
        with lock:
            db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
            engine = create_engine(
                db_path, echo=True
            )  # , check_same_thread=True
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
        lock = Lock()
        with lock:
            db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
            engine = create_engine(
                db_path, echo=True
            )  # , check_same_thread=True
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
        lock = Lock()
        with lock:
            db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
            engine = create_engine(
                db_path, echo=True  # , check_same_thread=True
            )
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

        lock = Lock()

        with lock:

            add_report = {}

            db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
            engine = create_engine(
                db_path, echo=True  # , check_same_thread=True
            )
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
        engine = create_engine(db_path, echo=True)  # , check_same_thread=True
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
        engine = create_engine(db_path, echo=True)  # , check_same_thread=True
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
        engine = create_engine(db_path, echo=True)
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
        lock = Lock()
        with lock:
            db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
            engine = create_engine(
                db_path, echo=True  # , check_same_thread=True
            )
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
        engine = create_engine(db_path, echo=True)
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
        engine = create_engine(db_path, echo=True)
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
        x = database_querys.get_all_active_tickers()

        # x = database_querys.get_logs()
        print(x)
        print("END")

    except Exception as e:

        raise Exception("Error with tickers", e)
