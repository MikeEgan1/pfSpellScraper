import json

class Spell(object):

    name = None
    school = None
    subschool = None
    descriptors = []
    levels = None
    action = None
    components = []
    range = None
    effect = None
    duration = None
    saving_throw = None
    spell_resistance = None
    description = None

    def __init__(self):
        return

    def toString(self):
        return self.__dict__

    def json(self):
        return json.dumps(self.__dict__)
