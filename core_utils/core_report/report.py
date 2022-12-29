# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 16:21:15 2022

@author: Gebruiker
"""

from core_utils.database_tables.tabels import unit_tests_and_errors,Ticker
import sqlalchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import constants

class report_unit_test():
    
    
    @staticmethod
    def report(location : str = "grotetest", message : str = "", error : bool = False):
        
        if location != "" :
            
            test_path = constants.SQLALCHEMY_DATABASE_URI
            engine = create_engine(test_path, echo = True)            
            Session = sessionmaker(bind=engine)
            session = Session()
            
            x = session.query(unit_tests_and_errors).get(location)
            
            print(x)
            
            # checks if the location exsists, if yes, action.
            if x == None: 
                
                
                
                Unittest = unit_tests_and_errors(id = location, error = error, error_code = message)
                
                session.add(Unittest)
                session.commit()
                
            else:
                
                Unittest = unit_tests_and_errors(id = location, error = error, error_code = message)
                
                x.id = location
                x.error = error
                x.error_code = message
                
                session.commit()
                
                
            #print(x)
                pass
            #Unittest = unit_tests_and_errors(id = location, error = error, error_code = message)
            
            #session.add(Unittest)
            #session.commit()
    
if __name__ == "__main__":      
    
    
    # test raport 
    report_unit_test.report("core_report", error=False)