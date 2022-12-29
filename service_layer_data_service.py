# -*- coding: utf-8 -*-
"""
Created on Fri May  6 17:16:04 2022

@author: Gebruiker

IMPORTANT NOTES:
    
    IF YOU EVER WANT AN OTHER TYPE OF STOCK_ANALYSES_PACKAGE, REMOVE NAME FROM 
    
"""

import database_querys_main 
import json
from core_scripts.stock_data_download import power_stock_object
import datetime
import constants
import service_layer_support
from core_utils.save_temp_data import save_and_load_temp_data
import sector_analyse
import pandas
import numpy as np

class return__analyses(object):
    
    @staticmethod
    def return_liquidity_analyses(active_filter : bool = False, 
                                  increasing: bool = False,
                                  decreasing: bool = False,
                                  min_number: int = -3,
                                  max_number: int = 3,
                                  profile_number : int = 0, 
                                  pagination_filter : bool = False,
                                  page_amount : int = 20,
                                  page_number : int = 1,
                                  ticker_name : str = None,
                                  single_stock : bool = False,
                                  daily_data : bool = False):
        """
        
        returns all liquidity analyses, tickers that have active status are added, tickers with profiles different than 0 are added

        Returns
        -------
        Json respons

        """
        
        # get the data.
        data = database_querys_main.database_querys.get_analyses_liquidity(as_pandas=True, daily=daily_data)
        
        # filter data.
        data = return__analyses__support.apply_filters_and_more(data,
                                      active_filter, 
                                      increasing,
                                      decreasing,
                                      min_number,
                                      max_number,
                                      profile_number, 
                                      pagination_filter,
                                      page_amount,
                                      page_number,
                                      ticker_name,
                                      single_stock,
                                      analyses_type = "LIQUIDITY")
                                      
 

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

    @staticmethod
    def return_moneyflow_analyses(active_filter : bool = False, 
                                  increasing: bool = False,
                                  decreasing: bool = False,
                                  min_number: int = -3,
                                  max_number: int = 3,
                                  profile_number : int = 0, 
                                  pagination_filter : bool = False,
                                  page_amount : int = 20,
                                  page_number : int = 1,
                                  ticker_name : str = None,
                                  single_stock : bool = False,
                                  daily_data : bool = False):
        """
        
        returns

        Returns
        -------
        None.
        
        # datastages : incomming formate, convert to workble data, convert to distributble data, wished output format. 
        # stage: Get the data. 
        # wanted filters : pagination, only above sertain thing, only below sertain thing. 

        # make applyble options for filters, 
        # make options dict and extract. 
        
        """
        
        # receives incomming data as dataframe. 
        data = database_querys_main.database_querys.get_analyses_moneyflows(as_pandas=True, daily = daily_data)
        
        # filter data.
        data = return__analyses__support.apply_filters_and_more(data,
                                      active_filter, 
                                      increasing,
                                      decreasing,
                                      min_number,
                                      max_number,
                                      profile_number, 
                                      pagination_filter,
                                      page_amount,
                                      page_number,
                                      ticker_name,
                                      single_stock,
                                      analyses_type = "MONEYFLOWS")
 

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
        

    
    @staticmethod
    def return_moneyflow_and_impact_analyses(active_filter : bool = False, 
                                  increasing: bool = False,
                                  decreasing: bool = False,
                                  min_number: int = -3,
                                  max_number: int = 3,
                                  profile_number : int = 0, 
                                  pagination_filter : bool = False,
                                  page_amount : int = 20,
                                  page_number : int = 1,
                                  ticker_name : str = None,
                                  single_stock : bool = False,
                                  daily_data : bool = False):
        """
        
        

        Returns
        -------
        None.

        """
        
        data = database_querys_main.database_querys.get_analyses_flows_and_impact(as_pandas=True, daily=daily_data)
        try: 
            data = return__analyses__support.apply_filters_and_more(data,
                                             active_filter, 
                                             increasing,
                                             decreasing,
                                             min_number,
                                             max_number,
                                             profile_number, 
                                             pagination_filter,
                                             page_amount,
                                             page_number,
                                             ticker_name,
                                             single_stock,
                                             analyses_type = "FLOWIMPACT")
            
        except Exception as e:
            
            data = return__analyses__support().error_handler(error_code = e,
                                                             ticker_in  = ticker_name, 
                                                             )    
            
        resp = json.dumps(data)
        
        return resp
    

    
    @staticmethod
    def return_stock_analyses(ticker_in : str, stock_analyses : str = "", periode = "W", length_time_series = "y3"):
        """
        

        Parameters
        ----------
        ticker_in : str
            DESCRIPTION.
        stock_analyses : str, optional
            DESCRIPTION. The default is "".

        Returns
        -------
        None.

        """
        
        #return__analyses__support.return_packaged_stock_analyses(ticker_name=ticker_in,)
        # returns the stock data in the right format.
        resp = service_layer_support.support_class.return_stock_analyses(ticker_in = ticker_in, stock_analyses = stock_analyses, periode=periode,lengt_timeserie=length_time_series)
        
        return resp
    
    @staticmethod
    def return_avalible_analyses_lengts():
        
        time_frames = ["q","y1","y2", "y3", "y5", "all"]
        
        resp = json.dumps(time_frames)
        
        new_resp = json.loads(resp)
        
        return new_resp
        
    @staticmethod
    def return_sector_analyses(sector_in : str = None,  
                               amout_of_years : int = 1,
                               periode = "W", 
                               package_in_json = True):
        """
        
        Loads all avalible analyeses for name.
        

        Parameters
        ----------
        ticker_in : str
            DESCRIPTION.
        stock_analyses : str, optional
            DESCRIPTION. The default is "".

        Returns
        -------
        None.

        """
        # returns full sector analyses.
        if sector_in == None: 
            
            data = return__analyses__support.return_full_sector_analyses()
            resp = json.dumps(data)
            
            return resp
        
        
        # returns single ticker
        else:
            
            # replace underscore for whitespace
            incomming_name = support__industry__and__sector.replace_white_space(sector_in)
            
            # check if sector exists
            if not support__industry__and__sector.check_if_exsists(incomming_name=incomming_name,sector=True):
                
                raise Exception("Wrong name, name does not exsits") 
            else:
                
                data = {}
                # load all analsyes and package them in. 
                
                data = support__industry__and__sector().return_all_analyses_large(string_incomming_name=incomming_name)
                
                # this turns the data into json, for test purposes this is an option
                if package_in_json: 
                    new_data = support__industry__and__sector().package_analyses_to_json(data,
                                                                                         tail_option_years = amout_of_years,
                                                                                         periode = periode)
                    
                    resp = json.dumps(new_data)
                    
                    new_resp = json.loads(resp)
                    
                    return new_resp 
                # only for test purposes
                else:
                    return data
                
                
    @staticmethod
    def return_industry_analyses(industry_in : str = None, amout_of_years : int = 1,periode = "W"):
        """ 
        

        Parameters
        ----------
        ticker_in : str
            DESCRIPTION.
        stock_analyses : str, optional
            DESCRIPTION. The default is "".

        Returns
        -------
        None.

        """
        # returns full sector analyses.
        if industry_in == None: 
            
            data = return__analyses__support.return_full_industry_analyses()
            resp = json.dumps(data)
            
            return resp
        
        # returns single ticker
        else:
            
            incomming_name = support__industry__and__sector.replace_white_space(industry_in)   
            
            if not support__industry__and__sector.check_if_exsists(incomming_name=incomming_name,industry=True):
                
                raise Exception("Wrong name, name does not exsits") 
            else:
                data = {}
                # load all analsyes and package them in. 
                
                #
                data = support__industry__and__sector().return_all_analyses_large(string_incomming_name=incomming_name)
                
                # parces data.
                new_data = support__industry__and__sector().package_analyses_to_json(data, 
                                                                                     tail_option_years = amout_of_years,
                                                                                     periode = periode)
                
                resp = json.dumps(new_data)
                
                new_resp = json.loads(resp)
                
                return new_resp 
            
class return__research__and__archives(object):
    
    
    @staticmethod
    def return_flow_impact_performance_based_archive(ticker : str = None,
                                                     periode : str = None,
                                                     overall_stats : bool = False,
                                                     style : str = "SCORE/SMART"):
        pass
        # retreives the data with ticker and periode.
        data = database_querys_main.database_querys.get_analyses_flow_impact_with_performance(ticker = ticker, periode = periode)
        
        # applys filters. 
        data = return__research__support.flow_performance_data_filter(data)
        
        # if overall stats
        if overall_stats:
            
            if style == "SMART":
                data = overall__stats.return_detailed_rapport(data, style="flow_impact_smart")
            elif style == "SCORE": 
                data = overall__stats.return_detailed_rapport(data, style="flow_impact_study")
            else:
                data = overall__stats.return_detailed_rapport(data, style="flow_impact_smart")
         
                    
        # use packager to package data.
        data = return__analyses__filters__support.package_in_right_format(data)
        
        # transforms the data for JSON.
        resp = json.dumps(data)
        
        return resp
        
        ## test
            
    
    @staticmethod
    def return_flow_impact_archive(ticker : str = None,
                                         periode : str = None,
                                         year : int = None, 
                                         month :int = None, 
                                         day : int = None, 
                                         weeknr : int = None):
        """
        

        Parameters
        ----------
        increasing : TYPE, optional
            DESCRIPTION. The default is increasing.
        decreasing : TYPE, optional
            DESCRIPTION. The default is decreasing.
        daily_data : TYPE, optional
            DESCRIPTION. The default is daily_data.

        Returns
        -------
        None.

        """
        
        #define route 1. Ticker and periodo = data. 2. is year and week nr. 3. is date with periode. 
        if type(ticker) == str and type(periode) == str:
            
            data = database_querys_main.database_querys.get_analyses_flow_impact_archive(ticker=ticker, periode=periode, as_pandas = True)
            
            data = return__research__support.clears__unsynch_profiles(data)
            
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
        
            
        if type(year) == int and type(weeknr) == int and type(periode) == str: 
            
            data = database_querys_main.database_querys.get_analyses_flow_impact_archive(ticker=ticker, periode=periode, year = year, weeknr = weeknr, as_pandas = True)
            
            data = return__research__support.clears__unsynch_profiles(data)
            
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
        
        if type(year) == int and type(month) == int and type(day) == int and type(periode) == str: 
            
            data = database_querys_main.database_querys.get_analyses_flow_impact_archive(periode = periode ,year = year, month = month , day = day, as_pandas = True)
            
            data = return__research__support.clears__unsynch_profiles(data)
            
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
            
   
    
class return__research__support(object): 
    
    @staticmethod
    def flow_performance_data_filter(data, overall_stats : bool = False):
        """
        Removes unneeded data.

        Parameters
        ----------
        data : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        # clears bad data 
        data = return__research__support.clears__unsynch_profiles(data)
        
        # resets yields to position. 
        data = return__research__support.sets__right_yields(data)
        
        # removes columns. 
        data = return__research__support.remove_unnessesary_columns(data)
        
        
        
        return data
        
        
    @staticmethod
    def remove_unnessesary_columns(data): 
        """
        Removes unnessary columms

        Parameters
        ----------
        data : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        df = data
        
        columns_to_remove = ['id_1', 'ticker_1',
               'year_1', 'month_1', 'date_1', 'weeknr_1', 'periode_1', 
               'itterations', 'returns', 'max_return']
        df = df.drop(columns_to_remove, axis=1)
        
        return df
    @staticmethod
    def clears__unsynch_profiles(data):
        """
        
        removes mismathching profiles. 

        Parameters
        ----------
        data : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        
        # set df 
        df = data
        run = True
        # loop true dataframe
        while run == True: 
            
            for i in range(0, len(df)):
                
                slide = df.iloc[i]
                
                if i == len(df)-1:
                    run = False
                
                
                # if both profiles are not positive or negative, remove. else continue
                if slide.Moneyflow < 0 and slide.Liquididy < 0:
                    continue
                elif slide.Moneyflow > 0 and slide.Liquididy > 0:
                    continue
                else:
                    df = df.drop(df.index[i])
                    break
                
            
        return df 
    
    @staticmethod
    def sets__right_yields(data):
        """
        Sets righ yield do profile

        Parameters
        ----------
        data : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        # set df 
        df = data
        
        # loop true dataframe
        for i in range(0, len(df)):
            
            slide = df.iloc[i]
            
            
            # if both profiles are not positive or negative, remove. else continue
            if slide.Score < 0: 
                slide.side = -1
                slide.yield_1w = slide.yield_1w * -1
                slide.yield_1m = slide.yield_1m * -1
                slide.yield_1q = slide.yield_1q * -1
                
                df.iloc[i] = slide 
                
            
                
        return df 

class overall__stats(object):
    
    @staticmethod
    def return_detailed_rapport(data, style="flow_impact_smart"):
        
        if style == "flow_impact_study":
             
            data = overall__stats.return_flow_impact_study_rapport(data)
            
            return data
    
        if style == "flow_impact_smart":
            
            data = overall__stats.return_simple_flow_impact_raport(data)
            
            return data
            
    @staticmethod
    def return_simple_flow_impact_raport(data):
        
        # dict for the data
        data_out = {}
        
        # returns list with details columns
        data_point = ['yield_1w', 'yield_1m', 'yield_1q']
        
        for x in data_point:
            
           work_data = data[data_point]
           data_out[str(x)] = overall__stats().return_details(data = work_data, column_name = x)
          
        
        return data_out
    @staticmethod  
    def return_flow_impact_study_rapport(data):
        
        # return all scores
        scores = list(data['Score'].values)
        
        # retreives list of all scores
        list_all_scores = overall__stats__support().return_unique_numbers_list(scores)
        
        # dict for the data
        data_out = {}
        
        # returns list with details columns
        data_point = ['yield_1w', 'yield_1m', 'yield_1q']
        
        # retreives details 
        for i in list_all_scores:
            
           work_data = data[data.Score == i]
           data_out[i] = {}
           for x in data_point:
               
              
               data_out[i][str(x)] = overall__stats().return_details(data = work_data, column_name = x)
         
        print(data_out)
        overall_data_out = {}
        
        overall_data_out["Scores"] = data_out
        
        
        
    @staticmethod
    def return_details(data, column_name : str = ""):      
        """
        

        Parameters
        ----------
        data : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        # check is name is oke, else raise error
        if column_name not in data.columns:
            raise Exception("Column name not found")
        
        # extract data. 
        data = data[column_name]
        
        # sets realdata
        x = real_data = data.values
        
        # select stats
        average = overall__stats__support.return_average(x)
        prercentage_positive = overall__stats__support().return_amount_positive(x)
        
        out_data = {}
        out_data["average"] = average
        out_data["prercentage_positive"] = prercentage_positive
        
        return out_data
        

class overall__stats__support(object):
    
    @staticmethod
    def return_average(data):
        """
        Returns average of data

        Parameters
        ----------
        data : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        # sets data
        x = data 
        
        # returns average
        average = x.mean()
        return average
    
    @staticmethod
    def return_amount_positive(data):
        """
        

        Parameters
        ----------
        data : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        
        pos_count, neg_count = 0, 0
        total = len(data) 
        # iterating each number in list
        for num in data:
         
            # checking condition
            if num >= 0:
                pos_count += 1
         
            else:
                neg_count += 1
                
        total_perce = (pos_count / total) * 100
        
        return total_perce
    
    @staticmethod
    def return_unique_numbers_list(data):
        """
        Creates list of unique numbers. 

        Parameters
        ----------
        data : TYPE === LIST
            DESCRIPTION.

        Returns
        -------
        None.

        """
        new_list = list(np.unique(data))
        return new_list
    
    def switch_all_numbers_to_positive(data):
        """
        switches a list to all positive numbers

        Parameters
        ----------
        data : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        res =  [abs(ele) for ele in data]
        return res
        
class return__analyses__support(object):
    
    @staticmethod
    def apply_filters_and_more( data,
                                active_filter : bool = False, 
                                increasing: bool = False,
                                decreasing: bool = False,
                                min_number: int = -3,
                                max_number: int = 3,
                                profile_number : int = 0, 
                                pagination_filter : bool = False,
                                page_amount : int = 20,
                                page_number : int = 1,
                                ticker_name : str = None,
                                single_stock_analyses : bool = False,
                                analyses_type : str = None,):
        """
        What you see in this function is that Analyses is retreived if no ticker is assigned, if so 
        this will turn in other modus. 

        Parameters
        ----------
        data : TYPE
            DESCRIPTION.
        active_filter : bool, optional
            DESCRIPTION. The default is False.
        increasing : bool, optional
            DESCRIPTION. The default is False.
        decreasing : bool, optional
            DESCRIPTION. The default is False.
        min_number : int, optional
            DESCRIPTION. The default is -3.
        max_number : int, optional
            DESCRIPTION. The default is 3.
        profile_number : int, optional
            DESCRIPTION. The default is 0.
        pagination_filter : bool, optional
            DESCRIPTION. The default is False.
        page_amount : int, optional
            DESCRIPTION. The default is 20.
        page_number : int, optional
            DESCRIPTION. The default is 1.
        ticker_name : str, optional
            DESCRIPTION. The default is None.
        analyses_type : str, optional
            DESCRIPTION. The default is None.

        Returns
        -------
        data : TYPE
            DESCRIPTION.

        """
        
        
        # if needed, returns stock with all the data instead. 
        if single_stock_analyses:
            if not ticker_name == None:
                
                
                # retreives the data. 
                data  =  return__analyses__support.return_packaged_stock_analyses(data, 
                                                                                  ticker_name, 
                                                                                  analyses_type)
                
                # packages the data
                data  =  return__analyses__filters__support().package_in_right_format(data)
                
                return data
                
      
        # if filter is active, apply filter conditions to dataframe.
        if active_filter:
        
        
           # adding filters to dataframe 
           data = return__analyses__filters.apply_analyses_filters(data,
                                                             increasing,
                                                             decreasing,
                                                             max_number,
                                                             min_number,
                                                             profile_number,  
                                                             ticker_name
                                                             )
        # adds pagination filter
        if pagination_filter:
            
           # assigns data with pagination data.
           data = return__analyses__filters.apply_pagination(data,
                                                       page_amount,
                                                       page_number
                                                       )
        
        data = return__analyses__filters__support().package_in_right_format(data)
        
        return data
    
    def return_packaged_stock_analyses(data, ticker_name: str = None, type_of_analyses = "FLOWIMPACT"):
        """
        
        Packages all the data for you and your api!!

        Parameters
        ----------
        data : TYPE
            DESCRIPTION.
        ticker_name : str, optional
            DESCRIPTION. The default is None.
        type_of_analyses : TYPE, optional
            DESCRIPTION. The default is "FLOWIMPACT".

        Returns
        -------
        total_package : TYPE
            DESCRIPTION.

        """
        
        ticker = ticker_name
        ticker = None
        
        if type_of_analyses == "FLOWIMPACT":
            
            total_package = {}
            
            # returns the flowimpact profiles. 
            data = return__analyses__filters.apply_analyses_filters(data = data, ticker_name = ticker)
            
            data = data.to_dict()
            
            if 0 == 0:
                pass
            # adds the package in main dict. ### profiles are going to be over writen...
            total_package['id'] = data['id']
            total_package['flowimpact_analyses'] = data
    
            #### here can be more analyses added.        
            analyses_list = ["moneyflow_data", "liquidity_data"]
            
            if 0==0:
                pass 
            # adds the analsyses.
            for analyses_name in analyses_list:
                
                # gets the analyses data.
                resp = service_layer_support.support_class.return_stock_analyses(ticker_in = ticker, 
                                                                                 stock_analyses = analyses_name,
                                                                                 return_as_json = False)
                # total
                total_package[analyses_name] = resp
            
            # analyses. 
            if 0==0:
                pass 
            
            return total_package
        
        if type_of_analyses == "MONEYFLOWS":
            
            total_package = {}
            
            # returns the flowimpact profiles. 
            data = return__analyses__filters.apply_analyses_filters(data = data, ticker_name = ticker)
            
            data = data.to_dict()
            
            if 0 == 0:
                pass
            # adds the package in main dict. ### profiles are going to be over writen...
            total_package['id'] = data['id']
            total_package['flowimpact_analyses'] = data
    
            #### here can be more analyses added.        
            analyses_list = ["moneyflow_data"]
            
            # adds the analsyses.
            for analyses_name in analyses_list:
                
                # gets the analyses data.
                resp = service_layer_support.support_class.return_stock_analyses(ticker_in = ticker, 
                                                                                 stock_analyses = analyses_name,
                                                                                 return_as_json = False)
                # total
                total_package[analyses_name] = resp
            
            # analyses. 
            if 0==0:
                pass 
            
            return total_package
        
        if type_of_analyses == "LIQUIDITY":
            
            total_package = {}
            
            # returns the flowimpact profiles. 
            data = return__analyses__filters.apply_analyses_filters(data = data, ticker_name = ticker_name)
            
            data = data.to_dict()
            
            if 0 == 0:
                pass
            # adds the package in main dict. ### profiles are going to be over writen...
            total_package['id'] = data['id']
            total_package['flowimpact_analyses'] = data
    
            #### here can be more analyses added.        
            analyses_list = ["liquidity_data"]
            
            # adds the analsyses.
            for analyses_name in analyses_list:
                
                # gets the analyses data.
                resp = service_layer_support.support_class.return_stock_analyses(ticker_in = ticker_name, 
                                                                                 stock_analyses = analyses_name,
                                                                                 return_as_json = False)
                # total
                total_package[analyses_name] = resp
            
            # analyses. 
            if 0==0:
                pass 
            
            return total_package

        
    @staticmethod           
    def error_handler(error_code = None, ticker_in = None): 
        
        print(error_code)
        return_data = {}
        if str(error_code) == "Ticker_is_not_avalible":
            
            return_data['ERROR'] = "ERROR, analyeses ticker:"+str(ticker_in) + " is not avalible"
        
        else:
            
            return_data['ERROR'] = "ERROR, something went wrong. CALL LEO FAST. +31620859007"
            
        return return_data
    
    
    @staticmethod           
    def return_full_sector_analyses():
        """
        
        Returns full dataframe of analyses. 

        Returns
        -------
        None.

        """
        data = database_querys_main.database_querys.get_analyses_sector(as_pandas = True)
        
        return data
    @staticmethod           
    def return_full_industry_analyses():
        """
        
        Returns full dataframe of analyses. 

        Returns
        -------
        None.

        """
        # get query with pandas. 
        # there will be database table that cointains all the data.
        pass
    
    @staticmethod           
    def return_sector_analyses(sector_analyses : str = None):
        """
        
        Returns full dataframe of analyses. 

        Returns
        -------
        None.

        """
        # get query with pandas. 
        
        # remove _ replace wit white space.
        pass
        
    @staticmethod           
    def return_full_industry_analyses(industry_analyses : str = None):
        """
        
        Returns full dataframe of analyses. 

        Returns
        -------
        None.

        """
        data = database_querys_main.database_querys.get_analyses_industry(as_pandas = False)

        return data
        
class support__industry__and__sector(object):
    

    @staticmethod           
    def replace_white_space(incomming_string : str = None):         
        """
        removes white space for sectors or industry's.

        Parameters
        ----------
        error_code : TYPE, optional
            DESCRIPTION. The default is None.
        ticker_in : TYPE, optional
            DESCRIPTION. The default is None.

        Returns
        -------
        None.

        """
        
        outgoing_string = incomming_string.replace("_"," ")
        
        return outgoing_string
    
    @staticmethod  
    def check_if_exsists(incomming_name : str = None ,sector : bool = False, industry:bool = False): 
        
        if sector:
            sectors = database_querys_main.database_querys.get_all_active_sectors()
            if incomming_name in sectors:
                return True
            else:
                return False
            
        if industry:
            industrys = database_querys_main.database_querys.get_all_active_industrys()
            if incomming_name in industrys:
                return True
            else:
                return False

    @staticmethod
    def return_all_analyses_large(string_incomming_name : str = None):
        """
        Returns moneyflow analyses

        Parameters
        ----------
        string_incomming_name : str, optional
            DESCRIPTION. The default is None.

        Returns
        -------
        None.

        """
        
        # set subitmes analyses.
        sub_analyses_atributes = ["indicator_timeserie_raw","indicator_timeserie_profile"]
        # sets industy
        sector_and_industy_analyesses = sector_analyse.sector_analyse()
        # sets analyses from main to var
        analyses = sector_and_industy_analyesses.analyeses
        
        data_out = {}
        
        slide = {}
        
        if 0 == 0:
            pass 
        
    
        # recieves the data.
        for analyse in analyses:
            
            # sets empty list
            slide = {}
            
            # loops true 
            for sub_analyses_ in sub_analyses_atributes:
                
                if 0 == 0:
                    pass 
                
                
                #### do this for all analyses, add them, possibly in loop.
                name_placeholder = str(string_incomming_name) + "." + analyse + "." + sub_analyses_
                
                # try or die
                try: 
                    
                    data = save_and_load_temp_data.save_and_load_temp_data_class.load_data(name_placeholder, "LARGE_ANALYSES")
                
                except:
                    
                    slide[sub_analyses_] = 0
                    
                    continue
                    
                slide[sub_analyses_] = data
            
            # 
            data_out[analyse] = slide
            
        return data_out

    @staticmethod
    def package_analyses_to_json(data, tail_option_years : int = 0, periode = "W"):
        """
        

        Parameters
        ----------
        data : TYPE
            DESCRIPTION.
        tail_option_years : int, optional
            DESCRIPTION. The default is 0.
        periode : TYPE, optional
            DESCRIPTION. The default is "W".

        Returns
        -------
        data : TYPE
            DESCRIPTION.

        """

        #two layers.
        for key_one in data.keys():
            
            for key_two in data[key_one].keys():
                
                df = data[key_one][key_two]
                
                # if problem with worng kind of pandas. Convert.
                if isinstance(df, pandas.core.series.Series):
                    df = df.to_frame()
                    
                new_data = support__industry__and__sector().set_index_to_column(df)
                
                # if tailing is wanted, tail. 
                if tail_option_years != 0:
                    
                    if periode == "W":
                        
                        amount_tail = tail_option_years * 51
                        
                    elif periode == "D":
                        
                        amount_tail = tail_option_years * 251
                        
                    new_data = new_data.tail(amount_tail)
                
                data[key_one][key_two] = new_data.to_json(orient="records")
                
                data[key_one][key_two] = json.loads(data[key_one][key_two])
                
                
        return data
                
                
    @staticmethod
    def set_index_to_column(data):
        
        df = data
        
        df["Dates"] = df.index.astype(str).values
        
        columns_titles = ["Dates","Data"]
        
        df_reorder=df.reindex(columns=columns_titles)
        
        df_reorder=df.reindex(columns=columns_titles)
                
        return df_reorder
class return__data(object):
    
    @staticmethod
    def return_stock_data_time_serie(ticker_in : str, time_frame : str = "", periode : str = "", tickers_only : bool = False):
        """
        
        
        returns stock data


        Parameters
        ----------
        ticker_in : str
            DESCRIPTION.

        Returns
        -------
        resp : TYPE
            DESCRIPTION.
            OHLC data of stock ticker.
            
        """
        # returns the stock data in the right format.
        resp = service_layer_support.support_class.return_data_right_format(ticker_in, time_frame, periode, tickers_only= tickers_only)
        
        return resp
    
    @staticmethod
    def return_all_sectors():
        
        data = database_querys_main.database_querys.get_all_active_sectors()
        
        resp = json.dumps(data, ensure_ascii=False,separators=(',', ':'))
        
        return resp

    
    @staticmethod
    def return_all_industrys():
        
        data = database_querys_main.database_querys.get_all_active_industrys()
        
        resp = json.dumps(data,ensure_ascii=False,separators=(',', ':'))
        
        return resp
    
    
    @staticmethod
    def return_last_daily_update():
        
        data = save_and_load_temp_data.save_and_load_temp_data_class.load_data("LAST_DAILY_UPDATE", "system_info")
        
        resp = json.dumps(data,ensure_ascii=False,separators=(',', ':'))
        
        return resp
    
      
class return__analyses__filters(object):
    
    @staticmethod
    def apply_analyses_filters(   data ,
                                  increasing: bool = False, 
                                  decreasing: bool = False,
                                  max_number: int = None,
                                  min_number: int = None, 
                                  profile_number : int = None, 
                                  ticker_name : str = None ):
        """
        
        ADDS filters to datatframe of retreived analysses. Works for all analyses universal. if include profile_

        Parameters
        ----------
        data : TYPE
            DESCRIPTION.
        increasing : bool, optional
            DESCRIPTION. The default is False.
        decreasing : bool, optional
            DESCRIPTION. The default is False.
        max_number : int, optional
            DESCRIPTION. The default is None.
        min_number : int, optional
            DESCRIPTION. The default is None.
        profile_number : int, optional
            DESCRIPTION. The default is None.
        ticker_name : str, optional
            DESCRIPTION. The default is None.

        Raises
        ------
        Exception
            DESCRIPTION.

        Returns
        -------
        data : TYPE
            DESCRIPTION.

        """

        # resets index.
        try:
            
            data = return__analyses__filters__support.set_index_with_id(data)
                
        except Exception as e:
            
            raise Exception("Unable_to_apply_filter",e)
        
        # if ticker is filled in, only the data of the filter will be retured. 
        if not ticker_name == None and type(ticker_name) != bool:

            if not ticker_name.upper() in data.id:
                #### implement error. 
                raise Exception("Ticker_is_not_avalible")
                
            else:    
                
                data = data.loc[ticker_name]
                
                return data
        
        # returns columnnames. that contain profile -- so this filter gets universal for all analyses.
        column_names = return__analyses__filters__support.return_columns_matching(data,'profile_')
        
        # sorts complete list. This works universal. 
        data = data.sort_values(column_names,  ascending=False)
        
        # changes decreasing/increasing values. 
        if not increasing or not decreasing:
            
            if decreasing:
                
                data = data.sort_values(column_names,  ascending=True)
                
            else:
                
                data = data.sort_values(column_names,  ascending=False)
                
                
        
        # sorts data between given numbers.
        if max_number != None and min_number != None :
           
           # between numbers_ this should be between if statments
           data = data[data[column_names[0]].between(min_number,max_number)]
           
           if 0 == 0:
               pass
           # return here because, otherwise it can be overwritten.
           
       
        if profile_number != None and profile_number != 0 :
            
            data = data[data[column_names[0]] == profile_number]
            # returns data because this is end. 
            if 0 == 0:
                pass
        
        return data
    
    @staticmethod        
    def apply_pagination(data, page_amount : int = 20, page_number : int = 1):
        """
        Pagnation.

        Parameters
        ----------
        data : dataframe with data.
        
        pagination_filter : bool, optional
            DESCRIPTION. The default is False.
        page_amount : int, optional
            DESCRIPTION. The default is 20.
        page_number : int, optional
            DESCRIPTION. The default is 1.

        Returns
        -------
        None.
            
        

        """
        # setup to pervent idiotic pagination.
        if len(data)<page_amount:
            return data 
        # gets starting number 
        
        # define page number: 
        end___number = page_amount * page_number 
        start_number = end___number - page_amount
        data = data.iloc[start_number:end___number] 
        
        return data
    
class return__analyses__filters__support(object):
    
    @staticmethod
    def set_index_with_id(data):
        """
        
        Sets index with ID's so that filtering is possible. 

        Parameters
        ----------
        dataframe : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        try:
            
            data.index = data.id
        
        except AttributeError:
            
            raise Exception("Cant_ids_to_index_filters_will_mall_function")
            
        return data
        
    def return_columns_matching(dataframe, word):
        """
        Returns list of column names that match profile. 

        Parameters
        ----------
        dataframe : TYPE
            DESCRIPTION.
        word : TYPE
            DESCRIPTION.

        Returns
        -------
        columns_that_contain_profile : TYPE
            DESCRIPTION.

        """
        
        columns_that_contain_profile = [col for col in dataframe.columns if word in col]
        
        return columns_that_contain_profile
    
    @staticmethod 
    def package_in_right_format(data):
        # transform data to json
        try:
            
            data = data.to_dict(orient='records')
        
        # if there is type error because frame only has one slide. don't use orent.
        except TypeError:
            
                data = data.to_dict()
            
        except AttributeError:
                
                return data
            
        return data
    
if __name__ == "__main__":
    
    #### end
    #global data
    #data = support__industry__and__sector().return_all_analyses_large(string_incomming_name="Personal Services")
    
    try:
        global x 
        
        x = return__research__and__archives.return_flow_impact_archive( ticker= "CHW",periode = "W" )
        print(x)
    except Exception as e:
        
        print(e)
    
   # print(data, "this is the data")
    