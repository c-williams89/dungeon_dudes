'''Character Class for Dungeon Dudes'''
from abc import abstractmethod
from typing import Dict, Tuple
import sys
from ..combatant_abc import Combatant
from ..combat_action import CombatAction
from .equipment import Equipment, Weapon, Armor, Accessory, can_equip
from .character_sheet import character_sheet
from ..dd_data import CombatPrint

class Character(Combatant):
    '''Abstract Base Class for Characters'''
    active_characters : Dict[str, 'Character'] = {}
    def __init__(self, name : str, char_type : str, stat_structure: dict,
                item_compatibility : list):
        super().__init__(name, char_type, stat_structure)
        self._item_compatibility : list = item_compatibility
        self._battles_won : int = 0
        self._scroll_of_escape = 1
        self._healing_potion = 1
        self._exp_to_next_iter = iter([range(1, 100)])
        self._exp_to_next : int = next(self._exp_to_next_iter)
        self.base_att_def_power()
        self.equip(self.generate_weapon())
        self.equip(self.generate_armor())
        self.equip(self.generate_accessory())
        Character.active_characters[self.name] : [str, 'Character'] = self

    @property
    def name(self) -> str:
        '''Getter for name'''
        return self._name

    @name.setter
    def name(self, name : str):
        '''Setter for Character Name'''
        space_count = name.count(' ')
        if space_count <= 2 and name.replace(' ', '').isalpha():
            return name.title()
        else:
            raise ValueError("Invalid name format")

    @property
    def battles_won(self) -> int:
        '''Getter for Number of Battles Won'''
        return self._battles_won

    @property
    def experience_to_next(self) -> int:
        '''Getter for Experience Points to Next Level'''
        return self._exp_to_next

    @property
    def item_compatibility(self) -> list:
        '''Getter for Item Compatibility'''
        return self._item_compatibility

    @property
    def weapon(self) -> str:
        '''Getter for Weapon Name'''
        return self._weapon.name

    @property
    def weapon_cost(self) -> int:
        '''Getter for Weapon Cost'''
        return self._weapon.cost

    @property
    def weapon_sheet(self) -> Weapon:
        '''Getter for the Weapon Object'''
        return self._weapon

    @property
    def armor(self) -> str:
        '''Getter for Armor Name'''
        return self._armor.name

    @property
    def armor_cost(self) -> int:
        '''Getter for Armor Cost'''
        return self._armor.cost

    @property
    def armor_sheet(self) -> Armor:
        '''Getter for the Weapon Object'''
        return self._armor

    @property
    def healing_potion(self) -> int:
        '''Getter for Number of Healing Potions'''
        return self._healing_potion

    @healing_potion.setter
    def healing_potion(self, value):
        if value < 0:
            self._healing_potion = 0
        else:
            self._healing_potion = int(value)

    @property
    def scroll_of_escape(self) -> int:
        '''Getter for Current Scroll of Escape Count'''
        return self._scroll_of_escape

    @scroll_of_escape.setter
    def scroll_of_escape(self, value):
        '''Setter for Scroll of Escape Count'''
        if value < 0:
            self._scroll_of_escape = 0
        else:
            self._scroll_of_escape = value

    @property
    @abstractmethod
    def max_special(self):
        '''Getter for Max Special Resource'''

    @property
    @abstractmethod
    def accessory_type(self) -> str:
        '''Returns the type of the Accessory the Class Uses'''

    @property
    @abstractmethod
    def accessory(self) -> str:
        '''Returns the name of the Equipped Accessory'''

    @property
    @abstractmethod
    def accessory_cost(self) -> int:
        '''Returns the cost of equipped Accessory'''

    @property
    @abstractmethod
    def accessory_sheet(self) -> Accessory:
        '''Returns the Accessory Object'''

    def gain_experience(self, amount : int, combat : bool = False):
        '''Gains experience and checks for level up'''
        self._experience_points += amount
        while self._experience_points >= self._exp_to_next:
            self.level_up(combat=combat)

    def level_up(self, combat=False):
        '''Level up a Character'''
        super().level_up()
        if combat:
            printer = CombatPrint()
            printer(f"{self.name} the {self.char_class} has reached level {self.level}!")
        else:
            print(f"{self.name} the {self.char_class} has reached level {self.level}!")
        self._experience_points -= self._exp_to_next
        try:
            self._exp_to_next : int = next(self._exp_to_next_iter)
        except StopIteration:
            if combat:
                printer("You've Reached Maximum Level!")
            else:
                print("You've Reached Maximum Level!")
            self._exp_to_next = float('inf')

    def equip(self, equipment: Equipment):
        '''Equips an Item'''
        if can_equip(self.item_compatibility, equipment.subtype):
            self.att_def_adjust(equipment)
            if equipment.equipment_type == "Weapon":
                self._weapon = equipment
            elif equipment.equipment_type == "Armor":
                self._armor = equipment
            elif equipment.equipment_type == "Accessory":
                self._accessory = equipment
        else:
            print(f"Cannot Equip {equipment.equipment_type} type {equipment.subtype}")

    def character_death(self, combat=False):
        '''Character Death Message'''
        if combat:
            printer = CombatPrint()
            printer(f"You have died."
              f" The Epic Adventure of {self.name} comes to an end.")
            input("Play again soon!  Press Enter to exit... ")
            sys.exit()
        print(f"You have died.\n"
              f"The Epic Adventure of {self.name} comes to an end.")
        input("Play again soon!  Press Enter to exit... ")
        sys.exit()

    def use_healing_potion(self) -> Tuple[bool, CombatAction]:
        '''Uses a Healing Potion and Returns the Current Combat Action'''
        printer = CombatPrint()
        success = True
        if self.hit_points == self.max_hit_points:
            printer("Cannot Use Healing Potion, already at Max Health")
            success = False
        elif self._healing_potion == 0:
            printer("Cannot Use Healing Potion, No Healing Potions Left")
            success = False
        if not success:
            return success, CombatAction([("Heal", 0, "Holy", "")], "")
        current = self.hit_points
        heal_amount = int(self.max_hit_points * 0.45)
        self.hit_points += heal_amount
        self._healing_potion -= 1
        printer(f'Drank a healing Potion and healed {self.hit_points - current} Hit Points')
        return success, CombatAction([("Heal", heal_amount, "Holy")],"")

    @abstractmethod
    def att_def_adjust(self, item: 'Equipment'):
        '''Attack and Defense Power Adjustment from gear'''

    @abstractmethod
    def generate_weapon(self) -> Weapon:
        '''Generates a suitable Weapon Equipment Item for your Class and Level'''

    @abstractmethod
    def generate_armor(self) -> Armor:
        '''Generates a suitable Armor Equipment Item for your Class and Level'''

    @abstractmethod
    def generate_accessory(self) -> Accessory:
        '''Generates a suitable Accessory Equipment Item for your Class and Level'''

    def __str__(self):
        '''Prints the Character Sheet for the Character'''
        char_sheet = character_sheet(self)
        return char_sheet
