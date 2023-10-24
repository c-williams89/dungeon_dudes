'''Bandit Module for Dungeon Dudes'''
from typing import Dict, Tuple
from random import choice, randint

from src.dd_data import LimitedDict
from ..humanoid import Humanoid
from ...dd_data import LimitedDict
from ...combat_action import CombatAction

class Bandit(Humanoid):
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
        self._dam_modifiers = LimitedDict(("Physical", "Fire"), default_value=100)
        
    @property
    def damage_modifiers(self) -> LimitedDict:
        return self._dam_modifiers
    
    @property
    def defense_modifiers(self) -> LimitedDict:
        return self._def_modifiers
    
    def get_skills(self) ->Dict[str, 'function']:
        return {}
    
    def get_skills_list(self) -> list:
        skills_list = ["Fireball", "Dirty Tricks"]
        return skills_list

    
    def fireball(self) -> Tuple:
        # damage_type = "Fire"
        damage_amt = self.intelligence
        msg: str = "Bandit Sorcerer casts fireball, dealing <value> fire damage"
        return ("Attack", damage_amt, "Fire", msg)
        # return CombatAction([("Attack",
        #                       damage_amt,
        #                       "Fire",
        #                       msg)], "")
    
    def dirty_tricks(self) -> Tuple:
        msg: str = "Bandit Rogue attacks for <value> Physical damage"
        damage_amt = int((3 * self.attack_power) / 4)
        return ("Attack", damage_amt, "Physical", msg)
        # return CombatAction([("Attack",
        #                       damage_amt,
        #                       "Physical",
        #                       msg)], "")
    
    # def increased_band_size(self):
    
    def get_action(self):
        actions = [self.fireball(),
                   self.fireball(),
                   self.dirty_tricks()]
        index = randint(0, (len(actions) - 1))
        option = actions.pop(index)
        return option
    
    def take_turn(self) -> CombatAction:
        damage: int = self.humanoid_damage(self.modify_damage((self.attack_power)))
        action = CombatAction([("Attack", damage, "Physical", "Some message"),
                             ("Attack", damage, "Physical", "Second message"),
                             self.get_action()], "")
        return action
