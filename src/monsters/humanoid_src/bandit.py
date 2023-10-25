'''Bandit Module for Dungeon Dudes'''
from typing import Dict, Tuple
from random import randint, randrange, choices

from src.dd_data import LimitedDict
from ..humanoid import Humanoid
from ...dd_data import LimitedDict
from ...combat_action import CombatAction


class Bandit(Humanoid):
    '''Bandit Module'''
    stats_structure: Dict[str, Tuple[int]] = {"Hit Points": (75, 20),
                                              "Strength": (5, 1),
                                              "Agility": (10, 3),
                                              "Intelligence": (7, 1),
                                              "Special": (0, 0)}

    def __init__(self, level_mod: int):
        self._hit_points: int = self.stats_structure["Hit Points"][0]
        self._damage_type = "Physical"
        super().__init__("Pack of Bandits",
                         level_mod,
                         self.stats_structure)
        self._dam_modifiers = LimitedDict(("Physical", "Fire"),
                                          default_value=100)

        if self.level < 8:
            self._num_bandits = 3
        elif self.level < 15:
            self._num_bandits = 4
        else:
            self._num_bandits = 5

        if self.level > 2:
            self._healing_potions += 1

    @property
    def damage_modifiers(self) -> LimitedDict:
        return self._dam_modifiers

    @property
    def defense_modifiers(self) -> LimitedDict:
        return self._def_modifiers

    @property
    def num_bandits(self):
        '''Getter for size of the band of bandits'''
        return self._num_bandits

    def take_damage(self, damage: int, dmg_type, message: str) -> bool:
        if "all enemies" in message.lower():
            damage *= self.num_bandits
        alive = super().take_damage(damage, dmg_type, message)
        return alive

    def get_skills(self) -> Dict[str, 'function']:
        return {}

    def get_skills_list(self) -> list:
        skills_list = ["Fireball", "Dirty Tricks"]
        return skills_list

    def fireball(self) -> Tuple:
        '''Returns tuple for Fireball attack'''
        damage: int = self.humanoid_damage(
            self.modify_damage(self.intelligence))
        msg: str = ("Bandit Sorcerer casts fireball, dealing <value> "
                    "fire damage")
        return ("Attack", damage, "Fire", msg)

    def dirty_tricks(self) -> Tuple:
        '''Returns tuple for Dirty Tricks attack'''
        msg: str = "Bandit Rogue attacks for <value> Physical damage"
        damage_amt = int((3 * self.attack_power) / 4)
        return ("Attack", damage_amt, "Physical", msg)

    def rallying_cry(self):
        '''Returns tuple for Rallying Cry action'''
        self.printer("Bandit Bard strengthens future physical attacks")
        return ("Battle Cry", 10, "Physical", "")

    def bless(self):
        '''Returns tuple for Battle Cry action'''
        self.printer("Bandit Cleric blesses the band, increasing damage "
                     "modifier and healing the band")
        self.hit_points += int(self.max_hit_points / 2)
        return ("Battle Cry", 10, "Physical", "")

    def get_action(self):
        '''Creates a list of actions based on level of the Band of Bandits,
        chooses a random action and returns the tuple of the corresponding
        action
        '''
        actions = [self.fireball,
                   self.fireball,
                   self.dirty_tricks]
        if self.level > 7:
            actions.append(self.rallying_cry)
        if self.level > 14:
            actions.append(self.bless)

        index = randint(0, (len(actions) - 1))
        option = actions.pop(index)
        return option()

    def turn_options(self):
        '''Creates a list of action tuples based on the number of bandits.
        1 Action and n-1 Attacks.
        '''
        damage: int = self.humanoid_damage(
            self.modify_damage((self.attack_power)))
        msg: str = "Bandit attacks, dealing <value> physical damage"
        attack = ("Attack", damage, "Physical", msg)
        action_list = []

        for _ in range(1, self._num_bandits):
            action_list.append(attack)
        action_list.append(self.get_action())
        return action_list

    def escape(self):
        '''Returns tuple for Escape Action'''
        return ("Escape", 0, "", "")

    def take_turn(self) -> CombatAction:
        '''Takes a turn for the Monster. Determines whether to consume a
        healing potion based on health, then creates list of options and
        selects an option based on health and weighted choice.
        '''
        action_list = []

        if self.hit_points < (self.max_hit_points / 2):
            if randrange(2):
                self.healing_potion()

        option_list = [self.escape, self.turn_options]
        if self.hit_points <= int(self.max_hit_points * .10):
            if self.healing_potions:
                option_list.append(self.healing_potion)
                option = choices(option_list, weights=(25, 25, 50), k=1)
                if option.__name__ != "turn_options":
                    action_list.append(option())
                else:
                    action_list = option()
            else:
                option = choices(option_list, weights=(25, 75), k=1)
                if option.__name__ != "turn_options":
                    action_list.append(option())
                else:
                    action_list = option()
        else:
            action_list = self.turn_options()

        return CombatAction(action_list, "")
