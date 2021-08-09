import os
import enum
from src.common.database_config import DBConfig


class DDL(enum.Enum):
    CREATE_TABLE_ARQUIVOS_INFO = """
        CREATE TABLE IF NOT EXISTS TB_ARQUIVOS_INFO
        (
            ID_ARQUIVO      INTEGER PRIMARY KEY,
            NOME_ARQUIVO    TEXT NOT NULL,
            TIPO_CONTEUDO   TEXT NOT NULL,
            CORPO           BLOB NOT NULL,
            DT_INSERCAO     TIMESTAMP DEFAULT CURRENT_TIMESTAP
        )
        
    """

    CREATE_TABLE_SALDO_OPERACAO = """
        CREATE TABLE IF NOT EXISTS TB_SALDO_OPERACAO
        (
            ID_OPERACAO INTEGER PRIMARY KEY,
            VALOR       DOUBLE NOT NULL CHECK (VALOR > 0),
            DT_OPERACAO TIMESTAMP  DEFAULT CURRENT_TIMESTAMP,
            TP_OPERACAO CHAR(1) CHECK (TP_OPERACAO IN ("C", "D"))
        )
    """


class Configuration:

    def __init__(self, test_call=None):
        self.__setup_for_tests(is_test=test_call)
        self.__db = DBConfig.get_instance()
        self.__cursor = self.__db.cursor()
        self.__execute_ddl_statements()

    def __execute_ddl_statements(self):
        for ddl in DDL:
            self.__cursor.execute(ddl.value)
        DBConfig.close_cursor(cursor=self.__cursor)

    @staticmethod
    def __setup_for_tests(is_test):
        if is_test:
            os.system('del *.db')
            os.environ.update({'database_test_name': 'dw-test.db'})
