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
from fastapi import BackgroundTasks, FastAPI, Response, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from database_querys_main import database_querys
import startup_support
import update_portfolios
import update_trend_time_series
import service_layer_data_service as services
import json
import constants
import uvicorn
from mangum import Mangum
import setup_server
from authentication import (
    login_user,
    verify_token,
    protected_add_user,
    protected_change_password,
    protected_delete_user,
    get_user_activity_data,
)

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

    setup_server.initialize_server()
    #
    startup_support.create_path_for_stock_data()
    # startup_script.start_update_scedule()
    data_update = update_portfolios.update_data()


@app.on_event("startup")
async def startup_event():
    onstart_function()


@app.get("/")
def read_root(request: Request):

    return {
        "Welcome to the trendimpact-core.. Build between Dec 29, 2022, and Jul 9 2023 in the name of Hanhart Trading Technologies "
    }


@app.post("/login")
def login(user: str, pasword: str):

    token = login_user(user, pasword)

    return Response(token)


@app.post("/verify_token")
def verify_token_user(token: str):

    data = verify_token(token)

    return data


@app.post("/create_user")
def create_new_user(
    token: str, username: str, password: str, role: str = "USER"
):

    data = protected_add_user(token, username, password, role)

    return data


@app.post("/create_change_password")
def delete_user(token: str, username: str):

    data = protected_delete_user(token, username)

    return data


@app.post("/create_delete_user")
def create_user(token: str, username: str, password: str):

    data = protected_change_password(token, username, password)

    return data


@app.get("/last_update")
def return_last_update(token: str):

    verify_token(token)

    data = database_querys.get_last_update()
    return Response(data)


@app.get("/trend_analyses")
def return_trend_analyses(token: str, ticker: str, request: Request):

    verify_token(
        token=token,
        expected_roles=["USER", "ADMIN"],
        endpoint="trend_analyses",
        values=f"ticker = {ticker}, host = {request.client.host}",
    )

    data = services.return_trend_analyses.get_trend_analyses(ticker)

    return Response(data)


@app.get("/trend_analyses_archive_performance")
def return_trend_archive_analyses(token: str, ticker: str):

    verify_token(
        token=token,
        expected_roles=["USER", "ADMIN"],
        endpoint="trend_analyses_archive_performance",
        values=f"ticker = {ticker}",
    )

    data = services.return_trend_analyses.get_trend_archive_analyses(ticker)

    return Response(data)


@app.get("/trend_analyses_archive_history_trades")
def return_trend_archive_trades(token: str, ticker: str):

    verify_token(
        token=token,
        expected_roles=["USER", "ADMIN"],
        endpoint="trend_analyses_archive_history_trades",
        values=f"ticker = {ticker}",
    )

    data = services.return_trend_analyses.get_trend_analyses_trades(ticker)

    return Response(data)


@app.get("/trend_analyses_trade_options")
def return_all_trend_options(
    token: str,
    page: int = 1,
    long: bool = True,
    short: bool = False,
    amount_days_of_new_trend: int = 5,
    percentage_2y_profitble: float = 90,
):

    verify_token(
        token=token,
        expected_roles=["USER", "ADMIN"],
        endpoint="trend_analyses_trade_options",
        values=f"page = {page},long = {long}, short = {short}",
    )

    data = services.return_trend_trade_options.return_trade_options(
        page=page,
        long=long,
        short=short,
        amount_days_of_new_trend=amount_days_of_new_trend,
        percentage_2y_profitble=percentage_2y_profitble,
    )

    return Response(data)


@app.get("/trend_strategy_status")
def return_all_trend_specs():

    data = services.return_trend_analyses.get_all_trend_specs()

    return Response(data)


@app.get("/avalible_portfolios")
def avalible_portfolios(
    token: str,
    page: int = 1,
    portfolio_strategy: str = "",
    amount_rows: int = 20,
    min_amount_stocks: int = 5,
    max_amount_stocks: int = 6,
):

    verify_token(
        token=token,
        expected_roles=["USER", "ADMIN"],
        endpoint="avalible_portfolios",
        values=f"page = {page},portfolio_strategy = {portfolio_strategy}, amount_rows = {amount_rows}, max_amount_stocks = {max_amount_stocks}",
    )

    data = services.return_portfolios_options.return_portfolios(
        page_number=page,
        portfolio_strategy=portfolio_strategy,
        page_amount=amount_rows,
        min_amount_stocks=min_amount_stocks,
        max_amount_stocks=max_amount_stocks,
    )

    return Response(data)


@app.get("/trading_portfolios")
def avalible_trading_portfolios(token: str, portfolio_id, request: Request):

    verify_token(
        token=token,
        expected_roles=["USER", "ADMIN"],
        endpoint="trading_portfolios",
        values=f"portfolio_id = {portfolio_id} host = {request.client.host}",
    )

    data = services.return_portfolios_options.return_trading_portfolios(
        id_=portfolio_id
    )

    return Response(data)


@app.post("/add_portfolios")
def add_portfolios(token: str, portfolio_id: str):

    verify_token(
        token=token,
        expected_roles=["USER", "ADMIN"],
        endpoint="add_portfolios",
        values=f"portfolio_id = {portfolio_id}",
    )

    data = services.return_portfolios_options.add_trading_portfolio(
        id_=portfolio_id
    )

    return data


@app.post("/add_portfolios_manually")
def add_manual_portfolios(token: str, portfolio_tickers: list):

    verify_token(
        token=token,
        expected_roles=["USER", "ADMIN"],
        endpoint="add_portfolios_manually",
        values=f"portfolio_tickers = {portfolio_tickers}",
    )

    data = services.return_portfolios_options.add_trading_portfolio_manual(
        id_=portfolio_tickers
    )

    return data


@app.delete("/remove_portfolio")
def remove_portfolio(token: str, portfolio_id: str):

    verify_token(
        token=token,
        expected_roles=["USER", "ADMIN"],
        endpoint="remove_portfolio",
        values=f"portfolio_id = {portfolio_id}",
    )

    data = services.return_portfolios_options.delete_trading_portfolio(
        id_=portfolio_id
    )

    return data


@app.get("/show_portfolio_performance")
def return_portfolio_performance(token: str, portfolio_id: str):

    verify_token(
        token=token,
        expected_roles=["USER", "ADMIN"],
        endpoint="show_portfolio_performance",
        values=f"portfolio_id = {portfolio_id}",
    )

    data = services.return_stats.return_trading_backtest(
        portfolio_id=portfolio_id
    )

    return data


@app.get("/show_logs")
def return_logs(token: str, page_number_in: int = 1):

    verify_token(
        token=token,
        expected_roles=["ADMIN", "USER"],
        endpoint="show_logs",
        values=f"page_number = {page_number_in}",
    )

    data = services.return_logs.return_logs_page(page_number=page_number_in)

    return data


@app.get("/show_special_logs")
def return_special_logs(
    token: str,
    page_number: int = 1,
    search_endpoint: str = None,
    search_user: str = None,
    page: int = 1,
    page_size: int = 100,
):

    verify_token(
        token=token,
        expected_roles=["ADMIN"],
        endpoint="show_logs",
        values=f"page_number = {page_number}",
    )

    data = get_user_activity_data(page_number, search_user, page, page_size)

    return data


@app.get("/show_user_trades")
def return_user_trades(
    token: str,
    trader_id: str = "49a55c9c-8dbd-11ed-8abb-001a7dda7110",
):
    verify_token(
        token=token,
        expected_roles=["ADMIN", "USER"],
        endpoint="show_user_trades",
        values=f"trader_id = {trader_id}",
    )

    data = services.return_trend_analyses.get_user_trades(
        uuid_portfolio=trader_id
    )

    return data


@app.post("/add_user_trades")
def add_user_trade(
    token: str,
    trader_id: str = "49a55c9c-8dbd-11ed-8abb-001a7dda7110",
    ticker: str = "",
):
    verify_token(
        token=token,
        expected_roles=["ADMIN", "USER"],
        endpoint="add_user_trades",
        values=f"trader_id = {trader_id}, ticker = {ticker}",
    )

    data = services.crud_user_trades.add_user_trade(
        uu_id_trader=trader_id, ticker_name=ticker
    )

    return data


@app.delete("/remove_user_trades")
def return_logs(
    token: str,
    trader_id: str = "49a55c9c-8dbd-11ed-8abb-001a7dda7110",
    ticker: str = "",
):

    verify_token(
        token=token,
        expected_roles=["ADMIN", "USER"],
        endpoint="remove_user_trades",
        values=f"trader_id = {trader_id}, ticker = {ticker}",
    )

    data = services.crud_user_trades.remove_user_trade(
        uu_id_trader="49a55c9c-8dbd-11ed-8abb-001a7dda7110", ticker_name=ticker
    )

    return data


@app.get("/avalible_tickers")
def return_all_tickers(
    token: str,
):

    verify_token(
        token=token,
        expected_roles=["ADMIN", "USER"],
        endpoint="avalible_tickers",
        values=f"trader id",
    )

    data = services.return_trend_analyses.get_all_tickers()

    return Response(data)


@app.post("/add_or_maintain_ticker")
def add_or_maintain_ticker(token: str, ticker: str = ""):

    verify_token(
        token=token,
        expected_roles=["ADMIN", "USER"],
        endpoint="add_or_maintain_ticker",
        values=f"ticker = {ticker}",
    )

    data = services.maintenance_tickers.add_or_remove_ticker(ticker)

    return data


@app.get("/sector_strategy")
def return_sector_strategy(
    token: str,
):

    verify_token(
        token=token,
        expected_roles=["ADMIN", "USER"],
        endpoint="sector_strategy",
        values=f" no values",
    )

    data = services.return_trend_analyses.get_sector_analyses()

    return Response(data)


@app.post("/create_portfolio_strategys_list")
def add_portofolio_strategys(token: str, name_strategy: str = ""):

    verify_token(
        token=token,
        expected_roles=["ADMIN"],
        endpoint="create_portfolio_strategys_list",
        values=f" name_strategy = {name_strategy} ",
    )

    data = database_querys.add_list_portfolio_strategys(
        name_list=name_strategy
    )

    return data


@app.post("/add_ticker_to_portfolio_strategys")
def add_ticker_to_portofolio_strategys(
    token: str, name_strategy: str = "", name_ticker: str = ""
):
    verify_token(
        token=token,
        expected_roles=["ADMIN"],
        endpoint="add_ticker_to_portfolio_strategys",
        values=f" name_strategy = {name_strategy}, name_ticker = {name_ticker} ",
    )

    data = database_querys.add_tickers_to_list(
        name_list=name_strategy, name_ticker=name_ticker
    )

    return data


@app.delete("/remove_portfolio_strategys")
def remove_list_portfolio_strategys(
    token: str, name_list: str = "", ticker_name: str = ""
):

    verify_token(
        token=token,
        expected_roles=["ADMIN"],
        endpoint="add_ticker_to_portfolio_strategys",
        values=f" name_list = {name_list}, ticker_name = {ticker_name} ",
    )

    data = database_querys.remove_list_portfolio_strategys(
        name_list, ticker_name
    )

    return data


@app.get("/return_portfolio_strategys")
def return_portofolio_strategys(
    token: str,
    name_list: str = "",
    ticker_name: str = "",
    return_all: bool = False,
):

    verify_token(
        token=token,
        expected_roles=["ADMIN"],
        endpoint="add_ticker_to_portfolio_strategys",
        values=f" name_list = {name_list}, ticker_name = {ticker_name} return_all = {return_all}",
    )

    data = database_querys.return_list_portfolio_strategys(
        name_list=name_list, ticker_name=ticker_name, return_all=return_all
    )

    return Response(data)


@app.get("/return_all_sector_trend_analyses_data")
def return_all_sector_trend_analyses_data(
    token: str,
):

    verify_token(
        token,
        ["SIENTIST", "USER", "ADMIN"],
        endpoint="return_all_sector_trend_analyses_data",
        values="KWEE",
    )

    data = services.return_trend_analyses.get_all_trend_analyses_cache()

    return data


@app.get("/return_sector_trend_options")
def return_sector_trend_options(
    token: str,
):

    verify_token(
        token,
        ["SIENTIST", "USER", "ADMIN"],
        endpoint="return_all_sector_trend_analyses_data",
        values="KWEE",
    )

    data = services.return_trend_analyses.get_all_types_of_trend_timeseries()

    return data


@app.post("/return_sector_trend_analyses")
def return_sector_trend_analyses(token: str, name_analyses: str):

    verify_token(
        token,
        ["SIENTIST", "USER", "ADMIN"],
        endpoint="return_all_sector_trend_analyses_data",
        values="KWEE",
    )

    data = services.return_trend_analyses.get_trend_timeseries_cached(
        name=name_analyses
    )

    return data


handler = Mangum(app)

if __name__ == "__main__":

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        debug=False,
        workers=4,
        limit_concurrency=1000,
    )
