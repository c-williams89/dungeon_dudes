from random import gauss, choice, randint
from math import ceil
from typing import Dict
from ..equipment import Weapon, Armor, Accessory
from ...dd_data import defensive_suffix_mapping

class WizardEquipmentGenerator:
    '''Equipment Generator for Fighter Class in Dungeon Dudes'''
    def __init__(self):
        self._defensive_suffix_mapping : Dict[tuple, str]= defensive_suffix_mapping
        self._weapons : list = ["Staff", "Wand"]
        self._elemental_types = ["Fire", "Ice", "Lightning"]
        self._weapon_prefix : Dict[int, str] = {
            10: "Sharpened", 20: "Rending", 30: "Brutal", 40: "Deadly", 50 : "Devastating"
        }

    @staticmethod
    def generate_value_mod(avg : int, std : int) -> [int, float]:
        '''Generates a value and the cost modification for that value'''
        value : int = gauss(avg, std)
        cost_mod : int = value/avg
        value = int(value)
        return value, cost_mod

    @staticmethod
    def generate_value(base : [int,float], *mods : float) -> int:
        '''Generates Item value from base value and mods'''
        for mod in mods:
            base *= mod
        return ceil(base)

    def generate_weapon(self, level: int) -> Weapon:
        '''
        Generates a Weapon Object Appropriate for a Wizard based on their level
        '''
        weapon_type = choice(self._weapons)

        # Generate attack power approximately 25% of the wizard's level (rounded up)
        attack = max(1, ceil(level * 0.25))

        # Generate a random elemental damage type (Fire, Ice, or Lightning)
        elemental_damage_type = choice(self._elemental_types)

        # Generate a modifier for the elemental damage approximately equal to the wizard's level
        elemental_damage_modifier = randint(level - 2, level + 2)

        # Generate a defense power or additional damage modifier approximately half of the wizard's level
        modifier = ceil(level * 0.5)

        weapon_name = f"{weapon_type} of {elemental_damage_type}"
        weapon_special = {"Offensive": [(elemental_damage_type, attack + elemental_damage_modifier)]}
        armor = 0
        cost = randint(level * 3, level * 5)  # Adjust the cost range as needed

        # Add defense power or additional damage modifier to the weapon
        if randint(0, 1) == 0:
            weapon_name += f" (+{modifier} Defense)"
            armor = modifier
        else:
            weapon_name += f" (+{modifier} {elemental_damage_type})"
            weapon_special["Offensive"].append((elemental_damage_type, modifier))

        return Weapon(weapon_type, weapon_name, attack, special=weapon_special, armor=armor, dmg_type=elemental_damage_type, cost=cost)

    def generate_armor(self, level : int) -> Armor:
        '''
        Generates an Armor Object Appropriate for a Wizard based on their level
        '''
        armor_type = "Robes"
        armor_name = "Robes of"

        # Calculate defense power approximately 0.5 times the wizard's level + 5
        defense_power = max(10, ceil(level * 0.5) + 5)

        # Choose 3 non-Physical damage types randomly
        defensive_modifiers = []
        for _ in range(3):
            damage_type = choice(self._elemental_types)
            modifier_value = 30 + (level * 3)
            defensive_modifiers.append((damage_type, modifier_value))

        # Generate additional defense modifier or defense power with a chance
        descriptor = ""
        desc_chance = randint(1, 5)
        if desc_chance >= 4:
            defense_power += max(1, ceil(gauss(level / 2, level / 5)))
            descriptor = "Fortification"
        elif desc_chance == 3:
            modifier_value = 30 + (level * 3)
            damage_type = choice(self._elemental_types)
            defensive_modifiers.append((damage_type, modifier_value))
            descriptor = "Empowerment"

        # Adjust the cost range 
        cost = randint(level * 2, level * 4)  
        cost = max(cost, 1)

        armor_name = f'{armor_name} {descriptor}'.strip()
        armor_special = {"Defensive": defensive_modifiers}
        return Armor(armor_type, armor_name, defense_power, special=armor_special, cost=cost)

    def generate_accessory(self, level: int) -> Accessory:
        '''
        Generates an Armor Object Appropriate for a Fighter based on their level
        '''
        accessory_type = "Arcane Orb"
        accessory_name = accessory_type

        # Calculate offensive modifiers for 1 Elemental damage type (Fire, Ice, Lightning)
        damage_type = choice(self._elemental_types)
        offensive_modifiers = [(damage_type, level + 20)]

        # Calculate defensive modifiers for 3 damage types with approximately 30 + (level * 3) modification value
        defensive_modifiers = []
        for _ in range(3):
            damage_type = choice(["Fire", "Ice", "Lightning", "Holy", "Poison"])
            modifier_value = 30 + (level * 3)
            defensive_modifiers.append((damage_type, modifier_value))

        # Add additional bonuses to offensive or defensive modifiers with a chance
        prefix = ""
        prefix_chance = randint(1, 4)
        modifier_bonus = 0
        if prefix_chance > 2:
            bonus_damage_type = choice(["Fire", "Ice", "Lightning"])
            modifier_bonus = level * 0.25
            offensive_modifiers.append((bonus_damage_type, modifier_bonus))
            prefix = "Resistant"
        elif prefix_chance == 2:
            offensive_modifiers[0] = (offensive_modifiers[0][0], offensive_modifiers[0][1] + ceil(gauss(level / 2, level / 5)))
            prefix = "Powerful"
        else:
            defensive_modifiers[0] = (defensive_modifiers[0][0], defensive_modifiers[0][1] + ceil(gauss(level / 2, level / 5)))
            prefix = "Fortified"

        cost = randint(level * 2, level * 4)  # Adjust the cost range as needed
        cost = max(cost, 1)

        accessory_name = f'{prefix} {accessory_name} of {damage_type}'.strip()
        accessory_special = {"Offensive": offensive_modifiers, "Defensive": defensive_modifiers, "Attack": 0, "Armor": 0}
        return Accessory(accessory_type, accessory_name, accessory_special, cost=cost)
