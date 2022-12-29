import constants

from core_scripts.synchronization import synch_class
from core_scripts.stock_data_download import power_stock_object_support_functions as support_functions
#from stock_analyses import stock_analyses, stock_analyses_with_ticker
import stock_analyses_main as stock_analyses
import stock_analyses_with_ticker_main as stock_analyses_with_ticker
from core_scripts.stock_data_download import power_stock_object as stock_object

import database_querys_main

import pandas as pd
import operator

"""

IMPORTANT: ALWAYSE USE DROP, this will renamed to SUMMED. 


LOGBOOK
    15-07 : removed cut logic in merge_data. Big problem occured with cutting data that dident function. 
            I dont know why, but the tickers are sorted so the longest will start and no data will be loset.
            in the module there is a statment that says if data is longer, tail, else return (DROP the thing). 
            This is focking crippeld. This statment fucks everything up.
            
            I replaced the mess.. legacy code bullshit done by an idiot myself with one python line that adds two frames..
            
  
"""


# can be removed after woch
import time


class sector_analyse:
    """
    
    """
    
    ## data storage of tickers and industry
    
    # use injected tickers : 
    use_injected_tickers : bool         = bool 
    # list with tickers
    injected_tickers : list             = []
    # dict of all related ticker data
    main_dict   : dict                  = dict 
    # gets list of sectors
    sectors     : list                  = list 
    # gets list of industy's
    industry    : list                  = list
    # gets list of tickers
    tickers     : list                  = list
    # gets list of the avalible analyses
    analyeses   : list                  = list
    
    ## selecteded tickers 
    ticker_selected : list              = list
    
    
    # there needs to be a setup that always loads the tickers and industry's and so on. 
    def __init__(self):
        
        # sets industy and tickers
        # stock_mother_object =       mother_data_object()
        
        # sets main dict
        # self.main_dict      =       stock_mother_object.main_dict
        
        # sest secpts
        self.sectors        =       database_querys_main.database_querys.get_all_active_sectors()
        
        # sets industy
        self.industry       =       database_querys_main.database_querys.get_all_active_industrys()
        
        # sets tickers               
        self.tickers        =       database_querys_main.database_querys.get_all_active_tickers()
    
        # boots analyes object
        main_stock_analyses = stock_analyses.main_analyeses(easy_load = True)
        
        # retreives the analyses 
        self.analyeses      =       main_stock_analyses.analyses_names
        
        
    def create_industy_or_sector_analyses(self, name_industry_or_sector : str = None, 
                                          periode : str = "W", 
                                          name_anlyeses = "MONEYFLOWS", 
                                          sub_atribute_analyses = "indicator_timeserie_raw", 
                                          methode : str = "SUMMED", 
                                          min_amount_rows : int = 500,
                                          use_injected_tickers : bool = False,
                                          average_out : bool = False
                                          ): 
        """
        

        Parameters
        ----------
        name_industry_or_sector : str, optional
            DESCRIPTION. The default is None.
        periode : str, optional
            DESCRIPTION. The default is "W".
        name_anlyeses : TYPE, optional
            DESCRIPTION. The default is "MONEYFLOWS".
        sub_atribute_analyses : TYPE, optional
            DESCRIPTION. The default is "indicator_timeserie_raw".
        methode : str, optional
            DESCRIPTION. The default is "DROP".
            
            "SUMMED"        =   Methode where all tickers are summed on top of  each other.
            "AVERAGE"       =   Average of all calculation. 
            "FIT"           =   FIT is the mode where all tickers are added. 
            "CBIND_DROP"    =   Wide means that all the series are cbinded if length is tall enough.
            "CBIND_FIT"     =   Cbinded and added with 0 if not matching length.
            
        min_amount_rows : int, optional
            DESCRIPTION. The default is 500.
            
        use_injected_tickers : bool = parameter for using injected tickers, those are injected in self.injected_tickers
        
        Returns
        -------
        sumed_industy_data : TYPE
            DESCRIPTION.

        """
        
        # check if analyses excists.
        if not name_anlyeses in self.analyeses:    
            
            raise Exception("input_analyses_not_avalible")
        
        # chosen for the injected tickers
        if use_injected_tickers:
        
            self.ticker_selected = self.injected_tickers
        
        # check if varible matches sector or industry and selects tickers
        elif name_industry_or_sector in self.industry:
        
            self.ticker_selected = database_querys_main.database_querys.get_all_stocks_with_industry(name_industry_or_sector)
        
        elif name_industry_or_sector in self.sectors:
            
            self.ticker_selected = database_querys_main.database_querys.get_all_stocks_with_sector(name_industry_or_sector)
        
        else:
            
            raise Exception("Input_value_name_industry_or_sector_did_not_match", "create_industy_or_sector_analyses" )
            
            
        if methode == "SUMMED": 
            # here should be the decleration for important datastoranges
            data_cluster   = cluster_data.create_mergede_frame_summed_indicator(
                
                                                                list_tickers = self.ticker_selected,
                                                                
                                                                name_analyeses   = name_anlyeses,
                                                                
                                                                atribute         = sub_atribute_analyses,
                                                               
                                                                periode          = periode,
                                                                
                                                                min_rows         = min_amount_rows,
                                                                
                                                                average_out_total = average_out
                                                                
                                                                )
        if methode == "FIT":
            
            data_cluster = cluster_data.create_merged_datafame_zero_drop(
                
                                                                list_tickers = self.ticker_selected,
                                                                
                                                                name_analyeses   = name_anlyeses,
                                                                
                                                                atribute         = sub_atribute_analyses,
                                                               
                                                                periode          = periode,
                                                                
                                                                )
        
        #### here should the average_out methode be added. MAKE SURE METHODE FIX is added.
        # this methode creates a dataframe with only 0, every stock that loops true it adds 1 on every field it gets. 
        # after this proces, the stocks loop again true a dataframe with only zero's but this time they add the indictator.
        # in the end, this proces the data is divided with the rates of the first dataframe.
        
        return   data_cluster


class sector_analyses_support_funtions(object):
    
    def check_input_parrameters(arguments : list = []):
        """
        Check if arguments are fitting needs.

        Parameters
        ----------
        arguments : list, optional
            DESCRIPTION. The default is [].

        Raises
        ------
        Exception
            DESCRIPTION.

        Returns
        -------
        None.

        """
        
        
        if len(arguments) != 3:
            raise Exception("Input value  is None", "sector_analyses_support_functions")
            
        # check data
        if not sector_analyses_support_funtions.check_if_constructior_values_are_legit(constructorvalues = arguments):

            raise Exception("Input value  is None", "sector_analyses_support_functions")
    
        # check if time frame is avalibel
        if not sector_analyses_support_funtions.check_if_timeframe_is_allowed( arguments[1]):
 
            raise Exception("Input Timeframe is not avalible", "sector_analyses_support_functions")
            
        # check if analyses exists.
        if not sector_analyses_support_funtions.check_if_analyses_exist(name_of_analyses=arguments[2]):
            
            raise Exception("Input Analyses is not avalible", "sector_analyses_support_functions")
        
    
    
    def get_raw_analyses(ticker = None, analyeses_name = "", periode = ""):
        
        # gets analyses dictornary
        dict_analayes = sector_analyses_support_funtions.get_analyses_with_ticker(ticker = ticker, analyeses_name = analyeses_name, periode = periode)
        
        # get raw analyeses
        raw_data = dict_analayes["indicator_timeserie_raw"]
        
        return raw_data
    
    def get_analyses(ticker = None, analyeses_name = "", periode = "", name_column_analyses = ""):
        """
        Returns an analyses if choice with the suited analyses, this means that you can load the RAW, Profiles and many more. 

        Parameters
        ----------
        ticker : TYPE, optional
            DESCRIPTION. The default is None.
        analyeses_name : TYPE, optional
            DESCRIPTION. The default is "".
        periode : TYPE, optional
            DESCRIPTION. The default is "".
        name_column_analyses : TYPE, optional
            DESCRIPTION. The default is "".

        Raises
        ------
        Exception
            DESCRIPTION.
        exception
            DESCRIPTION.

        Returns
        -------
        raw_data : TYPE
            DESCRIPTION.

        """
        """
        this function has a piped version of getting analsyses. 04-05-22 function implemented
        """
        
        # gets analyses dictornary
        try:
            
            # returns analayes dictornary.  
            #dict_analayes = sector_analyses_support_funtions.get_analyses_with_ticker(ticker=ticker, analyeses_name = analyeses_name, periode = periode)
            dict_analayes = stock_analyses_with_ticker.update_support_functions.get_stock_analyses_with_ticker(ticker=ticker, analyeses_name = analyeses_name, periode = periode)
       
        except ValueError:
            
            raise ValueError
            
        except Exception as e :
            
            print(e)
            # thows error. 
            raise Exception("Problem with loading analyses", "Sector analyses support function", e )
            
        # checks if the atribute is avalible.            
        if not sector_analyses_support_funtions.check_if_the_analyses_atribute_exsists(name_column_analyses):
            
            # raise exception if failed
            raise Exception("Atribute of the analyses is not avalible: " , )
        
        # get raw analyeses
        raw_data = dict_analayes[name_column_analyses]
        
        return raw_data
    
    
    def get_analyses_with_ticker(self, ticker = None, analyeses_name = "", periode = ""):
        """
        

        Parameters
        ----------
        ticker : TYPE, optional
            DESCRIPTION. The default is None.
        analyeses_name : TYPE, optional
            DESCRIPTION. The default is "".
        periode : TYPE, optional
            DESCRIPTION. The default is "".

        Raises
        ------
        Exception
            DESCRIPTION.

        Returns
        -------
        dictonary : TYPE
            DESCRIPTION.

        """
        
        # checks if analyses is exsisting
        if not sector_analyses_support_funtions.check_if_analyses_exist(name_of_analyses=analyeses_name):
         
            raise Exception("Analayses is not avalible for ticker = ", ticker , "class : sector support functions")
        
        # check if timeframe is alowed - addiontional function
        elif not sector_analyses_support_funtions.check_if_timeframe_is_allowed(timeframe=periode):
           
            raise Exception("timeframe is not avalible for ticker = ", ticker , "class : sector support functions")
        
        else:
            
            # sets stockdata
            stock_data = sector_analyses_support_funtions.get_stock_data_with_ticker(ticker=ticker , timeframe= periode)
             
            
            # sets analyeses object
            analyses = stock_analyses.main_analyeses(stock_ticker = ticker, stock_data = stock_data, timeframe=periode)
            
            # loads analayes
            analyses.load_analyese( title_analyses = analyeses_name)
            
            # extracts the dictonary
            dictonary =  analyses.analyeses_dictionary
            
            # returns the dictornaty
            return dictonary
        
    @staticmethod            
    def get_stock_data_with_ticker( ticker : str = "", timeframe = "D"):
        """
        Loads stockdata. Returns pandas dataframe with the stockdata.

        Parameters
        ----------
        ticker : TYPE, optional
            DESCRIPTION. The default is None.
        timeframe : TYPE, optional
            DESCRIPTION. The default is None.

        Returns
        -------
        None.

        

        05-01-2022  : Today I add that D and W data are booted seperate 
        """
        
        # boots powerstockobject with the selected ticker. 
        
        
        if timeframe == "D": 
            power_object = stock_object.power_stock_object(stock_ticker = ticker, simplyfied_load = True, periode_weekly = False)
        elif timeframe == "W":
            power_object = stock_object.power_stock_object(stock_ticker = ticker, simplyfied_load = True, periode_weekly = True)
        
        else:
            
            raise Exception("timeframe is not avalible for ticker = ", ticker , "class : sector support functions")
        
        return power_object.stock_data
        
    def return_tickers_industry(name_industry, list_industrys ) -> list:
        """
        Returns  the tickers of the selected industry

        Parameters
        ----------
        name_industry : TYPE
            DESCRIPTION.
        list_industrys : TYPE
            DESCRIPTION.

        Returns
        -------
        list
            DESCRIPTION.

        """
        
        ticker_selected = list(list_industrys[name_industry].keys())
        return ticker_selected
    
    def check_if_the_analyses_atribute_exsists(name_analyeses, return_avalible_analyses = False):
        """
        

        Parameters
        ----------
        name_analyeses : TYPE
            DESCRIPTION.
        return_avalible_analyses : TYPE, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        
        
        # if wanted, the function can return the avalible analyeses
        if return_avalible_analyses:
            x = stock_analyses.main_analyeses.atributes_analyeses
            return x 
        
        # check if the analyses excists. 
        if not name_analyeses in  stock_analyses.main_analyeses.atributes_analyeses:
            return False
        else:
            return True 
        return False
    
    @staticmethod 
    def check_if_timeframe_is_allowed(timeframe ):
        """
        Check if the time is allowd

        Parameters
        ----------
        timeframe : TYPE, optional
            DESCRIPTION. The default is None.

        Returns
        -------
        bool
            DESCRIPTION.

        """
        
        
        
        
        # avalible timeframes
        if timeframe in ["Monthly","Weekly","Daily", "D", "W", "M"] :
            return True
        else:
            return False
        return False
        
    def check_if_constructior_values_are_legit( constructorvalues = [], **kwargs) -> bool:
        """
        Checks of the input values are not equal to None 

        Parameters
        ----------
        constructorvalues : TYPE, optional
            DESCRIPTION. The default is [].

        Returns
        -------
        bool
            DESCRIPTION.

        """
        for i in range(0,len(constructorvalues)):
            if type(constructorvalues[i]) == None:
                return False
        return True
    
    @staticmethod
    def check_if_analyses_exist( name_of_analyses : str = "") -> bool:
        """
        checks if the analyses selected is avalible in the main_analyses objects

        Parameters
        ----------
        name_of_analyses : TYPE, optional
            DESCRIPTION. The default is None.

        Returns
        -------
        bool
            DESCRIPTION.

        """
        
     
        # loads main_stock_object. 
        main_stock_analyses = stock_analyses.main_analyeses(easy_load = True)
        
        # 
        if name_of_analyses in main_stock_analyses.analyses_names:
            return True
        else:
            return False
        
        return False
        
class cluster_data: 
    
    
    def __init__(self):
        pass 
    
    def create_merged_frame_max_length( list_ticker : list = [], colnames : list = [] , analyses : list = [] , atributes: list = [] , periode = "D"):
        """  
        If you want this function to work than you can use the sector analyses support function, there are the function
        
        fast loop to get the stockdata, after that the analyses and atributes, afterthat merge to main, and contiue.
        
        # get best possible length. 
        for i in range(0,len(list_ticker)):
            
            sector_analyses_support_funtions.get_stock_data_with_ticker(ticker=list_ticker[i],timeframe="D")
            """
        pass
    
    def create_merged_datafame_zero_drop(list_tickers : list  = [], 
                                                                   name_analyeses : str = None,
                                                                   atribute : str = "indicator_timeserie_raw",
                                                                   periode : str = "W",):
        
        # check if list is ledgid
        if not merge_support_functions.check_list_cluster_is_legid( list_tickers):
            raise Exception("Problem with list")
        
        
        # returns list with the tickers sorted from large to small. So the firstone can be used to sum the rest over it.         
        tickers_sorted = cluster_support_functions.returns_amount_of_valide_tickers(list_tickers,periode=periode, low_high = False)
        
        # sets main ticker
        main_ticker = tickers_sorted[0]
        
        # sets main data - downloads the first data. 
        main_data   = sector_analyses_support_funtions.get_analyses( ticker= main_ticker, 
                                                       analyeses_name = name_analyeses,
                                                       name_column_analyses= atribute,
                                                       periode = periode) 

        
        # adds tickers to the main dataframe
        for i in range(0,len(list_tickers)):
            
            try: 
                # retreives incomming data.
               new_data = sector_analyses_support_funtions.get_analyses( ticker= list_tickers[i], 
                                                              analyeses_name = name_analyeses,
                                                              name_column_analyses= atribute,
                                                              periode = periode)
               
            except ValueError:
                
               continue
           
            except Exception as e:
                
                continue 
           # merges the new analyses data with the main
           
            try: 
            
                main_data = merge_data.merge_data(dataframe_main = main_data, new_dataframe= new_data)
            
            except Exception as e: 
                
                print(e)
                continue
            
        
        return main_data
        
        
        
        return tickers_sorted
        
        
    
    def create_mergede_frame_summed_indicator(  list_tickers : list  = [], 
                                                                   name_analyeses : str = None,
                                                                   atribute : str = "indicator_timeserie_raw",
                                                                   periode : str = "W",
                                                                   min_rows : int = 500,
                                                                   average_out_total : bool = False
                                                                   ):
        """
        Returns a merge frame of sumed values of an anlyses
        
    

        Parameters
        ----------
        list_tickers : list, optional
            DESCRIPTION. The default is [].
        name_analyeses : str, optional
            DESCRIPTION. The default is None.
        atribute : str, optional
            DESCRIPTION. The default is "indicator_timeserie_raw".
        periode : str, optional
            DESCRIPTION. The default is "W".

        Raises
        ------
        Exception
            DESCRIPTION.

        Returns
        -------
        None.

        """
        
        
        
        # check if list is ledgid
        if not merge_support_functions.check_list_cluster_is_legid( list_tickers ):
            raise Exception("Problem with list")
   
        list_tickers = cluster_support_functions.returns_amount_of_valide_tickers(list_tickers,periode=periode, low_high = False)
        
        main_data = 0 
        main_ticker = 0
        
        # first loop insists only for the first stock to be picket
        for i in range(0,len(list_tickers)):
           
           try:
                # retreives incomming data.
               new_data = sector_analyses_support_funtions.get_analyses( ticker= list_tickers[i], 
                                                              analyeses_name = name_analyeses,
                                                              name_column_analyses= atribute,
                                                              periode = periode)
           except:
               
               list_tickers.remove(list_tickers[i])
               
               continue
           
           # selects the amount of rows
           amount_of_rows = cluster_support_functions.return_amount_of_rows_with_periode(periode)
        
    
           
           # check if data is allowd.to become main. This function only 
           if( cluster_support_functions.chech_if_data_is_allowd_for_main(new_data, min_amount_rows = amount_of_rows) 
              
              and 
              
              # check if main_data is allowd to assing
              cluster_support_functions.check_main_data_is_allowd_for_assign(new_data)
              
              ):
               
              # sets new data as main
              main_data = new_data
              
              # selected main 
              selected_main_data = main_data
              
              # sets main_ticker
              main_ticker= list_tickers[i]
              
              # breaks loop
              break
        
           else:
               
               continue
        if 0 ==0:
            pass
        # removes added ticker
        list_tickers.remove(main_ticker)
           
        #### here should be the point where the first frame is created. overwrite the incomming analyses data with 1. 
        #### VERY IMPRORTANT : IF VALUE is zero of the timeserie, add 0. 
           
        # adds tickers to the main dataframe
        for i in range(0,len(list_tickers)):
           
           # retreives incomming data.
            try: 
                # retreives incomming data.
               new_data = sector_analyses_support_funtions.get_analyses( ticker= list_tickers[i], 
                                                              analyeses_name = name_analyeses,
                                                              name_column_analyses= atribute,
                                                              periode = periode)
               
            except ValueError:
                
               continue
           
            except Exception as e:
                
                continue 
           # merges the new analyses data with the main
           
            try: 
            
                main_data = merge_data.merge_data(dataframe_main = main_data, new_dataframe= new_data)
            
            except Exception as e: 
                
                print(e)
                continue
        #### now, loop again. Add the indicator. 
        
        if average_out_total: 
            
            selected_main_data.Data = 1
            
            main_data_avg_amount = selected_main_data
            
            # adds tickers to the main dataframe
            for i in range(0,len(list_tickers)):
               
               # retreives incomming data.
                try: 
                    # retreives incomming data.
                   new_data = sector_analyses_support_funtions.get_analyses( ticker= list_tickers[i], 
                                                                  analyeses_name = name_analyeses,
                                                                  name_column_analyses= atribute,
                                                                  periode = periode)
                   
                except ValueError:
                    
                   continue
               
                except Exception as e:
                    
                    continue 
                
                new_data.Data = 1
                               
                try: 
                
                    main_data_avg_amount = merge_data.merge_data(dataframe_main = main_data_avg_amount, new_dataframe= new_data)
                
                except Exception as e: 
                    
                    print(e)
                    continue
            pd.set_option('display.float_format', '{:.2f}'.format)
               # merges the new analyses data with the main
            average_data = main_data / main_data_avg_amount
            
            return average_data
        #### now divide the second dataframe with the firstone. 
        
        return main_data
        
        

class cluster_support_functions:
    
    def returns_valide_ticker_with_length(list_tickers = [], amount_of_rows : int = 0):
        """
        

        Parameters
        ----------
        list_tickers : TYPE, optional
            DESCRIPTION. The default is [].
        periode : TYPE, optional
            DESCRIPTION. The default is periode.

        Returns
        -------
        list_stocks : TYPE
            DESCRIPTION.

        """
        
        # remove tickers that are two short.  
        amount_of_rows = amount_of_rows
        
        # lists of indicators
        list_stocks     = list_tickers
        list_numbers    = []
        
        # loops true tickers
        for i in range(0,len(list_tickers)):    
            
            
            
            # returns stock data.
            stock = sector_analyses_support_funtions.get_stock_data_with_ticker(list_tickers[i])
            
            # check if data is long enough. 
            if not cluster_support_functions.check_if_lengt_stock_is_long_enough(data=stock,minimum_lengt=amount_of_rows):
                
                ticker_that_needs_to_be_removed = list_tickers[i]
                
                
            else:
                ticker_that_needs_to_be_added = list_tickers[i]
                list_numbers.append(ticker_that_needs_to_be_added)
                
                
                
        return list_numbers
            
            
    def returns_amount_of_valide_tickers(list_tickers = [], periode = "", low_high = True):
        """
        Checks on length, soorts on lenght

        Parameters
        ----------
        list_tickers : TYPE, optional
            DESCRIPTION. The default is [].
        periode : TYPE, optional
            DESCRIPTION. The default is "".

        Returns
        -------
        None.

        """
        # remove tickers that are two short.  
        amount_of_rows = cluster_support_functions.return_amount_of_rows_with_periode(periode)
        
        # returns group tickers with right length.
        list_tickers = cluster_support_functions.returns_valide_ticker_with_length(list_tickers=list_tickers, amount_of_rows=amount_of_rows)
        
        # lists of indicators
        list_stocks     = []
        list_lengt      = []
        
        # loops true the stocks
        for i in range(0,len(list_tickers)):    
            
            # retreives the stock 
            stock = sector_analyses_support_funtions.get_stock_data_with_ticker(list_tickers[i], timeframe = periode)
            
            # extracts the length of a stock
            leng_stock = len(stock)
            
            # appends the amount to the list
            list_lengt.append(leng_stock)
                             
            # retreives the name of the stock
            name_stock = list_tickers[i]
            
            # appends the name of the stock
            list_stocks.append(list_tickers[i])
        
        # creates a sorted list.
        sorted_list = cluster_support_functions.return_sorted_stocks(list_tickers= list_stocks, 
                                                                     list_length = list_lengt,
                                                                     low_high= low_high)
        print(sorted_list, "end function")
        return sorted_list

            
    def return_sorted_stocks(list_tickers = [], list_length = [], low_high = True):
        """
        Returns a sorted list of stocks 

        Parameters
        ----------
        list_tickers : TYPE, optional
            DESCRIPTION. The default is [].
        list_length : TYPE, optional
            DESCRIPTION. The default is [].
        low_high : TYPE, optional
            DESCRIPTION. The default is True.

        Returns
        -------
        list_tickers : TYPE
            DESCRIPTION.

        """
        zipped = zip(list_tickers, list_length)
      
        # Converting to list
        zipped = list(zipped)
          
        # Printing zipped list
        print("Initial zipped list - ", str(zipped))
          
        # Using sorted and operator
        res = sorted(zipped, key = operator.itemgetter(1))
        
        res = sorted(zipped, key = operator.itemgetter(1))
        
        zipped = res
        
        unzipped_object = zip(*zipped)
        
        unzipped_list = list(unzipped_object)
        
        list_tickers = list(unzipped_list[0])
        
        print(list_tickers, "list in function")
        # 
        if not low_high:
            
            list_tickers.reverse()
            
        return list_tickers
            # printing result
        
        
        
    def return_amount_of_rows_with_periode(periode : str = "W"): 
        """
        Returns amount of rows that we think is nessary for an analyses.

        Parameters
        ----------
        periode : str, optional
            DESCRIPTION. The default is "W".

        Returns
        -------
        int
            DESCRIPTION.

        """
        
        if periode == "W":
            return 102
        if periode == "D":
            return 502
        if periode == "M":
            return 24
        else:
            return 0 
        
    def check_if_lengt_stock_is_long_enough(data = 0, minimum_lengt : int = 0):
        """
        Check if the 

        Parameters
        ----------
        data : TYPE, optional
            DESCRIPTION. The default is 0.
        minimum_lengt : int, optional
            DESCRIPTION. The default is 0.

        Raises
        ------
        Exception
            DESCRIPTION.

        Returns
        -------
        bool
            DESCRIPTION.

        """
        
        if minimum_lengt == 0:
            raise Exception("Error in providing length for the cluster data class function")
        if len(data) >= minimum_lengt:
            return True
        else: 
            return False
        
    def chech_if_data_is_allowd_for_main(data = 0 , min_amount_rows : int = 500):  
        """
        
        Check if the data is complete.( Ncol, + Len)
        Returns true if so. 

        Parameters
        ----------
        data : TYPE
            DESCRIPTION.

        Returns
        -------
        bool
            DESCRIPTION.

        """
        if(merge_support_functions.check_if_analyses_is_complete( data_frame = data  )
           
           and 
           
           len(data) > min_amount_rows):
            
            return True
        
        else:
            
            return False
       
    def check_main_data_is_allowd_for_assign(data):
        """
        Check if the data is allowd fo assigment. This happens when var is no int.
        

        Parameters
        ----------
        data : TYPE
            DESCRIPTION.

        Returns
        -------
        bool
            DESCRIPTION.

        """    
        if type(data) == int:
            
           return False
       
        else:
            
           return True
            
class merge_data:
    
    # object classes
    
    data_convertion_object = None
    
    def __init__(self):
        
        # creates data_convertion object
        self.data_convertion_object = support_functions.data_modifications()
        
        
    def merge_data( 
                   dataframe_main = None, 
                   new_dataframe = None, 
                   drop_rate = 0,            # the minimum length of a dataframe
                   ):  
        """
        
        merges data into one frame, this meanse that data from the new data is added to the datafrane_main
        
        return type 
        Error 1.    Data is droped

        Parameters
        ----------
        dataframe_main : TYPE, optional
            DESCRIPTION. The default is None.
        new_dataframe : TYPE, optional
            DESCRIPTION. The default is None.
        drop_rate : TYPE, optional
            DESCRIPTION. 
            
            Drop rate is the length for a stock that the datawill need to get added, to short means data is missing. 
            
            The default is None.
        # the minimum length of a dataframe : TYPE
            DESCRIPTION.

        Raises
        ------
        Exception
            DESCRIPTION.

        Returns
        -------
        int
            DESCRIPTION.

        """
        
        # check if the dataframes have None-Type datastructures
        if not merge_support_functions.check_types_data_are_valide(dataframe_main, new_dataframe):
            
            raise Exception("There was a Nonetype datavalue found in", " merge_data", "merge_data_class")
        
       
        # handy for data_prepartoin, shut down because of 
        #dataframe_main = merge_support_functions.prepair_main_data_first_stage( main_data = dataframe_main, drop_rate = len(dataframe_main))


        # check if the new_dataframe hase a valide lengt. 
        if not merge_support_functions.check_lenght_valide(drop_rate = drop_rate, data_two = new_dataframe):
            
             # drop the new data, the data is not long enaugh, if this happends there will be a drop in the frame.
             return dataframe_main  
         
                
        # merge the data
        merged_data = merge_support_functions.merge_two_dataframes(data_frame_main = dataframe_main, data_frame_new =new_dataframe )
          
        return merged_data
            
            
class merge_support_functions:
    
    
    def merge_rbind(self):
        # should be the function that Rrinds the whole dataframe. 
        pass
    
    def merge_two_dataframes( data_frame_main, data_frame_new):
        """
        function merges two dataframes, this means that the values are added toghetter into one datacolumn.
        This means that this requires no kind of Rbind or what so ever.

        Parameters
        ----------
        data_frame_main : TYPE
            
        DESCRIPTION.
            
            the dataframe that needs to be used as the mother frame. 
            
        data_frame_new : TYPE
        
        DESCRIPTION.
            
        this is the new dataframe. This one will be added to the data for the other dataframe.
        
        Returns
        -------
        the_full_dataframe : TYPE
        
            DESCRIPTION.

        """
        data_frame_main = data_frame_main.add(data_frame_new, fill_value=0)
        
        return data_frame_main
    
    def check_if_analyses_is_complete(data_frame):
        """
        Check if analyses is complete

        Parameters
        ----------
        data : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        # check if the frame contains the column data. 
        if len(data_frame.columns) == 1 and "Data" in data_frame.columns:
            
            # 
            return True
        else:
            return False
        
    def divide_data(data_frame , amount_of_divide = 100000000):
        """
        This is function is used to cut large numbers in to peases of 100 milion. 

        Parameters
        ----------
        data_frame : TYPE
            DESCRIPTION.
        amount_of_divide : TYPE, optional
            DESCRIPTION. The default is 10000000.

        Raises
        ------
        Exception
            DESCRIPTION.

        Returns
        -------
        data_frame : TYPE
            DESCRIPTION.

        """
        # check if dataframe is an analyeses object and contains the data.
        if len(data_frame.columns) == 1 and "Data" in data_frame.columns:
            
            # cuts the analyesses
            for i in range(0,len(data_frame)):
                
                # does action
                data_frame.iloc[i] = data_frame.iloc[i] / amount_of_divide
                
            # retiurns the data
            return data_frame
        
        # if the data is not the right type, there is a problem. 
        else:
            
            raise Exception("No legid analyses declared, could be an other dataframe of one with to much colums", "merge_support")
        
    
    def check_list_cluster_is_legid(list_in : list = [] ) -> bool:
        """
        Check if list is legal. 

        Parameters
        ----------
        list_in : list, optional
            DESCRIPTION. The default is [].

        Raises
        ------
        Exception
            DESCRIPTION.

        Returns
        -------
        bool
            DESCRIPTION.

        """
        # check if the input type is valide
        if not type(list_in) == list:
            
            #raises exception 
            raise Exception("input list is no lstt")
        
        # check if the list has enough items.
        if len(list_in) <= 2:
            
            # raises exception
            raise Exception("input list has not enough itmes")
        
        # if the data is the right input type && has the right length. it returns as true
        else:
            
            return True
        
    def unpack_the_dataframe( data_frame = None) -> list:
        
        # unpacks the values 
        data_values     = data_frame.values
        data_list       = data_values.tolist()
        data_unnested   = flat_list = [item for sublist in data_list for item in sublist]

        return data_unnested
        
    
    def prepair_main_data_first_stage(main_data, drop_rate = 0):
        """
        Prepairs the data, with this function the data will be cutt in the right format.

        Parameters
        ----------
        main_data : TYPE
            DESCRIPTION.
        drop_rate : TYPE, optional
            DESCRIPTION. The default is 0.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        
        ## this function is build for the data prepairations
        
        #
        # if the data needs to get a cut, this funnction will do it, the value of drope rate will be more than one. 
        if drop_rate > 0:
            
            # drops the amount of the droprate
            new_data_main = main_data.tail(drop_rate)
            
            # returns the amount 
            return new_data_main

        # returns the incomming data
        else:
            
            return main_data
            
    
    def check_if_lenghts_are_equal(self, data_frame_one = None, dataframe_new = None) -> bool:
        """
        Checks if the lengths are equal. 

        Parameters
        ----------
        data_frame_one : TYPE, optional
            DESCRIPTION. The default is None.
        dataframe_new : TYPE, optional
            DESCRIPTION. The default is None.

        Raises
        ------
        Exception
            DESCRIPTION.

        Returns
        -------
        bool
            DESCRIPTION.

        """
        
        # check if length of the dataframes are equal.
        if len(data_frame_one) == len(dataframe_new):
            
            return True
        
        else:
            
            raise Exception("The length of the two dataframes are not equal", "Merge_support_functions")
    
    def tail_the_lenght_in_right_formate(dataframe_new = None, data_frame_main = None):
        """
        

        Parameters
        ----------
        dataframe_new : TYPE, optional
            DESCRIPTION. The default is None.
        data_frame_main : TYPE, optional
            DESCRIPTION. The default is None.

        Returns
        -------
        None.

        """
        # tails the dataframe in the length of the dataframe. 
        data_frame_new  = dataframe_new.tail(len(data_frame_main))
        
        return data_frame_new
        
    def check_data_types_are_dictornary_typed(self, dataframe = None):
        """
        Check if the dataframes are comming from an dictonary or match to the Pandas.cor.Series.Serie - 
        the data that comes from 

        Parameters
        ----------
        dataframe : TYPE, optional
            DESCRIPTION. The default is None.

        Returns
        -------
        bool
            DESCRIPTION.

        """
        
        if isinstance(dataframe , pd.core.series.Series ):
            return True
        else:
            return False
        
    def check_types_data_are_valide(self, varible_one = None, varible_two = None):
        """
        Checks if the dataframes are not None_Type

        Parameters
        ----------
        varible_one : TYPE, optional
            DESCRIPTION. The default is None.
        varible_two : TYPE, optional
            DESCRIPTION. The default is None.

        Returns
        -------
        bool
            DESCRIPTION.

        """
        if type(varible_one) != None and type(varible_two) != None:
            return True
        else:
            return False
    
    def egalize_the_data(main_data, data_two):
        """
        Egalzies the data

        Parameters
        ----------
        main_data : TYPE
            DESCRIPTION.
        data_two : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """ 
        
        return data_two.tail(len())
        
    def check_if_main_is_longer(data_main , data_two):
        """
        Returns true if main data is longer. 

        Parameters
        ----------
        data_main : TYPE
            DESCRIPTION.
        data_two : TYPE
            DESCRIPTION.

        Returns
        -------
        bool
            DESCRIPTION.

        """
        if len(data_main) < len(data_two):
            return False
        else:
            return True 
        
    def check_lenght_valide( drop_rate = None, data_two = None):
        """
        Check if the length is valide. 

        Parameters
        ----------
        drop_rate : TYPE, optional
            DESCRIPTION. The default is None.
        data_two : TYPE, optional
            DESCRIPTION. The default is None.

        Returns
        -------
        bool
            DESCRIPTION.

        """
        
        # if Droprate is None return true - no tail needed.
        if type(drop_rate) == None or drop_rate == 0:
            
            return True
        
        elif len(data_two) >= drop_rate:
            
            return True
        
        elif type(drop_rate) != None and len(data_two) < drop_rate:
            return False
        # if tail is activated, tail the data the amount of the droprate. 
        else:
            raise Exception("There was a logical error in CheckVarible lenght, merge_support_functions")


class mother_data_object:
    """
    19-10-2021              : Today we added a clean function
                            ToDo - Add an mother_anaalyess analyses object. This already added in sector analyses but good to have around.
                            ToDo - Make a mental prepair for exchanges - tickers that belong to an exchange. Easy Just a dict with tickers from a text file, and a list of exchanges. Done Downlaod them on EOD data. done.
    """
    
    
    
    # gets list of sectors
    sectors     : list = list 
    # gets list of industy's
    industry    : list = list
    # gets list of tickers
    tickers     : list = list
    # gets dict of all data 
    main_dict   : dict = dict
    
    
    def __init__(self):
        
        raise Exception("ERROR, DONT USE THIS CLASS")
        # gets the motherobject( stock ticker and industrty's ) 
        synch_object    =   synch_class.data_synch(subfolder="Main_Data",ticker = "mother_object", data_extention = ".mother_data")
        
        # gets stock object. 
        stocks_mother_object = synch_object.retreived_data
        
        # retreives main dict 
        self.main_dict = stocks_mother_object
        
        # gets stock tickers
        synch_object    =   synch_class.data_synch(subfolder="Main_Data",ticker = "stock_tickers", data_extention = ".mother_data")
        
        # sets stocktickers 
        stock_tickers   =   synch_object.retreived_data
        
        # sets sectos
        self.sectors    =   list(stocks_mother_object["sector"].keys())
        
        # cleans the list 
        self.sectors    =   self.clean_lists( list_in = self.sectors )
        
        # sets industry's
        self.industry   =  list(stocks_mother_object["industry"].keys()) 
        
        # cleans the list
        self.industry   =  self.clean_lists( list_in = self.industry)
        
        # sets tickers
        self.tickers    =   list(stock_tickers.keys())
        
        # cleans the list
        self.tickers    =   self.clean_lists( list_in = self.tickers)
        
        # sets list of avalible analyses
        main_stock_analyses         =    stock_analyses.main_analyeses(easy_load = True)
        
        # sets avalible analyses
        self.available_analyses     =    main_stock_analyses.analyses_names
        
        # sets avalible atributes
        self.available_analyses_atributes   =   main_stock_analyses.atributes_analyeses
        
        
if __name__ == "__main__":    
    
    try:
        
        global sector_and_industy_analyesses
        sector_and_industy_analyesses = sector_analyse()
        
         
        # 
        x = sector_and_industy_analyesses
        
        # 
        #global p
        #p = database_querys_main.database_querys.get_all_stocks_with_industry(x.industry[130])
        
        # 
        x.injected_tickers = ["DIBS", "MORF", "OSCR", "AAPL"]
        
        # 
        x.use_injected_tickers = True
        global analyses_
        analyses_ = x.create_industy_or_sector_analyses(use_injected_tickers= True, sub_atribute_analyses="indicator_timeserie_profile", average_out=True)
        
    except Exception as e:
        
        raise Exception("Error with tickers", e)

                
                
                
                
        
        
        