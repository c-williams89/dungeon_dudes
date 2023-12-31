''' Module for the Dungeon Dudes Elemental Monster '''
from random import gauss
from .monsters_abc import Monster
from ..combat_action import CombatAction
from ..dd_data import CombatPrint, LimitedDict, damage_types


class Elemental(Monster):
    ''' Elemental Monster Class

        name, str --
        level_mod, int --
        stat_structure, dict --
    '''

    def __init__(self, name: str, level_mod: int, stat_structure: dict):
        self._gold = level_mod * 5
        super().__init__(name, level_mod, "Elemental", stat_structure)
        self.printer = CombatPrint()
        self._def_modifiers = LimitedDict(damage_types, default_value=100)
        self._dam_modifiers = LimitedDict(damage_types, default_value=100)

    def base_att_def_power(self):
        self._attack_power = self.strength
        self._defense_power = self.agility

    def attack(self) -> CombatAction:
        damage: int = self.damage_modify(self._attack_power)
        message: str = f"{self.name} Attacks with for <value> elemental damage"
        return CombatAction([("Attack", damage, "Elemental", message)], "")

    def damage_modify(self, damage) -> int:
        ''' Adds Variance to Damage Events '''
        modified: int = gauss(damage, .1)
        return modified

    @property
    def hit_points(self):
        ''' Override Parent Getter for HP '''
        return self._hit_points

    @hit_points.setter
    def hit_points(self, value):
        ''' Setter for Hit Points '''
        if value >= self.max_hit_points:
            self._hit_points = self.max_hit_points
        else:
            self._hit_points = int(value)

    def take_damage(self, damage: int, dmg_type, message: str) -> bool:
        ''' Processes Damage Events '''
        alive = True
        # check dmg_type against elemental type
        result = self.damage_check(damage, dmg_type)
        damage = int(result * self._def_modifiers[dmg_type]/100)
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

    def damage_check(self, damage: str, dmg_type: str) -> int:
        ''' Helper function for calculating damage '''
        # if damage type matches elemental type
        if self._elemental_type == dmg_type:
            # call elemental_immunity
            return self.elemental_immunity(damage)
        # call elemental_vulnerability
        result = self.elemental_vulnerability(dmg_type)
        if result is True:
            return damage * 1.50
        return damage

    def elemental_reconstitute(self) -> int:
        ''' Elementals heal for 8% of their current hit_points at the
        beginning of each of their turns (rounded up).
        '''
        if self._hit_points == self._max_hit_points:
            pass
        #  TODO: adjust for less than total but cannot overheal
        else:
            result = round(self._hit_points * 0.08)
            self._hit_points += result
            self.printer(f"{self.name} reconstitutes {result} hit points!")

    def elemental_immunity(self, damage: str) -> int:
        ''' Elementals are immune to all damage from their type '''
        damage = 0
        return damage

    def elemental_vulnerability(self, dmg_type: str) -> bool:
        ''' 50% increased damage taken according to following:

            fire vuln to ice
            ice vuln to lightning
            lightning vuln to fire

            dmg_type, str --

            returns, bool -- true if elemental type is vulnerable to dmg_type
        '''
        vulnerabilities = {
            "fire": "ice",
            "ice": "lightning",
            "lightning": "fire"
        }

        vulnerable = vulnerabilities.get(dmg_type)
        if vulnerable is None:
            return False
        if self._elemental_type == vulnerable:
            return True

    def take_turn(self) -> CombatAction:
        ''' Takes turn and returns the success status of the action and the
            action
        '''
        # reconstitutes every turn
        self.elemental_reconstitute()
        return self.attack()
