'''Module for Dungeon Dudes Main Menu'''
import cmd
from .new_game_menu import NewGameMenu
from .load_menu import LoadMenu
from ..menu_helpers import banner, clear, line_brackets, format_line

class MainMenu(cmd.Cmd):
    '''Main Menu for Dungeon Dudes'''
    prompt : str = 'Main Menu > '
    def __init__(self, adventure):
        super().__init__()
        self._session = adventure

    def preloop(self):
        '''Displays Menu When Class __init__ is called'''
        self.display_menu()

    def parseline(self, line : str) -> [str, str, str]:
        '''Parse Input to allow more human friendly input options'''
        command, arg, line = super().parseline(line)
        try:
            command : str = command.lower()
        except AttributeError:
            pass
        return command, arg, line

    def display_menu(self):
        '''Prints the Main Menu for Dungeon Dudes'''
        clear()
        print(banner())
        print(format_line)
        print(line_brackets("New  - Start a New Game"))
        print(line_brackets("Load - Load a Saved Game"))
        print(line_brackets("Exit - Exit Game"))
        print(format_line)

    def do_new(self, arg): # pylint: disable=unused-argument
        '''Launches New Game Menu'''
        NewGameMenu(self._session).cmdloop()
        self.display_menu()

    def do_load(self, arg): # pylint: disable=unused-argument
        """Launches Load Game Menu"""
        LoadMenu(self._session).cmdloop()
        self.display_menu()

    def do_exit(self, arg): # pylint: disable=unused-argument
        """Exit the program."""
        return True

    do_EOF = do_exit
