from bs4 import BeautifulSoup
import urllib2
import re

BASE_URL = "http://paizo.com/pathfinderRPG/prd/coreRulebook/"

classes = [
    'bard',
    'sorcerer',
    'wizard'
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
    'figment',
    'compulsion',
    'healing',
    'charm'
]

descriptors = [
    'light',
    'mind-affecting',
    'fear'
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
    for x in soup.find_all('p'):
        for y in x.find_all('b'):
            links = y.find_all('a')
            if len(links) > 0:
                spell = links[0]
                parse_spell(spell.get('href'), spell.text)

def parse_spell(url, spell_name):
    content = urllib2.urlopen(BASE_URL + url)
    soup = BeautifulSoup(content.read(), "html.parser")
    scrape_spell_page(soup)

    # print spell_name

def scrape_spell_page(soup):
    spell = {}
    body = soup.find_all('body')
    paragraphs = body[0].find_all('p')

    for paragraph in paragraphs:
        if "School" in paragraph.text:
            spell["school"], spell["levels"] = parse_school_and_levels(paragraph)
        elif "Casting Time" in paragraph.text:
            spell["action"] = parse_action(paragraph)
        elif "Components" in paragraph.text:
            spell["components"] = parse_components(paragraph)

    print spell

def parse_action(paragraph):
    return paragraph.text.replace("Casting Time", "")

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
    school = parse_school(parts[0])
    classes = parse_classes(parts[1])

    return school, classes

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
    for school in schools:
        result = re.search(school, part)

        if result:
            spell_school = result.group(0)

    if spell_school == None:
        print part

    return spell_school



if __name__ == "__main__":
    main()