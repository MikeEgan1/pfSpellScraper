from bs4 import BeautifulSoup
import re
import urllib2
import pf_data
from Spell import Spell


class SpellParser(object):
    orign_class = None

    def __init__(self, origin_class=None):
        self.orign_class = origin_class

    def parse_spell(self, url, spell_name, source_book):
        content = urllib2.urlopen(url)
        soup = BeautifulSoup(content.read(), "html.parser")
        spell = self.scrape_spell_page(soup)
        spell.name = spell_name
        spell.source_book = source_book
        spell.url = url
        return spell

    def scrape_spell_page(self, soup):
        spell = Spell()
        body = soup.find_all('body')
        paragraphs = body[0].find_all('p')

        for paragraph in paragraphs:
            if paragraph.attrs.get("class") is not None and paragraph.attrs.get("class")[0] == "stat-block-title":
                continue
            elif "School" in paragraph.text:
                spell.school, spell.levels, spell.subschool = self.parse_school_and_levels(paragraph)
            elif "Casting Time" in paragraph.text:
                spell.action = self.parse_action(paragraph)
            elif "Component" in paragraph.text:
                spell.components = self.parse_components(paragraph)
            elif "Range" in paragraph.text:
                spell.range = self.parse_range(paragraph)
            elif "Effect" in paragraph.text:
                spell.effect = self.parse_effect(paragraph)
            elif "Duration" in paragraph.text:
                spell.duration = self.parse_duration(paragraph)
            elif "Saving Throw" in paragraph.text:
                spell.saving_throw, spell.spell_resistance = self.parse_saving_throw(paragraph)
            elif "Report a Problem" in paragraph.text:
                continue
            else:
                # print paragraph.text
                if spell.description is None:
                    spell.description = paragraph.text
                else:
                    spell.description = spell.description + " " + paragraph.text

        return spell

    @staticmethod
    def parse_action(paragraph):
        return paragraph.text.replace("Casting Time", "")

    @staticmethod
    def parse_range(paragraph):
        return paragraph.text.replace("Range", "")

    @staticmethod
    def parse_effect(paragraph):
        return paragraph.text.replace("Effect", "")

    @staticmethod
    def parse_duration(paragraph):
        return paragraph.text.replace("Duration", "")

    @staticmethod
    def parse_saving_throw(paragraph):
        saving_throw_and_resistance = paragraph.text.split(";")
        if len(saving_throw_and_resistance) > 1:
            return saving_throw_and_resistance[0].replace("Saving Throw", "") \
                , saving_throw_and_resistance[1].replace("Spell Resistance", "")
        else:
            return saving_throw_and_resistance[0].replace("Saving Throw", ""), None

    def parse_components(self, paragraph):
        final_components = []
        components = paragraph.text.replace("Components", "").replace("Component:", "").split(",")
        for component in components:
            if any(comp in component for comp in ['M', 'F']):
                parsed_components = self.parse_component_with_item(component)
                if '/' in parsed_components[0]:
                    if len(parsed_components) == 1:
                        final_components.extend([x for x in parsed_components[0].split('/')])
                    else:
                        final_components.extend([[x, parsed_components[1]] for x in parsed_components[0].split('/')])
                else:
                    if len(parsed_components) == 1:
                        final_components.append(parsed_components[0])
                    else:
                        final_components.append(parsed_components)
            else:
                final_components.append(component.strip())

        return final_components

    @staticmethod
    def parse_component_with_item(component):
        components = component.strip().split(" ", 1)
        if len(components) < 2:
            return components

        components[1] = components[1].replace('(', "").replace(")", "")
        return components

    def parse_school_and_levels(self, paragraph):
        parts = paragraph.text.split(";")
        school, subschools = self.parse_school(parts[0])
        classes = self.parse_classes(parts[1])

        return school, classes, subschools

    def parse_classes(self, part):
        # TODO BUILD SUPPORT FOR ORIGIN CLASS
        class_level_dict = {}
        class_and_levels = part.replace("Level", "").split(",")

        for class_and_level in class_and_levels:
            class_level_split = class_and_level.strip().split(" ")
            spell_class = class_level_split[0]
            spell_level = class_level_split[1]

            if spell_class == "sorcerer/wizard":
                class_level_dict["sorcerer"] = spell_level
                class_level_dict["wizard"] = spell_level
            elif spell_class == "cleric":
                class_level_dict["cleric"] = spell_level
                class_level_dict["oracle"] = spell_level
            else:
                class_level_dict[spell_class] = spell_level

        if self.orign_class is not None:
            class_level_dict[self.orign_class["class"]] = self.orign_class["level"]

        return class_level_dict

    @staticmethod
    def parse_school(part):
        spell_school = None
        found_subschool = None
        for school in pf_data.schools:
            result = re.search(school, part)

            if result:
                spell_school = result.group(0)

        if spell_school is None:
            print part

        for subschool in pf_data.subschools:
            result = re.search(subschool, part)

            if result:
                found_subschool = subschool

        return spell_school, found_subschool
