# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 13:40:23 2023

@author: Gebruiker
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core_utils.database_tables.tabels import (
    User,
)  # Replace "your_module" with the correct module where the User class is defined
from database_connection import get_db_connection


def get_user_input():
    users = []
    while True:
        username = input(
            "Enter the username (or type 'exit' to stop entering users): "
        )
        if username.lower() == "exit":
            break

        password = input("Enter the password: ")
        role = ""
        while role not in ["USER", "SCIENTIST"]:
            role = input("Enter the role (USER or SCIENTIST): ").upper()

        user_data = {
            "username": username,
            "password": password,
            "role": role,
        }
        users.append(user_data)

    return users


def insert_users_to_database(users):
    connection_Db = get_db_connection()
    with connection_Db as session:
        for user_data in users:
            user = User(**user_data)
            session.add(user)

        # Commit the changes to the database
        session.commit()


if __name__ == "__main__":
    users_data = get_user_input()
    insert_users_to_database(users_data)
