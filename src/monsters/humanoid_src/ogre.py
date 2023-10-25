'''Ogre Module for Dungeon Dudes'''
from typing import Dict, Tuple
from random import choice, randint
from ..humanoid import Humanoid
from ...dd_data import LimitedDict
from ...combat_action import CombatAction


class Ogre(Humanoid):
    '''Ogre Module'''
    stats_structure: Dict[str, Tuple[int]] = {"Hit Points": (75, 20),
                                              "Strength": (18, 3),
                                              "Agility": (10, 3),
                                              "Intelligence": (7, 1),
                                              "Special": (0, 0)}
    ogre_types = [("Blood-Thirster", "Physical"), ("Ogre-Magi", "Physical")]

    def __init__(self, level_mod: int):
        ogre_type = choice(self.ogre_types)
        self._ogre_type: str = ogre_type[0]
        self._hit_points: int = self.stats_structure["Hit Points"][0]
        self._damage_type: str = ogre_type[1]
        super().__init__(f"{self._ogre_type} Ogre",
                         level_mod,
                         self.stats_structure)
        self._sub_type: str = "Ogre"
        self._dam_modifiers = LimitedDict(("Physical", (self._damage_type)),
                                          default_value=100)
        self._special_count = 0
        self._two_minds = False
        self._damage = self.humanoid_damage(self.modify_damage(self.strength))

    @property
    def damage_modifiers(self):
        return self._dam_modifiers

    @property
    def defense_modifiers(self):
        return self._def_modifiers

    @property
    def damage(self):
        return self._damage

    @property
    def ogre_type(self):
        return self._ogre_type

    def get_skills(self):
        return {}

    def get_skills_list(self) -> list:
        special_skills = {"Blood-Thirster": "Risky Blow",
                          "Ogre-Magi": "Wild Magics"}
        return special_skills

    def risky_blow(self) -> CombatAction:
        msg: str = ("Blood-Thirster Ogre performs a risky blow, dealing "
                    "<value> physical damage")
        risky_chance = randint(0, 10)
        if ((risky_chance % 2) == 0):
            damage = int(2 * self.damage)
            return ("Attack", damage, "Physical", msg)
        self.printer("Blood-Thirster Ogre missed with Risky Blow")
        return ("Miss", 0, "Miss", "")

    def wild_magics(self):
        self._two_minds = True
        options = ["Lightning", "Ice", "Fire"]
        damage_type = choice(options)
        damage_amt = self.intelligence
        msg: str = (f"{self.name} casts wild magics, dealing <value> "
                    f"{damage_type} damage and attacking again")
        return ("Attack", damage_amt, damage_type, msg)

    def frenzy(self):
        msg: str = ("Blood-Thirster Ogre goes into a frenzy, dealing <value> "
                    "damage")
        return ("Attack", self.damage, "Physical", msg)

    def improved_frenzy(self):
        msg: str = ("Blood-Thirster Ogre goes into an Improved Frenzy, dealing"
                    " <value> damage.")
        return ("Attack", self.damage, "Physical", msg)

    def special_skill(self):
        if self._ogre_type == "Blood-Thirster":
            return self.risky_blow()
        return self.wild_magics()

    def attack(self):
        damage: int = self.humanoid_damage(
            self.modify_damage(self._attack_power))
        msg: str = f"{self.name} Attacks with for <value> physical damage"
        return ("Attack", damage, "Physical", msg)

    def blood_thirster_attack(self):
        actions = []
        actions.append(self.risky_blow())
        if randint(0, 100) < 25:
            actions.append(self.frenzy())
            if self.level > 9:
                if randint(0, 100) < 25:
                    actions.append(self.improved_frenzy())
                else:
                    self.printer("Blood-Thirster Ogre's Improved Frenzy was "
                                 "Unsuccessful")
        else:
            self.printer("Blood-Thirster Ogre's Frenzy Unsuccessful")
        return actions

    def strategic_thinking(self):
        if ((self.hit_points > int(self.max_hit_points * .75)) or
           (self.hit_points < int(self.max_hit_points * .25))):
            self._damage += int(self.damage * .25)

    def bloodlust(self):
        pass

    def take_turn(self) -> CombatAction:
        '''Create list of normal attack and special attacks and choose one'''
        self.strategic_thinking()
        action_list = []
        if self.hit_points < int(self.max_hit_points / 2):
            if randint(0, 100) < 75:
                if self.healing_potions:
                    self.healing_potion()
                    self.bloodlust()
        if self.ogre_type == "Blood-Thirster":
            actions = [self.attack, self.blood_thirster_attack]
            option = choice(actions)
            if option == self.attack:
                action_list.append(option())
                return CombatAction(action_list, "")
            return CombatAction(option(), "")
        else:
            actions = [self.attack, self.wild_magics]
            option = choice(actions)
            if option == self.attack:
                action_list.append(option())
                if self.level > 4:
                    action_list.append(self.wild_magics())
            else:
                action_list.append(option())
                if self.level > 4:
                    action_list.append(self.attack())
            return CombatAction(action_list, "")
