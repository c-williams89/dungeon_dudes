'''Placeholder Module for Cleric Class'''
from typing import Dict, Tuple, List
from random import gauss, randint
from math import floor
from .character_abc import Character
from ..combatant_abc import Combatant
from .equipment import Equipment, Weapon, Armor, Accessory
from ..dd_data import LimitedDict, damage_types, CombatPrint
from ..combat_action import CombatAction
from .cleric_src import ClericEquipmentGenerator


class Cleric(Character):
    '''Cleric Class for Dungeon Dudes'''
    stats_structure: Dict[str, Tuple[int]] = {"Hit Points": (85, 20),
                                              "Strength": (13, 1),
                                              "Agility": (10, 1),
                                              "Intelligence": (10, 1),
                                              "Special": (50, 15)}
    item_compatibility: list = ["Mace", "Flail", "Heavy", "Holy Symbol"]

    def __init__(self, name: str):
        self.damage_types = damage_types
        self.skills_dict: Dict[int, List[str, 'function']] = {
            1:  ["Heal", self.heal],
            3:  ["Radiance", self.radiance],
            8:  ["Prayer", self.prayer],
            13: ["Avenger", self.avenger],
            17: ["Greater Heal", self.greater_heal]
        }

        armor_of_faith = '''Passive: Your defense power protects against '''\
            '''Holy Damage in addition to Physical damage.'''
        smite = '''Passive: You will deal additional Holy damage based on '''\
            '''33percent of your Intelligence stat.'''
        divine_blessing = '''Passive: When you take action in combat, you '''\
            '''will recover 10percent of your maximium HP when at full '''\
            '''Mana, and 10percent of your maximum mana when at full '''\
            '''Hit Points.'''
        retribution = '''Passive: Attacks on you deal (Level/5) less '''\
            '''damage, and your Holy damage is increased by (Level/10) '''\
            '''for the rest of the battle.'''
        battle_cleric = '''Passive: Smite now deals damage of '''\
            '''(Intelligence/2). Smite will also trigger when any '''\
            '''Healing spell is Activated'''
        improved_healing = '''Passive: When above 50percent Mana, '''\
            '''Heal and Greater heal consume 100percent more Mana '''\
            '''and deal Holy damage equal to the number of HP healed.'''

        self.passive_skills = {
            1:  ["Armor of Faith", armor_of_faith],
            1:  ["Smite", smite],
            5:  ["Divine Blessing", divine_blessing],
            10: ["Retribution", retribution],
            20: ["Battle Cleric", battle_cleric],
            25: ["Improved Healing", improved_healing]
        }

        self.printer = CombatPrint()
        self._weapon: Weapon = None
        self._armor: Armor = None
        self._accessory: Accessory = None
        self._def_modifiers = LimitedDict(self.damage_types, default_value=100)
        self._dam_modifiers = LimitedDict("Physical", default_value=100)

        self._equipment_generator = ClericEquipmentGenerator()
        super().__init__(name, "Cleric", self.stats_structure,
                         self.item_compatibility)

        self._exp_to_next_iter = iter([(40 * i ** 2) for i in range(1, 50)])
        self._exp_to_next: int = next(self._exp_to_next_iter)
        self._hit_points: int = self.stats_structure["Hit Points"][0]
        self._special: int = 50
        self._special_resource: str = "Mana"
        self._accessory_type: str = "Holy Symbol"
        self._avenged: bool = False
        self._nodamage: bool = False
        self._halfdamage: bool = False
        self._retribution: bool = False
        self._smite_multi: int = 3
        self._smite_damage: int = int(self.intelligence / self._smite_multi)
        self._battle_smite = ("Attack", self._smite_damage, "Holy",
                              f"{self.name}'s Smite deals an " +
                              "additional <value> damage!")

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
        self._attack_power = self.strength
        self._defense_power = self.agility // 2

    def modify_damage(self, damage) -> int:
        '''Adds Variance to Damage Events and Calculates Critical Chance'''
        std_dev_percent: int = 0.12
        modified: int = max(floor(gauss(damage,
                                        (std_dev_percent * damage))), 1)

        return modified

    def divine_blessing(self) -> None:
        '''Passive: When you take action in combat, you will recover '''
        ''' 10percent of your maximium HP when at full Mana, and '''
        ''' 10percent of your maximum mana when at full Hit Points.'''
        if self._level >= 5:
            if self.special == self.max_special:
                self.hit_points += int(self.max_hit_points * 0.10)
                self.printer(f"A Blessing! A Blessing from the Lord!",
                             f"{self.name} recovered",
                             f"{int(self.max_hit_points * 0.10)} HP",
                             "from Divine Blessing!")
            if self.hit_points == self.max_hit_points:
                self.special += int(self.max_special * 0.10)
                self.printer(f"A Blessing! A Blessing from the Lord!",
                             f"{self.name} recovered",
                             f"{int(self.max_special * 0.10)} Mana",
                             "from Divine Blessing!")

    def improved_healing(self, special_cost: int) -> None:
        '''Passive: When above 50percent Mana, '''
        '''Heal and Greater heal consume 100percent more Mana '''
        '''and deal Holy damage equal to the number of HP healed.'''
        if self.level >= 25 and (self.special > (self.max_special * 0.5)):
            msg: str = "Holy Damage of <value> caused by Improved Healing!"
            return ("Attack", self.modify_damage(special_cost), "Holy", msg)
        else:
            return ("Heal", 0, "Holy", "")

    def attack(self) -> CombatAction:
        '''Does Damage Based on Attack Power'''
        damage: int = max(1, self.modify_damage(self._attack_power))
        msg: str = (f"{self.name} attacks with {self.weapon} " +
                    f"for <value> {self._weapon.damage_type} damage!")
        self.divine_blessing()
        return CombatAction([("Attack", damage,
                            self._weapon.damage_type, msg),
                            self._battle_smite], "")

    def heal(self) -> [bool, CombatAction]:
        '''Heals for 50% of Max HP'''
        special_cost = 20
        if self.level >= 25 and (self.special > (self.max_special * 0.5)):
            special_cost *= 2

        if self.special >= special_cost:
            current = self.hit_points
            heal_amount = int(self.max_hit_points * 0.45)
            self.hit_points += heal_amount
            amount_healed = self.hit_points - current
            if amount_healed > 0:
                msg: str = (f"{self.name} healed {amount_healed} HP" +
                            f" for {special_cost} Mana!")
                self.special -= special_cost
                self.printer(msg)
                self.divine_blessing()
                improved_healing_atk = self.improved_healing(special_cost)
                if self.level >= 25:
                    battle_smite = self._battle_smite
                else:
                    battle_smite = ("Heal", 0, "Holy", "")
                return True, CombatAction([("Heal", amount_healed, "", ""),
                                           battle_smite,
                                           improved_healing_atk], "")
            else:
                self.printer("Heal Failed: Already at Full Health!")
                return False, CombatAction([("Heal", 0, "Holy", "")], "")

        else:
            self.printer("Heal Failed: Not Enough Mana Remaining")
            return False, CombatAction([("Heal", 0, "Holy", "")], "")

    def radiance(self) -> [bool, CombatAction]:
        '''Deal Holy damage to all enemies for Intelligence + AtkPower'''
        '''Heal HP by Intelligence//3'''
        special_cost = 40
        if self.special >= special_cost:
            damage: int = max(1, self.modify_damage(self.intelligence +
                                                    self._attack_power))
            healed = self.intelligence//3
            amt_healed = ((self.hit_points + (healed)) %
                          self.max_hit_points)
            self.hit_points = (min(self.max_hit_points,
                                   (self.hit_points + amt_healed)))
            msg: str = (f"{self.name} unleashing Radiance hitting all" +
                        f" enemies for <value> Holy dmg. Heals {healed}!")
            self.special -= special_cost
            self.divine_blessing()
            return True, CombatAction([("Attack", damage, "Holy", msg),
                                       self._battle_smite], "")

        else:
            self.printer("Radiance Failed: Not Enough Mana Remaining")
            return False, CombatAction([("Heal", 0, "Holy", "")], "")

    def prayer(self) -> [bool, CombatAction]:
        '''Protects self with incantation, raise defense modifier to'''
        '''Holy, Poison, and Physical by 5'''
        '''Reduce the Damage from the Next Damage Event to 0'''
        special_cost = 30
        if self.special >= special_cost:
            msg: str = (f"{self.name} performs a Prayer, increasing their" +
                        " defenses by 5! Next Damage will be Zero!")
            self._nodamage = True
            self.special -= special_cost
            self.printer(msg)
            return True, CombatAction([("Aura", -5, "Holy", ""),
                                       ("Aura", -5, "Poison", ""),
                                       ("Aura", -5, "Physical", "")
                                       ], "")

        else:
            self.printer("Prayer Failed: Not Enough Mana Remaining")
            return False, CombatAction([("Heal", 0, "Holy", "")], "")

    def avenger(self) -> [bool, CombatAction]:
        '''(Once per Battle) Increase Holy Damage Modifier by 30'''
        ''' Deal Intelligence * 6 Holy Damage'''
        special_cost = 100
        if self.special >= special_cost:
            if self._avenged is False:
                damage: int = max(1, self.modify_damage(self.intelligence * 6))
                msg = (f"Avenger Cleric {self.name} unleashes their" +
                       " wrinkly-brain intellect powers for <value> damage. " +
                       "Increases their Holy Damage by 30!")
                self.divine_blessing()
                self._avenged = True
                self.special -= special_cost
                return True, CombatAction([("Attack", damage, "Holy", msg),
                                           ("Battle Cry", 30, "Holy", ""),
                                           self._battle_smite], "")
            else:
                self.printer("Avenger Failed: Can only use ",
                             "Avenger once per Battle")
                return False, CombatAction([("Heal", 0, "Holy", "")], "")
        else:
            self.printer("Avenger Failed: Not Enough Mana Remaining")
            return False, CombatAction([("Heal", 0, "Holy", "")], "")

    def greater_heal(self) -> [bool, CombatAction]:
        """Heal for 70% of Max HP, Reduce next incoming Damage Event by 50%"""
        special_cost = 50
        if self.level >= 25 and (self.special > (self.max_special * 0.5)):
            special_cost *= 2

        if self.special >= special_cost:
            current = self.hit_points
            heal_amount = int(self.max_hit_points * 0.45)
            self.hit_points += heal_amount
            amount_healed = self.hit_points - current
            if amount_healed > 0:
                msg: str = (f"{self.name} greatly healed {amount_healed} HP" +
                            f" for {special_cost} Mana!")
                self.special -= special_cost
                self.printer(msg)
                self._halfdamage = True
                self.divine_blessing()
                improved_healing_atk = self.improved_healing(special_cost)
                if self.level >= 25:
                    battle_smite = self._battle_smite
                else:
                    battle_smite = ("Heal", 0, "Holy", "")
                return True, CombatAction([("Heal", amount_healed, "", msg),
                                           battle_smite,
                                           improved_healing_atk], "")
            else:
                self.printer("Greater Heal Failed: Already at Full Health!")
                return False, CombatAction([("Heal", 0, "Holy", "")], "")
        else:
            self.printer("Greater Heal Failed: Not Enough Mana Remaining")
            return False, CombatAction([("Heal", 0, "Holy", "")], "")

    def level_up(self, combat=False):
        super().level_up(combat=combat)
        if self._level in self.skills_dict:
            skill: str = self.skills_dict[self._level][0]
            msg: str = self.skills_dict[self._level][1].__doc__
            msg: str = "\n".join(line.strip() for line in msg.splitlines())
            if combat:
                self.printer(f'New Skill - {skill}:', msg)
            else:
                print(f'\nNew Skill - {skill}:', msg)
        if self._level in self.passive_skills:
            skill: str = self.passive_skills[self._level][0]
            msg: str = self.passive_skills[self._level][1]
            msg: str = "\n".join(line.strip() for line in msg.splitlines())
            if combat:
                self.printer(f'New Skill - {skill}:', msg)
            else:
                print(f'New Skill - {skill}:', msg)

        self._attack_power += 1
        if self.agility % 2 == 0:
            self._defense_power += 1
        if self.level is 20:
            self._smite_multi = 2

    ''' Getters and Setters for types and variables'''
    @property
    def special(self) -> int:
        '''Getter for Current Mana'''
        return self._special

    @property
    def max_special(self) -> int:
        '''Getter for Max Mana'''
        return self._stats.special

    @special.setter
    def special(self, change):
        '''Setter for Mana'''
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

    def take_damage(self, damage: int, dmg_type: str, msg: str) -> bool:
        '''Processes Damage Events'''
        alive = True
        dmg_modifier = 0

        ''' Armor of Faith Passive '''
        if dmg_type == "Physical" or dmg_type == "Holy":
            damage = damage - (self._defense_power // 2)

        ''' Retribution Passive '''
        if self.level >= 10:
            dmg_modifier = int(self.level // 5)
            if self._retribution is False:
                CombatAction([("Battle Cry", int(self.level // 10),
                               "Holy", "")], "")
            self._retribution = True

        damage = int(damage * self._def_modifiers[dmg_type]/100) - dmg_modifier

        if self._halfdamage is True:
            damage = damage // 2
            self.printer(f"{self.name} is affected by their Great Heal!",
                         "Damage was cut in Half!")
            self._halfdamage = False

        elif self._nodamage is True:
            damage = -1337
            self.printer(f"Whoa! {self.name} is livin on a prayer! Damage was",
                         "nullified by the Prayer ability!")
            self._nodamage = False

        if damage >= self.hit_points:
            msg = msg.replace('<value>', str(self._hit_points))
            self._hit_points = 0
            self.printer(msg)
            self.character_death(combat=True)
            alive = False
            return alive

        if damage != -1337:  # for _nodamage
            damage = max(1, damage)
        else:
            damage = 0
        self._hit_points -= damage
        msg = msg.replace('<value>', str(damage))
        self.printer(msg)
        return alive

    def get_skills(self) -> Dict[str, 'function']:
        '''Gets Skills Learned'''
        skill_list: dict = ({skill_info[0]: skill_info[1]
                             for level_learned, skill_info in
                             self.skills_dict.items()
                             if level_learned <= self.level})
        if self._avenged:
            del skill_list["Avenger"]
        return skill_list

    def get_skills_list(self) -> List[str]:
        '''Returns List of Skills Learned'''
        skill_list: list = ([skill_info[0]
                             for level_learned, skill_info in
                             self.skills_dict.items()
                             if level_learned <= self.level])
        return skill_list

    def win_battle(self, combatant: Combatant):
        '''Instructors for Wining a Battle'''
        if isinstance(combatant, Combatant):
            exp, gold, name = combatant.experience_points, \
                combatant.gold, combatant.name
            self._battles_won += 1
            self._avenged = False
            self._nodamage = False
            self._halfdamage = False
            self._retribution = False
            self.printer(f"You have defeated {name}!  Gained {gold} Gold.",
                         f" Gained {exp} Experience")

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
