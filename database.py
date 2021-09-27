import psycopg2
import numpy as np
from psycopg2.extensions import register_adapter, AsIs
psycopg2.extensions.register_adapter(np.int64, psycopg2._psycopg.AsIs)
import logging
import os
from config import \
    DB_USER, \
    DB_PASS, \
    DB_HOST, \
    DB_PORT, \
    DB_NAME

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class DataBaseConn:
    def __init__(self, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT, database=DB_NAME):
        logging.info("Db Starting the Connection")
        self._conn = psycopg2.connect(user=user,
                                      password=password,
                                      host=host,
                                      port=port,
                                      database=database)
        self._cursor = self._conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb is None:
            self.commit()
        else:
            logging.info("Rollbacking")
            self.rollback()
        logging.info("Db Closing the Connection")
        self.close()

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def rollback(self):
        self.connection.rollback()

    def commit(self):
        self.connection.commit()

    def close(self, commit=True):
        if commit:
            self.commit()
        self.connection.close()

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchall()

def get_query(query_name):
    abs_path = os.path.dirname(os.path.abspath(__file__)) + '/'
    with open(abs_path + 'queries/%s.sql' % query_name, 'r') as query:
        return query.read()
