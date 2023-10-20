'''Module for the Dungeon Dudes Chimera Beast'''
from typing import Dict, Tuple
from random import choice, randint
from ..beast import Beast
from ...dd_data import LimitedDict
from ...combat_action import CombatAction

class Chimera(Beast):
    '''Chimera Beast Class'''
    stats_structure: Dict[str, Tuple[int]] = {"Hit Points": (75, 16), "Strength": (15, 3),
                    "Agility" : (15, 3), "Intelligence" : (15, 3), "Special" : (0,0)}
    heads = ["Snake", "Eagle", "Lion"]

    def __init__(self, level_mod : int):
        self._hit_points : int = self.stats_structure["Hit Points"][0]
        super().__init__('Chimera', level_mod,
                         self.stats_structure)
        self._sub_type : str = "Chimera"
        self._dam_modifiers = LimitedDict(("Physical", "Poison", "Lightning"), default_value=100)

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
        skills_list = ["poison_breath", "summon_lightning", "lion_roar"]
        if self.level >= 3:
            skills_list.append("additional_attack")
        return skills_list

    def attack(self, current_head="Snake") -> CombatAction:
        '''Attack method for Chimera Heads'''
        damage : int = self.beast_damage(self.modify_damage(self._attack_power))
        message : str = f"{current_head} Head attacks with for <value> physical damage"
        return CombatAction([("Attack", damage, "Physical", message)], "")

    def additional_attack(self, current_head, com_action : CombatAction) -> CombatAction:
        '''Additional Attack for Chimera Heads'''
        heads = ["Snake", "Eagle", "Lion"]
        heads.remove(current_head)
        head = choice(heads)
        msg = f'{head} attacks in conjunction for <value> physical damage'
        dmg = self.beast_damage(self.modify_damage(self.attack_power))
        com_action.actions.append(("Attack", dmg, "Physical", msg))
        return com_action

    def poison_breath(self) -> CombatAction:
        '''Poison Breath Attack for Snake Head'''
        dmg : int = self.beast_damage(self.modify_damage(self.intelligence))
        msg : str = "Chimera's Snake Head breaths a noxious cloud for <value> poison damage"
        return CombatAction([("Attack", dmg, "Poison", msg )], "")

    def summon_lightning(self) -> CombatAction:
        '''Summon Lightning Attack for Eagle Head'''
        dmg : int = self.beast_damage(self.modify_damage(self.intelligence))
        msg : str = "Chimera's Eagle Head summons a storm which deals <value> lightning damage"
        return CombatAction([("Attack", dmg, "Lightning", msg )], "")

    def lion_roar(self) -> CombatAction:
        '''Roars for Physical Damage and Raises Modifiers'''
        modifiers : list = ["Physical", "Lightning", "Poison"]
        dmg : int = self.beast_damage(self.modify_damage(int(self.attack_power * 0.75)))
        battle_cries = [("Battle Cry", 10, damage_type, "") for damage_type in modifiers]
        msg : str = "Lion's Head Roars for <value> physical damage and raising attack modifiers"
        battle_cries.append(("Attack", dmg, "Physical", msg))
        return CombatAction(battle_cries, "")

    def snake_turn(self) -> CombatAction:
        '''Actions for turns where Snake is primary head'''
        turn_choice = randint(1,2)
        if turn_choice == 1:
            action = self.attack(current_head="Snake")
        else:
            action = self.poison_breath()
        if self.level >= 7:
            return self.additional_attack("Snake", action)
        return action

    def eagle_turn(self) -> CombatAction:
        '''Actions for turns where Eagle is primary head'''
        turn_choice = randint(1,2)
        if turn_choice == 1:
            action = self.attack(current_head="Eagle")
        else:
            action = self.summon_lightning()
        if self.level >= 5:
            return self.additional_attack("Eagle", action)
        return action

    def lion_turn(self) -> CombatAction:
        '''Actions for turns where Lion is primary head'''
        turn_choice = randint(1,2)
        if turn_choice == 1:
            action = self.attack(current_head="Lion")
        else:
            action = self.poison_breath()
        if self.level >= 3:
            return self.additional_attack("Lion", action)
        return action

    def take_turn(self) -> CombatAction:
        '''Determines which Head is Taking the turn and takes turn'''
        turns = [self.snake_turn, self.eagle_turn, self.lion_turn]
        return choice(turns)()
