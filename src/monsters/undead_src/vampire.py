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
        self._max_hp: int = self._hit_points
        self._sub_type: str = "Vampire"
        self._bat = False
        self._wolf = False
        self._icy_touch_nerf = False
        self._mist = False
        self._mist_counter = 0

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
        skills_list = []
        if self.level >= 5:
            skills_list.append("mist_form")
        if self.level >= 15:
            skills_list.append("mist_form")
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

        if self._mist == True:
            damage = 0
            self._mist = False

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

    def attack(self) -> CombatAction:
        attack_actions = []
        damage: int = (self.modify_damage(self.strength))
        message: str = f"{self.name} Attacks for <value> physical damage"
        attack_actions.append(("Attack", damage, "Physical", message))
        heal = self.leeching_strikes(damage)
        self._hit_points += heal
        heal_message: str = f"{self._sub_type} heals for {heal} with leeching strikes"
        self.printer(heal_message)
        if self._bat == True:
            bat_damage: int = self.modify_damage(self.strength * .5)
            bat_message: str = "Bat attacks for <value> physical damage"
            attack_actions.append(("Attack", bat_damage, "Physical", bat_message))
        if self._wolf == True:
            wolf_damage: int = self.modify_damage(self.strength * .5)
            wolf_message: str = "Wolf attacks for <value> physical damage"
            attack_actions.append(("Attack", wolf_damage, "Physical", wolf_message))
        return CombatAction(attack_actions, "")

    def icy_touch(self):
        icy_actions = []
        message: str = f"{self._sub_type} attacks for <value> with icy touch"
        damage: int = self.modify_damage(self.intelligence * 0.67)
        heal = self.leeching_strikes(damage)
        self._hit_points += heal
        heal_message: str = f"{self._sub_type} heals for {heal} with leeching strikes"
        self.printer(heal_message)
        icy_actions.append(("Attack", damage, "Ice", message))
        if self._icy_touch_nerf == False:
            phys_nerf = ("Hex", -10, "Physical", "")
            icy_actions.append(phys_nerf)
            ice_nerf = ("Hex", -10, "Ice", "")
            icy_actions.append(ice_nerf)
            self._icy_touch_nerf = True
        if self._bat == True:
            bat_damage: int = self.modify_damage(self.strength * .5)
            bat_message: str = "Bat attacks for <value> physical damage"
            icy_actions.append(("Attack", bat_damage, "Physical", bat_message))
        if self._wolf == True:
            wolf_damage: int = self.modify_damage(self.strength * .5)
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

    def improved_summon(self):
        message: str = f"{self._sub_type} has summoned his BAT and WOLF"
        self.printer(message)
        self._bat = True
        self._wolf = True

    def leeching_strikes(self, damage) -> int:
        heal: int = damage * .1
        return int(heal)
    
    def mist_form(self) -> CombatAction:
        message: str = f"{self._sub_type} has transformed into mist form"
        self.printer(message)
        self._mist = True
    
    def take_turn(self) -> CombatAction:
        if self.level >= 20:
            self.improved_summon()
        if self.level >= 10:
            if self._wolf == False:
                if self._bat == True:
                    self.summon_wolf()
        if self._bat == False:
            self.summon_bat() 

        if ((self._hit_points < (self._max_hp * .3)) & (self.level >= 5)):
            if ((self._hit_points < (self._max_hp * .1)) & (self.level >= 10)):
                message: str = f"{self._sub_type} call mist_form and has escaped the fight!"
                return CombatAction([("Escape", 0, "Physical", message)], "") 
            elif self._mist_counter == 0:
                self.mist_form()
                damage: int = self.stats_structure["Intelligence"][0] // 3
                message: str = f"{self._sub_type} attacks for {damage} ice damage"
                self._mist_counter += 1
                return CombatAction([("Attack", damage, "Ice", message)], "")

        rand_num = randint(1, 10)
        if (1 <= rand_num <= 7):
            option = self.icy_touch
        else:
            option = self.attack

        return option()

