'''Fire Elemental Module for Dungeon Dudes'''
from typing import Dict, Tuple
from random import choice, randint, random
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
        # elemental_type: tuple = choice(self.elemental_types)
        elemental_type: tuple = self.spawn_elemental(
            level_mod, self.elemental_types)
        self._hit_points: int = self.stats_structure["Hit Points"][0]
        self._elemental_type: str = elemental_type[0]
        self._damage_type: str = elemental_type[1]
        super().__init__(self._elemental_type, level_mod, self.stats_structure)
        self._sub_type: str = "Fire"
        self._dam_modifiers = LimitedDict(
            ("Fire", (self._damage_type)), default_value=100)
        self._reconstitute_count = 0
        self._burning_strike_count = 0
        self._special_count = 0
        self._max_hit_points = self._hit_points
        self._options = [self.attack]

    def base_att_def_power(self):
        self._attack_power = self.strength + self.intelligence
        self._defense_power = self.agility

    # def name(self):
    #     if level_mod <= 5:
        # self.name = "Lesser Fire Elemental"
    #     if self._level <=

    def spawn_elemental(self, level_mod, elemental_types: list):
        if level_mod <= 5:
            print(f'{elemental_types[0]}')
            return elemental_types[0]
        if level_mod in range(6, 11):
            tier_2 = {6: .2,
                      7: .4,
                      8: .6,
                      9: .8,
                      10: 1}
            if random() <= tier_2.get(level_mod):
                return elemental_types[1]
            else:
                return elemental_types[0]
        if level_mod in range(11, 21):
            tier_3 = {
                11: .1,
                12: .2,
                13: .3,
                14: .4,
                15: .5,
                16: .6,
                17: .7,
                18: .8,
                19: .9,
                20: 1}
            if random() <= tier_3.get(level_mod):
                return elemental_types[2]
            else:
                return elemental_types[1]
        if level_mod >= 20:
            return elemental_types[2]
        elif level_mod >= 25:
            if random() <= .01:
                return elemental_types[3]

    @property
    def damage_modifiers(self) -> LimitedDict:
        '''Getter for Damage Modifiers'''
        return self._dam_modifiers

    # @damage_modifiers.setter
    # def damage_modifiers(self, damage_enhancement: int) -> LimitedDict:
    #     ''' Setter for Damage Modifiers '''
    #     return self._dam_modifiers + damage_enhancement

    @property
    def defense_modifiers(self) -> LimitedDict:
        '''Getter for Defense Modifiers'''
        return self._def_modifiers

    def get_skills(self) -> Dict[str, 'function']:
        '''Get Skills Learned'''
        return {}

    def get_skills_list(self) -> list:
        '''Get List of Skills Learned'''
        self._options.append("burning_strike")
        self._options.append("immolate")

    def level_up(self):
        super().level_up()
        if self._level % 2 == 0:
            self._attack_power += 1
        else:
            self._defense_power += 1
        if self._level >= 5:
            self._options.append("explode")
        if self._level >= 11:
            self.elemental_reconstitute = self.improved_reconstitute

    def attack(self) -> CombatAction:
        '''Attack method for Fire Elemental '''
        damage: int = self.damage_modify(self._attack_power)
        message: str = f"{self.name} attacks with for <value> Fire damage"
        self.burning_strike()
        return CombatAction([("Attack", damage, "Fire", message)], "")

    def explode(self) -> CombatAction:
        ''' Once per battle: The Fire Elemental Explodes, dealing damage to
            itself equal to 25% its max_hit_points + 25% of its current
            hit_points and dealing an equal amount of Fire damage to their
            opponent.
        '''
        # TODO: add once per battle flag
        if self._level >= 5:
            self._max_hit_points = self._hit_points
            pass

    def improved_reconstitute(self) -> CombatAction:
        ''' passive: Greater Fire Elemental Reconstitute Healing is based on
            max_hit_points instead of current hit_points '''
        result = round(self._max_hit_points * 0.08)
        if self._hit_points < self._max_hit_points:
            pass
        # TODO: adjust for less than total but cannot overheal
        else:
            self._hit_points += result
            self.printer(f"{self.name} heals for {result}!")

    def burning_strike(self) -> CombatAction:
        ''' passive: Fire Elemental Attack increase their Fire damage offensive
            modifier by 5 for the remainder of combat in addition to the damage
            dealt.  This effect is capped at an increase of 20 '''
        # TODO: adjust to use damage_modifier correctly
        if self._burning_strike_count < 4:
            self.printer(f"Burning Strike increases {self.name}'s damage.")
            self._burning_strike_count += 1
            self._attack_power += self._burning_strike_count * 5

    def immolate(self) -> CombatAction:
        ''' Fire Elemental deals Fire damage to their opponent based on 75%
            attack_power. The next action the Fire Elemental takes also deals
            Fire damage to their opponent based on 50% of attack power. The
            effect of Reconstitute is increased by 1% for the remainder of
            the battle. (Maximum increase 4%) '''
        print("Using immolate")
        if self._reconstitute_count < 0.04:
            self._reconstitute_count += 0.01

    def scorched_earth(self) -> CombatAction:
        ''' Once per Combat: Fire Elemental lights the area blaze, dealing 33%
            attack_power based Fire damage every time the Fire Elemental takes
            an action for the remainder of combat. '''
        # TODO: add once per battle flag
        pass

    def take_turn(self) -> CombatAction:
        ''' Fire Elemental has a 75% to Attack each turn and a 25% chance to
            return a random skill, until they have maxed out the benefit of
            Burning Strikes. When Burning Strikes reaches maximum benefit, Fire
            Elementals have a 75% chance to return a random skill, and a 25%
            chance to Attack. '''
        self.elemental_reconstitute()
        return choice(self._options)()
