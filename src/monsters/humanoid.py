'''Module for the Dungeon Dudes Humanoid Monster'''
from random import randint
from .monsters_abc import Monster
from ..combat_action import CombatAction
from ..dd_data import CombatPrint, LimitedDict, damage_types

# NOTE: CombantantABC line 19 to modify starting level

class Humanoid(Monster):
    '''Humanoid Monster Class'''

    def __init__(self, name: str, level_mod: int, stat_structure: dict):
        self._gold = 10 + (8 * (level_mod - 1))
        super().__init__(name, level_mod, "Humanoid", stat_structure)
        self.printer = CombatPrint()
        self._def_modifiers = LimitedDict(damage_types, default_value=100)
        self._dam_modifiers = LimitedDict("Physical", default_value=100)
        self._healing_potions = 1

    def modify_damage(self, damage) -> int:
        '''Adds variance to damage events and calculates critical chance'''
        damage_min = int(damage * 0.75)
        damage_max = int(damage * 1.25)
        modified : int = randint(damage_min, damage_max)
        return modified

    def attack(self) -> CombatAction:
        damage: int = self.humanoid_damage(self.modify_damage(self._attack_power))
        message: str = f"{self.name} Attacks with for <value> physical damage"
        return CombatAction([("Attack", damage, "Physical", message)], "")

    def base_att_def_power(self):
        self._attack_power = self.strength
        self._defense_power = self.agility

    @property
    def hit_points(self):
        return self._hit_points

    @hit_points.setter
    def hit_points(self, value):
        if value >= self.max_hit_points:
            self._hit_points = self.max_hit_points
        else:
            self._hit_points = int(value)

    @property
    def healing_potions(self):
        return self._healing_potions

    def take_damage(self, damage: int, dmg_type, message: str) -> bool:
        alive = True
        if dmg_type == "Physical":
            damage = damage - (self._defense_power // 2)
        damage = int(damage * self._def_modifiers[dmg_type]/100)
        if damage >= self.hit_points:
            alive = False
            message = message.replace('<value>', str(self._hit_points))
            self.printer(message)
            self._hit_points = 0
            return alive
        damage = max(1, damage)
        self._hit_points -= damage
        message = message.replace('<value>', str(damage))
        self.printer(message)
        return alive

    def humanoid_damage(self, damage: float) -> int:
        '''
        Increases Humanoid's damage by 25% if Hit Points are greater than
        75% of Max Hit Points
        '''
        if self._hit_points > ((3 * self.max_hit_points) / 4):
            return int(damage * 1.25)
        return int(damage)

    def healing_potion(self, character):
        b_success = False
        if self.healing_potions > 0:
            health = int(self.max_hit_points * .45)
            self._hit_points += health
            self._healing_potions -= 1
            self.printer(f"{character} drank a healing potion and healed {health} hit points")
            b_success = True
        return b_success

    def take_turn(self) -> CombatAction:
        return self.attack()
