'''Module for the Dungeon Dudes Zombie Undead'''
from typing import Dict, List, Tuple

from src.dd_data import LimitedDict
from random import choice, randint
from ..undead import Undead
from ...dd_data import LimitedDict
from ...combat_action import CombatAction

class Vampire(Undead):
    '''Vampire Undead Class'''
    stats_structure: Dict[str, Tuple[int]] = {"Hit Points": (75, 15), "Strength": (10, 2),
                    "Agility" : (15, 3), "Intelligence" : (16, 4), "Special" : (0,0)}
    vampire_types = ["Vampire", "Elder Vampire"]

    def __init__(self, level_mod: int):
        vampire_type: str = "Vampire"
        self._hit_points: int = self.stats_structure["Hit Points"][0]
        self._vampire_type: str = vampire_type
        super().__init__(f"{self._vampire_type}", level_mod, self.stats_structure)
        self._sub_type: str = "Vampire"
        self._bat = False
        self._wolf = False
        self._icy_nerf = False

    def base_att_def_power(self):
        self._attack_power =  self.strength
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
        skills_list = ["summon_bat"]
        if self.level >= 5:
            skills_list.append("mist_form")
        if self.level >= 10:
            skills_list.append("summon_wolf")
        if self.level >= 15:
            skills_list.append("summon_wolf")
        if self.level >= 20:
            skills_list.append("summon_all")
        return skills_list
    
    def take_damage(self, damage: int, dmg_type, message: str) -> bool: # pylint: disable=unused-argument
        '''Process Damage Events'''
        alive = True
        if dmg_type == "Physical":
            damage = damage - (self._defense_power // 2)
        elif dmg_type == "Ice":
            damage = 0
        elif dmg_type == "Poison":
            damage = 0
        damage = int(damage * self._def_modifiers[dmg_type]/100)
   
        if damage >= self.hit_points:
            alive = False
            message = message.replace('<value>', str(self._hit_points))
            self.printer(message)
            self._hit_points = 0
            return alive
        
        self._hit_points -= damage
        message = message.replace('<value>', str(damage))
        self.printer(message)
        return alive

    def icy_touch(self):
        icy_actions = []
        message: str = f"{self._sub_type} attacks for <value> with icy touch"
        damage: int = self.stats_structure["Intelligence"][0] * 0.67
        heal = self.leeching_strikes(damage)
        self._hit_points += heal
        heal_message: str = f"{self._sub_type} heals for {heal} with leeching strikes"
        self.printer(heal_message)
        icy_actions.append(("Attack", damage, "Ice", message))
        if self._icy_nerf == False:
            stats_nerf = [("Hex", -10, "Physical", ""), ("Hex", -10, "Ice", "")]
            icy_actions.append(stats_nerf)
        if self._bat == True:
            bat_damage: int = self.attack_power * .5
            bat_message: str = "Bat attacks for <value> physical damage"
            icy_actions.append(("Attack", bat_damage, "Physical", bat_message))
        if self._wolf == True:
            wolf_damage: int = self.attack_power * .5
            wolf_message: str = "Wolf attacks for <value> physical damage"
            icy_actions.append(("Attack", wolf_damage, "Physical", wolf_message))
        return CombatAction(icy_actions, "")
    
    def summon_bat(self):
        message: str = f"{self._sub_type} has summoned his BAT companion"
        self.printer(message)
        self._bat = True

    def summon_wolf(self):
        message: str = f"{self._sub_type} has summoned his WOLF companion"
        self.printer(message)
        self._wolf = True

    def leeching_strikes(self, damage) -> int:
        heal: int = damage * .1
        return int(heal)
    
    def take_turn(self) -> CombatAction:
        if self.level >= 20:
            self.summon_bat()
            self.summon_wolf()
        if self.level >= 10:
            if self._wolf == False:
                if self._bat == True:
                    self.summon_wolf()
        if self._bat == False:
            self.summon_bat()

  

        options = [self.attack, self.icy_touch]
        return choice(options)()
    # def leeching_strikes(self):
    #     message: str = f"{self._sub_type} heals for <value> with leeching strikes"

