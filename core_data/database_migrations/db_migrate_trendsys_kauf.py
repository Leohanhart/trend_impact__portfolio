# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 00:40:21 2022

@author: Gebruiker
"""

from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
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

    class Table(Base):
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
        last_update = Column(DateTime(timezone=True), onupdate=func.now())

        # __table_args__ = (UniqueConstraint('ticker', 'periode'

    Base.metadata.create_all(engine)

    #os.rename(constants.DATABASE_SPAN_PATH, constants.DATABASE_MAIN_PATH)


if __name__ == "__main__":

    try:

        initialization()

    except Exception as e:

        raise Exception("Database could not be created", e)
