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
        "sqlite:///../../core_data/flowimpact_api_db.db", echo=True
    )
    Base = declarative_base()

    class Table(Base):
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

    Base.metadata.create_all(engine)

    # os.rename(constants.DATABASE_SPAN_PATH, constants.DATABASE_MAIN_PATH)


if __name__ == "__main__":

    try:

        initialization()

    except Exception as e:

        raise Exception("Database could not be created", e)
