'''Module for Dungeon Dudes Load Saved Game Menu'''
import cmd
from ..menu_helpers import banner, clear, line_brackets, format_line
from ..load_game import load_saves
from ..characters import Character
from ..dd_data import LimitedDict, CombatPrint
from .town_menu import TownMenu

class LoadMenu(cmd.Cmd):
    '''Load Menu for Dungeon Dudes'''
    prompt : str = 'Load Saved Game > '
    def __init__(self, adventure):
        super().__init__()
        self._session = adventure
        self._saves : LimitedDict = load_saves()
        self._formatted_saves : list = ([self.format_saves(key, value )
                                  for key, value in self._saves.items()])

    def preloop(self):
        '''Displays Menu When Class __init__ is called'''
        self.display_menu()

    def attempt_load(self, key: str):
        '''Loads Saved File if it's not EMPTY'''
        if isinstance(self._saves[key], Character):
            self._session.character = self._saves[key]
            self._session.character.printer = CombatPrint()
            TownMenu(self._session).cmdloop()
        else:
            print(f"Error Loading {key}.  Not a Valid Character")
            input("Press Enter to Continue....")
            self.display_menu()

    def parseline(self, line : str) -> [str, str, str]:
        '''Parse Input to allow more human friendly input options'''
        command, arg, line = super().parseline(line)
        try:
            command : str = command.lower()
        except AttributeError:
            pass
        return command, arg, line

    @staticmethod
    def format_saves(slot : str, character : [Character, str]) -> str:
        '''Formats Saved Characters in Readable String'''
        if isinstance(character, Character):
            formatted_save = (f'{slot.capitalize()} - {character.name}: Level {character.level}'
                            f' {character.char_class}, {character.battles_won} Battles Won')
            return line_brackets(formatted_save)
        formatted_save = f'{slot.capitalize()} - {character}'
        return line_brackets(formatted_save)

    def get_saves(self):
        '''Ensures self._saves is up to date'''
        self._saves : LimitedDict = load_saves()
        self._formatted_saves = ([self.format_saves(key, value )
                                  for key, value in self._saves.items()])

    def display_menu(self):
        '''Prints the Load Menu for Dungeon Dudes'''
        clear()
        self.get_saves()
        print(banner())
        print(format_line)
        print(*self._formatted_saves, sep="\n")
        print(line_brackets('Back - Go Back'))
        print(format_line)

    def do_autosave(self, arg): # pylint: disable=unused-argument
        '''Attempts to Load Autosave'''
        self.attempt_load("autosave")

    def do_save_1(self, arg): # pylint: disable=unused-argument
        '''Attempts to Load Save Slot 1'''
        self.attempt_load("save_1")

    def do_save_2(self, arg): # pylint: disable=unused-argument
        '''Attempts to Load Save Slot 2'''
        self.attempt_load("save_2")

    def do_save_3(self, arg): # pylint: disable=unused-argument
        '''Attempts to Load Save Slot 3'''
        self.attempt_load("save_3")

    def do_back(self, arg): # pylint: disable=unused-argument
        """Exit the program."""
        return True

    do_EOF = do_back
