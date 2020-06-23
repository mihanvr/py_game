from typing import List, Any


class Unit:
    position: int = 0
    health: int = 10
    name: str = 'Melee'

    battle_field = None
    target = None

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

    def do_command(self, command: str):
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
            target = None
            targets = [unit for unit in self.battle_field.units if unit != self]
            if len(targets) > 0:
                self.target = targets[0]
                print('Выбрана цель: ' + self.target.name)
            return False
        if command == 'attack':
            if self.target is None:
                print('Цель не выбрана')
                return False
            range = abs(self.position - self.target.position)
            if self.can_attack(range):
                damage = self.get_damage()
                self.target.health -= damage
                self.on_attack()
                print(self.name + ' атакует ' + self.target.name + '. Нанесено урона: ' + str(damage))
                return True
            else:
                print('Неверная дистанция атаки')
                return False
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
        weapon1 =  ("Короткий меч")
        weapon2 =  ("Короткий лук" )
        weapon3 =  ("Короткий посох")

def get_weapon(self):
        return self.weapon


class Mage(Unit):
    mana: int = 10
    mana_max: int = 10
    mana_regen: int = 2

    fireball_cost: int = 6
    fireball_damage: int = 4

    iceball_cost: int = 3
    iceball_damage: int = 2

    lightning_cost: int = 8
    lightning_damage: int = 6

    def can_attack(self, range: int):
        return self.mana >= self.fireball_cost

    def on_attack(self):
        self.mana -= self.fireball_cost

    def on_round_end(self):
        delta_mana = min(self.mana_regen, self.mana_max - self.mana)
        if delta_mana > 0:
            self.mana += delta_mana
            print(self.name + ' восстановил ' + str(delta_mana) + ' маны')

    def get_damage(self):
        return self.fireball_damage

    def __str__(self) -> str:
        return super().__str__() + ', mana:' + str(self.mana)


class BattleField:
    units: List[Unit] = []

    def add_unit(self, unit: Unit):
        self.units.append(unit)
        unit.battle_field = self


class Weapon:

    def get_damage(self, range: int):
        return 0

    def can_attack(self, range: int):
        return False


class WeaponMelee(Weapon):
    range: int = 1
    damage: int = 1


    def get_damage(self, range: int):
        return self.damage

    def can_attack(self, range: int):
        return range <= self.range

class WeaponRange(Weapon):
    min_range: int = 3
    max_range: int = 5
    damage: int = 3


class Weapon1:
    min_range: int = 1
    max_range: int = 3
    damage: int = 3

class Weapon2:
    min_range: int = 4
    max_range: int = 6
    damage: int = 4

class Weapon3:
    min_range: int = 3
    max_range: int = 7
    damage: int = 5




    def get_damage(self, range: int):
        return self.damage

    def can_attack(self, range: int):
        return self.min_range <= range <= self.max_range


melee = Warrior('Мечник', 10)
archer = Warrior('Лучник', 7)
mage = Mage('Маг', 7)

melee.position = 1
archer.position = 5
mage.position = 9

bow = WeaponRange()
sword = WeaponMelee()
archer.weapon = bow
melee.weapon = sword

battle_field = BattleField()

battle_field.add_unit(melee)
battle_field.add_unit(archer)
battle_field.add_unit(mage)




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
    pass

# active melee
# move 1
