import enum
from scripts.common.database_config import DBConfig


class SQLStatements(enum.Enum):
    CREATE_TABLE = 'CREATE TABLE IF NOT EXISTS TB_SALDO_OPERACAO( ' \
                   'ID_OPERACAO INTEGER PRIMARY KEY,' \
                   'VALOR DOUBLE NOT NULL CHECK (VALOR > 0), ' \
                   'DT_OPERACAO TIMESTAMP DEFAULT CURRENT_TIMESTAMP , ' \
                   'TP_OPERACAO CHAR(1) CHECK (TP_OPERACAO IN ("C", "D")) )'

    CREDITAR_OU_DEBITAR = 'INSERT INTO TB_SALDO_OPERACAO (VALOR, TP_OPERACAO)' \
                          'VALUES' \
                          '(?, ?)'

    CONSULTAR_SALDO = 'SELECT SUM(COALESCE (VALOR, 0)), TP_OPERACAO FROM TB_SALDO_OPERACAO GROUP BY TP_OPERACAO'


class TransactionalOps:

    def __init__(self):
        cursor = DBConfig.get_instance().cursor()
        cursor.execute(SQLStatements.CREATE_TABLE.value)
        DBConfig.close_cursor(cursor=cursor)

    @staticmethod
    def creditar_ou_debitar_valor(valor, op):

        if float(valor) > 0 and op in ['C', 'D']:
            cursor = None
            try:
                connection = DBConfig.get_instance()
                cursor = connection.cursor()
                cursor.execute(SQLStatements.CREDITAR_OU_DEBITAR.value, (valor, op))
                connection.commit()
                return {'mensagem': 'Sucesso!', 'valorInserido': valor}
            except Exception as error:
                print(str(error))
                return {'mensagem': 'Erro ao tentar realizar a operacao!'}
            finally:
                DBConfig.close_cursor(cursor=cursor)

    @staticmethod
    def consultar_saldo():
        cursor = None
        try:
            connection = DBConfig.get_instance()
            cursor = connection.cursor()
            cursor.execute(SQLStatements.CONSULTAR_SALDO.value)
            credito = debito = 0
            result_set = cursor.fetchall()
            for row in result_set:
                if 'C' in row:
                    credito = row[0]
                else:
                    debito = row[0] or 0

            return {'saldo': credito - debito}
        except Exception as error:
            print(str(error))
            return {'mensagem': 'Erro ao tentar realizar a operacao!'}
        finally:
            DBConfig.close_cursor(cursor=cursor)
