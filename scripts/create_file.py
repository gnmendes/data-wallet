import json
from datetime import datetime
import base64


class CreateFile:
    def __init__(self):
        self.file_name = 'some_text.txt'

    def write_file(self, data):
        with open(self.file_name, 'w+') as file:
            separate_lines = data.split('/n')
            for line in separate_lines:
                file.write(json.dumps(line))
            file.close()


class CrateFileForArchive(CreateFile):

    def write_file(self, data):

        for archive in data:
            archive_name = data[archive].filename.split('.')[0] + '.txt'
            with open(archive_name, 'w+') as file:
                file_info = {
                    'file_name': data[archive].filename,
                    'content_type': data[archive].content_type,
                    'saved_date': str(datetime.utcnow().now())
                }
                try:
                    file_info['file_data'] = base64.b64encode(data[archive].read()).decode('ascii')
                except Exception as e:
                    print(str(e))
                file.write(json.dumps(file_info, sort_keys=True))
            file.close()


class CreateFileFactory:
    __CONTENT_TYPES = {
        'application/json': CreateFile,
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': CrateFileForArchive
    }

    def __init__(self, content_type):
        self.content_type = content_type

    def get_instance(self):
        return self.__CONTENT_TYPES[self.content_type]
