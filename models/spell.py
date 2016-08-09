from models import Models

class Spell(Models):
    def __init__(self):
        super(Spell, self).__init__()

    def save(self, spell):
        sql = "Insert into spells (spell_data) values ('" + self.cm.get_connection().escape_string(spell.json()) + "')"
        self.save_to_mysql(sql)
        self.save_to_elastic_search("pfspells", "spell", spell.json())
