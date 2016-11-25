import MySQLdb


class ConnectionManager(object):
    def __init__(self):
        pass

    @staticmethod
    def get_connection():
        connection = MySQLdb.connect(host="127.0.0.1",
                                     user="pfSpell",
                                     passwd="scrapethatspell",
                                     db="pfSpells")

        connection.autocommit(True)
        return connection
