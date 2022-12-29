from core_update.update_stocks.update_stocks_main import update_stocks
from core_utils.database_querys import database_querys
import constants 
from core_scripts.stock_data_download import power_stock_object
from core_utils.database_querys import database_querys
from core_update.update_analyses import update_all_analyses
from core_update.update_large_analyses import update_large_complex_analyses

"""

Initalize stock_data

"""

class update_main_analyses:
    
    @staticmethod
    def update_analyses_main():
        """
        
        Update all anlyses, stockdata, analyses, large analyses. 

        Returns
        -------
        None.
 
        """
        
        update_stocks.download_stockdata()
        update_all_analyses.update_all_strategie_analyses.update_all()
        update_large_complex_analyses.update_large_analyses.update_all_sector_and_industry_analyses()
        
        
if __name__ == "__main__":          
   
    try: 
        update_main_analyses.update_analyses_main()
        
    except Exception as e:
        
        print(e)
    
    # initalize the tables. 