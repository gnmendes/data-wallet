import os
import json
import base64
from datetime import datetime
from scripts.util.utilities import InputValidator


class FileOperations:

    def __init__(self):
        self.files_dir = 'files'

    def get_files_list(self):
        return os.listdir('./{}'.format(self.files_dir))


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
            with open('{}/{}'.format(self.files_dir, archive_name), 'w+') as file:
                file_info = {
                    'file_name': received_files[archive].filename,
                    'content_type': received_files[archive].content_type,
                    'saved_date': datetime.utcnow().now().strftime('%d/%m/%y %H:%M:S')
                }
                try:
                    file_info['file_data'] = base64.b64encode(received_files[archive].read()).decode('ascii')
                except Exception as e:
                    print(str(e))
                file.write(json.dumps(file_info))
            file.close()


class CreateFileFactory:

    @staticmethod
    def get_instance(content_type):
        dummy_content_type = content_type if content_type else 'other'
        __CONTENT_TYPES = {
            'application/json': CreateFile,
            'other': CrateFileForArchive
        }
        return __CONTENT_TYPES[dummy_content_type]()
