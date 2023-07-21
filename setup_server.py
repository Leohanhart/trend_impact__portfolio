# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 17:24:19 2023

@author: Gebruiker
"""
from sqlalchemy import create_engine, MetaData
import database_connection
import initializer_db
from initializer_tickers_main import InitializeTickers
from core_utils.database_tables.tabels import User
import database_querys_main
from loguru import logger


def check_connection():

    database_connection.test_postgresql_connection()


def check_if_tables_exsist():

    engine = database_connection.get_db_engine()

    # important tables.
    table_names = [
        "tickers",
        "analyses_trend_kamal_performance",
        "analyses_trend_kamal",
    ]

    with engine.connect() as conn:
        table_exists = [
            engine.dialect.has_table(conn, table_name)
            for table_name in table_names
        ]

    # Check if tables exist
    if all(table_exists):
        logger.info("All tables exist.")
        return True
    else:
        missing_tables = [
            table_names[i]
            for i, exists in enumerate(table_exists)
            if not exists
        ]
        logger.warning(
            f"The following tables are missing: {', '.join(missing_tables)}"
        )

        if missing_tables:
            return False
        else:
            return True


def setup_users():

    db_connection = database_connection.get_db_connection()

    # Add users to the database
    users = [
        {
            "username": "LEODEADMIN",
            "password": "QWERTY12345",
            "role": "ADMIN",
        },
        {
            "username": "KWEE",
            "password": "UTRECHT123OPENICT",
            "role": "SCIENTIST",
        },
        {
            "username": "SWEN_TRADER_ZERO",
            "password": "DAVINCICOLLEGEWASEENGRAPIN2020",
            "role": "USER",
        },
        {
            "username": "ALGO_JACK",
            "password": "THISISJUSTANALGOWITHOUTANYIDEAS2023WESTARTED",
            "role": "USER",
        },
        {
            "username": "JOB_AND_FAM",
            "password": "ORCAWASJUSTAJOKE",
            "role": "USER",
        },
    ]

    with db_connection as session:

        for user_data in users:
            user = User(**user_data)
            session.add(user)

        # Commit the changes to the database
        session.commit()


def initialize_server():
    logger.info("Starting server initalization")
    check_connection()
    if not check_if_tables_exsist():
        # init db
        initializer_db.initialization()

        database_querys_main.database_querys.add_log_to_logbook(
            "Server DB initalized"
        )
        # init tickers
        InitializeTickers.initialize_all_tickers()

        database_querys_main.database_querys.add_log_to_logbook(
            "Tickers initalized"
        )
        # setup account
        setup_users()
