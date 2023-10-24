'''Module for Encounter Special Attack Menu'''
import cmd
from ..characters import Character
from ..combatant_abc import Combatant
from ..encounter import Encounter
from ..dd_data import CombatPrint
from ..menu_helpers import line_brackets

class SpecialAttackMenu(cmd.Cmd):
    '''Special Attack Menu'''

    def __init__(self, adventure, encounter):
        super().__init__()
        self.printer : CombatPrint = CombatPrint()
        self._session = adventure
        self._encounter : Encounter = encounter
        self.player_1 : Character = encounter.combatant_1
        self.player_2 : Combatant = encounter.combatant_2
        self.prompt : str = f'Special Attack: {self.player_1.level} {self.player_1.char_class} > '
        self._command_dict : dict = self.construct_command_dict(self.player_1.get_skills())
        self._command_menu : str = self.menu()

    @staticmethod
    def construct_command_dict(skills_dict):
        '''Constructs Command Dict from Character skills dict'''
        return ({i+1: {k: v} if (i < len(skills_dict)) else {} for i, (k, v)
                 in enumerate(list(skills_dict.items()) +
                [({}, {}) for _ in range(6 - len(skills_dict))])})

    def menu(self) -> str:
        '''Prints Combat Menu Options'''
        items : list = [list(value.keys())[0] if value else ""
                 for value in self._command_dict.values()]

        line_1 : str = line_brackets(f" 1. {items[0]:39}| 2. {items[1]:39}")
        line_2 : str = line_brackets(f" 3. {items[2]:39}| 4. {items[3]:39}")
        line_3 : str = line_brackets(f" 5. {items[4]:39}| 6. {items[5]:39}")
        return "\n".join([line_1, line_2, line_3])

    def loop_back(self):
        '''Loop Back'''
        self.display_menu()

    def preloop(self):
        '''Displays Menu When Class __init__ is called'''
        self.display_menu()

    def parseline(self, line) -> [str, str, str]:
        '''Parse Input to allow more human friendly input options'''
        command, arg, line = super().parseline(line)
        try:
            command : str = command.lower()
        except AttributeError:
            pass
        return command, arg, line

    def display_menu(self):
        '''Prints the Encounter Pane for Dungeon Dudes'''
        self.printer(menu=self._command_menu)

    def execute_special_action(self, number):
        '''Executes special action after checking if it exists'''
        func_map : dict = {"Aura": self._encounter.parse_aura,
                           "Hex": self._encounter.parse_hex,
                           "Battle Cry" : self._encounter.parse_battle_cry,
                           "Identify" : self._encounter.parse_identify}
        turn_over, actions = list(self._command_dict[number].values())[0]()
        actions = actions.actions
        action_types = [action[0] for action in actions]
        if "Escape" in action_types:
            self._encounter.escape_flag = True
            return True
        for action in actions:
            if action[0] == "Heal": # healing logic done within character locally
                continue
            if action[0] != "Attack":
                func_map[action[0]](action, 1)
            else:
                self._encounter.parse_attack(action, 1)
                if not self._encounter.combatants_alive:
                    break
        if turn_over:
            return True
        return False

    def do_1(self, arg): # pylint: disable=unused-argument
        '''Execute Action 1 if it exists'''
        if self._command_dict[1]:
            result = self.execute_special_action(1)
            if result:
                self._encounter.player_spl_att_complete = True
                return True
            return True

    def do_2(self, arg): # pylint: disable=unused-argument
        '''Execute Action 2 if it exists'''
        if self._command_dict[2]:
            result = self.execute_special_action(2)
            if result:
                self._encounter.player_spl_att_complete = True
                return True
            return True

    def do_3(self, arg): # pylint: disable=unused-argument
        '''Execute Action 3 if it exists'''
        if self._command_dict[3]:
            result = self.execute_special_action(3)
            if result:
                self._encounter.player_spl_att_complete = True
                return True
            return True

    def do_4(self, arg): # pylint: disable=unused-argument
        '''Execute Action 4 if it exists'''
        if self._command_dict[4]:
            result = self.execute_special_action(4)
            if result:
                self._encounter.player_spl_att_complete = True
                return True
            return True

    def do_5(self, arg): # pylint: disable=unused-argument
        '''Execute Action 5 if it exists'''
        if self._command_dict[5]:
            result = self.execute_special_action(5)
            if result:
                self._encounter.player_spl_att_complete = True
                return True
            return True

    def do_6(self, arg): # pylint: disable=unused-argument
        '''Execute Action 6 if it exists'''
        if self._command_dict[6]:
            result = self.execute_special_action(6)
            if result:
                self._encounter.player_spl_att_complete = True
                return True
            return True

    def do_back(self, arg): # pylint: disable=unused-argument
        """Back to Encounter Menu."""
        return True

    do_EOF = do_back
