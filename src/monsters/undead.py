'''Module for the Dungeon Dudes Beast Monster'''
from random import randint
from typing import Tuple
from .monsters_abc import Monster
from ..combat_action import CombatAction
from ..dd_data import CombatPrint, LimitedDict, damage_types


class Undead(Monster):
    '''Undead Monster Class'''

    def __init__(self, name: str, level_mod: int, stat_structure: dict):
        self.gold = level_mod * 4
        super().__init__(name, level_mod, "Undead", stat_structure)
        self.printer = CombatPrint()
        self._def_modifiers = LimitedDict(damage_types, default_value=100)
        self._def_modifiers["Holy"] += 50
        self._dam_modifiers = LimitedDict(("Physical", "Ice"),
                                          default_value=100)
        self._resist = True
        self._haunting = 0

    @staticmethod
    def modify_damage(damage) -> int:
        '''Adds Variance to Damage Events and Calculates Critical Chance'''
        damage_min = int(damage * 0.01)
        damage_max = int(damage * 1.75)
        modified: int = randint(damage_min, damage_max)
        return modified

    @property
    def hit_points(self) -> int:
        '''Override Parent Getter for HP'''
        return self._hit_points

    @hit_points.setter
    def hit_points(self, value):
        '''Setter for Hit Points'''
        if value >= self.max_hit_points:
            self._hit_points = self.max_hit_points
        else:
            self._hit_points = int(value)

    def resist_death(self, damage: int, message: str):
        '''First time an event would kill, reduce HP to 1'''
        message = message.replace('<value>', str(damage))
        resist_message = f"Resist Death saves {self.name}! HP reset to 1."
        self.printer(message)
        self.printer(resist_message)
        self._resist = False

    def haunting_arua(self) -> Tuple:
        '''First time an undead attacks, player Physical mod reduced by 10'''
        self._haunting += 1
        return ("Hex", -10, "Physical", "")

    def take_turn(self) -> CombatAction:  # pylint: disable=unused-argument
        '''Takes turn and returns the success of the action and the action'''
        return self.attack()
