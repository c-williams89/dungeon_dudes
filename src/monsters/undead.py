'''Module for the Dungeon Dudes Beast Monster'''
from random import randint
from .monsters_abc import Monster
from ..combat_action import CombatAction
from ..dd_data import CombatPrint, LimitedDict, damage_types

class Undead(Monster):
    '''Undead Monster Class'''

    def __init__(self, name: str, level_mod: int, stat_structure: dict):
        self.gold = level_mod * 4
        super().__init__(name, level_mod, "Undead", stat_structure)
        self.printer = CombatPrint()
        self._def_modifiers = LimitedDict(damage_types, default_value=100)
        self._dam_modifiers = LimitedDict(("Physical", "Ice"), default_value=100)

    def modify_damage(self, damage) -> int:
        '''Adds Variance to Damage Events and Calculates Critical Chance'''
        damage_min = int(damage * 0.01)
        damage_max = int(damage * 1.75)
        modified: int = randint(damage_min, damage_max)
        return modified
    
    def attack(self) -> CombatAction:
        damage: int = (self.modify_damage(self._attack_power))
        message: str = f"{self.name} Attacks with for <value> physical damage"
        return CombatAction([("Attack", damage, "Physical", message)], "")
    
    #TODO: will have to implement in individual monster type; banshee is diff
    # def base_att_def_power(self):
    #     self._attack_power = self.strength
    #     self._defense_power = self.agility

    @property
    def hit_points(self) -> int:
        '''Override Parent Getter for HP'''
        return self._hit_points
    
    @hit_points.setter
    def hit_points(self, value):
        '''Setter for Hit Points'''
        if value >= self.max_hit_points:
            self._hit_points = self.max_hit_points
        else:
            self._hit_points = int(value)

    def take_damage(self, damage: int, dmg_type, message: str) -> bool: # pylint: disable=unused-argument
        '''Process Damage Events'''
        alive = True
        if dmg_type == "Physical":
            damage = damage - (self._defense_power // 2)

        damage = int(damage * self._def_modifiers[dmg_type]/100)
        if damage >= self.hit_points:
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
    
    def resist_death(self, damage: float) -> int:
        '''First time an event would kill, reduce HP to 1'''
        pass

    def take_turn(self) -> CombatAction: # pylint: disable=unused-argument
        '''Takes turn and returns the success of the action and the action'''
        return self.attack()