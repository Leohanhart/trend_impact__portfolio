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
        "sqlite:///../../core_data/flowimpa5ct_api_db.db", echo=True)
    Base = declarative_base()

    class logbook(Base):

        __tablename__ = 'user_trades'

        id = Column(Integer, primary_key=True, autoincrement=True)
        user_id = Column(String)
        ticker = Column(String)

        __table_args__ = (UniqueConstraint('user_id', 'ticker', name='_tickers_unique_value'),
                          )

    Base.metadata.create_all(engine)

    #os.rename(constants.DATABASE_SPAN_PATH, constants.DATABASE_MAIN_PATH)


if __name__ == "__main__":

    try:

        initialization()

    except Exception as e:

        raise Exception("Database could not be created", e)
