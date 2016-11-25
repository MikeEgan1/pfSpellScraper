from models import Models


class Spell(Models):
    def __init__(self):
        super(Spell, self).__init__()

    def save(self, spell):
        body = self.get_exact_from_es("name", spell.name)
        result = self.get_from_es("pfspells", "spell", body)

        if len(result['hits']['hits']) < 1:
            sql = "Insert into spells (spell_data) " \
                  "values ('" + self.cm.get_connection().escape_string(spell.json()) + "')"
            self.save_to_mysql(sql)
            self.save_to_elastic_search("pfspells", "spell", spell.json())
        else:
            print "found dupe " + spell.name
