from uuid import uuid4
from flask import Flask, request, jsonify
from scripts.blockchain.blockchain import Blockchain
from scripts.common.utilities import InputValidator, CPFValidator
from scripts.non_transactional.archive_operations import CreateFileFactory, FileOperations

app = Flask(__name__)
bc = Blockchain()
file_ops = FileOperations()
node_identifier = str(uuid4()).replace('-', '.')


def _is_valid(required, data):
    return InputValidator.validate_input(required_parameters=required, incoming_data=data)


# PASSO 2:
@app.route('/mine', methods=['GET'])
def mine():
    last_block = bc.get_last_block
    last_proof = last_block.proof
    proof_mined = bc.proof_of_work(last_proof=last_proof)
    bc.add_new_transaction(sender='0', recipient=node_identifier,
                           data={'success': 'You mined a new proof and for this'
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


# PASSO 1:
@app.route('/transactions/new', methods=['POST'])
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


@app.route('/insert_document', methods=['POST'])
def receive_info():
    create_file = CreateFileFactory.get_instance(content_type=request.content_type)
    create_file.write_file(data=request)
    return jsonify('If everything had gone right and nothing gone wrong, this worked!'), 201


@app.route('/list_documents')
def list_files():
    return jsonify(file_ops.get_files_list()), 200


@app.route('/<file_name>')
def retrieve_file(file_name):
    return jsonify(file_ops.get_single_file(filename=file_name)), 200


"""
Configurações para rodar local, sendo passiveis de serem omitidas

**Non transactional values are inputted through those endpoints**
"""

if __name__ == '__main__':
    app.run(debug=True, port=8080)

