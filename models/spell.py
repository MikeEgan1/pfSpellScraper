from models import Models
import json


class Spell(Models):
    def __init__(self):
        super(Spell, self).__init__()

    def spell_exists(self, spell):
        sql = "select * from spells where `name` = '{name}'".format(name=self.cm.get_connection().escape_string(spell.name))
        cursor = self.save_to_mysql(sql)

        return cursor.rowcount

    def save(self, spell):

        if self.spell_exists(spell) or spell.name == "Storm of Vengeance":
            return

        print spell.name
        sql = "Insert into spells " \
              "(" \
              "`name`," \
              " school_id," \
              " subschool_id," \
              " description," \
              " `action`," \
              " components," \
              " `range`," \
              " effect," \
              " duration," \
              " saving_throw," \
              " spell_resistance," \
              " source_book," \
              " url)" \
              " values (" \
              " '{name}'," \
              " {school_id}," \
              " {subschool_id}," \
              " '{description}'," \
              " '{action}'," \
              " '{components}'," \
              " '{range}'," \
              " '{effect}'," \
              " '{duration}'," \
              " '{saving_throw}'," \
              " '{spell_resistance}'," \
              " '{source_book}'," \
              " '{url}');".format(
            name=self.connection.escape_string(spell.name) if spell.name is not None else "NULL",
            school_id=spell.school if spell.school is not None else 0,
            subschool_id=spell.subschool if spell.subschool is not None else "NULL",
            description=self.cm.get_connection().escape_string(spell.description.encode('utf8').replace("<i>", "").replace("</i>", "")),
            action=spell.action if spell.action is not None else "NULL",
            components=self.connection.escape_string(json.dumps(spell.components)),
            range=spell.range if not spell.range is not None else "NULL",
            effect=spell.effect if spell.effect is not None else "NULL",
            duration=spell.duration if spell.duration is not None else "NULL",
            saving_throw=getattr(spell, "saving_throw", "NULL"),
            spell_resistance=spell.spell_resistance,
            source_book=spell.source_book,
            url=spell.url
        )
        cursor = self.save_to_mysql(sql)

        insert_id = cursor.lastrowid

        for cls, level in spell.levels.iteritems():
            sql = "Insert into spells_by_class (class_id, spell_id, spell_level) values ({class_id}, {spell_id}, {spell_level})".format(class_id=cls, spell_id=insert_id, spell_level=level)
            self.save_to_mysql(sql)



