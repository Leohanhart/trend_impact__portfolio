# -*- coding: utf-8 -*-
"""
Created on Sat Apr 10 13:03:53 2021

@author: Gebruiker
"""

import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib import pyplot
import ta 
import os
import time
import pickle
import pandas_datareader as web
from datetime import datetime, timedelta
import pathlib
from datetime import date

class download_stock:
    
    """ 
    this class is used to download stocks. And Prepair them with frame. 
    """
    
    SystemAllowdToRun = True
    DownloadYahoo = True
    Stock_Data = ""

    def __init__(self, Stock_Ticker = "" ): 
        
        if type(Stock_Ticker) == str and Stock_Ticker == "":
             return 0
         
        self.Stock_Ticker = Stock_Ticker

         
    def dowloadStock(self):
        """
        Downloads stock object. Check Which source is allowd and then Adds. 

        Returns
        -------
        None.

        """
        
        # check if system is allowd to run
        if self.SystemAllowdToRun:
            
            # check if yahoo is the source of download
            if self.DownloadYahoo:
                
                try:
                #downloads the stock
                    self.__DowloadStockYahoo()
                    self.AddReturns()
                    
                    
                
                finally:
                    return 
                
            # check if financial prep is the source               
            elif self.DownloadFinPrep:
             
                self.DownloadFinPrep() 
             
        if len(self.Stock_Data) == 0: 
            self.SystemAllowdToRun = False
                
    def __DowloadStockYahoo(self):
        """
        Downlaods Data from Yahoo

        Returns
        -------
        None.

        """
        
        try: 
            self.Stock_Data = yf.download(self.Stock_Ticker) 
        except Exception as e:
            raise "Problem with downloading Yahoo"
        
        
        return self.Stock_Data
        
    def __DownloadFinancialPrep(self):
        """
        Downlaods Data from financial prep.

        Returns
        -------
        None.

        """
        
        self.Stock_Data = yf.download(self.Stock_Ticker)
        
    def __ReturnsReturns(self):
        """ 
        
        Returns monthly returns. Id is int month = jan is 1, mar = 2 ect.
        
        """
        
        Returns = []
            
        BoolInMonth = False
        
        for i in range(0,len(self.Stock_Data)):
           
            
            
            # Gets date
            date = self.Stock_Data.index[i]
            
            Open = float(self.Stock_Data["Open"][i])
     
            Close = float(self.Stock_Data["Close"][i])
                    
            if Open == 0 or Close == 0:
                
                Change = 0
                
            else:
                
                Change = float(round(((Close-Open)/Open)*100,2))
                    
            #print("End of the month", str(Change) )
           
            Returns.append(Change)
        
        df = pd.DataFrame(Returns)#,index=Returns[:,0])
        
        return df



    def AddReturns(self):
        """
        Add returns to the stock
        

        Returns
        -------
        None.

        """        
        if self.SystemAllowdToRun:
                
            x = pd.DataFrame( self.__ReturnsReturns()    )
            x.rename(columns = {list(x)[0]:'Change'}, inplace=True)
            data = self.Stock_Data
            #print(x)
            self.Stock_Data = pd.concat([self.Stock_Data.reset_index(), x], axis=1, ignore_index = False)
            self.Stock_Data.index = pd.to_datetime(data.index)
 # hierboven staat ergenens een fout. 


global Stock_Object 
Stock_Object = download_stock("AAPL")



class check_data_experiation:
    
    Stock_Data = ""
    
    
    def __init__(self, StockData = "" ): 
        """
        Needs to get a stockobject input. 

        Parameters
        ----------
        StockData : TYPE, optional
            DESCRIPTION. The default is "".

        Returns
        -------
        int
            DESCRIPTION.

        """
        
        if type(StockData) == str and StockData == "":
             return 0
         
        self.Stock_Data = StockData
         
    
    def __get_last_date_dataset(self):
        """
        This function is used to see what the last date of the data set is and used to 
        check if the data needs to be refreshed. Its part of the bool_Data_Expired. 

        Returns
        -------
        DateString : TYPE
            DESCRIPTION.

        """
        print("KANKER  rr51")
        Dates    =   self.Stock_Data.index
        
        if isinstance(Dates, pd.core.indexes.datetimes.DatetimeIndex) == False:
            return 0 
            
        
       # return Dates
        
        LastDate = Dates[len(Dates)-1]
        print("BINGO", LastDate)
        LastDate = LastDate.date()
        
        
        return LastDate
       
        year = LastDate.strftime("%Y")       
        month = LastDate.strftime("%m")
        day = LastDate.strftime("%d")
            
        DateString = year + "-" + month + "-" + day      
        
        return DateString
    
    def __get_day_last_data(self):
        """
        Returns the last day of the week type int. starting with 0 ("monday") and ending with 6(Sunday) 
        This is used for the boll data expired. 
        Returns
        -------
        Day : TYPE
            DESCRIPTION.

        """
        Dates    =   self.Stock_Data.index
        LastDate = Dates[len(Dates)-1]
        
        Day = LastDate.weekday()
        
        return Day
    
    def __Return_Day_of_the_week(self, AmountOfDays = 0):
        """
        This is the function that returns the int of the day. 

        Parameters
        ----------
        AmountOfDays : TYPE, optional
            DESCRIPTION. The default is 0.

        Returns
        -------
        DayOfTheWeek : TYPE
            DESCRIPTION.

        """
        
        now = datetime.now() # current date and time
        
        today = datetime.now()    
        n_days_ago = today - timedelta(days=AmountOfDays)
        
        now = n_days_ago
        
        # 0 is monday, 6 is sunday. So weekend is 5 and 6 
        DayOfTheWeek = int(now.weekday())
        
        return DayOfTheWeek    
    
    def Earlyer_then_Friyday(self):
        
        Dates    =   self.Stock_Data.index
        LastDate = Dates[len(Dates)-1]
        
        day_of_the_week = self.__Return_Day_of_the_week()
        if day_of_the_week == 5:
            today = datetime.now()    
            n_days_ago = today - timedelta(days=1)
            Day = n_days_ago.date()
            if LastDate != Day:
                return True
            elif LastDate == Day:
                return False
            else:
          
            
                if day_of_the_week == 6:
                    today = datetime.now()    
                    n_days_ago = today - timedelta(days = 2)
                    Day = n_days_ago.date()
                    if LastDate != Day:
                        return True    
                    elif LastDate == Day:
                         return False
                    else:
                        return False
                    
                    
    
    def Bool_Data_Expired(self):
        
        
     
        #this function was inefficent because there was a error in saving the data without date. 
        DateOfLastDownload  = self.__get_last_date_dataset()
        
        if type(DateOfLastDownload) == int(): 
            return 0
        
        DateOfToday         = self.__Return_Date_String(0)
        
        delta = DateOfToday - DateOfLastDownload
        
        
        Weekday = DateOfToday.weekday() 
        if Weekday == 5 and delta.days >= 2:
            
            return True
        if Weekday == 6 and delta.days >= 3:
            
            return True
        if Weekday != 5 and Weekday != 6 and delta.days >= 1:
          
            return True
        

        
    def __Return_Date_String(self, AmountOfDays = 0):
        
        now = datetime.now() # current date and time
        
        today = datetime.now()    
        today = today.date()
        
        return today
        n_days_ago = today - timedelta(days=AmountOfDays)
        
        now = n_days_ago
        
        year = now.strftime("%Y")
         
        month = now.strftime("%m")
             
        day = now.strftime("%d")
        
        string = str(year+"-"+month+"-"+day)
        
        return string
    
    

class error_handling:
    """
    This class is created for handling occuring errors
    
    1. if an error occurs the error class: self.error_occurred == TRUE
    2. the error code will show up. 
    3. the helping function will be added to error_handling_function
    """
    error_code = 0
    error_message = "No error occured"
    error_handling_function = 0 
    error_occurred = False
    
    def __init__(self, Return_Type = ""): 
        
        x = Return_Type
        if isinstance(x, tuple) and x[0] == "Error":
            self.error_occurred = True
    
    def __find_error(self, error_code = 0 ):
        
        if error_code == 0: 
            self.error_code = "Error, is found, but there is not cleared form where "
            
        if error_code == 501:
            self.error_code = "Error occured in a dataframe based eqation in the liquidity class, the wrong type of format is shown"
                
    def print_error_code(self):
        print(self.error_message)
        

class data_modifications:
    
    def convert_nested_analeses_dict_data_to_list(self, data = None) -> list:  
        """
        Converts all kinds of dictonary, they need to contain "Data"

        Parameters
        ----------
        data : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        #
        # check if type is correct
        print(type(data))
        if not isinstance(data,pd.core.frame.DataFrame ):
            #
            # else raise error, wrong formate
            raise Exception('Wrong formate, no match to dict', 'convert_nested_analeses_dict_data_to_list')
        #
        # raises error of data is missing
        elif not "Data" in data.columns:
            #
            # raises the missing colums name error
            raise Exception('Data column - named "Data" is missing in dict dict', 'convert_nested_analeses_dict_data_to_list')
        #
        # else, just execute the normal convertino
        else:
            #
            # extract values 
            value_data      =   data.values
            #
            # list the values
            nested_values   =   value_data.tolist()
            #
            # de-nest the values
            unnested_values = [item for sublist in nested_values for item in sublist]
            #
            # return the values
            return unnested_values
        
            
        