''' Module for the Dungeon Dudes Elemental Monster '''
from random import randint
from .monsters_abc import Monster
from ..combat_action import CombatAction
from ..dd_data import CombatPrint, LimitedDict, damage_types


class Elemental(Monster):
    ''' Elemental Monster Class

        name, str --
        level_mod, int --
        stat_structure, dict --
    '''

    def __init__(self, name: str, type: str, level_mod: int,
                 stat_structure: dict):
        self._gold = level_mod * 5
        super().__init__(name, level_mod, "Elemental", stat_structure)
        # elemental type
        self.type = type
        self.printer = CombatPrint()
        self._def_modifiers = LimitedDict(damage_types, default_value=100)
        self._dam_modifiers = LimitedDict("Physical", default_value=100)

    def base_att_def_power(self):
        self._attack_power = self.strength
        self._defense_power = self.agility

    def attack(self) -> CombatAction:
        damage: int = self.modify_damage(self._attack_power)
        # change for elemental type
        message: str = f"{self.name} Attacks with for <value> {self.type} damage"
        return CombatAction([("Attack", damage, {self.type}, message)], "")

    def modify_damage(self, damage) -> int:
        ''' Adds Variance to Damage Events and Calculates Critical Chance '''
        damage_min = int(damage * 0.95)
        damage_max = int(damage * 1.05)
        modified: int = randint(damage_min, damage_max)
        return modified

    # def elemental_damage(self, damage: float) -> int:
    #     '''Increases a Beast's Damage Under 25% Max Hp'''
    #     if self._hit_points <= (self.max_hit_points / 4):
    #         return int(damage * 1.25)
    #     return int(damage)

    @property
    def hit_points(self):
        ''' Override Parent Getter for HP '''
        return self._hit_points

    @hit_points.setter
    def hit_points(self, value):
        '''Setter for Hit Points'''
        if value >= self.max_hit_points:
            self._hit_points = self.max_hit_points
        else:
            self._hit_points = int(value)

    def take_damage(self, damage: int, dmg_type, message: str) -> bool:
        '''Processes Damage Events'''
        alive = True
        # call damage_check
        self.damage_check(damage)
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

    def damage_check(self, damage: str) -> callable:
        ''' Helper function for calculating damage '''
        # if damage type matches elemental type
        # call elemental_immunity
        # if damage type beats elemental type
        # call elemental_vulnerability
        # else
        # call take_damage

    def elemental_reconstitute(self) -> int:
        ''' Elementals heal for 8% of their current hit_points at the 
        beginning of each of their turns (rounded up).
        '''
        return round(self._hit_points * .08)

    def elemental_immunity(self, damage: str) -> bool:
        ''' Elementals are immune to all damage from their type '''
        alive = True
        return alive

    def elemental_vulnerability(self, damage: str) -> bool:
        ''' 50% increase in damage according to following:

            fire vuln to ice
            ice vuln to lightning
            lightning vuln to fire

        '''
        alive = True

        return alive

    def take_turn(self) -> CombatAction:  # pylint: disable=unused-argument
        ''' Takes turn and returns the success status of the action and the
            action
        '''
        return self.attack()
