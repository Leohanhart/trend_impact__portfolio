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
    engine = create_engine("sqlite:///../../core_data/flowimpact_api_db.db", echo = True)   
    Base = declarative_base()
    
    class Table(Base):
        """
        id = Column(String, unique = True, primary_key=True)
        sector = Column(String)
        industry = Column(String)
        Boolean = Column(String)
        
        """
    
        __tablename__ = 'analyses_trend_kamal_performance'
        
        id = Column(String, unique = True, primary_key=True)
        periode = Column(String)
        amount_of_trades_y2 = Column(Integer)
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
        
        
        

    Base.metadata.create_all(engine)
    
    #os.rename(constants.DATABASE_SPAN_PATH, constants.DATABASE_MAIN_PATH)
    
if __name__ == "__main__":    
    
    try:
        
        initialization()
        
    except Exception as e:
        
        raise Exception("Database could not be created", e)