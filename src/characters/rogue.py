'''Module for the Dungeon Dudes Rogue Class'''
from typing import Dict, Tuple, List
from random import gauss, randint
from math import floor
from .character_abc import Character
from ..combatant_abc import Combatant
from .equipment import Equipment, Weapon, Armor, Accessory
from ..dd_data import LimitedDict, damage_types, CombatPrint
from ..combat_action import CombatAction
from .rogue_src import RogueEquipmentGenerator


class Rogue(Character):
    '''Rogue Character Class'''
    stats_structure: Dict[str, Tuple[int]] = {"Hit Points": (75, 18),
                                              "Strength": (10, 1),
                                              "Agility": (12, 2),
                                              "Intelligence": (5, 1),
                                              "Special": (1, 0)}
    item_compatibility: list = ["Dagger", "Medium", "Thieves Tools"]

    def __init__(self, name: str):
        self.damage_types = damage_types

        self.skills_dict: Dict[int, List[str, 'function']] = {
            1: ["Luck", self.luck],
            3: ["Preparation", self.preparation],
            10: ["Evasion", self.evasion],
            13: ["Ambush", self.ambush],
            17: ["Increase Luck", self.increase_luck],
        }
        thieves_tricks = '''Passive: Rogues gain 30% more gold from '''\
            '''winning a battle.'''
        healing_potion_affinity = '''Passive: Using a Healing_Potion '''\
            '''during combat also gives the Rogue time to coat their '''\
            '''weapon in poison.  Rogues have a percentage chance '''\
            '''equal to their level * 1.5 to find a '''\
            '''Healing_Potion after winning a battle.'''
        surprise_attack = '''Passive: The first Attack each turn a Rogue '''\
            '''does deals 50% increased damage and lowers the enemies '''\
            '''Poison defensive modifier by an amount equal to the '''\
            '''Rogue’s level.'''
        auto_potion = '''Passive: Rogues automatically consume a '''\
            '''Healing_Potion on their first action in combat.  If the '''\
            '''Rogue is at maximum hit points, no "Healing_Potion" '''\
            '''is consumed but the Rogue gains all other benefits '''\
            '''of Healing Potion Affinity'''
        enhanced_abilities = '''Passive: Base modifier adjustment of '''\
            '''Preparation is increased to 20, Surprise Attack now '''\
            '''increases damage 75%, Evasion has a base avoidance '''\
            '''chance of 60% and lasts for 3 damage events. '''\
            '''Ambush now deals additional damage equal to '''\
            '''the Rogue’s agility, Increased Luck now '''\
            '''does 85% of Normal Damage.'''
        self.passive_skills = {
            1: ["Theives Tricks", thieves_tricks],
            5: ["Healing Potion Affinity", healing_potion_affinity],
            8: ["Surprise Attack", surprise_attack],
            20: ["Auto-Potion", auto_potion],
            25: ["Enhanced Abilities", enhanced_abilities]
        }
        self.printer = CombatPrint()
        self._weapon: Weapon = None
        self._armor: Armor = None
        self._accessory: Accessory = None
        self._def_modifiers = LimitedDict(self.damage_types, default_value=100)
        self._dam_modifiers = LimitedDict(("Physical", "Poision"),
                                          default_value=100)
        self._equipment_generator = RogueEquipmentGenerator()
        super().__init__(name, "Rogue", self.stats_structure,
                         self.item_compatibility)
        self._exp_to_next_iter = iter([(35 * i ** 2) for i in range(1, 50)])
        self._exp_to_next: int = next(self._exp_to_next_iter)
        self._hit_points: int = self.stats_structure["Hit Points"][0]
        self._special: int = 1
        self._special_resource: str = "Luck"
        self._accessory_type: str = "Thieves Tool"
        self._empowered: bool = False
        self._poison_coated: bool = False
        self._surprise_attack_left: bool = True
        self._ambush_left: bool = True
        self._evasion_active: bool = False
        self._evasion_count: int = 0
        self._evasion_chance: int = 0
        self._auto_potion_active: bool = False
        self._first_action: bool = True
        self._enhanced_abilities_on: bool = False

    def adjust_offensive_mod(self, modifiers: list, remove=False):
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
            att_dif: int = new.item_stats[0] - old.item_stats[0]
            def_dif: int = new.item_stats[1] - old.item_stats[1]
            return att_dif, def_dif
        return new.item_stats[0], new.item_stats[1]

    def att_def_adjust(self, item: Equipment):
        '''Adjusts attack and defense power based on new Equipment'''
        if isinstance(item, Weapon):
            att_dif, def_dif = self.att_def_dif(item, self._weapon)
            self.adjust_offensive_mod(item.damage_modifiers)
            if isinstance(self._weapon, Weapon):
                self.adjust_offensive_mod(self._weapon.damage_modifiers,
                                          remove=True)
        elif isinstance(item, Armor):
            att_dif, def_dif = self.att_def_dif(item, self._armor)
            self.adjust_defensive_mod(item.defense_modifiers)
            if isinstance(self._armor, Armor):
                self.adjust_defensive_mod(self._armor.defense_modifiers,
                                          remove=True)
        elif isinstance(item, Accessory):
            att_dif, def_dif = self.att_def_dif(item, self._accessory)
            self.adjust_offensive_mod(item.damage_modifiers)
            self.adjust_defensive_mod(item.defense_modifiers)
            if isinstance(self._accessory, Accessory):
                self.adjust_offensive_mod(self._accessory.damage_modifiers,
                                          remove=True)
                self.adjust_defensive_mod(self._accessory.defense_modifiers,
                                          remove=True)
        self._attack_power += att_dif
        self._defense_power += def_dif

    def base_att_def_power(self):
        '''Base attack and defense power'''
        self._attack_power = self.strength + self.agility
        self._defense_power = self.agility // 2

    def modify_damage(self, damage) -> int:
        '''Adds Variance to Damage Events'''
        return damage + floor(max(0, min(damage * 0.24, gauss(damage * 0.08,
                                                              damage * 0.04))))

    def poison_attack(self, base_damage) -> Tuple[str, int, str, str]:
        '''Returns a tuple for poison damage'''
        modified: int = self.modify_damage(base_damage)
        message: str = (f"{self.weapon} is coated with poison, "
                        "inflicting additional <value> poison damage")
        return ("Attack", modified, "Poison", message)

    def attack(self) -> CombatAction:
        '''Does Damage Based on Attack Power'''
        self.auto_potion()
        actions: List[tuple] = []
        if self._empowered:
            damage: int = self.modify_damage(int(self._attack_power * 1.24))
            message: str = (f"{self.name} attacks with {self.weapon} "
                            "for <value> EMPOWERED "
                            f"{self._weapon.damage_type} damage")
            self._empowered = False
        else:
            damage: int = self.modify_damage(self._attack_power)
            message: str = (f"{self.name} attacks with {self.weapon} "
                            f"for <value> {self._weapon.damage_type} damage")
        if self.level >= 8 and self._surprise_attack_left:
            if self._enhanced_abilities_on:
                damage = int(damage * 1.75)
            else:
                damage = int(damage * 1.5)
            self.printer(f"{self.name} Prepares for a surprise attack")
        actions.append(("Attack", damage, self._weapon.damage_type, message))
        if self._poison_coated:
            actions.append(self.poison_attack(self.intelligence))
        if self.level >= 8 and self._surprise_attack_left:
            self._surprise_attack_left = False
            actions.append(("Hex", self.level, "Poison", ""))
        return CombatAction(actions, "")

    def luck(self) -> [bool, CombatAction]:
        '''Empower next ability'''
        if self._special == 0:
            self.printer((f"{self.name} exhausted all lucks. "
                          "Unable to perform the action."))
            return False, CombatAction([("Aura", 0, "Physical", "")], "")
        self.auto_potion()
        message: str = f"{self.name} uses a luck to empower next ability."
        self._special -= 1
        self._empowered = True
        self.printer(message)
        return False, CombatAction([("Aura", 0, "Physical", "")], "")

    def preparation(self) -> [bool, CombatAction]:
        '''Analayze the battlefield, gaining 10 physical and poison damage '''\
            '''modifiers, and coating weapon in poison. Increase damage '''\
            '''modifiers by 5 if the weapon is arealdy coated. '''\
            '''Empower: Prepartion also Identify the enemy.'''
        self.auto_potion()
        if self._enhanced_abilities_on:
            physical_modifier = 20
            poison_modifier = 20
        else:
            physical_modifier = 10
            poison_modifier = 10
        # Weapon coated in poison
        if self._poison_coated:
            poison_modifier += 5
        # Coat weapons in poison
        self._poison_coated = True
        self.printer((f"{self.name} Prepares for the battle: "
                      f"Physical + Poison Damage UP, Coats Weapon in Poison"))
        actions: List[tuple] = [("Battle Cry", physical_modifier,
                                 "Physical", ""),
                                ("Battle Cry", poison_modifier, "Poison", "")]
        # Empowered
        if self._empowered:
            self.printer("Empowered: Identifying the enemy!")
            actions.append(("Identify", 0, "", ""))
        return True, CombatAction(actions, "")

    def use_healing_potion(self) -> Tuple[bool, CombatAction]:
        '''Uses a Healing Potion and Returns the Current Combat Action'''
        printer = CombatPrint()
        success = True
        if self.hit_points == self.max_hit_points:
            printer("Cannot Use Healing Potion, already at Max Health")
            success = False
        elif self._healing_potion == 0:
            printer("Cannot Use Healing Potion, No Healing Potions Left")
            success = False
        if not success:
            return success, CombatAction([("Heal", 0, "Holy", "")], "")
        current = self.hit_points
        heal_amount = int(self.max_hit_points * 0.45)
        self.hit_points += heal_amount
        self._healing_potion -= 1
        printer(("Drank a healing Potion and healed "
                 f"{self.hit_points - current} Hit Points"))
        # Healing Potion Affinity passive
        if self.level >= 5:
            printer(("Healing Potion Affinity Passive: "
                     f"Coated {self.weapon} in poison"))
            self._poison_coated = True
        return success, CombatAction([("Heal", heal_amount, "Holy")], "")

    def evasion(self) -> [bool, CombatAction]:
        '''50 % chance to avoid 100% of the damage for next two events'''
        self.auto_potion()
        self._evasion_active = True
        if self._enhanced_abilities_on:
            self._evasion_count = 3
            self._evasion_chance = 60
        else:
            self._evasion_count = 2
            self._evasion_chance = 50
        if self._empowered:
            self.printer("Empowered: Increasing evasion number and chance")
            self._evasion_count += 1
            self._evasion_chance += 10
            self._empowered = False
        self.printer((f"{self.name} Prepares to evade next "
                      f"{self._evasion_count} damage events with "
                      f"{self._evasion_chance} % chance"))
        return True, CombatAction([("Aura", 0, "Physical", "")], "")

    def ambush(self) -> [bool, CombatAction]:
        '''Once per battle, rogue attacks for damage equal to attack power '''\
            '''+ agility + strength. Consumes surprise attack'''
        self.auto_potion()
        base_damage = self._attack_power + self.agility + self.strength
        if self._enhanced_abilities_on:
            base_damage += self.agility
        damage: int = self.modify_damage(base_damage)
        message: str = f"{self.name} Ambushes for <value> damage"
        actions: List[tuple] = [("Attack", damage, "Physical", message)]
        if self._poison_coated:
            if self._empowered:
                self.printer(("Empowered: Dealing x3 times the base "
                              "poison damage"))
                actions.append(self.poison_attack(self.intelligence * 3))
                self._empowered = False
            else:
                actions.append(self.poison_attack(self.intelligence))
        self._empowered = False
        self._surprise_attack_left = False
        self._ambush_left = False
        return True, CombatAction(actions, "")

    def increase_luck(self) -> [bool, CombatAction]:
        '''Deal an attack with 70 % base damage, and gets 1 Luck'''
        self.auto_potion()
        if self._special < self.max_special:
            self.printer(f"{self.name} Prays to gain a luck")
            self._special += 1
        else:
            self.printer(f"{self.name} already has max Luck")
        base_modifier = 0.7
        if self._enhanced_abilities_on:
            base_modifier += 0.15
        base_attack = int(base_modifier * self._attack_power)
        damage = self.modify_damage(base_attack)
        message: str = (f"{self.name} quickly attacks "
                        f"for <value> {self._weapon.damage_type} damage "
                        f"while praying")
        actions: List[tuple] = [("Attack", damage, "Physical", message)]
        if self._poison_coated:
            actions.append(self.poison_attack(self.intelligence))
        return True, CombatAction(actions, "")

    def auto_potion(self):
        '''Execute Auto Potion passive'''
        if not self._auto_potion_active:
            return
        if not self._first_action:
            return
        self.printer("Auto-Potion Passive Activated!")
        if self.hit_points == self.max_hit_points:
            self.printer("Auto-Potion: Coating weapon in poison")
            self._poison_coated = True
            self._first_action = False
            return
        if self._healing_potion == 0:
            self.printer("Auto-Potion: No Healing Potions Left")
            self._first_action = False
            return
        current = self.hit_points
        heal_amount = int(self.max_hit_points * 0.45)
        self.hit_points += heal_amount
        self._healing_potion -= 1
        self.printer(("Drank a Healing Potioin and healed "
                      f"{self.hit_points - current} Hit Points"))
        self._first_action = False
        return

    def level_up(self, combat=False):
        super().level_up(combat=combat)
        luck_growth_rate: int = 2
        if self._level in self.skills_dict:
            skill: str = self.skills_dict[self._level][0]
            description: str = self.skills_dict[self._level][1].__doc__
            description: str = "\n".join(line.strip() for line
                                         in description.splitlines())
            if combat:
                self.printer(f'New Skill - {skill}:', description)
            else:
                print(f'\nNew Skill - {skill}:', description)
        if self._level in self.passive_skills:
            skill: str = self.passive_skills[self._level][0]
            description: str = self.passive_skills[self._level][1]
            description: str = "\n".join(line.strip() for line
                                         in description.splitlines())
            if combat:
                self.printer(f'New Skill - {skill}:', description)
            else:
                print(f'New Skill - {skill}:', description)
        if self._level % luck_growth_rate == 0:
            self._stats.special += 1
            self.special += 1
        self._attack_power += 3
        if self.agility % 2 == 0:
            self._defense_power += 1
        self._poison_coated = False
        if self._level >= 20:
            self._auto_potion_active = True
        if self._level >= 25:
            self._enhanced_abilities_on = True

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

    @property
    def empowered(self) -> bool:
        '''Getter for Empowered status'''
        return self._empowered

    @property
    def poison_coated(self) -> bool:
        '''Getter for Poison coating status'''
        return self._poison_coated

    @property
    def surprise_attack_left(self) -> bool:
        '''Getter for Surprise attack status'''
        return self._surprise_attack_left

    @property
    def ambush_left(self) -> bool:
        '''Getter for Ambush status'''
        return self._ambush_left

    @property
    def evasion_active(self) -> bool:
        '''Getter for Evasion status'''
        return self._evasion_active

    @property
    def evasion_count(self) -> int:
        '''Getter for Evasion count'''
        return self._evasion_count

    @property
    def evasion_chance(self) -> int:
        '''Getter for Evasion Chance'''
        return self._evasion_chance

    @property
    def auto_potion_active(self) -> bool:
        '''Getter for Auto Potioin status'''
        return self._auto_potion_active

    @property
    def first_action(self) -> bool:
        '''Getter for First Action status'''
        return self._first_action

    @property
    def enhanced_abilities_on(self) -> bool:
        '''Getter for Enhanced Abilities status'''
        return self._enhanced_abilities_on

    def take_damage(self, damage: int,
                    dmg_type: str,
                    message: str) -> bool:  # pylint: disable=unused-argument
        '''Processes Damage Events'''
        alive = True
        if dmg_type == "Physical":
            damage = damage - (self._defense_power // 2)
        damage = int(damage * self._def_modifiers[dmg_type]/100)
        if damage > 1 and self._evasion_active:
            if randint(0, 99) < self._evasion_chance:
                self.printer((f"{self.name} succssfully evaded "
                              f"incoming {damage} damage"))
                self._evasion_count -= 1
                if self._evasion_count == 0:
                    self.printer("Losing focus. Evasion fades off")
                    self._evasion_active = False
                    self._evasion_chance = 0
                return alive
            else:
                self.printer(f"{self.name} Failed to evade...")
                self._evasion_count -= 1
                if self._evasion_count == 0:
                    self.printer("Losing focus. Evasion fades off")
                    self._evasion_active = False
                    self._evasion_chance = 0
        if damage >= self.hit_points:
            message = message.replace('<value>', str(self._hit_points))
            self._hit_points = 0
            self.printer(message)
            self.character_death(combat=True)
            alive = False
            return alive
        damage = max(1, damage)
        self._hit_points -= damage
        message = message.replace('<value>', str(damage))
        self.printer(message)
        return alive

    def get_skills(self) -> Dict[str, 'function']:
        '''Gets Skills Learned'''
        skills_list_filter: dict = ({skill_info[0]: skill_info[1]
                                    for level_learned, skill_info in
                                    self.skills_dict.items() if
                                    level_learned <= self.level})
        if not self._ambush_left:
            del skills_list_filter["Ambush"]
        return skills_list_filter

    def get_skills_list(self) -> List[str]:
        '''Returns List of Skills Learned'''
        skills_list_filter: list = ([skill_info[0] for level_learned,
                                    skill_info in self.skills_dict.items() if
                                    level_learned <= self.level])
        return skills_list_filter

    def win_battle(self, combatant: Combatant):
        '''Instructors for Wining a Battle'''
        if isinstance(combatant, Combatant):
            exp = combatant.experience_points
            # Thieves Tricks - 30 % more gold from winning a battle
            self.printer("Thieves Trick Passive: Gaining 30% more gold")
            gold = combatant.gold + int(combatant.gold * 0.3)
            name = combatant.name
            self._battles_won += 1
            self._poison_coated = False
            self._empowered = False
            self._evasion_active = False
            self._surprise_attack_left = True
            self._first_action = True
            self._ambush_left = True
            self.printer((f"You have defeated {name}! "
                          f"Gained {gold} Gold. "
                          f"Gained {exp} Experience"))
            self._gold += gold
            self.gain_experience(exp, combat=True)
            # Healing potion affinity passive
            if self._level >= 5:
                random_int = randint(0, 99) * 10
                chance_for_potion = self.level * 15
                if random_int < chance_for_potion:
                    self.printer(("Healing Potion Affinity Passive: "
                                  "Lucky! You found a healing potion!"))
                    self.healing_potion = self.healing_potion + 1

    def generate_weapon(self) -> Weapon:
        '''Generates a suitable Weapon Equipment Item based on level'''
        return self._equipment_generator.generate_weapon(self._level)

    def generate_armor(self) -> Armor:
        '''Generates a suitable Armor Equipment Item based on level'''
        return self._equipment_generator.generate_armor(self._level)

    def generate_accessory(self) -> Accessory:
        '''Generates a suitable Armor Equipment Item based on level'''
        return self._equipment_generator.generate_accessory(self._level)
