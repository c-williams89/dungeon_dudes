'''Module for Monster Abstract Class for Dungeon Dudes'''
from abc import abstractmethod
from ..combatant_abc import Combatant
from ..combat_action import CombatAction

class Monster(Combatant):
    '''Monster Abstract Class for Dungeon Dudes'''

    def __init__(self, name: str, level_mod : int, mon_type : str, stat_structure : dict):
        super().__init__(name, mon_type, stat_structure)
        while self._level < level_mod:
            self.level_up()
        self._experience_base : int = (20 * self._level) - 8
        self._experience_points : int = self._experience_base
        self.base_att_def_power()

    @Combatant.experience_points.setter
    def experience_points(self):
        self._experience_points : int = self._experience_base

    def win_battle(self, combatant: Combatant): # pylint: disable=unused-argument
        '''Monsters don't do anything when winning a battle'''

    @property
    def special(self) -> [int, str]:
        '''Getter for Special Resource - Monsters by default don't have one'''
        return ""

    @property
    def special_resource(self) -> str:
        '''Getter for Special Resource - Monsters by default don't have one'''
        return ""

    @abstractmethod
    def take_turn(self) -> CombatAction:
        '''Prompts the Combatant to enter their action for the turn'''
