'''Module for the Dungeon Dudes Drake Monster'''
from typing import Dict, Tuple
from random import choice
from ..beast import Beast
from ...dd_data import LimitedDict
from ...combat_action import CombatAction

class Drake(Beast):
    '''Drake Beast Class'''
    stats_structure : Dict[str, Tuple[int]] = {"Hit Points": (65, 14), "Strength": (16, 3),
                        "Agility" : (12, 3), "Intelligence" : (5, 1), "Special" : (0,0)}
    drake_types = [("Storm", "Lightning"), ("Green", "Fire"), ("Swamp", "Poison")]

    def __init__(self, level_mod : int):
        drake_type : tuple = choice(self.drake_types)
        self._hit_points : int = self.stats_structure["Hit Points"][0]
        self._drake_type : str = drake_type[0]
        self._damage_type : str = drake_type[1]
        super().__init__(f'{self._drake_type} Drake',
                         level_mod, self.stats_structure)
        self._sub_type : str = "Drake"
        self._dam_modifiers = LimitedDict(("Physical", (self._damage_type)), default_value=100)
        self._def_modifiers[self._damage_type] -= 40

    @property
    def damage_modifiers(self) -> LimitedDict:
        '''Getter for Damage Modifiers'''
        return self._dam_modifiers

    @property
    def defense_modifiers(self) -> LimitedDict:
        '''Getter for Defense Modifiers'''
        return self._def_modifiers

    def get_skills(self) -> Dict[str, 'function']:
        '''Get Skills Learned'''
        return {}

    def get_skills_list(self) -> list:
        '''Get List of Skills Learned'''
        special_skills = {"Storm": "Lightning Strikes",
                          "Swamp": "Poison Cloud",
                          "Green": "Fiery Fortification"}
        return [f'{self._damage_type} Breath', special_skills[self._drake_type]]

    def lightning_strikes(self) -> CombatAction:
        '''
        Attacks for 3/4 normal damage and then follows 
        up with intelligence based lightning damage
        '''
        phys_dmg : int = int(self.attack().actions[0][1] * 0.75)
        lightning_dmg : int = self.beast_damage(self.modify_damage(self.intelligence))
        msg_1 : str = "Storm Drake strikes with its claws, dealing <value> physical damage."
        msg_2 : str = "Storm Drake's claws shock you for an additional <value> lightning damage."
        return CombatAction([("Attack", phys_dmg, "Physical", msg_1),
                             ("Attack", lightning_dmg, "Lightning", msg_2)], "")

    def poison_cloud(self) -> CombatAction:
        '''
        Lowers Poison and Physical Resists and deals Poison damage
        based on Intelligence
        '''
        poison_dmg : int = self.beast_damage(self.modify_damage(self.intelligence))
        msg : str = ("Swamp drain emits a poison cloud, lowering your" +
                       " resistances and dealing <value> poison damage")
        return CombatAction([("Hex", 15, "Poison", ""), 
                             ("Hex", 10, "Physical", ""),
                             ("Attack", poison_dmg, "Poison", msg)], "")

    def fiery_fortification(self) -> CombatAction:
        '''
        Increases Attack Power and Defense Power
        Deals Small Amount of Fire Damage
        '''
        fire_dmg : int = self.beast_damage(self.modify_damage(self.intelligence))
        msg : str = ("Green Drake surrounds itself in flame, increasing its offensive" +
                       " and defensive abilities and dealing <value> fire damage")
        self._attack_power += int(self.intelligence // 4)
        self._defense_power += int(self.intelligence // 4)
        return CombatAction([("Attack", fire_dmg, "Fire", msg)], "")

    def special_skill(self) -> CombatAction:
        '''Returns special attack per Drake type'''
        if self._drake_type == "Storm":
            return self.lightning_strikes()
        elif self._drake_type == "Swamp":
            return self.poison_cloud()
        return self.fiery_fortification()

    def breath(self) -> CombatAction:
        '''Breath Attack Deals Damage Based on Current HP and Intelligence'''
        message : str = (f"{self.name} breathes {self._damage_type}"
                         f" for <value> {self._damage_type} damage")
        damage : int = self.beast_damage(self.modify_damage(
            self.hit_points // 2 + self.intelligence))
        return CombatAction([("Attack", damage, self._damage_type, message)],"")

    def take_turn(self) -> CombatAction:
        '''Takes turn and returns the action'''
        options = [self.attack, self.breath, self.special_skill]
        return choice(options)()
