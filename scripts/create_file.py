import json
from datetime import datetime
import base64


class InputValidator:
    @staticmethod
    def validate_input(required_parameters, incoming_data):
        for param in required_parameters:
            if param not in incoming_data:
                return False
        return True


class CreateFile:
    def __init__(self):
        self.file_name = 'some_text.txt'
        self.required_fields = ['data', 'author']

    def write_file(self, data):
        incoming_data = data.get_json()
        if InputValidator.validate_input(required_parameters=self.required_fields, incoming_data=incoming_data):
            with open(self.file_name, 'w+') as file:
                file.write(json.dumps(incoming_data))
                file.close()


class CrateFileForArchive(CreateFile):

    def write_file(self, data):
        receveid_files = data.files
        for archive in receveid_files:
            archive_name = receveid_files[archive].filename.split('.')[0] + '.txt'
            with open(archive_name, 'w+') as file:
                file_info = {
                    'file_name': receveid_files[archive].filename,
                    'content_type': receveid_files[archive].content_type,
                    'saved_date': datetime.utcnow().now().strftime('%d/%m/%y %H:%M:S')
                }
                try:
                    file_info['file_data'] = base64.b64encode(receveid_files[archive].read()).decode('ascii')
                except Exception as e:
                    print(str(e))
                file.write(json.dumps(file_info))
            file.close()


class CreateFileFactory:

    @staticmethod
    def get_instance(content_type='other'):
        __CONTENT_TYPES = {
            'application/json': CreateFile,
            'other': CrateFileForArchive
        }
        return __CONTENT_TYPES[content_type]()
