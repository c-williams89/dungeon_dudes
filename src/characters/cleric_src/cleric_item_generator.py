from random import gauss, choice, randint
from math import ceil, floor
from typing import Dict
from ..equipment import Weapon, Armor, Accessory
from ...dd_data import defensive_suffix_mapping


class ClericEquipmentGenerator:
    '''Equipment Generator for Cleric Class in Dungeon Dudes'''
    def __init__(self):
        self._def_suffix_maps: Dict[tuple, str] = defensive_suffix_mapping
        self._weapons: list = ["Mace", "Flail"]
        self._weapon_prefix: Dict[int, str] = {
            10: "Sharpened", 20: "Rending", 30: "Brutal",
            40: "Deadly", 50: "Devastating"
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
        Generates a Weapon Object Appropriate for a Cleric based on level
        '''
        weapon_base_cost: int = level * 3
        weapon_type: str = choice(self._weapons)

        attack_average: int = level
        attack, atk_cost_mod = self.generate_value_mod(attack_average,
                                                       ceil(
                                                           attack_average/2.5))
        attack: int = max(10, ceil(attack) + 10)

        # Constants in case one-but-not-other modified in conditional
        holy_cost_modifier: int = 1
        phys_cost_modifier: int = 1

        if weapon_type == "Mace":
            physical_modifier_avg: int = level
            physical_modifier, phys_cost_modifier = self.generate_value_mod(
                physical_modifier_avg, ceil(physical_modifier_avg/5))

            prefix_key: [str, None] = max(filter(
                                        lambda key: key < physical_modifier,
                                        self._weapon_prefix.keys()),
                                        default=None)
            if prefix_key is None:
                prefix: str = ""
            else:
                prefix: str = self._weapon_prefix[prefix_key]

            weapon_special: dict = {"Offensive":
                                    [("Physical", physical_modifier)]}

        else:
            holy_modifier_avg: int = level
            holy_modifier, holy_cost_modifier = self.generate_value_mod(
                holy_modifier_avg, ceil(holy_modifier_avg/5))
            prefix_key: [str, None] = max(filter(
                                        lambda key: key < holy_modifier,
                                        self._weapon_prefix.keys()),
                                        default=None)
            if prefix_key is None:
                prefix: str = ""
            else:
                prefix: str = self._weapon_prefix[prefix_key]

            weapon_special: dict = {"Offensive":
                                    [("Holy", holy_modifier)]}

        armor: int = 0

        suffix: str = ""
        suffix_chance: int = randint(1, 5)
        armor_mod: int = 1
        wrath_mod: int = 1
        if suffix_chance == 5:
            armor += ceil(level/2)
            suffix: str = "of Defense"
            armor_mod: float = 1.5

        elif suffix_chance > 2:
            attack += ceil(level/2)
            suffix: str = "of Wrath"
            wrath_mod: float = 1.5

        cost: int = self.generate_value(weapon_base_cost, atk_cost_mod,
                                        phys_cost_modifier,
                                        holy_cost_modifier,
                                        armor_mod, wrath_mod)
        cost = max(cost, 1)
        weapon_name: str = f'{prefix} {weapon_type} {suffix}'.strip()
        return Weapon(weapon_type, weapon_name, attack, special=weapon_special,
                      armor=armor, cost=cost)

    def generate_armor(self, level: int) -> Armor:
        '''
        Generates an Armor Object Appropriate for a Cleric based on level
        '''
        armor_base_cost: int = ceil(level * 2.5)
        armor_type: str = "Heavy"
        armor_name: str = "Plate"

        armor_average: int = ceil(1.25 * level)
        armor, armor_cost_mod = self.generate_value_mod(armor_average,
                                                        armor_average/2.5)
        armor: int = max(10, ceil(armor) + 10)
        attack: int = 0

        modifiers, suffix = choice(list(self._def_suffix_maps.items()))
        modifier_amount: int = 20 + (level * 2)
        mod_1: int = randint(0, modifier_amount)
        mod_2: int = modifier_amount - mod_1
        mod_1: int = 0 - mod_1
        mod_2: int = 0 - mod_2
        prefix: str = ""
        prefix_chance: str = randint(1, 5)
        fortified_cost_mod: int = 1
        atk_cost_mod: int = 1
        if prefix_chance >= 4:
            armor += max(1, ceil(gauss(level/2, level/5)))
            prefix: str = "Fortified"
            fortified_cost_mod: float = 1.5
        elif prefix_chance == 3:
            attack += max(1, ceil(gauss(level/2, level/5)))
            prefix: str = "Powerful"
            atk_cost_mod: float = 1.5

        cost: int = self.generate_value(armor_base_cost, armor_cost_mod,
                                        fortified_cost_mod, atk_cost_mod)
        cost = max(cost, 1)
        armor_name: str = f'{prefix} {armor_name} of {suffix}'.strip()
        armor_special: dict = {"Defensive": [(modifiers[0], mod_1),
                                             (modifiers[1], mod_2)]}
        return Armor(armor_type, armor_name, armor=armor,
                     special=armor_special, attack=attack, cost=cost)

    def generate_accessory(self, level: int) -> Accessory:
        '''
        Generates the Accessory Object Appropriate for a Cleric
        '''
        accessory_base_cost: int = level * 2
        accessory_type: str = "Holy Symbol"
        accessory_name: str = accessory_type

        armor_average: int = level
        armor, armor_cost_mod = self.generate_value_mod(armor_average,
                                                        armor_average/2.5)
        armor: int = max(0, ceil(armor))

        attack_average: int = level
        attack, atk_cost_mod = self.generate_value_mod(attack_average,
                                                       ceil(attack_average/2.5)
                                                       )
        attack = max(0, attack)

        holy_modifier: int = level + 5
        offense_special = [("Holy", holy_modifier)]

        modifier_amount: int = 25 + (level * 2.5)
        defense_special = [
            ("Physical", 0 - int(modifier_amount // 3)),
            ("Holy", 0 - int(modifier_amount // 3)),
            ("Poison", 0 - int(modifier_amount // 3))
        ]
        modifiers, _ = choice(list(self._def_suffix_maps.items()))
        suffix = "Antioch"

        prefix_mod = 1
        prefix = ""
        prefix_chance = randint(1, 4)

        if prefix_chance > 2:
            damage_types: list = ["Fire", "Ice", "Lightning"]
            new_mod: str = choice([damage_type for damage_type in damage_types
                                  if damage_type not in modifiers])
            defense_special.append((new_mod, 0 - (10 + level)))
            prefix: str = "Resistant"
            prefix_mod: int = 2

        elif prefix_chance == 2:
            attack += ceil(gauss(level/4, level/5))
            prefix: str = "Powerful"
            prefix_mod: float = 1.5

        cost: int = self.generate_value(accessory_base_cost,
                                        atk_cost_mod, armor_cost_mod,
                                        prefix_mod)

        cost = max(cost, 1)
        accessory_name: str = f'{prefix} {accessory_name} of {suffix}'.strip()
        accessory_special = {"Attack": attack, "Armor": armor,
                             "Offensive": offense_special,
                             "Defensive": defense_special}
        return Accessory(accessory_type, accessory_name,
                         accessory_special, cost=cost)
