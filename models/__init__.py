from ConnectionManager import ConnectionManager
from elasticsearch import Elasticsearch
from elastic_search.queries.Builder import Builder

class Models(object):
    def __init__(self):
        self.cm = ConnectionManager()
        self.es = Elasticsearch()
        self.builder = Builder()

    def save_to_mysql(self, sql):
        connection = self.cm.get_connection()
        cursor = connection.cursor()
        cursor.execute(sql)

    def save_to_elastic_search(self, index, doc_type, body):
        self.es.index(index=index, doc_type=doc_type, body=body)

    def get_from_es(self, index, doc_type, body):
        return self.es.search(index=index, doc_type=doc_type, body=body)

    def get_exact_from_es(self, field, term):
        return self.builder.constant_score().filter().term(field, term).build()