from ConnectionManager import ConnectionManager
import domain_tables.classes

from domain_tables.descriptors import descriptors
from domain_tables.schools import schools
from domain_tables.subschools import subschools

def main():
  cm = ConnectionManager()
  connection = cm.get_connection()
  # create_classes(connection)
  insert_rows(connection,"descriptors", descriptors, "descriptor")
  insert_rows(connection,"schools", schools, "school")
  insert_rows(connection,"subschools", subschools, "subschool")

def insert_rows(connection, table_name, rows, data_field):
    cursor = connection.cursor()

    for i in xrange(len(rows)):
        sql = """insert into {table_name} ({data_field}) values ('{row}');""".format(table_name=table_name, data_field=data_field, row=rows[i])
        cursor.execute(sql)

def update_table(rows):
    pass

def create_classes(connection):
    insert_rows(connection, "classes", domain_tables.classes.classes)

if __name__ == "__main__":
     main()
