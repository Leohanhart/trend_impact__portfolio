# -*- coding: utf-8 -*-
"""
Created on Thu May  5 19:34:47 2022

@author: Gebruiker
"""
import constants
import sqlalchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import and_, or_, not_



if __name__ == '__main__':
    
    try:
        
        url = constants.SQLALCHEMY_DATABASE_URI
        
        db_path = constants.SQLALCHEMY_DATABASE_URI_Test
        engine = create_engine(db_path, echo = True)            
        Session = sessionmaker(bind=engine)
        session = Session()
        
        try:
        # Try to get the underlying session connection, If you can get it, its up
            connection = session.connection()
            print("True")
        except:
            print("False")
        

    except Exception as e:
        print(e)