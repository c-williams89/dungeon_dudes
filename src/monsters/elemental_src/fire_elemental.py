'''Fire Elemental Module for Dungeon Dudes'''
from typing import Dict, Tuple
from random import choice, randint
from ..elemental import Elemental
from ...combat_action import CombatAction
from ...dd_data import LimitedDict


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
        elemental_type: tuple = self.spawn_elemental(
            level_mod, self.elemental_types)
        self._hit_points: int = self.stats_structure["Hit Points"][0]
        self._elemental_type: str = elemental_type[0]
        self._damage_type: str = elemental_type[1]
        super().__init__(self._elemental_type, level_mod, self.stats_structure)
        self._sub_type: str = "Fire"
        self._dam_modifiers = LimitedDict(
            ("Fire", (self._damage_type)), default_value=100)
        self._reconstitute_count = 0.0
        self._burning_strike_count = 0
        self._special_count = 0
        self._max_hit_points = self._hit_points
        self._options = [self.immolate]
        self._explode_once = False
        self._scorched_once = False

    def base_att_def_power(self):
        self._attack_power = self.strength + self.intelligence
        self._defense_power = self.agility

    def spawn_elemental(self, level_mod: int, elemental_types: list):
        ''' Spawns elemental based on character level '''
        if level_mod <= 5:
            print(f'{elemental_types[0]}')
            return elemental_types[0]
        if level_mod in range(6, 11):
            tier_2 = {6: 20,
                      7: 40,
                      8: 60,
                      9: 80,
                      10: 100}
            if randint(1, 100) <= tier_2.get(level_mod):
                return elemental_types[1]
            return elemental_types[0]
        if level_mod in range(11, 21):
            tier_3 = {
                11: 10,
                12: 20,
                13: 30,
                14: 40,
                15: 50,
                16: 60,
                17: 70,
                18: 80,
                19: 90,
                20: 100}
            if randint(1, 100) <= tier_3.get(level_mod):
                return elemental_types[2]
            else:
                return elemental_types[1]
        if level_mod >= 20:
            return elemental_types[2]
        if level_mod >= 25:
            if randint(1, 100) <= 1:
                return elemental_types[3]

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
        self._options.append("immolate")

    def level_up(self):
        super().level_up()
        if self.level % 2 == 0:
            self._attack_power += 1
        else:
            self._defense_power += 1
        if self.level >= 5:
            self._options.append(self.explode)
            self._options.append(self.scorched_earth)
        if self.level >= 11:
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
        if self._explode_once is False:
            self._hit_points = int(self._max_hit_points * .25)
            damage: int = int(self._hit_points * .25)
            message: str = f"{self.name} explodes for <value> Fire damage"
            self._explode_once = True
            return CombatAction([("Attack", damage, "Fire", message)], "")
        return self.attack()

    def improved_reconstitute(self):
        ''' passive: Greater Fire Elemental Reconstitute Healing is based on
            max_hit_points instead of current hit_points '''
        result = round(self._max_hit_points * 0.08)
        if self._hit_points < self._max_hit_points:
            pass
        # TODO: adjust for less than total but cannot overheal
        else:
            self._hit_points += result
            self.printer(f"{self.name} heals for {result}!")

    def burning_strike(self):
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
        damage: int = int(self.damage_modify(self._attack_power) * .75)
        message: str = (f"{self.name} immolates you in <value> Fire damage "
                        f"and increases its reconstituting abilities!")
        if self._reconstitute_count < 0.04:
            self._reconstitute_count += 0.01
        return CombatAction([("Attack", damage, "Fire", message)], "")

    def scorched_earth(self):
        ''' Once per Combat: Fire Elemental lights the area blaze, dealing 33%
            attack_power based Fire damage every time the Fire Elemental takes
            an action for the remainder of combat. '''
        if self._scorched_once is False:
            self._scorched_once = True
            self.printer((f"{self.name} lights the ground ablaze, continually "
                         f"dealing damage."))

    def scorched_earth_trigger(self):
        ''' Triggered damage if Scorched Earth is active '''
        if self._scorched_once is True:
            damage: int = int(self.damage_modify(self._attack_power) * .33)
            message: str = ((f"{self.name}'s scorched earth deals <value> Fire"
                             f" damage this time."))
            return CombatAction([("Attack", damage, "Fire", message)], "")

    def take_turn(self) -> CombatAction:
        ''' Fire Elemental has a 75% to Attack each turn and a 25% chance to
            return a random skill, until they have maxed out the benefit of
            Burning Strikes. When Burning Strikes reaches maximum benefit, Fire
            Elementals have a 75% chance to return a random skill, and a 25%
            chance to Attack. '''
        self.elemental_reconstitute()
        if randint(1, 100) <= 25:
            return choice(self._options)(), self.scorched_earth_trigger()
        # TODO: switch skill/attack for burning_strike counter
        return self.attack(), self.scorched_earth_trigger()
