'''Murloc Module for Dungeon Dudes'''
from typing import Dict, Tuple
from random import randint

from src.dd_data import LimitedDict
from ..humanoid import Humanoid
from ...combat_action import CombatAction

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
    
    @property
    def tribe_size(self):
        return self._tribe_size

    def get_skills(self):
        return {}
    
    def get_skills_list(self):
        skills_list = ["Ice Bolt", "Forage"]
        return skills_list

    def ice_bolt(self):
        damage = self.humanoid_damage(self.modify_damage(self.intelligence))
        msg: str = "Murloc casts Ice Bolt for <value> Ice Damage"
        return("Attack", damage, "Ice", msg)
    
    def forage(self):
        self._healing_potions += 1
        self.printer(f"Murloc has gathered ingredients to make a healing "
                     f"potion. Murloc tribe now has {self.healing_potions} "
                     "Healing Potions.")
        return ("Heal", 0, "Heal", "")
    
    def get_action(self):
        actions = [self.ice_bolt,
                   self.ice_bolt,
                   self.forage,
                   self.forage]
        index = randint(0, (len(actions) - 1))
        option = actions.pop(index)
        return option()

    def take_turn(self):
        damage: int = self.humanoid_damage(self.modify_damage(self.attack_power))
        msg: str = "Murloc attacks, dealing <value> physical damage"
        attack = ("Attack", damage, "Physical", msg)
        action_list = []
        for _ in range(1, self.tribe_size):
            action_list.append(attack)
        action_list.append(self.get_action())
        action = CombatAction(action_list, "")
        return action
