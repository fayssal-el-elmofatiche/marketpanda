# © Copyright 2023 dnbf.tech GmbH
# Created by fayssalelmofatiche at 10.10.23
# Description: Class for defining different functions for data retrieval from sqlite database
from typing import List
import sqlite3
import os
from datetime import datetime
import pandas as pd


class MarketPanda:
    """
    Class for defining different functions for data retrieval from sqlite database
    """

    def __init__(self, db_path: str = None):
        """
        Initialize MarketPanda object
        """

        if db_path is None:
            # throw exception that the online database is not yet implemented
            raise NotImplementedError("Online database is not yet implemented. Please provide the path to a local database.")

        # Get the directory name of the current working directory
        #current_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct the path to the database
        #self.db_path = os.path.join(current_dir, db_path)
        self.db_path = db_path
        print(f"MarketPanda init: {self.db_path=}")

        # check if path exists
        if not os.path.exists(self.db_path):
            raise ValueError(f"Path {self.db_path} does not exist.")
        else:
            print(f"Path {self.db_path} exists.")

        self.conn = sqlite3.connect(self.db_path)

        

    # properties
    @property
    def db_path(self):
        return self._db_path

    @db_path.setter
    def db_path(self, db_path):
        self._db_path = db_path

    @property
    def conn(self):
        return self._conn

    @conn.setter
    def conn(self, conn):
        self._conn = conn

    @property
    def tables(self):
        # get list of tables from database
        query = "SELECT name FROM sqlite_master WHERE type='table';"
        tables = self.conn.execute(query).fetchall()
        return tables
    
    @property
    def tickers(self):
        """
        Retrieve all tickers from sqlite database
        :return: list of tickers
        """

        query = f"SELECT ticker, id FROM symbol;"
        df = pd.read_sql(query, self.conn)
        return df
    
    @property
    def ticker_ids(self):
        """
        Retrieve all ticker ids from sqlite database
        :return: list of ticker ids
        """

        query = f"SELECT id FROM symbol;"
        df = pd.read_sql(query, self.conn)
        return df
    
    @property
    def symbols(self):
        """
        Retrieve all symbols from sqlite database
        :return: list of symbols
        """

        query = f"SELECT * FROM symbol;"
        df = pd.read_sql(query, self.conn)
        return df
    
    @property
    def data_vendors(self):
        """
        Retrieve all data vendors from sqlite database
        :return: list of data vendors
        """

        query = f"SELECT * FROM data_vendor;"
        df = pd.read_sql(query, self.conn)
        return df
    
    @property
    def cpi(self):
        """
        Retrieve all cpi data
        :return: list of cpi
        """
        # Get the directory name of the database folder
        data_dir = os.path.dirname(os.path.abspath(self.db_path))
        print(f"data_dir: {data_dir}")

        # Construct the path to the cpi.csv file
        cpi_path = os.path.join(data_dir, "cpi.csv")

        df = pd.read_csv(cpi_path)
        return df
    
    
    def get_tickers(self) -> pd.DataFrame:
        """
        Retrieve all tickers from sqlite database
        :return: list of tickers
        """

        query = f"SELECT ticker, id FROM symbol;"
        df = pd.read_sql(query, self.conn)
        return df

    def get_ticker_id(self, ticker: str):
        """
        Retrieve ticker id from sqlite database
        :param ticker: string representing the ticker, e.g. "AAPL"
        :return: ticker id
        """
        query = f"SELECT id FROM symbol WHERE ticker = '{ticker}';"
        ticker_id = self.conn.execute(query).fetchone()[0]
        return ticker_id

    def get_data(self, tickers: List[str], start: str = None, end: str = None) -> pd.DataFrame:
        """
        Retrieve time series data from sqlite database for a list of tickers
        :param tickers:
        :return:
        """

        # get ticker ids
        ticker_ids = [self.get_ticker_id(ticker) for ticker in tickers]

        if len(ticker_ids) == 0:
            return pd.DataFrame()
        elif len(ticker_ids) == 1:
            symbol_id_where = f"symbol_id = {ticker_ids[0]}"
        else:
            symbol_id_where = f"symbol_id IN {tuple(ticker_ids)}"

        # check if start and end are provided
        if start is not None and end is not None:
            query = f"SELECT * FROM daily_price WHERE {symbol_id_where} AND price_date BETWEEN '{start}' AND '{end}';"
        else:
            query = f"SELECT * FROM daily_price WHERE {symbol_id_where};"

        df = self.get_query_data(query)

        # add column with corresponding ticker
        df["ticker"] = df.apply(lambda row: tickers[ticker_ids.index(row.name[0])], axis=1)

        return df

    def get_query_data(self, query: str) -> pd.DataFrame:
        """
        Retrieve time series data from sqlite database for a given query as a pandas dataframe
        :param query: string representing the SQL query
        :return: pandas dataframe with time series data for query.
        """
        df = pd.read_sql(query, self.conn)

        # convert to pandas dataframe
        df["date"] = pd.to_datetime(df["price_date"])
        df = df.set_index(["symbol_id", "price_date"])

        return df

    def get_data_by_date(self, tickers: List[str], date: str) -> pd.DataFrame:
        """
        Retrieve time series data from sqlite database for a list of tickers
        :param date: date in format YYYY-MM-DD
        :param tickers: list of tickers
        :return: pandas dataframe with time series data for the list of tickers.
        """
        print(f"DataWaiter get_data: {tickers}")

        # get ticker ids
        ticker_ids = [self.get_ticker_id(ticker) for ticker in tickers]
        query: str = f"SELECT * FROM daily_price WHERE symbol_id IN {tuple(ticker_ids)} AND price_date = '{date}';"

        df = self.get_query_data(query)

        # add column with corresponding ticker
        df["ticker"] = df.apply(lambda row: tickers[ticker_ids.index(row.name[0])], axis=1)

        return df
