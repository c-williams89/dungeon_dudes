'''Module for Dungeon Dudes Golem Monster'''
from random import gauss
from .monsters_abc import Monster
from ..combat_action import CombatAction
from ..dd_data import CombatPrint, LimitedDict, damage_types


class Golem(Monster):
    '''Golem Monster Class'''
    def __init__(self, name: str, level_mod: int, stat_structure: dict):
        self._gold = level_mod * 6
        self._experience_points = 10 * (20 * level_mod - 1)
        super().__init__(name, level_mod, "Golem", stat_structure)
        self.printer = CombatPrint()
        self._def_modifiers = LimitedDict(damage_types, default_value=100)
        self._dam_modifiers = LimitedDict("Physical", default_value=100)

    def modify_damage(self, damage) -> int:
        '''Add variance to damage events'''
        std_deviation = damage * 0.03
        modified = int(gauss(damage, std_deviation))
        return modified

    def attack(self) -> CombatAction:
        '''Golem attack deals phys damage with a base of its attack_power'''
        damage: int = self.golem_damage(self.modify_damage(self._attack_power))
        message: str = f"{self.name} Attacks with for <value> physical damage"
        return CombatAction([("Attack", damage, "Physical", message)], "")

    def base_att_def_power(self):
        self._attack_power = self.strength
        self._defense_power = self.agility * 2

    @property
    def hit_points(self):
        '''Override Parent Getter for HP'''
        return self._hit_points

    @hit_points.setter
    def hit_points(self, value):
        '''Setter for HP'''
        if value >= self.max_hit_points:
            self._hit_points = self.max_hit_points
        else:
            self._hit_points = int(value)

    def sum_parts(self):
        '''attack/defense power reduced by 15% for ever 25% loss of max HP'''
        if self.max_hit_points == 0:
            return

        health_percent = (self._hit_points / self.max_hit_points) * 100
        debuff_stack = 4 - int(health_percent // 25)
        multiplier = 1 - (0.15 * debuff_stack)
        self._attack_power = round(self._attack_power * multiplier)
        self._defense_power = round(self._defense_power * multiplier)

    def take_damage(self, damage: int, dmg_type: str, message: str) -> bool:
        '''Process damage events'''
        alive = True
        if dmg_type == "Poison":
            damage = 0
            msg: str = "Golems are immune to poison!"
            self.printer(msg)
        elif dmg_type == "Physical":
            damage = damage - (self._defense_power // 2)
            damage = int(damage * self._def_modifiers[dmg_type] / 100)
        else:
            damage = int(damage * self._def_modifiers[dmg_type] / 100)

        self.sum_parts()

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

    def golem_damage(self, damage: float) -> int:
        '''golem damage'''
        return int(damage)

    def take_turn(self) -> CombatAction:
        '''Take turn and return success status of action, and the action'''
        return self.attack()
