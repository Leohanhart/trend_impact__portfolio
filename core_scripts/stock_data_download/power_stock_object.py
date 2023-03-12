# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 09:42:53 2021

@author: Gebruiker
"""

# For the mother object: symbols list is the keyword for the action: https://eodhistoricaldata.com/pricing has on this link the function https://eodhistoricaldata.com/financial-apis/exchanges-api-list-of-tickers-and-trading-hours/

"""

Waar zitten we in? 

We zijn een middle class aan het bouwen : de power stock analyses, die gebruik maakt van de stock analyeses refactord.
in deze class worden de itmes prepaird en gereturnd. 

Taken. 
- Er moet een data inlow moduklle komen die er voornamelijk op gebaseerd is om data the laden

    Done, 


- Het is belangrijk dat er vooraf wordt nagedacht over hoe de class gebruik gaat maken van externe classen
- de data komt in een lijst of een array. 

"""

"""
Belangrijke mededeling: Yahoo finance API is een en al aan de ziekte overgedragen. 
Dat betekend dat je een patch moet instaleren, een fix voor een multi thread probleem. https://pypi.org/project/fix-yahoo-finance/
hier verklaard : https://stackoverflow.com/questions/68218506/did-yfinance-and-yahoo-fin-for-python-stop-working-recently


"""


"""
Taak 1. Zorgen dat de opgeslagen wordt. 
"""




import constants
import os
from core_scripts.synchronization import synch_class
from core_scripts.stock_data_download import power_stock_object_support_functions as support_functions
from core_scripts.stock_data_download import stockobject_supporting_functions as old_supporting_functions
from core_scripts.stock_analyses import old_stock_analyses as stock_analyses
import pandas as pd
class power_stock_object:
    """
    Power stock object. 
    """

    # controls
    # this is the amount of days between the last refresh. This is maily intresseting for dividend data. or shortratio data.
    control_days_for_refresh = 14

    # type of object
    type_of_object = "POWER"

    # technical
    first_run = False
    synch_object = None
    bool_allowd_to_run = True

    # fundamental
    stock_ticker = None

    # logbook.
    log_book_messages = []

    # analyses options selected:
    analyses_selected = ["last_calculation_profile_indicator_text",
                         "last_calculation_profile_change_text"]

    # rack_analyses:
    data_object = None  # storeage for al the data retreived form yahoo.

    # dictonary
    analyses_dict = {}

    # time serie data
    stock_data = None

    # company info
    company_ticker = ""
    sector = ""
    industry = ""

    # financials
    free_float = ""
    market_cap = ""
    dividends = ""
    book_value = ""
    short_ratio = ""
    cash_per_share = ""

    all_stock_data = ""

    # discounts
    future_fair_value_including_dividends = ""
    future_fair_discount = ""

    def __init__(self,

                 # stock ticer
                 stock_ticker: str = None,

                 # fastload, for fasterloading
                 fast_load: bool = False,

                 # simplyfiedload, only load nessary data.
                 simplyfied_load: bool = True,

                 # converts stock data to weekly data, used for analyses. So they can easely been done.
                 periode_weekly: bool = False,

                 # analyses modus, means that only the stockdata is loaded so it can be used for analyses.
                 analyeses_modus: bool = False):
        """ 
                 # stock ticer
                 stock_ticker       : str  = None, 

                 # fastload, for fasterloading
                 fast_load          : bool = False, 

                 # simplyfiedload, only load nessary data.
                 simplyfied_load    : bool = False, 

                 # converts stock data to weekly data, used for analyses. So they can easely been done.
                 periode_weekly     : bool = False, 

                 # analyses modus, means that only the stockdata is loaded so it can be used for analyses. 
                 analyeses_modus    : bool = False):
        """

        # print("Startup")

        #
        # check if the ticker is empty.
        if stock_ticker == None:
            print(1)
            #
            # blocks the object so it cant damage the system
            self.bool_allowd_to_run == False
            #
            raise Exception("Ticker is None")

        else:

            #
            # sets the stock ticker
            self.stock_ticker = stock_ticker

        if type(periode_weekly) != bool:

            raise Exception("Data is new. No data possible")

        # startup the power_stock_object
        self.__startup()

        # check the last update with the intention to flag if the system is ready to load or needs to be initalized
        #
        # loads the synch object

        #
        # sets the ticker

        try:

            self.synch_object = synch_class.data_synch(
                path=constants.CORE_DATA_____PATH, subfolder="stock_data",
                ticker=stock_ticker,
                data_extention="last_download_company_data_refresh",
                raise_error_if_found=True)

        except FileNotFoundError:

            print("I have cancer under controll.")
            # self.__first_run()

            # step one, new synch object (Maar er wordt nu een error getrowd.)
            self.synch_object = synch_class.data_synch(
                path=constants.CORE_DATA_____PATH, subfolder="stock_data",
                ticker=stock_ticker,
                data_extention="last_download_company_data_refresh",
                raise_error_if_found=False)

            # set two,
            self.reset_stock_data_experiment()
            self.save_new_data()

            return
            # hier moet een modules komen die A een last download variablen maakt en de data download en goed opslaat.

            self.save_new_data()

        self.synch_object.ticker = stock_ticker

        #
        # loads the data object
        self.synch_object.load_data()

        # Analyses modus, weekly
        #
        #
        if analyeses_modus and periode_weekly and not self.synch_object.is_data_new:

            #
            # load stock data
            self.load_stock_data(load_data_for_weekly=True)

            self.catch_error(self.stock_data)

            return

        # FAST BOOT MODUS / fast_load
        #
        # if fastmodus is on than only load the stock_data.
        elif fast_load != None and fast_load == True and self.synch_object.is_data_new != True:

            #
            # load stock.
            self.load_stock_data(load_data_for_weekly=periode_weekly)

            self.catch_error(self.stock_data)

            return

        # SYMPLIFIED BOOT / simplyfied_load
        #
        # there is an
        elif simplyfied_load != None and simplyfied_load == True and self.synch_object.is_data_new != True:

            #
            # if the cursor gets here then we are quite sure that the data is boot modus is simplyfied.
            # in that case we only load the stockdata

            #
            # first downloads the stock.
            self.load_stock_data(load_data_for_weekly=periode_weekly)

            # declare dataobject.
            # sets up the synch handler
            synch_handler = support_functions.handle_data_synch(
                self.synch_object)

            #
            # loads sector information
            self.sector = synch_handler.load_data_varible("sector")
            #
            # industrial details.
            self.industry = synch_handler.load_data_varible("industry")
            #
            # exchange

            self.catch_error(self.stock_data)

            return

        # turns on if class is not intalized before so everthing needs to be prepaired and saved.
        elif self.synch_object.is_data_new == True:

            if 0 == 0:
                pass
            # does the first run for the program. creates datafiles, does analyeses.
            self.__first_run()

        # startsup the regulair program
        else:

            #
            # check the dates of the last downlaod.
            last_data_refresh_date = self.synch_object.retreived_data
            #
            # loads the experition manager to conclude if there needs to be a second run.
            ex_manager = support_functions.experation_manager()
            #
            # checks the amount of is anouch to restart the boot.
            dates_between = ex_manager.days_between(last_data_refresh_date)

            # does the checking.
            if dates_between >= self.control_days_for_refresh:
                #

                # if this section is sparked it will generate new data files
                self.save_new_data()

        # starts the normal proces
        if self.synch_object.is_data_new == False:

            #
            # this section is sparked when the data needs to be rebooted.
            last_date = self.synch_object.retreived_data

            #
            # loads the data.
            self.load_data(periode_weekly=periode_weekly)

            self.catch_error(self.stock_data)

        self.catch_error(self.stock_data)

    def __del__(self):
        """


        Returns
        -------
        None.

        """
        # saves tha last data program.
        synch_handler = support_functions.handle_data_synch(self.synch_object)

    def __startup(self):
        """
        Starts up the data

        Returns
        -------
        None.

        """
        # this funtion is preset for the time that stock objects will run for there selvs.

    def __first_run(self):
        """
        This big porpose of this class is that it saves all the retreived data for the first time. 

        This is a function that's used if the class runs for the first time with this ticker
        - it sets the start date.
        - it clears the log. 
        - its good. 

        Returns
        -------
        None.

        """
        # saves the new data for the next time.
        self.save_new_data()

    def catch_error(self, data):

        if(callable(data)):
            print("Shooted the big error out of the sky.")
            self.__first_run()
            return

    def reset_stock_data_experiment(self):

        synch_handler = support_functions.handle_data_synch(self.synch_object)

        # retreive the data from yahoo.
        datesupport = support_functions.experation_manager()

        # retreives the last date so that we know what whent wrong.
        self.last_date_saved = datesupport.return_last_date_object()

        # dowload stockdata
        stock_dowload_object = old_supporting_functions.download_stock(
            self.stock_ticker)

        # Download stock.
        stock_dowload_object.dowloadStock()

        # set date
        self.stock_data = stock_dowload_object.Stock_Data

        # save the data.
        synch_handler.save_data_varible(
            self.stock_data, "stock_timeserie_data")

        # proveds the date. this is the last time that the object is used. After that it will be a ((cop))pie
        synch_handler.save_data_varible(
            self.last_date_saved, "last_download_company_timeserie_data_refresh")

        # proveds the date. this is the last time that the object is used. After that it will be a coppie
        synch_handler.save_data_varible(
            self.last_date_saved, "last_download_company_data_refresh")

        # this is not important but needed. otherwise progran is gonna cry.
        # company info
        self.company_ticker = self.stock_ticker
        self.sector = "Unkown"
        self.industry = "Unkown"

        #
        # financials
        self.free_float = "Unkown"
        self.market_cap = "Unkown"
        self.dividends = "Unkown"
        self.book_value = "Unkown"
        self.short_ratio = "Unkown"

        #
        # discount calculations
        self.cash_per_share = "Unkown"
        self.future_fair = "Unkown"
        self.future_fair_discount = "Unkown"

        #
        # dict with all the data.
        self.all_stock_data = "Unkown"

        synch_handler.save_data_varible(
            self.all_stock_data, "all_stock_data")

        # starts saving the data
        synch_handler.save_data_varible(self.free_float, "Free_Float")
        synch_handler.save_data_varible(self.market_cap, "Market_cap")
        synch_handler.save_data_varible(self.dividends, "Dividends",)
        synch_handler.save_data_varible(self.book_value, "Book_Value")
        synch_handler.save_data_varible(self.short_ratio, "Short_Ratio")

        #
        # the discounts
        synch_handler.save_data_varible(
            self.cash_per_share, "cash_per_share")
        synch_handler.save_data_varible(self.future_fair, "future_fair")
        synch_handler.save_data_varible(
            self.future_fair_discount, "future_fair_discount")

        #
        # fundamental details.
        synch_handler.save_data_varible(self.sector, "sector")
        synch_handler.save_data_varible(self.industry, "industry")

        return

    def load_data(self, periode_weekly: bool = None):

        # this annouces that the stock is found and that it can be pushed
        print("file extists. shit should load.")
        #
        # loads the new stock information - like the fundamentals
        self.load_new_stock_info_data()
        #
        # loads the new stock data.
        self.load_stock_data(load_data_for_weekly=periode_weekly)

    def load_new_stock_info_data(self):
        """
        Loads the data. 

        Returns
        -------
        None.

        """
        #
        # sets up the synch handler
        synch_handler = support_functions.handle_data_synch(self.synch_object)

        #
        # loads alll the data
        #self.all_stock_data = synch_handler.load_data_varible("all_stock_data")

        #
        # loads the sector that is retreived
        self.sector = synch_handler.load_data_varible("sector")
        #
        # loads the market capp data.
        self.market_cap = synch_handler.load_data_varible("Market_cap")
        #
        # loads the dividend
        self.dividends = synch_handler.load_data_varible("Dividends",)
        #
        # loads the bookvalue
        self.book_value = synch_handler.load_data_varible("Book_Value")
        #
        # loads the short ratio
        self.short_ratio = synch_handler.load_data_varible("Short_Ratio")
        #
        # loads the free_float
        self.free_float = synch_handler.load_data_varible("Free_Float")
        #
        # industrial details.
        self.industry = synch_handler.load_data_varible("industry")
        #
        # loads future fair value
        self.cash_per_share = synch_handler.load_data_varible("cash_per_share")
        #
        # loads cash per share.
        self.future_fair_value_including_dividends = synch_handler.load_data_varible(
            "future_fair")
        #
        # loads discount on fair.
        self.future_fair_discount = synch_handler.load_data_varible(
            "future_fair_discount")

    def load_stock_data(self,
                        # is creaded so you can test the refresh methode
                        ignore_last_refresh_date: bool = False,
                        # is creaded for analyses modus, runs on the weekly
                        load_data_for_weekly: bool = False
                        ):

        # short explenation
        # knows how to download stockdata.
        # checks if there is already an download attempt done today. if not. it downloads the stock data.
        # else it just loads the stock data.

        # print("Hi")
        # print(self.synch_object.Full__filename)

        #
        # dowload the last date that the stockdata was downloaded.
        synch_handler = support_functions.handle_data_synch(self.synch_object)

        #print("Synch handler 1",synch_handler.synch_object.Full__filename)
        #
        # loads the last date
        last_stock_download = synch_handler.load_data_varible(
            "last_download_company_timeserie_data_refresh")
        #
        # retreives the last data
        date_support = support_functions.experation_manager()
        #
        # check the amount of dats
        amount_of_dates = date_support.days_between(last_stock_download)

        #print("Synch handler 2",synch_handler.synch_object.Full__filename)
        # print(self.synch_object.Full__filename)
        #
        #

        #
        # loads stock and converts it to weekly data.
        if load_data_for_weekly and not date_support.return_true_if_weekly_expired(last_stock_download):

            self.stock_data = synch_handler.load_data_varible(
                "stock_timeserie_data")

            try:

                if not isinstance(self.stock_data, pd.core.frame.DataFrame):

                    raise Exception(
                        "Error, booted synch object is not equal pandas dataframe type", "powerstockobject, ")

                elif ['Date',
                      'Open',
                      'High',
                      'Low',
                      'Close',
                      'Adj Close',
                      'Volume',
                      'Change'] != list(self.stock_data.columns):

                    raise Exception(
                        "Error, booted synch object is not matching column names", "powerstockobject, ")

                else:

                    convertion_object = support_functions.time_conversion(
                        stock_data=self.stock_data)
                    self.stock_data = convertion_object.weekly_stock_data

                    self.catch_error(self.stock_data)
                    return
                    # convert the data

            except Exception as Error:
                print(len(Error.args))

        #
        # if the date is not equal to 0, it means that the data is expired. Even in the weekends or in holydays.
        if amount_of_dates != 0 or ignore_last_refresh_date == True:

            #print("Stock data is loaded")
            #
            # sets up a stock download object
            stock_dowload_object = old_supporting_functions.download_stock(
                self.stock_ticker)
            #
            # Download stock.
            stock_dowload_object.dowloadStock()
            #

            # set date
            self.stock_data = stock_dowload_object.Stock_Data

            #
            # orgainzes a sycnh handler
            synch_handler.save_data_varible(
                self.stock_data, "stock_timeserie_data")
            #
            # retrieves the current date
            current_date = date_support.return_last_date_object()
            #
            # pushes the last date of the download that has taking place.
            synch_handler.save_data_varible(
                current_date, "last_download_company_timeserie_data_refresh")

            if load_data_for_weekly:

                convertion_object = support_functions.time_conversion(
                    stock_data=self.stock_data)
                self.stock_data = convertion_object.weekly_stock_data

        # if there is no experation, just download the stock.
        else:

            #
            # loads the stocks
            self.stock_data = synch_handler.load_data_varible(
                "stock_timeserie_data")
            return

    def load_anlyses_first_time(self):
        """
        Loads the Analyses for the first time. 

        Returns
        -------
        None.

        """

        # creates synch object.
        synch_handler = support_functions.handle_data_synch(self.synch_object)

    def load_anlyses(self):
        #
        # uses extrenal class how cleans the analyses code. It returns NAMES and TIMESERIES. Q1: Where does the data analyses module jumps in.
        synch_handler = support_functions.handle_data_synch(self.synch_object)

    def save_new_data(self):
        """

        Saves new downlaoded data. It also works as load the first time.

        Returns
        -------
        None.

        """

        if 0 == 0:
            pass

        # declare dataobject.
        self.data_object = support_functions.load_company_data_yahoo(
            self.stock_ticker)

        # declare datasynch object.
        synch_handler = support_functions.handle_data_synch(self.synch_object)

        if 0 == 0:
            pass

        # check if the data is loaded without error.
        if self.data_object.error_code != None:

            self.bool_allowd_to_run = False

        # if the data is loaded without error it can be parsed.
        else:

            # loads the data.
            self.data_object.load_data()

            #
            # company info
            self.company_ticker = self.data_object.company_ticker
            self.sector = self.data_object.sector
            self.industry = self.data_object.industry

            #
            # financials
            self.free_float = self.data_object.free_float
            self.market_cap = self.data_object.market_cap
            self.dividends = self.data_object.dividends
            self.book_value = self.data_object.book_value
            self.short_ratio = self.data_object.short_ratio

            #
            # discount calculations
            self.cash_per_share = self.data_object.cash_per_share
            self.future_fair = self.data_object.future_fair_value_including_dividends
            self.future_fair_discount = self.data_object.future_price_discount

            #
            # dict with all the data.
            self.all_stock_data = self.data_object.data_object

            if 0 == 0:
                pass

            self.synch_object.new_data = self.all_stock_data
            self.synch_object.new_data

            synch_handler.save_data_varible(
                self.all_stock_data, "all_stock_data")

            if 0 == 0:
                pass

            # starts saving the data
            synch_handler.save_data_varible(self.free_float, "Free_Float")
            synch_handler.save_data_varible(self.market_cap, "Market_cap")
            synch_handler.save_data_varible(self.dividends, "Dividends",)
            synch_handler.save_data_varible(self.book_value, "Book_Value")
            synch_handler.save_data_varible(self.short_ratio, "Short_Ratio")

            #
            # the discounts
            synch_handler.save_data_varible(
                self.cash_per_share, "cash_per_share")
            synch_handler.save_data_varible(self.future_fair, "future_fair")
            synch_handler.save_data_varible(
                self.future_fair_discount, "future_fair_discount")

            #
            # fundamental details.
            synch_handler.save_data_varible(self.sector, "sector")
            synch_handler.save_data_varible(self.industry, "industry")

            # retreive the data from yahoo.
            datesupport = support_functions.experation_manager()

            # retreives the last date so that we know what whent wrong.
            self.last_date_saved = datesupport.return_last_date_object()

            # dowload stockdata
            stock_dowload_object = old_supporting_functions.download_stock(
                self.company_ticker)

            # Download stock.
            stock_dowload_object.dowloadStock()

            # set date
            self.stock_data = stock_dowload_object.Stock_Data

            # save the data.
            synch_handler.save_data_varible(
                self.stock_data, "stock_timeserie_data")

            # proveds the date. this is the last time that the object is used. After that it will be a ((cop))pie
            synch_handler.save_data_varible(
                self.last_date_saved, "last_download_company_timeserie_data_refresh")

            # proveds the date. this is the last time that the object is used. After that it will be a coppie
            synch_handler.save_data_varible(
                self.last_date_saved, "last_download_company_data_refresh")

            if 0 == 0:
                pass

            # report to logbook
            text_for_logbook = "Ticker = " + self.stock_ticker + \
                " started up at : " + self.last_date_saved
            self.report_to_the_logbook(text=text_for_logbook)

            # checks if there is an error saving the data.
            if self.synch_object.error_code == 1:
                self.bool_allowd_to_run = False

            if 0 == 0:
                pass

        # updates the new data.

    def report_to_the_logbook(self, text=None, read_logbook=False):

        # check if the data is filled and read is not turend on
        if text != None and read_logbook == False:

            # adds the logbook
            self.log_book_messages.append(text)

            # coppies the writer calss.
            syncher = self.synch_object
            syncher.data_extention = "LOGBOOK"
            syncher.refresh_object()
            syncher.overwrite_data()

        elif read_logbook == True:

            syncher = self.synch_object
            syncher.data_extention = "LOGBOOK"
            syncher.load_data()

            logbook = syncher.retreived_data

            if type(logbook) == list:
                for i in range(0, len(logbook)):
                    print(logbook[i])

    def save_files(self):
        pass

    def twitter_module(self, full_test_function=False):
        # if analyses is good. Tweet. (Link to picture, analyses name, GAPH) Tweet backtest of the signal.
        # also the forecasts. This can be done in thread. It depends on the analses. Forecasts are always
        # Posted if consider not normal.
        #

        #
        # creates data convertion object.
        data_convertion_object = support_functions.time_conversion(
            stock_data=self.stock_data)

        #
        # creates loop that loops true the converted data.
        for i in range(0, len(data_convertion_object.time_frames)):

            #
            # selectes the data in the converted object.
            data_for_analyeses = data_convertion_object.time_frames[list(
                data_convertion_object.time_frames.keys())[i]]

            #
            # creates the main object analyeses object, this one is used to load the analyeses.
            main_object = stock_analyses.main_analyeses(stock_ticker=self.stock_ticker,
                                                        stock_data=data_for_analyeses,
                                                        synchronize=False,
                                                        tailing_data=True,
                                                        timeframe=list(
                                                            data_convertion_object.time_frames.keys())[i]
                                                        )

            #
            # loads the name of the object analyeses
            analyses = main_object.analyses_names

            #
            # loop true analyses.
            for x in range(0, len(analyses)):

                #
                # loads the analyses
                main_object.load_analyese(analyses[x])

                global new_analyses
                #
                # sets the analyses
                new_analyses = main_object.analyeses_dictionary

                #
                # generate name for the data extention
                #
                # selects name of analyeses
                name_of_analyses = analyses[x]
                #
                # selects the timeframe name
                timeframe_of_analyses = list(
                    data_convertion_object.time_frames.keys())[i]
                #
                #
                extention_of_dict = name_of_analyses + "_" + timeframe_of_analyses
                ##

                #
                # loads old analyses.
                synch_object = synch_class.data_synch(
                    subfolder="Data_Folder", ticker=self.stock_ticker, data_extention=extention_of_dict)
                #
                # turns on if class is not intalized before so everthing needs to be prepaired and saved.
                if synch_object.is_data_new == True:

                    #
                    # if data is new, add new data and save data
                    synch_object.new_data = new_analyses
                    synch_object.save_data()

                    continue

                else:

                    # load old data
                    old_analyses = synch_object.retreived_data

                    #
                    # voor iedere analyses moet je nu kijken of het verschild.
                    for y in range(0, len(self.analyses_selected)):

                        #
                        # here is the old score set.
                        old_score = old_analyses[self.analyses_selected[y]]

                        #
                        # here is the new score set.
                        new_score = new_analyses[self.analyses_selected[y]]

                        # trigger is hit
                        if new_score != old_score or full_test_function == True:

                            # generate twitter text
                            text_generator = stock_analyses.twitter_text_generator(name_of_analyeses=analyses[x],

                                                                                   # this is the ticker name.
                                                                                   ticker_name=self.stock_ticker,
                                                                                   # this is the new recoomandtion
                                                                                   new_recommendation=new_score,
                                                                                   # this is the old recommendation
                                                                                   old_recommendation=old_score,
                                                                                   # this input is for example: News, opionus
                                                                                   text_input=None,
                                                                                   # this is the time frame : Weekly/daily/monthly
                                                                                   time_frame=list(
                                                                                       data_convertion_object.time_frames.keys())[i],
                                                                                   occation="CHANGE_PROFILE",         # this is the occation


                                                                                   )

                            print(y)
                            print("\n\n The twitter text is generated man")
                            # load twitter text.
                            text_generator.construct_analyses_texts()
                            twitter_text = text_generator.twitter_text_full
                            print(
                                "\n\n The twitter text is already generated man and isfinished")

                            print("// NU zijn we hier")

                            # load picture of plot
                            twitter_plot = stock_analyses.plot_generator(

                                data=None,             # data of the analyeses

                                analyeses_dictionary=new_analyses,   # analyeses data
                                # name of analyes
                                name_of_analyeses=analyses[x],
                                ticker_name=self.stock_ticker,            # ticker name
                                timeframe=list(data_convertion_object.time_frames.keys())[
                                    i],              # quite unimportantand
                                name_of_data=None,           # tile of the data
                                type_of_data=None,

                            )

                            # retreives the path for the picture
                            path_picture = twitter_plot.generate_change_profile_plot()

                            # create twitter object.

                            twitter_object = stock_analyses.twitter_module()

                            # send tweet
                            twitter_object.post_tweet(
                                twitter_text, path_picture)

                            # You need to change that if the analyses is used the twitter module changes adds
                            # the name of the analyses in class, so you can used that for your title.
                            # also there needs to be a class that returns the normal name, for hard
                            # analyses names, so LIQUIDT returns as liquidity, and the first plot is always, raw,
                            # second always profiles.

                        if y == len(self.analyses_selected):
                            synch_object.synchronized_data = new_analyses

    # you can test this module by not saving the change and manualy changing the data. or trigger

    def main_thread(self):
        pass
        # wait for new day, do analyses, forecasts, ect. #@ this can be done multi threaded, or just single threaded.


if __name__ == "__main__":

    try:

        power_stock_apple = power_stock_object("BABA")

    except Exception as e:

        raise Exception("Problem with the stockticker", e)
