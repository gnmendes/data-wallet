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
        return sha256(repr_encoded).hexdigest()


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
                      previous_hash=previous_hash)

        self.__clear_transactions()
        self.chain.append(block)
        return block

    def __clear_transactions(self):
        self.current_transactions = []

    def add_new_transaction(self, sender, recipient, data, valor=None):
        transaction_structure = {
            'sender': sender,
            'recipient': recipient,
            'data': data
        }
        if valor:
            transaction_structure['valor'] = valor

        self.current_transactions.append(transaction_structure)
        return self.get_last_block.index + 1

    def proof_of_work(self, last_proof):
        proof = 0
        while not self.valid_proof(last_proof=last_proof, proof=proof):
            proof = random.randint(1, 9999999)
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        proofs = '%d%d' % (last_proof, proof)
        guess_hash = sha256(proofs.encode()).hexdigest()
        return guess_hash[len(guess_hash)-2:] == '00'

    @property
    def get_last_block(self):
        return self.chain[-1]

    def __repr__(self):
        repr = []
        for block in self.chain:
            repr.append(block.__dict__)
        return repr
