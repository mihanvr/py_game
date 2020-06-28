import json
from typing import Dict

from battle.spells import Spell
from battle.weapons import Weapon


def load_weapon(weapon_db) -> Weapon:
    weapon = Weapon(
        name=weapon_db['name'],
        min_range=weapon_db['min_range'],
        max_range=weapon_db['max_range'],
        damage=weapon_db['damage']
    )
    weapon.id = weapon_db['id']
    return weapon


def load_weapons() -> Dict[str, Weapon]:
    weapons_db = json.load(open('../assets/weapons.json', encoding='utf-8'))
    weapons: Dict[str, Weapon] = {}

    for weapon_db in weapons_db:
        weapon = load_weapon(weapon_db)
        weapons[weapon.id] = weapon

    return weapons


def load_spell(spell_db) -> Spell:
    spell = Spell(
        damage=spell_db['damage'],
        cost=spell_db['cost'],
        bonus=spell_db['bonus']
    )
    spell.id = spell_db['id']
    spell.name = spell_db['name']
    return spell


def load_spells() -> Dict[str, Spell]:
    spells_db = json.load(open('../assets/spells.json', encoding='utf-8'))
    spells: Dict[str, Spell] = {}

    for spell_db in spells_db:
        spell = load_spell(spell_db)
        spells[spell.id] = spell

    return spells

weapons = load_weapons()
spells = load_spells()


def save_weapon(new_weapon: Weapon):
    with open('../assets/weapons.json') as weapon_db:
        data = json.load(weapon_db)
    weapon_dict: Dict = {'id': new_weapon.id, 'name': new_weapon.name, 'min_range': new_weapon.min_range, 'max_range': new_weapon.max_range, 'damage': new_weapon.damage}
    data.append(weapon_dict)
    with open('../assets/weapons.json', 'w') as weapon_db:
        json.dump(data, weapon_db)
    return None


def delete_weapon(id: str):
    weapons = json.loads(open('../assets/weapons.json').read())
    for weapon in weapons:
        if weapon['id'] == id:
            weapons.pop(weapons.index(weapon))
            json.dump(weapons, open('../assets/weapons.json', 'w'))
            return 'Weapon deleted'
    return 'Weapon not found'
