# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 13:49:15 2023

@author: Gebruiker
"""

import psycopg2


def drop_all_tables(database_uri):
    try:
        conn = psycopg2.connect(database_uri)
        cursor = conn.cursor()

        # Get a list of all tables in the public schema
        cursor.execute(
            """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public';
        """
        )

        # Generate and execute SQL statements to drop each table
        for (table_name,) in cursor.fetchall():
            drop_table_query = f"DROP TABLE IF EXISTS {table_name} CASCADE;"
            cursor.execute(drop_table_query)

        conn.commit()
        cursor.close()
        conn.close()
        print("All tables dropped successfully.")

    except psycopg2.Error as e:
        print("Error:", e)


if __name__ == "__main__":
    database_uri = "postgresql://root:root@localhost:5432/trend_impact_postgres"  # Replace with your actual database URI
    drop_all_tables(database_uri)
