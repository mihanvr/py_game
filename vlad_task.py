from typing import List, Any
import random


class Unit:
    position: int = 0
    health: int = 10
    name: str = 'Melee'

    battle_field = None
    target = None
    target_count = 0

    miss_chance = 10
    crit_chance = 10

    def __init__(self, name, health):
        self.name = name
        self.health = health

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

    def do_command(self, command: str):
        if command == 'help':
            print('look - узнать текущее состояние поля боя \nmove x - переместиться на x клеток \nselect target - выбрать цель атаки \nattack - атаковать выбранную цель \npass - пропустить ход \nchoose weapon x - снарядить юнита оружием x (только для класса Боец) \nchoose spell x - выбрать заклинание x (только для класса Маг) \nweapons - список оружий \nspells - список заклинаний')
            return False
        if command == 'weapons':
            print('Меч - sword \nКопьё - lance \nЛук - bow \nДлинный лук - long bow')
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


class Warrior(Unit):
    weapon = None

    def get_weapon(self):
        return self.weapon

    def __str__(self) -> str:
        return super().__str__() + ', weapon: ' + str(self.weapon.name)

    def do_command(self, command: str):
        if command.startswith('choose weapon'):
            if self.weapon == hand:
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


class Spell:
    def __init__(self, damage, cost, bonus):
        self.damage = damage
        self.cost = cost
        self.bonus = bonus

    def get_damage(self, range: int):
        return self.damage

    def can_attack(self, range: int):
        return True


fireball = Spell(4, 6, None)
pyroblast = Spell(9, 10, None)
inner_fire = Spell(6, 3, 'inner_fire_self_damage')
arcane_arrows = Spell(1, 3, 'random_arrows')
spells = {'fireball': fireball, 'arcane arrows': arcane_arrows, 'pyroblast': pyroblast, 'inner fire': inner_fire}


class Mage(Unit):
    mana: int = 10
    mana_max: int = 10
    mana_regen: int = 1

    active_spell = fireball

    def can_attack(self, range: int):
        return self.mana >= self.active_spell.cost

    def on_attack(self):
        self.mana -= self.active_spell.cost
        if self.active_spell.bonus is not None:
            if self.active_spell.bonus == 'random_arrows':
                for i in range(4):
                    battle_field.units[random.randint(0, len(battle_field.units) - 1)].health -= self.active_spell.damage
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
        return super().__str__() + ', mana:' + str(self.mana)

    def do_command(self, command: str):
        if command.startswith('choose spell'):
            s = str(command[13:])
            if s in spells:
                self.active_spell = spells[s]
                print('Выбрано заклинание ' + str(s))
                return True
            else:
                print('Такого заклинания не существует')
                return False
        return super().do_command(command)


class BattleField:
    units: List[Unit] = []

    def add_unit(self, unit: Unit):
        self.units.append(unit)
        unit.battle_field = self

    def remove_unit(self, unit: Unit):
        self.units.remove(unit)
        unit.battle_field = self


class Weapon:
    def __init__(self, name, min_range, max_range, damage):
        self.name = name
        self.min_range = min_range
        self.max_range = max_range
        self.damage = damage

    def get_damage(self, range: int):
        return self.damage

    def can_attack(self, range: int):
        return self.min_range <= range <= self.max_range



# class WeaponMelee(Weapon):
#     range: int = 1
#     damage: int = 1
#
#     def get_damage(self, range: int):
#         return self.damage
#
#     def can_attack(self, range: int):
#         return range <= self.range


# class WeaponRange(Weapon):
#     min_range: int = 3
#     max_range: int = 5
#     damage: int = 3
#
#     def get_damage(self, range: int):
#         return self.damage
#
#     def can_attack(self, range: int):
#         return self.min_range <= range <= self.max_range


melee = Warrior('Мечник', 10)
archer = Warrior('Лучник', 5)
mage = Mage('Маг', 5)

melee.position = 1
archer.position = 5
mage.position = 9


bow = Weapon('Лук', 3, 5, 3)
long_bow = Weapon('Длинный лук', 5, 7, 5)
sword = Weapon('Меч', 1, 1, 5)
lance = Weapon('Копьё', 1, 2, 4)
hand = Weapon('Без оружия', 1, 1, 1)
weapons = {'sword': sword, 'bow': bow, 'lance': lance, 'long bow': long_bow, 'hand': hand}
melee.weapon = weapons['hand']
archer.weapon = weapons['hand']

battle_field = BattleField()

battle_field.add_unit(melee)
battle_field.add_unit(archer)
battle_field.add_unit(mage)

print('Введите "help" для списка команд')

while True:
    for unit in battle_field.units:
        print('Ходит ' + unit.name)
        while True:
            command = input()
            if unit.do_command(command):
                break
    print('Раунд окончен')
    for unit in battle_field.units:
        unit.on_round_end()
        if unit.health <= 0:
            battle_field.remove_unit(unit)
            print(unit.name + ' погиб')
    if len(battle_field.units) == 1:
        print(str(battle_field.units[0].name) + ' победил')
        break
    if len(battle_field.units) == 0:
        print('Все юниты погибли')
        break
    pass
