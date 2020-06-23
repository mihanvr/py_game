import json
from typing import List, Optional

from battle.database import weapons, spells
from battle.units import Unit, Warrior, Mage, BattleField


def load_unit(unit_db: dict) -> Unit:
    unit_class = unit_db['class']
    unit: Unit
    if unit_class == 'warrior':
        unit = Warrior()
        weapon_id = unit_db.get('weapon', None)
        if weapon_id is not None:
            unit.weapon = weapons[weapon_id]
        else:
            unit.weapon = weapons['hand']
    elif unit_class == 'mage':
        unit = Mage()
        spell_id = unit_db.get('spell', None)
        if spell_id is not None:
            unit.active_spell = spells[spell_id]

    unit.name = unit_db['name']
    unit.health = unit_db['health']
    unit.position = unit_db['position']
    return unit


def create_new_game(response: List[str]) -> BattleField:
    field = BattleField()
    units_db = json.load(open('../assets/units.json', encoding='utf-8'))

    for unit_db in units_db:
        field.add_unit(load_unit(unit_db))
    response.append('new game created')
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
        response.append('Введите "load", чтобы продолжить игру, или "new", чтобы загрузить юнитов из шаблона')


battle_field: Optional[BattleField] = None


def do_game_loop(command, response):
    unit = battle_field.units[battle_field.active_unit_index]
    # print('Ходит ' + unit.name)
    if command == 'save':
        save_game(battle_field, response)
        return
    if not unit.do_command(command, response):
        response.append('unit not moved')
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


def do_command(command: str) -> List[str]:
    global battle_field
    response = []
    if battle_field is None:
        load_game(command, response)
    else:
        do_game_loop(command, response)
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
