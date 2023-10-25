from random import gauss, choice, randint
from math import ceil
from typing import Dict
from ..equipment import Weapon, Armor, Accessory
from ...dd_data import defensive_suffix_mapping


class RangerEquipmentGenerator:
    '''Equipment Generator for Fighter Class in Dungeon Dudes'''
    def __init__(self):
        self._defensive_suffix_mapping: Dict[tuple, str] = \
            defensive_suffix_mapping
        self._weapons: list = ["Bow"]
        self._weapon_prefix: Dict[int, str] = {
            10: "Long", 20: "Heavy",
            30: "Deadly", 40: "Vicious", 50: "Hellfire"
        }

    @staticmethod
    def generate_value_mod(avg: int, std: int) -> [int, float]:
        '''Generates a value and the cost modification for that value'''
        value: int = gauss(avg, std)
        cost_mod: int = value/avg
        value = int(value)
        return value, cost_mod

    @staticmethod
    def generate_value(base: [int, float], *mods: float) -> int:
        '''Generates Item value from base value and mods'''
        for mod in mods:
            base *= mod
        return ceil(base)

    def generate_weapon(self, level: int) -> Weapon:
        '''
        Generates a Weapon Object Appropriate for a Ranger based on their level
        '''
        weapon_base_cost: int = level * 3
        weapon_type: str = choice(self._weapons)

        attack_average: int = level
        attack, attack_cost_mod = self.generate_value_mod(attack_average,
                                                          attack_average/2.5)
        attack: int = max(10, ceil(attack) + 20)

        physical_modifier_avg: int = level + 10
        physical_modifier, physical_cost_modifier = self.generate_value_mod(
            physical_modifier_avg, ceil(physical_modifier_avg / 5))
        physical_modifier = max(10, physical_modifier)
        prefix_key: [str, None] =\
            max(filter(lambda key: key < physical_modifier,
                       self._weapon_prefix.keys()), default=None)
        if prefix_key is None:
            prefix: str = ""
        else:
            prefix: str = self._weapon_prefix[prefix_key]
        armor: int = 0
        suffix: str = ""
        suffix_chance: int = randint(1, 5)
        mod: int = 1
        if suffix_chance == 5:
            armor += int(level * 0.5)
            suffix: str = "of Defense"
            mod: float = 1.5
        elif suffix_chance > 2:
            attack += int(level * 0.5)
            suffix: str = "of Wrath"
            mod: float = 1.5
        cost: int = self.generate_value(weapon_base_cost,
                                        attack_cost_mod,
                                        physical_cost_modifier, mod)
        cost = max(cost, 1)
        weapon_name: str = f'{prefix} {weapon_type} {suffix}'.strip()
        weapon_special: dict = {"Offensive":
                                [("Physical", physical_modifier)]}
        return Weapon(weapon_type, weapon_name, attack, special=weapon_special,
                      armor=armor, cost=cost)

    def generate_armor(self, level: int) -> Armor:
        '''
        Generates an Armor Object Appropriate for a Fighter based
        on their level'''
        armor_base_cost: int = ceil(level * 2.5)
        armor_type: str = "Light"
        armor_name: str = "Leather"
        resist_modifiers: tuple = ['Fire', 'Ice', 'Lightning',
                                   'Poison', 'Holy']
        defensive_suffix: Dict[tuple, str] = {
            ("Fire", "Holy"): "Sacred Flame",
            ("Fire", "Poison"): "Toxic Ember",
            ("Ice", "Holy"): "Divine Frost",
            ("Ice", "Poison"): "Venomous Chill",
            ("Lightning", "Holy"): "Holy Thunder",
            ("Lightning", "Poison"): "Toxic Shock",
            }
        armor_average: int = ceil(0.65 * level)
        armor, armor_cost_mod = self.generate_value_mod(armor_average,
                                                        armor_average/2.5)
        armor: int = max(10, ceil(armor) + 10)
        attack: int = 0
        # Elemental Defensive Modifier
        modifiers, suffix = \
            choice(list(defensive_suffix.items()))
        modifier_amount: int = 30 + (level * 3)
        mod_1: int = randint(1, modifier_amount - 2)
        mod_2: int = randint(1, modifier_amount - 1 - mod_1)
        mod_3: int = modifier_amount - mod_1 - mod_2
        remaining_resist = list(set(resist_modifiers) - set(modifiers))
        mod_3_resist = choice(remaining_resist)
        # Additional Bonus for defense power or attack power
        prefix: str = ""
        prefix_chance: str = randint(1, 5)
        prefix_mod = 1
        fortified_cost_mod: int = 1
        if prefix_chance >= 4:
            armor += int(level * 0.5)
            prefix: str = "Fortified"
            fortified_cost_mod: float = 1.5
        elif prefix_chance == 3:
            attack += int(level * 0.5)
            prefix: str = "Powerful"
            fortified_cost_mod: float = 1.5

        cost: int = self.generate_value(armor_base_cost,
                                        armor_cost_mod,
                                        fortified_cost_mod,
                                        prefix_mod)
        cost = max(cost, 1)
        armor_name: str = f'{prefix} {armor_name} of {suffix}'.strip()
        armor_special: dict = {"Defensive": [(modifiers[0], mod_1),
                                             (modifiers[1], mod_2),
                                             (mod_3_resist, mod_3)]}
        return Armor(armor_type, armor_name, armor=armor,
                     special=armor_special,
                     attack=attack, cost=cost)

    def generate_accessory(self, level: int) -> Accessory:
        '''
        Generates an Armor Object Appropriate for a Fighter based on
        their level'''
        accessory_base_cost: int = level * 2
        accessory_type: str = "Quiver"
        accessory_name: str = accessory_type
        accessory_element: list = ['Ice', 'Fire', 'Lightning']
        armor_average: int = ceil(0.5 * level) + 3
        armor, armor_cost_mod = self.generate_value_mod(armor_average,
                                                        armor_average/2.5)
        armor: int = max(0, ceil(armor))

        attack_average: int = ceil(0.5 * level) + 3
        attack, attack_cost_mod = \
            self.generate_value_mod(attack_average, ceil(attack_average/2.5))
        attack = max(0, attack)
        # Additional Bonus for defense power or attack power
        prefix_mod = 1
        prefix: str = ""
        suffix: str = choice(accessory_element)
        prefix_chance: str = randint(1, 5)
        armor: int = 0
        attack: int = 0
        attack_cost_mod: int = 1
        if prefix_chance >= 4:
            armor += int(level * .5)
            prefix: str = "Fortified"
            attack_cost_mod: float = 1.5
        elif prefix_chance == 3:
            attack += int(level * .5)
            prefix: str = "Powerful"
            attack_cost_mod: float = 1.5

        cost: int = self.generate_value(accessory_base_cost, armor_cost_mod,
                                        attack_cost_mod, prefix_mod)
        cost = max(cost, 1)
        accessory_name: str = f'{prefix} {accessory_name} of {suffix}'.strip()
        accessory_special = {"Attack": attack, "Armor": armor,
                             "Offensive": [], "Defensive": []}
        item = Accessory(accessory_type, accessory_name,
                         accessory_special, cost=cost)
        item.element = suffix
        return item
