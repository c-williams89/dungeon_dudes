'''Module for the Dungeon Dudes Zombie Undead'''
from typing import Dict, Tuple
from random import randint
from src.dd_data import LimitedDict
from ..undead import Undead
from ...dd_data import LimitedDict
from ...combat_action import CombatAction


class Vampire(Undead):
    '''Vampire Undead Class'''
    stats_structure: Dict[str, Tuple[int, int]] = {"Hit Points": (75, 15),
                                                   "Strength": (10, 2),
                                                   "Agility": (15, 3),
                                                   "Intelligence": (16, 4),
                                                   "Special": (0, 0)}
    vampire_types = ["Vampire", "Elder Vampire"]

    def __init__(self, level_mod: int):
        vampire_type: str = "Vampire"
        self._hit_points: int = self.stats_structure["Hit Points"][0]
        self._vampire_type: str = vampire_type
        super().__init__(f"{self._vampire_type}", level_mod,
                         self.stats_structure)
        self._max_hp: int = self._hit_points
        self._sub_type: str = "Vampire"
        self._bat = False
        self._wolf = False
        self._icy_touch_nerf = False
        self._mist = False
        self._mist_counter = 0

    def base_att_def_power(self):
        self._attack_power = self.strength
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

    def take_damage(self, damage: int, dmg_type, message: str) -> bool:
        '''Process Damage Events'''
        alive = True
        if dmg_type == "Physical":
            damage = damage - (self._defense_power // 2)
        elif dmg_type == "Ice":
            damage = 0
        elif dmg_type == "Poison":
            damage = 0

        if self._mist is True:
            damage = 0
            self._mist = False

        damage = int(damage * self._def_modifiers[dmg_type]/100)

        if damage >= self.hit_points:
            if self._resist:
                self.resist_death(damage, message)
                self._hit_points = 1
                return alive
            alive = False
            message = message.replace('<value>', str(self._hit_points))
            self.printer(message)
            self._hit_points = 0
            return alive
        damage = max(1, damage)
        self._hit_points -= damage
        message = message.replace('<value>', str(damage))
        self.printer(message)
        return alive

    def attack(self) -> CombatAction:
        attack_actions = []
        if self._haunting == 0:
            attack_actions.append(self.haunting_arua())
        damage: int = (self.modify_damage(self.strength))
        if damage <= 0:
            damage = 1
        message: str = f"{self.name} Attacks for <value> physical damage"
        attack_actions.append(("Attack", damage, "Physical", message))
        heal = self.leeching_strikes(damage)
        self._hit_points += heal
        heal_msg: str = f"{self.name} heals for {heal} with leeching strikes"
        self.printer(heal_msg)
        if self._bat is True:
            bat_damage: int = self.modify_damage(self.strength * .5)
            if bat_damage <= 0:
                bat_damage = 1
            bat_msg: str = "Bat attacks for <value> physical damage"
            attack_actions.append(("Attack", bat_damage, "Physical", bat_msg))
        if self._wolf is True:
            wolf_dmg: int = self.modify_damage(self.strength * .5)
            if wolf_dmg <= 0:
                wolf_dmg = 1
            wolf_msg: str = "Wolf attacks for <value> physical damage"
            attack_actions.append(("Attack", wolf_dmg, "Physical", wolf_msg))
        return CombatAction(attack_actions, "")

    def icy_touch(self):
        '''deals icy touch damage'''
        icy_actions = []
        if self._haunting == 0:
            icy_actions.append(self.haunting_arua())
        message: str = f"{self._sub_type} attacks for <value> with icy touch"
        damage: int = self.modify_damage(self.intelligence * 0.67)
        if damage <= 0:
            damage = 1
        heal = self.leeching_strikes(damage)
        self._hit_points += heal
        heal_msg: str = f"{self.name} heals for {heal} with leeching strikes"
        self.printer(heal_msg)
        icy_actions.append(("Attack", damage, "Ice", message))
        if self._icy_touch_nerf is False:
            phys_nerf = ("Hex", -10, "Physical", "")
            icy_actions.append(phys_nerf)
            ice_nerf = ("Hex", -10, "Ice", "")
            icy_actions.append(ice_nerf)
            self._icy_touch_nerf = True
        if self._bat is True:
            bat_damage: int = self.modify_damage(self.strength * .5)
            if bat_damage <= 0:
                bat_damage = 1
            bat_message: str = "Bat attacks for <value> physical damage"
            icy_actions.append(("Attack", bat_damage, "Physical", bat_message))
        if self._wolf is True:
            wolf_damage: int = self.modify_damage(self.strength * .5)
            if wolf_damage <= 0:
                wolf_damage = 1
            wolf_msg: str = "Wolf attacks for <value> physical damage"
            icy_actions.append(("Attack", wolf_damage, "Physical", wolf_msg))
        return CombatAction(icy_actions, "")

    def summon_bat(self):
        '''summon bat companion'''
        message: str = f"{self._sub_type} has summoned his BAT companion"
        self.printer(message)
        self._bat = True

    def summon_wolf(self):
        '''summon wolf companion'''
        message: str = f"{self._sub_type} has summoned his WOLF companion"
        self.printer(message)
        self._wolf = True

    def improved_summon(self):
        '''when level 20 summon bat and wolf at same time'''
        message: str = f"{self._sub_type} has summoned his BAT and WOLF"
        self.printer(message)
        self._bat = True
        self._wolf = True

    @staticmethod
    def leeching_strikes(damage) -> int:
        '''heals for 10% of damage dealt'''
        heal: int = damage * .1
        return int(heal)

    def mist_form(self) -> CombatAction:
        '''reduces damage on next turn to 0; escapes on 2nd call'''
        message: str = f"{self._sub_type} has transformed into mist form"
        self.printer(message)
        self._mist = True

    def take_turn(self) -> CombatAction:
        if self.level >= 20:
            self.improved_summon()
        if self.level >= 10:
            if self._wolf is False:
                if self._bat is True:
                    self.summon_wolf()
        if self._bat is False:
            self.summon_bat()

        if (self._hit_points < (self._max_hp * .3)) & (self.level >= 5):
            if (self._hit_points < (self._max_hp * .1)) & (self.level >= 10):
                message: str = f"{self.name} calls mist_form and has escaped!"
                return CombatAction([("Escape", 0, "Physical", message)], "")
            if self._mist_counter == 0:
                self.mist_form()
                damage: int = self.stats_structure["Intelligence"][0] // 3
                if damage <= 0:
                    damage = 1
                msg: str = f"{self.name} attacks for {damage} ice damage"
                self._mist_counter += 1
                return CombatAction([("Attack", damage, "Ice", msg)], "")

        rand_num = randint(1, 10)
        if rand_num <= 7:
            option = self.icy_touch
        else:
            option = self.attack

        return option()
