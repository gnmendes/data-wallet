from flask import Flask, request
from scripts.create_file import CreateFileFactory

app = Flask(__name__)


@app.route('/receive_info', methods=['POST'])
def receive_info():
    create_file = CreateFileFactory.get_instance(content_type=request.content_type)
    create_file.write_file(data=request)
    return 'Hit the endpoint', 200


"""
Configurações para rodar local, sendo passiveis de serem omitidas
"""

if __name__ == '__main__':
    app.run(debug=True, port=8080)
