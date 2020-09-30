from pymongo import MongoClient
from enum import Enum


class MongoDBEnum(Enum):
    DATABASE_NAME = 'data-wallet'


class MongoStarter:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.database = self.__handle_database()

    def __handle_database(self):
        return self.client[MongoDBEnum.DATABASE_NAME.name]


class MongoDBOperations:

    def __init__(self):
        self.db = MongoStarter().database

    def create_collection(self, collection_name):
        assert collection_name
        return self.db[collection_name]

    @staticmethod
    def insert_document_at_collection(doc, collection):
        return collection.insert_one(doc)

    def collections_exists(self, collection_name):
        assert collection_name
        return self.db.get_collection(name=collection_name)

    @staticmethod
    def find_one(collection_name):
        assert collection_name
        return collection_name.find_one()

    @staticmethod
    def update_one(collection_name, query, newer_doc):
        assert collection_name, query
        return collection_name.update_one(query, newer_doc)
