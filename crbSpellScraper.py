from bs4 import BeautifulSoup
import urllib2
import re
import MySQLdb
import ConnectionManager

from elasticsearch import Elasticsearch
from spellParser import spellParser

BASE_URL = "http://paizo.com/pathfinderRPG/prd/coreRulebook/"

def main():
    cm = ConnectionManager()

    parse_all_spells(
        cm.get_connection(),
        spellParser(),
        Elasticsearch()
    )


def parse_all_spells(parser, connection, es_connection):
    spell_list_url = "spellLists.html"
    content = urllib2.urlopen(BASE_URL + spell_list_url)
    soup = BeautifulSoup(content.read(), "html.parser")
    for x in soup.find_all('p'):
        for y in x.find_all('b'):
            links = y.find_all('a')
            if len(links) > 0:
                spell = links[0]
                sp.parse_spell(BASE_URL + "" + spell.get('href'), spell.text, connection, es)


def save_to_mysql(connection, spell):
    cursor = connection.cursor()
    sql = "Insert into spells (spell_data) values ('" + connection.escape_string(spell.json()) + "')"
    cursor.execute(sql)

def save_to_elastic_search(es, spell):
    es.index(index="pfspells", doc_type="spell", body=spell.json())

if __name__ == "__main__":
    main()