import json
import random
import requests
from time import time
from hashlib import sha256
from urllib.parse import urlparse


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
        self.nodes = set()
        self.add_new_block(proof=100, previous_hash=1)

    def register_nodes(self, address):
        url_parsed = urlparse(address)
        self.nodes.add(url_parsed.netloc)

    def valid_chain(self, chain):
        last_block = chain[0]
        length = len(chain)
        for index in range(1, length):
            block = chain[index]
            if block.previous_hash != last_block.get_hash:
                return False

            if not self.valid_proof(last_proof=last_block['proof'],
                                    proof=block['proof']):
                return False
            last_block = block
        return True

    def resolve_conflicts(self):
        neighbours = self.nodes
        new_chain = None
        max_length = len(self.chain)

        for node in neighbours:
            response = requests.get('http://%s/chain' % node)
            if response.status_code == 200:
                chain, length = response.json()['chain'], response.json()['length']

                if length > max_length and self.valid_chain(chain=chain):
                    max_length = length
                    new_chain = chain
        if new_chain:
            self.chain = new_chain
            return True
        return False

    def add_new_block(self, proof, previous_hash=None):
        block = Block(index=len(self.chain) + 1,
                      timestamp=time(),
                      transactions=self.current_transactions,
                      proof=proof,
                      previous_hash=previous_hash or self.get_last_block.get_hash)
        
        self.__clear_transactions()
        self.chain.append(block)
        return block

    def __clear_transactions(self):
        self.current_transactions = []

    def add_new_transaction(self, sender, recipient, data):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'data': data
        })
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
