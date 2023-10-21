'''Module for Dungeon Dudes Town Menu'''
import cmd
from ..menu_helpers import banner, clear, format_line
from ..encounter import Encounter
from ..characters import Character
from .encounter_menu import EncounterMenu
from ..encounter_helpers import encounter_generator
from ..dd_data import CombatPrint

class DungeonMenu(cmd.Cmd):
    '''Encounter Menu for Dungeon Dudes'''
    prompt = 'Action > '
    def __init__(self, adventure):
        super().__init__()
        self._character : Character = adventure.character
        self._session = adventure
        self._encounter_count = 0
        self._amount_before_town = 4

    def loop_back(self):
        '''Loops User Back to Menu after Pressing Enter'''
        input("Press Enter to go back...")
        self.display_menu()

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
        '''Prints the Adventure Menu for Dungeon Dudes'''
        name = self._session.character.name
        clear()
        print(banner())
        print(format_line)
        print(f"{'| Welcome to Adventure '+ name +' - Prepare for Your Adventure Here':90}{'|':>}")
        print(format_line)
        print(f"{'| Start     - Begin your Dungeon Crawl, Gain xp/Gold':90}{'|':>}")
        print(f"{'| Back      - Return to Town':90}{'|':1>}")
        print(format_line)

    def do_start(self, arg): # pylint: disable=unused-argument
        '''Launches Dungeon Crawl with 4 Monster Gauntlet'''
        printer = CombatPrint()
        encounter : Encounter = encounter_generator(self._session.character)
        self._session.active_encounter = True
        EncounterMenu(self._session, encounter).cmdloop()
        if encounter.combatant_1_alive and encounter.combatant_2_alive:
            printer("Teleported Back to Town...")
            self._session.active_encounter = False
            input("Press Enter to Continue... ")
            return True
        if not encounter.combatant_2_alive:
            printer(f"{encounter.combatant_1.name} is victorious against"
                  f" {encounter.combatant_2.name}!")
            self._character.win_battle(encounter.combatant_2)
            self._encounter_count += 1
            if self._encounter_count < self._amount_before_town:
                input("Press Enter to Continue...")
                return self.do_start(None)
            else:
                printer("Returning to Town...")
                printer(f"You've Successfully Completed {self._amount_before_town} Battles!")
                self._session.active_encounter = False
                input("Press Enter to Continue...")
                return True

    def do_back(self, arg): # pylint: disable=unused-argument
        """Back to Town Menu."""
        return True

    do_EOF = do_back
