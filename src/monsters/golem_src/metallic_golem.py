'''Metallic Golem Module for Dungeon Dudes'''
from typing import Dict, Tuple
from random import choice, choices
from src.dd_data import LimitedDict
from ..golem import Golem
from ...dd_data import LimitedDict
from ...combat_action import CombatAction

class MetallicGolem(Golem):
    '''MetallicGolem Module'''
    stats_structure : Dict[str, Tuple[int]] = {"Hit Points": (60, 13), 
                                               "Strength": (18, 4),
                                               "Agility" : (11, 2), 
                                               "Intelligence" : (0, 0), 
                                               "Special" : (0,0)}
    metal_types = [("Iron", "Physical"), ("Chromatic", "Physical"), 
                   ("Mithril", "Physical")]

    def __init__(self, level_mod : int):
        if level_mod <= 10:
            comp = [("Iron", 0.75), ("Chromatic", 0.25)]
        else:
            comp = [("Iron", 0.55), ("Chromatic", 0.25), ("Mithril", 0.2)]

        metal_types, probabilities = zip(*comp)
        metal_type = choices(metal_types, probabilities)[0]
        for mt, dt in self.metal_types:
            if mt == metal_type:
                dmg_type = dt
                break

        self._hit_points : int = self.stats_structure["Hit Points"][0]
        self._metal_type : str = metal_type
        self._damage_type : str = dmg_type
        super().__init__(f'{self._metal_type} Golem',
                         level_mod, self.stats_structure)
        self._sub_type : float = metal_type
        self._dam_modifiers = LimitedDict("Physical",  default_value=100)
        self._prev_phys_dmg = 0 if self._metal_type == 'Iron' else None
        self._spiked_body_used = False
        self._exploded = False

    @property
    def damage_modifiers(self) -> LimitedDict:
        '''Getter for damage modifiers'''
        return self._dam_modifiers
    
    @property
    def defense_modifiers(self) -> LimitedDict:
        '''getter for defense modifiers'''
        return self._def_modifiers

    def get_skills(self) -> Dict[str, 'function']:
        '''Get Skills Learned'''
        return {}

    def get_skills_list(self) -> list:
        '''get list of skills learned'''
        skills_list = ["sum_parts"]

        # iron golem skills
        if self._metal_type == "Iron":
            skills_list.append("double_attack")
            if self.level >= 10:
                skills_list.append("spiked_body")

        # chromatic golem skills
        if self._metal_type == "Chromatic":
            if self.level >= 10:
                skills_list.append("explode")

        # mithril golem skills

        return skills_list
    
    def sum_parts(self):
        '''modify sum of their parts'''
        super().sum_parts()

        # check for explode
        if not self._exploded:
            hp_percent : int = (self._hit_points / self.max_hit_points) * 100
            if hp_percent <= 50 or hp_percent <= 25:
                if choice([True, False]):
                    self.explode()

    # iron golem skills
    def double_attack(self) ->CombatAction:
        '''
        Iron Golem quickly Attacks with both hands, dealing 75% attack_power 
        based damage with each strike.
        '''
        dble_attk_dmg : int = int(self.attack().actions[0][1] * 0.75)
        msg_1 : str = "Iron Golem strikes with its fist, dealing <value> physical damage."
        msg_2 : str = "Iron Golem quickly lashes out with its other fist for an additional <value> physical damage."
        return CombatAction([("Attack", dble_attk_dmg, "Physical", msg_1),
                             ("Attack", dble_attk_dmg, "Physical", msg_2)], "")

    def spiked_body(self) -> CombatAction:
        '''
        Once per Combat Iron Golem creates Iron Spikes out of its body,
        every time the Iron Golem takes Physical damage the its next Action 
        will deal 25% attack_power based damage to the opponent.
        '''
        if self._spiked_body_used:
            return CombatAction([], "Spiked body has already been used")
        spiked_dmg : int = self.golem_damage(self.modify_damage(self._attack_power * 0.25))
        self._spiked_body_used = True
        msg : str = ("Iron Golem spikes its body, causing its next action to "
                     "deal additional damage when it takes damage.")
        return CombatAction([("Buff", spiked_dmg, "Physical", msg)], "")
    
    # chromatic golem
    def explode(self) -> CombatAction:
        '''
        Once per Combat When Sum of their parts triggers at 50% or 25% 
        max_hit_points, Chromatic Golems have a 50% chance to Explode as their 
        next Action.  Explode reduces the Chromatic Golem to 1 hit_point, deals 
        1.5x attack_power based Physical damage, and attack_power based damage 
        of the current Improved Defensive Modifiers immunity damage type.  
        On their next Action, if the Golem is still alive, it takes no action 
        and is defeated.
        '''
        pass

    def take_damage(self, damage: int, dmg_type: str, message : str) -> bool:
        '''take damage with modifications'''
        if self._metal_type == "Iron":
            if dmg_type in ["Ice", "Fire", "Holy"]:
                damage = int(damage * 0.7)
                msg : str = ("The Iron Golem appears to take less damage from "
                             "that attack...")
                self.printer(msg)
            else:
                damage = damage
        return super().take_damage(damage, dmg_type, message)

    def attack(self) -> CombatAction:
        damage : int = self.golem_damage(self.modify_damage(self._attack_power))
        razor_sharp_bonus = 0
        if self._metal_type == 'Iron' and self._prev_phys_dmg:
            razor_sharp_bonus = int(self._prev_phys_dmg * 0.25)
            self._prev_phys_dmg = 0
        total_damage = damage + razor_sharp_bonus
        message : str = f"{self.name} Attacks for <value> physical damage"
        if self._metal_type == 'Iron':
            self._prev_phys_dmg = damage

        return CombatAction([("Attack", total_damage, "Physical", message)], "")
    
    def take_turn(self) -> CombatAction:
        '''takes turn and returns the action'''
        options = [self.attack]
        if self.level >= 10:
            options.append(self.spiked_body)
        return choice(options)()
