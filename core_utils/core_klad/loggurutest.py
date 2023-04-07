# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 16:42:06 2023

@author: Gebruiker
"""
from loguru import logger
def test():
    
    logger.info("starting up")
    

if __name__ == "__main__":

    # archive
    try:
        test()

    except Exception as e:

        raise Exception("Error with tickers", e)
