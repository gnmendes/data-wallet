import enum
import base64
from scripts.common.utilities import Util
from scripts.common.database_config import DBConfig


class SQLStatements(enum.Enum):
    CREATE_TABLE_ARQUIVOS_INFO = 'CREATE TABLE IF NOT EXISTS ' \
                                 'TB_ARQUIVOS_INFO( ' \
                                 'ID_ARQUIVO INTEGER PRIMARY KEY,' \
                                 'NOME_ARQUIVO TEXT NOT NULL,' \
                                 'TIPO_CONTEUDO TEXT NOT NULL,' \
                                 'CORPO BLOB NOT NULL,' \
                                 'DT_INSERCAO TIMESTAMP DEFAULT CURRENT_TIMESTAMP )'

    BUSCAR_ARQUIVOS = 'SELECT * FROM TB_ARQUIVOS_INFO'

    BUSCAR_ARQUIVO_POR_ID = 'SELECT * FROM TB_ARQUIVOS_INFO WHERE ID_ARQUIVO IN (?)'

    INSERIR_ARQUIVO = 'INSERT INTO TB_ARQUIVOS_INFO (NOME_ARQUIVO,' \
                      'TIPO_CONTEUDO,' \
                      'CORPO)' \
                      'VALUES' \
                      '(?,' \
                      '?,' \
                      ' ?)'

    DELETAR_ARQUIVOS_POR_ID = 'DELETE FROM TB_ARQUIVOS_INFO WHERE ID_ARQUIVO IN (?)'


class FileOps:
    def __init__(self):
        cursor = DBConfig.get_instance().cursor()
        self.__create_archives_table(cursor=cursor)
        DBConfig.close_cursor(cursor=cursor)

    def insert_new_files(self, files):
        files = self.__get_files(data=files)
        files_to_be_inserted = []
        for file in files:
            files_to_be_inserted.append((file.filename, file.content_type, file.read()))
        cursor = None
        try:
            connection = DBConfig.get_instance()
            cursor = connection.cursor()
            cursor.executemany(SQLStatements.INSERIR_ARQUIVO.value, files_to_be_inserted)
            connection.commit()
            return {'message': 'Total de linhas inseridas %d' % cursor.rowcount}
        except Exception as error:
            print(str(error))
            return Util.produces_error_object(err=error)
        finally:
            DBConfig.close_cursor(cursor=cursor)

    @staticmethod
    def __get_files(data):
        return data.files.to_dict(flat=False)['archive']

    def get_files(self):
        cursor = None
        try:
            connection = DBConfig.get_instance()
            cursor = connection.cursor()
            cursor.execute(SQLStatements.BUSCAR_ARQUIVOS.value)
            result_set = list(cursor.fetchall())
            return self.__make_json_serializable(registers=result_set)
        except Exception as error:
            print(str(error))
            return Util.produces_error_object(err=error)
        finally:
            DBConfig.close_cursor(cursor=cursor)

    def get_file_by_id(self, id_file):
        cursor = None
        try:
            assert id_file
            connection = DBConfig.get_instance()
            cursor = connection.cursor()
            cursor.execute(SQLStatements.BUSCAR_ARQUIVO_POR_ID.value, id_file)
            registers = list(cursor.fetchall())
            return self.__make_json_serializable(registers=registers)
        except Exception as error:
            print(str(error))
            return Util.produces_error_object(err=error)
        finally:
            DBConfig.close_cursor(cursor=cursor)

    def remove_files(self, ids):
        cursor = None


        try:
            arquivos_excluidos = self.get_file_by_id(id_file=ids)
            if 'error' not in arquivos_excluidos:
                connection = DBConfig.get_instance()
                cursor = connection.cursor()
                cursor.execute(SQLStatements.DELETAR_ARQUIVOS_POR_ID, ids)
                connection.commit()
            return arquivos_excluidos
        except Exception as error:
            print(str(error))
            return Util.produces_error_object(err=error)
        finally:
            DBConfig.close_cursor(cursor=cursor)

    @staticmethod
    def __create_archives_table(cursor):
        cursor.execute(SQLStatements.CREATE_TABLE_ARQUIVOS_INFO.value)

    @staticmethod
    def __make_json_serializable(registers):
        json_acceptable = []
        for register in registers:
            valid_body = {
                'idArquivo': register[0],
                'nomeArquivo': register[1],
                'contentType': register[2],
                'corpo': base64.b64encode(register[3]).decode('utf-8'),
                'dataInsercao': register[4]
            }
            json_acceptable.append(valid_body)
        return json_acceptable
