# -*- coding: utf-8 -*-
"""
Created on Thu May  4 15:46:39 2023

@author: Gebruiker
"""

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
        "sqlite:///../../core_data/flowimpact_api_db.db", echo=True
    )
    Base = declarative_base()

    class SectorTradeArchive(Base):
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

    Base.metadata.create_all(engine)

    # os.rename(constants.DATABASE_SPAN_PATH, constants.DATABASE_MAIN_PATH)


if __name__ == "__main__":

    try:

        initialization()

    except Exception as e:

        raise Exception("Database could not be created", e)
