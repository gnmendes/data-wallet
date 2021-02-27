import io
import json
from time import gmtime, strftime
import unittest
from scripts.initial_config import Configuration
Configuration(True)
from scripts.endpoints import app


class NonTransactTestCases(unittest.TestCase):

    def setUp(self) -> None:
        self.app_client = app.test_client()

    def test_deve_inserir_novos_arquivos(self) -> None:
        response = self.app_client.post('/arquivos',
                                        headers={'Content-Type': 'multipart/form-data'},
                                        data=self.__get_archive_mock())
        self.assertEqual(201, response.status_code, 'O código retornado deve ser 201, sinalizando que deu certo')
        self.assertIn('total de linhas inseridas', response.json['message'].lower(),
                      "O texto deve estar contido na mensagem")

    def test_deve_listar_arquivos(self) -> None:
        response = self.app_client.get('/arquivos')
        self.assertEqual(200, response.status_code, 'Os arquivos devem ser listados')
        self.assertIn(strftime('%Y-%m-%d', gmtime()), response.json[-1]['dataInsercao'],
                      'A data do último item inserido deve ser a de hoje')
        self.assertEqual(response.json[-1]['nomeArquivo'], 'mock-file.json', 'O nome do último arquivo inserido'
                                                                             'deve coincidir')

    def test_zdeve_excluir_primeiro_arquivo(self) -> None:
        response = self.app_client.delete('/arquivos/1')
        self.assertEqual(200, response.status_code, 'O arquivo de deve ter sido excluido')
        self.assertEqual(response.json[0]['nomeArquivo'], 'mock-file.json', 'O nome do arquivo excluido deve coincidir')
        self.assertEqual(response.json[0]['idArquivo'], 1, 'O id do arquivo excluido deve coincidir')

    @staticmethod
    def __get_archive_mock():
        return {'archive': (io.BytesIO(json.dumps({'nome': 'Gabriel', 'idade': 21})
                                       .encode()), 'mock-file.json')}


if __name__ == '__main__':
    unittest.main()
