import random
from dataclasses import dataclass
from typing import Optional

from battle.database import weapons


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

    def get_damage(self) -> int:
        weapon = self.get_weapon()
        if weapon is None:
            return 0
        return weapon.get_damage()

    def get_weapon(self) -> Optional['Weapon']:
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

    def do_command(self, command: str):
        if command == 'help':
            print(
                'look - узнать текущее состояние поля боя \nmove x - переместиться на x клеток \nselect target - выбрать цель атаки \nattack - атаковать выбранную цель \npass - пропустить ход \nchoose weapon x - снарядить юнита оружием x (только для класса Боец) \nchoose spell x - выбрать заклинание x (только для класса Маг) \nweapons - список оружий \nspells - список заклинаний')
            return False
        if command == 'weapons':
            print(weapons)
            # print('Меч - sword \nКопьё - lance \nЛук - bow \nДлинный лук - long bow')
            return False
        if command == 'spells':
            print('fireball, pyroblast, arcane arrows, inner fire')
            return False
        if command == 'pass':
            return True
        if command.startswith('move'):
            range = int(command[4:])
            self.position += range
            return True
        if command == 'look':
            print([str(x) for x in self.battle_field.units])
            return False
        if command == 'select target':
            targets = [unit for unit in self.battle_field.units if unit != self]
            if len(targets) > 0:
                self.target = targets[self.target_count]
                if self.target_count == len(targets) - 1:
                    self.target_count = 0
                else:
                    self.target_count += 1
                    print(self.target_count)
                print('Выбрана цель: ' + self.target.name)
            return False
        if command == 'attack':
            if self.target is None:
                print('Цель не выбрана')
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
                    print(self.name + ' атакует ' + self.target.name + '. Нанесено урона: ' + str(damage))
                    self.target_count = 0
                    return True
                else:
                    print(self.name + ' промахнулся')
                    return True
            else:
                print('Невозможно атаковать')
                return False
        print('Неизвестная команда')
        return False

    def on_attack(self):
        pass

    def on_round_end(self):
        pass


@dataclass
class Warrior(Unit):
    weapon: Optional['Weapon'] = None

    def get_weapon(self):
        return self.weapon

    def __str__(self) -> str:
        return super().__str__() + ', weapon: ' + str(self.weapon.name)

    def do_command(self, command: str):
        if command.startswith('choose weapon'):
            if self.weapon is None:
                w = str(command[14:])
                if w in weapons:
                    self.weapon = weapons[w]
                    print('Выбрано оружие: ' + self.weapon.name)
                    return True
                else:
                    print('Такого оружия не существует')
                    return False
            else:
                print('Оружие уже выбрано')
                return False
        return super().do_command(command)


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

    def do_command(self, command: str):
        if command == 'change hand':
            self.active_hand = 1 - self.active_hand
            print('сменил руку на ' + str(self.active_hand))
            return False
        return super().do_command(command)

    def __str__(self) -> str:
        return super().__str__() + ', hand:' + str(self.active_hand)
