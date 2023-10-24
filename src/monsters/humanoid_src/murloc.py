'''Murloc Module for Dungeon Dudes'''
from typing import Dict, Tuple

from src.dd_data import LimitedDict
from ..humanoid import Humanoid

class Murloc(Humanoid):
    '''Murloc Module'''
    stats_structure: Dict[str, Tuple[int]] = {"Hit Points": (75, 20),
                                              "Strength": (5, 1),
                                              "Agility": (10, 3),
                                              "Intelligence": (6, 2),
                                              "Special": (0, 0)}
    
    def __init__(self, level_mod: int):
        self._tribe_size = 4
        self._hit_points: int = self.stats_structure["Hit Points"][0]
        self._damage_type = "Physical"
        super().__init__("Murloc Tribe",
                         level_mod,
                         self.stats_structure)
        self._dam_modifiers = LimitedDict(("Physical",
                                           "Ice",
                                           "Poison",
                                           "Holy"), default_value=100)
        
    @property
    def damage_modifiers(self):
        return self._dam_modifiers
    
    @property
    def defense_modifiers(self):
        return self._def_modifiers
    
