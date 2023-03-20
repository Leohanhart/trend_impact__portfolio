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
from fastapi.middleware.cors import CORSMiddleware
from core_service_layer.data_service import get_system_info
import database_querys_main
import startup_script
import startup_support
import update_portfolios
import service_layer_data_service as services
import json
import constants
import uvicorn
from mangum import Mangum

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# startup_script.start_update_scedule()

"""
acceptatie criteria
- moet een endpoint komen waarbij je een status van een los aandeel kan 


"""


def onstart_function():

    startup_support.create_path_for_stock_data()
    startup_script.start_update_scedule()
    data_update = update_portfolios.update_data()


@app.on_event("startup")
async def startup_event():

    onstart_function()


@app.get("/")
def read_root():

    return {"Welcome to the trendimpact-core.. I Love you Leo, your girlfriend is so cute <3 <3 <3 , LIKE ELMO! ELMO IS GREAT 1337"}


@app.get("/trend_analyses")
def return_trend_analyses(ticker: str):

    data = services.return_trend_analyses.get_trend_analyses(ticker)

    return Response(data)


@app.get("/trend_analyses_archive")
def return_trend_archive_analyses(ticker: str):

    data = services.return_trend_analyses.get_trend_archive_analyses(ticker)

    return Response(data)


@app.get("/trend_analyses_trades")
def return_trend_archive_trades(ticker: str):

    data = services.return_trend_analyses.get_trend_analyses_trades(ticker)

    return Response(data)


@app.get("/trend_analyses_trade_options")
def return_all_trend_specs(page: int = 1,
                           long: bool = True,
                           short: bool = False,
                           amount_days_of_new_trend: int = 5,
                           percentage_2y_profitble: float = 90):

    data = services.return_trend_trade_options.return_trade_options(
        page=page,
        long=long,
        short=short,
        amount_days_of_new_trend=amount_days_of_new_trend,
        percentage_2y_profitble=percentage_2y_profitble

    )

    return Response(data)


@app.get("/trend_strategy_status")
def return_all_trend_specs():

    data = services.return_trend_analyses.get_all_trend_specs()

    return Response(data)


@app.get("/avalible_portfolios")
def avalible_portfolios(page: int = 1, min_amount_stocks: int = 5, max_amount_stocks=6):

    data = services.return_portfolios_options.return_portfolios()

    return Response(data)


@app.get("/trading_portfolios")
def avalible_portfolios(portfolio_id: str = ""):

    data = services.return_portfolios_options.return_trading_portfolios(
        id_=portfolio_id)

    return Response(data)


@app.post("/add_portfolios")
def add_portfolios(portfolio_id: str):

    data = services.return_portfolios_options.add_trading_portfolio(
        id_=portfolio_id)

    return data


@app.delete("/remove_portfolio")
def remove_portfolio(portfolio_id: str):

    data = services.return_portfolios_options.delete_trading_portfolio(
        id_=portfolio_id)

    return data


@app.get("/show_portfolio_performance")
def return_portfolio_performance(portfolio_id: str):

    data = services.return_stats.return_trading_backtest(
        portfolio_id=portfolio_id)

    return data


@app.get("/show_logs")
def return_logs(page_number: int = 1):

    data = services.return_logs.return_logs_page(page_number=page_number)

    return data


@app.get("/show_user_trades")
def return_user_trades(trader_id: str = "49a55c9c-8dbd-11ed-8abb-001a7dda7110"):

    data = services.return_trend_analyses.get_user_trades(
        uuid_portfolio=trader_id)

    return data


@app.post("/add_user_trades")
def add_user_trade(trader_id: str = "49a55c9c-8dbd-11ed-8abb-001a7dda7110", ticker: str = ""):

    data = services.crud_user_trades.add_user_trade(
        uu_id_trader=trader_id, ticker_name=ticker)

    return data


@app.delete("/remove_user_trades")
def return_logs(trader_id: str = "49a55c9c-8dbd-11ed-8abb-001a7dda7110", ticker: str = ""):

    data = services.crud_user_trades.remove_user_trade(uu_id_trader="49a55c9c-8dbd-11ed-8abb-001a7dda7110",
                                                       ticker_name=ticker)

    return data


@app.get("/avalible_tickers")
def return_all_tickers():

    data = services.return_trend_analyses.get_all_tickers()

    return Response(data)


@app.post("/add_or_maintain_ticker")
def add_or_maintain_ticker(ticker: str = ""):

    data = services.maintenance_tickers.add_or_remove_ticker(ticker)

    return data


handler = Mangum(app)

if __name__ == "__main__":

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, debug=True,
                workers=4, limit_concurrency=1000)
