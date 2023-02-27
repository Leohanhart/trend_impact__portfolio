# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 14:18:38 2022

@author: Gebruiker
"""

from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, JSON
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import datetime
import constants
import os


def initialization():
    db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
    engine = create_engine(
        "sqlite:///../../core_data/flowimpact_api_db.db", echo=True)
    Base = declarative_base()

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

    Base.metadata.create_all(engine)

    #os.rename(constants.DATABASE_SPAN_PATH, constants.DATABASE_MAIN_PATH)


if __name__ == "__main__":

    try:

        initialization()

    except Exception as e:

        raise Exception("Database could not be created", e)
