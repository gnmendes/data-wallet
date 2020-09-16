from flask import Flask, request
from scripts.create_file import CreateFileFactory, FileOperations

app = Flask(__name__)
file_ops = FileOperations()


@app.route('/receive_info', methods=['POST'])
def receive_info():
    create_file = CreateFileFactory.get_instance(content_type=request.content_type)
    create_file.write_file(data=request)
    return 'If everything had gone right and nothing gone wrong, this worked!', 200


@app.route('/list_files', method=['GET'])
def list_files():
    return file_ops.get_files_list(), 200


@app.route('/get_file', methods=['GET'])
def retrieve_file():
    return file_ops.get_file(filename=request.args.get('filename'))


"""
Configurações para rodar local, sendo passiveis de serem omitidas
"""

if __name__ == '__main__':
    app.run(debug=True, port=8080)
