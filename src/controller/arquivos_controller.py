from flask import request, jsonify
from flask_cors import cross_origin

from src.common.utilities import Util
from src.controller import app
from src.non_transactional.non_transact_ops import FileOps

arch_ops = FileOps()


@app.route('/arquivos', methods=['POST'])
@cross_origin()
def receive_file():
    rows_inserted = arch_ops.insert_new_files(files=request)
    return jsonify(rows_inserted), Util.get_status(body=rows_inserted, status_when_ok=201)


@app.route('/arquivos', methods=['GET'])
@cross_origin()
def list_files():
    archive = arch_ops.get_files()
    return jsonify(archive), Util.get_status(body=archive)


@app.route('/arquivos/<id_archive>', methods=['DELETE'])
@cross_origin()
def remove_archive(id_archive):
    body = arch_ops.remove_files(id=id_archive)
    return jsonify(body), Util.get_status(body=body)
