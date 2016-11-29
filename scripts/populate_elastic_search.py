import MySQLdb
from elasticsearch import Elasticsearch
from ConnectionManager import ConnectionManager
import json

def get_spells():
    cm = ConnectionManager()
    es = Elasticsearch()
    sql = """
    SELECT
      s.id,
      s.name,
      s.description,
      s.action,
      s.components,
      s.`range`,
      s.effect,
      s.duration,
      s.saving_throw,
      s.spell_resistance,
      s.source_book,
      sch.school,
      sub.subschool,
      group_concat(c.class) as class,
      group_concat(sbc.spell_level) as spell_level
    FROM spells s
      INNER JOIN spells_by_class sbc ON sbc.spell_id = s.id
      inner join classes c on sbc.class_id = c.id
      inner join schools sch on sch.id = s.school_id
      left join subschools sub on s.subschool_id = sub.id
    GROUP BY s.id;
    """
    connection = cm.get_connection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute(sql)
    resultSet = cursor.fetchall()

    for row in resultSet:
        row["class_levels"] = dict(zip(row["class"].split(","),row["spell_level"].split(",")))
        row["components"] = row["components"].decode('string_escape')
        del(row["class"])
        del(row["spell_level"])

        es.index(index="pfspells", doc_type='spell', id=row["id"], body=row)

def main():
    get_spells()
    # es = Elasticsearch()
    # res = es.index(index="pfspells", doc_type='spell', body={})

if __name__ == "__main__":
    main()