import os
import os.path
import json
import base64
from datetime import datetime
from scripts.util.utilities import InputValidator


class FileOperations:

    def __init__(self):
        self.files_dir = 'files'

    def get_files_list(self):
        return {'files_founded': os.listdir('./{}'.format(self.files_dir))}

    def get_file(self, filename):
        file_path = self.__files_pathfinder(filename=filename)
        if file_path:
            with open(file_path, 'r') as file:
                content_file = {
                    'content': json.loads(file.read())
                }
                print(content_file)
                file.close()
                return content_file
        return {'error': 'Não foi encotrada nenhuma ocorrência para o nome de arquivo informado!'}

    def __files_pathfinder(self, filename):
        for root, dirs, files in os.walk('./{}'.format(self.files_dir)):
            for name in files:
                if name == filename:
                    return os.path.abspath(os.path.join(root, name))
        return None

    @staticmethod
    def dir_exists(path, create_if_doesnt):
        if not create_if_doesnt:
            return os.path.exists(path)
        else:
            return True if os.path.exists(path) else FileOperations.create_dir(path=path)

    @staticmethod
    def create_dir(path):
        return os.makedirs(path, exist_ok=True)


class CreateFile(FileOperations):
    def __init__(self):
        super().__init__()
        self.file_name = 'some_text.txt'
        self.required_fields = ['data', 'author']

    def write_file(self, data):
        incoming_data = data.get_json()
        if InputValidator.validate_input(required_parameters=self.required_fields, incoming_data=incoming_data):
            with open('{}/{}'.format(self.files_dir, self.file_name), 'w+') as file:
                file.write(json.dumps(incoming_data))
                file.close()


class CrateFileForArchive(CreateFile):

    def write_file(self, data):
        received_files = data.files
        for archive in received_files:
            archive_name = received_files[archive].filename.split('.')[0] + '.txt'
            FileOperations.dir_exists(path='{}/{}'.format(os.getcwd(), 'files'), create_if_doesnt=True)
            file_path = '{}/{}'.format('files', archive_name)

            with open(file_path, 'w+') as file:
                file_info = {
                    'file_name': received_files[archive].filename,
                    'content_type': received_files[archive].content_type,
                    'saved_date': datetime.utcnow().now().strftime('%d/%m/%y %H:%M:S')
                }
                try:
                    file_info['file_data'] = base64.b64encode(received_files[archive].read()).decode('utf-8')
                except Exception as e:
                    print(str(e))
                file.write(json.dumps(file_info))
            file.close()


class CreateFileFactory:

    @staticmethod
    def get_instance(content_type):
        dummy_content_type = content_type if content_type == 'application/json' else 'other'
        __CONTENT_TYPES = {
            'application/json': CreateFile,
            'other': CrateFileForArchive
        }
        return __CONTENT_TYPES[dummy_content_type]()
