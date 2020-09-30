from functools import reduce

from .mongodb_config import MongoDBOperations as MongoOps
from enum import Enum


class TransactEnum(Enum):
    REQUIRED_FIELDS_COLLECTION = 'RequiredFields'


class TransactionalData:

    def __init__(self):
        self.mongo_ops = MongoOps()

    def register_required_fields(self, fields):

        collection = self.mongo_ops.collections_exists(collection_name=TransactEnum.REQUIRED_FIELDS_COLLECTION.name)
        if not collection:
            collection = self.mongo_ops.create_collection(collection_name=TransactEnum.REQUIRED_FIELDS_COLLECTION.name)

        doc = self.mongo_ops.find_one(collection_name=TransactEnum.REQUIRED_FIELDS_COLLECTION.name)
        inserted_id = None
        if doc:
            self.mongo_ops.update_one(collection_name=TransactEnum.REQUIRED_FIELDS_COLLECTION.name,
                                      query=doc, newer_doc={*doc, *fields['required']})
        else:
            inserted_id = self.mongo_ops.insert_document_at_collection(doc=fields, collection=collection)

        if inserted_id:
            with open('./inserted_ones', 'a+') as file:
                file.write('{first_register:%s}' % inserted_id)
                file.close()

#TODO: REFACTOR TOTAL NO NOME DAS CLASSES
#TODO: DEIXAR O PROCESSO MAIS MADURO
#TODO: ADICIONAR BLOCKCHAIN NO MEIO