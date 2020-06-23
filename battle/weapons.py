from dataclasses import dataclass


@dataclass()
class Weapon:

    id: str = ''
    name: str = ''
    min_range: int = 0
    max_range: int = 0
    damage: int = 0

    def get_damage(self, range: int):
        return self.damage

    def can_attack(self, range: int):
        return self.min_range <= range <= self.max_range
