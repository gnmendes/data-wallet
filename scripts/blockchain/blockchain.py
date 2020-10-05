import json
import random
from time import time
from hashlib import sha256


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


class Transaction:

    def __init__(self, sender, recipient, data):
        self.sender = sender
        self.recipient = recipient
        self.data = data


class Blockchain:

    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.add_new_block(proof=100, previous_hash=1)

    def add_new_block(self, proof, previous_hash=None):
        block = Block(index=len(self.chain) + 1,
                      timestamp=time(),
                      transactions=self.current_transactions,
                      proof=proof,
                      previous_hash=previous_hash or sha256('FIRST HASH'.encode()).hexdigest())
        self.__clear_transactions()
        self.chain.append(block)
        return block

    def __clear_transactions(self):
        self.current_transactions = []

    def add_new_transaction(self, sender, recipient, data):
        self.current_transactions.append(
            Transaction(sender=sender,
                        recipient=recipient,
                        data=data))
        return self.get_last_block['index'] + 1

    def proof_of_work(self, last_proof):
        proof = 0
        while not self.valid_proof(last_proof=last_proof, proof=proof):
            proof = random.randint(1, 9999999)
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess_hash = '%d%d' % last_proof, proof
        return sha256(guess_hash).hexdigest()[:-1] == '00'

    @property
    def get_last_block(self):
        return self.chain[-1]
