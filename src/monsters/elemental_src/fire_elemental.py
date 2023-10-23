'''Fire Elemental Module for Dungeon Dudes'''
from typing import Dict, Tuple
from random import choice, randint
from ..elemental import Elemental
from ...combat_action import CombatAction
from ...dd_data import CombatPrint, LimitedDict, damage_types


class FireElemental(Elemental):
    '''Fire Elemental Module'''
    stats_structure: Dict[str, Tuple[int]] = {"Hit Points": (65, 16),
                                              "Strength": (10, 2),
                                              "Agility": (10, 3),
                                              "Intelligence": (5, 1),
                                              "Special": (0, 0)}
    elemental_types = [("Lesser Fire Elemental", "Fire"),
                       ("Fire Elemental", "Fire "),
                       ("Greater Fire Elemental", "Fire"),
                       ("Fire Elemental Lord", "Fire")]

    def __init__(self, level_mod: int):
        elemental_type: tuple = choice(self.elemental_types)
        self._hit_points: int = self.stats_structure["Hit Points"][0]
        self._elemental_type: str = elemental_type[0]
        self._damage_type: str = elemental_type[1]
        super().__init__(self._elemental_type, level_mod, self.stats_structure)
        self._sub_type: str = "Fire"
        self._dam_modifiers = LimitedDict(
            ("Fire", (self._damage_type)), default_value=100)
        self._reconstitute_value = 0
        self._special_count = 0

    def base_att_def_power(self):
        self._attack_power = self.strength + self.intelligence
        self._defense_power = self.agility

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
        special_skills = {"Lesser": "Explode",
                          "Greater": "Improved Reconstitute"}
        return [f'{self._damage_type} Empowerment',
                special_skills[self._griffon_type]]

    def explode(self) -> CombatAction:
        ''' Once per battle: The Fire Elemental Explodes, dealing damage to
            itself equal to 25% its max_hit_points + 25% of its current
            hit_points and dealing an equal amount of Fire damage to their
            opponent.
        '''
        self._hit_points = self._hit_points
        pass

    def improved_reconstitute(self) -> CombatAction:
        ''' passive: Greater Fire Elemental Reconstitute Healing is based on
            max_hit_points instead of current hit_points '''
        pass

    def burning_strike(self) -> CombatAction:
        ''' passive: Fire Elemental Attack increase their Fire damage offensive
            modifier by 5 for the remainder of combat in addition to the damage
            dealt.  This effect is capped at an increase of 20 '''
        pass

    def immolate(self) -> CombatAction:
        ''' Fire Elemental deals Fire damage to their opponent based on 75%
            attack_power. The next action the Fire Elemental takes also deals
            Fire damage to their opponent based on 50% of attack power. The
            effect of Reconstitute is increased by 1% for the remainder of
            the battle. (Maximum increase 4%) '''
        pass

    def scorched_earth(self) -> CombatAction:
        ''' Once per Combat: Fire Elemental lights the area blaze, dealing 33%
            attack_power based Fire damage every time the Fire Elemental takes
            an action for the remainder of combat. '''
        pass

    def take_turn(self) -> CombatAction:
        ''' Fire Elemental has a 75% to Attack each turn and a 25% chance to
            return a random skill, until they have maxed out the benefit of
            Burning Strikes. When Burning Strikes reaches maximum benefit, Fire
            Elementals have a 75% chance to return a random skill, and a 25%
            chance to Attack. '''
        # if self > level_11:
        # do improved reconstitute
        # else:
        # do reconstitute
        options = [self.attack, self.special_skill]
        return choice(options)()
