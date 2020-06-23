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
