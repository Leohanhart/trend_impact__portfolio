# -*- coding: utf-8 -*-

import constants 

import database_querys_main as database_querys

import stock_analyses_with_ticker_main as stock_analyses_with_ticker

from core_scripts.stock_data_download import power_stock_object as stock_object

from core_update.update_analyses import update_support

import time
import numpy as np
import pandas as pd
import os
import datetime

#### this is the start


"""

Made to update flowimpact Archive, 

"""

class update_performance_indicators_archive(object):
    
    @staticmethod
    def update_backtest_trades_archive(amount_periode : int = 250, full_option : bool = False):
        """
        

        Parameters
        ----------
        amount_periode : int, optional
            DESCRIPTION. The default is 250.
        full_option : bool, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        None.

        """
        # load periodes
        periodes = ["D","W"]
        
        #load tickers 
        tickers = update_flowimpact_support.load_tickers()
        
        trade_data = None
        
        for periode_in in periodes:
            for ticker in tickers: 
                
                # load trades specefic periodes. W first. D second.
                if periode_in == "W":
                    trade_data = generate_backtest_trades.generate_backtest_trades(ticker_in = ticker
                                                                      , periode_weekly = True
                                                                      , tail_amount=amount_periode)
                else:
                    trade_data = generate_backtest_trades.generate_backtest_trades(ticker_in = ticker
                                                                      , periode_weekly =False
                                                                      , tail_amount=amount_periode)
                
                # ERROR HANDLED: if problem occures at data generation, this will prevent it from breaking the system.
                if trade_data is None:
                    continue
                
                
                # data in aggegrator
                aggegrator = data_aggegrate_backtest_trades()
                aggegrator.aggegrate(trade_data)
                
                for i in range(0,len(aggegrator.data_slides)):
                    
                    
                    model = aggegrator.data_slides[i]
                    
                    model.periode = periode_in
                    
                    try:
                        database_querys.database_querys.update_archive_performance(model)
                    except Exception as e: 
                        continue
                    
                    
        return 
                
            
    
class update_flowimpact_archive(object):
    
    @staticmethod
    def update_flow_impact_archive():
        """
        
        updates flowimpact archive. 

        Returns
        -------
        None.

        """
        periodes = ["D","W"]
        #load tickers 
        tickers = update_flowimpact_support.load_tickers()
        
        # loops
        aggerator = None
    
        for i in range(0,len(tickers)):
            
            
            try: 
            # load flow_analyuses
                flow_analyses   = update_flowimpact_support.load_flows_analyses(tickers[i], periodes[0])
                
                # load impact_analusyses
                impa_analyses   = update_flowimpact_support.load_impact_analyses(tickers[i], periodes[0]) 
                
                # close data 
                close_data      = update_flowimpact_support.load_close_data(tickers[i], periodes[0]) 
            
            except: 
                continue
            # set aggegrator
            aggerator               = data_aggregator_flowimpact()
            aggerator.ticker        = str(tickers[i])
            aggerator.close_        = close_data
            aggerator.periode       = periodes[0]
            aggerator.impact        = impa_analyses
            aggerator.moneyflows    = flow_analyses
            
            try: 
                
                # aggegrate 
                aggerator.aggegrate()
                
            except Exception as e:
                print(e)
            
            if not aggerator.data_slides:
                continue
            
            # proces data. 
            for x in range(0,len(aggerator.data_slides)):
                
               
                
                model = aggerator.data_slides[x]
                
                try:
                    database_querys.database_querys.update_archive_flowimpact(model)
                except Exception as e:
                    print(e)
                
                
           
        
        
    
        for i in range(0,len(tickers)):
            
            
            try: 
            # load flow_analyuses
                flow_analyses   = update_flowimpact_support.load_flows_analyses(tickers[i], periodes[1])
                
                # load impact_analusyses
                impa_analyses   = update_flowimpact_support.load_impact_analyses(tickers[i], periodes[1]) 
                
                # close data 
                close_data      = update_flowimpact_support.load_close_data(tickers[i], periodes[1]) 
            
            except: 
                continue
            # set aggegrator
            aggerator               = data_aggregator_flowimpact()
            aggerator.ticker        = str(tickers[i])
            aggerator.close_        = close_data
            aggerator.periode       = periodes[1]
            aggerator.impact        = impa_analyses
            aggerator.moneyflows    = flow_analyses
            
            try: 
                # aggegrate 
                aggerator.aggegrate()
            except:
                continue
            
            # proces data. 
            for i in range(0,len(aggerator.data_slides)):
                
               
                
                model = aggerator.data_slides[i]
                
                database_querys.database_querys.update_archive_flowimpact(model)
                
                del model 
                
            del aggerator
            
        
        # load anlyses, 
        
        # load other analyses, 
        
        # cut analyses,
        
        # aggegrate analyses, 
        
        # process the analyses. 
        
        
class update_flowimpact_support(object):
    
    @staticmethod
    def load_tickers():    
        tickers = database_querys.database_querys.get_all_active_tickers()
        return tickers
    
    @staticmethod
    def load_flows_analyses(ticker : str, periode : str):
        periode : str = periode
        ticker_in : str = ticker
        analyses : str = "MONEYFLOWS"
        
        # get data
        analyses_out = stock_analyses_with_ticker.update_support_functions.get_stock_analyses_with_ticker(ticker, analyses , periode )
        return analyses_out
    
    @staticmethod
    def load_impact_analyses(ticker : str, periode : str):
        periode : str = periode
        ticker_in : str = ticker
        analyses : str = "LIQUIDTY"

        # get data
        analyses_out = stock_analyses_with_ticker.update_support_functions.get_stock_analyses_with_ticker(ticker, analyses , periode )
            
        return analyses_out

    @staticmethod
    def load_close_data(ticker : str, periode : str): 
        """
        Returns stock close data.

        Parameters
        ----------
        ticker : str
            DESCRIPTION.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        
        if periode == "D":  
            
            power_object = stock_object.power_stock_object(stock_ticker = ticker, simplyfied_load = True, periode_weekly = False)
        
        elif periode == "W": 
            
            power_object = stock_object.power_stock_object(stock_ticker = ticker, simplyfied_load = True, periode_weekly = True)
             
        return power_object.stock_data.Close
        
class data_aggregator_flowimpact:
    """
    
    Class takes the data, aggegrates the data. 
    
    Mentions: In the tail_data function there is space to tail the data, periode should be used to set the amount of data.
    
    """ 
    # datafields
    moneyflows  = None
    impact      = None 
    combined_   = None
    close_      = None
    ticker      = None
    periode     = None
    tail_amount_daily  = None # see mentions
    tail_amount_weekly = None # see mentions
    
    # packed data
    data_slides = []
    
    # tails data to speed op proces. 
    tail_all_data = True
   
    
    def __init__(self): 
        self.data_slides = [] 
    
    def aggegrate(self):
        
        # proces data
        self.process_data()
            
        # aggegrate data. 
        for i in range(0,len(self.moneyflows.Data)):
            
            # Creates data point
            # set moneyflow
            moneyflows_data_point   = self.moneyflows.Data[i]
            # set inpact
            impact_data_point       = self.impact.Data[i]
            # check 
            
            if moneyflows_data_point != 0 and impact_data_point != 0:
                
                # adds id
                self.add_id_to_data_slides(i)
        

    def add_id_to_data_slides(self, i : int): 
        """
        

        Parameters
        ----------
        field : int
            DESCRIPTION.

        Returns
        -------
        None.

        """
        
        
        # set moneyflow
        moneyflows_data_point   = self.moneyflows.Data[i]
        
        # set inpact
        impact_data_point       = self.impact.Data[i]
        
        # set score 
        score = (moneyflows_data_point + impact_data_point) / 2
        
        #
        # set close
        close                   = round(self.close_[i],2)
        
        # 
        date                    = self.close_.index[i]
        
        # 
        day = date.day
        
        # 
        month = date.month
        
        # 
        year = date.year
        
        # 
        weeknr = date.weekofyear 
        
        # creating the model
        model = flowimpact_model()
        
        # filling in the model.
        model.Liquididy = int(impact_data_point)
        model.Moneyflow = int(moneyflows_data_point)
        model.close     = close
        model.Score     = score
        model.date      = day
        model.weeknr    = weeknr
        model.month     = month
        model.year      = year
        model.periode   = self.periode
        model.ticker    = self.ticker
        
        self.data_slides.append(model)
        
        
    
    def process_data(self):
        """
        Processes data.

        Returns
        -------
        None.

        """
        
        # tail data for timesaving .
        if self.tail_all_data:
            self.tail_data()
        else: 
            # equilize 
            self.equalize_data()
        
    def aggegrate_data(self): 
        pass 
    
    def equalize_data(self):
        """
        Equalize stocks, moneyflow has one more.

        Returns
        -------
        None.

        """
        self.impact = self.impact["indicator_timeserie_profile"]
        self.moneyflows = self.moneyflows["indicator_timeserie_profile"].tail(len(self.impact))
        self.close_ = self.close_.tail(len(self.impact))
        
        if len(self.moneyflows) != len(self.impact):
            raise Exception("ERROR")
        
        
        
    def tail_data(self):
        """
        Tails data in smaller peaces

        Returns
        -------
        None.

        """
        self.moneyflows = self.moneyflows["indicator_timeserie_profile"].tail(250)
        self.impact = self.impact["indicator_timeserie_profile"].tail(250)
        self.close_ = self.close_.tail(len(self.impact))
        
        if 0 == 0: 
            pass

class flowimpact_model():
    
    ticker  = None
    year    = None 
    month   = None 
    date    = None
    weeknr  = None
    periode = None
    Moneyflow = None
    Liquididy = None
    Score       = None
    close       = None 
    

class data_aggegrate_backtest_trades:
    
    ticker_name : str = None
    periode     : str = None 
        
    data_slides = []
    
    def __init__(self):
        self.data_slides = []
    
    def aggegrate(self, backtest_data):
        
        data = backtest_data
        
        """
        """
        # loop true data slide.
        for x in range(0,len(data)):
            
            model = trade_performance_model()
            
            # slide data.
            slide_data = data.iloc[x]
            
            
            date = slide_data['index']
            date = datetime.datetime.strptime(date,"%d-%m-%Y")
            
            # extrating date c 
            day = date.day
            
            # 
            month = date.month
            
            # 
            year = date.year
            
            # 
            weeknr = datetime.date(year, month, day).isocalendar()[1]
                
            # 
            ticker = data.iloc[x].ticker
            side = data.iloc[x].side
            itterations = data.iloc[x].itterations
            returns = slide_data['return']
            max_return = data.iloc[x].max_return
            standard_devation = data.iloc[x].standard_devation
            yield_1w = data.iloc[x].yield_1w
            yield_1m = data.iloc[x].yield_1m
            yield_1q = data.iloc[x].yield_1q
            
            # 
            model.ticker = ticker
            model.side = side 
            model.itterations = itterations
            model.returns = returns
            model.max_return = max_return
            model.standard_devation = standard_devation
            model.yield_1w = yield_1w
            model.yield_1m = yield_1m
            model.yield_1q = yield_1q
            model.date = day
            model.year = year 
            model.month = month
            model.weeknr = weeknr
            
            self.data_slides.append(model)
            
             
        
class trade_performance_model():
    """
    Zit grote fout in, moet namelijk long and short yield in één data slide stoppen. Dus dit is niet goed. 
    
    Het is makkelijker om in de service layer columen te schrappen in de return dan iets anders. 
    
    """
    ticker  = None
    year    = None 
    month   = None 
    date    = None
    weeknr  = None
    periode = None
    itterations = None # deze mag weg
    trade_return = None # deze moet long en short zijn. 
    max_return       = None # deze moet long en short zijn. 
    standard_devation       = None # deze moet long en short zijn 
    yield_1w = None # deze moet long en short zijn. 
    yield_1m = None # deze moet long en short zijn. 
    yield_1q = None # deze moet long en short zijn. 
    
# -*- coding: utf-8 -*-
"""
Created on Sun May 15 17:28:48 2022

@author: Gebruiker
09-06
- added validation pictures. 
- added random add pictures to validation.

"""


class generate_backtest_trades(object):
    
    @staticmethod
    def generate_backtest_trades(ticker_in : str = "", periode_weekly : bool = True, tail_amount = 0):
        """
        Generates all trading pictures. 

        Raises
        ------
        Exception
            DESCRIPTION.

        Returns
        -------
        None.

        """
        # loads stockdata
        power_object = stock_object.power_stock_object( stock_ticker= ticker_in, simplyfied_load=True, periode_weekly=periode_weekly )
        
        # sets stockdata in var
        stockdata = power_object.stock_data
        
        if tail_amount!=0:
            stockdata = stockdata.tail(tail_amount + 200) # 200 is added because this data is needed in the to estimate standard deviation.
        # check if the trades can be generated
        try:
            
            # creates frame to work with.
            df_trades = trade_backtest.return_frame_trades(stock_ticker= ticker_in, data = stockdata,tail_amount = tail_amount)
            
        except Exception as e:
        
            raise e
           
        # set total amount 
        return df_trades
            
   
class trade_backtest(object):
    
    @staticmethod
    def return_frame_trades(stock_ticker , data, side : int = 1, tail_amount = 0, inserted_periode = "W"):
        """
        Return frame of backtestd trades and different yields
        
        if int 404 is thrown, that was the last data point 

        Parameters
        ----------
        stock_ticker : TYPE
            DESCRIPTION.
        data : TYPE
            DESCRIPTION.
        side : int, optional
            DESCRIPTION. The default is 1.
        tail_amount : TYPE, optional
            DESCRIPTION. The default is 0.

        Returns
        -------
        df : TYPE
            DESCRIPTION.

        """
        
        # if tail amount == zero, test will be fine on full data. 
        if tail_amount == 0:
            df = data 
            
            trades_df = []
            
            for i in range(1,len(df)):
                
                work_data = df[i:len(df)]
                
                past_data = df[0:i]
                
                detail_long = trade_backtest.return_stats_trade(stock_ticker,work_data,past_data,1)
                detail_short = trade_backtest.return_stats_trade(stock_ticker,work_data,past_data,-1)
                
                if detail_long == 404 or detail_short == 404:
                    break 
                
                trades_df.append(detail_long)
                trades_df.append(detail_short)
            
            df = pd.DataFrame(trades_df)
            
            return df
        
        # if we need to slice in the dose (sample size, the data needs to be cut)
        
        else:
            
            
            
            df = data 
            
            trades_df = []
            
            if (len(df) - tail_amount) < 30: 
                return 
            
            for i in range(tail_amount,len(df)):
                
                work_data = df[i-1:len(df)]
                
                past_data = df[0:i]
                
                detail_long = trade_backtest.return_stats_trade(stock_ticker,work_data,past_data,1,inserted_periode)
                detail_short = trade_backtest.return_stats_trade(stock_ticker,work_data,past_data,-1,inserted_periode)
                
                if detail_long == 404 or detail_short == 404:
                    break 
                
                trades_df.append(detail_long)
                trades_df.append(detail_short)
            
            df = pd.DataFrame(trades_df)
            
            return df
            
            
            
    @staticmethod
    def return_stats_trade(stock_ticker,work_data, past_data, side : int = 1 , periode : str = "W"):       
        
        # return preset yield
        yield_1w = trade_backtest.return_preset_yield(work_data, 1, periode, side)
        yield_1m = trade_backtest.return_preset_yield(work_data, 4, periode, side)
        yield_1q = trade_backtest.return_preset_yield(work_data, 12, periode, side) 
        
        if yield_1q == 404 and type(yield_1q) == int:
            return 404
            
        std = trade_backtest.return_std(past_data, tail_amount=200, percentage=False)
        
        stoploss = (2 * std) 
        
        price_open = work_data.iloc[0].Open
        
        start_price =  work_data.iloc[0].Open
        
        end_price = work_data.iloc[0].Open
        
        difference = 0
        
        itteration = 0
        
        last_price = 0 
        
        highest_price = 0 
        
        alt_stoploss = 0 
        
        for i in range(1,len(work_data)):
            
            itteration += 1
            
            if end_price == 0: 
                
                end_price = work_data.iloc[i].Open
                
            # set stoploss price.
            if side == 1: 
                
                last_price = work_data.iloc[i].Low
                
            else:
                
                last_price = work_data.iloc[i].High
             
            
            if side == 1: 
                
                difference = ( last_price - price_open ) 
            else:
                
                difference = ( price_open - last_price ) 
                
            if side == 1:
                
                if last_price > highest_price:
                    
                    highest_price = last_price
                
                if highest_price == 0:
                    
                    highest_price = last_price
            else:
                
                if last_price < highest_price:
                    
                    highest_price = last_price
                
                if highest_price == 0:
                    
                    highest_price = last_price

            # check if stoploss is hit, else reset open_price
            if side == 1:
                
                if difference < (stoploss*-1):
                    
                    end_price = work_data.iloc[i].Open
                    
                    break
                

            else:
                
                if difference > stoploss:
                    
                    end_price = work_data.iloc[i].Open
                    
                    break
                
            # close take profit 
            if side == 1: 
                
                if (highest_price - last_price) >= stoploss:
                    end_price = work_data.iloc[i].Open
                    
                    break
            else:
                
                if (last_price - highest_price ) >= stoploss:
                    end_price = work_data.iloc[i].Open
                    
                    break
            
            if side == 1: 
                
                alt_stoploss = highest_price - stoploss
                
            else:
                
                alt_stoploss = highest_price + stoploss
            
        # sorting details. 
        if side == 1: 
            returns = (((last_price - start_price)/start_price) * 100)
        else:
            returns = ((( start_price - last_price )/start_price) * 100)
        
        #max return 
        # sorting details. 
        if side == 1: 
            max_returns = (((highest_price - start_price)/start_price) * 100)
        else:
            max_returns = ((( start_price - highest_price )/start_price) * 100)
        
        
        
        
        details = {}
        details["index"]                = work_data.index[0].strftime('%d-%m-%Y')
        details["ticker"]               = stock_ticker
        details["side"]                 = side
        details["itterations"]          = itteration
        details["return"]               = round(returns,2)
        details["max_return"]           = round(max_returns,2)
        details["standard_devation"]    = round(std/start_price,2)
        details["yield_1w"]             = yield_1w
        details["yield_1m"]             = yield_1m
        details["yield_1q"]             = yield_1q
        

        return details
           
    
    @staticmethod
    def return_std(df, tail_amount : int = 30, percentage : bool = False):
        """
        Returns standard devation of dataframe. 
        
        Contracts the High and the low, is posible to return as percentage if bool is turned on. 
        if tailamount is higher than 0 it wil be tailed. 

        Parameters
        ----------
        df : TYPE
            DESCRIPTION.
        tail_amount : int, optional
            DESCRIPTION. The default is 0.
        percentage : bool, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        # if tail set tail. 
        if tail_amount != 0: 
            if len(df) > tail_amount:
                # set dataframe.
                df = df.tail(tail_amount)
            
        # sets var with list of vars
        p = df.Low.to_list()
        
        # sets var with list of vars
        o = df.High.to_list()
    
        # sets array
        i = np.array([o,p])
        
        # sets std. 
        y = np.std(i)
        
        # as percentage 
        if percentage: 
            
            x  = df.tail(1)
            perc_tot = y / x.Close[0]
            
            if perc_tot < 2:
                return 2 
            return perc_tot
            
        return y 
    
    @staticmethod
    def return_preset_yield(work_data, weeks_return : int, periode : str, side : int):
        """
        
        This indicator is set to return the preset yield, based on periode the return will be set. 
        
        
        Parameters
        ----------
        work_data : TYPE
            DESCRIPTION.
        head_amount : int
            DESCRIPTION.
        periode : str
            DESCRIPTION.

        Returns
        -------
        None.

        """
        # set amount of days
        if periode == "W":
            amount_return = weeks_return
        elif periode == "D":
            amount_return = (weeks_return *5)
        
        else:
            return 0 
        
        if amount_return > len(work_data):
            
            return 404
        try: 
            # get start and end price
            start   = float(work_data.iloc[1].Open)
            end     = float(work_data.iloc[1*amount_return].Close)  
                
            change  = float(round((((end - start)/start) * 100),2))
            
            # return correct side. 
            if side == 1:
                return change
            else:
                change = change *-1
                return change 
        except:
            return 404
  
    
if __name__ == "__main__":    
    
    try:
        
        print("Starting up ...")
        update_flowimpact_archive.update_flow_impact_archive()
        update_performance_indicators_archive.update_backtest_trades_archive()
        
        print("Finnished")
        
        """
        print("test")

        #generate_trade_pictures.generate_all_trade_pictures()
        #### end 
        generator = generate_backtest_trades()
        global data
        data = generator.generate_backtest_trades(ticker_in="NLY", periode_weekly=True, tail_amount=250)
        
        aggegrator = data_aggegrate_backtest_trades()
        
        aggegrator.aggegrate(data)
        
        
        
        print("START")
        update_flowimpact_archive.update_flow_impact_archive()
        
        model = flowimpact_model()
        
        model.Liquididy = 1
        model.Moneyflow = 1
        model.close     = 12
        model.Score     = 1
        model.date      = 1
        model.weeknr    = 51
        model.month     = 2
        model.year      = 2000
        model.periode   = "D"
        model.ticker    = "LEO"
        
        database_querys.database_querys.update_archive_flowimpact(model)
        """
        print("END")
        
    except Exception as e:
        
        raise Exception("Error with tickers", e)
    
    