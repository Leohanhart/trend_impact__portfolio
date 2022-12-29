# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 11:58:52 2022

@author: Gebruiker
"""

import constants


import sqlalchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from core_scripts.synchronization import synch_class
from core_scripts.stock_data_download import power_stock_object
from core_utils.database_tables.tabels import Ticker

import time
import uuid

import numpy as np
import os

#db_path = constants.SQLALCHEMY_DATABASE_URI
#engine = create_engine(db_path, echo = True)            
#Session = sessionmaker(bind=engine)
#session = Session()


class initialization():
    
    # the list for the tickers.
    tickers : list = []
    
    
    def __init__(self, load_tickers_only : bool = False):
        """
    
        /Dont use this function        
        
        Parameters
        ----------
        load_tickers_only : bool, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        # 
        pass
        
        stocks = initialization_support.load_tickers_txt() 
            
        # check tickers 
        if load_tickers_only:
            
            self.tickers = stocks
            
            return self.tickers
        
        # setting up db stream
        db_path = constants.SQLALCHEMY_DATABASE_URI
        engine = create_engine(db_path, echo = True)            
        Session = sessionmaker(bind=engine)
        session = Session()
       
        
        # loop true the tickers, add to DB
        for i in range(0,len(stocks)):
             
            db_path = constants.SQLALCHEMY_DATABASE_URI
            engine = create_engine(db_path, echo = True)            
            Session = sessionmaker(bind=engine)
            session = Session() 
            
            # 
            stock_ticker_in =  list(stocks.keys())[i]
            
            print(stock_ticker_in)
            
            # getting the stock object
            stocks_object = power_stock_object.power_stock_object(stock_ticker = stock_ticker_in)
            
            # testing if stock is: A, valide. B, still active. C, delisted 
            status_stock = initialization_support.check_if_ticker_valide(stocks_object)
            
            
            # query for DB
            data = session.query(Ticker).get(stock_ticker_in)
            
            # 
            # checks if the location exsists, if yes, action.
            if data == None: 
                
                if stocks_object.sector == None or stocks_object:
                    continue 
                # option 1, Ticker is active
                
                ticker = Ticker(id = stock_ticker_in, 
                                  sector = stocks_object.sector , 
                                  industry = stocks_object.industry,
                                  exchange = stocks_object.all_stock_data['exchange'],
                                  active = True
                                  )
                
                session.add(ticker)
                session.commit()
            
            else:
                
                if stocks_object.sector == None:
                    
                    #Ticker = unit_tests_and_errors(id = location, error = error, error_code = message) 

                    data.active = False

                    session.commit()
            
            session.close()
            
            
    
class initialization_support: 
    
    @staticmethod
    def check_if_ticker_valide(stocks_object : object = None):
        """
        Checks if ticker is valide, meaning: workable data, sector and industy and that stock is not delisted
        
        first check are based on invalide/mallefide, if error occures it will be because dataframe is loaded
        correctly, that's why if the exception is thrown this will result in a positive signal(return tru). 
        
        Parameters
        ----------
        stocks_object : object, optional
            DESCRIPTION. The default is None.

        Returns
        -------
        bool
            DESCRIPTION.

        """
        return True
        try:
        
            if(
                    not stocks_object.sector 
                    or stocks_object.stock_data == None
                    or type(stocks_object.stock_data) == None 
                    or stocks_object.stock_data is None 
                    ):
                return False
            else:
                return True
            
        except Exception as e:
            
            return True 
            
    
    @staticmethod
    def load_tickers_txt():
        """
        
        Loads stocks from the txt file.

        Returns
        -------
        stocks : DICT
        
            DESCRIPTION.

        """
        stocks = {}
        
        path_tickers = constants.TICKER_DATA___PATH
        
        path_file = os.path.join(path_tickers, 'stocks.txt')
        
        
        
        with open(path_file) as f:
            contents = f.readlines()
            #print(contents)
            
            # create a dictonary for the stocks.     
        for i in range(0,len(contents)):
            x = contents[i].replace("\n", "")
            stocks[x] = ""
            
        return stocks
    
    @staticmethod
    def speed_limiter(start_time : float = 0, end_time : float = 0, limiter : float = 2.6 ):
        """
        Speedlimiter calculates additional time and sleeps in the meanwhile.
        
        Used when a function needs to be speedlimit doe to api restrictions. 
        
        what happens is that the function calclulatse the passet time and sleeps the additional time so 
        
        te speedlimiter will not be upset. 

        Parameters
        ----------
        start_time : float, optional
            DESCRIPTION. The default is 0.
        end_time : float, optional
            DESCRIPTION. The default is 0.
        limiter : TYPE, optional
            DESCRIPTION. The default is 2.6.

        Returns
        -------
        None.

        """
        
        #print(start_time, end_time)
        
        # sets seconds past
        time_past = end_time - start_time
        
        #print(time_past)
        
        # subtracts the limit time
        additional_time = limiter - time_past   
        
        # if additional time is larger than 
        if additional_time > 0: 
            
            #print("this is the total sleep time", additional_time )
            
            #time.sleep(additional_time)
        
            return additional_time
        
        else:
            
            print("No time to sleep")
            
            return 0.0001
            
    @staticmethod
    def load_malfunctioning_ticker():
        pass
                    
    
class initiaze_tickers:
    
    def __init__(self):
            
        stocks = initialization_support.load_tickers_txt() 
        
        start_time = time.time()
        end_time = time.time()
        
        for stock in stocks:
            
            # handle speedlimmit Yahoo. 
            end_time = time.time()
            time_to_sleep = initialization_support.speed_limiter(start_time,end_time,2.6)
            time.sleep(time_to_sleep)
            start_time = time.time()
            
            
            global stocks_object
            # getting the stock object
            stocks_object = power_stock_object.power_stock_object(stock_ticker = stock)
            
            global status_stock
            # testing if stock is: A, valide. B, still active. C, delisted 
            status_stock = initialization_support.check_if_ticker_valide(stocks_object)
            
            
            print(stock)
            data = session.query(Ticker).get(stock)
            
            # tries to run all functions. 
            """
            
            3 types of stocks.
            1. Has sector, industry, timeseries, exchange
            2. Has industry, timeseries,
            3. is totally invlaide. 
            
            - Invalides have no timeserie. 
            
            There must be a check that or assigns the db vars with the value, otherwise NA. 
            
            
            
            """
            # check if sector is legid
            if not stocks_object.sector:
                
                sector_in = "NA"
                            
            else:
                
                sector_in = stocks_object.sector
                
                
            # check if industry is legid
            if not stocks_object.industry:
                
                industry_in = "NA"

            else:
                
                industry_in = stocks_object.industry
                                            
            # check if stockexchange is legid. 
            if not stocks_object.all_stock_data == False :
                
                exchange_in = "NA"

            else:
                
                exchange_in = stocks_object.all_stock_data['exchange']
                
            
            # tries manipulation on time serie, if fails, problem with time serie, stock is inactive.
            try: 
            
                stocks_object.stock_data.tail()
                
                active_in = True
            except:
                print("Time serie was not taileble")
                active_in = False
                
            
            
            # check if data is new. 
            if data == None:
                
                # if data is new, ticker is added, in_ data is inserted. if single var fails, rest is added anyway.
                ticker = Ticker(id = str(stock), 
                                  sector = sector_in, 
                                  industry = industry_in,
                                  exchange = exchange_in,
                                  active = active_in
                                  )
                # ticker class is added
                session.add(ticker)
                # ticker class is commited.
                session.commit()
                continue
               
            # if ticker already exsist there is only one var that's need to be maintained. The active var. 
            else:
                
                    
                
                # sets bool
                data.active = False
                # commits.
                session.commit()
                continue
            
                
            

    
                

            
        
if __name__ == "__main__":    
    
    try:
        
        x = initiaze_tickers()
        #stocks_object = power_stock_object.power_stock_object(stock_ticker = "AAIO")
        
        # testing if stock is: A, valide. B, still active. C, delisted 
        #status_stock = initialization_support.check_if_ticker_valide(stocks_object)
        
        #print(status_stock)
        
    except Exception as e:
        
        raise Exception("Error with tickers", e)

        
        
