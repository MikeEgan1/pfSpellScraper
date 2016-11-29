from ConnectionManager import ConnectionManager
from elasticsearch import Elasticsearch
from elastic_search.queries.Builder import Builder


class Models(object):
    def __init__(self):
        self.cm = ConnectionManager()
        self.es = Elasticsearch()
        self.builder = Builder()
        self.connection = self.cm.get_connection()

    def save_to_mysql(self, sql):
        cursor = self.connection.cursor()
        cursor.execute(sql)
        return cursor

    def save_to_elastic_search(self, index, doc_type, body):
        self.es.index(index=index, doc_type=doc_type, body=body)

    def get_from_es(self, index, doc_type, body):
        return self.es.search(index=index, doc_type=doc_type, body=body)

    def get_exact_from_es(self, field, term):
        return self.builder.constant_score().filter().term(field, term).build()
