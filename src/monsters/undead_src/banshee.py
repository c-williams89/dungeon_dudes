'''Module for the Dungeon Dudes Banshee Undead'''
from typing import Dict, List, Tuple
from src.dd_data import LimitedDict
from random import choice, randint
from ..undead import Undead
from ...dd_data import LimitedDict
from ...combat_action import CombatAction

class Banshee(Undead):
    '''Banshee Undead Class'''
    stats_structure: Dict[str, Tuple[int]] = {"Hit Points": (65, 13), "Strength": (0, 0),
                    "Agility" : (15, 3), "Intelligence" : (16, 4), "Special" : (0,0)}
    
    def __init__(self, level_mod: int):
        self._hit_points: int = self.stats_structure["Hit Points"][0]
        super().__init__('Banshee', level_mod, self.stats_structure)
        self._sub_type: str = "Banshee"
        self._dam_modifiers = LimitedDict(("Ice"), default_value=100)
        self._damage_event_counter = 5
        self._chilling_aura_counter = 10
        self._was_blizzard = False
    
    def base_att_def_power(self):
        self._attack_power =  self.intelligence
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
        return []
    
    def take_damage(self, damage: int, dmg_type, message: str) -> bool: # pylint: disable=unused-argument
        '''Process Damage Events'''
        alive = True
        if dmg_type == "Physical":
            damage = damage - (self._defense_power // 2)
        elif dmg_type == "Poison":
            damage = 0

        if self.level < 15:
            random_num = randint(1, 10)
            if random_num == 1:
                self.printer("Banshee reduces damage to ZERO")
                damage = 0
        else:
            random_num = randint(1, 20)
            if random_num <= 3:
                self.printer("Banshee reduces damage to ZERO")

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
        self._damage_event_counter -= 1
        if self._damage_event_counter == 0:
            self._damage_event_counter = 5
        return alive

    def attack(self) -> CombatAction:
        attack_actions = []
        damage : int = self.modify_damage(self._attack_power)
        message : str = f"{self.name} Attacks with for <value> ice damage"
        attack_actions.append(("Attack", damage, "Ice", message))
        
        if (5 <= self.level < 15) & (self._chilling_aura_counter > 0):
            attack_actions.append(("Hex", -4, "Ice", ""))
            self._chilling_aura_counter -= 1
        elif (self.level >= 15) & (self._chilling_aura_counter > 0):
            attack_actions.append(("Hex", -5, "Ice", ""))
            self._chilling_aura_counter -= 1

        if self.level >= 10:
            bliz_damage: int = self.modify_damage(self.intelligence * .1)
            bliz_message: str = f"{self.name} Attacks with <value> Blizzard damage"
            attack_actions.append(("Attack", bliz_damage, "Ice", bliz_message))
        return CombatAction(attack_actions, "")
    
    def anti_magic_shield(self):
        pass
    
    def take_turn(self) -> CombatAction:
        return self.attack()