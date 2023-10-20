'''Character Ability Score Management Class'''
from typing import Tuple

class Stats:
    '''Object that manages the ability scores for a Classes'''

    def __init__(self, stats_structure: dict):
        self._max_hit_points : Tuple[int] = stats_structure["Hit Points"]
        self._strength : Tuple[int] = stats_structure["Strength"]
        self._agility : Tuple[int] = stats_structure["Agility"]
        self._intelligence : Tuple[int] = stats_structure["Intelligence"]
        self._max_special : Tuple[int] = stats_structure["Special"]

    def level_up(self):
        '''Increases Stats on Level up'''
        self._max_hit_points : Tuple[int] = (self._max_hit_points[0] + self._max_hit_points[1],
                                       self._max_hit_points[1])
        self._strength : Tuple[int] = (self._strength[0] + self._strength[1],
                                       self._strength[1])
        self._agility : Tuple[int] = (self._agility[0] + self._agility[1],
                                       self._agility[1])
        self._intelligence : Tuple[int] = (self._intelligence[0] + self._intelligence[1],
                                       self._intelligence[1])
        self._max_special : Tuple[int] = (self._max_special[0] + self._max_special[1],
                                        self._max_special[1])


    @property
    def max_hit_points(self) -> int:
        '''Getter for Hit Points'''
        return self._max_hit_points[0]
    
    @property
    def hp_growth(self) -> int:
        '''Getter for HP Growth Per Level'''
        return self._max_hit_points[1]
    
    @property
    def strength(self) -> int:
        '''Getter for Strength Stat'''
        return self._strength[0]

    @property
    def agility(self) -> int:
        '''Getter for Agility Stat'''
        return self._agility[0]

    @property
    def intelligence(self) -> int:
        '''Getter for Intelligence Stat'''
        return self._intelligence[0]

    @property
    def special(self) -> int:
        '''Getter for Special Stat (Class Specific)'''
        return self._max_special[0]

    @special.setter
    def special(self, change):
        self._max_special : Tuple[int] = (change, self._max_special[1])

    def __str__(self):
        return (f"{'Strength:':20}{self.strength:5}\t"
                f"{'Agility:':20}{self.agility:5}\t"
                f"{'Intelligence:':20}{self.intelligence:5}")
