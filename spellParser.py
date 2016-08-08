from bs4 import BeautifulSoup
import re
import urllib2
from Spell import Spell

class spellParser(object):
    def __init__(self):
        pass

    def parse_spell(self, url, spell_name):
        content = urllib2.urlopen(url)
        soup = BeautifulSoup(content.read(), "html.parser")
        spell = self.scrape_spell_page(soup)
        spell.name = spell_name

        return spell

    def scrape_spell_page(self, soup):
        spell = Spell()
        body = soup.find_all('body')
        paragraphs = body[0].find_all('p')

        for paragraph in paragraphs:
            if paragraph.attrs.get("class") != None and paragraph.attrs.get("class")[0] == "stat-block-title":
                continue
            elif "School" in paragraph.text:
                spell.school, spell.levels, spell.subschool = parse_school_and_levels(paragraph)
            elif "Casting Time" in paragraph.text:
                spell.action = parse_action(paragraph)
            elif "Component" in paragraph.text:
                spell.components = parse_components(paragraph)
            elif "Range" in paragraph.text:
                spell.range = parse_range(paragraph)
            elif "Effect" in paragraph.text:
                spell.effect = parse_effect(paragraph)
            elif "Duration" in paragraph.text:
                spell.duration = parse_duration(paragraph)
            elif "Saving Throw" in paragraph.text:
                spell.saving_throw, spell.spell_resistance = parse_saving_throw(paragraph)
            elif "Report a Problem" in paragraph.text:
                continue
            else:
                # print paragraph.text
                if spell.description == None:
                    spell.description = paragraph.text
                else:
                    spell.description = spell.description + " " + paragraph.text

        return spell



