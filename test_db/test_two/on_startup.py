import constants
from datetime import datetime, timedelta
import multiprocessing
import time 
import threading
import constants
import sys
import os
from core_utils.save_temp_data import save_and_load_temp_data as save_and_load_temp

from core_update.update_stocks import update_stocks_main
from core_update.update_main import update_main

from core_utils.database_querys import database_querys

from core_utils.database_tables.tabels import Ticker,Analyses_Liquidityimpact,Analyses_Moneyflow

import sqlalchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import and_, or_, not_

db_path = constants.SQLALCHEMY_DATABASE_URI
engine = create_engine(db_path, echo = True)            
Session = sessionmaker(bind=engine)
session = Session()


class startup:
    """
    
    In onstartup is a class with a proces that triggers a loop in a seperated thread that runs every 24 hour. 
    
    If failure occures, the first place to look is the destroctor, that one could be a problem. 
    
    
    How does this class work? 
    
    "the opperator" is the function that needs to be triggerd to start a deamon thread that runs every 24 hour. - this happens when the class is constructed. 
    "the daily loop" is Functions that gets deacttaced from the main thread an will contiunesly wait, check for updates or updates. 
    "the function to run daily" runs all the functions that needs to be runned every 24 hours. 
    
    If You want to add a function to the proceess, add this one to function to run daily. 
    
    
    
    
    """
    
    is_allowed_to_run   : bool = True
    print_content       : bool = False
    
    def __init__(self):
        """
        Starts refresh sycle 

        Returns
        -------
        None.

        """
        
        print("Startup refresh")
        self.add_paths()
        self.opperator()
    
    def __del__(self):
        """
        If class is deleted this function will be triggerd to stop the deamon thread.

        Returns
        -------
        None.

        """
        print("Shutdown refhesh")
        self.is_allowed_to_run = False
        
    def add_paths(self):
        """
        
        this function adds paths on runtime. 
        
        """
        
        # paths that are added on runtime
        paths_to_add = [ 
                        constants.CORE_DATA_____PATH,
                        constants.CORE_SCIPTS___PATH,
                        constants.CORE_SERVICE__PATH,
                        constants.CORE_UPDATE___PATH,
                        constants.CORE_UTILS____PATH,
                        constants.SQLALCHEMY_DATABASE_URI,
                        constants.CORE_UPDATE_ALL_ANALYSES_PATH
                        
        ]
        
        # adding paths
        for paths in paths_to_add:
            
            sys.path.append(paths)
            
        # sets current work directory 
        os.chdir(constants.ROOT_DIR)
        if self.print_content:
            print(sys.path)
            print(os.getcwd())
            
        
    def opperator(self):
        """
        Operator needs to be run to start the giant loop that refresh ever 24h, checking for it every 4H 

        Returns
        -------
        None.

        """
    	
        proces_background = threading.Thread(name='daemon',target=self.daily_loop)
        proces_background.setDaemon(True)
        proces_background.start()
        
        
    def daily_loop(self):
        """
        
        function is (needed) added to deamonthread that triggers every 24 hours. 

        Returns
        -------
        None.

        """
        
        # creates support functions 
        support_function = startup_support_functions()
        
        print("ADDED DAILYLOOP ... \n")
        
        # if pickle is interfering with other versions this function will fix the format. 
        try: 
                       
            # 
            support_function.check_experation()
                
        except Exception as e:
            
            if str(e) == "PICKLE_ERROR":
                print("Error with initzliatieon")
                self.first_initalization()
                self.function_to_run_daily()
                support_function.save_date()
                
                
        # runs for ever
        while True: 
            
            
            time.sleep(5)
            print("Checked for refesh..")
            # if support function  
            if support_function.check_experation():
                print("Refesh giant succes, refresh the system... tadadad")
                self.function_to_run_daily()
                support_function.save_date()
                
            else:
                print("no refesh needded...")
                
                #### remove this .
                self.function_to_run_daily()
                break
                
            if not self.is_allowed_to_run:
                
                break 
            
        print(4)
        
    def first_initalization(self):
        """
        
        This function runs if startup fails. This problem is maily occuring when pickle5 and pickle4 protocol interfairs.
        problem is very hard to solve, but fix is quite easy. Reload all the data. 

        Returns
        -------
        None.

        """

        # check when run for the last time. 
        
        # if expired, run 24 loop, else just sleep for 2 hours. 
        pass
    
    def function_to_run_daily(self):
        """
        
        This function is loaded with functions that needs to run every 24 hour. 

        Returns
        -------
        None.

        """

        # updates all analyses.
        update_stocks_main.update_stocks.download_stockdata()
        
        update_main.update_main_analyses.update_analyses_main()
        
        
class startup_support_functions:
    
    @staticmethod
    def check_experation():
        """
        Checks experiation of the datestring, returns true if date has expired.

        Returns
        -------
        bool
            DESCRIPTION.

        """
        # load data
        data_manager = save_and_load_temp.save_and_load_temp_data_class()
        
        try: 
            # loads data from file.
            date_old    =   data_manager.load_data("last_refesh", "SYSTEM")
        
        except Exception as e:
            
            startup_support_functions.save_date()
            
            return True
            
            
        # sets string to time object.
        old_date = datetime.strptime(date_old, "%d-%m-%Y")
        
        # sets now date 
        now = datetime.now()
        
        # checks difference. 
        difference =  now - old_date
        
        # creates differnt with date now. 

        if difference.days != 0: 
            return True 
        else:
            return False
        
        #print(type(difference.days))
        
    @staticmethod
    def save_date():
        """
        
        Creates a file with datestring of last refresh.

        Returns
        -------
        last_date : TYPE
            DESCRIPTION.

        """
        
        data_manager = save_and_load_temp.save_and_load_temp_data_class()
        now = datetime.now()
        last_date = now.strftime("%d-%m-%Y")
        
        data_manager.save_data(last_date, "last_refesh", "SYSTEM")

        return last_date
    
    @staticmethod
    def save_test_date():
        data_manager = save_and_load_temp.save_and_load_temp_data_class()

        date_expired = datetime.today() - timedelta(days=10)
        text = date_expired.strftime("%d-%m-%Y")
        
        data_manager.save_data(text , "last_refesh", "SYSTEM")
        
        
        return date_expired
    

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
        
        return data    

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

startup_file = startup()
        
if __name__ == '__main__':
    
    try:
        
        startup_file = startup()
    except Exception as e:
        print(e)