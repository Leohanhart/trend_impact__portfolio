# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 16:31:33 2023

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
        "sqlite:///../../core_data/flowimpact_api_db.db", echo=True
    )
    Base = declarative_base()

    class Table(Base):
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

    Base.metadata.create_all(engine)

    # os.rename(constants.DATABASE_SPAN_PATH, constants.DATABASE_MAIN_PATH)


if __name__ == "__main__":

    try:

        initialization()

    except Exception as e:

        raise Exception("Database could not be created", e)
