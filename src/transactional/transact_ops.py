import enum
from src.common.database_config import DBConfig


class TransactionalSQLStatements(enum.Enum):

    CREDITAR_OU_DEBITAR = 'INSERT INTO TB_SALDO_OPERACAO (VALOR, TP_OPERACAO)' \
                          'VALUES' \
                          '(?, ?)'

    CONSULTAR_SALDO = 'SELECT SUM(COALESCE (VALOR, 0)), TP_OPERACAO FROM TB_SALDO_OPERACAO GROUP BY TP_OPERACAO'


class TransactionalOps:

    @staticmethod
    def creditar_ou_debitar_valor(valor, op):

        if float(valor) > 0 and op in ['C', 'D']:
            cursor = None
            try:
                connection = DBConfig.get_instance()
                cursor = connection.cursor()
                cursor.execute(TransactionalSQLStatements.CREDITAR_OU_DEBITAR.value, (valor, op))
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
            cursor.execute(TransactionalSQLStatements.CONSULTAR_SALDO.value)
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
