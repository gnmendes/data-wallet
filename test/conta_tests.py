import json
import unittest
from src.initial_config import Configuration
Configuration(True)
from src.endpoints import app


class ContaTestCases(unittest.TestCase):

    def setUp(self) -> None:
        self.app_client = app.test_client()

    def test_deve_creditar(self):
        response = self.app_client.post('/conta', headers={'Content-Type': 'application/json'},
                                        data=json.dumps({'valor': 1300})
                                        )
        self.assertEqual(200, response.status_code, 'a chamada deve ter dado certo')
        self.assertEqual(1300, response.json['valorInserido'], 'deve ter inserido o valor especificado')

    def test_deve_debitar_caso_saldo_positivo(self):
        response = self.__consultar_saldo()
        self.assertEqual(200, response.status_code, 'deve ter conseguido obter o saldo')
        if response.json['saldo'] - 1234 > 0:
            response = self.app_client.delete('/conta', headers={'Content-Type': 'application/json'},
                                              data=json.dumps({'valor': 1234}))
            self.assertEqual(200, response.status_code, 'o valor da conta deve ter sido subtraido')
            self.assertEqual(1234, response.json['valorInserido'], 'deve ter sido subtraido esse valor')
            response = self.__consultar_saldo()
            self.assertEqual(200, response.status_code, 'deve ter conseguido obter o saldo')
            self.assertEqual(66, response.json['saldo'], 'O valor restante pós operações deve coincidir!')

    def __consultar_saldo(self):
        return self.app_client.get('/conta')


if __name__ == '__main__':
    unittest.main()
