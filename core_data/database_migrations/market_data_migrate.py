# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 12:18:29 2023

@author: Gebruiker
"""

# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 14:18:38 2022

@author: Gebruiker
"""

from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, Date
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
        constants.SQLALCHEMY_DATABASE_URI_layer_zero, echo=True
    )
    Base = declarative_base()

    class Table(Base):
        __tablename__ = "market_data"
        index_column = Column(String, primary_key=True, unique=True)
        regularMarketVolume = Column(Float)
        marketCap = Column(Float)

    Base.metadata.create_all(engine)


if __name__ == "__main__":

    try:

        initialization()

    except Exception as e:

        raise Exception("Database could not be created", e)
