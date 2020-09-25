import os
import os.path
import json
import base64
from datetime import datetime
from scripts.common.utilities import InputValidator, Util


# TODO: ver como poe senha nos arquivos
# TODO: ver como faz para tornar isso daqui em executavel

class DirectoryOperations:

    @staticmethod
    def dir_exists(path, create_if_doesnt=None):
        if not create_if_doesnt:
            return os.path.exists(path)
        else:
            return True if os.path.exists(path) else DirectoryOperations.create_dir(path=path)

    @staticmethod
    def create_dir(path):
        return os.makedirs(path, exist_ok=True)


class FileOperations:
    """
        Classe responsável por comportar as operações básicas de arquivos/diretórios
    """

    def __init__(self):
        self.files_dir = 'files'
        self.search_for = None

    def get_files_list(self):
        path = f'{os.getcwd()}/{self.files_dir}'
        if DirectoryOperations.dir_exists(path=path):
            return {'files_founded': os.listdir(path)}
        return {'error': 'Não existem arquivos a serem listados!'}

    def get_single_file(self, filename):
        file_paths = self.__files_pathfinder(filename=filename)
        if file_paths:
            file_contents = []
            for file_path in file_paths:
                with open(file_path, 'r') as file:
                    file_contents.append(json.loads(file.read()))
                    file.close()
            print(file_contents)
            return {'files_founded': file_contents}
        return {'error': 'Não foi encotrada nenhuma ocorrência para o nome de arquivo informado!'}

    def __files_pathfinder(self, filename):

        paths = []
        for root, dirs, files in os.walk('./{}'.format(self.files_dir)):
            for name in files:
                if Util.anything_after_matches(search_for=filename, name=name):
                    paths.append(os.path.abspath(os.path.join(root, name)))
        return paths


class CreateFileForJSON:
    """
        Classe responsável por salvar os em arquivos o body recebido nas requsições
        cujo o tipo do conteúdo é JSON
    """

    def __init__(self):
        self.files_dir = 'files'
        self.sub_dir = 'json_storage'
        self.file_name = 'stored_json_data.txt'
        self.required_fields = ['data', 'author']

    def write_file(self, data):
        DirectoryOperations.dir_exists(path='{}/{}/{}'.format(os.getcwd(), self.files_dir, self.sub_dir),
                                       create_if_doesnt=True)
        incoming_data = data.get_json()
        if InputValidator.validate_input(required_parameters=self.required_fields, incoming_data=incoming_data):
            with open('{}/{}/{}'.format(self.files_dir, self.sub_dir, self.file_name), 'a') as file:
                file.write(json.dumps(incoming_data))
                file.close()


class CrateFileForArchive(CreateFileForJSON):

    def write_file(self, data):
        received_files = data.files.to_dict(flat=False)['archive']
        for archive in received_files:
            archive_name = archive.filename.split('.')[0] + '.txt'
            DirectoryOperations.dir_exists(path='{}/{}'.format(os.getcwd(), self.files_dir), create_if_doesnt=True)
            file_path = '{}/{}'.format('files', archive_name)

            with open(file_path, 'w+') as file:
                file_info = {
                    'file_name': archive.filename,
                    'content_type': archive.content_type,
                    'saved_date': datetime.utcnow().now().strftime('%d/%m/%y %H:%M:%S')
                }
                try:
                    file_info['file_data'] = base64.b64encode(archive.read()).decode('utf-8')
                except Exception as e:
                    print(str(e))
                file.write(json.dumps(file_info))
            file.close()


class CreateFileFactory:

    @staticmethod
    def get_instance(content_type):
        dummy_content_type = content_type if content_type == 'application/json' else 'other'
        __CONTENT_TYPES = {
            'application/json': CreateFileForJSON,
            'other': CrateFileForArchive
        }
        return __CONTENT_TYPES[dummy_content_type]()
