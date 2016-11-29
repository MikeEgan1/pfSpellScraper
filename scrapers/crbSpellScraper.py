from bs4 import BeautifulSoup
import urllib2

from SpellParser import SpellParser
from models.spell import Spell

BASE_URL = "http://paizo.com/pathfinderRPG/prd/coreRulebook/"

def main():
    parse_all_spells(SpellParser())

def parse_all_spells(parser):
    spell_model = Spell()
    spell_list_url = "spellLists.html"
    content = urllib2.urlopen(BASE_URL + spell_list_url)
    soup = BeautifulSoup(content.read(), "html.parser")
    for x in soup.find_all('p'):
        for y in x.find_all('b'):
            links = y.find_all('a')
            if len(links) > 0:
                spell = links[0]
                parsed_spell = parser.parse_spell(BASE_URL + "" + spell.get('href'), spell.text, "crb")
                spell_model.save(parsed_spell)

if __name__ == "__main__":
    main()
