from src.initial_config import Configuration
from src.common.utilities import Util, CPFValidator

from src.transactional.transact_ops import TransactionalOps



Configuration()

''' BANCO FICTÍCIO '''


# @app.route('/conta', methods=['POST'])
# @cross_origin()
# def receive_money():
#     valor = request.get_json()['valor']
#     return jsonify(TransactionalOps.creditar_ou_debitar_valor(valor=valor, op='C')), 200
#
#
# @app.route('/conta', methods=['DELETE'])
# @cross_origin()
# def pay_bills():
#     valor = request.get_json()['valor']
#     return jsonify(TransactionalOps.creditar_ou_debitar_valor(valor=valor, op='D')), 200
#
#
# @app.route('/conta', methods=['GET'])
# @cross_origin()
# def check_balance():
#     return jsonify(TransactionalOps.consultar_saldo()), 200


''' DADOS TRANSACIONAVEIS '''


# @app.route('/chain/mine', methods=['GET'])
# @cross_origin()
# def mine():
#     last_block = bc.get_last_block
#     last_proof = last_block.proof
#     proof_mined = bc.proof_of_work(last_proof=last_proof)
#     bc.add_new_transaction(sender='0', recipient=node_identifier,
#                            data={'success': 'You mined a new proof and for this '
#                                             'your registry are being adding to the chain!'})
#     previous_hash = last_block.get_hash
#     block = bc.add_new_block(proof=proof_mined, previous_hash=previous_hash)
#     response = {
#         'message': 'New block forged!',
#         'index': block.index,
#         'transactions': block.transactions,
#         'proof': block.proof,
#         'previousHash': str(block.previous_hash)
#     }
#
#     return jsonify(response), 200
#
#
# @app.route('/chain', methods=['POST'])
# @cross_origin()
# def new_transactions():
#     register = request.get_json()
#     response = {'message': 'Não foi possível identificar todos os atributos obrigatórios!'}
#
#     if Util.is_valid(required=['sender', 'recipient', 'data'], data=register) and \
#             CPFValidator.is_cpf_valid(cpf=register['sender']) and CPFValidator.is_cpf_valid(cpf=register['recipient']):
#
#         valor = register['valor'] if 'valor' in register else None
#         index = bc.add_new_transaction(sender=register['sender'], recipient=register['recipient'],
#                                        data=register['data'], valor=valor)
#         response = {'message': f'Transação não confirmada adicionada! índice {index}'}
#         return jsonify(response), 201
#     return jsonify(response), 400
#
#
# @app.route('/chain', methods=['GET'])
# @cross_origin()
# def obtain_the_whole_chain():
#     response = {'chain': bc.__repr__(), 'length': len(bc.chain)}
#     return jsonify(response), 200


''' DADOS NÃO TRANSACIONAVEIS '''


# @app.route('/arquivos', methods=['POST'])
# @cross_origin()
# def receive_file():
#     rows_inserted = arch_ops.insert_new_files(files=request)
#     return jsonify(rows_inserted), Util.get_status(body=rows_inserted, status_when_ok=201)
#
#
# @app.route('/arquivos', methods=['GET'])
# @cross_origin()
# def list_files():
#     archive = arch_ops.get_files()
#     return jsonify(archive), Util.get_status(body=archive)
#
#
# @app.route('/arquivos/<id_archive>', methods=['DELETE'])
# @cross_origin()
# def remove_archive(id_archive):
#     body = arch_ops.remove_files(id=id_archive)
#     return jsonify(body), Util.get_status(body=body)

#
# if __name__ == '__main__':
#     app.run(debug=True, port=8080)
