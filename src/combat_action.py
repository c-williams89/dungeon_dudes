'''Combat Action Class for Dungeon Dudes'''
from typing import Tuple, List
from .dd_data.meta_data import supported_actions

class CombatAction:
    '''Combat Action Class'''
    def __init__(self, actions : List[Tuple[str, int, str, str]],
                 message : str, special : str =None):
        self._actions : list = [action for action in actions
                         if action[0] in supported_actions]
        print(self._actions)
        self._message : str = message
        if not special:
            self._special = ""
        else:
            self._special = special

    @property
    def message(self) -> str:
        '''Getter for Action Message'''
        return self._message

    @property
    def special(self) -> str:
        '''Getter for Action Special Message'''
        return self._special

    @property
    def actions(self) -> list:
        '''Getter for Actions List'''
        return self._actions
