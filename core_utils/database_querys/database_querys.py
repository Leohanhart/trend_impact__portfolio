# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 14:25:08 2022

@author: Gebruiker
"""

import constants

from core_scripts.synchronization import synch_class
from core_scripts.stock_analyses import stock_analyses
from core_scripts.stock_data_download import power_stock_object
from core_utils.database_tables.tabels import Ticker,Analyses_Liquidityimpact,Analyses_Moneyflow

import pandas as pd


import sqlalchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import and_, or_, not_



class database_querys:
    
    
    @staticmethod
    def get_all_active_tickers():
        """
        Returns 

        Returns
        -------
        data : List
            DESCRIPTION.
            list with all tickers:  
                ['ADTN',
             'ADTX',
             'ADUS',
             'ADV',
             'ADVM',
             'ADXN',
             'ADXS',
             'AEAC']

        """
        
        db_path = constants.SQLALCHEMY_DATABASE_URI
        engine = create_engine(db_path, echo = True)            
        Session = sessionmaker(bind=engine)
        session = Session()
        
        
        data = session.query(Ticker).filter(Ticker.active == True).all()
        data = database_querys_support.unpack_all_tickers(data)
        
        session.close()
        
        return data

    @staticmethod
    def get_all_active_industrys():
        """
        Returns all active industry's

        Returns
        -------
        data : TYPE
            DESCRIPTION.

        """
        db_path = constants.SQLALCHEMY_DATABASE_URI
        engine = create_engine(db_path, echo = True)            
        Session = sessionmaker(bind=engine)
        session = Session()
        
        data = session.query(Ticker).filter(Ticker.active == True).all()
        data = database_querys_support.unpack_all_industrys(data)
        
        session.close()
        
        return data
    
    @staticmethod
    def get_all_active_sectors():
        """
        Returns all active sectors

        Returns
        -------
        data : TYPE
            DESCRIPTION.

        """
        db_path = constants.SQLALCHEMY_DATABASE_URI
        engine = create_engine(db_path, echo = True)            
        Session = sessionmaker(bind=engine)
        session = Session()
        
        data = session.query(Ticker).filter(Ticker.active == True).all()
        data = database_querys_support.unpack_all_sectors(data)
    
        session.close()
        
        return data
    
    @staticmethod
    def get_all_stocks_with_industry(name_industry : str = ""):
        
        db_path = constants.SQLALCHEMY_DATABASE_URI
        engine = create_engine(db_path, echo = True)            
        Session = sessionmaker(bind=engine)
        session = Session()
        
        data = session.query(Ticker).filter(Ticker.industry == name_industry).all()
        data = database_querys_support.unpack_all_tickers(data)
        
        session.close()
        
        return data
    
    @staticmethod
    def get_all_stocks_with_sector(name_sector : str = ""):
        
        db_path = constants.SQLALCHEMY_DATABASE_URI
        engine = create_engine(db_path, echo = True)            
        Session = sessionmaker(bind=engine)
        session = Session()
        
        data = session.query(Ticker).filter(Ticker.sector == name_sector).all()
        data = database_querys_support.unpack_all_tickers(data)
        
        session.close()
        
        return data
        
        
    @staticmethod
    def get_sector_with_ticker(ticker : str = ""): 
        """
        Returns sector with ticker

        Parameters
        ----------
        ticker : str, optional
            DESCRIPTION. The default is "".

        Returns
        -------
        ticker : TYPE
            DESCRIPTION.

        """
        db_path = constants.SQLALCHEMY_DATABASE_URI
        engine = create_engine(db_path, echo = True)            
        Session = sessionmaker(bind=engine)
        session = Session()
        
        query = session.query(Ticker).filter(Ticker.id == ticker).all()
        data = session.query(Ticker).filter(Ticker.sector == query[0].__dict__["sector"]).all()
        ticker = database_querys_support.unpack_all_tickers(data)
        
        session.close()
        
        return ticker

    @staticmethod
    def get_industry_with_ticker(ticker : str = ""): 
        """
        Returns industry with ticker.

        Parameters
        ----------
        ticker : str, optional
            DESCRIPTION. The default is "".

        Returns
        -------
        ticker : TYPE
            DESCRIPTION.

        """
        db_path = constants.SQLALCHEMY_DATABASE_URI
        engine = create_engine(db_path, echo = True)            
        Session = sessionmaker(bind=engine)
        session = Session()
        
        query = session.query(Ticker).filter(Ticker.id == ticker).all()
        data = session.query(Ticker).filter(Ticker.industry == query[0].__dict__["industry"]).all()
        ticker = database_querys_support.unpack_all_tickers(data)
        
        session.close()
        
        return ticker
    
    
        pass
    
    @staticmethod
    def get_analyses_flows_and_impact(as_pandas = False):
        """
        Returns flowsanalyses and liquidity impact, 

        Parameters
        ----------
        as_pandas : TYPE, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        db_path = constants.SQLALCHEMY_DATABASE_URI
        engine = create_engine(db_path, echo = True)            
        Session = sessionmaker(bind=engine)
        session = Session()
        
        
        if not as_pandas:
            
            secon_query =  session.query(Analyses_Moneyflow,Analyses_Liquidityimpact).filter(and_(Analyses_Moneyflow.id == Analyses_Liquidityimpact.id, Analyses_Liquidityimpact.profile != 0, Analyses_Moneyflow.profile != 0 )).all()
            
            session.close()
            
            return secon_query
        else:
            
            query_string =  session.query(Analyses_Moneyflow,Analyses_Liquidityimpact).filter(and_(Analyses_Moneyflow.id == Analyses_Liquidityimpact.id, Analyses_Liquidityimpact.profile_liq != 0, Analyses_Moneyflow.profile_mon != 0 )).statement.compile()
            
            df = pd.read_sql_query(query_string,session.bind)
            
            session.close()
            
            return df
    
    @staticmethod
    def get_analyses_moneyflows(as_pandas = False):
        """
        
        Returns moneyflow analyses 

        Parameters
        ----------
        as_pandas : TYPE, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        db_path = constants.SQLALCHEMY_DATABASE_URI
        engine = create_engine(db_path, echo = True)            
        Session = sessionmaker(bind=engine)
        session = Session()
        
        if not as_pandas:
            
            query = session.query(Analyses_Moneyflow).filter(Analyses_Moneyflow.profile != 0 ).all()
            
            session.close()
            
            return query
        
        else:
            
            query_string = session.query(Analyses_Moneyflow).filter(Analyses_Moneyflow.profile != 0 ).statement.compile()
            
            df = pd.read_sql_query(query_string,session.bind)
            
            session.close()
            
            return df
            

    @staticmethod
    def get_analyses_liquidity(as_pandas = False):
        """
        Returns liquidity analyses.

        Parameters
        ----------
        as_pandas : TYPE, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        db_path = constants.SQLALCHEMY_DATABASE_URI
        engine = create_engine(db_path, echo = True)            
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # if not as pandas return as query. 
        if not as_pandas:
        
            query = session.query(Analyses_Liquidityimpact).filter(Analyses_Liquidityimpact.profile != 0 ).all()
            
            session.close()
            
            return query
        
        # if panda's is wanted. 
        else:
            
            query_string = session.query(Analyses_Liquidityimpact).filter(Analyses_Liquidityimpact.profile != 0 ).statement.compile()
            
            df = pd.read_sql_query(query_string,session.bind)
            
            session.close()
            
            return df
            
    
    @staticmethod
    def update_analyses_moneyflow(ticker_id : str = "", 
                                  periode : str = "W", 
                                  profile : int = 0, 
                                  profile_rate_of_change : int = 0, 
                                  rate_of_change : float= 0 , 
                                  last :float = 0,
                                  last_signal : int = 0,
                                  periode_since_signal = 0):
        """
        

        Parameters
        ----------
        ticker_id : TYPE, optional
            DESCRIPTION. The default is "".
        periode : str, optional
            DESCRIPTION. The default is "".
        profile : int, optional
            DESCRIPTION. The default is 0 : profile_rate_of_change : int = 0.
        last_update : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        db_path = constants.SQLALCHEMY_DATABASE_URI
        engine = create_engine(db_path, echo = True)            
        Session = sessionmaker(bind=engine)
        session = Session()
        
        x = session.query(Analyses_Moneyflow).filter(Analyses_Moneyflow.id == ticker_id,
                                                     Analyses_Moneyflow.periode_mon == periode
                                                     ).first()
        
        #x = session.query(Analyses_Liquidityimpact).get(ticker_id, )
        
        
        if x == None: 
            
            
            
            Mon_analyses = Analyses_Moneyflow(id = ticker_id, 
                                             periode_mon  = periode, 
                                             profile_mon  = profile,
                                             profile_rate_of_change_mon = profile_rate_of_change, 
                                             rate_of_change_mon = rate_of_change , 
                                             last_mon =  last,
                                             last_signal_mon = last_signal,
                                             periode_since_signal_mon = periode_since_signal
                                             )
            
            session.add(Mon_analyses)
            session.commit()
            
        else:
            
            Liq_analyses = Analyses_Moneyflow(id = ticker_id, 
                                             periode_mon  = periode, 
                                             profile_mon  = profile,
                                             profile_rate_of_change_mon = profile_rate_of_change, 
                                             rate_of_change_mon = rate_of_change , 
                                             last_mon =  last,
                                             last_signal_mon = last_signal,
                                             periode_since_signal_mon = periode_since_signal
                                             )
            
            x.profile_mon = profile
            x.profile_rate_of_change_mon = profile_rate_of_change
            x.rate_of_change_mon = rate_of_change
            x.last_mon = last
            x.last_signal_mon = last_signal
            x.periode_since_signal_mon = periode_since_signal
            
            session.commit()
        
        session.close()
    
    @staticmethod
    def update_analyses_liquidity(ticker_id : str = "", 
                                  periode : str = "", 
                                  profile : int = 0, 
                                  profile_rate_of_change : int = 0, 
                                  rate_of_change : float= 0 , 
                                  last :float = 0,
                                  last_signal : int = 0,
                                  periode_since_signal = 0):
        """
        

        Parameters
        ----------
        ticker_id : TYPE, optional
            DESCRIPTION. The default is "".
        periode : str, optional
            DESCRIPTION. The default is "".
        profile : int, optional
            DESCRIPTION. The default is 0 : profile_rate_of_change : int = 0.
        last_update : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        db_path = constants.SQLALCHEMY_DATABASE_URI
        engine = create_engine(db_path, echo = True)            
        Session = sessionmaker(bind=engine)
        session = Session()
        
        x = session.query(Analyses_Liquidityimpact).filter(Analyses_Liquidityimpact.id == ticker_id,
                                                           Analyses_Liquidityimpact.periode_liq == periode 
                                                           ).first()
        
        if x == None : 
            
            
            
            Liq_analyses = Analyses_Liquidityimpact(id = ticker_id, 
                                             periode_liq  = periode, 
                                             profile_liq  = profile,
                                             profile_rate_of_change_liq = profile_rate_of_change, 
                                             rate_of_change_liq = rate_of_change , 
                                             last_liq =  last,
                                             last_signal_liq = last_signal,
                                             periode_since_signal_liq = periode_since_signal
                                             )
            
            session.add(Liq_analyses)
            session.commit()
            
        else:
            
            Liq_analyses = Analyses_Liquidityimpact(id = ticker_id, 
                                             periode_liq  = periode, 
                                             profile_liq  = profile,
                                             profile_rate_of_change_liq = profile_rate_of_change, 
                                             rate_of_change_liq = rate_of_change , 
                                             last_liq =  last,
                                             last_signal_liq = last_signal,
                                             periode_since_signal_liq = periode_since_signal 
                                             )
            
            x.profile_liq = profile
            x.profile_rate_of_change_liq = profile_rate_of_change
            x.rate_of_change_liq = rate_of_change
            x.last_liq = last
            x.last_signal_liq = last_signal
            x.periode_since_signal_liq = periode_since_signal
            
            session.commit()
        
        session.close()
        
        return True

class database_querys_support:
    
    
    @staticmethod
    def check_incomming_vars():
        pass
    
    @staticmethod
    def unpack_all_tickers(tickers):
        
        tickers_list = []
        
        for i in tickers:
            tickers_list.append(i.id)
             
        return tickers_list
    
    @staticmethod
    def unpack_all_sectors(tickers):
        
        sector_list = []
        
        for i in tickers:
            
            if type(i.sector) == None:
                continue
            
            if i.sector == None:
                continue
            
            if i.sector is None:
                continue
            
            if i.sector not in sector_list:        
                sector_list.append(i.sector)
                
        return sector_list
    
    @staticmethod
    def unpack_all_industrys(tickers):
        
        industry_list = []
        
        for i in tickers:
            if i.industry:
                if i.industry not in industry_list:        
                    industry_list.append(i.industry)
            
             
        return industry_list
        
        
        
        
if __name__ == "__main__":    
    
    try:
        
        
        print("START")
        #global x 
        #x = database_querys.get_analyses_flows_and_impact( )
        #global pandanas_pf
        #pandanas_pf = database_querys.get_analyses_flows_and_impact( as_pandas = True)
        x = database_querys.get_all_active_tickers()
        #database_querys.update_analyses_moneyflow(ticker_id = "AAPL", periode ="W", profile =5, profile_rate_of_change= 5, rate_of_change = 5, last = 10.00, last_signal =5, periode_since_signal=0)
        #global list_industry
        #list_industry = database_querys.get_all_active_industrys()
        
        #global ticker_industry
        
        #ticker_industry = database_querys.get_all_stocks_with_industry( list_industry[8])
        print(x)
        print("END")
        
    except Exception as e:
        
        raise Exception("Error with tickers", e)

        