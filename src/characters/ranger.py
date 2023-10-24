'''Module for the Dungeon Dudes Ranger Class'''
from typing import Dict, Tuple, List
from random import gauss, choice
from math import floor
from .character_abc import Character
from ..combatant_abc import Combatant
from .equipment import Equipment, Weapon, Armor, Accessory
from ..dd_data import LimitedDict, damage_types, CombatPrint
from ..combat_action import CombatAction
from .ranger_src import RangerEquipmentGenerator


class Ranger(Character):
    '''Ranger Class for Dungeon Dudes'''
    stats_structure : Dict[str, Tuple[int]]= {"Hit Points": (90, 22), 
                                              "Strength": (7, 1),
                                              "Agility" : (14, 2),
                                              "Intelligence" : (5, 0),
                                              "Special": (2,1)}
    item_compatibility : list = ["Bow", "Light", "Quiver"]

    def __init__(self, name):
        self.damage_types = damage_types

        self.skills_dict :Dict[int, List[str, 'function']] = {
            1:["Summon Wolf Companion", self.summon_wolf ],
            3:["Take Aim", self.take_aim],
            5:["Summon Bear Companion", self.summon_bear],
            8:["Steel Trap", self.steel_trap],
            13:["Summon Cat Companion", self.summon_cat],
         }
        awareness = '''Passive: Whenever the Ranger spends a turn without '''\
        '''directly damaging the opponent, they gain Awareness and their '''\
        '''next damaging attack will consume Focus to deal 50% increased damage'''
        improved_awareness = '''Passive: Gaining awareness also increases '''\
                        '''attack power scaling of Ranger's next damaging '''\
                        '''action by 25% and improves defense against '''\
                        '''elements by 10'''
        focused_regen = '''Passive: The Ranger recovers a % of their '''\
                    '''hit points equal to their current focus '''\
                    '''after defeating an enemy'''
        lucky_strike = '''Passive: Ranger has 50% chance to consume focus '''\
                    '''point and deal 50% increased damage. Recover 1 '''\
                    '''focus point and additional focus for each active '''\
                    '''animal companion after defeating an enemy'''
        improved_animal_companion = '''The first 2 animal companion's '''\
                    '''summoned each encounter do not pass the Ranger's '''\
                    '''turn. Attack power and defense power provided by '''\
                    '''companions is doubled and companions deal additional'''\
                    ''' 10% of the Ranger's attack power'''
        self.passive_skills = {
            1: ["Awareness", awareness],
            10: [["Improved Awareness", improved_awareness],
                 ["Focused Regeneration", focused_regen]],
            20: ["Lucky Strike", lucky_strike],
            25: ["Improved Animal Companion 2", improved_animal_companion]
        }
        self.printer = CombatPrint()
        self._weapon : Weapon = None
        self._armor : Armor = None
        self._accessory : Accessory = None
        self._def_modifiers = LimitedDict(self.damage_types, default_value=100)
        self._dam_modifiers = LimitedDict("Physical", default_value=100)
        self._equipment_generator = RangerEquipmentGenerator()
        super().__init__(name, "Ranger", self.stats_structure, 
                         self.item_compatibility)
        self._exp_to_next_iter = iter([(40 * i ** 2) for i in range(1, 50)])
        self._exp_to_next :int = next(self._exp_to_next_iter)
        self._hit_points :int = self.stats_structure["Hit Points"][0]
        self._special :int = 2
        self._special_resource :str = "Focus"
        self._accessory_type :str = "Quiver"
        self._focus :bool = False
        self._companion :Dict[str: list(bool, int)] = {'Wolf': [False, 0],
                                                       'Bear': [False, 0], 
                                                       'Cat': [False, 0]}
        self._total_companion :int = 1
        self._improved_animal_companion :bool = False
        self._summoned :int = 0
        self._trap = [False, (self._attack_power * .50)]

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
        self._attack_power = self.strength + (self.agility // 2)
        self._defense_power = self.agility // 2

    def modify_damage(self, damage) -> int:
        '''Adds Variance to Attack, Companion, and Trap Events'''
        combat_list :List(tuple) = list()
        modifier : int = floor(max(0, min(damage*.24,
                                     (gauss(damage*.08, damage*.04)))))
        # If level is above 20, Calculate Lucky Strike
        if self._level >= 20:
            lucky_strike = [True, False]
            chance = choice(lucky_strike)
            if chance is True:
                damage *= 1.5
        # If Focus is on increase damage by 50%
        if self._focus:
            if self._special > 0:
                damage *= 1.5
                self._focus = False
                self._special -= 1
        # Calculate the total attack damage
        damage += modifier
        msg = (f"{self.name} attacks with {self.weapon} "
                      f"for <value> {self._weapon.damage_type} damage")
        basic_attack = ("Attack", damage, self._weapon.damage_type, msg)
        combat_list.append(basic_attack)
        # Companions damage
        for key, value in self._companion.items():
            if value[0] is True:
                companion_msg : str = \
                    f"{key} companion attacks for {int(value[1])} damage"
                combat_list.append(("Attack", int(value[1]), 'Physical',
                                    companion_msg))
        # Trap damage
        if self._trap[0]:
            trap_msg :str = f"Steel Trap inflicts {self._trap[1]} damage"
            combat_list.append(("Attack", int(self._trap[1]), 'Physical',
                                trap_msg))
        return combat_list

    def attack(self) -> CombatAction:
        '''Does Damage Based on Attack Power'''
        damage : int = self.modify_damage(self._attack_power)

        return CombatAction(damage, "")

    def check_summon(self, companion: str):
        '''Check if companion can be summoned'''
        # Check if companion has been already summoned
        if self._companion[companion][0]:
            return True
        # If summoned companions is less than total available summon
        elif self._summoned < self._total_companion:
            self._companion[companion][0] = True
            self._summoned += 1
        # If summoned companions is equal to the total available summon
        if self._summoned == self._total_companion:
            for key, value in self._companion.items():
                if key != companion and value is True:
                    # Replace oldest companion with the new companion
                    value = False
                    self._companion[companion] = True
        return False

    def summon_attack_modifier(self, modifier:int):
        '''Calculate the companions damage'''
        end_turn = True
        bonus_modifier = 10
        if self._level < 15:
            damage = self._attack_power * (modifier / 100)
        elif 15 <= self._level < 25:
            damage = self._attack_power * (modifier / 100)
            if self._summoned < self._total_companion:
                end_turn = False
            else:
                end_turn = True
        else:
            damage = self._attack_power * ((modifier + bonus_modifier) / 100)
            if self._summoned < self._total_companion:
                end_turn = False
            else:
                end_turn = True
        modified_damage = damage + floor(max(0, min(damage*.24,
                                     (gauss(damage*.08, damage*.04)))))
        return end_turn, modified_damage

    def summon_wolf(self) ->  [bool, CombatAction]:
        '''Summons a Wolf Companion. Whenever the Ranger deals damage, the 
        Wolf attacks, dealing Physical damage based on 60% of the Ranger's
        attack'''
        end_turn = True
        base_modifier = 60
        self._focus = True
        # Check if the wolf is already summoned
        summoned = self.check_summon('Wolf')
        if summoned:
            self.printer("You already summoned a 'Wolf' companion")
            return end_turn, CombatAction([], "")
        # Calculate Wolf Damage
        end_turn, damage = self.summon_attack_modifier(base_modifier)
        self._companion['Wolf'][1] = damage
        # Calculate Defense Modifier
        resist_type : List[str] = ["Physical", "Ice"]
        if self._level < 15:
            defense_modifier = 10
        else:
            defense_modifier = 20
        aura : List[tuple] = [("Aura", defense_modifier, damage_type, "")
                                for damage_type in resist_type]
        self.printer(f"{self.name} summons a Wolf companion")
        return end_turn, CombatAction(aura, "")

    def take_aim(self) ->  [bool, CombatAction]:
        '''Take aim triggers Awareness'''
        self._focus = True
        self.printer(f"{self.name}'s awareness is increased.")
        return True, CombatAction([], "")

    def summon_bear(self) ->  [bool, CombatAction]:
        '''Summon a Bear Companion. Whenever the Ranger deals damage, the
        Bear attacks and deals 60% of the Ranger's attack'''
        end_turn = True
        base_modifier = 60
        defense_modifier = .10
        self._focus = True
        # Check if the wolf is already summoned
        summoned = self.check_summon("Bear")
        if summoned:
            self.printer("You already summoned a 'Bear' companion")
            return end_turn, CombatAction([], "")

        # Calculate Bear Damage
        end_turn, damage = self.summon_attack_modifier(base_modifier)
        self._companion['Bear'][1] = damage
        # Calculate Defense Modifier
        resist_type : List[str] = ["Physical"]
        if self._level < 15:
            defense_modifier = 10
        else:
            defense_modifier = 20
        aura : List[tuple] = [("Aura", defense_modifier, damage_type, "")
                                for damage_type in resist_type]
        if self.level >= 25:
            self._defense_power += self._defense_power * (2 * defense_modifier)
        else:
            self._defense_power += self._defense_power * defense_modifier
        self.printer(f"{self.name} summons a Bear companion")
        return end_turn, CombatAction(aura, "")


    def steel_trap(self) ->  [bool, CombatAction]:
        '''Ranger traps their opponent, dealing 'physical' damage based on 75% 
        of the Ranger's attack power, and 'physical' damage based on 50% of the
        Ranger's attack power each turn for the remainder of the encounter'''
        # Check if the trap is deployed already
        if self._trap:
            self.printer("Steel Trap has been already deployed")
            return False, CombatAction([],"")
        # Turn the trap flag on
        self._trap = True
        self.printer(f"{self.name} uses steele traps!")
        return True, CombatAction([], "")

    def summon_cat(self):
        '''Summon a Cat Companion. Whenever the Ranger deals damage, the 
        Cat attacks, dealing Physical Damage based on 75% of the Ranger's
        attack '''
        end_turn = True
        base_modifier = 75
        attack_modifier = .10
        self._focus = True
        # Check if the cat is already summoned
        summoned = self.check_summon("Cat")
        if summoned:
            self.printer("You already summoned a 'Cat' companion")
            return end_turn, CombatAction([],"")
        # Calculate Cat Damage and attack modifier
        end_turn, damage = self.summon_attack_modifier(base_modifier)
        self._companion['Cat'][1] = damage
        if self.level >= 25:
            self._attack_power += self._attack_power * (2 * attack_modifier)
        else:
            self._attack_power += self._attack_power * attack_modifier
        # Calculate Defense Modifier
        resist_type : List[str] = ["Lightning", "Fire"]
        if self._level < 15:
            defense_modifier = 10
        else:
            defense_modifier = 20
        aura : List[tuple] = [("Aura", defense_modifier, damage_type, "")
                                for damage_type in resist_type]
        self.printer(f"{self.name} summons a Cat companion")
        return end_turn, CombatAction(aura, "")


    # def summon_clean_up(self):
    #     for key, value in self._companion.items():
    #         if key == "Bear":
    #             self._defense_power = 

    def level_up(self, combat=False):
        super().level_up(combat=combat)
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
        self._attack_power += 2
        self._defense_power += 1

    @property
    def special(self) -> int:
        '''Getter for Current Focus'''
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
                return alive
            else:
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
        skills_list_filter : dict = ({skill_info[0]:skill_info[1] for level_learned, skill_info in
                               self.skills_dict.items() if level_learned <= self.level})
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
            self.printer(f"You have defeated {name}!  Gained {gold} Gold.  Gained {exp} Experience")
            # Focused Regeneration
            if self._level >= 10:
                current = self.hit_points
                self.hit_points += floor(self.max_hit_points * .25)
                self.printer(f"You heal {self.hit_points - current} "
                             f"hit points from Focused Regeneration")
            # Lucky Strike
            if self._level >= 20:
                max_focus = 2 + (self._level - 1)
                if self._special < max_focus:
                    self._special += 1 + self._summoned
                if self._special > max_focus:
                    self._special = max_focus
                self.printer(f"You gain {1 + self._summoned} "
                             f"focus points from Lucky Strike")
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