'''Stone Golem Module for Dungeon Dudes'''
from typing import Dict, Tuple
from random import choice, choices
from src.dd_data import LimitedDict
from ..golem import Golem
from ...dd_data import LimitedDict
from ...combat_action import CombatAction

class StoneGolem(Golem):
    '''StoneGolem Module'''
    stats_structure : Dict[str, Tuple[int]] = {"Hit Points": (75, 17), 
                                               "Strength": (18, 4),
                                               "Agility" : (10, 2), 
                                               "Intelligence" : (0, 0), 
                                               "Special" : (0,0)}
    stone_types = [("Granite", "Physical"), ("Obsidian", "Physical")]
    # stone_types = ["Granite", "Obsidian"]
    # weight = [0.75, 0.25]

    def __init__(self, level_mod : int):
        # stone_type = choices(self.stone_types, self.weight, k=1)[0]
        # self._stone_type = stone_type
        stone_type : tuple = choice(self.stone_types)
        self._hit_points : int = self.stats_structure["Hit Points"][0]
        self._stone_type : str = stone_type[0]
        super().__init__(f'{self._stone_type} Golem',
                         level_mod, self.stats_structure)
        self._sub_type : float = stone_type[1]
        self._dam_modifiers = LimitedDict("Physical",  default_value=100)
        self.has_splinter = False
        self.use_shards = False
        self.hardened = False
        self.used_lightning_rod = False
        self.used_thermal_core = False
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
        '''get list of skills learned'''
        skills_list = ["grounded", "ignore pain"]
        if self.level >= 5:
            skills_list.append("absorb heat")

        # granite golem skills
        if self._stone_type == "Granite":
            if self.level >= 5:
                skills_list.append("splinter")
            if self.level >= 10:
                skills_list.append("exploding_shards")
            if self.level >= 15:
                skills_list.append("lightning_rod")

        # obsidian golem skills
        if self._stone_type == "Obsidian":
            if self.level >= 3:
                skills_list.append("harden")
            if self.level >= 10:
                skills_list.append("improved_absorb_heat")
            if self.level >= 15:
                skills_list.append("thermal_core")

        return skills_list

    # passives
    def grounded(self, dmg_type: str) -> int:
        '''Stone Golems are immune to lightning'''
        if dmg_type == "Lightning":
            return 0
        return 1
    
    def ignore_pain(self, damage: int) -> int:
        '''ignore 2 damage from every incoming attack event
            increases by 2 every 10th level (1, 11, 21, 31, 41)'''
        ignore_pain_value = 2 * (self.level // 10 + 1)
        return max(0, damage - ignore_pain_value)

    def absorb_heat(self, dmg_type: str):
        '''improves physical damage offensive mod if hit by fire'''
        if dmg_type == "Fire":
            self._dam_modifiers["Physical"] = min(50, self._dam_modifiers["Physical"] + 10)
    
    # granite golem
    def splinter(self):
        '''splinter off a lesser golem when sum of their parts is triggered'''
        self.has_splinter = True
        self.use_shards = True

    def exploding_shards(self, init_dmg: int) -> int:
        '''deal additional damage w/first attack after splinter'''
        if self.splintered_flag:
            add_dmg = init_dmg
            self.splintered_flag = False
            return init_dmg + add_dmg
        return init_dmg

    def lightning_rod(self) -> CombatAction:
        '''one-time use: calls lightning bolt every time an action is taken'''
        if not self.used_lightning_rod:
            self.used_lightning_rod = True
            msg : str = "Granite Golem becomes a lightning rod, calling down bolts of electricity with each action."
            return CombatAction([("Status Effect", "Lightning Rod", "Special", msg)], "")

    # obsidian golem
    def harden(self):
        '''Improves defensive Physical modifier when taking an action'''
        self._def_modifiers["Physical"] = min(self._def_modifiers["Physical"] + 5, 40)
        self.hardened = True

    def improved_absorb_heat(self, dmg_type: str):
        '''Enhanced version of absorb_heat for Obsidian Golems'''
        if dmg_type == "Fire":
            self._dam_modifiers["Physical"] = min(self._dam_modifiers["Physical"] + 10, 70)
            self.defense_power *= 0.95
            self.attack_power *= 1.10
            self.hardened = False
    
    def thermal_core(self) -> CombatAction:
        '''Ignites the Obsidian Golem, affecting actions and incoming damage'''
        if not self.thermal_core_used:
                self.thermal_core_used = True
                self.ignite_flag = True
                msg : str = "Obsidian Golem's core overheats, adding fire damage to its actions and making it vulnerable to additional fire damage."
                return CombatAction([("Status Effect", "Thermal Core", "Special", msg)], "")

    def attack(self) -> CombatAction:
        '''Stone Golem attack deals physical damage based on its attack power'''
        
        damage = self.golem_damage(self.modify_damage(self._attack_power))
        actions = []

        # Check for splinter
        if self.has_splinter:
            splinter_damage = int(damage * 0.33)
            actions.append(("Splinter", splinter_damage, "Physical", "Splinter deals <value> additional physical damage"))
            damage += splinter_damage

        # Check for exploding shards
        if self.use_shards:
            shard_damage = int(damage * 1)
            actions.append(("Exploding Shards", shard_damage, "Physical", "Shards explode for <value> additional physical damage"))
            damage += shard_damage
            self.use_shards = False

        # Check for thermal core
        if self.ignited:
            add_fire_dmg = int(self.level * 0.5)
            actions.append(("Thermal Core", add_fire_dmg, "Fire", "Thermal core adds <value> fire damage"))
            damage += add_fire_dmg

        main_attack_message = f"{self.name} attacks for <value> physical damage"
        actions.append(("Main Attack", damage, "Physical", main_attack_message))

        return CombatAction(actions, "")


    def take_damage(self, damage: int, dmg_type: str, message : str) -> bool:
        # Stone Golems are immune to lightning damage
        if dmg_type == "Lightning":
            damage = self.grounded(dmg_type)
        
        # Ignore a certain amount of damage based on level
        damage = self.ignore_pain(damage)
        
        # Process fire damage to improve Physical damage modifiers
        if dmg_type == "Fire":
            self.absorb_heat(dmg_type)

        return super().take_damage(damage, dmg_type, message)

    def special_skill(self) -> CombatAction:
        '''return special attack per golem type'''
        if self._stone_type == "Granite":
            return self.lightning_rod()
        elif self._stone_type == "Obsidian":
            return self.thermal_core()

    def take_turn(self) -> CombatAction:
        '''Takes turn and returns the action'''
        options = [self.attack, self.special_skill]
        return choice(options)()