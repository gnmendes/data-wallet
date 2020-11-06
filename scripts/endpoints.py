from uuid import uuid4
from flask import Flask, request, jsonify
from flask_cors import cross_origin

from scripts.blockchain.blockchain import Blockchain
from scripts.non_transactional.non_transact_ops import FileOps
from scripts.transactional.transact_ops import TransactionalOps
from scripts.common.utilities import InputValidator, CPFValidator

app = Flask(__name__)
bc = Blockchain()
arch_ops = FileOps()
node_identifier = str(uuid4()).replace('-', '.')


def _is_valid(required, data):
    return InputValidator.validate_input(required_parameters=required, incoming_data=data)


def get_status(body, status_when_ok=200):
    return body['error'] if 'error' in body else status_when_ok


@app.route('/conta', methods=['POST'])
def creditar():
    valor = request.get_json()['valor']
    return jsonify(TransactionalOps.creditar_ou_debitar_valor(valor=valor, op='C')), 200


@app.route('/conta', methods=['DELETE'])
def debitar():
    valor = request.get_json()['valor']
    saldo = TransactionalOps.consultar_saldo()['saldo']

    if valor and saldo and saldo - float(valor) > 0:
        return jsonify(TransactionalOps.creditar_ou_debitar_valor(valor=valor, op='D')), 200
    return jsonify({'error': 'O débito negativaria a conta, por isso não foi possível completar '
                             'a operação!'}), 400


@app.route('/conta', methods=['GET'])
def consultar():
    return jsonify(TransactionalOps.consultar_saldo()), 200


@app.route('/chain/mine', methods=['GET'])
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


''' DADOS TRANSACIONAVEIS '''


@app.route('/chain', methods=['POST'])
def new_transactions():
    register = request.get_json()
    response = {'message': 'Não foi possível identificar todos os atributos obrigatórios!'}

    if _is_valid(required=['sender', 'recipient', 'data'], data=register) \
            and _is_valid(data=register['data'], required=['cpf']):

        if CPFValidator.is_cpf_valid(cpf=register['data']['cpf']):
            index = bc.add_new_transaction(sender=register['sender'], recipient=register['recipient'],
                                           data=register['data'])
            response = {'message': f'Transação não confirmada adicionada! índice {index}'}
            return jsonify(response), 201
    return jsonify(response), 400


@app.route('/chain', methods=['GET'])
def obtain_the_whole_chain():
    response = {'chain': bc.__repr__(), 'length': len(bc.chain)}
    return jsonify(response), 200


''' DADOS NÃO TRANSACIONAVEIS '''


@app.route('/arquivos', methods=['POST'])
@cross_origin()
def receive_info():
    rows_inserted = arch_ops.insert_new_files(files=request)
    return jsonify(rows_inserted), get_status(body=rows_inserted, status_when_ok=201)


@app.route('/arquivos', methods=['GET'])
def list_files():
    archive = arch_ops.get_files()
    return jsonify(archive), get_status(body=archive)


@app.route('/arquivos/<id_archive>')
def retrieve_file(id_archive):
    result = arch_ops.get_file_by_id(id_file=id_archive)
    return jsonify(result), get_status(body=result)


@app.route('/arquivos', methods=['DELETE'])
def remove_archive():
    ids = request.get_json()['ids']
    if ids:
        body = arch_ops.remove_files(ids=ids)
        return jsonify(body), get_status(body=body)
    return jsonify({'error': 'Solicitação de exclusão não inclui ids'}), 400


if __name__ == '__main__':
    app.run(debug=True, port=8080)
