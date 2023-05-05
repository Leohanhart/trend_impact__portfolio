# -*- coding: utf-8 -*-
"""
Created on Thu May  4 17:03:21 2023

@author: Gebruiker
"""

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

    class SectorTrend(Base):
        __tablename__ = "sector_trend"

        id = Column(String, primary_key=True)
        trend = Column(Float)
        profile_std = Column(Float)
        trend_profile = Column(Float)
        std_profile = Column(Float)
        side = Column(Float)
        stats = Column(String)
        updatedAt = Column(String, nullable=False)

    Base.metadata.create_all(engine)

    # os.rename(constants.DATABASE_SPAN_PATH, constants.DATABASE_MAIN_PATH)


if __name__ == "__main__":

    try:

        initialization()

    except Exception as e:

        raise Exception("Database could not be created", e)
