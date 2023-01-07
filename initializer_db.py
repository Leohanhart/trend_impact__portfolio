# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 15:04:34 2022

@author: Gebruiker
"""
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, JSON
from sqlalchemy import create_engine
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import datetime
import constants
import os


def initialization():
    # path_db =constants.DATABASE_MAIN_PATH OLD
    #path_db =constants.SQLALCHEMY_DATABASE_URI_layer_zero
    engine = create_engine(
        'sqlite:///core_data/flowimpact_api_db.db', echo=True)

    Base = declarative_base()

    class Ticker(Base):
        """
        id = Column(String, unique = True, primary_key=True)
        sector = Column(String)
        industry = Column(String)
        Boolean = Column(String)

        """

        __tablename__ = 'tickers'

        id = Column(String, unique=True, primary_key=True)
        sector = Column(String)
        industry = Column(String)
        exchange = Column(String)
        active = Column(Boolean)

    class unit_tests_and_errors(Base):
        """
        id = Column(String, unique = True, primary_key=True)
        sector = Column(String)
        industry = Column(String)
        Boolean = Column(String)

        """

        __tablename__ = 'unit_tests_and_errors'

        id = Column(String, unique=True, primary_key=True)
        error = Column(Boolean)
        error_code = Column(String, nullable=True)

    class log(Base):
        __tablename__ = 'logs_and_reports'

        id = Column(Integer, primary_key=True)
        message = Column(String)
        time_created = Column(DateTime(timezone=True),
                              server_default=func.now())
        time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    class Analyses_trend_kamal(Base):
        """
        id = Column(String, unique = True, primary_key=True)
        sector = Column(String)
        industry = Column(String)
        Boolean = Column(String)

        """

        __tablename__ = 'analyses_trend_kamal'

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

    class Analyses_trend_kamal_archive(Base):
        """
        id = Column(String, unique = True, primary_key=True)
        sector = Column(String)
        industry = Column(String)
        Boolean = Column(String)

        """

        __tablename__ = 'analyses_trend_kamal_archive'

        id = Column(Integer, primary_key=True)
        ticker = Column(String)
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

        __table_args__ = (UniqueConstraint('ticker', 'year_start', 'month_start', 'date_start', 'periode', name='_tickers_unique_value'),
                          )

    class Analyses_trend_kamal_performance(Base):
        """
        id = Column(String, unique = True, primary_key=True)
        sector = Column(String)
        industry = Column(String)
        Boolean = Column(String)

        """

        __tablename__ = 'analyses_trend_kamal_performance'

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
        __tablename__ = 'portfolio'
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

    class trading_portfolio(Base):
        __tablename__ = 'trading_portfolio'
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
        __tablename__ = 'closed_portfolio'
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

    Base.metadata.create_all(engine)

    os.rename(constants.DATABASE_SPAN_PATH, constants.DATABASE_MAIN_PATH)


if __name__ == "__main__":

    try:

        initialization()

    except Exception as e:

        raise Exception("Database could not be created", e)
