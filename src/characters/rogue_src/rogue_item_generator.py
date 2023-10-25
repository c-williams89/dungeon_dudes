'''Module for Dungeon Dudes Rogue class Equipment'''
from random import gauss, choice, randint
from math import ceil
from typing import Dict, Union, Tuple
from ..equipment import Weapon, Armor, Accessory
from ...dd_data import defensive_suffix_mapping


class RogueEquipmentGenerator:
    '''Equipment Generator for Rogue Class in Dungeon Dudes'''
    def __init__(self):
        self._defensive_suffix_mapping: Dict[tuple,
                                             str] = defensive_suffix_mapping
        self._weapons: list = ["Dagger"]
        self._weapon_prefix: Dict[int, str] = {
            10: "Sharpened", 20: "Rending", 30: "Brutal", 40: "Deadly",
            50: "Devastating"
        }

    @staticmethod
    def generate_value_mod(avg: int, std: int) -> Tuple[int, float]:
        '''Generates a value and the cost modification for that value'''
        value: int = int(gauss(avg, std))
        cost_mod: int = int(value / avg)
        value = int(value)
        return value, cost_mod

    @staticmethod
    def generate_value(base: Union[int, float], *mods: float) -> int:
        '''Generates Item value from base value and mods'''
        for mod in mods:
            base *= mod
        return ceil(base)

    def generate_weapon(self, level: int) -> Weapon:
        '''
        Generates a Weapon Object Appropriate for a Rogue based on their level
        '''
        weapon_base_cost: int = level * 3
        weapon_type: str = choice(self._weapons)

        attack_average: int = level
        attack, attack_cost_mod = self.generate_value_mod(
            attack_average, ceil(attack_average/2.5))
        attack = max(10, ceil(attack))

        physical_modifier_avg: int = level
        physical_modifier, physical_cost_modifier = self.generate_value_mod(
            physical_modifier_avg, ceil(physical_modifier_avg/5))

        # Over level 10
        if level >= 10:
            poison_modifier_avg: int = level // 2
            poison_modifier, poison_cost_modifier = self.generate_value_mod(
                poison_modifier_avg, ceil(poison_modifier_avg/5)
            )
        prefix_key: int = max(
            filter(lambda key: key < physical_modifier,
                   self._weapon_prefix.keys()), default=0)
        if prefix_key == 0:
            prefix: str = ""
        else:
            prefix = self._weapon_prefix[prefix_key]
        armor: int = 0
        suffix: str = ""
        suffix_chance: int = randint(1, 5)
        armor_mod: float = 1
        wrath_mod: float = 1
        if suffix_chance == 5:
            armor += ceil(gauss(level/2, level/5))
            suffix = "of Defense"
            armor_mod = 1.5
        elif suffix_chance > 2:
            attack += ceil(gauss(level/2, level/5))
            suffix = "of Wrath"
            wrath_mod = 1.5
        if level >= 10:
            cost: int = self.generate_value(weapon_base_cost,
                                            attack_cost_mod,
                                            physical_cost_modifier,
                                            poison_cost_modifier,
                                            armor_mod,
                                            wrath_mod)
        else:
            cost = self.generate_value(weapon_base_cost,
                                       attack_cost_mod,
                                       physical_cost_modifier,
                                       armor_mod,
                                       wrath_mod)
        cost = max(cost, 1)
        weapon_name: str = f'{prefix} {weapon_type} {suffix}'.strip()
        if level >= 10:
            weapon_special: dict = {"Offensive":
                                    [("Physical", physical_modifier),
                                     ("Poison", poison_modifier)]}
        else:
            weapon_special = {"Offensive":
                              [("Physical", physical_modifier)]}
        return Weapon(weapon_type, weapon_name, attack, special=weapon_special,
                      armor=armor, cost=cost)

    def generate_armor(self, level: int) -> Armor:
        '''
        Generates an Armor Object Appropriate for a Rogue based on their level
        '''
        armor_base_cost: int = ceil(level * 2.5)
        armor_type: str = "Medium"
        armor_name: str = "Hide"

        armor_average: int = ceil(0.85 * level)
        armor, armor_cost_mod = self.generate_value_mod(armor_average,
                                                        int(armor_average/2.5))
        armor = max(10, ceil(armor) + 8)
        attack: int = 0

        modifiers, suffix = choice(
            list(self._defensive_suffix_mapping.items()))
        modifier_amount: int = 20 + (level * 2)
        mod_1: int = randint(0, modifier_amount)
        mod_2: int = modifier_amount - mod_1
        mod_1 = 0 - mod_1
        mod_2 = 0 - mod_2
        prefix: str = ""
        prefix_chance: int = randint(1, 5)
        fortified_cost_mod: float = 1
        attack_cost_mod: float = 1
        if prefix_chance >= 4:
            armor += max(1, ceil(gauss(level/2, level/5)))
            prefix = "Fortified"
            fortified_cost_mod = 1.5
        elif prefix_chance == 3:
            attack += max(1, ceil(gauss(level/2, level/5)))
            prefix = "Powerful"
            attack_cost_mod = 1.5

        cost: int = self.generate_value(armor_base_cost, armor_cost_mod,
                                        fortified_cost_mod, attack_cost_mod)
        cost = max(cost, 1)
        armor_name = f'{prefix} {armor_name} of {suffix}'.strip()
        armor_special: dict = {"Defensive": [(modifiers[0], mod_1),
                                             (modifiers[1], mod_2)]}
        return Armor(armor_type, armor_name,
                     armor=armor, special=armor_special,
                     attack=attack, cost=cost)

    def generate_accessory(self, level: int) -> Accessory:
        '''
        Generates an Armor Object Appropriate for a Rogue based on their level
        '''
        accessory_base_cost: int = level * 2
        accessory_type: str = "Thieves Tools"
        accessory_name: str = accessory_type

        armor_average: int = ceil(0.5 * level) + 3
        armor: int = 0
        armor_cost_mod: float = 0
        armor, armor_cost_mod = self.generate_value_mod(armor_average,
                                                        int(armor_average/2.5))
        armor = max(0, ceil(armor))

        attack_average: int = ceil(0.75 * level) + 10
        attack, attack_cost_mod = self.generate_value_mod(
            attack_average, ceil(attack_average/2.5))
        attack = max(0, attack)

        modifiers, suffix = choice(list(self._defensive_suffix_mapping.items()
                                        ))
        modifier_amount: int = 20 + (level * 2)
        mod_1: int = randint(0, modifier_amount)
        mod_2: int = modifier_amount - mod_1
        mod_1 = 0 - mod_1
        mod_2 = 0 - mod_2
        prefix_mod: float = 1
        defense_special = [(modifiers[0], mod_1), (modifiers[1], mod_2)]
        offense_special: list = []
        prefix = ""
        prefix_chance = randint(1, 4)
        off_mod: str = ""
        new_mod: str = ""
        if prefix_chance == 1:
            new_mod = "Physical"
            defense_special.append((new_mod, 0 - (level // 2 + 10)))
            prefix = "Hardened"
            prefix_mod = 2
        elif prefix_chance == 2:
            off_mod = "Physical"
            offense_special.append((off_mod, ceil(level * 0.3)))
            prefix = "Aggressive"
            prefix_mod = 1.5
        elif prefix_chance == 3:
            off_mod = "Poison"
            offense_special.append((off_mod, ceil(level * 0.3)))
            prefix = "Poisonous"
            prefix_mod = 1.5

        cost: int = self.generate_value(accessory_base_cost,
                                        attack_cost_mod,
                                        armor_cost_mod,
                                        prefix_mod)

        cost = max(cost, 1)
        accessory_name = f'{prefix} {accessory_name} of {suffix}'.strip()
        accessory_special = {"Attack": attack,
                             "Armor": armor,
                             "Offensive": offense_special,
                             "Defensive": defense_special}
        return Accessory(accessory_type, accessory_name,
                         accessory_special, cost=cost)
