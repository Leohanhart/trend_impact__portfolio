# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 16:09:54 2022

@author: Gebruiker
"""
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import datetime
import constants
import os 

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
    
class Analyses_Moneyflow_Daily(Base):
    """
    id = Column(String, unique = True, primary_key=True)
    sector = Column(String)
    industry = Column(String)
    Boolean = Column(String)
    
    """

    __tablename__ = 'analyses_moneyflow_daily'
    
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

class Analyses_Liquidityimpact_Daily(Base):
    """
    id = Column(String, unique = True, primary_key=True)
    sector = Column(String)
    industry = Column(String)
    Boolean = Column(String)
    
    """

    __tablename__ = 'analyses_liquidityimpact_daily'
    
    id = Column(String, unique = True, primary_key=True)
    periode_liq = Column(String)
    profile_liq = Column(Integer)
    profile_rate_of_change_liq = Column(Integer)
    rate_of_change_liq = Column(Float)
    last_liq = Column(Float)
    last_signal_liq = Column(Integer)
    periode_since_signal_liq = Column(Integer)
    
class Analyses_Industry(Base):
    """
    id = Column(String, unique = True, primary_key=True)
    sector = Column(String)
    industry = Column(String)
    Boolean = Column(String)
    
    """

    __tablename__ = 'analyses_industry'
    
    id = Column(String, unique = True, primary_key=True)
    last_mon = Column(Float)
    last_liq = Column(Float)
    last_vol = Column(Float)
    last_avg_mon = Column(Float)
    last_avg_liq = Column(Float)
    last_avg_vol = Column(Float)
    profile_mon = Column(Integer)
    profile_liq = Column(Integer)
    profile_vol = Column(Integer) # this is volatility
    profile_avg_mon = Column(Integer)
    profile_avg_liq = Column(Integer)
    profile_avg_vol = Column(Integer) # this is volatility
    profile_avg_total_mon = Column(Integer) 
    profile_avg_total_liq = Column(Integer)
    profile_avg_total_vol = Column(Integer) # this is volatility
    last_profile_avg_mon = Column(Integer)
    last_profile_avg_liq = Column(Integer)
    last_profile_avg_vol = Column(Integer)
    
class Analyses_Industry_Forecast(Base):
    """
    id = Column(String, unique = True, primary_key=True)
    sector = Column(String)
    industry = Column(String)
    Boolean = Column(String)
    
    """
    __tablename__ = 'analyses_industry_forecast'
    id = Column(String, unique = True, primary_key=True)
    forecast_mon = Column(Float) 
    forecast_liq = Column(Float) 
    forecast_vol = Column(Float) 
    
class Analyses_Sector(Base):
    """
    
    Last is last score. 
    profile is statistic profile.
    avg_total is average on total. 
    
    """

    __tablename__ = 'analyses_sector'
    
    id = Column(String, unique = True, primary_key=True)
    last_mon = Column(Float)
    last_liq = Column(Float)
    last_vol = Column(Float)
    last_avg_mon = Column(Float)
    last_avg_liq = Column(Float)
    last_avg_vol = Column(Float)
    profile_mon = Column(Integer)
    profile_liq = Column(Integer)
    profile_vol = Column(Integer) # this is volatility
    profile_avg_mon = Column(Integer)
    profile_avg_liq = Column(Integer)
    profile_avg_vol = Column(Integer) # this is volatility
    profile_avg_total_mon = Column(Integer) 
    profile_avg_total_liq = Column(Integer)
    profile_avg_total_vol = Column(Integer) # this is volatility
    last_profile_avg_mon = Column(Integer)
    last_profile_avg_liq = Column(Integer)
    last_profile_avg_vol = Column(Integer)
    
class Analyses_Sector_Forecast(Base):
    """
    id = Column(String, unique = True, primary_key=True)
    sector = Column(String)
    industry = Column(String)
    Boolean = Column(String)
    
    """
    __tablename__ = 'analyses_sector_forecast'
    
    id = Column(String, unique = True, primary_key=True)
    forecast_mon = Column(Float) 
    forecast_liq = Column(Float) 
    forecast_vol = Column(Float) 
    
    
    
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

class Analyses_archive_flowimpact(Base):
    
    __tablename__ = "analyses_archive_flowimpact"
    
    id = Column(Integer, primary_key=True)
    ticker  = Column(String)
    year    = Column(Integer)
    month   = Column(Integer)
    date    = Column(Integer)
    weeknr  = Column(Integer)
    periode = Column(String)
    Moneyflow = Column(Integer)
    Liquididy = Column(Integer)
    Score       = Column(Float)
    close       = Column(Float) 
    
    __table_args__ = (UniqueConstraint('ticker', 'year','month','date', name='_tickers_unique_value'),
                     )
    
    
class Analyses_archive_performance(Base):
    
    __tablename__ = "analyses_archive_performance"
    
    id = Column(Integer, primary_key=True)
    ticker  = Column(String)
    year    = Column(Integer)
    month   = Column(Integer)
    date    = Column(Integer)
    weeknr  = Column(Integer)
    periode = Column(String)
    side        = Column(Integer)
    itterations = Column(Integer)
    returns     = Column(Float)
    max_return  = Column(Float) 
    standard_devation = Column(Float) 
    yield_1w    = Column(Float) 
    yield_1m    = Column(Float) 
    yield_1q    = Column(Float) 
    
    
    __table_args__ = (UniqueConstraint('ticker', 'year','month','date','periode','side', name='_tickers_unique_value'),
                     )   
    
    
    
    
    
    
    
    
    