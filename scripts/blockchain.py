import json
from hashlib import sha256 as encryptor


class Block:

    def __init__(self, data, index, timestamp, previous_hash):
        self.data = data
        # self.transactions = transactions
        self.index = index
        self.timestamp = timestamp
        self.previous_hash = previous_hash

    def generate_hash(self, block):
        if not block:
            raise Exception('Náo se criptografa algo vazio!')

        __json_repr = self.__repr__().encode()
        return encryptor(__json_repr).hexdigest()
    """"
    Sobreescrevendo o método para obter uma representação da
    classe customizada (com as chaves ordenadas)
    """
    def __repr__(self):
        return json.dumps(self.__dict__, sort_keys=True)

