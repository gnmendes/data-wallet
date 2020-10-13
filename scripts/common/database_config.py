import sqlite3
import threading


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
            DBConfig.__connection = sqlite3.connect('data-wallet.db', check_same_thread=False)

    @staticmethod
    def close_cursor(cursor):
        if cursor:
            cursor.close()
