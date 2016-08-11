from bs4 import BeautifulSoup
import urllib2

from ConnectionManager import ConnectionManager
from elasticsearch import Elasticsearch
from spellParser import spellParser

from models.spell import Spell
BASE_URL = "http://paizo.com/pathfinderRPG/prd/advancedPlayersGuide/"


def main():
    cm = ConnectionManager()

    parse_all_spells(
            spellParser(),
            cm.get_connection(),
            Elasticsearch()
    )


def parse_all_spells(parser, connection, es_connection):
    spell_model = Spell()
    spell_list_url = "advancedSpellLists.html"
    content = urllib2.urlopen(BASE_URL + spell_list_url)
    soup = BeautifulSoup(content.read(), "html.parser")
    for x in soup.find_all('p'):
        for y in x.find_all('b'):
            links = y.find_all('a')
            if len(links) > 0:
                spell = links[0]
                parsed_spell = parser.parse_spell("http://paizo.com" + "" + spell.get('href'), spell.text, "apg");
                print parsed_spell.name
                spell_model.save(parsed_spell)

if __name__ == "__main__":
    main()
