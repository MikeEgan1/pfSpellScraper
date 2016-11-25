from ConnectionManager import ConnectionManager
from resources import *

def main():
  cm = ConnectionManager()
  connection = cm.get_connection()

def table_exists(connection, table_name):
    sql = "SELECT * FROM information_schema.TABLES where TABLE_NAME = {}".format(table_name)
    cursor = connection.cursor()
    print cursor.execute(sql)

def create_table(connection, table_name):
    pass

def insert_rows(rows):
    pass

def update_table(rows):
    pass

if __name__ == "__main__"():
     main()
