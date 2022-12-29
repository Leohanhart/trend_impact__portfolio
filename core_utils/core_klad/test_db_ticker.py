# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 17:13:42 2022

@author: Gebruiker
"""

import constants

from core_scripts.synchronization import synch_class
from core_scripts.stock_analyses import stock_analyses
from core_scripts.stock_data_download import power_stock_object
from core_utils.database_tables.tabels import Ticker

import sqlalchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

db_path = constants.SQLALCHEMY_DATABASE_URI
engine = create_engine(db_path, echo = True)            
Session = sessionmaker(bind=engine)
session = Session()

import uuid

class test:
    
    def __init__(self):
        
        self.add_ticker_and_more()
        
        for i in range(0,10):
            
            data = session.query(Ticker).get("AAPL")
            
            
            
            ticker = Ticker(id = str(uuid.uuid4()), 
                              sector = "DING", 
                              industry = "DING",
                              exchange = "DING",
                              active = True
                              )
            
            session.add(ticker)
            session.commit()

            
            #self.add_ticker_and_more()    
            
    def add_ticker_and_more(self):
    
        data = session.query(Ticker).get("AAPL")
        
        
        
        ticker = Ticker(id = str(uuid.uuid4()), 
                          sector = "DING", 
                          industry = "DING",
                          exchange = "DING",
                          active = True
                          )
        
        session.add(ticker)
        session.commit()

x = test()