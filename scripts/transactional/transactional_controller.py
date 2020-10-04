from flask import Flask, request, jsonify
from ..common.utilities import CPFValidator, InputValidator
from .data_handler import TransactionalData

app = Flask(__name__)

'''
    Era o endpoint para receber dados e adicionar registros a blockchain
'''
@app.route('introduce_data', method=['POST'])
def create_something():
    body = request.get_json()
    InputValidator.validate_input(required_parameters=['cpf'], incoming_data=request.get_json())
    CPFValidator.is_cpf_valid(cpf=body['cpf'])
    # transact = TransactionalData()

    return None


@app.route('/define_required_ones', method=['POST'])
def define_required_field():
    transact = TransactionalData()
    transact.register_required_fields(fields=request.get_json())

    return jsonify('If everything gone right and nothings gone wrong, so it worked'), 201
