'''Bandit Module for Dungeon Dudes'''
from typing import Dict, Tuple

class Bandit:
    '''Bandit Module'''
    stats_structure: Dict[str, Tuple[int]] = {"Hit Points": (75, 20),
                                              "Strength": (5, 1),
                                              "Agility": (10, 3),
                                              "Intelligence": (7, 1),
                                              "Special": (0, 0)}
    
    def __init__(self, level_mod: int):
        self._hit_points: int = self.stats_structure["Hit Points"][0]
        self._damage_type = "Physical"
        super().__init__(f"Pack of Bandits",
                         level_mod,
                         self.stats_structure)
        
    