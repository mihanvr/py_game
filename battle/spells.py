from dataclasses import dataclass
from typing import Optional


@dataclass()
class Spell:
    id: str = ''
    name: str = 'none'
    damage: int = 0
    cost: int = 0
    bonus: Optional[str] = None

    def get_damage(self, range: int):
        return self.damage

    def can_attack(self, range: int):
        return True
