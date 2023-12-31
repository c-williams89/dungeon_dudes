'''Frost Elemental Module for Dungeon Dudes'''
from typing import Dict, Tuple
from random import choice, random, randint
from ..elemental import Elemental
from ...combat_action import CombatAction
from ...dd_data import LimitedDict


class FrostElemental(Elemental):
    '''Frost Elemental Module'''
    stats_structure: Dict[str, Tuple[int]] = {"Hit Points": (78, 16),
                                              "Strength": (5, 1),
                                              "Agility": (12, 4),
                                              "Intelligence": (10, 2),
                                              "Special": (0, 0)}
    elemental_types = [("Frost Elemental", "Ice"),
                       ("Frost Elemental Lord", "Ice")]

    def __init__(self, level_mod: int):
        elemental_type: tuple = self.spawn_elemental(
            level_mod, self.elemental_types)
        self._hit_points: int = self.stats_structure["Hit Points"][0]
        self._max_hit_points: int = self._hit_points
        self._elemental_type: str = elemental_type[0]
        self._damage_type: str = elemental_type[1]
        super().__init__(self._elemental_type, level_mod, self.stats_structure)
        self._sub_type: str = "Ice"
        self._dam_modifiers = LimitedDict(
            ("Ice", (self._damage_type)), default_value=100)
        self._special_count = 0
        self._brittle_count = 0
        self._options = [self.brittle_strikes, self.freeze]

    def spawn_elemental(self, level_mod: int, elemental_types: list):
        ''' Spawns elemental based on character level '''
        if level_mod >= 25:
            increased_odds = level_mod - 25
            base_value = .0
            lord_chance = .01
            for n in range(increased_odds):
                base_value += lord_chance
            if random() <= lord_chance:
                return elemental_types[1]
        return elemental_types[0]

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

    def get_skills_list(self):
        '''Get List of Skills Learned'''
        self._options = ["brittle_strikes", "freeze"]

    def level_up(self):
        super().level_up()
        if self.level % 2 == 0:
            self._attack_power += 1
        else:
            self._defense_power += 1
        if self.level >= 5:
            self._options.append(self.blizzard)
        if self.level >= 10:
            self._options.append(self.frost_splinter)
        if self.level >= 15:
            self._options.append(self.improved_blizzard)
        if self.level >= 20:
            self._options.append(self.improved_frost_splinter)

    def attack(self) -> CombatAction:
        '''Attack method for Fire Elemental '''
        damage: int = self.damage_modify(self._attack_power)
        message: str = f"{self.name} attacks with for <value> Ice damage"
        return CombatAction([("Attack", damage, "Ice", message)], "")

    def brittle_strikes(self):
        ''' passive: Frost Elemental Attack reduces their opponents defensive
            modifier to Ice by 5 in addition to the damage dealt.  This effect
            is capped at a reduction of 25.
        '''
        pass

    def freeze(self) -> CombatAction:
        ''' Frost Elemental pulses a wave of Ice dealing 75% attack_power based
            Ice damage and improve the Frost Elementals defensive modifier to
            Physical damage by 10 for the remainder of the encounter.
            (Maximum improvement of 30)
        '''
        damage: int = self.damage_modify(self._attack_power) * .75
        message: str = (f"{self.name} pulses a wave of freezing Ice for "
                        f"<value> damage and increases its defense to Physical"
                        f" damage.")
        # TODO: add defense reduction modification
        return CombatAction([("Attack", damage, "Ice", message)], "")

    def blizzard(self) -> CombatAction:
        ''' Once per Combat: Frost Elemental Summons a Blizzard, which deals
            10% of the Frost Elementals current hit_points in Ice damage each
            turn and heals the Frost Elemental for 6% max_hit_points per turn.
            The blizzard lasts for the Frost Elementals next 3 attacks when
            cast.
        '''
        pass

    def improved_freeze(self) -> CombatAction:
        ''' passive:  After the defensive Physical modifier for Freeze reaches
            its maximum effect, subsequent casts of Freeze deal twice as much
            damage.
        '''
        pass

    def frost_splinter(self) -> CombatAction:
        ''' once per combat: Frost Elemental splints a piece of itself,
            summoning an Lesser Frost Elemental which attacks immediately for
            33% attack_power based damage. The Lesser Frost Elemental attacks
            every time the Frost Elemental takes an action for the remainder of
            the encounter.
        '''
        pass

    def improved_blizzard(self) -> CombatAction:
        ''' passive: Blizzard now lasts for 5 turns, deals damage based on 10%
            max_hit_points instead of current hit_points, heals for the same
            amount, and increases Lesser Frost Elemental Damage by 25% while
            it is active.
        '''
        pass

    def improved_frost_splinter(self) -> CombatAction:
        ''' passive Frost Splinter can now be cast twice per combat
        '''
        pass

    def take_turn(self) -> CombatAction:
        ''' Frost Elemental has a 60% to Attack each turn and a 40% chance to
            return a random skill, until they have maxed out the benefit of
            Brittle Strikes.  When Brittle Strikes reaches maximum benefit,
            Frost Elementals have a 75% chance to return a random skill, and a
            25% chance to Attack.
        '''
        self.elemental_reconstitute()
        # if randint(1, 100) <= 40:
        #     return choice(self._options)()
        # else:
        #     return self.attack()
        return self.attack()
