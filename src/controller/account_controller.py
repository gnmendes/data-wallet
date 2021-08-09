from flask import jsonify, request
from flask_cors import cross_origin

from src.controller import app
from src.transactional.transact_ops import TransactionalOps


@app.route('/account', methods=['POST'])
@cross_origin()
def receive_money():
    valor = request.get_json()['valor']
    return jsonify(TransactionalOps.creditar_ou_debitar_valor(valor=valor, op='C')), 200


@app.route('/account', methods=['DELETE'])
@cross_origin()
def pay_bills():
    valor = request.get_json()['valor']
    return jsonify(TransactionalOps.creditar_ou_debitar_valor(valor=valor, op='D')), 200


@app.route('/account', methods=['GET'])
@cross_origin()
def check_balance():
    return jsonify(TransactionalOps.consultar_saldo()), 200
