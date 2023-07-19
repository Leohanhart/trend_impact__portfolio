# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 15:04:34 2022

@author: Gebruiker
"""
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Float,
    DateTime,
    JSON,
    Date,
)
from sqlalchemy import create_engine
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import datetime
import constants
import os
import database_connection


def initialization():

    #
    engine = database_connection.get_db_engine()

    Base = declarative_base()

    class Ticker(Base):
        """
        id = Column(String, unique = True, primary_key=True)
        sector = Column(String)
        industry = Column(String)
        Boolean = Column(String)

        """

        __tablename__ = "tickers"

        id = Column(String, unique=True, primary_key=True)
        sector = Column(String)
        industry = Column(String)
        exchange = Column(String)
        blacklist = Column(Boolean)
        safe = Column(Boolean)
        active = Column(Boolean)

    class unit_tests_and_errors(Base):
        """
        id = Column(String, unique = True, primary_key=True)
        sector = Column(String)
        industry = Column(String)
        Boolean = Column(String)

        """

        __tablename__ = "unit_tests_and_errors"

        id = Column(String, unique=True, primary_key=True)
        error = Column(Boolean)
        error_code = Column(String, nullable=True)

    class logbook(Base):

        __tablename__ = "logbook"

        id = Column(Integer, primary_key=True, autoincrement=True)
        created = Column(DateTime, default=func.now())
        message = Column(String)

    class log(Base):
        __tablename__ = "logs_and_reports"

        id = Column(Integer, primary_key=True)
        message = Column(String)
        time_created = Column(
            DateTime(timezone=True), server_default=func.now()
        )
        time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    class Analyses_trend_kamal(Base):
        """
        id = Column(String, unique = True, primary_key=True)
        sector = Column(String)
        industry = Column(String)
        Boolean = Column(String)

        """

        __tablename__ = "analyses_trend_kamal"

        id = Column(String, unique=True, primary_key=True)
        periode = Column(String)
        trend = Column(Integer)
        duration = Column(Integer)
        profile = Column(Integer)
        profile_std = Column(Integer)
        volatility = Column(Float)
        current_yield = Column(Float)
        max_drawdown = Column(Float)
        exp_return = Column(Float)
        max_yield = Column(Float)
        last_update = Column(DateTime(timezone=True), onupdate=func.now())

    class Analyses_trend_kamal_archive(Base):
        """
        id = Column(String, unique = True, primary_key=True)
        sector = Column(String)
        industry = Column(String)
        Boolean = Column(String)

        """

        __tablename__ = "analyses_trend_kamal_archive"

        id = Column(Integer, primary_key=True)
        ticker = Column(String)

        start_date = Column(Date)
        end_date = Column(Date)

        year_start = Column(Integer)
        month_start = Column(Integer)
        date_start = Column(Integer)
        weeknr_start = Column(Integer)

        year_end = Column(Integer)
        month_end = Column(Integer)
        date_end = Column(Integer)
        weeknr_end = Column(Integer)

        periode = Column(String)
        trend = Column(Integer)
        duration = Column(Integer)
        profile = Column(Integer)
        profile_std = Column(Integer)
        volatility = Column(Float)
        current_yield = Column(Float)
        max_drawdown = Column(Float)
        exp_return = Column(Float)
        max_yield = Column(Float)

        __table_args__ = (
            UniqueConstraint(
                "ticker",
                "year_start",
                "month_start",
                "date_start",
                "periode",
                name="_tickers_unique_value",
            ),
        )

    class Analyses_trend_kamal_performance(Base):
        """
        id = Column(String, unique = True, primary_key=True)
        sector = Column(String)
        industry = Column(String)
        Boolean = Column(String)

        """

        __tablename__ = "analyses_trend_kamal_performance"

        id = Column(String, unique=True, primary_key=True)
        periode = Column(String)
        amount_of_trades_y2 = Column(Float)
        total_return_y2 = Column(Float)
        total_average_return_y2 = Column(Float)
        total_profitible_trades_y2 = Column(Float)
        total_exp_volatility_y2 = Column(Float)
        total_volatility_y2 = Column(Float)
        total_return_all = Column(Float)
        total_profitible_trades_all = Column(Float)
        total_average_return_all = Column(Float)
        total_sharp_y2 = Column(Float)
        total_sharp_y5 = Column(Float)
        total_sharp_all = Column(Float)
        profible_profile = Column(Integer, nullable=True)

    class portfolio(Base):
        __tablename__ = "portfolio"
        id = Column(Integer, primary_key=True)
        portfolio_id = Column(String, nullable=False, unique=True)
        portfolio_strategy = Column(String, nullable=False)
        portfolio_amount = Column(Integer)
        list_of_tickers = Column(JSON, nullable=False)
        list_of_balances = Column(JSON, nullable=False)
        list_of_sides = Column(JSON, nullable=False)
        list_of_performance = Column(JSON, nullable=False)
        total_expected_return = Column(Float)
        total_sharp_y2 = Column(Float)
        total_volatility_y2 = Column(Float)
        createdAt = Column(String, nullable=False)

    class PortfolioArchive(Base):
        __tablename__ = "portfolio_archive"

        portfolio_id = Column(
            String, primary_key=True, nullable=False, unique=True
        )
        created = Column(DateTime, default=func.now())

    class TrendArchiveArchive(Base):
        __tablename__ = "trend_archive_archive"
        archive_id = Column(
            String, primary_key=True, nullable=False, unique=True
        )
        updated_at = Column(DateTime)

    class trading_portfolio(Base):
        __tablename__ = "trading_portfolio"
        id = Column(Integer, primary_key=True)
        portfolio_id = Column(String, nullable=False)
        portfolio_strategy = Column(String, nullable=False)
        list_of_tickers = Column(JSON, nullable=False)
        list_of_balances = Column(JSON, nullable=False)
        list_of_sides = Column(JSON, nullable=False)
        list_of_performance = Column(JSON, nullable=False)
        total_expected_return = Column(Float)
        total_sharp_y2 = Column(Float)
        total_volatility_y2 = Column(Float)
        createdAt = Column(String, nullable=False)
        updatedAt = Column(String, nullable=False)

    class closed_portfolio(Base):
        __tablename__ = "closed_portfolio"
        id = Column(Integer, primary_key=True)
        portfolio_id = Column(String, nullable=False)
        portfolio_strategy = Column(String, nullable=False)
        list_of_tickers = Column(JSON, nullable=False)
        list_of_balances = Column(JSON, nullable=False)
        list_of_sides = Column(JSON, nullable=False)
        list_of_performance = Column(JSON, nullable=False)
        total_expected_return = Column(Float)
        total_sharp_y2 = Column(Float)
        total_volatility_y2 = Column(Float)

    class user_trades(Base):

        __tablename__ = "user_trades"

        id = Column(Integer, primary_key=True, autoincrement=True)
        user_id = Column(String)
        ticker = Column(String)

        __table_args__ = (
            UniqueConstraint(
                "user_id", "ticker", name="_tickers_uniqueodeo_value"
            ),
        )

    class Trend_Analysis_Time_series(Base):
        __tablename__ = "trend_analyses_timeseries"

        id = Column(Integer, primary_key=True, autoincrement=True)
        date = Column(Date, nullable=False)
        name = Column(String(50), nullable=False)
        trend = Column(Float, nullable=False)
        duration = Column(Integer, nullable=False)
        profile = Column(Float, nullable=False)
        profile_std = Column(Float, nullable=False)
        volatility = Column(Float, nullable=False)
        current_yield = Column(Float, nullable=False)
        max_drawdown = Column(Float, nullable=False)
        exp_return = Column(Float, nullable=False)
        max_yield = Column(Float, nullable=False)
        longs = Column(Integer, nullable=False)
        shorts = Column(Integer, nullable=False)
        total = Column(Integer, nullable=False)

        __table_args__ = (
            UniqueConstraint("date", "name", name="uq_date_name"),
        )

    class Sector_Trade_Archive(Base):
        __tablename__ = "sector_trades_archive"
        id = Column(String, primary_key=True)
        amount_2_years = Column(Integer)
        positive_percent_y2 = Column(Float)
        mean_performance_y2 = Column(Float)
        amount_5_years = Column(Integer)
        positive_percent_y5 = Column(Float)
        amount_all_years = Column(Integer)
        positive_all_percent = Column(Float)
        mean_all_performance_ = Column(Float)

    class Sector_Trend(Base):
        __tablename__ = "sector_trend"

        id = Column(String, primary_key=True)
        trend = Column(Float)
        profile_std = Column(Float)
        trend_profile = Column(Float)
        std_profile = Column(Float)
        side = Column(Float)
        stats = Column(String)
        updatedAt = Column(String, nullable=False)

    class Portfolio_Strategy(Base):
        __tablename__ = "portfolio_strategys"

        id = Column(Integer, primary_key=True, autoincrement=True)
        strategy = Column(String, nullable=False)
        ticker = Column(String, nullable=True)

        __table_args__ = (
            UniqueConstraint("strategy", "ticker", name="uq_strategy_ticker"),
        )

    class User(Base):
        __tablename__ = "users"
        id = Column(Integer, primary_key=True, index=True)
        username = Column(String, unique=True)
        password = Column(String)
        role = Column(String)

    class UserActivity(Base):
        __tablename__ = "user_activity"

        id = Column(Integer, primary_key=True, index=True)
        user = Column(String)
        endpoint = Column(String)
        values = Column(String, nullable=False)
        timestamp = Column(DateTime, default=func.now())

    Base.metadata.create_all(engine)

    # os.rename(constants.DATABASE_SPAN_PATH, constants.DATABASE_MAIN_PATH)


if __name__ == "__main__":

    try:

        initialization()

    except Exception as e:

        raise Exception("Database could not be created", e)
