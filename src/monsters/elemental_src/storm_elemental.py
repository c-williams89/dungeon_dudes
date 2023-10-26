'''Storm Elemental Module for Dungeon Dudes'''
from typing import Dict, Tuple
from random import choice, randint, random
from ..elemental import Elemental
from ...combat_action import CombatAction
from ...dd_data import LimitedDict


class StormElemental(Elemental):
    '''Storm Elemental Module'''
    stats_structure: Dict[str, Tuple[int]] = {"Hit Points": (60, 15),
                                              "Strength": (5, 1),
                                              "Agility": (12, 3),
                                              "Intelligence": (10, 2),
                                              "Special": (5, 0)}
    elemental_types = [("Storm Elemental", "Lightning"),
                       ("Storm Elemental Lord", "Lightning")]

    def __init__(self, level_mod: int):
        elemental_type: tuple = self.spawn_elemental(
            level_mod, self.elemental_types)
        self._hit_points: int = self.stats_structure["Hit Points"][0]
        self._max_hit_points: int = self._hit_points
        self._elemental_type: str = elemental_type[0]
        self._damage_type: str = elemental_type[1]
        super().__init__(self._elemental_type, level_mod, self.stats_structure)
        self._sub_type: str = "Lightning"
        self._dam_modifiers = LimitedDict(
            ("Lightning", (self._damage_type)), default_value=100)
        self._options = [self.static_shock, self.double_shock]
        self._static_shock_count = 0

    def spawn_elemental(self, level_mod: int, elemental_types: list):
        ''' Spawns elemental based on character level '''
        if level_mod >= 25:
            increased_odds = level_mod - 25
            base_value = .0
            lord_chance = .01
            for _ in range(increased_odds):
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
        # level 1
        self._options.append("static_shock")
        self._options.append("double_shock")

    def level_up(self):
        super().level_up()
        if self._level % 2 == 0:
            self._attack_power += 1
        else:
            self._defense_power += 1
        if self._level >= 5:
            self._options.append("lightning_storm")
        if self._level >= 10:
            self._options.append("improved_static_shock")
        if self._level >= 15:
            self._options.append("improved_lightning_storm")
        if self._level >= 20:
            self._options.append("summon_lesser_elemental")

    def attack(self) -> CombatAction:
        damage: int = self.damage_modify(self._attack_power)
        message: str = f"{self.name} Attacks with for <value> Lightning damage"
        return CombatAction([("Attack", damage, "Lightning", message)], "")

    def static_shock(self):
        ''' passive: Storm Elemental Attack grants them a Static Shock. When
            they reach 5 static shock they automatically unleash a Shock Nova
            which deals attack_power * 150% base damage as Lightning damage and
            resets static shock stacks to 0.
        '''
        pass

    def double_shock(self):
        ''' Storm Elemental quickly shocks their opponent twice, dealing 50%
            attack_power base damage as Lightning damage and gaining a charge
            of Static Shock each time.
        '''
        pass

    def lightning_storm(self):
        ''' Once per Combat: Storm Elemental summons a lightning storm, dealing
            33% attack_power base damage as Lightning damage and granting a
            charge of Static Shock each time the Storm Elemental takes an
            action for the remainder of combat.
        '''
        pass

    def improved_static_shock(self):
        ''' passive: Storm Elementals now begin combat with 1 charge of Static
            Shock and Shock Nova deals attack_power * 200% base damage.
        '''
        pass

    def improved_lightning_storm(self):
        ''' passive: When the Storm Elemental unleashes Shock Nova, Lightning
            Storm is automatically cast if it has not be cast already.
        '''
        pass

    def summon_lesser_elemental(self):
        ''' The Storm Elemental Summons a Lesser Storm Elemental which attacks
            immediately for 33% attack_power.  The Lesser Storm Elemental will
            attack each time the Storm Elemental takes an action this combat.
            When Shock Nova is unleashed, All Lesser Storm Elementals are
            destroyed, each Lesser Elemental destroyed this way makes the Shock
            Nova deal 20% more damage (non compounding) and causes the Storm
            Elemental to gain 1 Static Shock charge.
        '''
        pass

    def take_turn(self) -> CombatAction:
        ''' Storm Elemental has a 75% to Attack each turn and a 25% chance to
            return a random skill, until they have unleashed a Shock Nova.
            After unleashing a Shock Nova, Storm Elementals have a 100% chance
            to return a random non-Attack action.
        '''
        self.elemental_reconstitute()
        # if randint(1, 100) <= 25:
        #     return choice(self._options)()
        # # TODO: after self._static_shock_count == 5
        # return self.attack()
        return self.attack()
