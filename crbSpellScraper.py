from bs4 import BeautifulSoup
import urllib2
import re
import MySQLdb



from spellParser import spellParser
from Spell import Spell

BASE_URL = "http://paizo.com/pathfinderRPG/prd/coreRulebook/"

classes = [
    'bard',
    'sorcerer',
    'wizard',
    'cleric',
    'druid',
    'paladin',
    'ranger'
]

schools = [
    'evocation',
    'enchantment',
    'divination',
    'illusion',
    'abjuration',
    'necromancy',
    'conjuration',
    'transmutation',
    'universal'
]

subschools = [
    'calling',
    'creation',
    'healing',
    'summoning',
    'teleportation',
    'scrying',
    'charm',
    'compulsion',
    'figment',
    'glamer',
    'pattern',
    'phantasm',
    'shadow',
    'polymorph'
    ''
]

descriptors = [
    'acid',
    'air',
    'chaotic',
    'cold',
    'curse',
    'darkness',
    'death',
    'disease',
    'earth',
    'electricity',
    'emotion',
    'evil',
    'fear',
    'fire',
    'force',
    'good',
    'language-dependant',
    'lawful',
    'light',
    'mind-affecting',
    'pain',
    'poison',
    'ruse',
    'shadow',
    'sonic',
    'water'
]

components = [
    "V",
    "S",
    "F",
    "DF",
    "F/DF",
    "M/DF"
]

def main():
    spell_list_url = "spellLists.html"
    content = urllib2.urlopen(BASE_URL + spell_list_url)
    soup = BeautifulSoup(content.read(), "html.parser")
    connection = get_connection()
    for x in soup.find_all('p'):
        for y in x.find_all('b'):
            links = y.find_all('a')
            if len(links) > 0:
                spell = links[0]
                parse_spell(spell.get('href'), spell.text, connection)

def get_connection():
    return MySQLdb.connect(host="localhost",
                         user="pfSpell",
                         passwd="scrapethatspell",
                         db="pfSpells")

def parse_spell(url, spell_name, connection):
    content = urllib2.urlopen(BASE_URL + url)
    soup = BeautifulSoup(content.read(), "html.parser")
    spell = scrape_spell_page(soup)
    spell.name = spell_name
    cursor = connection.cursor()
    cursor.execute("Insert into spells values ({})".format(spell.json()))

def scrape_spell_page(soup):
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

    print spell.subschool
    return spell

def parse_action(paragraph):
    return paragraph.text.replace("Casting Time", "")

def parse_range(paragraph):
    return paragraph.text.replace("Range", "")

def parse_effect(paragraph):
    return paragraph.text.replace("Effect", "")

def parse_duration(paragraph):
    return paragraph.text.replace("Duration", "")

def parse_saving_throw(paragraph):
    saving_throw_and_resistance = paragraph.text.split(";")
    if len(saving_throw_and_resistance) > 1:
        return saving_throw_and_resistance[0].replace("Saving Throw", ""), saving_throw_and_resistance[1].replace("Spell Resistance", "")
    else:
        return saving_throw_and_resistance[0].replace("Saving Throw", ""), None

def parse_components(paragraph):
    final_components = []
    components = paragraph.text.replace("Components", "").replace("Component:", "").split(",")
    for component in components:
        if any(comp in component for comp in ['M', 'F']):
            parsed_components = parse_component_with_item(component)
            if '/' in parsed_components[0]:
                final_components.extend([[x, parsed_components[1]] for x in parsed_components[0].split('/')])
            else:
                if len(parsed_components) == 1:
                    final_components.append(parsed_components[0])
                else:
                    final_components.append(parsed_components)
        else:
            final_components.append(component)

    return final_components



def parse_component_with_item(component):
    components = component.strip().split(" ", 1)
    if len(components) < 2:
        return components

    components[1] = components[1].replace('(', "").replace(")", "")
    return components

def parse_school_and_levels(paragraph):
    parts = paragraph.text.split(";")
    school, subschools = parse_school(parts[0])
    classes = parse_classes(parts[1])

    return school, classes, subschools

def parse_classes(part):
    class_level_dict = {}
    class_and_levels = part.replace("Level", "").split(",")

    for class_and_level in class_and_levels:
        class_level_split = class_and_level.strip().split(" ")
        spell_class = class_level_split[0]
        spell_level = class_level_split[1]

        if spell_class == "sorcerer/wizard":
            class_level_dict["sorcerer"] =  spell_level
            class_level_dict["wizard"] =  spell_level
        else:
            class_level_dict[spell_class] = spell_level

    return class_level_dict

def parse_school(part):
    spell_school = None
    found_subschool = None
    for school in schools:
        result = re.search(school, part)

        if result:
            spell_school = result.group(0)

    if spell_school == None:
        print part

    for subschool in subschools:
        result = re.search(subschool, part)

        if result:
            found_subschool = subschool

    return spell_school, found_subschool



if __name__ == "__main__":
    main()