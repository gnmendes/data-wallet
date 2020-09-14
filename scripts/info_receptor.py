from flask import Flask, request
from scripts.create_file import CreateFileFactory

app = Flask(__name__)


class InputValidator:
    @staticmethod
    def validate_input(required_parameters, incoming_data):
        for param in required_parameters:
            if param not in incoming_data:
                return False
                # raise Exception('Os valores submetidos não são válidos!')
        return True


@app.route('/receive_info', methods=['POST'])
def receive_info():
    create_file = CreateFileFactory('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet').get_instance()
    incoming_data = None
    required_parameters = ['data', 'author']
    if request.content_type == 'application/json':
        incoming_data = request.get_json()
        if InputValidator.validate_input(required_parameters, incoming_data):
            create_file().write_file(data=incoming_data)
    else:
        create_file().write_file(request.files)

    return 'Hit the endpoint', 200

"""
Configurações para rodar local, sendo passiveis de serem omitidas
"""

if __name__ == '__main__':
    app.run(debug=True, port=8080)
