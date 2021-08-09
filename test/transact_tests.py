import unittest
import json
from src.initial_config import Configuration
Configuration(True)
from src.endpoints import app


class TransactionalTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.app_client = app.test_client()

    def test_deve_inserir_transacao_com_cpf_tipo_inteiro(self):
        response = self.app_client.post('/chain',
                                        data=json.dumps(self.__get_unconfirmed_transact()),
                                        headers={'Content-Type': 'application/json'})
        self.assertEqual(201, response.status_code,
                         'O status code deve ser 201 indicando que a transação foi adicionada')
        self.assertIn('transação não confirmada adicionada', response.json['message'].lower())

    def test_deve_minerar_um_bloco(self):
        response = self.app_client.get('/chain/mine')

        self.assertEqual(200, response.status_code, 'O bloco deve ter sido minerado')
        self.assertEqual(2, response.json['index'], 'O indice deve ser o 2')
        self.assertEqual('New block forged!', response.json['message'], 'A mensagem quando minerado com sucesso'
                                                                        'deve corresponder')

    def test_deve_trazer_a_representacao_cadeia(self):
        response = self.app_client.get('/chain')

        self.assertEqual(200, response.status_code, 'O status deve indicar que a requisicao ocorreu OK')
        self.assertEqual(2, response.json['length'], 'O comprimento da cadeia deve corresponder')

    @staticmethod
    def __get_unconfirmed_transact():
        return {
            'sender': 36968670046,
            'recipient': 85846492045,
            'data': {
                'idade':  21,
                'nome': 'Gabriel Mendes'
            }
        }


if __name__ == '__main__':
    unittest.main()
