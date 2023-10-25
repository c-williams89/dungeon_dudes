'''Stone Golem Module for Dungeon Dudes'''
from typing import Dict, Tuple
from random import choice, choices
from src.dd_data import LimitedDict
from ..golem import Golem
from ...dd_data import LimitedDict
from ...combat_action import CombatAction


class StoneGolem(Golem):
    '''StoneGolem Module'''
    stats_structure: Dict[str, Tuple[int]] = {"Hit Points": (75, 17),
                                              "Strength": (18, 4),
                                              "Agility": (10, 2),
                                              "Intelligence": (0, 0),
                                              "Special": (0, 0)}
    stone_types = [("Granite", "Physical"), ("Obsidian", "Physical")]
    weight = [0.75, 0.25]

    def __init__(self, level_mod: int):
        stone_type = choices(self.stone_types, self.weight, k=1)[0]
        self._stone_type = stone_type
        self._hit_points: int = self.stats_structure["Hit Points"][0]
        self._stone_type: str = stone_type[0]
        self._damage_type: str = stone_type[1]
        super().__init__(f'{self._stone_type} Golem',
                         level_mod, self.stats_structure)
        self._sub_type: float = stone_type[1]
        self._dam_modifiers = LimitedDict("Physical", default_value=100)
        self.splintered = False
        self.absorbed_heat = False
        self.hardened = False
        self.used_lightning_rod = False
        self.thermal_core_used = False
        self.ignited = False

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
        '''get list of skills learnedMetallic'''
        skills_list = []
        # granite golem skills
        if self._stone_type == "Granite":
            if self.level >= 15:
                skills_list.append("lightning_rod")
        # obsidian golem skills
        if self._stone_type == "Obsidian":
            if self.level >= 15:
                skills_list.append("thermal_core")
        return skills_list

    # passives
    def grounded(self, dmg_type: str) -> int:
        '''Stone Golems are immune to lightning'''
        if dmg_type == "Lightning":
            msg: str = "Stone Golems are immune to lightning!"
            self.printer(msg)
            return 0
        return 1

    def ignore_pain(self, damage: int) -> int:
        '''
        ignore 2 damage from every incoming attack event
        increases by 2 every 10th level (1, 11, 21, 31, 41)
        '''
        ignore_pain_value = 2 * (self.level // 10 + 1)
        return max(0, damage - ignore_pain_value)

    def absorb_heat(self, dmg_type: str):
        '''improves physical damage offensive mod if hit by fire'''
        self.absorbed_heat = True
        if dmg_type == "Fire":
            self._dam_modifiers["Physical"] = \
                min(50, self._dam_modifiers["Physical"] + 10)

    def sum_parts(self):
        '''modify sum of their parts'''
        super().sum_parts()
        health_percent = (self._hit_points / self.max_hit_points) * 100
        if health_percent <= 75 and not self.splintered:
            self.splinter()

    # granite golem
    def splinter(self) -> CombatAction:
        '''splinter off a lesser golem when sum of their parts is triggered'''
        self.splintered = True
        splinter_dmg: int = \
            self.golem_damage(self.modify_damage(self.attack_power * 0.33))
        msg: str = ("A lesser golem splinters off and attacks, dealing "
                    "<value> physical damage")
        return CombatAction([("Attack", splinter_dmg, "Physical", msg)], "")

    def exploding_shards(self) -> CombatAction:
        '''
        When preforming their first Attack after summoning a Splinter, Stone
        Golems throw off shards of rock, dealing an additional 100%
        attack_power based Physical damage.  If Absorb Heat has triggered this
        encounter, the Exploding Shards also explode for 50% attack_power based
        Fire damage.
        '''
        if self.splintered:
            shard_dmg: int = \
                self.golem_damage(self.modify_damage(self.attack_power))
            shard_msg: str = ("The attack explodes into shards, dealing "
                              "<value> extra physical damage")

            if self.absorbed_heat:
                heat_dmg: int = \
                    self.golem_damage(self.modify_damage(self.attack_power * 0.5))
                heat_msg: str = ("The shards are superheated, dealing <value> "
                                 "fire damage")
                self.absorbed_heat = False
                self.splintered = False
                return CombatAction([("Attack", shard_dmg, "Physical",
                                      shard_msg),
                                     ("Attack", heat_dmg, "Fire",
                                      heat_msg)], "")

    def lightning_rod(self) -> CombatAction:
        '''one-time use: calls lightning bolt every time an action is taken'''
        if not self.used_lightning_rod:
            self.used_lightning_rod: bool = True
            msg: str = ("Granite Golem becomes a lightning rod, calling down "
                        "bolts of electricity with each action.")
            return CombatAction([("Status Effect", "Lightning Rod",
                                  "Special", msg)], "")

    # obsidian golem
    def harden(self):
        '''Improves defensive Physical modifier when taking an action'''
        self._def_modifiers["Physical"] = \
            min(self._def_modifiers["Physical"] + 5, 40)
        self.hardened = True

    def improved_absorb_heat(self, dmg_type: str):
        '''Enhanced version of absorb_heat for Obsidian Golems'''
        if dmg_type == "Fire":
            self._dam_modifiers["Physical"] = \
                min(self._dam_modifiers["Physical"] + 10, 70)
            self.defense_power *= 0.95
            self.attack_power *= 1.10
            self.hardened = False

    def thermal_core(self) -> CombatAction:
        '''Ignites the Obsidian Golem, affecting actions and incoming damage'''
        if not self.thermal_core_used:
            self.thermal_core_used = True
            self.ignited = True
            msg: str = ("Obsidian Golem's core overheats, adding fire "
                        "damage to its actions and making it vulnerable to"
                        " additional fire damage.")
            return CombatAction([("Status Effect", "Thermal Core", "Special",
                                  msg)], "")

    def attack(self) -> CombatAction:
        '''Stone Golem attack deals physical damage based on attack power'''
        damage: int = self.golem_damage(self.modify_damage(self._attack_power))
        message: str = f"{self.name} Attacks for <value> physical damage"
        # Check for splinter
        if self.splintered:
            splinter_dmg: int = \
                self.golem_damage(self.modify_damage(self.attack_power * 0.33))
            splinter_msg: str = ("The lesser golem attacks for an additional"
                                 " <value> physical damage")
            return CombatAction([("Attack", damage, "Physical", message),
                                 ("Attack", splinter_dmg, self._damage_type,
                                  splinter_msg)], "")
        # Check for exploding shards
        self.exploding_shards()
        # Check for thermal core
        if self.ignited:
            add_fire_dmg = int(self.level * 0.5)
            damage += add_fire_dmg
        return CombatAction([("Attack", damage, "Physical", message)], "")

    def take_damage(self, damage: int, dmg_type: str, message: str) -> bool:
        # Stone Golems are immune to lightning damage
        damage *= self.grounded(dmg_type)
        # Ignore a certain amount of damage based on level
        damage = self.ignore_pain(damage)
        # Process fire damage to improve Physical damage modifiers
        if dmg_type == "Fire":
            self.absorb_heat(dmg_type)
        return super().take_damage(damage, dmg_type, message)

    def special_skill(self):
        '''return special attack per golem type'''
        if self._stone_type == "Granite":
            return self.lightning_rod()
        if self._stone_type == "Obsidian":
            return self.thermal_core()

    def take_turn(self) -> CombatAction:
        '''Takes turn and returns the action'''
        options = [self.attack]
        if self._stone_type == "Granite":
            if self.level >= 15:
                options.append(self.lightning_rod)
        if self._stone_type == "Obsidian":
            if self.level >= 15:
                options.append(self.thermal_core)
        return choice(options)()
