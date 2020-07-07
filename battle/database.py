import json
import os.path

from battle.spells import Spell
from battle.users import User
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
        if os.path.isfile(self.path):
            self.all_items = list(map(self.json_to_type_object, json.load(open(self.path, encoding='utf-8'))))
        else:
            self.all_items = []

    def get_all(self):
        return self.all_items

    def find_one(self, id: str):
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

    def create_one_json(self, json):
        self.create_one(self.json_to_type_object(json))

    def create_one(self, entity):
        self.all_items.append(entity)

    def update_one(self, json):
        existed: object = self.find_one(json['id'])
        existed.__dict__.update(json)

    def __getitem__(self, id: str):
        return self.find_one(id)

    def __contains__(self, id):
        return self.find_one(id) is not None


weapon_repository = BaseRepository('../assets/weapons.json', lambda x: Weapon(**x))
weapon_repository.load_all()

spell_repository = BaseRepository('../assets/spells.json', lambda x: Spell(**x))
spell_repository.load_all()

users_repository = BaseRepository('../assets/users.json', lambda x: User(**x))
users_repository.load_all()


def find_by_token(token: str):
    for user in users_repository.get_all():
        if user.token == token:
            return user
    return None


def find_by_login(login: str):
    for user in users_repository.get_all():
        if user.login == login:
            return user
    return None


users_repository.find_by_token = find_by_token
users_repository.find_by_login = find_by_login


weapons = weapon_repository
spells = spell_repository
