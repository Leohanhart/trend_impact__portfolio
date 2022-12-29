
"""
Created on Thu Mar 31 14:48:20 2022

@author: Gebruiker
"""
import database_querys_main 
import json
from core_scripts.stock_data_download import power_stock_object
import stock_analyses_with_ticker_main as stock_analyses_with_ticker
import datetime
import constants
from collections import ChainMap

class support_class(object):
    
    
    @staticmethod
    def return_stock_analyses(ticker_in : str, stock_analyses : str = "", return_as_json = True, periode = "W", lengt_timeserie = "y3"): 
        """
        
        Example usesge: 
            
            x = support_class.return_stock_analyses("CAR", "moneyflow_data")
            
        Parameters
        ----------
        ticker_in : str
            DESCRIPTION.
        stock_analyses : str, optional
            DESCRIPTION. The default is "".

        Returns
        -------
        None.

        
        #### hier moet eerst een if statement komen om te kijken welke analyses
        #### het grote probleem zit in de truck om de analyses in records te krijgen. 
        #### mogelijk moet er dan een sup cat worden aangemaakt per analyse. Dat is moeilijk.
        """
        # declaire vars
        return_data = {}
        
        analyses = None
        
        # checks active tickers
        data = database_querys_main.database_querys.get_all_active_tickers()
        
        # fixes capitallettter error
        if ticker_in != "" and type(ticker_in):
            ticker_in = ticker_in.upper()
        
        # checks if ticker is active. 
        if ticker_in not in data:
            
            # throws error if something is wrong. 
            return_data['ERROR'] = "ERROR, incomming ticker: " + ticker_in + " is not avalible"
            # package jason
            resp = json.dumps(data)
            
            return resp
        
        # check if analyses exsists.
        if stock_analyses not in constants.stock_avalible_analyses:
            
            # throws error if something is wrong. 
            return_data['ERROR'] = "ERROR, analyeses ticker: " + stock_analyses + " is not avalible"
            # packages jason
            resp = json.dumps(data)
            
            return resp
    	
        # if moneyflow analyes, return moneyflow analyess
        if stock_analyses == "moneyflow_data":        
            
            periode : str = "W"
            ticker_in : str = ticker_in
            analyses : str = "MONEYFLOWS"
            
            try:
                # get data
                analyses = stock_analyses_with_ticker.update_support_functions.get_stock_analyses_with_ticker(ticker_in, analyses , periode )
                
            except Exception as e:
                
                # throws error if something is wrong. 
                return_data['ERROR'] = "ERROR, problem loading MONEYFLOWS ticker: " + ticker_in + " data is not avalible. " + ". " + e
                # packages jason
                resp = json.dumps(return_data)
                
                return resp
            
            #### here could be inplemented optional other data.
        
        # if moneyflow analyes, return liqduity data analyess
        if stock_analyses == "liquidity_data": 
            periode : str = "W"
            ticker_in : str = ticker_in
            analyses : str = "LIQUIDTY"
            
            try:
                
                # get data
                analyses = stock_analyses_with_ticker.update_support_functions.get_stock_analyses_with_ticker(ticker_in, analyses , periode )
        
            except Exception as e:
                
                # throws error if something is wrong. 
                return_data['ERROR'] = "ERROR, problem loading LIQUIDTY ticker: " + ticker_in + " data is not avalible. " + ". " + e
                # packages jason
                resp = json.dumps(data)
                
                return resp
        
        
        # returns a dict of analyses with dicts of the analyses, instate of just the 
        packaged_analyses_dict = support_functions.package_analyses_to_json(analyses,periode_analyses=periode,periode_timeseries=lengt_timeserie)
        
        """
        if seperated analyses are nessseary, here is the place to implement it.
        
        just check if nesseary, retreive the data from the bitch. Put in var, dump, finisched.
        
        """
        # return packaged_analyses_dict
        
        # packges the analyses and returns it. 
        if not return_as_json:
            
            return analyses
        
        # returns as normal     
        resp = json.dumps(packaged_analyses_dict)
        
        return resp
        
                    
            
        
        
    @staticmethod
    def return_data_right_format(ticker_in : str, time_frame : str = "", periode : str = "", tickers_only : bool = False):
        """
        
        Returns the data within the right formats

        Parameters
        ----------
        ticker_in : str
            DESCRIPTION.
        time_frame : str, optional
            DESCRIPTION. The default is "".
        periode : str, optional
            DESCRIPTION. The default is "".

        Returns
        -------
        resp : TYPE
            DESCRIPTION.

        """
        return_data = {}
        time_delta = 0 
        
        # checks active tickers
        data = database_querys_main.database_querys.get_all_active_tickers()
        
        # return tickers only.
        if tickers_only:
            
            resp = data
            
            return resp
        
        # fixes capitallettter error
        if ticker_in != "":
            ticker_in = ticker_in.upper()
        
        # checks if ticker is active. 
        if ticker_in not in data:
            
            # throws error if something is wrong. 
            return_data['ERROR'] = "ERROR, incomming ticker: " + ticker_in + " is not avalible"
            
            #
            resp = json.dumps(return_data)
            
            return resp
            
        else:
            
            # check if time frame is allowd
            if time_frame != "" and time_frame not in constants.stock_avalible_timeframes:
                # throws error if something is wrong. 
                return_data['ERROR'] = "ERROR, incomming timeframe: " + time_frame + " is not avalible"
                
                #
                
                resp = json.dumps(return_data)
                
                return resp
            
            # checks if periode is allowd.
            if periode != "" and periode not in constants.stock_avalible_periodes:
                # throws error if something is wrong. 
                return_data['ERROR'] = "ERROR, incomming periode: " + periode + " is not avalible"
                
                #
                
                resp = json.dumps(return_data)
                
                return resp
            
            # set periode 
            if periode == "w":
                
                # creating powerstock object
                stocks_object = power_stock_object.power_stock_object(stock_ticker = ticker_in, periode_weekly=True)
                
                data = stocks_object.stock_data
                
                data = data.to_dict(orient='records')
                
                resp = json.dumps(data)
                
                return data
            else:
                stocks_object = power_stock_object.power_stock_object(stock_ticker = ticker_in, periode_weekly=False)
                
            # if periode is set. Set the timeframe
            if time_frame != "":
                
                # set time frame 
                if time_frame == "q":
                    
                    time_delta = 92
                    
                elif time_frame == "y":
                    
                    time_delta = 365
        
                elif time_frame == "y1":
                    
                    time_delta = 365
                    
                elif time_frame == "y3":
                    
                    time_delta = 1095
                    
                elif time_frame == "y5":
                    
                    time_delta = 1825
                    
                elif time_frame == "y10":
                    
                    time_delta = 3650
                    
                elif time_frame == "all":
                    
                    # return the data
                    data = stocks_object.stock_data
                    data.Date = data.Date.dt.strftime('%d-%m-%Y') 
                    data = data.to_dict(orient='records')
                    
                    resp = json.dumps(data)
                    
                    return resp
                # returns with time delta
                
                
                
                # checks and sets timedelta if is longer than avaliblity
                if len(data) < time_delta:
                    time_delta = len(data)-1
                
                # selects date for filter
                previous_date = datetime.datetime.today() - datetime.timedelta(days=time_delta)
                now_date = datetime.datetime.today()
                
                # sets data after filter
                data = stocks_object.stock_data.loc[previous_date:now_date]
                
                # sets date
                data.Date = data.Date.dt.strftime('%d-%m-%Y') 
                
                data = data.to_dict(orient='records')
                
                
                resp = json.dumps(data)
                 
                return resp
            
            
            print("We are here.")
            
            # return the data
            data = stocks_object.stock_data
            data.Date = data.Date.dt.strftime('%d-%m-%Y') 
            
            global data_exit
            # data routes.
            result = data.to_json(orient='records') 
            parsed = json.loads(result)
            data_exit = json.dumps(parsed)  
            
            #resp = json.dumps(data_xd)
              
            return data.to_json(orient='records') 




class support_functions(object):
    
    @staticmethod
    def package_analyses_to_json(analyses, periode_analyses = "W", periode_timeseries = "y2"):
        """
        Packages analyses to json. 
        
        Works only for the costum analsyses build by Leo Hanhart
        
        Creates a dict with dicts of the analyses. proces is easy.

        Parameters
        ----------
        analyses : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        time_frame = periode_timeseries
        # vars
        cluster_analyses = {}
        
        analyses_time_series = ['indicator_timeserie_raw', 'indicator_timeserie_profile', 'indicator_timeserie_profile_change', 'indicator_timeserie_change']
        analyses_single_vars = ['last_calculation_indicator', 'last_calculation_profile_indicator_text', 'last_calculation_profile_indicator_number', 'last_calculation_profile_change_text', 'last_calculation_profile_change_number']
        
        # tries to set single vars in cluster analyses - this should be very ease
        try:
            
            # loops true the single vars. 
            for i in analyses_single_vars:
                
                cluster_analyses[i] = analyses[i]
                
        # if fails it needs to be reported, could be if mismatch with error.
        except Exception as e:
            
            raise Exception("Trouble with converting single vars.")
            
        try:
            
            for i in analyses_time_series:
                
                # sets analyses dataframe in var'single_analyses'
                singel_analyses = analyses[i]
                
                # get time delta
                if time_frame != "all" :
                    
                    if periode_analyses == "D":
                    
                        if time_frame == "q":
                            
                            time_delta = 92
                            
                        elif time_frame == "y":
                            
                            time_delta = 365
                
                        elif time_frame == "y1":
                            
                            time_delta = 365
                            
                        elif time_frame == "y2":
                            
                            time_delta = 710
                        elif time_frame == "y3":
                            
                            time_delta = 1095
                            
                        elif time_frame == "y5":
                            
                            time_delta = 1825
                            
                        elif time_frame == "y10":
                            
                            time_delta = 3650
                            
                    if periode_analyses == "W":
                        
                        if time_frame == "q":
                            
                            time_delta = 13
                            
                        elif time_frame == "y":
                            
                            time_delta = 51
                
                        elif time_frame == "y1":
                            
                            time_delta = 51
                        
                        elif time_frame == "y2":
                            
                            time_delta = 102
                            
                        elif time_frame == "y3":
                            
                            time_delta = 153
                            
                        elif time_frame == "y5":
                            
                            time_delta = 205
                            
                        elif time_frame == "y10":
                            
                            time_delta = 510
                        
                        
                    singel_analyses= singel_analyses.tail(time_delta)
                    
                    
                    
                # reset index. 
                o = singel_analyses.reset_index()
                
                # o stands for object. this line converts data to right date format. WHY? the normal time stamp is not allowd to convert to json. 
                o.Date = o.Date.dt.strftime('%d-%m-%Y')
                
                # converts the timeserie data to json data. 
                data = o.to_dict(orient='records')
                
                # set tot cluster with same name
                cluster_analyses[i] = data
                
        # if fails it needs to be reported, could be hard error. 
        except Exception as e:
            
            raise Exception("Trouble with converting timeseries vars.")

        return cluster_analyses


    @staticmethod
    def tail_analyse_analyses(lengt_periode = 502): 
        
        pass



if __name__ == "__main__":    
    
    try:
        
        global x 
        
        x = support_class.return_stock_analyses("CAR", "moneyflow_data",return_as_json=False)
    
    except Exception as e:
        
        print(e)
    
    