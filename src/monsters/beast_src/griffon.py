'''Module for the Dungeon Dudes Griffon Beast'''
from typing import Dict, Tuple
from random import choice
from ..beast import Beast
from ...dd_data import LimitedDict
from ...combat_action import CombatAction

class Griffon(Beast):
    '''Griffon Beast Class'''
    stats_structure: Dict[str, Tuple[int]] = {"Hit Points": (65, 15), "Strength": (20, 4),
                        "Agility" : (12, 4), "Intelligence" : (5, 1), "Special" : (0,0)}
    griffon_types = [("Sunfire", "Fire"), ("Anointed", "Holy")]

    def __init__(self, level_mod : int):
        griffon_type : tuple = choice(self.griffon_types)
        self._hit_points : int = self.stats_structure["Hit Points"][0]
        self._griffon_type : str = griffon_type[0]
        self._damage_type : str = griffon_type[1]
        super().__init__(f'{self._griffon_type} Griffon', level_mod,
                         self.stats_structure)
        self._sub_type : str = "Griffon"
        self._dam_modifiers = LimitedDict(("Physical", (self._damage_type)), default_value=100)
        self._empowered = False
        self._special_count = 0

    @property
    def damage_modifiers(self) -> LimitedDict:
        '''Getter for Damage Modifiers'''
        return self._dam_modifiers

    @property
    def defense_modifiers(self) -> LimitedDict:
        '''Getter for Defense Modifiers'''
        return self._def_modifiers

    def get_skills(self) -> Dict[str, 'function']:
        '''Get Skills Learned'''
        return {}

    def get_skills_list(self) -> list:
        '''Get List of Skills Learned'''
        special_skills = {"Anointed": "Hymn",
                          "Sunfire": "Cauterizing Burst"}
        return [f'{self._damage_type} Empowerment',
                special_skills[self._griffon_type]]

    def hymn(self) -> CombatAction:
        '''
        Increases Physical and Holy Defensive Modifiers by 10
        and does HP based Holy Damage
        '''
        self._special_count += 1
        msg : str = ("Anointed Griffon performs a hymn, increasing its defenses "
            "and pulses for <value> holy damage")
        damage : int = self.beast_damage(self.modify_damage(self.hit_points//5))
        if self._special_count > 2:
            return CombatAction([("Attack", damage, "Holy", msg)], "")
        return CombatAction([("Attack", damage, "Holy", msg), ("Aura", 10, "Holy", "")
                                ,("Aura", 10, "Physical", "")], "")

    def cauterizing_burst(self) -> CombatAction:
        '''
        Heals for an amount Equal to Intelligence
        and does HP based Fire Damage
        '''
        self.hit_points += self.intelligence
        msg : str = ("Sunfire Griffon cauterizes its wounds and then bursts for "
                   "<value> fire damage")
        damage : int = self.beast_damage(self.modify_damage(self.hit_points//5))
        return CombatAction([("Attack", damage, "Fire", msg)], "")

    def special_skill(self) -> CombatAction:
        '''Returns special attack per Griffon type'''
        if self._griffon_type == "Sunfire":
            return self.cauterizing_burst()
        return self.hymn()

    def empowerment(self) -> CombatAction:
        '''
        Attacks for 75% normal damage and empowers future attacks to
        deal additional damage based on damage type
        '''
        self._empowered = True
        damage : int = self.beast_damage(self.modify_damage(self._attack_power * .75))
        msg : str = (f"{self.name} empowers with {self._damage_type} dealing "
                     f"<value> {self._damage_type} damage and increasing future "
                     f"attack damage")
        return CombatAction([("Attack", damage, self._damage_type, msg)], "")


    def attack(self) -> CombatAction:
        damage : int = self.beast_damage(self.modify_damage(self._attack_power))
        message : str = f"{self.name} Attacks with for <value> physical damage"
        if self._empowered:
            secondary_dmg : int = self.beast_damage(self.modify_damage(self.intelligence))
            secondary_msg : str = (f"{self.name}'s claws deal an additional <value> "
                                   f"{self._damage_type} damage")
            return CombatAction([("Attack", damage, "Physical", message),
                                 ("Attack", secondary_dmg, self._damage_type, secondary_msg)]
                                 , "")
        return CombatAction([("Attack", damage, "Physical", message)], "")

    def take_turn(self) -> CombatAction:
        '''Takes turn and returns the action'''
        if not self._empowered:
            options = [self.attack, self.empowerment, self.special_skill]
        else:
            options = [self.attack, self.special_skill]
        return choice(options)()
