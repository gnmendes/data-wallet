from uuid import uuid4
from flask import Flask, request, jsonify
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


@app.route('/conta/creditar', methods=['POST'])
def creditar():
    valor = request.get_json()['valor']
    return jsonify(TransactionalOps.creditar_ou_debitar_valor(valor=valor, op='C')), 200


@app.route('/conta/debitar', methods=['DELETE'])
def debitar():
    valor = request.get_json()['valor']
    saldo = TransactionalOps.consultar_saldo()['saldo']

    if valor and saldo and saldo - float(valor) > 0:
        return jsonify(TransactionalOps.creditar_ou_debitar_valor(valor=valor, op='D')), 200
    return jsonify({'error': 'O débito negativaria a conta, por isso não foi possível completar '
                             'a operação!'}), 400


@app.route('/conta/saldo', methods=['GET'])
def consultar():
    return jsonify(TransactionalOps.consultar_saldo())


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


'''
    Submeter um registro não implica, necessariamente em ele ser valido:
    Basicamente, ele só é somado a cadeia de transações não confirmadas - quando há a mineração
    é gerado então um bloco e esse sim é adicionado a cadeia
'''


@app.route('/chain/transactions/new', methods=['POST'])
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


@app.route('/chain/representation', methods=['GET'])
def obtain_the_whole_chain():
    response = {'chain': bc.__repr__(), 'length': len(bc.chain)}
    return jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    nodes = request.get_json()['nodes']

    if not nodes:
        return 'Nenhum nó submetido!'

    for node in nodes:
        bc.register_nodes(node)

    response = {
        'mensagem': 'Sucesso! Novos nós foram registrados',
        'nodes': bc.nodes
    }

    return jsonify(response), 201


@app.route('/nodes/resolve')
def consensus():
    replaced = bc.resolve_conflicts()
    response = {'message': 'Our chain is authoritative',
                'chain': bc.__repr__()}
    if replaced:
        response['message'] = 'Our chain was replaced'
    return jsonify(response), 200


'''
Daqui pra baixo são endpoints relacionados aos dados não transacionaveis
'''


@app.route('/arquivo/inserir', methods=['POST'])
def receive_info():
    rows_inserted = arch_ops.insert_new_files(files=request)
    status = rows_inserted['error'] if 'error' in rows_inserted else 201
    return jsonify(rows_inserted), status


@app.route('/arquivo/listar')
def list_files():
    archive = arch_ops.get_files()
    status = archive['error'] if 'error' in archive else 200
    return jsonify(archive), status


@app.route('/arquivo/<id_archive>')
def retrieve_file(id_archive):
    result = arch_ops.get_file_by_id(id_file=id_archive)
    status = result['error'] if 'error' in result else 200
    return jsonify(result), status


"""
Configurações para rodar local, sendo passiveis de serem omitidas

**Non transactional values are inputted through those endpoints**
"""

if __name__ == '__main__':
    app.run(debug=True, port=8080)
