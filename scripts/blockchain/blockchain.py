import json
from hashlib import sha256
from time import time


class Block:

    def __init__(self, index, timestamp, transactions, proof, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.proof = proof
        self.previous_hash = previous_hash

    @property
    def get_hash(self):
        repr_encoded = json.dumps(self.__dict__, sort_keys=True).encode()
        return sha256(repr_encoded)


class Blockchain:

    def __init__(self):
        self.chain = []
        self.current_transactions = []

    def add_new_block(self, proof, previous_hash=None):
        block = Block(index=len(self.chain) + 1,
                      timestamp=time(),
                      transactions=self.current_transactions,
                      proof=proof,
                      previous_hash=previous_hash or self.chain[-1].get_hash)
