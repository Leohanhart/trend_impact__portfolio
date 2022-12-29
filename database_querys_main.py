# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 14:25:08 2022

@author: Gebruiker

FIX TO DO 
- There is a problem with (Flow and liquidity) function, loads tickers that are positive and negative same instance.
fix this with multiple statments appeard to be very hard, SQLalchemy dont likes turnekey functions, mabey turn. 

FIX = add, postive only, netagive onle and add these to the querty function for execeturion.

TASKS TO DO: 
    
    AFTER NEW DATABASE MIGRATION 
    - create get _ analyseses (Liq / Mon) For daily tables and also update.







"""

import constants

from core_utils.database_tables.tabels import Ticker,Analyses_Liquidityimpact,Analyses_Moneyflow,Analyses_Industry, Analyses_Sector, Analyses_Moneyflow_Daily, Analyses_Liquidityimpact_Daily, log, Analyses_archive_flowimpact, Analyses_archive_performance

import pandas as pd


import json
from datetime import datetime
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
        
        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo = False)            
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
        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo = True)            
        Session = sessionmaker(bind=engine)
        session = Session()
        
        data = session.query(Ticker).filter(Ticker.active == True).all()
        data = database_querys_support.unpack_all_industrys(data)
        
        if "NA" in data: 
            
            data.remove("NA")
            
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
        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo = True)            
        Session = sessionmaker(bind=engine)
        session = Session()
        
        data = session.query(Ticker).filter(Ticker.active == True).all()
        data = database_querys_support.unpack_all_sectors(data)
        
        if "NA" in data: 
            
            data.remove("NA")
        
        session.close()
        
        return data
    
    @staticmethod
    def get_all_stocks_with_industry(name_industry : str = ""):
        """
    
        returns all industry name tickers        
        
        Parameters
        ----------
        name_industry : str, optional
            DESCRIPTION. The default is "".

        Returns
        -------
        data : TYPE
            DESCRIPTION.

        """
        
        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo = True)            
        Session = sessionmaker(bind=engine)
        session = Session()
        
        data = session.query(Ticker).filter(Ticker.industry == name_industry, Ticker.active == True).all()
        data = database_querys_support.unpack_all_tickers(data)
        
        session.close()
        
        if "NA" in data: 
            
            data.remove("NA")
        
        return data
    
    @staticmethod
    def get_all_stocks_with_sector(name_sector : str = ""):
        """
        
        returns all secotrs with the name of an industry.

        Parameters
        ----------
        name_sector : str, optional
            DESCRIPTION. The default is "".

        Returns
        -------
        data : TYPE
            DESCRIPTION.

        """
        
        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo = True)            
        Session = sessionmaker(bind=engine)
        session = Session()
        
        data = session.query(Ticker).filter(Ticker.sector == name_sector, Ticker.active == True).all()
        data = database_querys_support.unpack_all_tickers(data)
        
        session.close()
        
        if "NA" in data: 
            
            data.remove("NA")
        
        
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
        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo = True)            
        Session = sessionmaker(bind=engine)
        session = Session()
        
        query = session.query(Ticker).filter(Ticker.id == ticker).all()
        data = session.query(Ticker).filter(Ticker.sector == query[0].__dict__["sector"]).all()
        ticker = database_querys_support.unpack_all_tickers(data)
        
        session.close()
        
        if "NA" in data: 
            
            data.remove("NA")
        
        
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
        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo = True)            
        Session = sessionmaker(bind=engine)
        session = Session()
        
        query = session.query(Ticker).filter(Ticker.id == ticker).all()
        data = session.query(Ticker).filter(Ticker.industry == query[0].__dict__["industry"]).all()
        ticker = database_querys_support.unpack_all_tickers(data)
        
        session.close()
        
        if "NA" in data: 
            
            data.remove("NA")
        
        
        return ticker
    
    
    @staticmethod
    def get_analyses_flows_and_impact(as_pandas = False, daily : bool = False):
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
        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo = True)            
        Session = sessionmaker(bind=engine)
        session = Session()
        
        if not daily:
            
            if not as_pandas:
                
                # in een ver gaande theorie zou je ook & kunnen gebruiken voor and en | voor or 
                secon_query =  session.query(Analyses_Moneyflow,Analyses_Liquidityimpact).filter(and_(Analyses_Moneyflow.id == Analyses_Liquidityimpact.id, Analyses_Liquidityimpact.profile != 0, Analyses_Moneyflow.profile != 0 )).all()
                
                session.close()
                
                return secon_query
            
            else:
                
                query_string =  session.query(Analyses_Moneyflow,Analyses_Liquidityimpact).filter(and_(Analyses_Moneyflow.id == Analyses_Liquidityimpact.id, Analyses_Liquidityimpact.profile_liq != 0, Analyses_Moneyflow.profile_mon != 0 )).statement.compile()
                
                df = pd.read_sql_query(query_string,session.bind)
                
                session.close()
                
                return df
            
        else:
            if not as_pandas:
                
                # in een ver gaande theorie zou je ook & kunnen gebruiken voor and en | voor or 
                secon_query =  session.query(Analyses_Moneyflow_Daily, Analyses_Liquidityimpact_Daily).filter(and_(Analyses_Moneyflow_Daily.id == Analyses_Liquidityimpact_Daily.id, Analyses_Liquidityimpact_Daily.profile_liq != 0, Analyses_Moneyflow_Daily.profile_mon != 0 )).all()
                
                session.close()
                
                return secon_query
            else:
                
                query_string =  session.query(Analyses_Moneyflow_Daily, Analyses_Liquidityimpact_Daily).filter(and_(Analyses_Moneyflow_Daily.id == Analyses_Liquidityimpact_Daily.id, Analyses_Liquidityimpact_Daily.profile_liq != 0, Analyses_Moneyflow_Daily.profile_mon != 0 )).statement.compile()
                
                df = pd.read_sql_query(query_string,session.bind)
                
                session.close()
                
                return df
            
    
    @staticmethod
    def get_analyses_moneyflows(as_pandas = False, daily : bool = False):
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
        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo = True)            
        Session = sessionmaker(bind=engine)
        session = Session()
        # so if weekly
        if not daily:
            if not as_pandas:
                
                query = session.query(Analyses_Moneyflow).filter(Analyses_Moneyflow.profile_mon != 0 ).all()
                
                session.close()
                
                return query
            
            else:
                
                query_string = session.query(Analyses_Moneyflow).filter(Analyses_Moneyflow.profile_mon != 0 ).statement.compile()
                
                df = pd.read_sql_query(query_string,session.bind)
                
                session.close()
                
                return df
        # so daily
        else:
            if not as_pandas:
                
                query = session.query(Analyses_Moneyflow_Daily).filter(Analyses_Moneyflow_Daily.profile_mon != 0 ).all()
                
                session.close()
                
                return query
            
            else:
                
                query_string = session.query(Analyses_Moneyflow_Daily).filter(Analyses_Moneyflow_Daily.profile_mon != 0 ).statement.compile()
                
                df = pd.read_sql_query(query_string,session.bind)
                
                session.close()
                
                return df
            
            

    @staticmethod
    def get_analyses_liquidity(as_pandas = False, daily : bool = False):
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
        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo = True)            
        Session = sessionmaker(bind=engine)
        session = Session()
        
        if not daily:
            # if not as pandas return as query. 
            if not as_pandas:
            
                query = session.query(Analyses_Liquidityimpact).filter(Analyses_Liquidityimpact.profile_liq != 0 ).all()
                
                session.close()
                
                return query
            
            # if panda's is wanted. 
            else:
                
                query_string = session.query(Analyses_Liquidityimpact).filter(Analyses_Liquidityimpact.profile_liq != 0 ).statement.compile()
                
                df = pd.read_sql_query(query_string,session.bind)
                
                session.close()
                
                return df
            
        else: 
            # if not as pandas return as query. 
            if not as_pandas:
            
                query = session.query(Analyses_Liquidityimpact_Daily).filter(Analyses_Liquidityimpact_Daily.profile_liq != 0 ).all()
                
                session.close()
                
                return query
            
            # if panda's is wanted. 
            else:
                
                query_string = session.query(Analyses_Liquidityimpact_Daily).filter(Analyses_Liquidityimpact_Daily.profile_liq != 0 ).statement.compile()
                
                df = pd.read_sql_query(query_string,session.bind)
                
                session.close()
                
                return df

    @staticmethod
    def get_analyses_industry(as_pandas = False):
        
        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo = True)            
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # if not as pandas return as query. 
        if not as_pandas:
        
            query = session.query(Analyses_Industry).all()
            
            session.close()
            
            return query
        
        # if panda's is wanted. 
        else:
            
            query_string = session.query(Analyses_Industry).statement.compile()
            
            df = pd.read_sql_query(query_string,session.bind)
            
            session.close()
            
            return df

    @staticmethod
    def get_analyses_sector(as_pandas = False):
        """
        

        Parameters
        ----------
        as_pandas : TYPE, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        
        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo = True)            
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # if not as pandas return as query. 
        if not as_pandas:
        
            query = session.query(Analyses_Sector).all()
            
            session.close()
            
            return query
        
        # if panda's is wanted. 
        else:
            
            query_string = session.query(Analyses_Sector).statement.compile()
            
            df = pd.read_sql_query(query_string,session.bind)
            
            session.close()
            
            return df
    
    
    @staticmethod
    def get_analyses_flow_impact_with_performance(ticker : str = None,
                                         periode : str = "W",
                                         year : int = 2020, 
                                         month :int = 1, 
                                         day : int = 12, 
                                         weeknr : int = None,
                                         as_pandas = True):
        """
        

        Parameters
        ----------
        ticker : str, optional
            DESCRIPTION. The default is None.
        periode : str, optional
            DESCRIPTION. The default is None.
        year : int, optional
            DESCRIPTION. The default is None.
        month : int, optional
            DESCRIPTION. The default is None.
        day : int, optional
            DESCRIPTION. The default is None.
        weeknr : int, optional
            DESCRIPTION. The default is None.
        as_pandas : TYPE, optional
            DESCRIPTION. The default is True.

        Returns
        -------
        None.

        """
       
        
        # creates database engine.
        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo = True)            
        Session = sessionmaker(bind=engine)
        session = Session()

        if type(ticker) == str:
            
            # if pandas, return all. 
            if as_pandas:
                    
                    
                    if periode == None :
                        
                        query_string = session.query(Analyses_archive_flowimpact,Analyses_archive_performance).filter(
                            and_(Analyses_archive_flowimpact.ticker     == ticker,
                                 Analyses_archive_performance.ticker    == ticker ,
                                 Analyses_archive_performance.periode   == "W" , 
                                 Analyses_archive_flowimpact.periode    == "W", 
                                 Analyses_archive_flowimpact.year       == Analyses_archive_performance.year,
                                 Analyses_archive_flowimpact.month      == Analyses_archive_performance.month,
                                 Analyses_archive_flowimpact.date       == Analyses_archive_performance.date,
                                 #Analyses_archive_performance.side == 1, 
                                 Analyses_archive_flowimpact.weeknr == Analyses_archive_performance.weeknr )).statement.compile()

                        
                        
                        df = pd.read_sql_query(query_string , session.bind)
                        
                        # close session
                        session.close()
                        
                        # return frame. 
                        return df
                        
                    elif periode != None:
                        
                        # generate query
                        query_string = session.query(Analyses_archive_flowimpact,Analyses_archive_performance).filter(
                            and_(Analyses_archive_flowimpact.ticker     == ticker,
                                 Analyses_archive_performance.ticker    == ticker ,
                                 Analyses_archive_performance.periode   == "W" , 
                                 Analyses_archive_flowimpact.periode    == "W", 
                                 Analyses_archive_flowimpact.year       == Analyses_archive_performance.year,
                                 Analyses_archive_flowimpact.month      == Analyses_archive_performance.month,
                                 Analyses_archive_flowimpact.date       == Analyses_archive_performance.date,
                                 Analyses_archive_performance.side == 1, 
                                 Analyses_archive_flowimpact.weeknr == Analyses_archive_performance.weeknr )).statement.compile()

                        
                        
                        # load dataframe with query
                        
                        df = pd.read_sql_query(query_string , session.bind)
                        
                        # close session
                        session.close()
                        
                        # return frame. 
                        return df
                    
        else: 
            
            return 404 
        """
        
        #query_string = session.query(Analyses_archive_flowimpact,
        #                             Analyses_archive_performance
        #                             ).filter(
        #Analyses_archive_performance.ticker == Analyses_archive_flowimpact.ticker
        #Analyses_archive_performance.ticker == ticker,
        #Analyses_archive_flowimpact.year == Analyses_archive_performance.year,
        #Analyses_archive_flowimpact.month == Analyses_archive_performance.month,
        #Analyses_archive_flowimpact.date == Analyses_archive_performance.date,
        #Analyses_archive_flowimpact.periode == periode    ,
        #Analyses_archive_performance.periode == periode, 
        #Analyses_archive_performance.side == 1
        #).statement.compile()#.all()
    
        query_string = session.query(Analyses_archive_flowimpact,Analyses_archive_performance).filter(
            and_(Analyses_archive_flowimpact.ticker     == ticker,
                 Analyses_archive_performance.ticker    == ticker ,
                 Analyses_archive_performance.periode   == periode , 
                 Analyses_archive_flowimpact.periode    == periode, 
                 Analyses_archive_flowimpact.year       == Analyses_archive_performance.year,
                 Analyses_archive_flowimpact.month      == Analyses_archive_performance.month,
                 Analyses_archive_flowimpact.date       == Analyses_archive_performance.date,
                 Analyses_archive_performance.side == 1, 
                 Analyses_archive_flowimpact.weeknr == Analyses_archive_performance.weeknr )).statement.compile()


        df = pd.read_sql_query(query_string , session.bind)
        
        # close session
        session.close()
        
        # return frame. 
        return df
        
        
        return 
        """
        """
            # there was a MINDBOGGLEING BLUE SCREEN ERROR IN THE SECOND QUERY. DONT USE. 
            pass
            # periode weeknr or not. 
            if periode == "W":
                
                if  type(weeknr) != int:
                    
                    query_string = session.query(Analyses_archive_flowimpact,Analyses_archive_performance).filter(
                             Analyses_archive_performance.periode   == periode , 
                             Analyses_archive_flowimpact.periode    == periode, 
                             Analyses_archive_flowimpact.year       == year,
                             Analyses_archive_performance.year      == year,
                             Analyses_archive_flowimpact.month      == month,
                             Analyses_archive_performance.month     == month,
                             Analyses_archive_flowimpact.date       == day,
                             Analyses_archive_performance.date      == day,
                             Analyses_archive_performance.side      == 1
                             ).statement.compile()
                    
                    df = pd.read_sql_query(query_string , session.bind)
                    
                    # close session
                    session.close()
                    
                    # return frame. 
                    return df

                else:
                    
                    query_string = session.query(Analyses_archive_flowimpact,Analyses_archive_performance).filter(
                             #Analyses_archive_performance.periode   == periode , 
                             Analyses_archive_flowimpact.periode    == periode, 
                             Analyses_archive_flowimpact.year       == year,
                             #Analyses_archive_performance.year      == year,
                             Analyses_archive_flowimpact.weeknr     == weeknr,
                             #Analyses_archive_performance.weeknr    == weeknr
                             ).statement.compile()
                    
                    df = pd.read_sql_query(query_string , session.bind)
                    
                    # close session
                    session.close()
                    
                    # return frame. 
                    return df
            # daily
            else:
                
                query_string = session.query(Analyses_archive_flowimpact,Analyses_archive_performance).filter(
                         Analyses_archive_performance.periode   == periode, 
                         Analyses_archive_flowimpact.periode    == periode, 
                         Analyses_archive_flowimpact.year       == year,
                         Analyses_archive_performance.year      == year,
                         Analyses_archive_flowimpact.month      == month,
                         Analyses_archive_performance.month     == month,
                         Analyses_archive_flowimpact.date       == day,
                         Analyses_archive_performance.date      == day,
                         Analyses_archive_performance.side      == 1
                         ).statement.compile()
                
                df = pd.read_sql_query(query_string , session.bind)
                
                # close session
                session.close()
                
                # return frame. 
                return df
            
            
           
        """
                    
        
    
    @staticmethod
    def get_analyses_flow_impact_archive(ticker : str = None,
                                         periode : str = None,
                                         year : int = None, 
                                         month :int = None, 
                                         day : int = None, 
                                         weeknr : int = None,
                                         as_pandas = True):
        """
        

        Returns
        -------
        None.

        
        """
 
        
        # creates database engine.
        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo = True)            
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # if tocker only 
        # senario's, 1. Researche wants it all. 2. wants specefic stock with periode. 3. wants specefic date, with periode. 
        
        
        
        if type(ticker) == str:
            
            # if pandas, return all. 
            if as_pandas:
                    
                    
                    if periode == None :
                        
                        query_string = session.query(Analyses_archive_flowimpact).filter(
                        Analyses_archive_flowimpact.ticker == ticker                   
                        ).statement.compile()#.all()
                        # load dataframe with query
                        
                        df = pd.read_sql_query(query_string , session.bind)
                        
                        # close session
                        session.close()
                        
                        # return frame. 
                        return df
                        
                    elif periode != None:
                        
                        # generate query
                        query_string = session.query(Analyses_archive_flowimpact).filter(
                        Analyses_archive_flowimpact.ticker == ticker,
                        Analyses_archive_flowimpact.periode == periode
                        ).statement.compile()#.all()
                        # load dataframe with query
                        
                        df = pd.read_sql_query(query_string , session.bind)
                        
                        # close session
                        session.close()
                        
                        # return frame. 
                        return df
                    
                    
                    elif type(year) == int and  type(month) == int and type(day) == int and type(weeknr) == None and periode != None: 
                        
                                               
                        # generate query
                        query_string = session.query(Analyses_archive_flowimpact).filter(
                        Analyses_archive_flowimpact.ticker == ticker,
                        Analyses_archive_flowimpact.periode == periode,
                        Analyses_archive_flowimpact.year == year,
                        Analyses_archive_flowimpact.month == month,
                        Analyses_archive_flowimpact.date == day
                        # generate 
                        ).statement.compile()#.all()
                        # load dataframe with query
                        
                        df = pd.read_sql_query(query_string , session.bind)
                        
                        # close session
                        session.close()
                        
                        # return frame. 
                        return df
                    
                    elif type(year) == int and  type(month) == int and type(day) == int and type(weeknr) == None and periode == None: 
                        
                                               
                        # generate query
                        query_string = session.query(Analyses_archive_flowimpact).filter(
                        Analyses_archive_flowimpact.ticker == ticker,
                        Analyses_archive_flowimpact.year == year,
                        Analyses_archive_flowimpact.month == month,
                        Analyses_archive_flowimpact.date == day
                        # generate 
                        ).statement.compile()#.all()
                        # load dataframe with query
                        
                        df = pd.read_sql_query(query_string , session.bind)
                        
                        # close session
                        session.close()
                        
                        # return frame. 
                        return df
                    
                    elif type(weeknr) != None and periode != None: 
                        
                                                
                        # generate query
                        query_string = session.query(Analyses_archive_flowimpact).filter(
                        Analyses_archive_flowimpact.weeknr == weeknr
                        # generate 
                        ).statement.compile()#.all()
                        # load dataframe with query
                        
                        df = pd.read_sql_query(query_string , session.bind)
                        
                        # close session
                        session.close()
                        
                        # return frame. 
                        return df
                        # generate 
                    
               

                
        if ticker == None:
            
            if as_pandas:
                
                if type(year) == int and type(month) == int and type(day) == int and type(weeknr) != int and periode != None: 
                                           
                    # generate query
                    query_string = session.query(Analyses_archive_flowimpact).filter(
                    Analyses_archive_flowimpact.periode == periode,
                    Analyses_archive_flowimpact.year == year,
                    Analyses_archive_flowimpact.month == month,
                    Analyses_archive_flowimpact.date == day
                    # generate 
                    ).statement.compile()#.all()
                    # load dataframe with query
                    
                    df = pd.read_sql_query(query_string , session.bind)
                    
                    # close session
                    session.close()
                    
                    # return frame. 
                    return df
                
                elif type(year) == int and  type(month) == int and type(day) == int and type(weeknr) == None and periode == None: 
                    
                                           
                    # generate query
                    query_string = session.query(Analyses_archive_flowimpact).filter(
                    Analyses_archive_flowimpact.year == year,
                    Analyses_archive_flowimpact.month == month,
                    Analyses_archive_flowimpact.date == day
                    # generate 
                    ).statement.compile()#.all()
                    # load dataframe with query
                    
                    df = pd.read_sql_query(query_string , session.bind)
                    
                    # close session
                    session.close()
                    
                    # return frame. 
                    return df
                
                elif type(year) == int and type(weeknr) == int and type(periode) == str: 
                    
                                            
                    # generate query
                    query_string = session.query(Analyses_archive_flowimpact).filter(
                    Analyses_archive_flowimpact.periode == periode,
                    Analyses_archive_flowimpact.year == year,
                    Analyses_archive_flowimpact.weeknr == weeknr
                    # generate 
                    ).statement.compile()#.all()
                    # load dataframe with query
                    
                    df = pd.read_sql_query(query_string , session.bind)
                    
                    # close session
                    session.close()
                    
                    # return frame. 
                    return df
                
                    # generate 
                
                elif type(year) == int and type(weeknr) != None and periode == None: 
                    
                                            
                    # generate query
                    query_string = session.query(Analyses_archive_flowimpact).filter(
                    Analyses_archive_flowimpact.year == year,
                    Analyses_archive_flowimpact.weeknr == weeknr
                    # generate 
                    ).statement.compile()#.all()
                    # load dataframe with query
                    
                    df = pd.read_sql_query(query_string , session.bind)
                    
                    # close session
                    session.close()
                    
                    # return frame. 
                    return df
                
                    # generate 
                
                
        return 404            
                
    @staticmethod
    def get_analyses_performance_archive(ticker : str = None,
                                         periode : str = None,
                                         year : int = None, 
                                         month :int = None, 
                                         day : int = None, 
                                         weeknr : int = None,
                                         as_pandas = True):
        """
        

        Returns
        -------
        None.

        
        """
     
        
        # creates database engine.
        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo = True)            
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # if tocker only 
        # senario's, 1. Researche wants it all. 2. wants specefic stock with periode. 3. wants specefic date, with periode. 
        
        
        
        if type(ticker) == str:
            
            # if pandas, return all. 
            if as_pandas:
                    
                    
                    if periode == None :
                        
                        query_string = session.query(Analyses_archive_performance).filter(
                        Analyses_archive_performance.ticker == ticker                   
                        ).statement.compile()#.all()
                        # load dataframe with query
                        
                        df = pd.read_sql_query(query_string , session.bind)
                        
                        # close session
                        session.close()
                        
                        # return frame. 
                        return df
                        
                    elif periode != None:
                        
                        # generate query
                        query_string = session.query(Analyses_archive_performance).filter(
                        Analyses_archive_performance.ticker == ticker,
                        Analyses_archive_performance.periode == periode
                        ).statement.compile()#.all()
                        # load dataframe with query
                        
                        df = pd.read_sql_query(query_string , session.bind)
                        
                        # close session
                        session.close()
                        
                        # return frame. 
                        return df
                    
                    
                    elif type(year) == int and  type(month) == int and type(day) == int and type(weeknr) == None and periode != None: 
                        
                                               
                        # generate query
                        query_string = session.query(Analyses_archive_performance).filter(
                        Analyses_archive_performance.ticker == ticker,
                        Analyses_archive_performance.periode == periode,
                        Analyses_archive_performance.year == year,
                        Analyses_archive_performance.month == month,
                        Analyses_archive_performance.date == day
                        # generate 
                        ).statement.compile()#.all()
                        # load dataframe with query
                        
                        df = pd.read_sql_query(query_string , session.bind)
                        
                        # close session
                        session.close()
                        
                        # return frame. 
                        return df
                    
                    elif type(year) == int and  type(month) == int and type(day) == int and type(weeknr) == None and periode == None: 
                        
                                               
                        # generate query
                        query_string = session.query(Analyses_archive_performance).filter(
                        Analyses_archive_performance.ticker == ticker,
                        Analyses_archive_performance.year == year,
                        Analyses_archive_performance.month == month,
                        Analyses_archive_performance.date == day
                        # generate 
                        ).statement.compile()#.all()
                        # load dataframe with query
                        
                        df = pd.read_sql_query(query_string , session.bind)
                        
                        # close session
                        session.close()
                        
                        # return frame. 
                        return df
                    
                    elif type(weeknr) != None and periode != None: 
                        
                                                
                        # generate query
                        query_string = session.query(Analyses_archive_performance).filter(
                        Analyses_archive_performance.weeknr == weeknr
                        # generate 
                        ).statement.compile()#.all()
                        # load dataframe with query
                        
                        df = pd.read_sql_query(query_string , session.bind)
                        
                        # close session
                        session.close()
                        
                        # return frame. 
                        return df
                        # generate 
                    
               

                
        if ticker == None:
            
            if as_pandas:
                
                if type(year) == int and type(month) == int and type(day) == int and type(weeknr) != int and periode != None: 
                                           
                    # generate query
                    query_string = session.query(Analyses_archive_performance).filter(
                    Analyses_archive_performance.periode == periode,
                    Analyses_archive_performance.year == year,
                    Analyses_archive_performance.month == month,
                    Analyses_archive_performance.date == day
                    # generate 
                    ).statement.compile()#.all()
                    # load dataframe with query
                    
                    df = pd.read_sql_query(query_string , session.bind)
                    
                    # close session
                    session.close()
                    
                    # return frame. 
                    return df
                
                elif type(year) == int and  type(month) == int and type(day) == int and type(weeknr) == None and periode == None: 
                    
                                           
                    # generate query
                    query_string = session.query(Analyses_archive_performance).filter(
                    Analyses_archive_performance.year == year,
                    Analyses_archive_performance.month == month,
                    Analyses_archive_performance.date == day
                    # generate 
                    ).statement.compile()#.all()
                    # load dataframe with query
                    
                    df = pd.read_sql_query(query_string , session.bind)
                    
                    # close session
                    session.close()
                    
                    # return frame. 
                    return df
                
                elif type(year) == int and type(weeknr) == int and type(periode) == str: 
                    
                                            
                    # generate query
                    query_string = session.query(Analyses_archive_performance).filter(
                    Analyses_archive_performance.periode == periode,
                    Analyses_archive_performance.year == year,
                    Analyses_archive_performance.weeknr == weeknr
                    # generate 
                    ).statement.compile()#.all()
                    # load dataframe with query
                    
                    df = pd.read_sql_query(query_string , session.bind)
                    
                    # close session
                    session.close()
                    
                    # return frame. 
                    return df
                
                    # generate 
                
                elif type(year) == int and type(weeknr) != None and periode == None: 
                    
                                            
                    # generate query
                    query_string = session.query(Analyses_archive_performance).filter(
                    Analyses_archive_performance.year == year,
                    Analyses_archive_performance.weeknr == weeknr
                    # generate 
                    ).statement.compile()#.all()
                    # load dataframe with query
                    
                    df = pd.read_sql_query(query_string , session.bind)
                    
                    # close session
                    session.close()
                    
                    # return frame. 
                    return df
                
                    # generate 
                
                
        return 404                
        
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
        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo = True)            
        Session = sessionmaker(bind=engine)
        session = Session()
        
        if periode == "D":
            
            x = session.query(Analyses_Moneyflow_Daily).filter(Analyses_Moneyflow_Daily.id == ticker_id
                                                         ).first()
            
            #x = session.query(Analyses_Liquidityimpact).get(ticker_id, )
            
            
            if x == None: 
                
                
                
                Mon_analyses = Analyses_Moneyflow_Daily(id = ticker_id, 
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
                
    
                x.profile_mon = profile
                x.profile_rate_of_change_mon = profile_rate_of_change
                x.rate_of_change_mon = rate_of_change
                x.last_mon = last
                x.last_signal_mon = last_signal
                x.periode_since_signal_mon = periode_since_signal
                
                session.commit()
            
            session.close()
            
        elif periode == "W":
            
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
        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo = True)            
        Session = sessionmaker(bind=engine)
        session = Session()
        
        if periode == "D": 
            
            x = session.query(Analyses_Liquidityimpact_Daily).filter(Analyses_Liquidityimpact_Daily.id == ticker_id
                                                               ).first()
            
            if x == None : 
                
                
                
                Liq_analyses = Analyses_Liquidityimpact_Daily(id = ticker_id, 
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
                
    
                
                x.profile_liq = profile
                x.profile_rate_of_change_liq = profile_rate_of_change
                x.rate_of_change_liq = rate_of_change
                x.last_liq = last
                x.last_signal_liq = last_signal
                x.periode_since_signal_liq = periode_since_signal
                
                session.commit()
                
        elif periode == "W":
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
                
    
                
                x.profile_liq = profile
                x.profile_rate_of_change_liq = profile_rate_of_change
                x.rate_of_change_liq = rate_of_change
                x.last_liq = last
                x.last_signal_liq = last_signal
                x.periode_since_signal_liq = periode_since_signal
                
                session.commit()
            
            session.close()
            
            return True

    @staticmethod
    def update_analyses_industry(   id_in : str = None,
                                    last_mon : float = None, 
                                    last_liq : float = None, 
                                    last_vol : float = None, 
                                    last_avg_mon : float = None, 
                                    last_avg_liq : float = None, 
                                    last_avg_vol : float = None, 
                                    profile_mon : int = None, 
                                    profile_liq : int = None, 
                                    profile_vol : int = None, # this is volatility
                                    profile_avg_mon : int = None, 
                                    profile_avg_liq : int = None, 
                                    profile_avg_vol : int = None,  # this is volatility
                                    profile_avg_total_mon : int = None,  
                                    profile_avg_total_liq : int = None, 
                                    profile_avg_total_vol : int = None,  # this is volatility
                                    last_profile_avg_mon : int = None, 
                                    last_profile_avg_liq : int = None, 
                                    last_profile_avg_vol : int = None ):
        """
        

        Parameters
        ----------
        id : str, optional
            DESCRIPTION. id is the string of the id
        last_mon : float, optional
            DESCRIPTION. last real value
        last_liq : float, optional
            DESCRIPTION. last liquidit impact value
        last_vol : float, optional
            DESCRIPTION. last volatility 
        last_avg_mon : float, optional
            DESCRIPTION. average moneyflow
        last_avg_liq : float, optional
            DESCRIPTION. average liqduiity
        last_avg_vol : float, optional
            DESCRIPTION. average volatiltiy
        profile_mon : int, optional
            DESCRIPTION. profile moneyflow
        profile_liq : int, optional
            DESCRIPTION. profile liquidity
        profile_vol : int, optional
            DESCRIPTION. profile volatility
        # this is volatility                                    profile_avg_mon : int, optional
            DESCRIPTION. Average profile = total / total tickers
        profile_avg_liq : int, optional
            DESCRIPTION. average profile liquidity
        profile_avg_vol : int, optional
            DESCRIPTION. average profile volatility
        # this is volatility                                    profile_avg_total_mon : int, optional
            DESCRIPTION. 
        profile_avg_total_liq : int, optional
            DESCRIPTION. profile based on total analyses, so all industries average liquidity profile / Mean, STD / MAIN = profile
        profile_avg_total_vol : int, optional
            DESCRIPTION. profile volatility based on main 
        # this is volatility                                    last_profile_avg_mon : int, optional
            DESCRIPTION. pofile based on real value.  agains total
        last_profile_avg_liq : int, optional
            DESCRIPTION. pofile based on real value.  agains total
        last_profile_avg_vol : int, optional
            DESCRIPTION. pofile based on real value.  agains total

        Returns
        -------
        None.

        """

        
        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo = True)            
        Session = sessionmaker(bind=engine)
        session = Session()
        
        x = session.query(Analyses_Industry).filter(Analyses_Industry.id == id_in
                                                           ).first()
        # check if ticker exsists
        if x == None: 
            
            
            # if not assinged, object needs to be made. 
            Industry_analyses = Analyses_Industry(id = id_in,
                                                  last_mon = 0, 
                                                  last_liq = 0, 
                                                  last_vol = 0, 
                                                  last_avg_mon = 0, 
                                                  last_avg_liq = 0, 
                                                  last_avg_vol = 0, 
                                                  profile_mon = 0, 
                                                  profile_liq = 0, 
                                                  profile_vol = 0, # this is volatility
                                                  profile_avg_mon = 0, 
                                                  profile_avg_liq = 0, 
                                                  profile_avg_vol = 0,  # this is volatility
                                                  profile_avg_total_mon = 0,  
                                                  profile_avg_total_liq = 0, 
                                                  profile_avg_total_vol = 0,  # this is volatility
                                                  last_profile_avg_mon = 0, 
                                                  last_profile_avg_liq = 0, 
                                                  last_profile_avg_vol = 0)
            # adds and commits
            session.add(Industry_analyses)
            session.commit()
            session.close()
            
            # resets the connection
            db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
            engine = create_engine(db_path, echo = True)            
            Session = sessionmaker(bind=engine)
            session = Session()
            
            x = session.query(Analyses_Industry).filter(Analyses_Industry.id == id_in
                                                               ).first()
        
        items = [ id_in, last_mon, last_liq, last_vol, last_avg_mon , 
                 last_avg_liq,last_avg_vol,profile_mon, profile_liq, 
                 profile_vol, profile_avg_mon,profile_avg_liq, profile_avg_vol, profile_avg_total_mon, profile_avg_total_liq , 
                                              profile_avg_total_vol,last_profile_avg_mon,last_profile_avg_liq, last_profile_avg_vol ]
        
        
        # checks if there is one item that contians a int or an float, if so updates. 
        if any(isinstance(item, int) for item in items)or any(isinstance(item, float) for item in items) and x != None: 
            
            if last_mon:
                
                x.last_mon = last_mon
            
            if last_liq != None:
                
                x.last_liq = last_liq
                
            if last_vol:
                
                x.last_vol = last_vol
                
            if last_avg_mon  :
                
                x.last_avg_mon = last_avg_mon
            
            if last_avg_liq:
                
                x.last_avg_liq = last_avg_liq
                
            if last_avg_vol:
                
                x.last_avg_vol = last_avg_vol
                
            if profile_mon:
                
                x.profile_mon = profile_mon
                
            if profile_liq:
                
                x.profile_liq = profile_liq
            
            if profile_vol:
                
                x.profile_vol = profile_vol
                
            if profile_avg_mon:
                
                profile_avg_mon = profile_avg_mon
                
            if profile_avg_liq:
                
                x.profile_avg_liq = profile_avg_liq
                
            if profile_avg_vol: 
                
                x.profile_avg_vol = profile_avg_vol
                
            if profile_avg_total_mon:
                
                x.profile_avg_total_mon = profile_avg_total_mon
                
            if profile_avg_total_liq:
                
                x.profile_avg_total_liq = profile_avg_total_liq 
                
            if profile_avg_total_vol:
                
                x.profile_avg_total_vol = profile_avg_total_vol 
                
            if last_profile_avg_mon:
                
                x.last_profile_avg_mon = last_profile_avg_mon 
                
            if last_profile_avg_liq: 
                
                x.last_profile_avg_liq = last_profile_avg_liq
                
            if last_profile_avg_vol: 
                
                x.last_profile_avg_vol = last_profile_avg_vol
            
            session.commit()
        
        session.close()
            

    @staticmethod
    def update_analyses_sector(   id_in : str = None,
                                    last_mon : float = None, 
                                    last_liq : float = None, 
                                    last_vol : float = None, 
                                    last_avg_mon : float = None, 
                                    last_avg_liq : float = None, 
                                    last_avg_vol : float = None, 
                                    profile_mon : int = None, 
                                    profile_liq : int = None, 
                                    profile_vol : int = None, # this is volatility
                                    profile_avg_mon : int = None, 
                                    profile_avg_liq : int = None, 
                                    profile_avg_vol : int = None,  # this is volatility
                                    profile_avg_total_mon : int = None,  
                                    profile_avg_total_liq : int = None, 
                                    profile_avg_total_vol : int = None,  # this is volatility
                                    last_profile_avg_mon : int = None, 
                                    last_profile_avg_liq : int = None, 
                                    last_profile_avg_vol : int = None ):
        """
        

        Parameters
        ----------
        id : str, optional
            DESCRIPTION. id is the string of the id
        last_mon : float, optional
            DESCRIPTION. last real value
        last_liq : float, optional
            DESCRIPTION. last liquidit impact value
        last_vol : float, optional
            DESCRIPTION. last volatility 
        last_avg_mon : float, optional
            DESCRIPTION. average moneyflow
        last_avg_liq : float, optional
            DESCRIPTION. average liqduiity
        last_avg_vol : float, optional
            DESCRIPTION. average volatiltiy
        profile_mon : int, optional
            DESCRIPTION. profile moneyflow
        profile_liq : int, optional
            DESCRIPTION. profile liquidity
        profile_vol : int, optional
            DESCRIPTION. profile volatility
        # this is volatility                                    profile_avg_mon : int, optional
            DESCRIPTION. Average profile = total / total tickers
        profile_avg_liq : int, optional
            DESCRIPTION. average profile liquidity
        profile_avg_vol : int, optional
            DESCRIPTION. average profile volatility
        # this is volatility                                    profile_avg_total_mon : int, optional
            DESCRIPTION. 
        profile_avg_total_liq : int, optional
            DESCRIPTION. profile based on total analyses, so all industries average liquidity profile / Mean, STD / MAIN = profile
        profile_avg_total_vol : int, optional
            DESCRIPTION. profile volatility based on main 
        # this is volatility                                    last_profile_avg_mon : int, optional
            DESCRIPTION. pofile based on real value.  agains total
        last_profile_avg_liq : int, optional
            DESCRIPTION. pofile based on real value.  agains total
        last_profile_avg_vol : int, optional
            DESCRIPTION. pofile based on real value.  agains total

        Returns
        -------
        None.

        """

        
        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo = True)            
        Session = sessionmaker(bind=engine)
        session = Session()
        
        x = session.query(Analyses_Sector).filter(Analyses_Sector.id == id_in
                                                           ).first()
        # check if ticker exsists
        if x == None: 
            
            
            # if not assinged, object needs to be made. 
            Industry_analyses = Analyses_Sector(id = id_in,
                                                  last_mon = 0, 
                                                  last_liq = 0, 
                                                  last_vol = 0, 
                                                  last_avg_mon = 0, 
                                                  last_avg_liq = 0, 
                                                  last_avg_vol = 0, 
                                                  profile_mon = 0, 
                                                  profile_liq = 0, 
                                                  profile_vol = 0, # this is volatility
                                                  profile_avg_mon = 0, 
                                                  profile_avg_liq = 0, 
                                                  profile_avg_vol = 0,  # this is volatility
                                                  profile_avg_total_mon = 0,  
                                                  profile_avg_total_liq = 0, 
                                                  profile_avg_total_vol = 0,  # this is volatility
                                                  last_profile_avg_mon = 0, 
                                                  last_profile_avg_liq = 0, 
                                                  last_profile_avg_vol = 0)
            # adds and commits
            session.add(Industry_analyses)
            session.commit()
            session.close()
            
            # resets the connection
            db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
            engine = create_engine(db_path, echo = True)            
            Session = sessionmaker(bind=engine)
            session = Session()
            
            x = session.query(Analyses_Industry).filter(Analyses_Industry.id == id_in
                                                               ).first()
        
        items = [ id_in, last_mon, last_liq, last_vol, last_avg_mon , 
                 last_avg_liq,last_avg_vol,profile_mon, profile_liq, 
                 profile_vol, profile_avg_mon,profile_avg_liq, profile_avg_vol, profile_avg_total_mon, profile_avg_total_liq , 
                                              profile_avg_total_vol,last_profile_avg_mon,last_profile_avg_liq, last_profile_avg_vol ]
        
        
        # checks if there is one item that contians a int or an float, if so updates. 
        if any(isinstance(item, int) for item in items)or any(isinstance(item, float) for item in items) and x != None: 
            
            if last_mon:
                
                x.last_mon = last_mon
            
            if last_liq != None:
                
                x.last_liq = last_liq
                
            if last_vol:
                
                x.last_vol = last_vol
                
            if last_avg_mon  :
                
                x.last_avg_mon = last_avg_mon
            
            if last_avg_liq:
                
                x.last_avg_liq = last_avg_liq
                
            if last_avg_vol:
                
                x.last_avg_vol = last_avg_vol
                
            if profile_mon:
                
                x.profile_mon = profile_mon
                
            if profile_liq:
                
                x.profile_liq = profile_liq
            
            if profile_vol:
                
                x.profile_vol = profile_vol
                
            if profile_avg_mon:
                
                profile_avg_mon = profile_avg_mon
                
            if profile_avg_liq:
                
                x.profile_avg_liq = profile_avg_liq
                
            if profile_avg_vol: 
                
                x.profile_avg_vol = profile_avg_vol
                
            if profile_avg_total_mon:
                
                x.profile_avg_total_mon = profile_avg_total_mon
                
            if profile_avg_total_liq:
                
                x.profile_avg_total_liq = profile_avg_total_liq 
                
            if profile_avg_total_vol:
                
                x.profile_avg_total_vol = profile_avg_total_vol 
                
            if last_profile_avg_mon:
                
                x.last_profile_avg_mon = last_profile_avg_mon 
                
            if last_profile_avg_liq: 
                
                x.last_profile_avg_liq = last_profile_avg_liq
                
            if last_profile_avg_vol: 
                
                x.last_profile_avg_vol = last_profile_avg_vol
            
            session.commit()
        
        session.close()
    
    def update_archive_flowimpact(model): 
        
    
        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo = True)            
        Session = sessionmaker(bind=engine)
        session = Session()
        
        x = session.query(Analyses_archive_flowimpact).filter(
            Analyses_archive_flowimpact.ticker == model.ticker,
            Analyses_archive_flowimpact.year == model.year,
            Analyses_archive_flowimpact.month == model.month,
            Analyses_archive_flowimpact.date == model.date
                                                           ).first()
        # check if ticker exsists
        if x == None: 
        
            Mon_archive_analyses = Analyses_archive_flowimpact(
                                                        
                                                        ticker  = model.ticker,
                                                        year    = model.year,
                                                        month   = model.month,
                                                        date    = model.date,
                                                        weeknr  = model.weeknr,
                                                        periode = model.periode,
                                                        Moneyflow = model.Moneyflow,
                                                        Liquididy = model.Liquididy,
                                                        Score       = model.Score,
                                                        close       = model.close
                                                
                                             )
            
            session.add(Mon_archive_analyses)
            session.commit()
        
        # else work with it.
        else:
            
            x.ticker  = model.ticker,
            x.year    = model.year,
            x.month   = model.month,
            x.date    = model.date,
            x.weeknr  = model.weeknr,
            x.periode = model.periode,
            x.Moneyflow = model.Moneyflow,
            x.Liquididy = model.Liquididy,
            x.Score       = model.Score,
            x.close       = model.close
            
            session.commit()
        
        session.close()

    def update_archive_performance(model): 
        
        
        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo = True)            
        Session = sessionmaker(bind=engine)
        session = Session()
        
        x = session.query(Analyses_archive_performance).filter(
            Analyses_archive_performance.ticker == model.ticker,
            Analyses_archive_performance.year   == model.year,
            Analyses_archive_performance.month  == model.month,
            Analyses_archive_performance.date   == model.date,
            Analyses_archive_performance.periode == model.periode,
            Analyses_archive_performance.side   == model.side
                                                           ).first()
        # check if ticker exsists
        if x == None: 
        
            performance_archive_analyses = Analyses_archive_performance(
                                                        
                                                    ticker  = model.ticker,
                                                    year    = model.year,
                                                    month   = model.month ,
                                                    date    = model.date,
                                                    weeknr  = model.weeknr,
                                                    periode = model.periode,
                                                    side        = int(model.side),
                                                    itterations = int(model.itterations),
                                                    returns     = model.returns,
                                                    max_return  = model.max_return,
                                                    standard_devation = model.standard_devation,
                                                    yield_1w    = model.yield_1w,
                                                    yield_1m    = model.yield_1m,
                                                    yield_1q    = model.yield_1q
                                                
                                             )
            
            session.add(performance_archive_analyses)
            session.commit()
        
        # else work with it.
        else:

            x.ticker  = model.ticker
            x.year    = model.year
            x.month   = model.month 
            x.date    = model.date
            x.weeknr  = model.weeknr
            x.periode = model.periode
            x.side        = model.side
            x.itterations = model.itterations
            x.returns     = model.returns
            x.max_return  = model.max_return
            x.standard_devation = model.standard_devation
            x.yield_1w    = model.yield_1w
            x.yield_1m    = model.yield_1m
            x.yield_1q    = model.yield_1q
            
            session.commit()
        
        session.close()
        
        
    
    def return_portoflolios():
        pass 
    
    def add_portolio_at_overview():
        pass
    
    def remove_portolio_at_overview():
        pass
    
    def trade_open_portfolio():
        pass
    
    def trade_close_portfolio(): 
        pass
    
    def trade_delete_portolio():
        pass 
    
    def log_item(id_int : int, message : str ):
        """
        adds log item.

        Parameters
        ----------
        id_int : int
            DESCRIPTION.
        message : str
            DESCRIPTION.

        Returns
        -------
        None.

        """
        
        # 
        now = datetime.now() # current date and time
        
        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo = False)            
        Session = sessionmaker(bind=engine)
        session = Session()
        
        date_time = now.strftime("%d-%m-%Y, %H:%M:%S")
        x = session.query(log).filter(log.id == id_int).first()
        
        if x == None : 
            
            
            
            Log = log(id = id_int, 
                      message = message + " " + date_time)
            
            session.add(Log)
            session.commit()
            
        else:
            
            x.message = message + " " + date_time
            

            session.commit()
            
            


    def log_item_get(as_pandas : bool = True, as_json : bool = True):    
        
        # if not as pandas return as query. 
        db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
        engine = create_engine(db_path, echo = False)            
        Session = sessionmaker(bind=engine)
        session = Session()
        
        if not as_pandas:
        
            query = session.query(log).all()
            
            session.close()
            
            return query
        
        # if panda's is wanted. 
        else:
            
            query_string = session.query(log).statement.compile()
            
            data = pd.read_sql_query(query_string,session.bind)
            
            data.drop(['time_created', 'time_updated'], axis=1, inplace=True)
            
            session.close() 
            
            if not as_json: 
                return data 
            else:
                # transform data to json
                try: 
                    
                    data = data.to_dict(orient='records')
                
                # if packaging already done, dump and return.
                except AttributeError: 
                    
                    resp = json.dumps(data)
                    
                    return resp
                
                # else dump and return. 
                resp = json.dumps(data)
                return resp
                
            
        
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
        
        #### end
        
        print("START")
        
        #x = database_querys.get_analyses_flows_and_impact( )
        #global pandanas_pf
        #pandanas_pf = database_querys.get_all_stocks_with_industry(name_industry="Consumer Electronics")
        #x = database_querys.get_all_active_tickers()
        #database_querys.update_analyses_liquidity(ticker_id = "XLE", periode ="W", profile =None, profile_rate_of_change= 5, rate_of_change = 5, last = 10.00, last_signal =5, periode_since_signal=0)
        #database_querys.update_analyses_sector(id_in=  "Homos", last_mon = 2)
        #x = database_querys.get_analyses_liquidity(as_pandas=True,daily=True)
        global x 
        # x = database_querys.get_analyses_industry(as_pandas=True)
        x = database_querys.get_analyses_flow_impact_archive(ticker = "CSCO", periode="W")
        
        # print("  \n\n Score = ", x.Score.sum())
        #global list_industry
        
        #database_querys.log_item_get()
        #database_querys.log_item(12313,"test for no")
        #list_industry = database_querys.get_all_active_industrys()
        
        #global ticker_industry
        
        #ticker_industry = database_querys.get_all_stocks_with_industry( list_industry[8])
        print(x.tail(30))
        print("END")
        
    except Exception as e:
        
        raise Exception("Error with tickers", e)

        