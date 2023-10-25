'''Treasure Golem Module for Dungeon Dudes'''
from typing import Dict, Tuple
from random import choice
from src.dd_data import LimitedDict
from ..golem import Golem
from ...dd_data import LimitedDict
from ...combat_action import CombatAction


class TreasureGolem(Golem):
    '''TreasureGolem Module'''
    stats_structure: Dict[str, Tuple[int]] = {"Hit Points": (70, 15),
                                              "Strength": (18, 4),
                                              "Agility": (8, 2),
                                              "Intelligence": (0, 0),
                                              "Special": (0, 0)}

    def __init__(self, level_mod: int):
        self._hit_points: int = self.stats_structure["Hit Points"][0]
        super().__init__('Treasure Golem',
                         level_mod, self.stats_structure)
        self._sub_type: str = "Treasure Golem"
        self._gold = level_mod * 20
        self._dam_modifiers = LimitedDict("Physical", default_value=100)
        self._gem_rain_active = False
        self._gold_to_iron_flag = False
        self._next_attack_bonus = self._attack_power
        self._experience_points = 5 * (10 * (level_mod - 1))

    @property
    def damage_modifiers(self) -> LimitedDict:
        '''Getter for damage modifiers'''
        return self._dam_modifiers

    @property
    def defense_modifiers(self) -> LimitedDict:
        '''getter for defense modifiers'''
        return self._def_modifiers

    def get_skills(self) -> Dict[str, 'function']:
        '''get skills learned'''
        return {}

    def get_skills_list(self) -> list:
        '''get list of skills learned'''
        skills_list = ["molten gold"]
        if self.level >= 5:
            skills_list.append("gem rain")
        if self.level >= 10:
            skills_list.append("gold to iron")
        return skills_list

    def special_skill(self) -> CombatAction:
        '''return special skill'''
        skill = choice([self.molten_gold, self.gem_rain, self.gold_to_iron])
        return skill()

    def molten_gold(self, dmg_type):
        '''
        passive: Whenever a Treasure Golem takes Fire damage, they lose 5%
        of their gold (max -50%) and their next Attack deals
        50% attack_power additional Fire damage.
        '''
        if dmg_type == 'Fire':
            self._gold = max(self._gold * 0.95, self._gold - 50)
            self._next_attack_bonus = self._attack_power * 0.5

    def gem_rain(self) -> CombatAction:
        '''
        summons a rain for razer sharp Gems.  The gems dealt
        50% attack_power based Physical damage immediately and 20%
        attack_power Physical damage every time the Treasure Golem takes an
        action for the remainder of the encounter.  Gem Rain initial
        increases the Treasure Golems gold by 10% and every round the gems
        fall increases it's gold by an additional 4%
        '''
        self._gold += int(self._gold * 0.1)
        initial_damage = self._attack_power * 0.5
        self._gem_rain_active = True
        msg = (f"{self.name} performs gem rain, increasing its gold "
               "and deals <value> physical damage initially. Gems will "
               "continue to fall.")
        return CombatAction([("Attack", initial_damage, "Physical", msg)], "")

    def gold_to_iron(self) -> CombatAction:
        '''
        improves its defensive modifiers vs Physical, Fire, Ice, and Holy
        damage by 15 for the remainder of combat.  Treasure Golem worsens
        its defensive modifier vs Lightning by 15 for the remainder of combat.
        (max +45/-45).  This reduces the Treasure Golems gold by 15%
        '''
        self._gold_to_iron_flag = True
        for element in ['Physical', 'Fire', 'Ice', 'Holy']:
            self._def_modifiers[element] = \
                min(self._def_modifiers[element] + 15, 45)
        self._def_modifiers['Lightning'] = \
            max(self._def_modifiers['Lightning'] - 15, -45)
        self._gold = int(self._gold * 0.85)
        msg = (f"{self.name} transmutes gold to iron, improving its defenses "
               "but making it more vulnerable to lightning.")
        return CombatAction([("Aura", 15, "Physical", ""),
                             ("Aura", 15, "Fire", ""),
                             ("Aura", 15, "Ice", ""),
                             ("Aura", 15, "Holy", ""),
                             ("Aura", -15, "Lightning", "")], msg)

    def attack(self) -> CombatAction:
        '''attack function'''
        damage: int = \
            self.golem_damage(self.modify_damage(self._attack_power))
        message: str = f"{self.name} Attacks for <value> physical damage"

        if self._gem_rain_active:
            secondary_dmg: int = \
                self.golem_damage(self.modify_damage(self._attack_power * 0.2))
            secondary_msg: str = (f"{self.name}'s gem rain deals an "
                                  f"additional <value> physical damage")
            return CombatAction([("Attack", damage, "Physical", message),
                                 ("Attack", secondary_dmg, "Physical",
                                  secondary_msg)], "")
        return CombatAction([("Attack", damage, "Physical", message)], "")

    def take_turn(self) -> CombatAction:
        '''takes turn and returns the action'''
        options = [self.attack]
        if self.level >= 5:
            options.append(self.gem_rain)
        if self.level >= 10:
            options.append(self.gold_to_iron)
        return choice(options)()
