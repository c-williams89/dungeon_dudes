'''Ogre Module for Dungeon Dudes'''
from typing import Dict, Tuple
from random import choice, randint
from ..humanoid import Humanoid
from ...dd_data import LimitedDict
from ...combat_action import CombatAction

'''
For both ogres, they can each conduct a normal attack for physical damage.
For blood-thirster, special attack is risky blow.
For ogre magi, special attack is wild magics
'''

class Ogre(Humanoid):
    '''Ogre Module'''
    stats_structure: Dict[str, Tuple[int]] = {"Hit Points": (75, 20),
                                              "Strength": (5, 1),
                                              "Agility": (10, 3),
                                              "Intelligence": (7, 1),
                                              "Special": (0,0)}
    ogre_types = [("Blood-Thirster", "Physical"), ("Ogre-Magi", "Physical")]

    def __init__(self, level_mod: int):
        ogre_type = self.ogre_types[0]
        # ogre_type: tuple = choice(self.ogre_types)
        self._hit_points: int = self.stats_structure["Hit Points"][0]
        self._ogre_type: str = ogre_type[0]
        self._damage_type: str = ogre_type[1]
        super().__init__(f"{self._ogre_type} Ogre",
                         level_mod,
                         self.stats_structure)
        self._sub_type: str = "Ogre"
        self._dam_modifiers = LimitedDict(("Physical", (self._damage_type)),
                                          default_value=100)
        self._special_count = 0
        self._two_minds = False

    @property
    def damage_modifiers(self):
        return self._dam_modifiers
    
    @property
    def defense_modifiers(self):
        return self._def_modifiers
    
    def get_skills(self): 
        return {}
    
    def get_skills_list(self) -> list:
        special_skills = {"Blood-Thirster": "Risky Blow",
                          "Ogre-Magi": "Wild Magics"}

    def risky_blow(self) -> CombatAction:
        msg: str = ("Blood-Thirster Ogre performs a risky blow, dealing "
                    "<value> physical damage")
        risky_chance = randint(0, 10)
        damage: int = 0
        if ((risky_chance % 2) == 0):
            damage = int(2 * (self.humanoid_damage(self.modify_damage(self.hit_points))))
        return CombatAction([("Attack", damage, "Risky Blow", msg)], "")
    
    def wild_magics(self):
        self._two_minds = True
        options = ["Lightning", "Ice", "Fire"]
        damage_type = choice(options)
        damage_amt = self.intelligence
        msg: str = (f"{self.name} casts wild magics, dealing <value> "
                    f"{damage_type} damage and attacking again")
        return CombatAction([("Attack", damage_amt, damage_type, msg), 
                            ("Attack", damage_amt, damage_type, msg)],
                            "")

    def frenzy(self) -> CombatAction:
        pass

    def improved_frenzy(self):
        pass

    def special_skill(self):
        if self._ogre_type == "Blood-Thirster":
            return self.risky_blow()
        return self.wild_magics()
    
    def attack(self):
        damage: int = self.humanoid_damage(self.modify_damage(self._attack_power))
        message: str = f"{self.name} Attacks with for <value> physical damage"
        if self._two_minds:
            return CombatAction([("Attack", damage, "Physical", message),
                                 ("Attack", damage, "Physical", message)],
                                 "")
        else:
            return CombatAction([("Attack", damage, "Physical", message)], "")

    def take_turn(self) -> CombatAction:
        '''Create list of normal attack and special attacks and choose one'''
        options = [self.attack, self.special_skill]
        return choice(options)()
