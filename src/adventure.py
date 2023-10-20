'''
Session Management Module for Dungeon Dudes
Sessions are named Adventures per the project theme
'''
from src import singleton
from src.characters import Character

@singleton
class Adventure:
    '''Session Manager for the Current Game'''
    def __init__(self):
        self._character : Character = None
        self._active_encounter : bool = False
        self._last_shop_visit : int = 0
        self._shop_inventory : list = []

    @property
    def character(self) -> Character:
        '''Getter for Current Character'''
        return self._character

    @character.setter
    def character(self, character: Character):
        if isinstance(character, Character):
            self._character = character
        else:
            print("Not a valid Character for this Adventure!")

    @property
    def active_encounter(self) -> bool:
        '''Returns if Adventure is Currently Executing Combat'''
        return self._active_encounter

    @active_encounter.setter
    def active_encounter(self, value : bool):
        if isinstance(value, bool):
            self._active_encounter = value

    @property
    def shop_inventory(self):
        '''Getter for shop inventory, restocks if needed'''
        if self._character.level != self._last_shop_visit:
            self.stock_shop()
        return self._shop_inventory

    def stock_shop(self):
        '''Restocks the Shop and Sets the Level the Shop was Last Stocked at'''
        self._shop_inventory.clear()
        self._shop_inventory.extend([self._character.generate_weapon(),
                                     self._character.generate_armor(),
                                     self._character.generate_accessory()])
        self._last_shop_visit = self._character.level
