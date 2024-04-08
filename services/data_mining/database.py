from elasticsearch import Elasticsearch


class Database:
    def __init__(self):
        self.es = Elasticsearch()

    def read(self, query):
        return self.es.search(body=query)

    def write(self, table, data):
        for record in data:
            self.es.index(index=table, body=record)
