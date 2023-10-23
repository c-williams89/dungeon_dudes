"""Module for the Dungeon Dudes Wizard Class"""
from typing import Dict, Tuple, List
from random import gauss, randint
from math import floor
from .character_abc import Character
from ..combatant_abc import Combatant
from .equipment import Equipment, Weapon, Armor, Accessory
from ..dd_data import LimitedDict, damage_types, CombatPrint
from ..combat_action import CombatAction
# TODO: from .wizard_src import WizardEquipmentGenerator

class Wizard(Character):
    '''Wizard Class for Dungeon Dudes'''
    stats_structure : Dict[str, Tuple[int]]= {"Hit Points": (60, 12), "Strength": (5, 0),
                        "Agility" : (10, 2), "Intelligence" : (17, 2), "Special": (50,20)}
    item_compatibility : list = ["Staff", "Wand", "Robes", "Arcane Orb"]
    def __init__(self, name : str):
        self.damage_types = damage_types
        
        self.skills_dict : Dict[int, List[str, 'function']] = {
            2 : ["Blink", self.blink],
            3 : ["Blizzard", self.blizzard],
            8 : ["Lightning Bolt", self.lightning_bolt],
            13 : ["Reflect Damage", self.reflect_damage],
            20 : ["Mana Burn", self.mana_burn]
        }
        mana_regeneration = '''Passive: You've regained 15 percent of your'''\
            '''mana.'''
        elemental_affinity = '''Passive: You've gained a 25 percent damage'''\
            '''boost to your bext elemental attack'''
        improved_passives = '''Passive: 25 percent of your armors'''\
            '''non-physical damage modifier now applies to your physical'''\
                '''damage'''
        elemental_master = '''Passive: You now deal +50 percent damage if'''\
            '''you've dealt fire, ice, and lightning damage this combat'''
            
        self.passive_skills = {
            5 : ["Mana Regeneration", mana_regeneration],
            10 : ["Elemental Affinity", elemental_affinity], 
            17 : ["Improved Passives", improved_passives],
            25 : ["Elemental Master", elemental_master]
        }
        
        self.printer = CombatPrint()
        self._weapon : Weapon = None
        self._armor : Armor = None
        self._accessory : Accessory = None
        self._def_modifiers = LimitedDict(self.damage_types, default_value=100)
        self._dam_modifiers = LimitedDict("Elemental", default_value=100)
        
        # TODO: Create equipment generator for wizard
        self._equipment_generator = WizardEquipmentGenerator()
        super().__init__(name, "Wizard", self.stats_structure, self.item_compatibility)
        self._exp_to_next_iter = iter([(50 * i ** 2) for i in range(1, 50)])
        self._exp_to_next : int = next(self._exp_to_next_iter)
        self._hit_points : int = self.stats_structure["Hit Points"][0]
        self._special : int = 1
        self._special_resource : str = "Mana"
        self._accessory_type : str = "Arcane Orb"
        self._critical_modifier : int = 1

        