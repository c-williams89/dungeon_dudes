'''Murloc Module for Dungeon Dudes'''
from typing import Dict, Tuple
from random import randint

from src.dd_data import LimitedDict
from ..humanoid import Humanoid
from ...combat_action import CombatAction


class Murloc(Humanoid):
    '''Murloc Module'''
    stats_structure: Dict[str, Tuple[int]] = {"Hit Points": (75, 20),
                                              "Strength": (5, 1),
                                              "Agility": (10, 3),
                                              "Intelligence": (6, 2),
                                              "Special": (0, 0)}

    def __init__(self, level_mod: int):

        self._poisoned = False
        self._hit_points: int = self.stats_structure["Hit Points"][0]
        self._damage_type = "Physical"
        super().__init__("Murloc Tribe",
                         level_mod,
                         self.stats_structure)
        self._dam_modifiers = LimitedDict(("Physical",
                                           "Ice",
                                           "Poison",
                                           "Holy"), default_value=100)

        if self.level < 10:
            self._tribe_size = 4
        else:
            self._tribe_size = 5

        self._damage = self.humanoid_damage(
            self.modify_damage(self.intelligence))
        self._damage_type = "Physical"
        self._msg = "Murloc attacks, dealing <value> physical damage"
        self._base_attack = ("Attack", self.damage, "Physical", self._msg)

    @property
    def damage_modifiers(self):
        return self._dam_modifiers

    @property
    def defense_modifiers(self):
        return self._def_modifiers

    @property
    def tribe_size(self):
        return self._tribe_size

    @property
    def damage(self):
        return self._damage

    @property
    def base_attack(self):
        return self._base_attack

    @property
    def damage_type(self):
        return self.damage_type

    @property
    def poisoned(self) -> bool:
        return self._poisoned

    def get_skills(self):
        return {}

    def get_skills_list(self):
        skills_list = ["Ice Bolt", "Forage"]
        return skills_list

    def take_damage(self, damage: int, dmg_type, message: str) -> bool:
        if "all enemies" in message.lower():
            damage *= self.tribe_size
        alive = super().take_damage(damage, dmg_type, message)
        return alive

    def get_base_att(self):
        if self.poisoned:
            if randint(0, 9) < 3:
                msg: str = "Murloc attacks, dealing <value> Poison damage"
                self._base_attack = ("Attack",
                                     int(self.damage * 1.3),
                                     "Poison",
                                     msg)
        return self.base_attack

    def ice_bolt(self):
        damage = self.humanoid_damage(self.modify_damage(self.intelligence))
        msg: str = "Murloc casts Ice Bolt for <value> Ice Damage"
        return ("Attack", damage, "Ice", msg)

    def forage(self):
        self._healing_potions += 1
        self.printer(f"Murloc has gathered ingredients to make a healing "
                     f"potion. Murloc tribe now has {self.healing_potions} "
                     "Healing Potions.")
        return ("Heal", 0, "Heal", "")

    def poisons(self):
        self._poisoned = True
        self.printer("Murloc Rogue has coated Murloc Weapons in Poison")
        return ("", 0, "", "")

    def holy_nova(self):
        health = int(self.max_hit_points * .3)
        self.hit_points += health
        msg: str = ("Murloc Oracle errupts with Holy energy, dealing <value> "
                    f"Holy Damage and heling the tribe by {health} Hit Points")
        return ("Attack", self.damage, "Holy", msg)

    def get_action(self):
        actions = [self.ice_bolt,
                   self.ice_bolt,
                   self.forage,
                   self.forage]
        if self.level > 2:
            actions.append(self.poisons)
        if self.level > 9:
            actions.append(self.holy_nova)
        index = randint(0, (len(actions) - 1))
        option = actions.pop(index)
        return option()

    def take_turn(self):
        action_list = []
        action_list.append(self.get_action())
        base_att = self.get_base_att()
        for _ in range(1, self.tribe_size):
            action_list.append(base_att)
        action = CombatAction(action_list, "")
        return action
