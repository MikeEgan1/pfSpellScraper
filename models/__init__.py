from ConnectionManager import ConnectionManager
from elasticsearch import Elasticsearch

class Models(object):
    def __init__(self):
        self.cm = ConnectionManager()
        self.es = Elasticsearch()

    def save_to_mysql(self, sql):
        connection = self.cm.get_connection()
        cursor = connection.cursor()
        cursor.execute(sql)

    def save_to_elastic_search(self, index, doc_type, body):
        self.es.index(index=index, doc_type=doc_type, body=body)
