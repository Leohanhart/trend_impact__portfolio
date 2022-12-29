# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 20:08:00 2022

@author: Gebruiker



1. Downlaod analyses - in update script is the file that I need. 
- check the save path -- possible add these to constants. 

2. Add the details in the DB, now the analyses are loaded in seperated tables. 

possibly its more efficent to create a table, id = uu, ticker = ticker, analyses = analyses. Work fine, 
table will be giant. Tink about it. 

3. Continue, now you have the analyses on top of your hand. 


"""


import update_flows_analyses
import update_liquidity_analyses

    
class update_all_strategie_analyses:
    
    @staticmethod
    def update_all():
        """
        
        Updates all analyses. 

        Raises
        ------
        Exception
            DESCRIPTION.

        Returns
        -------
        None.

        """
        
        try:
            # update liquidity analyses
            update_liquidity_analyses.update_liquidity_impact_analyses.update_analyses()
            update_liquidity_analyses.update_liquidity_impact_analyses.update_analyses(periode="D")
            # update moneyflow analyses
            update_flows_analyses.update_money_flow_analyses.update_analyses()
            update_flows_analyses.update_money_flow_analyses.update_analyses(periode="D")
        
        except Exception as e:
            
            print(e)
            raise Exception("ERROR_LOADING_ANALYSES", e)
            
        
if __name__ == "__main__":    
    
    try:
        
        print("START")
        update_all_strategie_analyses.update_all()
        print("END")
        
    except Exception as e:
        
        raise Exception("Error with tickers", e)