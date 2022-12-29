# -*- coding: utf-8 -*-
"""
Created on Thu May  5 17:17:51 2022

Idea's correlation / cointegration table. Use for prediction. 
- portolio optimizer. 

@author: Gebruiker
- fix that stocks update only till last friday., make sure strat updaters only use that data.
- fix, only first 1000 tickers are added. 
^ Only run script on Ipython terminal. Mabey split the Server and update script seperated. 


"""

from typing import Optional
from fastapi import BackgroundTasks, FastAPI, Response, HTTPException
from core_service_layer.data_service import get_system_info
import database_querys_main
import startup_script
import service_layer_data_service
import json
import constants
import uvicorn
from mangum import Mangum

app = FastAPI()

#startup_script.start_update_scedule()
def onstart_function():
    
    startup_script.start_update_scedule()
    
@app.on_event("startup")
async def startup_event():
    
    
    onstart_function()
    

@app.get("/")
def read_root():
    
    return {"Welcome to the flowimpact core.. I Love you Leo, LIKE ELMO"}

@app.get("/test")
def test_root():
    
    data = get_system_info.return_system_info.return_hello_statment()
    
    return data

@app.get("/last_update_daily")
def receive_update():
    
    data = service_layer_data_service.return__data().return_last_daily_update()
    
    return data


@app.get("/logs")
def read_logs():
    
    data = database_querys_main.database_querys.log_item_get()
    return data




@app.get("/archive_flowimpact_data")
def return_archive_flowimpact_data( ticker : str = None,
                                     periode : str = None,
                                     year : int = None, 
                                     month :int = None, 
                                     day : int = None, 
                                     weeknr : int = None,):
    
    data = service_layer_data_service.return__research__and__archives.return_flow_impact_archive(ticker = ticker, 
                                                                                            periode = periode, 
                                                                                            year = year,
                                                                                            month = month,
                                                                                            day = day,
                                                                                            weeknr = weeknr,
                                                                                            ) 
    
    
    #data = service_layer_data_service.return__analyses.return_liquidity_analyses()
    return Response(data)

@app.get("/analyses_liquidity")
def return_liquidity_analyses(active_filter : bool = True, 
                                      increasing: bool = False,
                                      decreasing: bool = False,
                                      min_number: int = -3,
                                      max_number: int = 3,
                                      profile_number : int = 0, 
                                      pagination_filter : bool = True,
                                      page_amount : int = 20,
                                      page_number : int = 1,
                                      daily_data : bool = False):
    
    
    data = service_layer_data_service.return__analyses.return_liquidity_analyses(active_filter = active_filter,
                                                                                            increasing = increasing, 
                                                                                            decreasing = decreasing, 
                                                                                            min_number = min_number, 
                                                                                            max_number = max_number, 
                                                                                            profile_number = profile_number,
                                                                                            pagination_filter = pagination_filter , 
                                                                                            page_amount = page_amount , 
                                                                                            page_number = page_number,
                                                                                            daily_data = daily_data
        ) 
    
    
    #data = service_layer_data_service.return__analyses.return_liquidity_analyses()
    return Response(data)




@app.get("/analyses_moneyflow")
def return_moneyflow_analyses(active_filter : bool = True, 
                                      increasing: bool = False,
                                      decreasing: bool = False,
                                      min_number: int = -3,
                                      max_number: int = 3,
                                      profile_number : int = 0, 
                                      pagination_filter : bool = True,
                                      page_amount : int = 20,
                                      page_number : int = 1,
                                      daily_data : bool = False):
    
    data = service_layer_data_service.return__analyses.return_moneyflow_analyses(active_filter = active_filter,
                                                                                            increasing = increasing, 
                                                                                            decreasing = decreasing, 
                                                                                            min_number = min_number, 
                                                                                            max_number = max_number, 
                                                                                            profile_number = profile_number,
                                                                                            pagination_filter = pagination_filter, 
                                                                                            page_amount = page_amount, 
                                                                                            page_number = page_number,
                                                                                            daily_data = daily_data)
    
    return Response(data)



@app.get("/analyses_flows_and_impact")
def return_flows_and_impact_analyses( active_filter : bool = False, 
                                      increasing: bool = False,
                                      decreasing: bool = False,
                                      min_number: int = -3,
                                      max_number: int = 3,
                                      profile_number : int = 0, 
                                      pagination_filter : bool = False,
                                      page_amount : int = 20,
                                      page_number : int = 1,
                                      daily_data : bool = False):
    
    data = service_layer_data_service.return__analyses.return_moneyflow_and_impact_analyses(active_filter = active_filter,
                                                                                            increasing = increasing, 
                                                                                            decreasing = decreasing, 
                                                                                            min_number = min_number, 
                                                                                            max_number = max_number , 
                                                                                            profile_number = profile_number ,
                                                                                            pagination_filter = pagination_filter , 
                                                                                            page_amount = page_amount, 
                                                                                            page_number = page_number,
                                                                                            daily_data = daily_data )
    
    return Response(data)

@app.get("/analyses_moneyflow/{stock_ticker}")
def flows_ticker(stock_ticker: str = "CAR", periode_in : str = "W", length_ts : str = "y3", q: Optional[str] = None):
    
    data = service_layer_data_service.return__analyses.return_stock_analyses(ticker_in = stock_ticker,
                                                                             stock_analyses="moneyflow_data",
                                                                             periode=periode_in,
                                                                             length_time_series=length_ts
                                                                             )
    
    return Response(data)

@app.get("/analyses_liquidity/{stock_ticker}")
def liquidityimpact_ticker(stock_ticker: str = "CAR", periode_in : str = "W", length_ts : str = "y3", q: Optional[str] = None):
    
    data = service_layer_data_service.return__analyses.return_stock_analyses(ticker_in = stock_ticker,
                                                                             stock_analyses="liquidity_data",
                                                                             periode=periode_in,
                                                                             length_time_series=length_ts
                                                                             )
    return Response(data)

@app.get("/analyses_lengths/")
def return_avalible_time_series_lengts( q: Optional[str] = None):
    
    data = service_layer_data_service.return_avalible_analyses_lengts()
    
    return Response(data)



@app.get("/sector_analyses/{sector_name}")
def sector_analyses_name(sector_name: str = None, 
                         tail_option_years : int = 1, q: Optional[str] = None):
    
    
    try:
        data = service_layer_data_service.return__analyses.return_sector_analyses(sector_in = sector_name, amout_of_years=tail_option_years)
        
    except Exception as e:
        
        if not e:
            
            e = "No error code is given"
            
        raise HTTPException(status_code=500, detail=e)
    
    return data

@app.get("/sector_analyses")
def sector_analyses( q: Optional[str] = None):
    """
    speculation MAX : name, amount of stocks?, amount of moneyflow(Total), AVG return sector, profile LIQ, profile MON, forecast_liq, forcast_mon, 
    Volatility, volatity forecast, 
    
    FOR NOW : name ,moneyflow, liq + profiles 
    """
    data = service_layer_data_service.return__analyses.return_sector_analyses()
    
    
    return Response(data)

@app.get("/industry_analyses/{industry_name}")
def industry_analyses_name(industry_name: str = None, tail_option_years : int = 1, q: Optional[str] = None):
    
    try:
        data = service_layer_data_service.return__analyses.return_industry_analyses(industry_in = industry_name, amout_of_years=tail_option_years)
    
    except Exception as e:
        
        if not e:
            
            e = "No error code is given"
            
        raise HTTPException(status_code=500, detail=e)
    
    return Response(data)


@app.get("/industry_analyses")
def return_flows_and_impact_analyses( q: Optional[str] = None):
    
    data = service_layer_data_service.return__analyses.return_moneyflow_and_impact_analyses()
    
    
    return Response(data)

@app.get("/data/avalible_analyses")
def load_avalible_analyeses():    
    
    option_list = constants.stock_avalible_analyses
 
    json_object = json.dumps(option_list, ensure_ascii=True)
    
    return Response(json_object)

@app.get("/data/avalible_periodes")
def load_data_options_periodes():    
    
    option_list = constants.stock_avalible_periodes
 
    json_object = json.dumps(option_list)
    
    return Response(json_object)

@app.get("/data/avalible_timeframes")
def load_data_options_timeframe():    
    
    option_list = constants.stock_avalible_timeframes
 
    json_object = json.dumps(option_list)
    
    return option_list

@app.get("/data/avalible_tickers")
def load_data_options_tickers():    
    
    resp = service_layer_data_service.return__data.return_stock_data_time_serie(ticker_in = "", time_frame = "", periode ="", tickers_only=True)
    
    resp = json.dumps(resp, ensure_ascii=False,separators=(',', ':'))
    
    resp = json.loads(resp)
    
    return resp

@app.get("/sectors")
def load_sectors():    
    
    resp = service_layer_data_service.return__data.return_all_sectors()
    
    resp = json.loads(resp)
    
    return resp

@app.get("/industries")
def load_industries():    
    
    resp = service_layer_data_service.return__data.return_all_industrys()
    
    resp = json.loads(resp)
    
    return resp

@app.get("/data/time_serie_data/{stock_ticker}")
def load_stock_data(stock_ticker: str = "AAPL", q: Optional[str] = None):    
    
    resp = service_layer_data_service.return__data.return_stock_data_time_serie(ticker_in = stock_ticker)
    
    resp = json.loads(resp)
    
    return resp

@app.get("/data/time_serie_data/{stock_ticker}/{periode}")
def load_stock_data_spec_periode(stock_ticker: str = "AAPL",periode: str = "d", q: Optional[str] = None):    
    
    resp = service_layer_data_service.return__data.return_stock_data_time_serie(ticker_in = stock_ticker,periode = periode)
    
    return {resp}

@app.get("/data/time_serie_data/{stock_ticker}/{periode}/{timeframe}")
def load_stock_data_parced(stock_ticker: str, periode: str, timeframe: str, q: Optional[str] = None):    
    
    resp = service_layer_data_service.return__data.return_stock_data_time_serie(ticker_in = stock_ticker, time_frame = timeframe, periode = periode)
    
    return {resp}

@app.get("/data/{stock_analyses}/{stock_ticker}")
def load_stock_data_analyses(stock_ticker: str , stock_analyses: str, q: Optional[str] = None):    
    """
    Moet gestest worden.

    Parameters
    ----------
    stock_ticker : str
        DESCRIPTION.
    stock_analyses : str
        DESCRIPTION.
    q : Optional[str], optional
        DESCRIPTION. The default is None.

    Returns
    -------
    set
        DESCRIPTION.

    """
    resp = service_layer_data_service.return__analyses.return_stock_analyses(ticker_in = stock_ticker, stock_analyses = stock_analyses)
    
    return {resp}

"""
add sector analsyes to stock data options.

create way to retreive sectors.
create way to retreive sector analyses. 

"""

handler = Mangum(app)

if __name__ == "__main__":
    
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True,debug=True,
                workers=4, limit_concurrency=1000)