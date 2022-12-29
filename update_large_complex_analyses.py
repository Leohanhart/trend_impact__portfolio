# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 20:11:07 2022

@author: Gebruiker


Q&A


- Sector analyses
- Industry analyses. 
- Exchange analyses. (Both liquidity and Money floww all 3 above)
- More

- Overview of all last industry's inflows and impact. Including profiles idividual, sub profiels. Save as DF

Needs to be overthougt about a analyses object for sectors. ( For synching the profiles)

(A) this function is implementned so that on at daily update there will be no activity untill this is needed.

plan: 
    1. Create differeny idea's for different strategies. 
    
    2. create module for portoflio, just save with 

"""

import sector_analyse
from core_utils.save_temp_data import save_and_load_temp_data
import database_querys_main
import time
from tqdm import tqdm
import support_class
import pandas as pd


#### currently in development So no clean loop.
class update_large_analyses:
    
    # function how saves the analyses
    # function who loads the anylyses. 
    
    # function that doe's all the large and complex analyses.
    
    @staticmethod
    def update_all_sector_and_industry_analyses(periode : str = "W", industrys_update : bool = True,
                                                sectors_update : bool = True):
        
        """
        Vragen en antwoorden: 
            
            Hoe gaan we dat doen met de gemiddelde analyses? 
            
            Hoe gaan we dat doen met opslaan? 
            
            Hoe gaan we dat doen met query? Je moet een soortvan field declaration doen dus "Veld :profile_vol" waarde = 10. 
            Anders gaat hij dingen lopen overschrijven. 
        
        """
        
        # read (A)
        if periode == "D": 
            return 
        
        if periode == "W":

            if industrys_update:
                
                update_secotor_and_industry_analyses.update_industrys_weekly()

                
            if sector_analyse:
                
                update_secotor_and_industry_analyses.update_sectors_weekly()

                
            # update databases
            update_secotor_and_industry_analyses.update_database_industry()
            update_secotor_and_industry_analyses.update_database_sector()
            
            # updates the statistics in the databases.
            update_secotor_and_industry_analyses.update_database_statistics()

                
        #### here should be the Sector and industry main update.
        
        """ 
        
        Analyses needs to be injected static,
        Analyses needs to be static, last and profile, avg profile
        
        """
class update_large_analyses_support(object):
    
    
    @staticmethod
    def update():
        pass
    
    
class update_secotor_and_industry_analyses(object):
    
    #### only volatiliy needs to be implemented yet.
    
    @staticmethod
    def update_database_statistics():
        
        # do query on sector and industry, take avg from column and more.
        pass
    
    @staticmethod
    def update_database_sector():
        """
        
        Saves all profiles for sector analsyes

        Returns
        -------
        None.

        """
        # spawns analyses class object.
        sector_and_industy_analyesses = sector_analyse.sector_analyse()
        
        # return sectors
        sector_and_industy_analyesses.sectors   = sectors       = database_querys_main.database_querys.get_all_active_sectors()
        
        # sets industy
        sector_and_industy_analyesses.industry  = industry      = database_querys_main.database_querys.get_all_active_industrys()
        
        # sets tickers               
        sector_and_industy_analyesses.tickers   = tickers       = database_querys_main.database_querys.get_all_active_tickers()
        
        sub_analyses_atributes = ["indicator_timeserie_raw","indicator_timeserie_profile"]
        
        
        #### volatility needs to be implemented
        analyses_names  = [ "MONEYFLOWS", "LIQUIDTY"]
    
        # update all sectors
        for sector in sector_and_industy_analyesses.sectors: # eerste fout, los van elkaar doen.
            
        
        
        
            #loading moneyflows

            name_placeholder = str(sector + "." + "MONEYFLOWS"+ "." + "indicator_timeserie_raw")
            # saves analyses
            # try or die
            try: 
                
                data = save_and_load_temp_data.save_and_load_temp_data_class.load_data(name_placeholder, "LARGE_ANALYSES")
                
                if not isinstance(data, pd.DataFrame):
                    
                    data = data.to_frame()
                
                slide = data.tail(1)
                value_last = int(slide.values)
                    
                database_querys_main.database_querys.update_analyses_sector(id_in=sector,last_mon=value_last)
                
                
            except:
                
                database_querys_main.database_querys.update_analyses_sector(id_in=sector,last_mon=0)
                
            name_placeholder = str(sector + "." + "MONEYFLOWS"+ "." + "indicator_timeserie_raw"+".AVERAGE")
            # saves analyses
            # try or die
            try: 
                
                data = save_and_load_temp_data.save_and_load_temp_data_class.load_data(name_placeholder, "LARGE_ANALYSES")
                
                if not isinstance(data, pd.DataFrame):
                    
                    data = data.to_frame()
                
                slide = data.tail(1)
                value_last = int(slide.values)
                    
                database_querys_main.database_querys.update_analyses_sector(id_in=sector,last_avg_mon=value_last)
                
                
            except:
                
                database_querys_main.database_querys.update_analyses_sector(id_in=sector,last_avg_mon=0)
                
            
            name_placeholder = str(sector + "." + "MONEYFLOWS"+ "." + "indicator_timeserie_profile")
            # saves analyses
            # try or die
            try: 
                
                data = save_and_load_temp_data.save_and_load_temp_data_class.load_data(name_placeholder, "LARGE_ANALYSES")
                
                if not isinstance(data, pd.DataFrame):
                    
                    data = data.to_frame()
                
                slide = data.tail(1)
                
                value_last = int(slide.values)
                    
                database_querys_main.database_querys.update_analyses_sector(id_in=sector,profile_mon=value_last)
                
                
            except:
                
                database_querys_main.database_querys.update_analyses_sector(id_in=sector,profile_mon=0)
                
            name_placeholder = str(sector + "." + "MONEYFLOWS"+ "." + "indicator_timeserie_profile" +".AVERAGE")
            # saves analyses
            # try or die
            try: 
                
                data = save_and_load_temp_data.save_and_load_temp_data_class.load_data(name_placeholder, "LARGE_ANALYSES")
                
                if not isinstance(data, pd.DataFrame):
                    
                    data = data.to_frame()
                
                slide = data.tail(1)
                
                value_last = int(slide.values)
                    
                database_querys_main.database_querys.update_analyses_sector(id_in=sector,profile_avg_mon=value_last)
                
                
            except:
                
                database_querys_main.database_querys.update_analyses_sector(id_in=sector,profile_avg_mon=0)
                
            #loading liqduit

            name_placeholder = str(sector + "." + "LIQUIDTY"+ "." + "indicator_timeserie_raw")
            # saves analyses
            # try or die
            try: 
                
                data = save_and_load_temp_data.save_and_load_temp_data_class.load_data(name_placeholder, "LARGE_ANALYSES")
                
                if not isinstance(data, pd.DataFrame):
                    
                    data = data.to_frame()
                
                slide = data.tail(1)
                value_last = int(slide.values)
                    
                database_querys_main.database_querys.update_analyses_sector(id_in=sector,last_liq=value_last)
                
            except:
                
                database_querys_main.database_querys.update_analyses_sector(id_in=sector,last_liq=0)
                
            
            name_placeholder = str(sector + "." + "LIQUIDTY"+ "." + "indicator_timeserie_raw"+".AVERAGE")
            # saves analyses
            # try or die
            try: 
                
                data = save_and_load_temp_data.save_and_load_temp_data_class.load_data(name_placeholder, "LARGE_ANALYSES")
                
                if not isinstance(data, pd.DataFrame):
                    
                    data = data.to_frame()
                
                slide = data.tail(1)
                value_last = int(slide.values)
                    
                database_querys_main.database_querys.update_analyses_sector(id_in=sector,last_avg_liq=value_last)
                
            except:
                
                database_querys_main.database_querys.update_analyses_sector(id_in=sector,last_avg_liq=0)
                
            
            name_placeholder = str(sector + "." + "LIQUIDTY"+ "." + "indicator_timeserie_profile")
            # saves analyses
            # try or die
            try: 
                
                data = save_and_load_temp_data.save_and_load_temp_data_class.load_data(name_placeholder, "LARGE_ANALYSES")
                
                if not isinstance(data, pd.DataFrame):
                    
                    data = data.to_frame()
                
                slide = data.tail(1)
                
                value_last = int(slide.values)
                    
                database_querys_main.database_querys.update_analyses_sector(id_in=sector,profile_liq=value_last)
                
                
            except:
                
                database_querys_main.database_querys.update_analyses_sector(id_in=sector,profile_liq=0)
                
            name_placeholder = str(sector + "." + "LIQUIDTY"+ "." + "indicator_timeserie_profile" + ".AVERAGE")
            # saves analyses
            # try or die
            try: 
                
                data = save_and_load_temp_data.save_and_load_temp_data_class.load_data(name_placeholder, "LARGE_ANALYSES")
                
                if not isinstance(data, pd.DataFrame):
                    
                    data = data.to_frame()
                
                slide = data.tail(1)
                
                value_last = int(slide.values)
                    
                database_querys_main.database_querys.update_analyses_sector(id_in=sector,profile_avg_liq=value_last)
                
                
            except:
                
                database_querys_main.database_querys.update_analyses_sector(id_in=sector,profile_avg_liq=0)
                
                
    @staticmethod
    def update_database_industry():
        """
        
        Saves all profiles for sector analsyes

        Returns
        -------
        None.

        """
        # spawns analyses class object.
        sector_and_industy_analyesses = sector_analyse.sector_analyse()
        
        # return sectors
        sector_and_industy_analyesses.sectors   = sectors       = database_querys_main.database_querys.get_all_active_sectors()
        
        # sets industy
        sector_and_industy_analyesses.industry  = industry      = database_querys_main.database_querys.get_all_active_industrys()
        
        # sets tickers               
        sector_and_industy_analyesses.tickers   = tickers       = database_querys_main.database_querys.get_all_active_tickers()
        
        sub_analyses_atributes = ["indicator_timeserie_raw","indicator_timeserie_profile"]
        
        
        #### volatility needs to be implemented
        analyses_names  = [ "MONEYFLOWS", "LIQUIDTY"]
    
        # update all sectors
        for industry in sector_and_industy_analyesses.industry: # eerste fout, los van elkaar doen.
            
        
        
        
            name_placeholder = str(industry + "." + "MONEYFLOWS"+ "." + "indicator_timeserie_raw")
            # saves analyses
            # try or die
            try: 
                
                data = save_and_load_temp_data.save_and_load_temp_data_class.load_data(name_placeholder, "LARGE_ANALYSES")
                
                if not isinstance(data, pd.DataFrame):
                    
                    data = data.to_frame()
                
                slide = data.tail(1)
                value_last = int(slide.values)
                   
                database_querys_main.database_querys.update_analyses_industry(id_in=industry,last_mon=value_last)
                
                
            except:
                
                database_querys_main.database_querys.update_analyses_industry(id_in=industry,last_mon=0)
                
            name_placeholder = str(industry + "." + "MONEYFLOWS"+ "." + "indicator_timeserie_raw"+".AVERAGE")
            # saves analyses
            # try or die
            try: 
                
                data = save_and_load_temp_data.save_and_load_temp_data_class.load_data(name_placeholder, "LARGE_ANALYSES")
                
                if not isinstance(data, pd.DataFrame):
                    
                    data = data.to_frame()
                
                slide = data.tail(1)
                value_last = int(slide.values)
                    
                database_querys_main.database_querys.update_analyses_industry(id_in=industry,last_avg_mon=value_last)
                
                
            except:
                
                database_querys_main.database_querys.update_analyses_industry(id_in=industry,last_avg_mon=0)
                
            
            name_placeholder = str(industry + "." + "MONEYFLOWS"+ "." + "indicator_timeserie_profile")
            # saves analyses
            # try or die
            try: 
                
                data = save_and_load_temp_data.save_and_load_temp_data_class.load_data(name_placeholder, "LARGE_ANALYSES")
                
                if not isinstance(data, pd.DataFrame):
                    
                    data = data.to_frame()
                
                slide = data.tail(1)
                
                value_last = int(slide.values)
                    
                database_querys_main.database_querys.update_analyses_industry(id_in=industry,profile_mon=value_last)
                
                
            except:
                
                database_querys_main.database_querys.update_analyses_industry(id_in=industry,profile_mon=0)
                
            name_placeholder = str(industry + "." + "MONEYFLOWS"+ "." + "indicator_timeserie_profile" +".AVERAGE")
            # saves analyses
            # try or die
            try: 
                
                data = save_and_load_temp_data.save_and_load_temp_data_class.load_data(name_placeholder, "LARGE_ANALYSES")
                
                if not isinstance(data, pd.DataFrame):
                    
                    data = data.to_frame()
                
                slide = data.tail(1)
                
                value_last = int(slide.values)
                    
                database_querys_main.database_querys.update_analyses_industry(id_in=industry,profile_avg_mon=value_last)
                
                
            except:
                
                database_querys_main.database_querys.update_analyses_industry(id_in=industry,profile_avg_mon=0)
                
            #loading liqduit

            name_placeholder = str(industry + "." + "LIQUIDTY"+ "." + "indicator_timeserie_raw")
            # saves analyses
            # try or die
            try: 
                
                data = save_and_load_temp_data.save_and_load_temp_data_class.load_data(name_placeholder, "LARGE_ANALYSES")
                
                if not isinstance(data, pd.DataFrame):
                    
                    data = data.to_frame()
                
                slide = data.tail(1)
                value_last = int(slide.values)
                    
                database_querys_main.database_querys.update_analyses_industry(id_in=industry,last_liq=value_last)
                
            except:
                
                database_querys_main.database_querys.update_analyses_industry(id_in=industry,last_liq=0)
                
            
            name_placeholder = str(industry + "." + "LIQUIDTY"+ "." + "indicator_timeserie_raw"+".AVERAGE")
            # saves analyses
            # try or die
            try: 
                
                data = save_and_load_temp_data.save_and_load_temp_data_class.load_data(name_placeholder, "LARGE_ANALYSES")
                
                if not isinstance(data, pd.DataFrame):
                    
                    data = data.to_frame()
                
                slide = data.tail(1)
                value_last = float(slide.values)
                    
                database_querys_main.database_querys.update_analyses_industry(id_in=industry,last_avg_liq=value_last)
                
            except:
                
                database_querys_main.database_querys.update_analyses_industry(id_in=industry,last_avg_liq=0)
                
            
            name_placeholder = str(industry + "." + "LIQUIDTY"+ "." + "indicator_timeserie_profile")
            # saves analyses
            # try or die
            try: 
                
                data = save_and_load_temp_data.save_and_load_temp_data_class.load_data(name_placeholder, "LARGE_ANALYSES")
                
                if not isinstance(data, pd.DataFrame):
                    
                    data = data.to_frame()
                
                slide = data.tail(1)
                
                value_last = int(slide.values)
                    
                database_querys_main.database_querys.update_analyses_industry(id_in=industry,profile_liq=value_last)
                
                
            except:
                
                database_querys_main.database_querys.update_analyses_industry(id_in=industry,profile_liq=0)
                
            name_placeholder = str(industry + "." + "LIQUIDTY"+ "." + "indicator_timeserie_profile" + ".AVERAGE")
            # saves analyses
            # try or die
            try: 
                
                data = save_and_load_temp_data.save_and_load_temp_data_class.load_data(name_placeholder, "LARGE_ANALYSES")
                
                if not isinstance(data, pd.DataFrame):
                    
                    data = data.to_frame()
                
                slide = data.tail(1)
                
                value_last = int(slide.values)
                    
                database_querys_main.database_querys.update_analyses_industry(id_in=industry,profile_avg_liq=value_last)
                
                
            except:
                
                database_querys_main.database_querys.update_analyses_industry(id_in=industry,profile_avg_liq=0)
            
            
            
            
    

    
    @staticmethod
    def update_industrys_weekly():
        # spawns analyses class object.
        sector_and_industy_analyesses = sector_analyse.sector_analyse()
        
        # return sectors
        sector_and_industy_analyesses.sectors   = sectors       = database_querys_main.database_querys.get_all_active_sectors()
        
        # sets industy
        sector_and_industy_analyesses.industry  = industry      = database_querys_main.database_querys.get_all_active_industrys()
        
        # sets tickers               
        sector_and_industy_analyesses.tickers   = tickers       = database_querys_main.database_querys.get_all_active_tickers()
        
        sub_analyses_atributes = ["indicator_timeserie_raw","indicator_timeserie_profile"]
        
    
        # loops true industries and fixes the thing. 
        for industry in sector_and_industy_analyesses.industry: # eerste fout, los van elkaar doen.
            # loop true analsyes
            for analyses  in sector_and_industy_analyesses.analyeses: # he will loop all analyses.
                # loops true atributes.
                for sub_analyses in sub_analyses_atributes:
                        
                    # creates analyses
                    try: 
                        analyses_out = sector_and_industy_analyesses.create_industy_or_sector_analyses(name_industry_or_sector = industry,
                                                                                                       periode="W",
                                                                                                       name_anlyeses= analyses,
                                                                                                       sub_atribute_analyses=sub_analyses,
                                                                                                       methode = "SUMMED"
                                                                                                       )
                    except Exception as e:
                        
                        raise ValueError
                        continue
                        
                        
                    
                    #analyses_out = analyses_out['Data'].round(decimals = 0)
                    # creates analyses name
                    name_placeholder = str(industry + "." + analyses + "." + sub_analyses)
                    # saves analyses
                    save_and_load_temp_data.save_and_load_temp_data_class.save_data(analyses_out, name_placeholder, "LARGE_ANALYSES")
                    
                    try: 
                        analyses_out = sector_and_industy_analyesses.create_industy_or_sector_analyses(name_industry_or_sector = industry,
                                                                                                       periode="W",
                                                                                                       name_anlyeses= analyses,
                                                                                                       sub_atribute_analyses=sub_analyses,
                                                                                                       methode = "SUMMED",
                                                                                                       average_out=True
                                                                                                       )
                    except Exception as e:
                        
                        raise ValueError
                        continue
                        
                        
                    
                    #analyses_out = analyses_out['Data'].round(decimals = 0)
                    # creates analyses name
                    name_placeholder = str(industry + "." + analyses + "." + sub_analyses + ".AVERAGE")
                    # saves analyses
                    save_and_load_temp_data.save_and_load_temp_data_class.save_data(analyses_out, name_placeholder, "LARGE_ANALYSES")
                    
                    
                    
    @staticmethod
    def update_sectors_weekly():
        
        # spawns analyses class object.
        sector_and_industy_analyesses = sector_analyse.sector_analyse()
        
        # return sectors
        sector_and_industy_analyesses.sectors   = sectors       = database_querys_main.database_querys.get_all_active_sectors()
        
        # sets industy
        sector_and_industy_analyesses.industry  = industry      = database_querys_main.database_querys.get_all_active_industrys()
        
        # sets tickers               
        sector_and_industy_analyesses.tickers   = tickers       = database_querys_main.database_querys.get_all_active_tickers()
        
        sub_analyses_atributes = ["indicator_timeserie_raw","indicator_timeserie_profile"]
        

            
        # update all sectors
        for sector in sector_and_industy_analyesses.sectors: # eerste fout, los van elkaar doen.
            # loop true analsyes
            for analyses  in sector_and_industy_analyesses.analyeses: # he will loop all analyses.
                # loops true atributes.
                for sub_analyses in sub_analyses_atributes:
                    # extract tickers
                
                    
                    tickers = database_querys_main.database_querys.get_all_stocks_with_sector(sector)
                    
                 
                    
                    sector_and_industy_analyesses.use_injected_tickers = True
                    
                    sector_and_industy_analyesses.injected_tickers = tickers
                    
                    # creates analyses
                    try: 
                        analyses_out = sector_and_industy_analyesses.create_industy_or_sector_analyses(name_industry_or_sector = industry,
                                                                                                       periode="W",
                                                                                                       name_anlyeses= analyses,
                                                                                                       sub_atribute_analyses=sub_analyses,
                                                                                                       methode = "SUMMED",
                                                                                                       use_injected_tickers=True
                                                                                                       )
                    except Exception as e:
                        
                        print(str(e))
                        continue
                        
                        
                    print(analyses_out.Data)
                    # creates analyses name
                    name_placeholder = str(sector + "." + analyses + "." + sub_analyses)
                    # saves analyses
                    save_and_load_temp_data.save_and_load_temp_data_class.save_data(analyses_out, name_placeholder, "LARGE_ANALYSES")
                    
                    try: 
                        analyses_out = sector_and_industy_analyesses.create_industy_or_sector_analyses(name_industry_or_sector = industry,
                                                                                                       periode="W",
                                                                                                       name_anlyeses= analyses,
                                                                                                       sub_atribute_analyses=sub_analyses,
                                                                                                       methode = "SUMMED",
                                                                                                       use_injected_tickers=True,
                                                                                                       average_out=True
                                                                                                       )
                    except Exception as e:
                        
                        print(str(e))
                        continue
                        
                        
                    print(analyses_out.Data)
                    # creates analyses name
                    name_placeholder = str(sector + "." + analyses + "." + sub_analyses  + ".AVERAGE")
                    # saves analyses
                    save_and_load_temp_data.save_and_load_temp_data_class.save_data(analyses_out, name_placeholder, "LARGE_ANALYSES")
                    
    
                    
                    
class update_secotor_and_industry_analyses_support(object):
    
    @staticmethod
    def functionshouldbehere():
        pass
    
    
    
    
    
if __name__ == "__main__":    
    
    try:
        
        
        print("START")
        #update_secotor_and_industry_analyses.update_database_industry()
        update_large_analyses.update_all_sector_and_industry_analyses()
        print("END")
        
    except Exception as e:
        
        raise Exception("Error with tickers", e)

                
                
                
                
                
                
                
                