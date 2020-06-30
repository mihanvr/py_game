import json

from battle.spells import Spell
from battle.weapons import Weapon


class BaseRepository:
    path: str
    all_items = None
    json_to_type_object = None

    def __init__(self, path: str, json_to_type_object):
        self.path = path
        self.json_to_type_object = json_to_type_object

    def save_all(self):
        dict_list = list(map(lambda x: x.__dict__, self.all_items))
        json_list = json.dumps(dict_list, ensure_ascii=False)
        with open(self.path, 'w', encoding='utf-8') as file:
            file.write(json_list)

    def load_all(self):
        self.all_items = list(map(self.json_to_type_object, json.load(open(self.path, encoding='utf-8'))))

    def get_all(self):
        return self.all_items

    def get_one(self, id: str):
        for x in self.all_items:
            if x.id == id:
                return x
        return None

    def delete_one(self, id: str):
        for i in range(len(self.all_items)):
            x = self.all_items[i]
            if x.id == id:
                del self.all_items[i]
                self.save_all()
                return x
        return None

    def create_one(self, json):
        self.all_items.append(self.json_to_type_object(json))

    def update_one(self, json):
        existed: object = self.get_one(json['id'])
        existed.__dict__.update(json)

    def __getitem__(self, id: str):
        return self.get_one(id)

    def __contains__(self, id):
        return self.get_one(id) is not None


weapon_repository = BaseRepository('../assets/weapons.json', lambda x: Weapon(**x))
weapon_repository.load_all()

spell_repository = BaseRepository('../assets/spells.json', lambda x: Spell(**x))
spell_repository.load_all()


weapons = weapon_repository
spells = spell_repository
