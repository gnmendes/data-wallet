from flask import Flask, request, jsonify
from ..non_transactional.archive_operations import CreateFileFactory, FileOperations

app = Flask(__name__)
file_ops = FileOperations()


@app.route('/receive_info', methods=['POST'])
def receive_info():
    create_file = CreateFileFactory.get_instance(content_type=request.content_type)
    create_file.write_file(data=request)
    return jsonify('If everything had gone right and nothing gone wrong, this worked!'), 201


@app.route('/list_files')
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
