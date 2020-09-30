from flask import Flask, request

from scripts.common.utilities import CPFValidator, InputValidator
from .something import TransactionalData

app = Flask(__name__)


@app.route('introduce_data', method=['POST'])
def create_something():
    body = request.get_json()
    InputValidator.validate_input(required_parameters=['cpf'], incoming_data=request.get_json())
    CPFValidator.is_cpf_valid(cpf=body['cpf'])
    # bc = BlockChain()

    return None


@app.route('/define_required_ones', method=['POST'])
def define_required_field():
    transact = TransactionalData()
    transact.register_required_fields(fields=request.get_json())

    return 'If everything gone right and nothings gone wrong, so it worked', 201
