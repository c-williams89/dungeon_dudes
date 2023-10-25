"""Module for the Dungeon Dudes Wizard Class"""
from typing import Dict, Tuple, List
from random import gauss, randint
from math import floor, ceil
from .character_abc import Character
from ..combatant_abc import Combatant
from .equipment import Equipment, Weapon, Armor, Accessory
from ..dd_data import LimitedDict, damage_types, CombatPrint
from ..combat_action import CombatAction
from .wizard_src import WizardEquipmentGenerator


class Wizard(Character):
    '''Wizard Class for Dungeon Dudes'''
    stats_structure: Dict[str, Tuple[int]] = {"Hit Points": (60, 12),
                                              "Strength": (5, 0),
                                              "Agility": (10, 2),
                                              "Intelligence": (17, 2),
                                              "Special": (50, 20)}

    item_compatibility: list = ["Staff", "Wand", "Robes", "Arcane Orb"]

    def __init__(self, name: str):
        self.damage_types = damage_types

        self.skills_dict: Dict[int, List[str, 'function']] = {
            1: ["Fire ball", self.fire_ball],
            2: ["Blink", self.blink],
            3: ["Blizzard", self.blizzard],
            8: ["Lightning Bolt", self.lightning_bolt],
            13: ["Reflect Damage", self.reflect_damage],
            20: ["Mana Burn", self.mana_burn]
        }
        mana_regeneration = '''Passive: You've regained 15 percent of your'''\
            '''mana.'''
        elemental_affinity = '''Passive: You've gained a 25 percent damage'''\
            '''boost to your bext elemental attack'''
        improved_passives = '''Passive: 25 percent of your armors'''\
            '''non-physical damage modifier now applies to your physical'''\
            '''damage'''
        elemental_master = '''Passive: You now deal +50 percent damage if'''\
            '''you've dealt fire, ice, and lightning damage this combat'''

        self.passive_skills = {
            5: ["Mana Regeneration", mana_regeneration],
            10: ["Elemental Affinity", elemental_affinity],
            17: ["Improved Passives", improved_passives],
            25: ["Elemental Master", elemental_master]
        }

        self.printer = CombatPrint()
        self._weapon: Weapon = None
        self._armor: Armor = None
        self._accessory: Accessory = None
        self._def_modifiers = LimitedDict(self.damage_types, default_value=100)
        self._dam_modifiers = LimitedDict(("Fire", "Lightning", "Ice"),
                                          default_value=100)
        self._equipment_generator = WizardEquipmentGenerator()
        super().__init__(name, "Wizard", self.stats_structure,
                         self.item_compatibility)
        self._exp_to_next_iter = iter([(50 * i ** 2) for i in range(1, 50)])
        self._exp_to_next: int = next(self._exp_to_next_iter)
        self._hit_points: int = self.stats_structure["Hit Points"][0]
        self._special: int = 50
        self._special_resource: str = "Mana"
        self._accessory_type: str = "Arcane Orb"
        self._stored_damage: int = 0
        self._damage_taken: int = 0
        self._is_on_fire: bool = False
        self._is_frozen: bool = False
        self._reflect: bool = False
        self._last_element_att: str = ""

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
        self._attack_power = self.intelligence
        self._defense_power = self.agility // 2

    def modify_damage(self, damage, spell_type=None) -> int:
        '''Adds Variance to Damage Events'''
        max_mana = self._stats.special
        current_mana = self._special
        mana_dev = current_mana/max_mana
        modified: float = (damage * (mana_dev/2) - 0.15)

        if self.level >= 10:
            if spell_type and spell_type != self._last_element_att:
                modified *= 1.25

        return modified

    def attack(self) -> CombatAction:
        '''Does Damage Based on Attack Power'''
        damage: int = self.modify_damage(self._attack_power)
        message: str = (f"{self.name} attacks with {self.weapon} "
                        f"for <value> {self._weapon.damage_type} damage")
        attack_action = [("Attack", damage, self._weapon.damage_type, message)]

        if self._is_on_fire:
            # Calculate the damage for the burning effect
            burning_damage: int = self.intelligence
            burn_message: str = (f"{self.name}'s fireball continues to burn")
            burning_effect = ("Attack", burning_damage, "Fire", burn_message)
            attack_action.append(burning_effect)

        if self._is_frozen:
            frozen_damage: int = self.intelligence
            freeze_message: str = (f"{self.name}'s blizzard continues to "
                                   "freeze all enemies")
            freeze_effect = ("Attack", frozen_damage, "Ice", freeze_message)
            attack_action.append(freeze_effect)

        if self._reflect:
            reflect_damage: int = self._stored_damage
            reflect_message: str = (f"{self.name} uses reflect to attack the "
                                    "enemy with lightning")
            reflect_effect = ("Attack", reflect_damage, "Lightning",
                              reflect_message)
            attack_action.append(reflect_effect)

        return CombatAction(attack_action, "")

    def fire_ball(self) -> [bool, CombatAction]:
        '''Wizard launches a fireball at their enemy dealing Fire damage based
        on Intelligence x 3.  The Wizard burns the enemy for additional damage
        based on their Intelligence x1 the following round'''
        if self._special >= 20:
            # Calculate the initial fireball damage
            initial_damage = 3 * self.intelligence
            self._is_on_fire = True
            self._last_element_att = "Fire"
            message = (f"{self.name} throws a fireball, dealing "
                       f"{initial_damage} Fire damage.")
            # Reduce mana for using fireball
            self._special -= 20
            # Create a CombatAction for the initial fireball attack
            fireball_action = CombatAction([("Attack", initial_damage,
                                             "Fire", message)], "")

            '''Return a list with the initial fireball action and the burning
            effect'''
            return True, fireball_action

        '''If the Wizard doesn't have enough special for the fireball,
        return False and an empty action'''
        return False, CombatAction([], "")

    def blink(self) -> [bool, CombatAction]:
        '''The Wizard Escapes the Battle and returns to town'''
        # Verify Wizard has enough mana
        if self._special >= 30:
            message: str = (f"{self.name} uses Blink to escape the battle"
                            "and return to town.")
            blink_effect = CombatAction([("Escape", 0, "Physical", message)],
                                        "")
            # Reduce mana after using "Blink"
            self._special -= 30
            return True, blink_effect

        '''If the Wizard doesn't have enough special for blink, return False
        and an empty action'''
        return False, CombatAction([], "")

    def blizzard(self) -> [bool, CombatAction]:
        """The wizard summons a blizzard to the battlefield"""
        # Verify wizard has enough mana
        if self._special >= 40:
            # Calculate amount of damage dealt
            blizzard_damage = self.intelligence
            self._is_frozen = True
            self._last_element_att = "Ice"
            message = (f"{self.name} summons a blizzard, dealing "
                       f"{blizzard_damage} Ice damage to all enemies.")
            # Reduce mana after spell is cast
            self._special -= 40
            # Create combat action
            blizzard_action = CombatAction([("Attack", blizzard_damage, "Ice",
                                             message)], "")

            return True, blizzard_action
        # If wizard does not have enough mana for blizzard return False
        return False, CombatAction([], "")

    def lightning_bolt(self) -> [bool, CombatAction]:
        '''The Wizard strikes their opponent with Lightning, dealing
        Intelligence x5 based damage.'''
        # Verify wizard has enough mana
        if self._special >= 50:
            # Calculate the Lightning damage based on Intelligence
            lightning_damage = self.intelligence * 5
            self._last_element_att = "Lightning"
            message = (f"{self.name} strikes their opponent with Lightning, "
                       f"dealing {lightning_damage} Lightning damage.")
            # Reduce mana for using lightning_bolt
            self._special -= 50
            # Create a CombatAction
            lightning_bolt_action = CombatAction([("Attack", lightning_damage,
                                                   "Lightning", message)], "")
            return True, lightning_bolt_action
        # If wizard does not have enough mana for blizzard return False
        return False, CombatAction([], "")

    def reflect_damage(self) -> [bool, CombatAction]:
        '''For the remainder of the combat, whenever the Wizard is damaged,
        a % of the damage equal to the Wizard’s level (rounded up) is stored.
        This stored damage is added to the Wizard’s next damaging attack as
        Lightning damage.'''
        # Verify wizard has enough mana
        if self._special >= 30:
            self._reflect = True

            '''Calculate the stored damage percentage based on the Wizard's
            level (rounded up)'''
            self._stored_damage = round((self._damage_taken/self.level) * 100)
            message = (f"{self.name} activates Reflect Damage. "
                       f"{self._stored_damage}% of incoming damage will be "
                       "stored for the next attack.")
            reflect_action = CombatAction([("Aura", 0, "Holy", message)], "")
            # Reduce mana for using reflect_damage
            self._special -= 30
            return True, reflect_action
        # If the Wizard doesn't have enough mana, return False
        return False, CombatAction([], "")

    def mana_burn(self) -> [bool, CombatAction]:
        '''Consume all your remaining mana to do Fire, Ice, and Lightning
        damage to an enemy. The base damage of each damage type is 50%
        of the consumed mana (rounded up).'''

        # Check if the Wizard has any remaining mana
        if self._special > 0:

            '''Calculate the base damage for each damage type based on 50% of
            consumed mana (rounded up)'''
            base_fire_damage = ceil(0.5 * self.special)
            base_lightning_damage = ceil(0.5 * self.special)
            base_ice_damage = ceil(0.5 * self.special)
            # Create a message indicating the mana burn action
            self.printer(f"{self.name} consumes all remaining mana to perform "
                         "a Mana Burn attack.")
            # Create a list of actions for each damage type
            actions = [
                ("Attack", base_fire_damage, "Fire",
                 "<value> Fire damage from Mana Burn."),
                ("Attack", base_ice_damage, "Ice",
                 "<value> Ice damage from Mana Burn."),
                ("Attack", base_lightning_damage, "Lightning",
                 "<value> Lightning damage from Mana Burn.")
            ]

            # Create a CombatAction with the actions and the message
            mana_burn_action = CombatAction(actions, "")
            # Consume all remaining mana
            self._special = 0

            '''Return True to indicate a successful Mana Burn and the
            CombatAction'''
            return True, mana_burn_action

        # If the Wizard has no remaining mana, return False
        return False, CombatAction([], "")

    def level_up(self, combat=False):
        super().level_up(combat=combat)
        if self._level in self.skills_dict:
            skill: str = self.skills_dict[self._level][0]
            description: str = self.skills_dict[self._level][1].__doc__
            description: str = "\n".join(line.strip() for line in description.
                                         splitlines())
            if combat:
                self.printer(f'New Skill - {skill}:', description)
            else:
                print(f'\nNew Skill - {skill}:', description)
        if self._level in self.passive_skills:
            skill: str = self.passive_skills[self._level][0]
            description: str = self.passive_skills[self._level][1]
            description: str = "\n".join(line.strip() for line in description.
                                         splitlines())
            if combat:
                self.printer(f'New Skill - {skill}:', description)
            else:
                print(f'New Skill - {skill}:', description)

        self._attack_power += 2
        self._defense_power += 1

    @property
    def special(self) -> int:
        '''Getter for current Mana'''
        return self._special

    @property
    def max_special(self):
        '''Getter for max Mana'''
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

    def take_damage(self, damage: int, dmg_type: str, message: str) -> bool:
        '''Processes Damage Events'''
        mana_percentage = self._special/self._stats.special * 100
        alive = True
        if dmg_type != "Physical":
            damage = damage - round(self.intelligence/5)

        if dmg_type == "Physical" and mana_percentage > 50:
            damage = round(damage - (damage * 0.15))

        damage = int(damage * self._def_modifiers[dmg_type]/100)

        if damage >= self.hit_points:
            message = message.replace('<value>', str(self._hit_points))
            self._hit_points = 0
            self.printer(message)
            self.character_death(combat=True)
            alive = False
            return alive
        damage = max(1, damage)
        self._hit_points -= damage
        self._damage_taken = damage
        message = message.replace('<value>', str(damage))
        self.printer(message)
        return alive, damage

    def win_battle(self, combatant: Combatant):
        '''Instructors for Wining a Battle'''
        if isinstance(combatant, Combatant):
            exp, gold, name = combatant.experience_points, combatant.gold,
            combatant.name
            self._battles_won += 1
            self.printer(f"You have defeated {name}!  Gained {gold} Gold.  "
                         f"Gained {exp} Experience")
            if self._level >= 5 and self._special < self._stats.special:
                current = self._special
                self._special += round(self._stats.special * 0.15)
                self.printer(f"You regained {self._special - current} mana "
                             f"from Mana Regeneration")
            self._gold += gold
            self.gain_experience(exp, combat=True)

    def get_skills(self) -> Dict[str, 'function']:
        '''Gets Skills Learned'''
        skills_list_filter: dict = ({skill_info[0]: skill_info[1] for
                                     level_learned, skill_info in
                                     self.skills_dict.items() if
                                     level_learned <= self.level})

        return skills_list_filter

    def get_skills_list(self) -> List[str]:
        '''Returns List of Skills Learned'''
        skills_list_filter: list = ([skill_info[0] for level_learned,
                                     skill_info in self.skills_dict.items() if
                                     level_learned <= self.level])
        return skills_list_filter

    def generate_weapon(self) -> Weapon:
        '''Generates a suitable Weapon Equipment Item based on level'''
        return self._equipment_generator.generate_weapon(self._level)

    def generate_armor(self) -> Armor:
        '''Generates a suitable Armor Equipment Item based on level'''
        return self._equipment_generator.generate_armor(self._level)

    def generate_accessory(self) -> Accessory:
        '''Generates a suitable Armor Equipment Item based on level'''
        return self._equipment_generator.generate_accessory(self._level)

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
        if self._level >= 5 and self._special < self._stats.special:
            current_special = self._special
            self._special += round(self._stats.special * 0.15)
            self._attack_power += round(self._attack_power * 0.15)
            self.printer(f"You regained {self._special - current_special} "
                         "mana from drinking healing potion")

        printer('Drank a healing Potion and healed '
                f'{self.hit_points - current} Hit Points')
        return success, CombatAction([("Heal", heal_amount, "Holy")], "")
