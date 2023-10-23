'''Module for the Dungeon Dudes Zombie Undead'''
from typing import Dict, List, Tuple
# from random import choice, randint
from ..undead import Undead
from ...dd_data import LimitedDict
from ...combat_action import CombatAction

class Zombie(Undead):
    '''Zombie Undead Class'''
    stats_structure: Dict[str, Tuple[int]] = {"Hit Points": (85, 20), "Strength": (4, 1),
                    "Agility" : (8, 3), "Intelligence" : (0, 0), "Special" : (4,0)}
    
    def __init__(self, level_mod: int):
        self._hit_points: int = self.stats_structure["Hit Points"][0]
        super().__init__('Zombie', level_mod, self.stats_structure)
        self._sub_type: str = "Zombie"
        self._dam_modifiers = LimitedDict(("Physical", "Poison"), default_value=100)
    
    def base_att_def_power(self):
        self._attack_power =  self.strength
        self._defense_power = self.agility

    @property
    def damage_modifiers(self) -> LimitedDict:
        '''Getter for Damage Modifiers'''
        return self._dam_modifiers
    
    @property
    def defense_modifiers(self) -> LimitedDict:
        '''Getter for Defense Modifiers'''
        return self._def_modifiers
    
    def get_skills_list(self) -> List[str]:
        return []
    
    def get_skills(self) -> Dict[str, 'function']:
        return {}

    def attack(self) -> CombatAction:
        '''Attack method for Zombie Horde'''
        horde_size = (self.level // 8) + 6
        horde_actions = []
        for _ in range(horde_size):
            damage: int = (self.modify_damage(self._attack_power))
            message: str = f"{self._sub_type} A zombie attacks with for <value> physical damage"
            horde_actions.append(("Attack", damage, "Physical", message))
        return CombatAction(horde_actions, "")
    
    def take_turn(self) -> CombatAction:
        return self.attack()
