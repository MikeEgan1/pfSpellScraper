### This is the query builder for elastic search

class Builder(object):
    query = {
        "query" : {}
    }

    def constant_score(self):
        self.query["query"]["constant_score"] = {}
        return self

    def filter(self):
        self.query["query"]["constant_score"]["filter"] = {}
        return self

    def term(self, key, value):
        self.query["query"]["constant_score"]["filter"]["term"] = {
            key : value
        }
        return self

    def build(self):
        return self.query