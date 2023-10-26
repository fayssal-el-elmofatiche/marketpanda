# build_db_tables.py

# Imports
import sqlite3
import os
from dotenv import load_dotenv


def create_exchange_table(connection, cursor):
    """Create the exchange table to store the details
    of traded exchanges.

    Parameters
    ----------
    connection : 'psycopg2.extensions.connection'
        The connection object to interact
        with the database
    cursor : 'psycopg2.extensions.cursor'
        The cursor object that accepts SQL
        commands
    """

    cursor.execute("""
    CREATE TABLE exchange(
    id SERIAL PRIMARY KEY NOT NULL,
    abbrev VARCHAR(32) NOT NULL,
    name VARCHAR(255) NOT NULL,
    city VARCHAR(255) NULL,
    country VARCHAR(255) NULL,
    currency VARCHAR(64) NULL,
    timezone_offset TIME NULL,
    created_date TIMESTAMPTZ NOT NULL,
    last_updated TIMESTAMPTZ NOT NULL
    )""")
    connection.commit()


def create_data_vendor_table(connection, cursor):
    """Create the exchange table to store the details
    of traded exchanges.

    Parameters
    ----------
    connection : 'psycopg2.extensions.connection'
        The connection object to interact
        with the database
    cursor : 'psycopg2.extensions.cursor'
        The cursor object that accepts SQL
        commands
    """

    cursor.execute("""
    CREATE TABLE data_vendor(
    id SERIAL PRIMARY KEY NOT NULL,
    name VARCHAR(64) NOT NULL,
    website_url VARCHAR(255) NULL,
    support_email VARCHAR(255) NULL,
    created_date TIMESTAMPTZ NOT NULL,
    last_updated TIMESTAMPTZ NOT NULL
    )""")
    connection.commit()


def create_symbol_table(connection, cursor):
    """Create the exchange table to store the details
    of traded exchanges.

    Parameters
    ----------
    connection : 'psycopg2.extensions.connection'
        The connection object to interact
        with the database
    cursor : 'psycopg2.extensions.cursor'
        The cursor object that accepts SQL
        commands
    """

    cursor.execute("""
    CREATE TABLE symbol(
    id SERIAL PRIMARY KEY NOT NULL,
    exchange_id INT NULL REFERENCES exchange (id) ON DELETE RESTRICT ON UPDATE CASCADE,
    ticker VARCHAR(32) NOT NULL,
    instrument VARCHAR(64) NOT NULL,
    name VARCHAR(255) NULL,
    sector VARCHAR(255) NULL,
    currency VARCHAR(32) NULL,
    current_constituent BOOLEAN NOT NULL,
    created_date TIMESTAMPTZ NOT NULL,
    last_updated TIMESTAMPTZ NOT NULL
    )""")
    connection.commit()


def create_daily_price_table(connection, cursor):
    """Create the exchange table to store the details
    of traded exchanges.

    Parameters
    ----------
    connection : 'psycopg2.extensions.connection'
        The connection object to interact
        with the database
    cursor : 'psycopg2.extensions.cursor'
        The cursor object that accepts SQL
        commands
    """

    cursor.execute("""
    CREATE TABLE daily_price(
    id SERIAL PRIMARY KEY NOT NULL,
    data_vendor_id INT NOT NULL REFERENCES data_vendor (id) ON DELETE RESTRICT ON UPDATE CASCADE,
    symbol_id INT NOT NULL REFERENCES symbol (id) ON DELETE RESTRICT ON UPDATE CASCADE,
    price_date DATE NOT NULL,
    created_date TIMESTAMPTZ NOT NULL,
    last_updated TIMESTAMPTZ NOT NULL,
    open_price NUMERIC(19,4) NULL,
    high_price NUMERIC(19,4) NULL,
    low_price NUMERIC(19,4) NULL,
    close_price NUMERIC(19,4) NULL,
    volume BIGINT NULL
    )""")
    connection.commit()


def create_cpi_table(connection):
    """
    Create the cpi table to store the relevant details of the cpi data
    
    Parameters
    ----------
    connection : 'sqlite3.connection'
        The connection object to interact
        with the database
    """

    cursor = connection.cursor()
    cursor.execute("""
CREATE TABLE cpi(
    id INTEGER PRIMARY KEY NOT NULL,
    date DATE NOT NULL,
    year INT NOT NULL,
    value NUMERIC NOT NULL,
    series_id TEXT NOT NULL,
    series_title TEXT NOT NULL,
    series_survey TEXT NOT NULL,
    series_seasonally_adjusted INTEGER NOT NULL,
    series_periodicity_id TEXT NOT NULL,
    series_periodicity_code TEXT NOT NULL,
    series_periodicity_name TEXT NOT NULL,
    series_area_id TEXT NOT NULL,
    series_area_code TEXT NOT NULL,
    series_area_name TEXT NOT NULL,
    series_items_id TEXT NOT NULL,
    series_items_code TEXT NOT NULL,
    series_items_name TEXT NOT NULL,
    period_id TEXT NOT NULL,
    period_code TEXT NOT NULL,
    period_name TEXT NOT NULL,
    period_abbreviation TEXT NOT NULL,
    period_month INT NOT NULL,
    period_type TEXT NOT NULL);
    """)
    connection.commit()
    cursor.close()
    print("cpi table created successfully")


if __name__ == "__main__":
    conn = sqlite3.connect("../data/marketvault.db")
    cur = conn.cursor()

    # Build the tables in the remote database.
    table_creators = [
        #create_exchange_table,
        #create_data_vendor_table,
        #create_symbol_table,
        #create_daily_price_table,
        create_cpi_table
    ]

    for creator in table_creators:
        creator(conn, cur)

    # Close connections to the database
    cur.close()
    conn.close()
    print(
        f"The following tables have successfully been added {table_creators}"
    )

