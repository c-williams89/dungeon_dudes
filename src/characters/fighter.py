'''Module for the Dungeon Dudes Fighter Class'''
from typing import Dict, Tuple, List
from random import gauss, randint
from math import floor
from .character_abc import Character
from ..combatant_abc import Combatant
from .equipment import Equipment, Weapon, Armor, Accessory
from ..dd_data import LimitedDict, damage_types, CombatPrint
from ..combat_action import CombatAction
from .fighter_src import FighterEquipmentGenerator

class Fighter(Character):
    '''Fighter Character Class'''
    stats_structure : Dict[str, Tuple[int]]= {"Hit Points": (100, 25), "Strength": (13, 2),
                        "Agility" : (10, 1), "Intelligence" : (5, 0), "Special": (1,0)}
    item_compatibility : list = ["Sword", "Axe", "Mace", "Heavy", "Shield"]
    def __init__(self, name : str):
        self.damage_types = damage_types

        self.skills_dict : Dict[int, List[str, 'function']]= {
            3 : ["Whirlwind", self.whirlwind],
            10 : ["Fortify", self.fortify],
            13 : ["Weaken", self.weaken],
            17 : ["Strengthen", self.strengthen],
            25 : ["Rampage", self.rampage]
        }
        critical_strikes = '''Passive: Your physical damage attack and abilities have a'''\
            '''10% to deal double damage.'''
        second_wind = '''Passive: You heal for 25 percent of your Maximum Hit Points '''\
            '''whenever you defeat an enemy'''
        improved_critical = '''Passive: Your Critical Strikes now do x3 Damage (was x2)'''
        self.passive_skills = {
           5 : ["Critical Strikes", critical_strikes],
           8 : ["Second Wind", second_wind],
           20: ["Improved Critical Strikes", improved_critical]
        }
        self.printer = CombatPrint()
        self._weapon : Weapon = None
        self._armor : Armor = None
        self._accessory : Accessory = None
        self._def_modifiers = LimitedDict(self.damage_types, default_value=100)
        self._dam_modifiers = LimitedDict("Physical", default_value=100)
        self._equipment_generator = FighterEquipmentGenerator()
        super().__init__(name, "Fighter", self.stats_structure, self.item_compatibility)
        self._exp_to_next_iter = iter([(40 * i ** 2) for i in range(1, 50)])
        self._exp_to_next : int = next(self._exp_to_next_iter)
        self._hit_points : int = self.stats_structure["Hit Points"][0]
        self._special : int = 1
        self._special_resource : str = "Heroism"
        self._accessory_type : str = "Shield"
        self._critical_modifier : int = 1
        self._rampaged : bool = False

    def adjust_offensive_mod(self, modifiers : list, remove=False):
        '''Adjusts Offensive Modifiers from Equipment'''
        if not remove:
            for modifier in modifiers:
                if modifier[0] in self._dam_modifiers:
                    self._dam_modifiers[modifier[0]] += modifier[1]
        else:
            for modifier in modifiers:
                if modifier[0] in self._dam_modifiers:
                    self._dam_modifiers[modifier[0]] -= modifier[1]

    def adjust_defensive_mod(self, modifiers: list, remove=False):
        '''Adjusts Defensive Modifiers from Equipment'''
        if not remove:
            for modifier in modifiers:
                if modifier[0] in self._def_modifiers:
                    self._def_modifiers[modifier[0]] += modifier[1]
        else:
            for modifier in modifiers:
                if modifier[0] in self._def_modifiers:
                    self._def_modifiers[modifier[0]] -= modifier[1]

    @staticmethod
    def att_def_dif(new: Equipment, old: [Equipment, None]) -> Tuple[int, int]:
        '''Gets the Attack Defense Difference when Equipping new Items'''
        if isinstance(old, Equipment):
            att_dif : int = new.item_stats[0] - old.item_stats[0]
            def_dif : int = new.item_stats[1] - old.item_stats[1]
            return att_dif, def_dif
        return new.item_stats[0], new.item_stats[1]

    def att_def_adjust(self, item: Equipment):
        '''Adjusts attack and defense power based on new Equipment'''
        if isinstance(item, Weapon):
            att_dif, def_dif = self.att_def_dif(item, self._weapon)
            self.adjust_offensive_mod(item.damage_modifiers)
            if isinstance(self._weapon, Weapon):
                self.adjust_offensive_mod(self._weapon.damage_modifiers, remove=True)    
        elif isinstance(item, Armor):
            att_dif, def_dif = self.att_def_dif(item, self._armor)
            self.adjust_defensive_mod(item.defense_modifiers)
            if isinstance(self._armor, Armor):
                self.adjust_defensive_mod(self._armor.defense_modifiers, remove=True)    
        elif isinstance(item, Accessory):
            att_dif, def_dif = self.att_def_dif(item, self._accessory)
            self.adjust_offensive_mod(item.damage_modifiers)
            self.adjust_defensive_mod(item.defense_modifiers)
            if isinstance(self._accessory, Accessory):
                self.adjust_offensive_mod(self._accessory.damage_modifiers, remove=True)
                self.adjust_defensive_mod(self._accessory.defense_modifiers, remove=True)
        self._attack_power += att_dif
        self._defense_power += def_dif

    def base_att_def_power(self):
        '''Base attack and defense power'''
        self._attack_power = self.strength
        self._defense_power = self.agility // 2

    def modify_damage(self, damage, auto_crit = False) -> int:
        '''Adds Variance to Damage Events and Calculates Critical Chance'''
        std_dev_percent : int = 0.08
        modified : int = max(floor(gauss(damage, (std_dev_percent * damage))), 1)
        if auto_crit:
            self.printer("Critical Hit!")
            return modified * self._critical_modifier
        elif self._critical_modifier != 1:
            if randint(1,10) == 10:
                self.printer("Critical Hit!")
                return modified * self._critical_modifier

        return modified

    def attack(self) -> CombatAction:
        '''Does Damage Based on Attack Power'''
        damage : int = self.modify_damage(self._attack_power)
        message : str = (f"{self.name} attacks with {self.weapon} "
                         f"for <value> {self._weapon.damage_type} damage")
        return CombatAction([("Attack", damage, self._weapon.damage_type, message)], "")

    def whirlwind(self) ->  [bool, CombatAction]:
        '''Does Physical damage based 75% attack_power to All enemies'''
        damage : int = (2* self._accessory.item_stats[1]) + int((0.75 * self._defense_power))
        damage : int = self.modify_damage(damage)
        message : str = f"{self.name} unleashing a whirlwind hitting all enemies for <value> Physical damage"
        return True, CombatAction([("Attack", damage, "Physical", message)], "")

    def fortify(self) ->  [bool, CombatAction]:
        '''Increase resist to physical and all elemental sources by 0.15 '''\
        '''for the remainder of the encounter'''
        resist_types : List[str] = ["Physical", "Fire", "Ice", "Lightning"]
        aura : List[tuple] = [("Aura", 15, damage_type, "") for damage_type in resist_types]
        self.printer(f"{self.name} Defends and braces against the Elements")
        return True, CombatAction(aura, "")

    def weaken(self) ->  [bool, CombatAction]:
        '''Deal an attack which does half normal damage, Opponents' '''\
        '''physical mitigation modifier is reduced by 0.1 for the remainder of the encounter.'''
        action_type, damage, dmg_type, _ = self.attack().actions[0]
        damage : int = damage // 2
        message : str = (f"Makes a calculated strike for <value> {dmg_type} Damage"
                   f", and weakens the target's physical mitigation")
        return True, CombatAction([(action_type, damage, dmg_type, message),
                                   ("Hex", 10, "Physical", "")], "")

    def strengthen(self) ->  [bool, CombatAction]:
        '''Deal an attack which does half normal damage,'''\
        '''Your physical damage modifier increased by 0.1 for the remainder of the encounter'''
        action_type, damage, dmg_type, _ = self.attack().actions[0]
        damage : int = damage // 2
        message : str = (f"Makes a calculated strike for <value> {dmg_type} Damage"
                   f", and strengthens their future physical attacks")
        return True, CombatAction([(action_type, damage, dmg_type, message),
                             ("Battle Cry", 10, "Physical", "")], "")

    def rampage(self) -> [bool, CombatAction]:
        '''Once per battle: Attack this turn with a 100 percent chance to deal a critical strike'''
        if not self._rampaged:
            self._rampaged : bool = True
            damage : int = self.modify_damage(self._attack_power, auto_crit=True)
            message : str = (f"Rampages, critically striking with {self.weapon}"
                            f" for <value> {self._weapon.damage_type} damage")
            return True, CombatAction([("Attack", damage, self._weapon.damage_type, message)], "")
        self.printer("Ability Failed: Can only use Rampage once per Battle")
        return False, CombatAction([("Attack", 0, "Physical", "")], "")

    def level_up(self, combat=False):
        super().level_up(combat=combat)
        heroism_growth_rate : int = 4
        crit_multiplier_increases = [5, 20]
        if self._level in self.skills_dict:
            skill : str = self.skills_dict[self._level][0]
            description : str = self.skills_dict[self._level][1].__doc__
            description : str = "\n".join(line.strip() for line in description.splitlines())
            if combat:
                self.printer(f'New Skill - {skill}:', description)
            else:
                print(f'\nNew Skill - {skill}:', description)
        if self._level in self.passive_skills:
            skill : str = self.passive_skills[self._level][0]
            description : str = self.passive_skills[self._level][1]
            description : str = "\n".join(line.strip() for line in description.splitlines())
            if combat:
                self.printer(f'New Skill - {skill}:', description)
            else:
                print(f'New Skill - {skill}:', description)
        if self._level in crit_multiplier_increases:
            self._critical_modifier += 1
        if self._level % heroism_growth_rate == 0:
            self._stats.special += 1
            self.special += 1
        self._attack_power += 2
        if self.agility % 2 == 0:
            self._defense_power += 1

    @property
    def special(self) -> int:
        '''Getter for Current Heroism'''
        return self._special

    @property
    def max_special(self) -> int:
        '''Getter for Max Heroism'''
        return self._stats.special

    @special.setter
    def special(self, change):
        '''Setter for Heroism'''
        if change >= self.max_special:
            self._special = self.max_special
        else:
            self._special = change

    @property
    def hit_points(self):
        '''Override Parent Getter for HP'''
        return self._hit_points

    @hit_points.setter
    def hit_points(self, value):
        '''Setter for Hit Points'''
        if value >= self.max_hit_points:
            self._hit_points = self.max_hit_points
        else:
            self._hit_points = int(value)

    @property
    def special_resource(self) -> str:
        '''Getter for Special Resource Name'''
        return self._special_resource

    @property
    def accessory_type(self) -> str:
        '''Getter for Accessory Type for Class'''
        return self._accessory_type

    @property
    def accessory_cost(self) -> int:
        '''Getter for Accessory Cost'''
        return self._accessory.cost

    @property
    def accessory_sheet(self) -> Accessory:
        '''Getter for Accessory Object'''
        return self._accessory

    @property
    def accessory(self) -> str:
        '''Getter for Accessory Name'''
        try:
            return self._accessory.name
        except AttributeError:
            return "None"

    @property
    def damage_modifiers(self) -> LimitedDict:
        '''Getter for Damage Modifiers'''
        return self._dam_modifiers

    @property
    def defense_modifiers(self) -> LimitedDict:
        '''Getter for Defense Modifiers'''
        return self._def_modifiers

    def trigger_heroism(self, damage: int):
        '''Triggers Heroism to Prevent Character Death'''
        self._special -= 1
        self._hit_points = self.max_hit_points // 4
        self.printer(f"Incoming Damage {damage} greater than current Hit Points: {self.hit_points}")
        self.printer(f"Heroism Consumed, {self._special} remaining.",
            f"Hit Points set to: {self._hit_points}")

    def take_damage(self, damage: int, dmg_type : str, message : str) -> bool: # pylint: disable=unused-argument
        '''Processes Damage Events'''
        alive = True
        if dmg_type == "Physical":
            damage = damage - (self._defense_power // 2)
        damage = int(damage * self._def_modifiers[dmg_type]/100)
        if damage >= self.hit_points:
            if self._special > 0:
                message = message.replace('<value>', str(damage))
                self.printer(message)
                self.trigger_heroism(damage)
                return alive
            else:
                message = message.replace('<value>', str(self._hit_points))
                self._hit_points = 0
                self.printer(message)
                self.character_death(combat=True)
                alive = False
                return alive
        self._hit_points -= damage
        message = message.replace('<value>', str(damage))
        self.printer(message)
        return alive

    def get_skills(self) -> Dict[str, 'function']:
        '''Gets Skills Learned'''
        skills_list_filter : dict = ({skill_info[0]:skill_info[1] for level_learned, skill_info in
                               self.skills_dict.items() if level_learned <= self.level})
        if self._rampaged:
            del skills_list_filter["Rampage"]
        return skills_list_filter

    def get_skills_list(self) -> List[str]:
        '''Returns List of Skills Learned'''
        skills_list_filter : list = ([skill_info[0] for level_learned, skill_info in
                               self.skills_dict.items() if level_learned <= self.level])
        return skills_list_filter

    def win_battle(self, combatant : Combatant):
        '''Instructors for Wining a Battle'''
        if isinstance(combatant, Combatant):
            exp, gold, name = combatant.experience_points, combatant.gold, combatant.name
            self._battles_won += 1
            self._rampaged = False
            self.printer(f"You have defeated {name}!  Gained {gold} Gold.  Gained {exp} Experience")
            if self._level >= 8:
                current = self.hit_points
                self.hit_points += floor(self.max_hit_points * .25)
                self.printer(f"You heal {self.hit_points - current} hit points from Second Wind")
            self._gold += gold
            self.gain_experience(exp, combat=True)

    def generate_weapon(self) -> Weapon:
        '''Generates a suitable Weapon Equipment Item based on level'''
        return self._equipment_generator.generate_weapon(self._level)

    def generate_armor(self) -> Armor:
        '''Generates a suitable Armor Equipment Item based on level'''
        return self._equipment_generator.generate_armor(self._level)

    def generate_accessory(self) -> Accessory:
        '''Generates a suitable Armor Equipment Item based on level'''
        return self._equipment_generator.generate_accessory(self._level)
