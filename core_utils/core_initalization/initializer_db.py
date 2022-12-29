# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 15:04:34 2022

@author: Gebruiker
"""
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import datetime
import constants
import os 

def initialization():
    path_db =constants.DATABASE_MAIN_PATH
    engine = create_engine('sqlite:///flowimpact_api_db.db', echo = True)

    Base = declarative_base()
    
    class Ticker(Base):
        """
        id = Column(String, unique = True, primary_key=True)
        sector = Column(String)
        industry = Column(String)
        Boolean = Column(String)
        
        """
    
        __tablename__ = 'tickers'
        
        id = Column(String, unique = True, primary_key=True)
        sector = Column(String)
        industry = Column(String)
        exchange = Column(String)
        active = Column(Boolean)
    
    class Analyses_Moneyflow(Base):
        """
        id = Column(String, unique = True, primary_key=True)
        sector = Column(String)
        industry = Column(String)
        Boolean = Column(String)
        
        """
    
        __tablename__ = 'analyses_moneyflow'
        
        id = Column(String, unique = True, primary_key=True)
        periode_mon = Column(String)
        profile_mon = Column(Integer)
        profile_rate_of_change_mon = Column(Integer)
        rate_of_change_mon = Column(Float)
        last_mon = Column(Float)
        last_signal_mon = Column(Integer)
        periode_since_signal_mon = Column(Integer)
    
    class Analyses_Liquidityimpact(Base):
        """
        id = Column(String, unique = True, primary_key=True)
        sector = Column(String)
        industry = Column(String)
        Boolean = Column(String)
        
        """
    
        __tablename__ = 'analyses_liquidityimpact'
        
        id = Column(String, unique = True, primary_key=True)
        periode_liq = Column(String)
        profile_liq = Column(Integer)
        profile_rate_of_change_liq = Column(Integer)
        rate_of_change_liq = Column(Float)
        last_liq = Column(Float)
        last_signal_liq = Column(Integer)
        periode_since_signal_liq = Column(Integer)
        
    class unit_tests_and_errors(Base):
        """
        id = Column(String, unique = True, primary_key=True)
        sector = Column(String)
        industry = Column(String)
        Boolean = Column(String)
        
        """
    
        __tablename__ = 'unit_tests_and_errors'
        
        id = Column(String, unique = True, primary_key=True)
        error = Column(Boolean)
        error_code = Column(String, nullable=True) 
        
    class log(Base):
        __tablename__ = 'logs_and_reports'
        
        id = Column(Integer, primary_key=True)
        message = Column(String)
        time_created = Column(DateTime(timezone=True), server_default=func.now())
        time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    Base.metadata.create_all(engine)
    
    os.rename(constants.DATABASE_SPAN_PATH, constants.DATABASE_MAIN_PATH)
    
if __name__ == "__main__":    
    
    try:
        
        initialization()
        
    except Exception as e:
        
        raise Exception("Database could not be created", e)

