from flask import jsonify, request
from flask_cors import cross_origin

from src.blockchain.blockchain import Blockchain
from uuid import uuid4

from src.common.utilities import Util, CPFValidator
from src.controller import app

bc = Blockchain()
node_identifier = str(uuid4()).replace('-', '.')

""" DADOS TRANSACIONAVEIS """


@app.route('/chain/mine', methods=['GET'])
@cross_origin()
def mine():
    last_block = bc.get_last_block
    last_proof = last_block.proof
    proof_mined = bc.proof_of_work(last_proof=last_proof)
    bc.add_new_transaction(sender='0', recipient=node_identifier,
                           data={'success': 'You mined a new proof and for this '
                                            'your registry are being adding to the chain!'})
    previous_hash = last_block.get_hash
    block = bc.add_new_block(proof=proof_mined, previous_hash=previous_hash)
    response = {
        'message': 'New block forged!',
        'index': block.index,
        'transactions': block.transactions,
        'proof': block.proof,
        'previousHash': str(block.previous_hash)
    }

    return jsonify(response), 200


@app.route('/chain', methods=['POST'])
@cross_origin()
def new_transactions():
    register = request.get_json()
    response = {'message': 'Não foi possível identificar todos os atributos obrigatórios!'}

    if Util.is_valid(required=['sender', 'recipient', 'data'], data=register) and \
            CPFValidator.is_cpf_valid(cpf=register['sender']) and CPFValidator.is_cpf_valid(cpf=register['recipient']):

        valor = register['valor'] if 'valor' in register else None
        index = bc.add_new_transaction(sender=register['sender'], recipient=register['recipient'],
                                       data=register['data'], valor=valor)
        response = {'message': f'Transação não confirmada adicionada! índice {index}'}
        return jsonify(response), 201
    return jsonify(response), 400


@app.route('/chain', methods=['GET'])
@cross_origin()
def obtain_the_whole_chain():
    response = {'chain': bc.__repr__(), 'length': len(bc.chain)}
    return jsonify(response), 200
