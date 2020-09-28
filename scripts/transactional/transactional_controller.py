from flask import Flask, request
from scripts.common.utilities import CPFValidator as cpf, InputValidator
app = Flask(__name__)


@app.route('introduce_data', method=['POST'])
def create_something():
    assert InputValidator.validate_input(required_parameters=['cpf'], incoming_data=request.get_json())
    cpf.is_cpf_valid(cpf=request.get_json()['cpf'])
    return None
