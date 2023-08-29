# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 14:48:20 2022

@author: Gebruiker
"""
import os
import sys


# stock details
stock_avalible_analyses = (
    "stock_data",
    "liquidity_data",
    "moneyflow_data",
    "time_serie_data",
)

stock_avalible_periodes = "d", "w"

stock_avalible_timeframes = "q", "y", "y1", "y3", "y5", "y10", "all"

# analyses details
analyses_time_series = [
    "indicator_timeserie_raw",
    "indicator_timeserie_profile",
    "indicator_timeserie_profile_change",
    "indicator_timeserie_change",
]
analyses_single_vars = [
    "last_calculation_indicator",
    "last_calculation_profile_indicator_text",
    "last_calculation_profile_indicator_number",
    "last_calculation_profile_change_text",
    "last_calculation_profile_change_number",
]


# project_root.
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# project folders
CORE_DATA_____PATH = os.path.join(ROOT_DIR, "core_data")
CORE_SCIPTS___PATH = os.path.join(ROOT_DIR, "core_scripts")
CORE_SERVICE__PATH = os.path.join(ROOT_DIR, "core_service_layer")
CORE_UPDATE___PATH = os.path.join(ROOT_DIR, "core_update")
CORE_UTILS____PATH = os.path.join(ROOT_DIR, "core_utils")


# database
# SQLite extention
SQLite_EXTENTION = "sqlite:///"

# data_files
# project data_temp
DATA_TEMP_PATH = os.path.join(CORE_DATA_____PATH, "data_temp")
DATA_STOCK_DATA_PATH = os.path.join(CORE_DATA_____PATH, "stock_data")


# data_files.
DATABASE_HEAD_PATH = os.path.join(SQLite_EXTENTION, CORE_DATA_____PATH)
DATABASE_MAIN_PATH = os.path.join(DATABASE_HEAD_PATH, "flowimpact_api_db.db")

DABASE_INIT_FIPATH = os.path.join(CORE_UTILS____PATH, "core_initalization")
DATABASE_SPAN_PATH = os.path.join(DABASE_INIT_FIPATH, "flowimpact_api_db.db")

TICKER_DATA___PATH = os.path.join(CORE_DATA_____PATH, "stock_tickers_data")


# database path
db_dir = "../../core_data/flowimpact_api_db.db"
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.abspath(db_dir)  # works

db_dir = "../core_data/flowimpact_api_db.db"
SQLALCHEMY_DATABASE_URI_layer_one = "sqlite:///" + os.path.abspath(
    db_dir
)  # works

db_dir = "core_data/flowimpact_api_db.db"
SQLALCHEMY_DATABASE_URI_layer_zero = (
    "postgresql://root:root@85.215.212.222:5432/trend_impact_postgres"
)

# removed : after sqlite "sqlite://"
SQLALCHEMY_DATABASE_URI_Test = "sqlite://" + os.path.abspath(db_dir)
# additional file paths for linking
CORE_UPDATE_ALL_ANALYSES_PATH = os.path.join(
    CORE_UPDATE___PATH, "update_analyses"
)

APIKEY_FINNHUB = "cirr0upr01qhsmrvtj70cirr0upr01qhsmrvtj7g"
