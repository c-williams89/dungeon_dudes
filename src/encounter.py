'''Module for the Encounter Class for Dungeon Dudes'''
from typing import Tuple, Dict
from random import randint
from .combatant_abc import Combatant
from .characters import Character
from .combat_action import CombatAction
from .dd_data import LimitedDict, CombatPrint 
from .dd_data.meta_data import damage_types
from .menu_helpers import line_brackets

class Encounter:
    '''Encounter Class for Dungeon Dudes'''
    def __init__(self, combatant_1 : Combatant, combatant_2 : Combatant):
        self._combatant_1 : Character = combatant_1
        self._combatant_2 : Combatant = combatant_2
        self._combatant_1_aura : LimitedDict = LimitedDict(damage_types, default_value=100)
        self._combatant_1_battle_cry : LimitedDict = LimitedDict(damage_types, default_value=100)
        self._combatant_2_aura : dict = LimitedDict(damage_types, default_value=100)
        self._combatant_2_battle_cry : dict = LimitedDict(damage_types, default_value=100)
        self._combatant_identified : Dict[int, bool] = {1 : True, 2: True}
        self.escape_flag : bool = False
        self.combatant_1_alive : bool = True
        self.combatant_2_alive : bool = True
        self.player_spl_att_complete : bool = False
        self._damage_com_1 = LimitedDict(damage_types, default_value=0)
        self._damage_com_2 = LimitedDict(damage_types, default_value=0)
        self._turn_count : int = 1
        self.printer = CombatPrint()

    @property
    def combatant_1(self) -> Combatant:
        '''Getter for Combatant 1'''
        return self._combatant_1

    @property
    def combatant_2(self) -> Combatant:
        '''Getter for Combatant 2'''
        return self._combatant_2

    def combatants_alive(self) -> bool:
        '''Returns if all combatants are still alive'''
        return self.combatant_1_alive and self.combatant_2_alive

    def get_modifier(self, dm_type: str, com_num: int) -> int:
        '''Gets the modifier for com_num doing dm_type to opponent'''
        if com_num == 1:
            aura_mod : int = self._combatant_2_aura[dm_type]
            offensive_mod : int = self.clamp_modifier(self._combatant_1_battle_cry[dm_type])
        else:
            aura_mod : int = self._combatant_1_aura[dm_type]
            offensive_mod : int = self.clamp_modifier(self._combatant_2_battle_cry[dm_type])
        defensive_mod : int = self.clamp_modifier(200-aura_mod)
        return defensive_mod/100 * offensive_mod/100

    def parse_attack(self, action: CombatAction, com_num : int):
        '''Parses Attack Actions'''
        damage : int = action[1]
        dm_type : str = action[2]
        dm_message : str = action[3]
        if com_num == 1:
            mod : float = self.get_modifier(dm_type, 1)
            self.send_attacks(int(damage*mod), dm_type, dm_message, 1)
        else:
            mod : float = self.get_modifier(dm_type, 2)
            self.send_attacks(int(damage*mod), dm_type, dm_message, 2)

    def send_attacks(self, damage : int, dm_type : str, dm_message : str, com_num : int):
        '''Sends attacks to combatant and checks if they're alive'''
        if com_num == 1:
            alive : bool = self._combatant_2.take_damage(damage, dm_type, dm_message)
            if not alive:
                self.combatant_2_alive = False
        else:
            alive : bool = self._combatant_1.take_damage(damage, dm_type, dm_message)
            if not alive:
                self.combatant_1_alive = False

    @staticmethod
    def clamp_modifier(mod : float) -> float:
        '''Ensures a modifier is between 0.1 and 2'''
        return max(10, min(mod, 200))

    def turn_order(self) -> Tuple[int]:
        '''Determines Turn Order from Agility Scores'''
        agility_1 = self.combatant_1.defense_power
        agility_2 = self.combatant_2.agility
        initiative_1 : int = agility_1 + randint(1, max(agility_1, agility_2))
        initiative_2 : int = agility_2 + randint(1, max(agility_1, agility_2))
        return True if initiative_1 >= initiative_2 else False

    def parse_heal(self, action: tuple, com_num : int):
        '''Parses Heal Actions'''

    def parse_aura(self, action: tuple, com_num : int):
        '''Parses Aura Actions'''
        if com_num == 1:
            self._combatant_1_aura[action[2]] += action[1]
        else:
            self._combatant_2_aura[action[2]] += action[1]
        self.printer()

    def parse_battle_cry(self, action: tuple, com_num : int):
        '''Parses Battle Cry Actions'''
        if com_num == 1:
            self._combatant_1_battle_cry[action[2]] += action[1]
        else:
            self._combatant_2_battle_cry[action[2]] += action[1]
        self.printer()

    def parse_hex(self, action: tuple, com_num : int):
        '''Parses Hex Actions'''
        if com_num == 1:
            self._combatant_2_aura[action[2]] -= action[1]
        else:
            self._combatant_1_aura[action[2]] -= action[1]
        self.printer()

    def parse_identify(self, action: tuple, com_num : int): # pylint: disable=unused-argument
        '''Parses Fortify Actions'''
        if com_num == 1:
            self._combatant_identified[2] : bool = True
        else:
            self._combatant_identified[1] : bool = True

    def identified(self, value, com_num):
        '''Obscures Value on Character Pane if target not identified'''
        return value if self._combatant_identified[com_num] else "??"

    def modifier_lines(self) -> str:
        '''Formats All Modifier information'''
        combatant : Combatant = self._combatant_1
        combatant2 : Combatant  = self._combatant_2
        dam_types : tuple = combatant.damage_types
        dam_modifiers : dict = combatant.damage_modifiers
        def_modifiers : dict = combatant.defense_modifiers
        dam_modifiers2 : dict = combatant2.damage_modifiers
        def_modifiers2 : dict = combatant2.defense_modifiers
        modifiers = []
        for _, dam_type in enumerate(dam_types):
            modifiers.append((f'{dam_type}: {dam_modifiers.get(dam_type, 100)}',
                            f'{dam_type}: {100 - def_modifiers.get(dam_type, 100)}',
                            f'{dam_type}: {dam_modifiers2.get(dam_type, 100)}',
                            f'{dam_type}: {100 - def_modifiers2.get(dam_type, 100)}'))
        return modifiers

    def combat_modifier_lines(self):
        '''Formats all Aura and Battle Cry Information'''
        clamp = self.clamp_modifier
        dam_types : tuple = self._combatant_1.damage_types
        dam_modifiers : dict = self._combatant_1_battle_cry
        def_modifiers : dict = self._combatant_1_aura
        dam_modifiers2 : dict = self._combatant_2_battle_cry
        def_modifiers2 : dict = self._combatant_2_aura
        modifiers = []
        for _, dam_type in enumerate(dam_types):
            modifiers.append((f'{dam_type}: {clamp(dam_modifiers.get(dam_type, 100))}',
                            f'{dam_type}: {clamp(200 -def_modifiers.get(dam_type, 100))}',
                            f'{dam_type}: {clamp(dam_modifiers2.get(dam_type, 100))}',
                            f'{dam_type}: {clamp(200 -def_modifiers2.get(dam_type, 100))}'))
        return modifiers


    def menu(self):
        '''Prints Combat Menu Options'''
        heal_potion_str : str = f" Healing_Potion ({self.combatant_1.healing_potion})"
        escape_scroll_str : str = f" Scroll_of_Escape ({self.combatant_1.scroll_of_escape})"
        line_1 = line_brackets(f"{'Attack':43}|{heal_potion_str:43}")
        line_2 = line_brackets(f"{'Special_Attack':43}|{escape_scroll_str:43}")
        line_3 = line_brackets(f"{'':43}|{'':43}")
        return "\n".join([line_1, line_2, line_3])

    def __str__(self):
        '''Prints out Character Panes in Combat'''
        char_1 = self._combatant_1
        char_2 = self._combatant_2
        format_line = "*" * 91
        lines = [format_line]
        title_1 = f"{f'{char_1.name}':30}{f'{char_1.char_class}: {char_1.level} ':>13}"
        title_2 = f"{f'{char_2.name}':30}{f'{char_2.char_class}: {char_2.level} ':>13}"
        lines.extend([line_brackets(f"{title_1}| {title_2}"), format_line])
        hp_val_1 = f'{self.identified(char_1.hit_points, 1)}/{self.identified(char_1.max_hit_points, 1)}'
        sp_val_1 = (f'{self.identified(char_1.special_resource, 1)}: {self.identified(char_1.special, 1)}'
                             if char_1.special else "")
        hp_val_2 = f'{self.identified(char_2.hit_points, 2)}/{self.identified(char_2.max_hit_points, 2)}'
        sp_val_2 = (f'{self.identified(char_2.special_resource, 2)}: {self.identified(char_2.special, 2)}'
                             if char_2.special else "")
        hp_sp_1 = f"{f'HP: {hp_val_1}':30}{f'{sp_val_1} ':>13}"
        hp_sp_2 = f"{f'HP: {hp_val_2}':30}{f'{sp_val_2} ':>13}"
        att_1 = f"{'Attack Power: ' + str(self.identified(char_1.attack_power, 1)):21}"
        def_1 = f"{'Defense Power:' + str(self.identified(char_1.defense_power, 1)) + ' ':>22}"
        att_2 = f"{'Attack Power: ' + str(self.identified(char_2.attack_power, 2)):21}"
        def_2 = f"{'Defense Power:' + str(self.identified(char_2.defense_power, 2)) + ' ':>22}"
        modifier_title = f"{f'Offensive':21}{f'| Defensive':22}{f'| Offensive':22}{f'| Defensive':22}"
        lines.extend([line_brackets(f"{hp_sp_1}| {hp_sp_2}"), 
                      line_brackets(f"{att_1}{def_1}| {att_2}{def_2}"),
                      format_line, f"|{'-' * 38}  Modifiers  {'-' * 38}|", format_line,
                      line_brackets(modifier_title), format_line]
                      )
        modifiers = self.modifier_lines()
        for _, mod in enumerate(modifiers):
            line_pt1 = f"{f'{self.identified(mod[0], 1):21}'f'| {self.identified(mod[1], 1):20}'}"
            line_pt2 = f"{f'| {self.identified(mod[2], 2):21}'f'| {self.identified(mod[3], 2)}'}"
            lines.append(line_brackets(f"{line_pt1}{line_pt2}"))
        combat_mod_title = f"{f'Battle Cry':21}{f'| Aura':22}{f'| Battle Cry':22}{f'| Aura':22}"
        lines.extend([format_line, line_brackets(combat_mod_title), format_line])
        combat_mods = self.combat_modifier_lines()
        for _, mod in enumerate(combat_mods):
            line_pt1 = f"{f'{self.identified(mod[0], 1):21}'f'| {self.identified(mod[1], 1):20}'}"
            line_pt2 = f"{f'| {self.identified(mod[2], 2):21}'f'| {self.identified(mod[3], 2)}'}"
            lines.append(line_brackets(f"{line_pt1}{line_pt2}"))
        lines.append(format_line)

        return "\n".join(lines)
