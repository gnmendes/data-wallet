from .blockchain.blockchain import Blockchain
from .common.utilities import InputValidator
from uuid import uuid4
from flask import Flask, request

app = Flask(__name__)
bc = Blockchain()


def _is_valid(required, data):
    return InputValidator.validate_input(required_parameters=required, incoming_data=data)


@app.route('/mine', methods=['GET'])
def mine():
    pass


@app.route('/transactions/new', methods=['POST'])
def new_transactions():
    register = request.get_json()
    if _is_valid(required=['sender', 'recipient', 'data'], data=register) and _is_valid(data=register['data'],
                                                                                        required=['cpf']):
        pass


@app.route('/chain', methods=['GET'])
def obtain_the_whole_chain():
    pass


#TODO: TRAZER TODOS OS ENDPOINTS PRA ESSE ARQUIVO