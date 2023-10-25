'''Module for Dungeon Dudes Town Menu'''
import cmd
from ..encounter import Encounter
from ..characters import Character
from ..monsters import Monster
from ..dd_data import CombatPrint
from ..combat_action import CombatAction
from .special_attack_menu import SpecialAttackMenu

class EncounterMenu(cmd.Cmd):
    '''Encounter Menu for Dungeon Dudes'''

    def __init__(self, adventure, encounter):
        super().__init__()
        self.printer : CombatPrint = CombatPrint()
        self.printer.clear_history()
        self.printer.set_encounter(encounter)
        self._session = adventure
        self._encounter : Encounter = encounter
        self.player_1_turn : bool = True
        self.player_1 : Character = encounter.combatant_1
        self.player_2 : Monster = encounter.combatant_2
        self.player_1_alive : bool = True
        self.player_2_alive : bool = True
        self.prompt = f'{self.player_1.name}: {self.player_1.level} {self.player_1.char_class} > '
        if not self._encounter.turn_order():
            self.printer(f"{self.player_2.name} acts before you are ready!")
            self.ai_turn()

    def ai_turn(self):
        '''Calls Monster to Preform their turn'''
        actions : CombatAction = self.player_2.take_turn().actions
        result = self.send_actions(actions, 2)
        if result:
            return True
        self.player_1_turn : bool = True
        self.loop_back()
        return False

    def loop_back(self):
        '''Menu if Player Turn, AI if not'''
        if self.player_1_turn:
            self.display_menu()
        else:
            result = self.ai_turn()
            if result:
                return True

    def send_actions(self, actions, num):
        '''Parses Actions'''
        func_map : dict = {"Aura": self._encounter.parse_aura,
                           "Hex": self._encounter.parse_hex,
                           "Battle Cry" : self._encounter.parse_battle_cry,
                           "Identify" : self._encounter.parse_identify}
        action_types = [action[0] for action in actions]
        if "Escape" in action_types:
            self.non_scroll_escape(num)
            return True
        for action in actions:
            if action[0] == "Heal": # healing logic done within character locally
                continue
            if action[0] != "Attack":
                func_map[action[0]](action, num)
            else:
                self._encounter.parse_attack(action, num)
                if not self._encounter.combatants_alive():
                    return True
        return False

    def do_attack(self, arg):
        '''Does attack action for active player'''
        actions : CombatAction = self.player_1.attack()
        result = self.send_actions(actions.actions, 1)
        if result:
            return True
        self.player_1_turn : bool = False
        if self.player_2.hit_points == 0:
            self.player_2_alive : bool = False
            return True
        self.loop_back()

    def do_special_attack(self, arg):
        '''Launches Special Attack Menu for active player'''
        SpecialAttackMenu(self._session, self._encounter).cmdloop()
        if self._encounter.escape_flag:
            self.non_scroll_escape(1)
            return True
        if self._encounter.player_spl_att_complete:
            self.player_1_turn : bool = False
            self._encounter.player_spl_att_complete: bool = False
        if self.player_2.hit_points == 0:
            self.player_2_alive : bool = False
            return True
        self.loop_back()


    def do_healing_potion(self, arg):
        '''Uses Healing Potion for active player'''
        success, actions = self.player_1.use_healing_potion()
        if success:
            result = self.send_actions(actions.actions, 1)
            if result:
                return True
            self.player_1_turn : bool = False
        if self.player_2.hit_points == 0:
            self.player_2_alive : bool = False
            return True
        self.loop_back()

    def non_scroll_escape(self, num):
        '''Escapes to Town when triggered by something other than scroll'''
        if num == 1:
            self.printer(f"{self.player_1.name} escapes to town")
        else:
            self.printer(f"{self.player_2.name} flees the battle")
        input("Press Enter to Continue")
        self.do_scroll_of_escape("")

    def do_scroll_of_escape(self, arg):
        '''Active Player ends Combat with a scroll of escape'''
        if not self.player_1_turn:
            return True
        if self.player_1.scroll_of_escape > 0:
            self.player_1.scroll_of_escape -= 1
            self.printer(f"{self.player_1.name} escapes to town with a scroll of escape")
            return True
        self.loop_back()

    def preloop(self):
        '''Displays Menu When Class __init__ is called'''
        self.display_menu()

    def parseline(self, line):
        '''Parse Input to allow more human friendly input options'''
        command, arg, line = super().parseline(line)
        try:
            command : str = command.lower()
        except AttributeError:
            pass
        return command, arg, line

    def display_menu(self):
        '''Prints the Encounter Pane for Dungeon Dudes'''
        self.printer()

    def do_back(self, arg): # pylint: disable=unused-argument
        """Back to Town Menu."""
        self.do_scroll_of_escape("")

    do_EOF = do_back
