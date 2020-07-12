import json
from typing import List, Optional

from battle.database import weapons, spells
from battle.units import Unit, Warrior, Mage, Archer, BattleField
from battle.users import User


def load_unit(unit_db: dict) -> Unit:
    unit_class = unit_db['class']
    unit: Unit
    if unit_class == 'warrior':
        unit = Warrior(None)
        weapon_id = unit_db.get('weapon', None)
        if weapon_id is not None:
            unit.weapon = weapons[weapon_id]
        else:
            unit.weapon = weapons['hand']
    if unit_class == 'archer':
        unit = Archer(None)
        weapon_id = unit_db.get('weapon', None)
        if weapon_id is not None:
            unit.weapon = weapons[weapon_id]
        else:
            unit.weapon = weapons['hand']
    elif unit_class == 'mage':
        unit = Mage(None)
        spell_id = unit_db.get('spell', None)
        if spell_id is not None:
            unit.active_spell = spells[spell_id]

    unit.name = unit_db['name']
    unit.health = unit_db['health']
    unit.position = unit_db['position']
    return unit


def create_new_game(response: List[str]) -> BattleField:
    field = BattleField()
    dummy_unit = Unit(None, 0, 0, 'dummy')
    field.add_unit(dummy_unit)
    response.append('new game created, type "create unit <unit_class>" to add units')
    return field


def save_game(battle_field, response:List[str]):
    units = []
    for unit in battle_field.units:
        if isinstance(unit, Warrior):
            units.append(
                {"class": "warrior",
                 "name": str(unit.name),
                 "health": unit.health,
                 "position": unit.position,
                 "weapon": unit.weapon.id
                 })
        if isinstance(unit, Archer):
            units.append(
                {"class": "archer",
                 "name": str(unit.name),
                 "health": unit.health,
                 "position": unit.position,
                 "weapon": unit.weapon.id
                 })
        if isinstance(unit, Mage):
            units.append(
                {"class": "mage",
                 "name": str(unit.name),
                 "health": unit.health,
                 "position": unit.position,
                 "spell": unit.active_spell.id
                 })
    root = {
        'units': units,
        'active_unit_index': battle_field.active_unit_index,
    }
    with open('../client/save.json', 'w') as f:
        json.dump(root, f)
    response.append('Игра сохранена')
    return 0


def load_saved_game(response: List[str]) -> BattleField:
    field = BattleField()
    root = json.load(open('../client/save.json', encoding='utf-8'))
    for unit_db in root['units']:
        field.add_unit(load_unit(unit_db))
    field.active_unit_index = root['active_unit_index']
    response.append('game loaded')
    return field


def load_game(command: str, response: List[str]):
    global battle_field
    if command == 'new':
        battle_field = create_new_game(response)
    elif command == 'load':
        battle_field = load_saved_game(response)
    else:
        response.append('Введите "load", чтобы продолжить игру, или "new", чтобы создать новую')


battle_field: Optional[BattleField] = None


def do_game_loop(command, user: User, response):
    unit = battle_field.units[battle_field.active_unit_index]
    # print('Ходит ' + unit.name)
    if command == 'save':
        save_game(battle_field, response)
        return
    if command.startswith('create unit'):
        unit_class = str(command[12:])
        print(unit_class)
        root = json.load(open('../assets/units.json', encoding='utf-8'))
        for un in root:
            if un['class'] == unit_class:
                new_unit = load_unit(un)
                new_unit.login = user.login
                battle_field.add_unit(new_unit)
                response.append('Unit created')
                return
        response.append('Unknown class')
        return
    if (unit.login != user.login) and not command.startswith('create unit'):
        response.append("You don't own this unit")
        return
    if not unit.do_command(command, response):
        response.append('Unit not moved')
        return
    battle_field.active_unit_index += 1
    if battle_field.active_unit_index < len(battle_field.units):
        return

    response.append('Раунд окончен')
    battle_field.active_unit_index = 0
    remove_units = []
    for unit in battle_field.units:
        unit.on_round_end()
        if unit.health <= 0:
            remove_units.append(unit)
            response.append(unit.name + ' погиб')
    for remove_unit in remove_units:
        battle_field.units.remove(remove_unit)
    for unit in remove_units:
        battle_field.remove_unit(unit)
    if len(battle_field.units) == 1:
        response.append(str(battle_field.units[0].name) + ' победил')
        return
    if len(battle_field.units) == 0:
        response.append('Все юниты погибли')
        return
    pass


def do_command(command: str, user: User) -> List[str]:
    global battle_field
    response = []
    if battle_field is None:
        load_game(command, response)
    else:
        do_game_loop(command, user, response)
    return response


# print('Введите "help" для списка команд')

# while True:
#     unit = battle_field.units[battle_field.active_unit_index]
#     print('Ходит ' + unit.name)
#     while True:
#         command = input()
#         if command == 'save':
#             save_game(battle_field)
#             continue
#         if unit.do_command(command):
#             break
#     battle_field.active_unit_index += 1
#     if battle_field.active_unit_index < len(battle_field.units):
#         continue
#
#     print('Раунд окончен')
#     battle_field.active_unit_index = 0
#     remove_units = []
#     for unit in battle_field.units:
#         unit.on_round_end()
#         if unit.health <= 0:
#             remove_units.append(unit)
#             print(unit.name + ' погиб')
#     for remove_unit in remove_units:
#         battle_field.units.remove(remove_unit)
#     for unit in remove_units:
#         battle_field.remove_unit(unit)
#     if len(battle_field.units) == 1:
#         print(str(battle_field.units[0].name) + ' победил')
#         break
#     if len(battle_field.units) == 0:
#         print('Все юниты погибли')
#         break
#     pass
# print("Игра окончена")
