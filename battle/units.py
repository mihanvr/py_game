import random
from dataclasses import dataclass
from typing import Optional, List

from battle.database import weapons, spells


@dataclass
class Unit:
    position: int = 0
    health: int = 10
    name: str = 'Melee'

    battle_field: Optional['BattleField'] = None
    target: Optional['Unit'] = None
    target_count: int = 0

    miss_chance: int = 10
    crit_chance: int = 10

    def can_attack(self, range: int):
        weapon = self.get_weapon()
        if weapon is None:
            return False
        return weapon.can_attack(range)

    def __str__(self) -> str:
        return self.name + ': ' + str(self.health) + 'hp, pos:' + str(self.position)

    def get_damage(self):
        weapon = self.get_weapon()
        if weapon is None:
            return 0
        return weapon.get_damage(range)

    def get_weapon(self):
        return None

    def miss(self):
        num = random.randint(1, self.miss_chance)
        if num == 1:
            return True
        else:
            return False

    def crit(self):
        num = random.randint(1, self.crit_chance)
        if num == 1:
            return True
        else:
            return False

    def do_command(self, command: str, response: List[str]):
        if command == 'help':
            response.append(
                'look - узнать текущее состояние поля боя \nmove x - переместиться на x клеток \nselect target - выбрать цель атаки \nattack - атаковать выбранную цель \npass - пропустить ход \nchoose weapon x - снарядить юнита оружием x (только для класса Боец) \nchoose spell x - выбрать заклинание x (только для класса Маг) \nweapons - список оружий \nspells - список заклинаний')
            return False
        if command == 'weapons':
            response.append(weapons)
            return False
        if command == 'spells':
            response.append('fireball, pyroblast, arcane arrows, inner fire')
            return False
        if command == 'pass':
            return True
        if command.startswith('move'):
            range = int(command[4:])
            self.position += range
            return True
        if command == 'look':
            units_list = [str(x) for x in self.battle_field.units]
            response.append("\n".join(units_list))
            return False
        if command == 'select target':
            targets = [unit for unit in self.battle_field.units if unit != self]
            if len(targets) > 0:
                self.target = targets[self.target_count]
                if self.target_count == len(targets) - 1:
                    self.target_count = 0
                else:
                    self.target_count += 1
                    response.append(self.target_count)
                response.append('Выбрана цель: ' + self.target.name)
            return False
        if command == 'attack':
            if self.target is None:
                response.append('Цель не выбрана')
                return False
            range = abs(self.position - self.target.position)
            if self.can_attack(range):
                if not self.miss():
                    if self.crit():
                        damage = self.get_damage() * 2
                    else:
                        damage = self.get_damage()
                    self.target.health -= damage
                    self.on_attack()
                    response.append(self.name + ' атакует ' + self.target.name + '. Нанесено урона: ' + str(damage))
                    self.target_count = 0
                    return True
                else:
                    response.append(self.name + ' промахнулся')
                    return True
            else:
                response.append('Невозможно атаковать')
                return False
        response.append('Неизвестная команда')
        return False

    def on_attack(self):
        pass

    def on_round_end(self):
        pass


class Melee(Unit):
    left_hand_range: int = 1
    right_hand_range: int = 2

    left_hand_damage: int = 5
    right_hand_damage: int = 3

    active_hand: int = 0  # 0 - left,  1 - right

    def can_attack(self, range: int):
        if self.active_hand == 0:
            return range <= self.left_hand_range
        else:
            return range <= self.right_hand_range

    def get_damage(self):
        if self.active_hand == 0:
            return self.left_hand_damage
        else:
            return self.right_hand_damage

    def do_command(self, command: str, response: List[str]):
        if command == 'change hand':
            self.active_hand = 1 - self.active_hand
            response.append('сменил руку на ' + str(self.active_hand))
            return False
        return super().do_command(command, response)

    def __str__(self) -> str:
        return super().__str__() + ', hand:' + str(self.active_hand)


@dataclass
class Warrior(Unit):
    weapon: Optional['Weapon'] = None

    def get_weapon(self):
        return self.weapon

    def __str__(self) -> str:
        return super().__str__() + ', weapon: ' + str(self.weapon.name)

    def do_command(self, command: str, response: List[str]):
        if command.startswith('choose weapon'):
            w = str(command[14:])
            if w in weapons:
                self.weapon = weapons[w]
                response.append('Выбрано оружие: ' + self.weapon.name)
                return True
            else:
                response.append('Такого оружия не существует')
                return False
        return super().do_command(command, response)


class Mage(Unit):
    mana: int = 10
    mana_max: int = 10
    mana_regen: int = 1

    active_spell: Optional['Spell'] = None

    def can_attack(self, range: int):
        return self.mana >= self.active_spell.cost

    def on_attack(self):
        self.mana -= self.active_spell.cost
        if self.active_spell.bonus is not None:
            if self.active_spell.bonus == 'random_arrows':
                for i in range(4):
                    self.battle_field.units[
                        random.randint(0, len(self.battle_field.units) - 1)].health -= self.active_spell.damage
            if self.active_spell.bonus == 'inner_fire_self_damage':
                self.health -= 3

    def on_round_end(self):
        delta_mana = min(self.mana_regen, self.mana_max - self.mana)
        if delta_mana > 0:
            self.mana += delta_mana
            print(self.name + ' восстановил ' + str(delta_mana) + ' маны')

    def get_damage(self):
        return self.active_spell.damage

    def __str__(self) -> str:
        return super().__str__() + ', mana:' + str(self.mana) + ', spell:' + str(self.active_spell.name)

    def do_command(self, command: str, response: List[str]):
        if command.startswith('choose spell'):
            s = str(command[13:])
            if s in spells:
                self.active_spell = spells[s]
                response.append('Выбрано заклинание ' + str(s))
                return True
            else:
                response.append('Такого заклинания не существует')
                return False
        return super().do_command(command, response)


class BattleField:
    units: List[Unit] = []
    active_unit_index: int = 0

    def add_unit(self, unit: Unit):
        self.units.append(unit)
        unit.battle_field = self

    def remove_unit(self, unit: Unit):
        self.units.remove(unit)
        unit.battle_field = self
