# -*- coding: utf-8 -*-
"""
Created on Fri Jun 25 17:51:00 2021

@author: Gebruiker
"""

import math as math
from core_scripts.synchronization import synch_class
import pandas as pd
import os

from dateutil.parser import parse
from matplotlib.offsetbox import OffsetImage

from core_scripts.stock_data_download import (
    power_stock_object_support_functions as support_functions,
)
import constants
import numpy as np
from datetime import datetime

# import power_stock_object as power_object
import warnings
import time
from datetime import datetime

import tweepy

import constants


""" 
Kort logboek

     - functie moet werken met een tail functie in de profiled level ding. 
     oplossing is de liquidity data tailen en verpakken in de speciale liquidity data
     voor de profiliereing
     - mijn idee om een tail functie te maken. Die dan de oude data laad voor het profieleren. 
     
     
     # problemen 
     1. bij de recovery ontstaat er bij mij wat onduidelijkheid over wat er pricies 
     met de nieuwe data gedaan wordt. 
     
     test 
     - de profiler
     - de recoverty
     
     14-02: Vandaag ga ik verder met de het ophalen en synchen van de data. Ik gebruik hiervoor de setup_envoirment
     29-04-22: Vandaag zijn de paden van de analyses aangepast.
     - Moneyflows, liquidityimpact.

"""


class main_analyeses:
    """


    How to work with the analyeses dictonairy?

    1. accessible items

    "indicator_timeserie_change"

    "indicator_timeserie_profile_change"

    "indicator_timeserie_profile"

    "indicator_timeserie_raw"

    "last_calculation_profile_indicator_number"

    "last_calculation_profile_change_text"

    "last_calculation_profile_change_number"

    "last_calculation_profile_indicator_text"

    "last_calculation_indicator"


    step 1. creat an main_analyses object with the stock data in the class. ( remember, the data needs to be converted to the timeframe of choice matching to the class)

    step 2. load the avalible analyeses. with object.analyses_names

    """

    # stockdata details.
    stock_ticker = None
    stock_data = None
    timeframe = None

    # name of avalible analyses
    analyses_names = ["MONEYFLOWS", "LIQUIDTY"]

    # name of atributes analyses
    atributes_analyeses = [
        "indicator_timeserie_change",
        "indicator_timeserie_profile_change",
        "indicator_timeserie_profile",
        "indicator_timeserie_raw",
        "last_calculation_profile_indicator_number",
        "last_calculation_profile_change_text",
        "last_calculation_profile_change_number",
        "last_calculation_profile_indicator_text",
        "last_calculation_indicator",
    ]

    # data dictionary
    analyeses_dictionary = {}

    # synchronize
    synchronize: bool = True

    use_automatic_time = (
        True  # can be used to help set profiles easy. If turend off ignored.
    )

    def __init__(
        self,
        stock_ticker="AAPL",
        stock_data=None,  # this is the parameter for the stock_data
        synchronize=False,  # this is the parameter for optional synchroinzation (not pluged in)
        tailing_data=False,  # this is parametering for tailing the data          (this is done to spead up the proces)
        timeframe="D = daily, W = Weekly, M = montly, Q = quarterly, Y = yearly",
        easy_load=False,
    ):
        """


        Parameters
        ----------
        stock_ticker : TYPE, optional
            DESCRIPTION. The default is "AAPL".
        stock_data : TYPE, optional
            DESCRIPTION. The default is None.
        # this is the parameter for the stock_data                 synchronize : TYPE, optional
            DESCRIPTION. The default is False.
        # this is the parameter for optional synchroinzation (not pluged in)                 tailing_data : TYPE, optional
            DESCRIPTION. The default is False.
        # this is parametering for tailing the data          (this is done to spead up the proces)                 timeframe : TYPE, optional
            DESCRIPTION. The default is "D = daily, W = Weekly, M = montly, Q = quarterly, Y = yearly".
        easy_load : TYPE, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        None.

        """
        # if only gets loaded if they only need the name of the avalible analayses
        if easy_load:
            return

        # check if none-type first methode.
        if type(stock_data) == None:
            return

        # check if none-type second methode.
        if stock_data is None:
            return

        # sets system varibles
        self.stock_data = stock_data
        #
        # sets ticker ovject
        self.stock_ticker = stock_ticker

        #
        # set synchronization
        self.synchronize = synchronize

        #
        # check if time frame is filled in well
        if (
            timeframe
            == "D = daily, W = Weekly, M = montly, Q = quarterly, Y = yearly"
        ):
            #
            # if it fails it marks it down as non
            self.timeframe = None
            #
            # if timeframe is filled in, it needs to be assinged.

        # sets the timeframe
        elif (
            timeframe == "Daily"
            or timeframe == "D"
            or timeframe == "Weekly"  # checks the daily  data
            or timeframe == "W"
            or timeframe == "Monthly"  # checks the weekly data
            or timeframe == "M"
            or timeframe == "Yearly"  # checks the montly data
            or timeframe == "Y"
            or timeframe == "Quarterly"  # checks the yearly data
            or timeframe == "Q"  # checks the quater data
        ):

            #
            # sets the daily timeframe
            if timeframe == "Daily" or timeframe == "D":

                self.timeframe = "D"

                if tailing_data == True:

                    self.stock_data = stock_data.tail(502)

                return

            # sets the weekly timeframe
            if timeframe == "Weekly" or timeframe == "W":

                self.timeframe = "W"

                if tailing_data == True:

                    self.stock_data = stock_data.tail(104)

                return

            # sets the Monthly timeframe
            if timeframe == "Monthly" or timeframe == "M":

                self.timeframe = "M"

                if tailing_data == True:

                    self.stock_data = stock_data.tail(24)

                return

            # sets the monthly data
            if timeframe == "Yearly" or timeframe == "Y":

                self.timeframe = "Y"

                if tailing_data == True:

                    self.stock_data = stock_data.tail(10)

                return

            # sets the quartlydata
            if timeframe == "Quarterly" or timeframe == "Q":

                self.timeframe = "Q"

                if tailing_data == True:

                    self.stock_data = stock_data.tail(16)

                return

        else:
            #
            # sets the timeframe to non
            self.timeframe = None

    def load_analyese(self, title_analyses=None):
        """
        Loads analyses

        Parameters
        ----------
        title_analyses : TYPE, optional
            DESCRIPTION. The default is None.

        Returns
        -------
        None.

        """

        #
        # check if names are in the thing.
        if title_analyses != None and title_analyses in self.analyses_names:

            # if moneyflow analyeses is hit
            if title_analyses == "MONEYFLOWS":

                # boots moneyflow object
                moneyflow_analyses = money_flows(
                    stock_ticker=self.stock_ticker,
                    synchronize=self.synchronize,
                    stock_data=self.stock_data,
                    timeframe=self.timeframe,
                )
                # loads analyses in dict object
                # moneyflow_analyses.money_flow_analyeses(full_run = True)
                # sets dict object ass main object.
                self.analyeses_dictionary = (
                    moneyflow_analyses.analyeses_dictionary
                )

            # if the liquidty analyeses is hit.
            if title_analyses == "LIQUIDTY":

                #
                # boots the liquidty analyses
                liquidity_analyeses = liquidity_impact(
                    stock_ticker=self.stock_ticker,
                    stock_data=self.stock_data,
                    synchronize=self.synchronize,
                    timeframe=self.timeframe,
                )
                #
                # runs the full liquidity analyses
                # liquidity_analyeses.liquidity_impact_analyeses(full_run = True)
                #
                # adds the dict object to the analyeses.
                self.analyeses_dictionary = (
                    liquidity_analyeses.analyeses_dictionary
                )


class profiling:
    """
    This class is made for profiling

    """

    # data
    stock_data = None

    def __init__(
        self,
        stock_ticker="",
        stock_data=None,
        synchronize=False,
        timeframe="D = daily, W = Weekly, M = montly, Q = quarterly, Y = yearly",
    ):

        self.stock_data = stock_data
        self.timeframe = timeframe

    def return__profile(
        self,
        data=None,
        test_function=False,
        length_for_calculation=0,
        return_outcome_as_number=False,
        based_on_change=False,
        automatic_use_time_standards=True,
    ):

        # global ts
        #
        # sets time serie data
        ts = data
        # print(ts)
        # print("\n\n this is the incomming len", len(ts))

        if 0 == 0:
            pass
        ###### Converts the data to data of change or melts the data to the timeframe of wish. #############################################################################
        #
        #
        # packages the data in dataframe
        df_ts = self.convert_data_to_dataframe(data=ts)

        #
        # for test function
        if test_function:
            print(
                "in profiler function the timeseries is converted to dataframe"
            )
        #
        # checks if it based on change
        if based_on_change == True:
            #
            # for test function
            if test_function:
                print(
                    "in profiler function the timeseries is converted to changed time serie"
                )

            list_for_calculation = data
            #
            # remove 0 in case it doenst work
            list_for_calculation = [
                i if i != 0 else 0.01 for i in list_for_calculation
            ]
            #
            # does the calculations nanual
            list_for_convertation = [
                a1 - a2
                for a1, a2 in zip(
                    list_for_calculation[1:], list_for_calculation
                )
            ]
            #
            # round the numbers.
            list_for_convertation = [
                round(num, 2) for num in list_for_convertation
            ]
            #
            # convert the session.
            df_ts = self.convert_data_to_dataframe(data=ts)
            #
            # changes the data frame in dataframe of change
            # df_ts = df_ts.pct_change()
        #
        # checks if the data needs to be tailed by date, only possible if not turend of and commanded
        if (
            automatic_use_time_standards == True
            and type(self.timeframe) != None
        ):

            #
            # for test function
            if test_function:
                print(
                    "in profiler function the timeseries the periode is converted to the timeframe "
                )

            #
            # if matches the weekly peride
            if self.timeframe == "D":
                #
                # tails to 1D in weeks
                df_ts = df_ts.tail(251)

            #
            # if matches the weekly peride
            if self.timeframe == "W":
                #
                # tails to 1y in weeks
                df_ts = df_ts.tail(51)
            #
            # if matches the montly periode
            if self.timeframe == "M":
                #
                # if
                df_ts = df_ts.tail(12)
            #
            # if machtes with the one q periode
            if self.timeframe == "Q":
                df_ts = df_ts.tail(12)
            #
            # if machtes with the one year periode
            if self.timeframe == "Y":
                df_ts = df_ts.tail(5)

        df_ts.columns = ["Data"]
        df_ts["Data"].fillna(0)

        # print("this is the len of the dataframe ", len(df_ts))
        #
        # reconvert to list.
        ts = df_ts.values.tolist()

        # print("\n\n this is the incomming len after pars", len(ts))
        #
        #
        ##################################################################################################################################################################

        #
        # extracts the data for list size.
        if type(ts) != list:
            #
            # for test function
            if test_function:
                print(
                    "in profiler function the timeseries is converted to list"
                )
            #
            # changes the data type
            ts = ts.to_list()

        #
        # extracts the length for the calculation if required. Can be 0 if not used.
        if length_for_calculation != 0:

            #
            # for test function
            if test_function:
                print(
                    "in profiler function the timeseries is converted to lenght by imput"
                )
            #
            # just tries to cutt the length. This is already done above but for certain synchorinzation methodes it can be usefull.
            try:
                #
                #
                ts = ts[len(ts) - length_for_calculation + 1 : len(ts) - 1]

            except:
                #
                # if it fails, just return 0 or normal.
                if return_outcome_as_number != False:

                    #
                    #
                    status = 0

                    #
                else:

                    #
                    #
                    status = "NORMAL"
                return status

        #
        # checks if the lenght is long enough
        if len(ts) <= 2:

            #
            # for test function
            if test_function:
                print(
                    "in profiler function the timeseries is errored out because of a len error"
                )
            #
            # sets to status normal
            status = "NORMAL"
            #
            # check wich return time
            if return_outcome_as_number != False:

                status = 0

            return status

        ###### solves nested problem if appears

        #
        # if nested, this will run
        if any(isinstance(ts, list) for i in ts):
            #
            # if nested this will run
            ts = [ts for ts in ts for ts in ts]

            if test_function:
                print("the timeserie data is de-nested")

        ###### solves the divde by 0 error.

        if all(ts == 0 for ts in ts):

            status = "NORMAL"
            #
            # check wich return time
            if return_outcome_as_number != False:

                status = 0

            return status

        # print(ts)

        ###### profiles the data ( Normal even destribution unskewed) #############################################################

        last_attempt = ts[len(ts) - 1]
        #
        # removes NA.
        # ts = [incom for incom in ts if math.isnan(ts) != "nan"]
        #
        # extract averages.
        average = avg = round(sum(ts) / len(ts), 2)
        #
        # gets standaard devetion.

        std = np.std(ts)
        #
        # extracts the minimum
        minn = min(ts)
        #
        # extraxts the maximum
        maxx = max(ts)
        #
        # print("AVG = ",average, "STD =", std, "MAX = ",maxx)
        extreme_high = average + (3 * std)
        strong_high = average + (2 * std)
        normal_high = average + (1 * std)
        normal = average = avg
        normal_low = average - (1 * std)
        strong_low = average - (2 * std)
        extreme_low = average - (3 * std)

        last_month = last_attempt

        #
        # checks if one of the values is NA -- made after an terrible error occured.
        if math.isnan(average) or math.isnan(std):

            #
            # if this codes runs its clear that there is something really wrong

            #
            #
            if test_function == True:
                print("profiler, there is an error occured")

            #
            # sets normal status
            status = "NORMAL"

            if return_outcome_as_number != False:
                status = 0

        # print("\n\n", last_attempt, " =  This is the last attemt")
        # print( "Average ", average ," std" ,std, " P", amountperiode, length_for_calculation, "lAST = ", last_month )

        if last_month >= normal_low and last_month <= normal_high:
            status = "NORMAL"
            if return_outcome_as_number != False:
                status = 0

        if last_month >= strong_low and last_month <= normal_low:
            status = "LOW"
            if return_outcome_as_number != False:
                status = -1

        if last_month <= strong_low and last_month >= extreme_low:
            status = "STRONG_LOW"
            if return_outcome_as_number != False:
                status = -2
        if last_month <= extreme_low:
            status = "EXTREME_LOW"
            if return_outcome_as_number != False:
                status = -3
        if last_month <= strong_high and last_month >= normal_high:
            status = "HIGH"
            if return_outcome_as_number != False:
                status = 1

        if last_month >= strong_high and last_month <= extreme_high:
            status = "STRONG_HIGH"
            if return_outcome_as_number != False:
                status = 2

        if last_month >= extreme_high:
            status = "EXTREME_HIGH"
            if return_outcome_as_number != False:
                status = 3

        ######  End distribution ####################################################################################################################################################

        # print(status)
        # print( status, "= status, Average =", average ," std" ,std, " P",  length_for_calculation, "lAST = ", last_month, " the len of the time serie =" , len(ts) )

        return status

    def convert_data_to_dataframe(self, data=None):

        #
        # tails the data so it matches with the amount of data.
        idata = self.stock_data.tail(len(data))
        #
        # sets data to an other vairble
        ldata = data
        #
        # creates a data frame ()
        ldataf = pd.DataFrame(ldata)
        #
        # uses index
        data_index = idata.index

        if len(data_index) != len(ldataf):

            if 0 == 0:
                pass

        # datadasframe = pd.DataFrame(index=datesindex, data=ldataf.values)
        the_created_dataframe = pd.DataFrame(
            index=data_index, data=ldataf.values
        )
        #
        # sets data frame to class object
        self.data_frame = the_created_dataframe
        #
        # changes the name of the colums
        self.data_frame.columns = ["Data"]
        #
        # replaces the Na's with zero's ( Ment for the change dataframe)
        self.data_frame["Data"] = self.data_frame["Data"].fillna(0)

        return self.data_frame


class twitter_text_generator:

    """
    This class works the following, the details are setteled, there will be a list that.

    # HOW TO ADD AN MODULE

    1. add the analyeses in the main module
    2. add the text of the analyses.


    """

    # fundamentals
    name_of_analyse = None
    occation = None
    additional_text = None
    twitter_text_elements = []
    twitter_text_full = None
    twitter_hashtages = None

    # amount of occations
    occations_list = ["CHANGE_PROFILE", "CHANGE_IN_RATE_OF_CHANGE"]
    analyses_names = (
        main_analyeses.analyses_names
    )  # routes the analyeses names
    text_dictionary = {}

    def __init__(
        self,
        name_of_analyeses=None,
        ticker_name=None,  # this is the ticker name.
        new_recommendation=None,  # this is the new recoomandtion
        old_recommendation=None,  # this is the old recommendation
        text_input=None,  # this input is for example: News, opionus
        time_frame=None,  # this is the time frame : Weekly/daily/monthly
        occation="CHANGE_PROFILE||NEWS||RATING||UNDERPRICED",  # this is the occation
        folder_name="DataFolder",
    ):
        """


        Parameters
        ----------
        name_of_analyeses : TYPE, optional
            DESCRIPTION. The default is None.
        ticker_name : TYPE, optional
            DESCRIPTION. The default is None.
        new_recommendation : TYPE, optional
            DESCRIPTION. The default is None.
        old_recommendation : TYPE, optional
            DESCRIPTION. The default is None.
        text_input : TYPE, optional
            DESCRIPTION. The default is None.
        time_frame : TYPE, optional
            DESCRIPTION. The default is None.
        occation : TYPE, optional
            DESCRIPTION. The default is "CHANGE_PROFILE||NEWS||RATING||UNDERPRICED".

        Raises
        ------
        ValueError
            DESCRIPTION.

        Returns
        -------
        None.

        """
        # sets name of analyeses
        self.name_of_analyse = name_of_analyeses
        #
        # sets tickername
        self.ticker_name = ticker_name
        #
        # sets timeframe
        self.time_frame = time_frame
        #
        # checks occation
        if occation not in self.occations_list:

            raise ValueError("ValueError exception thrown")

        #
        else:

            self.occation = occation

        #
        # sets new recomandation
        self.new_recommendation = new_recommendation
        #
        # sets old recommandation
        self.old_recommendation = old_recommendation
        #
        #
        self.additional_text = text_input
        #
        #
        # run afterwarts
        # self.construct_analyses_texts()
        self.twitter_hashtages = ["#MARKETJUNKS", "#ICMM", "#LeoHanhart"]

    def construct_analyses_texts(self):
        """
        If there needs to be added an analyses we can just do that here.

        Returns
        -------
        None.

        """

        ## NOTICE ## if there needs to be an uniek analyses you can start this function with an IF statment.

        #
        # resets the string elements
        self.twitter_text_elements = []

        ### add the date ###
        # get date
        #
        now = datetime.now()
        #
        #
        date_time = now.strftime("%m-%d-%Y")

        self.twitter_text_elements.append(date_time)
        ####################

        self.twitter_text_elements.append(",")

        ### add ticker ###
        ticker_string = "instrument : " + self.ticker_name + "."
        self.twitter_text_elements.append(ticker_string)
        self.twitter_hashtages.insert(0, "#" + self.ticker_name)

        print(
            "\n\n\nthis is the text 1",
            self.twitter_text_elements,
            "\n\nAnd the hashtaged",
            self.twitter_hashtages,
        )
        time.sleep(5)

        ### add text occation ###
        occation = self.returns_occation_text(self.occation)
        self.twitter_text_elements.append(occation)

        print(
            "\n\n\nthis is the text 2",
            self.twitter_text_elements,
            "\n\nAnd the hashtaged",
            self.twitter_hashtages,
        )
        time.sleep(5)

        ### add analyses introduction
        analyes_text = self.return_analyeses_description(self.analyses_names)
        self.twitter_text_elements.append(analyes_text)

        print(
            "\n\n\nthis is the text 3",
            self.twitter_text_elements,
            "\n\nAnd the hashtaged",
            self.twitter_hashtages,
        )
        time.sleep(5)

        ### add timeframe ###
        time_frame = self.returns_data_horizon(self.time_frame)
        # self.twitter_text_elements.append(time_frame)

        ### add recommandations ###
        recommandation = self.return_recommandations(
            new_recommendation=self.new_recommendation,
            old_recommendation=self.old_recommendation,
        )
        self.twitter_text_elements.append(recommandation)

        ### add text ###
        if self.additional_text != None:
            #
            # adds additional text.
            self.twitter_text_elements.append(self.additional_text)

        # get hassages.
        self.twitter_hastages_text = " ".join(self.twitter_hashtages)

        # pasts twitter text
        self.twitter_text_full = " ".join(self.twitter_text_elements)

        # mounts the two twitter texts
        self.twitter_text_full = (
            self.twitter_text_full + self.twitter_hastages_text
        )

        # make sure it doesnt cutt the tighs of witter.
        self.twitter_text_full = self.twitter_text_full[:280]

        # self.twitter_hashtages       =   ["#MARKETJUNKS","#ICMM","#LeoHanhart"]

        print("This is the end of the function")
        time.sleep(5)

        # return self.twitter_text_full

    def returns_occation_text(self, imput_occation=None):
        """
        Recommandations

        Parameters
        ----------
        imput_occation : TYPE, optional
            DESCRIPTION. The default is None.

        Returns
        -------
        str
            DESCRIPTION.

        """

        # always ends with
        if type(self.occation) == str and self.occation == "CHANGE_PROFILE":
            self.twitter_hashtages.append("#change_in_profile")
            return "There was profile change announced for the"

        if (
            type(self.occation) == str
            and self.occation == "CHANGE_IN_RATE_OF_CHANGE"
        ):
            self.twitter_hashtages.append("#UNUSUAL_ACTIVITY")
            return "We have noticed an unnormal situation in the mesurements for an analyses. This occures when measurements decrease/increase much faster then normal what can advancely result in a profile change for the"

    def return_analyeses_description(self, input_analyeses):
        """
        Returns recommadations

        Parameters
        ----------
        input_analyeses : TYPE
            DESCRIPTION.

        Raises
        ------

            DESCRIPTION.

        Returns
        -------
        str
            DESCRIPTION.

        """
        # return liquidity analyeses
        if self.name_of_analyse not in self.analyses_names:

            raise "There is something wrong. No analyses like this found"

        # returns liquidity analyeses
        if (
            type(self.name_of_analyse) == str
            and self.name_of_analyse == "LIQUIDTY"
        ):
            #
            # returns the text.

            self.twitter_hashtages.append("#liquidity_analyses")
            return "the liquidity analyses."

        #
        # returns the moneyflow analyses.
        if (
            type(self.name_of_analyse) == str
            and self.name_of_analyse == "MONEYFLOWS"
        ):
            self.twitter_hashtages.append("#moneyflows_analyses")
            return "the moneyflow analyeses."

    # def receive_analyeses_text(self):
    def returns_data_horizon(self, time_frame):
        """
        Returns recommandation

        Parameters
        ----------
        time_frame : TYPE
            DESCRIPTION.

        Returns
        -------
        str
            DESCRIPTION.

        """
        if time_frame == "D":
            self.twitter_hashtages.append("#daily_timeframe")
            return "We used the daily timeframe for this analyses."
        if time_frame == "W":
            self.twitter_hashtages.append("#weekly_timeframe")
            return "We used the weekly timeframe for this analyses."
        if time_frame == "M":
            self.twitter_hashtages.append("#monthly_timeframe")
            return "We used the monthly timeframe for this analyses."
        if time_frame == "Q":
            self.twitter_hashtages.append("#quarterly_timeframe")
            return "We used the quaterly timeframe for this analyses."
        if time_frame == "Y":
            self.twitter_hashtages.append("#yearly_timeframe")
            return "We used the yearly timeframe for this analyses."

    def return_recommandations(self, new_recommendation, old_recommendation):
        """
        Retuns recommantions

        Parameters
        ----------
        new_recommendation : TYPE
            DESCRIPTION.
        old_recommendation : TYPE
            DESCRIPTION.

        Raises
        ------
        Exception
            DESCRIPTION.

        Returns
        -------
        text : TYPE
            DESCRIPTION.

        """
        if new_recommendation != None and old_recommendation != None:
            #
            # sets text
            text = (
                '\n\nThe old recommandation was "'
                + old_recommendation
                + '" the new recommandation is "'
                + new_recommendation
                + '". '
            )
            #
            # sets twitter hashtage
            twitter_hastage = "#" + new_recommendation
            #
            # adds twitter hastages.
            self.twitter_hashtages.append(twitter_hastage)
            #
            # retuns text
            return text
        else:
            raise Exception("10001", "NO reccomandion occured")


class plot_generator:

    # fundamental
    data = None

    # information
    ticker_name = None
    name_of_data = None
    type_of_data = None
    timeframe = None
    last_plot_name = None
    name_of_analyses = None

    #
    name_analyses_postready = None

    # location saved picture.
    location_picture = ""

    def __init__(
        self,
        data=None,  # data of the analyeses
        analyeses_dictionary=None,  # analyeses data
        name_of_analyeses=None,  # name of analyes
        ticker_name=None,  # ticker name
        timeframe=None,  # quite unimportantand
        name_of_data=None,  # tile of the data
        type_of_data=None,
        path=None,
    ):  #

        # set varibles
        self.data = data
        self.timeframe = timeframe
        self.ticker_name = ticker_name
        self.name_of_data = name_of_data
        self.name_of_analyses = name_of_analyeses
        self.analyeses_dictionary = analyeses_dictionary

        # create name for the plot
        self.__construct_picture_name()

        return

    def plot_analyses_raw(self):
        pass

    def plot_analyeses_full_picture(self):
        pass

    def plot_2_frames_with_logo(
        self,
        main_title="Main analyses nane",
        df1=None,
        x1=None,
        y1=None,
        title1="Title of the first plot",
        df2=None,
        x2=None,
        y2=None,
        title2="The title of the second plot",
        xlabel="Date",
        ylabel="Value",
        dpi=100,
        ticker_name=None,
        analyses_name=None,
        time_frame="weekly",
        path=None,
    ):
        pass

        # retreives the logo/ try and catch can be added for deployment
        logo = plt.imread("icmm_logo.png")
        #
        # this print can be added

        #
        # this figure is added
        fig = plt.figure(figsize=(20, 8), dpi=200)
        #
        #
        # organize the picture and adding the logo.
        addLogo = OffsetImage(logo, zoom=0.45)
        # addLogo.set_zorder(100)
        addLogo.set_offset(
            (2551, 1280)
        )  # pass the position in a tuple # pass the position in a tuple

        #
        # te figures gridpec
        gs = fig.add_gridspec(2, hspace=0.2)
        #
        # making the x shared
        axs = gs.subplots(sharex=True, sharey=False)
        # creating the fig title.
        fig.suptitle(
            main_title, fontsize=32, family=["Times"], y=0.99, color="#045BFF"
        )

        #
        # creating the first band
        axs[0].plot(x1, y1, "tab:red")
        axs[0].set_title(title1)
        axs[0].yaxis.tick_right()

        #
        # creating the second plot
        axs[1].plot(x2, y2, "tab:green")
        axs[1].set_title(title2)
        axs[1].yaxis.tick_right()
        axs[1].add_artist(addLogo)
        # axs[1].figimage(logo)
        # axs[2].axis('off')

        # get date for plot
        now = datetime.now()
        date = now.strftime("%m-%d-%Y")

        #
        # check if there is a path filled in, after that it can be used.
        if type(path) != None:
            # plt.show()
            if (
                ticker_name != None
                and analyses_name != None
                and time_frame != None
            ):

                my_path = os.path.dirname(os.path.abspath(__file__))
                my_file = (
                    ticker_name
                    + "_"
                    + analyses_name
                    + "_"
                    + time_frame
                    + "_"
                    + ".png"
                )
                fullpath = my_path + "\\Pictures\\" + my_file

                # plot_name = path+ ""+ ticker_name +"_" +analyses_name +"_" +time_frame+"_"+".png"

                self.last_plot_name = fullpath

                #
                # saving the file in the folder

                plt.savefig(fullpath, bbox_inches="tight")

                plt.draw()
                plt.show()

                return fullpath

        else:

            my_file = (
                ticker_name
                + "_"
                + analyses_name
                + "_"
                + time_frame
                + "_"
                + ".png"
            )
            plt.savefig(my_file, bbox_inches="tight")
            plt.draw()
            plt.show()

    def __construct_picture_name(self):

        analyses_name_prepaired = self.name_of_analyses.lower()

        analyses_name_added = analyses_name_prepaired + "-" + "analyses"

        self.name_analyses_postready = analyses_name_added

        self.name_of_picture = (
            self.ticker_name
            + ", "
            + analyses_name_added
            + ", "
            + self.timeframe
        )

        return self.name_of_picture

    def generate_change_profile_plot(self):
        """
        this function is made for the Liquidty analyses and the Moneyflow analyses.

        """

        #
        # check if the data is listed in the dictonary
        if "indicator_timeserie_raw" in self.analyeses_dictionary:

            #
            # set data the raw indicator data. - in the data is also the change of the data. it could potentially be that
            data_raw = self.analyeses_dictionary["indicator_timeserie_raw"]

            if self.name_of_analyses == "MONEYFLOWS":
                data_raw = data_raw.cumsum()
            #
            # set data
        else:

            #
            # if the data is incomplete then there is something very bad going on. So error is thrown.
            raise Exception(
                "error thrown, no raw indicator data in dictonary",
                "plot_generator",
                self.ticker_name + self.name_of_analyses,
            )
        #
        # check if the other data is complete, most of the time this work if the other thing works
        if "indicator_timeserie_profile" in self.analyeses_dictionary:

            #
            # sets the profile data
            data_profile = self.analyeses_dictionary[
                "indicator_timeserie_profile"
            ]

            #
            # sets data
        else:

            #
            # throws an error if the data is not there.
            raise Exception(
                "error thrown, no profile indicator data in dictonary",
                "plot_generator",
                self.ticker_name + self.name_of_analyses,
            )

        #
        # creates a path for the plot extention.
        my_path = os.path.dirname(os.path.abspath(__file__))
        #
        # this generates a plot name for the picture
        my_file = self.__construct_picture_name()
        #
        # this adds an extention to the pictuer
        my_extention = ".png"  # hier kun je heel makkelijk een ander type foto implementeren.
        #
        # creates the full path.
        fullpath = my_path + "\\Pictures\\" + my_file + my_extention

        print(self.name_of_picture)
        return
        #
        # generates plot
        plot_link = self.plot_2_frames_with_logo(
            #
            # sets the main title
            main_title=self.name_of_picture,
            #
            # sets the raw data
            df1=data_raw,
            #
            # sets the raw data indexx
            x1=data_raw.index,
            #
            # sets the daw Data. - used a clasic forwarding method
            y1=data_raw.Data,
            #
            # sets the tile
            title1=self.name_analyses_postready + ", raw data",
            #
            # sets the data for the second plot
            df2=data_profile,
            #
            # sets the data profile index
            x2=data_profile.index,
            #
            # sets the data profile data
            y2=data_profile.Data,
            #
            # sets the name of a analyses
            title2=self.name_analyses_postready + ", profile data",
            #
            # sets the x lable, this should be data
            xlabel="Date",
            #
            # sets x lable
            ylabel="Value",
            #
            # sets dpi
            dpi=100,
            #
            # sets ticker name
            ticker_name=self.ticker_name,
            #
            # sets analyses name
            analyses_name=self.name_of_analyses,
            #
            # sets timeframe
            time_frame=self.timeframe,
            path=0,
        )

        return plot_link


class twitter_module:
    def __init__(self):

        # load analyses, ticker, ect,
        # generate text,
        # generate plot,
        # post tweet,
        # save message.
        pass

    def post_tweet(self, text=None, path_photo=None):
        """
        this is a test text

        Parameters
        ----------
        text : TYPE, optional
            DESCRIPTION. The default is None.
        path_photo : TYPE, optional
            DESCRIPTION. The default is None.

        Returns
        -------
        None.

        """
        # Authenticate to Twitter
        auth = tweepy.OAuthHandler(
            "wX4lco85Qu9zYqLPchbD4DUov",
            "G3mKMivifmMJoE8pZGats8fHl8BrMUfMRuhklL6r90aJ0139Qy",
        )
        auth.set_access_token(
            "1227626390171852800-2nSTPjqtaHXk6zO3omtGD6WnUyQDN5",
            "aGYrAJR6uUkKJYjltSPGkdzsE6wyh9O1nGeJz4Rs1GsU4",
        )

        # Create API object
        api = tweepy.API(auth)

        # load image
        imagePath = path_photo
        status = text

        # Send the tweet.
        api.update_with_media(imagePath, status)


class liquidity_analyses_rf:
    """
    Voor het afsluiten moeten

    - getest worden of het werkt,
        - de recovery               #    Werkt perfect. - nog een keer testen voor pfofilene
        - geprofilers serie         X
        - de regular profiler.      X

    - er moet toegevoegd worden dat de liquidity analyses .

    """

    # object fundamentals
    stock_ticker = None
    stock_data = None
    class_extention = "liquidity_timeserie"
    class_extention_profiler = "liquidity_profiler_timeserie"

    # object data
    liquidity_data_set = None  # values.
    liquidity_data_set_df = None  # timeserie.
    liquidity_data_loaded = False

    # object profile
    liquidity_profiler_set = (
        None  # used for the calculations in return_liquidity_profiler
    )
    liquidity_data_profiles = None  # the time serie.
    liquidity_profiledata_set_df = None
    liquidity_data_profiles_loaded = False
    recoverd_profiles = False
    temporary_profiles_for_recovery = None

    # error handlinges
    Error = False
    Error_code = ""

    def __init__(self, stock_ticker="", stock_data=None, synchronize=False):
        """


        Parameters
        ----------
        stock_ticker : TYPE, optional
            DESCRIPTION. The default is "".
        stock_data : TYPE, optional
            DESCRIPTION. The default is None.

        Returns
        -------
        None.

        """
        #
        # sets system varibles
        self.stock_data = stock_data
        #
        # sets ticker ovject
        self.stock_ticker = stock_ticker
        #
        # saves or re-engages.
        if synchronize != False:
            #
            # if loads the files, daily data, with ticker
            self.check_or_load_the_timeserie_data()
            #
            # loads profiles with tickers.
            self.check_or_load_the_profiler_data()

        else:
            #
            # loads normal ( Slow ) startup
            self.alternative_startup

    def alternative_startup(self):

        self.liquidity_data_set = self.liquidity_timeserie()
        self.liquidity_profiler_set = self.liquidity_timeserie_profile()

    def check_or_load_the_timeserie_data(self):

        # check if its the first time that the this analyses is done for a stock.
        self.synch_object = synch_class.data_synch(
            path=constants.CORE_DATA_____PATH,
            subfolder="stock_data",
            ticker=self.stock_ticker,
            data_extention=self.class_extention,
        )

        # sets the stock ticker
        self.synch_object.ticker = self.stock_ticker

        # sets the static data object(Used for synching and pachaging data. )
        self.synch_object.static_data = self.stock_data

        self.synch_object.load_data()

        # turns on if class is not intalized before so everthing needs to be prepaired and saved.

        # this procces saves the the liquidity data.
        if self.synch_object.is_data_new == True:

            #
            # gets the time serie
            self.liquidity_data_set = self.liquidity_timeserie()
            #

            # sets bool
            self.liquidity_data_loaded = True
            #
            # Package the data.
            # first prepair the stockdata
            self.synch_object.prepair_stock_data_for_static_data(
                data=self.stock_data
            )
            #
            #

            self.synch_object.prepair_data_in_dataframe(
                data=self.liquidity_data_set
            )
            #
            # gets saves time serie local.
            self.liquidity_data_set_df = self.synch_object.new_data
            #
            # saves the time serie as dataframe
            self.synch_object.synch_data_timeserie()

        # turns on if the data is not new.
        else:

            # check if the data is expided
            if self.synch_object.returns_true_if_expired_with_data() == True:

                # returns the amount of days
                amount_of_days = self.synch_object.return_amount_of_days()

                # returns a liquidity
                liquidity_aditiona_data_set = self.liquidity_timeserie(
                    amount_of_days
                )

                # sets the data.
                self.synch_object.new_data = liquidity_aditiona_data_set

                # synches, and automaticly saves the retreived and merged time serie.
                self.synch_object.synch_data_timeserie()

                # sets liquide data.
                self.liquidity_data_set = self.synch_object.synchronized_data
                # sets bool
                self.liquidity_data_loaded = True

            # if not expider just load the retreived data as expired.
            else:

                # sets lid data
                self.liquidity_data_set = self.synch_object.retreived_data
                self.liquidity_data_loaded = True

    def check_or_load_the_profiler_data(self):

        # check if its the first time that the this analyses is done for a stock.
        self.synch_object_profiler = synch_class.data_synch(
            path=constants.CORE_DATA_____PATH,
            subfolder="stock_data",
            ticker=self.stock_ticker,
            data_extention=self.class_extention_profiler,
        )

        # sets the stock ticker
        self.synch_object_profiler.ticker = self.stock_ticker

        # sets the static data object(Used for synching and pachaging data. )
        self.synch_object_profiler.static_data = self.stock_data

        self.synch_object_profiler.load_data()

        # turns on if class is not intalized before so everthing needs to be prepaired and saved.

        # this procces saves the the liquidity data.
        if self.synch_object_profiler.is_data_new == True:

            #
            # gets the time serie
            self.liquidity_profiler_set = self.liquidity_timeserie_profile()
            #
            # sets bool
            self.liquidity_data_profiles_loaded = True
            #
            # Package the data.
            # first prepair the stockdata
            self.synch_object_profiler.prepair_stock_data_for_static_data(
                data=self.stock_data
            )
            #
            #
            self.synch_object_profiler.prepair_data_in_dataframe(
                data=self.liquidity_profiler_set
            )
            #
            self.liquidity_profiledata_set_df = self.synch_object.new_data
            #
            # gets a synch object.
            self.synch_object_profiler.synch_data_timeserie()

        # turns on if the data is not new.
        else:

            # check if the data is expided
            if (
                self.synch_object_profiler.returns_true_if_expired_with_data()
                == True
            ):

                #
                # returns the amount of days
                amount_of_days = (
                    self.synch_object_profiler.return_amount_of_days()
                )
                #
                # returns a liquidity
                liquidity_aditiona_data_set = (
                    self.liquidity_timeserie_profile_recover(
                        amount_of_days, tial_amount=True
                    )
                )
                #
                # sets the data.
                self.synch_object_profiler.prepair_data_in_dataframe(
                    liquidity_aditiona_data_set
                )
                #
                #
                # synches, and automaticly saves the retreived and merged time serie.
                self.synch_object_profiler.synch_data_timeserie()
                #
                # sets liquide data.
                self.liquidity_profiledata_set_df = (
                    self.synch_object_profiler.synchronized_data
                )
                #
                self.liquidity_profiler_set = (
                    self.liquidity_data_profiles.values
                )
                #
                self.liquidity_profiler_set = (
                    self.liquidity_profiler_set.tolist()
                )
                #
                self.liquidity_data_profiles_loaded = True

            #
            # if not expider just load the retreived data as expired.
            else:

                #
                # sets lid data
                # sets liquide data.
                self.liquidity_profiledata_set_df = (
                    self.synch_object_profiler.retreived_data
                )
                #
                #
                self.liquidity_profiler_set = (
                    self.liquidity_profiledata_set_df.values
                )
                #
                #
                self.liquidity_profiler_set = (
                    self.liquidity_profiler_set.tolist()
                )
                #
                #
                self.liquidity_data_profiles_loaded = True

    def liquidty_analyses_with_stock_object_row(self, sample_data=""):

        # explaind. Eigenschappen:
        # het getal word groter als of de impact groter wordt. of het aantal shares lager wordt.
        # met andere woorden, hoe hoger de score , of hoe minder shares er gedaan zijn

        # check if the right  type is fowarded, data is already checked on NA's
        if isinstance(sample_data, pd.core.series.Series):

            # varibles are set voor equation
            data = sample_data
            volume = int(data["Volume"])
            price = data["Adj Close"]
            volume_in_capital = volume * price
            volume_in_hondermilions = volume_in_capital / 100000000
            change = volume = data["Change"]

            # checks if calculatie is wrong.
            if change == 0 or volume_in_hondermilions == 0:
                return 0
            equation = change / volume_in_hondermilions

            return equation
        else:
            return ("Error", 501)

    def liquidity_timeserie(self, length_for_calculation=0):

        # here needs to be checkt if the file is loaded.
        if self.liquidity_data_loaded == True:

            return self.liquidity_data_set
        else:

            if length_for_calculation == 0:
                length_for_calculation = int(len(self.stock_data) - 1)

            workdata = self.stock_data.iloc[
                len(self.stock_data)
                - length_for_calculation : len(self.stock_data)
            ]
            calculations = []
            for x in range(0, len(workdata)):

                outcome = self.liquidty_analyses_with_stock_object_row(
                    workdata.iloc[x]
                )

                if outcome == 0:

                    calculations.append(outcome)
                    continue

                calculations.append(outcome)

            self.liquidity_data_set = calculations
            self.liquidity_data_loaded = True
            return calculations

    def liquidity_timeserie_profile(
        self, length_for_calculation=0, tial=0, test=False
    ):
        """
        The lengt for calculation function doesnt work and should never be used in these modes.

        Parameters
        ----------
        length_for_calculation : TYPE, optional
            DESCRIPTION. The default is 0.
        tial : TYPE, optional
            DESCRIPTION. The default is 0.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """

        # here needs to be checkt if the file is loaded.
        if self.liquidity_data_profiles_loaded == True and test == False:

            #
            # loads liquidity data.
            return self.liquidity_data_set

        # starts running if the serie in not loaded yet.
        else:
            #

            if length_for_calculation == 0:
                #
                #
                length_for_calculation = int(len(self.stock_data) - 1)

            # sets the wordking data while lenght for calculations can be used for tailing
            workdata = self.stock_data.iloc[
                len(self.stock_data)
                - length_for_calculation : len(self.stock_data)
            ]
            #
            # this unit is used for the calculations
            calculations = []
            #
            # this unit is used for the profiles
            profiles = []

            # this loop loops true the workdata
            for x in range(0, len(workdata)):

                #
                # the data is put in this liquidity analyeses
                outcome = self.liquidty_analyses_with_stock_object_row(
                    workdata.iloc[x]
                )
                #
                # if the outcom errors it recevies a 0. Then 0 will be add.
                if outcome == 0:

                    #
                    # this row adds the calculatios to the vector
                    calculations.append(outcome)
                    #
                    # this row adds the outcome -- in this case 0 to the arry
                    profiles.append(outcome)
                    #
                    # and continues
                    continue

                #
                # if not 0 the calculation is added
                calculations.append(outcome)
                # print(calculations)
                # time.sleep(2.4)
                #
                # the liquidity profiler set is a global object that uses
                # the new data, instead of the other data. so new profiles are not
                # disturbed with new large outcomes.
                self.liquidity_profiler_set = calculations
                #
                #
                # returns the liquidty profile
                the_last_profile = self.return_liquidity_profile(
                    length_for_calculation=250,
                    return_outcome_as_number=True,
                    profiler_timeseries_recoverage=True,
                )
                #
                # print(the_last_profile, "this is the last profile")
                # this adds the outcome to the array where it all happends.
                profiles.append(the_last_profile)

            #
            # if the loop is finished, the profiles are joint
            self.liquidity_data_profiles = profiles
            #
            # the data of the liquidity profiler is resetted.
            self.liquidity_profiler_set = profiles

            return profiles

    def liquidity_timeserie_profile_recover(
        self, length_for_calculation=0, tial_amount=0
    ):

        # IMPORTANT NOTICE
        #   - workdata is used for the profiles, this always needs to be the missing amount,
        #   - calculations is a different story because it is used for profiling, This should always be a
        # the most eases, profile the new patterns with the old liquidity outcome headed the serie
        # with total length min - the length for calculation. After that, all the data can be added.

        # here needs to be checkt if the file is loaded.
        if self.liquidity_data_profiles_loaded == True:

            #
            # REMOVE THIS FOR RIGHT ONE.
            return self.liquidity_data_set

        else:

            #
            # sets work calculation
            workdata = self.stock_data.iloc[
                len(self.stock_data) - tial_amount : len(self.stock_data)
            ]
            #
            # check if there is a length for calculation.
            if length_for_calculation != 0:

                #
                # sets calculations as mentioned above. This need to land in the return profile
                calculations = self.liquidity_data_set[
                    len(self.liquidity_data_set)
                    - length_for_calculation : len(self.liquidity_data_set)
                    - tial_amount
                ]
                #
                # if there is no limmet set, its need to be the whole data set.
            else:

                #
                # fill in the calculations with the wole data set, this should be filterd.
                calculations = self.liquidity_data_set[
                    1 : len(self.liquidity_data_set) - tial_amount
                ]

            #
            # the liquidity profiles is always reset.
            profiles = []
            calculations = []
            #
            # loops true the fork data.
            for x in range(0, len(workdata)):

                #
                # this is the outcome of a single rowed liquidity data analyesse
                outcome = self.liquidty_analyses_with_stock_object_row(
                    workdata.iloc[x]
                )
                #
                # if tghe outcome is zero then it always zero
                if outcome == 0:
                    #
                    # appending the calcualtions to the lists
                    calculations.append(outcome)
                    #
                    # apppending to the profiles
                    profiles.append(outcome)
                    continue

                #
                # adding the calculations
                calculations.append(outcome)

                #
                # setting the calculations to the liquidity profiler set. This is In object parsing
                self.temporary_profiles_for_recovery = calculations
                #
                # the last
                the_last_profile = self.return_historic_liquidity_profile()

                #
                # adding profiles.
                profiles.append(the_last_profile)

            #
            # setting the revoved profiles to recoverd profiles.
            self.recoverd_profiles = profiles
            #
            # removing the profiler set because it can not interrupt the system anymore.
            self.liquidity_profiler_set = None

    def return_liquidity_profile(
        self,
        length_for_calculation=0,
        return_outcome_as_number=False,
        profiler_timeseries_recoverage=False,
    ):

        # check if the profiler needs to be limited to a certain periode.
        # for example, the calculation for a profile can be heavy wrong
        # after a stock chrash so its very important that you cutt it to 2,3,4,5 years.
        ts = []
        # laden van de time serie
        if self.liquidity_data_loaded != True:
            self.liquidity_timeserie()
            # self.Error_code = "Function used before data was loaded."

            # return False
        #
        # if this function is used in a profiler setup then other data needs to be loaded.
        if profiler_timeseries_recoverage == True:

            #
            # sets profiler data
            ts = self.liquidity_profiler_set

        else:

            #
            # extracts the data in array size. If this is nessary.

            if type(self.liquidity_data_set) != list:

                #
                #
                ts = self.liquidity_data_set.values

            else:
                ts = self.liquidity_data_set

        # extracts the data for list size.
        if type(ts) != list:
            #
            # changes the data type
            ts = ts.to_list()

        #
        # extracts the length for the calculation if required.
        if length_for_calculation != 0:

            #
            # sets the length
            ts = ts[len(ts) - length_for_calculation + 1 : len(ts) - 1]
        #
        # get last month.

        #
        # prevent 0 len error
        if len(ts) == 0:
            #
            # sets to status normal
            status = "NORMAL"
            #
            # check wich return time
            if return_outcome_as_number != False:

                status = 0

            return status

        last_attempt = ts[len(ts) - 1]
        #
        # removes NA.
        ts = [incom for incom in ts if str(incom) != "nan"]
        #
        # extract averages.
        average = avg = sum(ts) / len(ts)
        #
        # gets standaard devetion.
        std = np.std(ts)
        #
        # extracts the minimum
        minn = min(ts)
        #
        # extraxts the maximum
        maxx = max(ts)
        #
        # print("AVG = ",average, "STD =", std, "MAX = ",maxx)
        extreme_high = average + (3 * std)
        strong_high = average + (2 * std)
        normal_high = average + (1 * std)
        normal = average = avg
        normal_low = average - (1 * std)
        strong_low = average - (2 * std)
        extreme_low = average - (3 * std)

        last_month = last_attempt
        # print("\n\n", last_attempt, " =  This is the last attemt")
        # print( "Average ", average ," std" ,std, " P", amountperiode, length_for_calculation, "lAST = ", last_month )

        if last_month >= normal_low and last_month <= normal_high:
            status = "NORMAL"
            if return_outcome_as_number != False:
                status = 0

        if last_month >= strong_low and last_month <= normal_low:
            status = "LOW"
            if return_outcome_as_number != False:
                status = -1

        if last_month <= strong_low and last_month >= extreme_low:
            status = "STRONG_LOW"
            if return_outcome_as_number != False:
                status = -2
        if last_month <= extreme_low:
            status = "EXTREME_LOW"
            if return_outcome_as_number != False:
                status = -3
        if last_month <= strong_high and last_month >= normal_high:
            status = "HIGH"
            if return_outcome_as_number != False:
                status = 1

        if last_month >= strong_high and last_month <= extreme_high:
            status = "STRONG_HIGH"
            if return_outcome_as_number != False:
                status = 2

        if last_month >= extreme_high:
            status = "EXTREME_HIGH"
            if return_outcome_as_number != False:
                status = 3

        # print(status)
        return status

    def return_historic_liquidity_profile(
        self,
        length_for_calculation=0,
        return_outcome_as_number=True,
        profiler_timeseries_recoverage=True,
    ):

        # check if the profiler needs to be limited to a certain periode.
        # for example, the calculation for a profile can be heavy wrong
        # after a stock chrash so its very important that you cutt it to 2,3,4,5 years.

        # laden van de time serie

        # if this function is used in a profiler setup then other data needs to be loaded.
        if profiler_timeseries_recoverage == True:

            #
            # sets profiler data
            ts = self.temporary_profiles_for_recovery

        else:

            #
            # extracts the data in array size.
            ts = self.liquidity_data_set.values

        #
        # extracts the data for list size.
        if type(ts) != list:
            #
            # changes the data type
            ts = ts.to_list()

        #
        # extracts the length for the calculation if required.
        if length_for_calculation != 0:

            #
            # sets the length
            ts = ts[len(ts) - length_for_calculation + 1 : len(ts) - 1]
        #
        # get last month.
        last_attempt = ts[len(ts) - 1]
        #
        # removes NA.
        ts = [incom for incom in ts if str(incom) != "nan"]
        #
        # extract averages.
        average = avg = sum(ts) / len(ts)
        #
        # gets standaard devetion.
        std = np.std(ts)
        #
        # extracts the minimum
        minn = min(ts)
        #
        # extraxts the maximum
        maxx = max(ts)
        #
        # print("AVG = ",average, "STD =", std, "MAX = ",maxx)
        extreme_high = average + (3 * std)
        strong_high = average + (2 * std)
        normal_high = average + (1 * std)
        normal = average = avg
        normal_low = average - (1 * std)
        strong_low = average - (2 * std)
        extreme_low = average - (3 * std)

        last_month = last_attempt

        # print( "Average ", average ," std" ,std, " P", amountperiode, length_for_calculation, "lAST = ", last_month )

        if last_month >= normal_low and last_month <= normal_high:
            status = "NORMAL"
            if return_outcome_as_number != False:
                status = 0

        if last_month >= strong_low and last_month <= normal_low:
            status = "LOW"
            if return_outcome_as_number != False:
                status = -1

        if last_month <= strong_low and last_month >= extreme_low:
            status = "STRONG_LOW"
            if return_outcome_as_number != False:
                status = -2
        if last_month <= extreme_low:
            status = "EXTREME_LOW"
            if return_outcome_as_number != False:
                status = -3
        if last_month <= strong_high and last_month >= normal_high:
            status = "HIGH"
            if return_outcome_as_number != False:
                status = 1

        if last_month >= strong_high and last_month <= extreme_high:
            status = "STRONG_HIGH"
            if return_outcome_as_number != False:
                status = 2

        if last_month >= extreme_high:
            status = "EXTREME_HIGH"
            if return_outcome_as_number != False:
                status = 3

        return status

    def rolling_liquidity_profile_timeserie(self, lenght_of_profile=10):

        #
        # takes liquidity profiles
        liq_profiles = self.liquidity_data_profiles
        #
        # loop door array van de profiles
        calculations = []
        for i in (0, len(liq_profiles)):

            #
            # blocks overfill of work data / lenght error
            if i + lenght_of_profile <= len(liq_profiles):

                # select work data
                work_data = liq_profiles[i : i + lenght_of_profile]

                # take average: Key ellement of this methode
                avg = sum(work_data) / len(work_data)

                # add calculations
                calculations.append(avg)

        return calculations

    def rolling_liquidity_profiler(
        self,
        incomming_data="incommingdata",
        length_for_profile=250,
        return_outcome_as_number=True,
    ):

        # check if the data is fine
        if type(incomming_data) != list:
            return 9000

        # checks if the data needs to be cut
        if len(incomming_data) >= length_for_profile:

            # tails the incomming data if nessary.
            incomming_data = incomming_data[
                len(incomming_data) - length_for_profile : len(incomming_data)
            ]

        ts = incomming_data

        # get last month.
        last_attempt = ts[len(ts) - 1]
        #
        # removes NA.
        ts = [incom for incom in ts if str(incom) != "nan"]
        #
        # extract averages.
        average = avg = sum(ts) / len(ts)
        #
        # gets standaard devetion.
        std = np.std(ts)
        #
        # extracts the minimum
        minn = min(ts)
        #
        # extraxts the maximum
        maxx = max(ts)
        #
        # print("AVG = ",average, "STD =", std, "MAX = ",maxx)
        extreme_high = average + (3 * std)
        strong_high = average + (2 * std)
        normal_high = average + (1 * std)
        normal = average = avg
        normal_low = average - (1 * std)
        strong_low = average - (2 * std)
        extreme_low = average - (3 * std)

        last_month = last_attempt

        # print( "Average ", average ," std" ,std, " P", amountperiode, length_for_calculation, "lAST = ", last_month )

        if last_month >= normal_low and last_month <= normal_high:
            status = "NORMAL"
            if return_outcome_as_number != False:
                status = 0

        if last_month >= strong_low and last_month <= normal_low:
            status = "LOW"
            if return_outcome_as_number != False:
                status = -1

        if last_month <= strong_low and last_month >= extreme_low:
            status = "STRONG_LOW"
            if return_outcome_as_number != False:
                status = -2
        if last_month <= extreme_low:
            status = "EXTREME_LOW"
            if return_outcome_as_number != False:
                status = -3
        if last_month <= strong_high and last_month >= normal_high:
            status = "HIGH"
            if return_outcome_as_number != False:
                status = 1

        if last_month >= strong_high and last_month <= extreme_high:
            status = "STRONG_HIGH"
            if return_outcome_as_number != False:
                status = 2

        if last_month >= extreme_high:
            status = "EXTREME_HIGH"
            if return_outcome_as_number != False:
                status = 3


# testen


class money_flows:
    """


    AFTERS CONSTRUCTION
    - Change the folder to the Data_Folder

    ATENTINO

    for daily synchorinzation
    - you need to find the amount of days between the two dates. So, you pick the days between function
    or you just add the two dates in the iloc function and see the amount of rows.

    """

    # stockdata details.
    stock_ticker = None
    stock_data = None
    timeframe = None

    # data dictionary
    analyeses_dictionary = {}

    # analyeses information
    name_of_analyeses = "MONEYFLOWS"

    # twitter details
    text_for_twitter = None
    link_for_image = None

    synchronize: bool = False
    first_run: bool = False
    use_automatic_time = (
        True  # can be used to help set profiles easy. If turend off ignored.
    )

    def __init__(
        self,
        stock_ticker="",
        stock_data=None,
        synchronize=False,
        timeframe="D = daily, W = Weekly, M = montly, Q = quarterly, Y = yearly",
    ):
        """


        Parameters
        ----------
        stock_ticker : TYPE, optional
            DESCRIPTION. The default is "".
        stock_data : TYPE, optional
            DESCRIPTION. The default is None.
        synchronize : TYPE, optional
            DESCRIPTION. The default is False.
        timeframe : TYPE, optional
            DESCRIPTION. The default is "D = daily, W = Weekly, M = montly, Q = quarterly, Y = yearly".

        Raises
        ------
        Exception
            DESCRIPTION.

        Returns
        -------
        None.

        """
        # starts time
        start = time.time()

        # technical data for calculations

        # sets system varibles
        self.stock_data = stock_data
        #
        # sets ticker ovject
        self.stock_ticker = stock_ticker

        # check if stock_data is not
        if stock_data is not None:

            self.profiler = profiling(
                stock_data=stock_data, timeframe=timeframe
            )

        else:

            raise Exception(
                "Ticker_None",
                "This error occures when ticker is Nonetype object",
            )

        self.synchronize = synchronize

        #
        # check if time frame is filled in well
        if (
            timeframe
            == "D = daily, W = Weekly, M = montly, Q = quarterly, Y = yearly"
        ):

            #
            # if it fails it marks it down as non
            self.timeframe = None

            #
            # if timeframe is filled in, it needs to be assinged.
        elif (
            timeframe == "D"
            or timeframe == "W"
            or timeframe == "M"
            or timeframe == "Y"
            or timeframe == "Q"
        ):
            #
            # if it fits, it assings.
            self.timeframe = timeframe

            # check if formate time serie is right
            if self.timeframe == "W":

                if not isinstance(pd.infer_freq(self.stock_data.index), str):

                    raise Exception(
                        "Time formate is wrong, analyses dident run"
                    )

                elif "W" not in pd.infer_freq(self.stock_data.index):

                    raise Exception(
                        "Time formate is wrong, probably something else the nweekly"
                    )

        else:
            #
            # sets the timeframe tonon
            self.timeframe = None

        """  
        What happends after this is quite ease to understand. 
        The data is retreived. 
        If the data is new, a new file is created. 
        If the file exsits there will be a check for howlong this is. 
        If the data is expired. 
        
        NEW DEAL: 
            
            Only use the experaion class in the synch class. 
            so first make a flowobject with the timeframe and anlyses and the dict extention
            if data is new. Run full analyesse just like negative experation.
            else check experation
            if get how much and r. un analyses. 
        else: just return the dict. 
        
        """

        end = time.time()
        print(end - start)
        print("this is the start")

        # creates name extrention
        data_extention = self.data_extention = (
            self.timeframe + self.name_of_analyeses + "_dictonary"
        )

        # creates data object
        self.synch_object = synch_class.data_synch(
            path=constants.CORE_DATA_____PATH,
            subfolder="stock_analyses_data",
            ticker=self.stock_ticker,
            data_extention=data_extention,
        )

        # if data is new refresh.
        if self.synch_object.is_data_new:

            print("the data is new")
            # set first run to true
            self.first_run = True
            # starts full analyses.
            self.money_flow_analyeses(full_run=True)
            return

        ###### hier
        # checks if the data is not new and, if the timeframe is defined and synch is true.
        elif (
            not self.synch_object.is_data_new
            and type(timeframe) != None
            and synchronize
        ):

            if not self.synch_object.return_last_modification_file(
                view=timeframe, experiation_bool=True
            ):
                print("the data is booted, known and not expired")
                self.analyeses_dictionary = self.synch_object.retreived_data
                return

            else:

                print("the data known but expired")

                # prepair the data for checking the experation.
                self.analyeses_dictionary = self.synch_object.retreived_data

                if not self.synch_object.check_incomming_dict_legit(
                    self.analyeses_dictionary
                ):
                    self.first_run = True
                    # starts full analyses.
                    self.liquidity_impact_analyeses(full_run=True)

                # set indicator
                indicator = self.analyeses_dictionary[
                    "indicator_timeserie_raw"
                ]

                print(self.analyeses_dictionary)

                print(indicator, "= the indicator, is the ts", self.stock_data)
                # get tge amount expired
                amount_of_expired = self.synch_object.time_bewteen_time_series(
                    indicator, self.stock_data, self.timeframe
                )

                # if ammount is 0, section mabey run because time passed but because of weekend, no data is missing.
                if amount_of_expired == 0:
                    print("time was expired but data not. ")
                    return

                else:
                    # if amount of data is missing - because its monday, it will work
                    self.money_flow_analyeses(
                        full_run=True, tail_amount=amount_of_expired
                    )

                return

        return

    def money_flow_with_row(self, data_row=None):
        """
        Artikel of the calculation : https://school.stockcharts.com/doku.php?id=technical_indicators:chaikin_money_flow_cmf

        Parameters
        ----------
        data_row : TYPE, optional
            DESCRIPTION. The default is None.

        Returns
        -------
        None.

        """
        #
        # converting data to varible
        x = data_row

        #
        # step one extracting the data
        #
        # checking if the data is deliverd
        if type(data_row) == None:
            #
            # couting if the data is not revieved.
            raise Exception("No data received in moneyflow anallyses ticker")

        # checking if the columns fitt
        # print(x.index)
        if (
            "Open" in x.index
            and "High" in x.index
            and "Low" in x.index
            and "Close" in x.index
            and "Volume" in x.index
        ):

            price_open = round(x.loc["Open"], 2)
            price_high = round(x.loc["High"], 2)
            price_low = round(x.loc["Low"], 2)
            price_close = round(x.loc["Close"], 2)
            price_volume = round(x.loc["Volume"], 2)

            # print(price_open,price_high,price_low,price_close,price_volume)

        else:

            raise Exception("Error in data", "moneyflow analyses, money_flows")

        warnings.filterwarnings("error")

        try:

            money_flow_multiplier = (
                (price_close - price_low) - (price_high - price_close)
            ) / (price_high - price_low)

        except RuntimeWarning:

            return 0
        #
        #
        money_flow_volume = money_flow_multiplier * price_volume

        money_flow_volume = round(money_flow_volume, 0)

        # print( money_flow_multiplier, price_volume , money_flow_volume, money_flow_volume )
        return money_flow_volume

    def money_flow_analyeses(
        self,
        full_run=False,
        test_function=False,
        tail_amount=0,
        length_for_calculation=0,
        return_last_varible_only=False,
        as_profile=False,
        based_on_change=False,
        return_as_number=True,
    ):
        """


        Parameters
        ----------
        full_run : TYPE, optional

            DESCRIPTION.

            with this input turned on, it loads the full analyses and saves it in the dictionary

            The default is False.



        test_function : TYPE, optional

            DESCRIPTION.

            this parrameter is used to test the function, its prints where the function reaches

            The default is False.


        length_for_calculation : TYPE, optional

            DESCRIPTION.

            this parrameter is for synchronize purposes, you can tail the last rows if designers.

            its higly recommanded to not use this function att will, only within synchroinze construction (Never tested)

            The default is 0.

        return_last_varible_only : TYPE, optional

            DESCRIPTION.

            this parrameter can be combined with the profile or change parrameter. Its used for returning the last
            and only value. So if you want to return a normal profile you can use this in cominiation with

            - as profile = true
            - based on change = true
            - return as number

            The default is False.


        as_profile : TYPE, optional


        DESCRIPTION.

        returns as 3 _+ -3 or (NOMRAL , HIGH ,LOW ,EXTREEM HIGH ,EXTREEM LOW)

        The default is False.

        based_on_change : TYPE, optional

            DESCRIPTION.

            uses the change data insted of the outcome of the parrameter,
            so instet of 10,20,10,5 it interpertes as 0, 100%, -100%, -100% and it creates a profile.

            The default is False.
        return_as_number : TYPE, optional
            DESCRIPTION. The default is True.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        # as profile means: Not a indicator data but profile of the data.
        # return last varible only means: that only the last calculation is published

        # route 1. = indicator data time serie.
        # route 2. = profile timeserie  - take the regulare calculations and create a profile of that.
        # route 3. = profile of change-
        # route 4. = profile of last indicator varible
        # route 5. = profile of last change varible

        # all in outcomes are putt in a class dictoinary. That's the most efficiont.

        #
        # if length is 0 the stock data should be parsed. - this function is only for data tail purposes, so very additional and primerly unnessary
        if length_for_calculation == 0:

            #
            # sets the length for the calculations // this function is an additnal function if you skipp tailing.
            if test_function:
                print("Length for calculation is run, block one ")
            length_for_calculation = int(len(self.stock_data))

        #
        # hier word de werk data ge-set / here the data becomes set.
        workdata = self.stock_data.iloc[
            len(self.stock_data)
            - length_for_calculation : len(self.stock_data)
        ]

        #
        # the list of calculations
        self.calculations = []

        #
        # boots converter object
        data_converter = support_functions.data_modifications()

        if self.synchronize and not self.first_run and tail_amount > 0:

            # load the dictonaty, list the calculations and put them in the list. - taild to weekly format -

            #
            # loads dict data
            data_from_dict = self.analyeses_dictionary[
                "indicator_timeserie_raw"
            ]
            #
            # pushed converted data into analyses list
            self.calculations = (
                data_converter.convert_nested_analeses_dict_data_to_list(
                    data_from_dict
                )
            )

            # - --- -- There needs to be a solution for if the first run is done.

        #
        # the list of profiles.
        self.calculations_profile = []

        if self.synchronize and not self.first_run and tail_amount > 0:

            # load the dictonaty, list the calculations and put them in the list. - taild to weekly format -

            #
            # loads dict data
            data_from_dict = self.analyeses_dictionary[
                "indicator_timeserie_profile"
            ]
            #
            # pushes the data in list, just like above here.
            self.calculations_profile = (
                data_converter.convert_nested_analeses_dict_data_to_list(
                    data_from_dict
                )
            )

        #
        # rate of change calculation
        self.calculations_profile_change = []

        if self.synchronize and not self.first_run and tail_amount > 0:

            # load the dictonaty, list the calculations and put them in the list. - taild to weekly format -

            #
            # loads dict data
            data_from_dict = self.analyeses_dictionary[
                "indicator_timeserie_profile_change"
            ]
            #
            # pushes the data in list, just like above here.
            self.calculations_profile_change = (
                data_converter.convert_nested_analeses_dict_data_to_list(
                    data_from_dict
                )
            )

            # - --- -- There needs to be a solution for if the first run is done.

        # loops true the dataset.
        # returns the outcome of the calculation.
        # checks if hte
        ##########################################################

        #
        # loops true the data set.
        if (
            tail_amount == 0
        ):  # and synch and not first run                                                   # this means that the synchronisation is turned on.
            for x in range(0, len(workdata)):

                outcome = 0
                # calculates the normal indicator
                #
                # returns the normal indicator
                outcome = self.money_flow_with_row(workdata.iloc[x])

                if outcome == 0:
                    self.calculations.append(0)

                    self.calculations_profile.append(0)

                    self.calculations_profile_change.append(0)

                    continue
                #
                # if function is tested.
                if test_function:
                    print("Normal outcome is tested")
                #
                # check if outcome is equal to zero.
                self.calculations.append(outcome)

                #
                # calculates the profile. if its not changed based and if it's not the last varible only.
                if (
                    as_profile == True
                    and based_on_change != True
                    and return_last_varible_only != True
                    or full_run == True
                ):

                    #
                    # if function is tested.
                    if test_function:
                        print("calculating profile")

                    #
                    # returns the profile if the a
                    outcome_profile = self.return__profile(
                        data=self.calculations,
                        test_function=test_function,
                        length_for_calculation=length_for_calculation,
                        return_outcome_as_number=return_as_number,
                    )
                    #
                    # adds the calculation to the profile.
                    self.calculations_profile.append(outcome_profile)

                #
                # calculates the profile based on change.
                if (
                    as_profile == True
                    and based_on_change == True
                    and return_last_varible_only != True
                    or full_run == True
                ):

                    #
                    #
                    self.outcome_profile_change = self.return__profile(
                        data=self.calculations,
                        test_function=test_function,
                        length_for_calculation=length_for_calculation,
                        return_outcome_as_number=return_as_number,
                        based_on_change=True,
                    )
                    #
                    # if there is no thing marked, it can just roll
                    self.calculations_profile_change.append(
                        self.outcome_profile_change
                    )
                    #
                    #
                    #
                    # if function is tested
                    if test_function:
                        #
                        # prints where the ill is.
                        print("Calculating change")
                        # breaks loop
                        break
                else:
                    continue

        # the synchronization is started.
        else:

            for x in range(len(workdata) - tail_amount, len(workdata)):

                outcome = 0
                # calculates the normal indicator
                #

                # returns the normal indicator
                outcome = self.money_flow_with_row(workdata.iloc[x])

                if outcome == 0:

                    self.calculations.append(0)

                    self.calculations_profile.append(0)

                    self.calculations_profile_change.append(0)

                    continue

                #
                # if function is tested.
                if test_function:
                    print("Normal outcome is tested")
                #
                # check if outcome is equal to zero.
                self.calculations.append(outcome)

                #
                # calculates the profile. if its not changed based and if it's not the last varible only.
                if (
                    as_profile == True
                    and based_on_change != True
                    and return_last_varible_only != True
                    or full_run == True
                ):

                    #
                    # if function is tested.
                    if test_function:
                        print("calculating profile")

                    #
                    # returns the profile if the a
                    try:

                        outcome_profile = self.return__profile(
                            data=self.calculations,
                            test_function=test_function,
                            length_for_calculation=length_for_calculation,
                            return_outcome_as_number=return_as_number,
                        )

                    except Exception as inst:

                        print(type(inst))
                        print(inst.args)
                        print(inst)

                    #
                    # adds the calculation to the profile.
                    self.calculations_profile.append(outcome_profile)

                # calculates the profile based on change.
                if (
                    as_profile == True
                    and based_on_change == True
                    and return_last_varible_only != True
                    or full_run == True
                ):

                    #
                    #
                    self.outcome_profile_change = self.return__profile(
                        data=self.calculations,
                        test_function=test_function,
                        length_for_calculation=length_for_calculation,
                        return_outcome_as_number=return_as_number,
                        based_on_change=True,
                    )
                    #
                    # if there is no thing marked, it can just roll
                    self.calculations_profile_change.append(
                        self.outcome_profile_change
                    )
                    #
                    #
                    #
                    # if function is tested

                    if test_function:
                        #
                        # prints where the ill is.
                        print("Calculating change")
                        # breaks loop
                        break
                else:
                    continue

        if full_run == True:
            if test_function:
                print("Runn full function is accesed")
                return
            #
            # receives the last varible
            self.analyeses_dictionary[
                "last_calculation_indicator"
            ] = self.calculations[len(self.calculations) - 1]
            #
            # receives the last profile - as text NORMAL/HIGH ect( Its calculated so thats why)
            self.analyeses_dictionary[
                "last_calculation_profile_indicator_text"
            ] = self.return__profile(
                data=self.calculations,
                based_on_change=False,
                return_outcome_as_number=False,
                automatic_use_time_standards=self.use_automatic_time,
            )
            #
            # receives the last profile - as a number
            self.analyeses_dictionary[
                "last_calculation_profile_indicator_number"
            ] = self.return__profile(
                data=self.calculations,
                based_on_change=False,
                return_outcome_as_number=True,
                automatic_use_time_standards=self.use_automatic_time,
            )
            #
            # reveices the last profile based on change, marked as a text.
            self.analyeses_dictionary[
                "last_calculation_profile_change_text"
            ] = self.return__profile(
                data=self.calculations,
                based_on_change=True,
                return_outcome_as_number=False,
                automatic_use_time_standards=self.use_automatic_time,
            )
            #
            # receives the last profile based on change number.
            self.analyeses_dictionary[
                "last_calculation_profile_change_number"
            ] = self.return__profile(
                data=self.calculations,
                based_on_change=True,
                return_outcome_as_number=True,
                automatic_use_time_standards=self.use_automatic_time,
            )
            #
            # timeserie of the indicator data
            self.analyeses_dictionary[
                "indicator_timeserie_raw"
            ] = self.convert_data_to_dataframe(self.calculations)
            #
            # timeserie of the indicator data
            self.analyeses_dictionary[
                "indicator_timeserie_profile"
            ] = self.convert_data_to_dataframe(self.calculations_profile)
            #
            # time serie
            self.analyeses_dictionary[
                "indicator_timeserie_profile_change"
            ] = self.convert_data_to_dataframe(
                self.calculations_profile_change
            )
            #
            # creates the data_serie for change

            # prepair data
            list_for_calculation = self.calculations
            #
            # remove 0 in case it doenst work
            list_for_calculation = [
                i if i != 0 else 0.01 for i in list_for_calculation
            ]
            #
            # does the calculations nanual
            list_for_convertation = [
                a1 - a2
                for a1, a2 in zip(
                    list_for_calculation[1:], list_for_calculation
                )
            ]
            #
            # round the numbers.
            list_for_convertation = [
                round(num, 2) for num in list_for_convertation
            ]
            #
            # convert the session.
            indicator_timeserie_change = self.convert_data_to_dataframe(
                data=list_for_convertation
            )
            # removes NA's
            indicator_timeserie_change = indicator_timeserie_change.fillna(0)

            self.analyeses_dictionary[
                "indicator_timeserie_change"
            ] = indicator_timeserie_change
            #
            # saves synch

            # print("here is the analyses", self.analyeses_dictionary)
            if self.synchronize:

                # creates name extrention
                data_extention = self.data_extention = (
                    self.timeframe + self.name_of_analyeses + "_dictonary"
                )

                # creates data object

                self.synch_object = synch_class.data_synch(
                    path=constants.CORE_DATA_____PATH,
                    subfolder="stock_analyses_data",
                    ticker=self.stock_ticker,
                    data_extention=data_extention,
                )

                if self.first_run == True:

                    # adds data
                    self.synch_object.synchronized_data = (
                        self.analyeses_dictionary
                    )
                    self.synch_object.new_data = self.analyeses_dictionary
                    self.synch_object.save_data()

                else:

                    self.synch_object.synchronized_data = (
                        self.analyeses_dictionary
                    )
                    self.synch_object.new_data = self.analyeses_dictionary
                    self.synch_object.save_data()
                # saves data

                """
                Uncomment this and you will save the data. So do this on the end. 
                """
                self.synch_object.save_data()

            #
            #
            return self.analyeses_dictionary

        #
        # ( Loose varibles ) returns the last varilble. ( This can be used for sector wide researches. )
        if return_last_varible_only == True and return_as_number == False:
            #
            # tests te fuction
            if test_function:
                #
                # prints the message
                print("return last varible is tested")
                return

            #
            # returns the last varible
            outcome = self.calculations[len(self.calculations) - 1]
            #
            #
            return outcome

        #
        # ( Loose varible ) returns loosse and last profile as number( This can be used for the dashboard).
        elif (
            as_profile == True
            and based_on_change != True
            and return_last_varible_only == True
            and return_as_number != True
        ):

            if test_function:
                print("returns last profile number")
                return
            #
            # returns the last profile, as text
            outcome = self.return__profile(
                data=self.calculations,
                based_on_change=False,
                return_outcome_as_number=False,
                automatic_use_time_standards=self.use_automatic_time,
            )
            #
            #
            return outcome
        #
        # (Loos varible) returns loose profile as text
        elif (
            as_profile == True
            and based_on_change != True
            and return_last_varible_only == True
            and return_as_number != True
        ):

            #
            # returns profile as number
            if test_function:
                print("Returns last profile as number")
                return
            #
            # returns the last profile, as text
            outcome = self.return__profile(
                data=self.calculations,
                based_on_change=False,
                return_outcome_as_number=True,
                automatic_use_time_standards=self.use_automatic_time,
            )
            #
            #
            return outcome

        # returns regular time serie. So hard numbers - no profiles - and date's included.
        elif (
            as_profile != True
            and based_on_change != True
            and return_last_varible_only != True
            and return_as_number != True
        ):

            if test_function:
                print("Returns indicator time serie")
                return
            #
            # packages the calculations
            outcome = self.convert_data_to_dataframe(self.calculations)
            #
            # returs the timeserie.
            return outcome

        #
        # return the time serie as profiled
        elif (
            as_profile != True
            and based_on_change != True
            and return_last_varible_only != True
            and return_as_number != True
        ):
            if test_function:

                print("Returns profiled timeserie")

                return
            #
            # packages the calculations
            outcome = self.convert_data_to_dataframe(self.outcome_profile)
            #
            # returs the timeserie of profile.
            return outcome

        #
        #
        # self.moneyflow_data_set = self.calculations

        # if calculations_profile != []:

        #    self.moneyflow_profile_data = self.calculations_profile

        # self.moneyflow_profile_change_data = self.outcome_profile_change

        # self.moneyflow_data_loaded = True

        # self.convert_data_to_dataframe(self.calculations)

        # convert the data into dataframes.

        #
        # if function is tested
        if test_function:
            print("Reaches end of function")
            return

        return self.calculations

    def return__profile(
        self,
        data=None,
        test_function=False,
        length_for_calculation=0,
        return_outcome_as_number=False,
        based_on_change=False,
        automatic_use_time_standards=True,
    ):

        global ts
        #
        # sets time serie data
        ts = data

        # print("\n\n this is the incomming len", len(ts))

        ###### Converts the data to data of change or melts the data to the timeframe of wish. #############################################################################
        #
        #
        # packages the data in dataframe
        df_ts = self.convert_data_to_dataframe(data=ts)

        #
        # for test function
        if test_function:
            print(
                "in profiler function the timeseries is converted to dataframe"
            )
        #
        # checks if it based on change
        if based_on_change == True and len(data) >= 2:
            #
            # for test function
            if test_function:
                print(
                    "in profiler function the timeseries is converted to changed time serie"
                )
            #
            # prepair data
            list_for_calculation = data
            #
            # remove 0 in case it doenst work
            list_for_calculation = [
                i if i != 0 else 0.01 for i in list_for_calculation
            ]
            #
            # does the calculations nanual
            list_for_convertation = [
                a1 - a2
                for a1, a2 in zip(
                    list_for_calculation[1:], list_for_calculation
                )
            ]
            #
            # round the numbers.
            list_for_convertation = [
                round(num, 2) for num in list_for_convertation
            ]
            #
            # convert the session.
            df_ts = self.convert_data_to_dataframe(data=ts)

        #
        # checks if the data needs to be tailed by date, only possible if not turend of and commanded
        if (
            automatic_use_time_standards == True
            and type(self.timeframe) != None
        ):

            #
            # for test function
            if test_function:
                print(
                    "in profiler function the timeseries the periode is converted to the timeframe "
                )

            #
            # if matches the weekly peride
            if self.timeframe == "D":
                #
                # tails to 1D in weeks
                df_ts = df_ts.tail(251)

            #
            # if matches the weekly peride
            if self.timeframe == "W":
                #
                # tails to 1y in weeks
                df_ts = df_ts.tail(51)
            #
            # if matches the montly periode
            if self.timeframe == "M":
                #
                # if
                df_ts = df_ts.tail(12)
            #
            # if machtes with the one q periode
            if self.timeframe == "Q":
                df_ts = df_ts.tail(4)
            #
            # if machtes with the one year periode
            if self.timeframe == "Y":
                df_ts = df_ts.tail(10)

        # print("this is the len of the dataframe ", len(df_ts))
        #
        # reconvert to list.
        ts = df_ts.values.tolist()

        # print("\n\n this is the incomming len after pars", len(ts))
        #
        #
        ##################################################################################################################################################################

        #
        # extracts the data for list size.
        if type(ts) != list:
            #
            # for test function
            if test_function:
                print(
                    "in profiler function the timeseries is converted to list"
                )
            #
            # changes the data type
            ts = ts.to_list()

        #
        # extracts the length for the calculation if required. Can be 0 if not used.
        if length_for_calculation != 0:

            #
            # for test function
            if test_function:
                print(
                    "in profiler function the timeseries is converted to lenght by imput"
                )
            #
            # just tries to cutt the length. This is already done above but for certain synchorinzation methodes it can be usefull.
            try:
                #
                #
                ts = ts[len(ts) - length_for_calculation + 1 : len(ts) - 1]

            except:
                #
                # if it fails, just return 0 or normal.
                if return_outcome_as_number != False:

                    #
                    #
                    status = 0

                    #
                else:

                    #
                    #
                    status = "NORMAL"
                return status

        #
        # checks if the lenght is long enough
        if len(ts) <= 2:

            #
            # for test function
            if test_function:
                print(
                    "in profiler function the timeseries is errored out because of a len error"
                )
            #
            # sets to status normal
            status = "NORMAL"
            #
            # check wich return time
            if return_outcome_as_number != False:

                status = 0

            return status

        ###### solves nested problem if appears

        #
        # if nested, this will run
        if any(isinstance(ts, list) for i in ts):
            #
            # if nested this will run
            ts = [ts for ts in ts for ts in ts]

            if test_function:
                print("the timeserie data is de-nested")
        #

        ######

        ###### profiles the data ( Normal even destribution unskewed) #############################################################

        last_attempt = ts[len(ts) - 1]
        #
        # removes NA.
        ts = [ts for ts in ts if str(ts) != "nan"]
        #
        # extract averages.
        average = avg = round(sum(ts) / len(ts), 2)
        #
        # gets standaard devetion.

        std = np.std(ts)
        #
        # extracts the minimum
        minn = min(ts)
        #
        # extraxts the maximum
        maxx = max(ts)
        #
        # print("AVG = ",average, "STD =", std, "MAX = ",maxx)
        extreme_high = average + (3 * std)
        strong_high = average + (2 * std)
        normal_high = average + (1 * std)
        normal = average = avg
        normal_low = average - (1 * std)
        strong_low = average - (2 * std)
        extreme_low = average - (3 * std)

        last_month = last_attempt

        #
        # checks if one of the values is NA -- made after an terrible error occured.
        if math.isnan(average) or math.isnan(std):

            #
            # if this codes runs its clear that there is something really wrong

            #
            #
            if test_function == True:
                print("profiler, there is an error occured")

            #
            # sets normal status
            status = "NORMAL"

            if return_outcome_as_number != False:
                status = 0

        # print("\n\n", last_attempt, " =  This is the last attemt")
        # print( "Average ", average ," std" ,std, " P", length_for_calculation, "lAST = ", last_month )

        if last_month >= normal_low and last_month <= normal_high:
            status = "NORMAL"
            if return_outcome_as_number != False:
                status = 0

        if last_month >= strong_low and last_month <= normal_low:
            status = "LOW"
            if return_outcome_as_number != False:
                status = -1

        if last_month <= strong_low and last_month >= extreme_low:
            status = "STRONG_LOW"
            if return_outcome_as_number != False:
                status = -2
        if last_month <= extreme_low:
            status = "EXTREME_LOW"
            if return_outcome_as_number != False:
                status = -3
        if last_month <= strong_high and last_month >= normal_high:
            status = "HIGH"
            if return_outcome_as_number != False:
                status = 1

        if last_month >= strong_high and last_month <= extreme_high:
            status = "STRONG_HIGH"
            if return_outcome_as_number != False:
                status = 2

        if last_month >= extreme_high:
            status = "EXTREME_HIGH"
            if return_outcome_as_number != False:
                status = 3

        ######  End distribution ####################################################################################################################################################

        # print(status)
        # print( status, "= status, Average =", average ," std" ,std, " P",  length_for_calculation, "lAST = ", last_month, " the len of the time serie =" , len(ts) )

        return status

    def convert_data_to_dataframe(self, data=None):

        #
        # tails the data so it matches with the amount of data.

        idata = self.stock_data.tail(len(data))
        #
        # sets data to an other vairble
        ldata = data

        #
        # creates a data frame ()
        ldataf = pd.DataFrame(ldata)

        ldataf = ldataf.tail(len(idata))

        #
        # uses index
        data_index = idata.index

        """ Hier onder zit de fout. """

        # datadasframe = pd.DataFrame(index=datesindex, data=ldataf.values)
        the_created_dataframe = pd.DataFrame(
            index=data_index, data=ldataf.values
        )

        #
        # sets data frame to class object

        self.data_frame = the_created_dataframe
        #
        # changes the name of the colums

        self.data_frame.columns = ["Data"]
        #
        # replaces the Na's with zero's ( Ment for the change dataframe)
        self.data_frame["Data"] = self.data_frame["Data"].fillna(0)

        return self.data_frame


class liquidity_impact:
    """


    TASKS
    - twitter module
    - plot module.

    NOTES:
        full function is gestest.

    """

    # fundamental data
    name_of_analyses = "LIQUIDTY"

    # stockdata details.
    stock_ticker = None
    stock_data = None
    timeframe = None

    # data dictionary
    analyeses_dictionary = {}

    # tools
    profiler = None

    # twitter details
    text_for_twitter = None
    link_for_image = None

    synchronize: bool = False
    first_run: bool = False

    use_automatic_time = True

    use_automatic_time = (
        True  # can be used to help set profiles easy. If turend off ignored.
    )

    def __init__(
        self,
        stock_ticker="",
        stock_data=None,
        synchronize=False,
        timeframe="D = daily, W = Weekly, M = montly, Q = quarterly, Y = yearly",
    ):
        """


        Parameters
        ----------
        stock_ticker : TYPE, optional
            DESCRIPTION. The default is "".
        stock_data : TYPE, optional
            DESCRIPTION. The default is None.
        synchronize : TYPE, optional
            DESCRIPTION. The default is False.
        timeframe : TYPE, optional
            DESCRIPTION. The default is "D = daily, W = Weekly, M = montly, Q = quarterly, Y = yearly".

        Returns
        -------
        None.

        """

        # technical data for calculations

        # sets system varibles
        self.stock_data = stock_data

        #
        # sets ticker ovject
        self.stock_ticker = stock_ticker

        #
        # check if stock_data is not
        if stock_data is not None:
            self.profiler = profiling(
                stock_data=stock_data, timeframe=timeframe
            )
        else:
            raise Exception(
                "Ticker_None",
                "This error occures when ticker is Nonetype object",
            )

        #
        #
        self.synchronize = synchronize
        #
        # check if time frame is filled in well
        if (
            timeframe
            == "D = daily, W = Weekly, M = montly, Q = quarterly, Y = yearly"
        ):
            #
            # if it fails it marks it down as non
            self.timeframe = None
            #
            # if timeframe is filled in, it needs to be assinged.
        elif (
            timeframe == "D"
            or timeframe == "W"
            or timeframe == "M"
            or timeframe == "Y"
        ):
            #
            # if it fits, it assings.
            self.timeframe = timeframe

            # check if formate time serie is right
            if self.timeframe == "W":
                if type(pd.infer_freq(self.stock_data.index)) != str:
                    raise Exception(
                        "Time formate is wrong, analyses dident run"
                    )
                elif "W" not in pd.infer_freq(self.stock_data.index):

                    raise Exception(
                        "Time formate is wrong, probably something else the nweekly"
                    )

        else:
            #
            # sets the timeframe tonon
            self.timeframe = None

        # creates name extrention
        data_extention = self.data_extention = (
            self.timeframe + self.name_of_analyses + "_dictonary"
        )

        # creates data object
        self.synch_object = synch_class.data_synch(
            path=constants.CORE_DATA_____PATH,
            subfolder="stock_analyses_data",
            ticker=self.stock_ticker,
            data_extention=data_extention,
        )

        if not self.synchronize:
            print("the data is new")
            # set first run to true
            self.first_run = True
            # starts full analyses.
            self.liquidity_impact_analyeses(full_run=True)

        # if data is new refresh.
        if self.synch_object.is_data_new:

            print("the data is new")
            # set first run to true
            self.first_run = True
            # starts full analyses.
            self.liquidity_impact_analyeses(full_run=True)
            return

        # checks if the data is not new and, if the timeframe is defined and synch is true.
        elif (
            not self.synch_object.is_data_new
            and type(timeframe) != None
            and synchronize
        ):
            if not self.synch_object.return_last_modification_file(
                view=timeframe, experiation_bool=True
            ):
                print("the data is booted and known")
                self.analyeses_dictionary = self.synch_object.retreived_data
                return
            else:
                print("the data known but expired")

                # prepair the data for checking the experation.
                self.analyeses_dictionary = self.synch_object.retreived_data

                # check if data is legid
                if not self.synch_object.check_incomming_dict_legit(
                    self.analyeses_dictionary
                ):

                    self.first_run = True
                    # starts full analyses.
                    self.liquidity_impact_analyeses(full_run=True)

                # set indicator
                indicator = self.analyeses_dictionary[
                    "indicator_timeserie_raw"
                ]

                # get tge amount expired
                amount_of_expired = self.synch_object.time_bewteen_time_series(
                    indicator, self.stock_data, self.timeframe
                )

                # if ammount is 0, section mabey run because time passed but because of weekend, no data is missing.
                if amount_of_expired == 0:
                    return

                else:
                    # if amount of data is missing - because its monday, it will work
                    self.liquidity_impact_analyeses(
                        full_run=True, tail_amount=amount_of_expired
                    )

                return

        return

    def liquidty_analyses_with_row(self, data_row=""):
        """


        # explaind. Eigenschappen:
            # het getal word groter als of de impact groter wordt. of het aantal shares lager wordt.
            # met andere woorden, hoe hoger de score , of hoe minder shares er gedaan zijn

        Parameters
        ----------
        data_row : TYPE, optional
            DESCRIPTION. The default is "".

        Returns
        -------
        TYPE
            DESCRIPTION.

        """

        #
        # converts the data
        x = data_row

        #
        # checking if the data is deliverd
        if type(data_row) == None:
            #
            # couting if the data is not revieved.
            print("No data received in moneyflow anallyses ticker")

        #
        # checking if data is in the right formate.
        if isinstance(data_row, pd.core.series.Series) == False:
            print("Giant error, wrong formate in eqaution")

        #
        # checking if the columns fitt
        if (
            "Open" in x.index
            and "High" in x.index
            and "Low" in x.index
            and "Close" in x.index
            and "Volume" in x.index
        ):

            price_open = x.loc["Open"]
            price_high = x.loc["High"]
            price_low = x.loc["Low"]
            price_close = x.loc["Close"]
            price_adjusted_close = x.loc["Adj Close"]
            price_volume = x.loc["Volume"]
            price_change = x.loc["Change"]

            #
            # fixing the potential first open bug.
            if price_open == 0.0:
                #
                # setting the price right
                price_open = 0.01

            # fixing the change 0 bugg.
            if price_change == 0.0:
                #
                # fixing the bug
                price_change = ((price_close - price_open) / price_open) * 100

            # start eqation

            volume_in_capital = price_volume * price_adjusted_close
            volume_in_hondermilions = volume_in_capital / 100000000

            # print(volume_in_hondermilions, " = the fvolume and this is the change", price_change )
            # precent devide true 0.
            if price_change == 0.00 or volume_in_hondermilions == 0.000000000:

                # print("The wrong one is send")
                return 0

            ## doest the equation.
            equation = price_change / volume_in_hondermilions

            # print("The right one should be send")
            return equation

        else:
            print("Error should return")
            # or returns error.
            return ("Error", 501)

    def liquidity_impact_analyeses(
        self,
        full_run=False,
        test_function=False,
        tail_amount=0,
        length_for_calculation=0,
        return_last_varible_only=False,
        as_profile=False,
        based_on_change=False,
        return_as_number=True,
    ):
        """


        Parameters
        ----------
        full_run : TYPE, optional

            DESCRIPTION.

            with this input turned on, it loads the full analyses and saves it in the dictionary

            The default is False.



        test_function : TYPE, optional

            DESCRIPTION.

            this parrameter is used to test the function, its prints where the function reaches

            The default is False.


        length_for_calculation : TYPE, optional

            DESCRIPTION.

            this parrameter is for synchronize purposes, you can tail the last rows if designers.

            its higly recommanded to not use this function att will, only within synchroinze construction (Never tested)

            The default is 0.

        return_last_varible_only : TYPE, optional

            DESCRIPTION.

            this parrameter can be combined with the profile or change parrameter. Its used for returning the last
            and only value. So if you want to return a normal profile you can use this in cominiation with

            - as profile = true
            - based on change = true
            - return as number

            The default is False.


        as_profile : TYPE, optional


        DESCRIPTION.

        returns as 3 _+ -3 or (NOMRAL , HIGH ,LOW ,EXTREEM HIGH ,EXTREEM LOW)

        The default is False.

        based_on_change : TYPE, optional

            DESCRIPTION.

            uses the change data insted of the outcome of the parrameter,
            so instet of 10,20,10,5 it interpertes as 0, 100%, -100%, -100% and it creates a profile.

            The default is False.
        return_as_number : TYPE, optional
            DESCRIPTION. The default is True.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        # as profile means: Not a indicator data but profile of the data.
        # return last varible only means: that only the last calculation is published

        # route 1. = indicator data time serie.
        # route 2. = profile timeserie  - take the regulare calculations and create a profile of that.
        # route 3. = profile of change-
        # route 4. = profile of last indicator varible
        # route 5. = profile of last change varible

        # all in outcomes are putt in a class dictoinary. That's the most efficiont.

        # if length is 0 the stock data should be parsed.
        if length_for_calculation == 0:

            if test_function:
                print("Length for calculation is run, block one ")

            length_for_calculation = int(len(self.stock_data) - 1)

        #
        #
        workdata = self.stock_data.iloc[
            len(self.stock_data)
            - length_for_calculation : len(self.stock_data)
        ]

        #
        # the list of calculations
        self.calculations = []
        #
        # the list of profiles.
        self.calculations_profile = []
        #
        #
        self.calculations_profile_change = []

        #
        # the list of calculations
        self.calculations = []

        #
        # boots converter object
        data_converter = support_functions.data_modifications()

        if self.synchronize and not self.first_run and tail_amount > 0:

            # load the dictonaty, list the calculations and put them in the list. - taild to weekly format -

            #
            # loads dict data
            data_from_dict = self.analyeses_dictionary[
                "indicator_timeserie_raw"
            ]
            #
            # pushed converted data into analyses list
            self.calculations = (
                data_converter.convert_nested_analeses_dict_data_to_list(
                    data_from_dict
                )
            )

            # - --- -- There needs to be a solution for if the first run is done.

        #
        # the list of profiles.
        self.calculations_profile = []

        if self.synchronize and not self.first_run and tail_amount > 0:

            # load the dictonaty, list the calculations and put them in the list. - taild to weekly format -

            #
            # loads dict data
            data_from_dict = self.analyeses_dictionary[
                "indicator_timeserie_profile"
            ]
            #
            # pushes the data in list, just like above here.
            self.calculations_profile = (
                data_converter.convert_nested_analeses_dict_data_to_list(
                    data_from_dict
                )
            )

        #
        # rate of change calculation
        self.calculations_profile_change = []

        if self.synchronize and not self.first_run and tail_amount > 0:

            # load the dictonaty, list the calculations and put them in the list. - taild to weekly format -

            #
            # loads dict data
            data_from_dict = self.analyeses_dictionary[
                "indicator_timeserie_profile_change"
            ]
            #
            # pushes the data in list, just like above here.
            self.calculations_profile_change = (
                data_converter.convert_nested_analeses_dict_data_to_list(
                    data_from_dict
                )
            )

            # - --- -- There needs to be a solution for if the first run is done.

        # loops true the dataset.
        # returns the outcome of the calculation.
        # checks if hte
        ##########################################################

        # loops true the dataset.
        # returns the outcome of the calculation.
        # checks if hte

        #
        # loops true the data set.
        if tail_amount == 0:

            for x in range(0, len(workdata)):

                # calculates the normal indicator
                #
                # returns the normal indicator
                outcome = self.liquidty_analyses_with_row(workdata.iloc[x])

                #
                # if function is tested.
                if test_function:
                    print("Normal outcome is tested")
                #
                # check if outcome is equal to zero.
                self.calculations.append(outcome)
                # print(outcome, " I s the outcome")
                #
                # calculates the profile. if its not changed based and if it's not the last varible only.
                if (
                    as_profile == True
                    and based_on_change != True
                    and return_last_varible_only != True
                    or full_run == True
                ):

                    #
                    # if function is tested.
                    if test_function:
                        print("calculating profile")

                    #
                    # returns the profile if the a
                    outcome_profile = self.profiler.return__profile(
                        data=self.calculations,
                        test_function=test_function,
                        length_for_calculation=length_for_calculation,
                        return_outcome_as_number=return_as_number,
                    )
                    #
                    # adds the calculation to the profile.
                    self.calculations_profile.append(outcome_profile)

                #
                # calculates the profile based on change.
                if (
                    as_profile == True
                    and based_on_change == True
                    and return_last_varible_only != True
                    or full_run == True
                ):

                    #
                    #
                    self.outcome_profile_change = (
                        self.profiler.return__profile(
                            data=self.calculations,
                            test_function=test_function,
                            length_for_calculation=length_for_calculation,
                            return_outcome_as_number=return_as_number,
                            based_on_change=True,
                        )
                    )
                    #
                    # if there is no thing marked, it can just roll
                    self.calculations_profile_change.append(
                        self.outcome_profile_change
                    )
                    #
                    #
                    #
                    # if function is tested
                    if test_function:
                        #
                        # prints where the ill is.
                        print("Calculating change")
                        # breaks loop
                        break
                else:
                    continue

        else:
            for x in range(len(workdata) - tail_amount, len(workdata)):

                # calculates the normal indicator
                #
                # returns the normal indicator
                outcome = self.liquidty_analyses_with_row(workdata.iloc[x])

                #
                # if function is tested.
                if test_function:
                    print("Normal outcome is tested")
                #
                # check if outcome is equal to zero.
                self.calculations.append(outcome)
                # print(outcome, " I s the outcome")
                #
                # calculates the profile. if its not changed based and if it's not the last varible only.
                if (
                    as_profile == True
                    and based_on_change != True
                    and return_last_varible_only != True
                    or full_run == True
                ):

                    #
                    # if function is tested.
                    if test_function:
                        print("calculating profile")

                    #
                    # returns the profile if the a
                    outcome_profile = self.profiler.return__profile(
                        data=self.calculations,
                        test_function=test_function,
                        length_for_calculation=length_for_calculation,
                        return_outcome_as_number=return_as_number,
                    )
                    #
                    # adds the calculation to the profile.
                    self.calculations_profile.append(outcome_profile)

                #
                # calculates the profile based on change.
                if (
                    as_profile == True
                    and based_on_change == True
                    and return_last_varible_only != True
                    or full_run == True
                ):

                    #
                    #
                    self.outcome_profile_change = (
                        self.profiler.return__profile(
                            data=self.calculations,
                            test_function=test_function,
                            length_for_calculation=length_for_calculation,
                            return_outcome_as_number=return_as_number,
                            based_on_change=True,
                        )
                    )
                    #
                    # if there is no thing marked, it can just roll
                    self.calculations_profile_change.append(
                        self.outcome_profile_change
                    )
                    #
                    #
                    #
                    # if function is tested
                    if test_function:
                        #
                        # prints where the ill is.
                        print("Calculating change")
                        # breaks loop
                        break
                else:
                    continue
        # loops end.
        # self.calculations = [round(num, 5) for num in  self.calculations]

        if full_run == True:
            if test_function:
                print("Runn full function is accesed")
                return
            #
            # receives the last varible
            self.analyeses_dictionary[
                "last_calculation_indicator"
            ] = self.calculations[len(self.calculations) - 1]
            #
            # receives the last profile - as text NORMAL/HIGH ect( Its calculated so thats why)
            self.analyeses_dictionary[
                "last_calculation_profile_indicator_text"
            ] = self.profiler.return__profile(
                data=self.calculations,
                based_on_change=False,
                return_outcome_as_number=False,
                automatic_use_time_standards=self.use_automatic_time,
            )
            #
            # receives the last profile - as a number
            self.analyeses_dictionary[
                "last_calculation_profile_indicator_number"
            ] = self.profiler.return__profile(
                data=self.calculations,
                based_on_change=False,
                return_outcome_as_number=True,
                automatic_use_time_standards=self.use_automatic_time,
            )
            #
            # reveices the last profile based on change, marked as a text.
            self.analyeses_dictionary[
                "last_calculation_profile_change_text"
            ] = self.profiler.return__profile(
                data=self.calculations,
                based_on_change=True,
                return_outcome_as_number=False,
                automatic_use_time_standards=self.use_automatic_time,
            )
            #
            # receives the last profile based on change number.
            self.analyeses_dictionary[
                "last_calculation_profile_change_number"
            ] = self.profiler.return__profile(
                data=self.calculations,
                based_on_change=True,
                return_outcome_as_number=True,
                automatic_use_time_standards=self.use_automatic_time,
            )
            #
            # timeserie of the indicator data
            self.analyeses_dictionary[
                "indicator_timeserie_raw"
            ] = self.convert_data_to_dataframe(self.calculations)
            #
            # timeserie of the indicator data
            self.analyeses_dictionary[
                "indicator_timeserie_profile"
            ] = self.convert_data_to_dataframe(self.calculations_profile)
            #
            # time serie
            self.analyeses_dictionary[
                "indicator_timeserie_profile_change"
            ] = self.convert_data_to_dataframe(
                self.calculations_profile_change
            )
            #
            # creates the data_serie for change
            indicator_timeserie_change = self.convert_data_to_dataframe(
                self.calculations
            )
            # changes value to value of change
            indicator_timeserie_change = (
                indicator_timeserie_change.pct_change()
            )
            # removes NA's
            indicator_timeserie_change = indicator_timeserie_change.fillna(0)

            self.analyeses_dictionary[
                "indicator_timeserie_change"
            ] = indicator_timeserie_change

            #
            #
            if self.synchronize:

                # creates name extrention
                data_extention = self.data_extention = (
                    self.timeframe + self.name_of_analyses + "_dictonary"
                )

                # creates data object
                self.synch_object = synch_class.data_synch(
                    path=constants.CORE_DATA_____PATH,
                    subfolder="stock_analyses_data",
                    ticker=self.stock_ticker,
                    data_extention=data_extention,
                )

                print("point touched")
                if self.first_run == True:

                    # adds data
                    self.synch_object.synchronized_data = (
                        self.analyeses_dictionary
                    )
                    self.synch_object.new_data = self.analyeses_dictionary
                    self.synch_object.save_data()

                else:

                    self.synch_object.synchronized_data = (
                        self.analyeses_dictionary
                    )
                    self.synch_object.new_data = self.analyeses_dictionary
                    self.synch_object.save_data()
                # saves data

                """
                Uncomment this and you will save the data. So do this on the end. 
                """
                self.synch_object.save_data()

            #
            #
            return self.analyeses_dictionary

        #
        # ( Loose varibles ) returns the last varilble. ( This can be used for sector wide researches. )
        if return_last_varible_only == True and return_as_number == False:
            #
            # tests te fuction
            if test_function:
                #
                # prints the message
                print("return last varible is tested")
                return

            #
            # returns the last varible
            outcome = self.calculations[len(self.calculations) - 1]
            #
            #
            return outcome

        #
        # ( Loose varible ) returns loosse and last profile as number( This can be used for the dashboard).
        elif (
            as_profile == True
            and based_on_change != True
            and return_last_varible_only == True
            and return_as_number != True
        ):

            if test_function:
                print("returns last profile number")
                return
            #
            # returns the last profile, as text
            outcome = self.return__profile(
                data=self.calculations,
                based_on_change=False,
                return_outcome_as_number=False,
                automatic_use_time_standards=self.use_automatic_time,
            )
            #
            #
            return outcome
        #
        # (Loos varible) returns loose profile as text
        elif (
            as_profile == True
            and based_on_change != True
            and return_last_varible_only == True
            and return_as_number != True
        ):

            #
            # returns profile as number
            if test_function:
                print("Returns last profile as text")
                return
            #
            # returns the last profile, as text
            outcome = self.return__profile(
                data=self.calculations,
                based_on_change=False,
                return_outcome_as_number=True,
                automatic_use_time_standards=self.use_automatic_time,
            )
            #
            #
            return outcome

        # returns regular time serie. So hard numbers - no profiles - and date's included.
        elif (
            as_profile != True
            and based_on_change != True
            and return_last_varible_only != True
            and return_as_number != True
        ):

            if test_function:
                print("Returns indicator time serie")
                return
            #
            # packages the calculations
            outcome = self.convert_data_to_dataframe(self.calculations)
            #
            # returs the timeserie.
            return outcome

        #
        # return the time serie as profiled
        elif (
            as_profile != True
            and based_on_change != True
            and return_last_varible_only != True
            and return_as_number != True
        ):
            if test_function:

                print("Returns profiled timeserie")

                return
            #
            # packages the calculations
            outcome = self.convert_data_to_dataframe(self.outcome_profile)
            #
            # returs the timeserie of profile.
            return outcome

        #
        #
        # self.moneyflow_data_set = self.calculations

        # if calculations_profile != []:

        #    self.moneyflow_profile_data = self.calculations_profile

        # self.moneyflow_profile_change_data = self.outcome_profile_change

        # self.moneyflow_data_loaded = True

        # self.convert_data_to_dataframe(self.calculations)

        # convert the data into dataframes.

        #
        # if function is tested
        if test_function:
            print("Reaches end of function")
            return

        return self.calculations

    def convert_data_to_dataframe(self, data=None):

        #
        # tails the data so it matches with the amount of data.
        idata = self.stock_data.tail(len(data))
        #
        # sets data to an other vairble
        ldata = data
        #
        # creates a data frame ()
        ldataf = pd.DataFrame(ldata)
        #
        # uses index
        data_index = idata.index

        # datadasframe = pd.DataFrame(index=datesindex, data=ldataf.values)
        the_created_dataframe = pd.DataFrame(
            index=data_index, data=ldataf.values
        )
        #
        # sets data frame to class object
        self.data_frame = the_created_dataframe
        #
        # changes the name of the colums
        self.data_frame.columns = ["Data"]
        #
        # replaces the Na's with zero's ( Ment for the change dataframe)
        self.data_frame["Data"] = self.data_frame["Data"].fillna(0)

        return self.data_frame


"""


#class price_elasticy_analyses: 
start = time.time()

global stock
stock = power_object.power_stock_object("DXLG", fast_load= True)

end = time.time()

elapsed = end - start
print(elapsed)

#class price_elasticy_analyses: 
start = time.time()

stock = power_object.power_stock_object("DXLG", fast_load= False)

end = time.time()

elapsed = end - start
print(elapsed)


converter = support_functions.date_to_week_converction(stock.stock_data)

stock.stock_data = converter.weekly_stock_data



#global moneyflow_analyses

#liquidity_analyses = liquidity_impact(stock_ticker = stock.stock_ticker , stock_data = stock.stock_data,    synchronize=False, timeframe="D")
#print("\\n\n\n testing the function \n\n")

global x 
x = twitter_text_generator(name_of_analyeses="LIQUIDTY" , ticker_name="AAPL",    new_recommendation="STRONG_BUY", old_recommendation = "HOLD", time_frame= "W",occation="CHANGE_PROFILE")

global i_data
i_data = money_flows(stock_ticker="DXLG",stock_data= stock.stock_data,timeframe="D")
i_data.money_flow_analyeses(full_run=True)

print('\n\n')
print(x.twitter_text_full)
#print(x)



#(liq_ana.liquidity_data_profiles)
#print(x)
"""
