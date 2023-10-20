'''
Module for Combatant Abstract Class in Dungeon Dudes
Both Characters and Monsters are Combatants.  
Encounters are designed to interact with Combatant Objects
'''
from abc import ABC, abstractmethod
from typing import List, Tuple, Dict
from .stats import Stats
from .dd_data import LimitedDict, damage_types

class Combatant(ABC):
    '''Combatant Class'''
    def __init__(self, name : str, com_class: str, stat_structure: dict):
        self._name : str = name
        self._class : str = com_class
        self._stats = Stats(stat_structure)
        self.damage_types = damage_types
        if not hasattr(self, '_level'):
            self._level : int = 1
        if not hasattr(self, '_hit_points'):
            self._hit_points : int = 0
        if not hasattr(self, '_attack_power'):
            self._attack_power : int = 0
        if not hasattr(self, '_defense_power'):
            self._defense_power : int = 0
        if not hasattr(self, '_gold'):
            self._gold : int = 100
        if not hasattr(self, '_experience_points'):
            self._experience_points : int = 0

    @property
    def gold(self) -> int:
        '''Getter for Combatant Gold'''
        return self._gold

    @gold.setter
    def gold(self, new_gold : int):
        '''Setter for Combatant Gold'''
        if new_gold < 0:
            self._gold = 0
        else:
            self._gold = new_gold

    @property
    def max_hit_points(self) -> int:
        '''Getter for Max Hit Points'''
        return self._stats.max_hit_points

    @property
    def hit_points(self) -> int:
        '''Getter for Hit Points'''
        return self._hit_points

    @hit_points.setter
    @abstractmethod
    def hit_points(self, value : int):
        '''Setter for Hit Points'''

    @property
    def experience_points(self) -> int:
        '''Getter for Experience Points'''
        return self._experience_points

    @property
    def attack_power(self) -> int:
        '''Getter for Attack Power'''
        return self._attack_power

    @property
    def defense_power(self) -> int:
        '''Getter for Defense Power'''
        return self._defense_power

    @property
    def strength(self) -> int:
        '''Getter for Strength Stat'''
        return self._stats.strength

    @property
    def agility(self) -> int:
        '''Getter for Agility Stat'''
        return self._stats.agility

    @property
    def intelligence(self) -> int:
        '''Getter for Intelligence Stat'''
        return self._stats.intelligence

    @property
    def level(self) -> int:
        '''Getter for Level'''
        return self._level

    @property
    def name(self) -> str:
        '''Getter for Name'''
        return self._name

    @property
    def char_class(self) -> str:
        '''Getter for _class'''
        return self._class

    @property
    @abstractmethod
    def damage_modifiers(self) -> LimitedDict:
        '''Getter for Damage Modifiers'''

    @property
    @abstractmethod
    def defense_modifiers(self) -> LimitedDict:
        '''Getter for Defense Modifiers'''

    @property
    @abstractmethod
    def special(self) -> [int, str]:
        '''Getter for Special Resource'''

    @property
    @abstractmethod
    def special_resource(self) -> str:
        '''Getter for Special Resource Name'''

    @abstractmethod
    def attack(self) -> Tuple[bool, str, List[Tuple[str, int, str]]]:
        '''attack method for character'''

    @abstractmethod
    def get_skills_list(self) -> List[str]:
        '''Returns a list of the skills the character has learned'''

    @abstractmethod
    def get_skills(self) -> Dict[str, 'function']:
        '''Returns a Dictionary of learned skills and their method'''

    @abstractmethod
    def win_battle(self, combatant: 'Combatant'):
        '''Instructions for when a combatant beats another combatant'''

    @abstractmethod
    def base_att_def_power(self):
        '''Sets base Attack and Defense Power based on Class'''

    @abstractmethod
    def take_damage(self, damage: int, dmg_type : str, message : str):
        '''Adjusts Hit Points in a Class Specific Way in Response to Damage Events'''

    def level_up(self):
        '''Level up a Combatant'''
        self._stats.level_up()
        self._hit_points += self._stats.hp_growth
        self._level += 1
