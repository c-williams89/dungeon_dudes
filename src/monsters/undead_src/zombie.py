'''Module for the Dungeon Dudes Zombie Undead'''
from typing import Dict, List, Tuple
from ..undead import Undead
from ...dd_data import LimitedDict
from ...combat_action import CombatAction


class Zombie(Undead):
    '''Zombie Undead Class'''
    stats_structure: Dict[str, Tuple[int, int]] = {"Hit Points": (85, 20),
                                                   "Strength": (4, 1),
                                                   "Agility": (8, 3),
                                                   "Intelligence": (0, 0),
                                                   "Special": (4, 0)}

    def __init__(self, level_mod: int):
        self._hit_points: int = self.stats_structure["Hit Points"][0]
        super().__init__('Zombie', level_mod, self.stats_structure)
        self._hit_points += self.update_max_hp()
        self._sub_type: str = "Zombie"
        self._dam_modifiers = LimitedDict(("Physical", "Poison"),
                                          default_value=100)
        self._haunting = 0
        self._horde_size = 6

    @property
    def damage_modifiers(self) -> LimitedDict:
        '''Getter for Damage Modifiers'''
        return self._dam_modifiers

    @property
    def defense_modifiers(self) -> LimitedDict:
        '''Getter for Defense Modifiers'''
        return self._def_modifiers

    def base_att_def_power(self):
        self._attack_power = self.strength
        self._defense_power = self.agility

    def update_max_hp(self) -> int:
        '''Updates max HP based on size of horde'''
        bonus_multiplier = self.level // 8
        bonus_hp = bonus_multiplier * 20
        return bonus_hp

    def get_skills_list(self) -> List[str]:
        return []

    def get_skills(self) -> Dict[str, 'function']:
        return {}

    def take_damage(self, damage: int, dmg_type, message: str) -> bool:
        '''Process Damage Events'''
        alive = True
        if dmg_type == "Physical":
            damage = damage - (self._defense_power // 2)
        damage = int(damage * self._def_modifiers[dmg_type]/100)

        if "all enemies" in message.lower():
            damage *= self._horde_size

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
        '''Attack method for Zombie Horde'''
        self._horde_size += self.level // 8
        horde_actions = []
        if self._haunting == 0:
            horde_actions.append(self.haunting_arua())
        for _ in range(self._horde_size):
            damage: int = (self.modify_damage(self.strength))
            if damage <= 0:
                damage = 1
            message: str = f"{self.name} attacks for <value> physical damage"
            horde_actions.append(("Attack", damage, "Physical", message))
        return CombatAction(horde_actions, "")

    def take_turn(self) -> CombatAction:
        return self.attack()
