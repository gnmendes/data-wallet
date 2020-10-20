import os
import sqlite3
import threading
from dotenv import load_dotenv
load_dotenv()


class DBConfig:
    __connection = None

    @staticmethod
    def get_instance():
        if DBConfig.__connection is None:
            with threading.Lock():
                if DBConfig.__connection is None:
                    DBConfig()
        return DBConfig.__connection

    def __init__(self):
        if DBConfig.__connection is not None:
            raise Exception('Its a Singleton Class')
        else:
            db_name = os.environ.get('DATABASE_TEST_NAME') or os.environ.get('DATABASE_NAME')
            DBConfig.__connection = sqlite3.connect(db_name, check_same_thread=False)

    @staticmethod
    def close_cursor(cursor):
        if cursor:
            cursor.close()
