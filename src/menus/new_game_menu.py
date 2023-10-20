'''Module for Dungeon Dudes New Game Menu'''
import cmd
from ..menu_helpers import banner, clear, line_brackets, format_line
from ..characters import Character, Fighter, Rogue, Wizard, Cleric, Ranger
from .town_menu import TownMenu

def generate_name() -> str:
    '''Takes Input for Character Name and Validates'''
    no_name : bool = True
    while no_name:
        name : str = input("Please Enter a Character Name: ").strip()
        space_count : int = name.count(' ')
        if space_count <= 2 and name.replace(' ', '').isalpha():
            no_name : bool = False
        else:
            print("Invalid Name Format")
    return name.title()

def name_wrapper(func) -> 'function':
    '''Wrapper for Class Creation to get Character Names'''
    def get_name(*args, **kwargs):
        name = generate_name()
        func(name, *args, **kwargs)

    return get_name

class NewGameMenu(cmd.Cmd):
    '''New Game Menu for Dungeon Dudes'''
    prompt : str = 'New Game > '
    def __init__(self, adventure):
        super().__init__()
        self._session = adventure

    def preloop(self):
        '''Displays Menu When Class __init__ is called'''
        self.display_menu()

    def parseline(self, line : str) -> [str, str, str] :
        '''Parse Input to allow more human friendly input options'''
        command, arg, line = super().parseline(line)
        try:
            command : str = command.lower()
        except AttributeError:
            pass
        return command, arg, line

    def attempt_game_launch(self, class_name : str, character : object):
        '''Checks if an Object is a Valid Character'''
        if isinstance(character, Character):
            self._session.character : Character = character
            TownMenu(self._session).cmdloop()
            self.display_menu()
        else:
            print(f"Error: {class_name} Class has not been Implemented")
            input("Press Enter to go back....")
            self.display_menu()

    def display_menu(self):
        '''Prints the New Game Menu for Dungeon Dudes'''
        clear()
        print(banner())
        print(format_line)
        print(line_brackets("Choose Your Class to Start Your Adventure!"))
        print(line_brackets("Fighter   - Brave Warrior, Skill in Combat Arts"))
        print(line_brackets("Rogue     - Agile Assassin, Master of Poisons and Deception"))
        print(line_brackets("Wizard    - Elemental Spell Caster, Harnessing Powerful Magic"))
        print(line_brackets("Cleric    - Divine Healer, Channeling the Gods to Mend and Smite."))
        print(line_brackets("Ranger    - Nature's Warden, Blending Archery and Animal Companions."))
        print(line_brackets("Back      - Return to Main Menu"))
        print(format_line)

    def do_fighter(self, arg): # pylint: disable=unused-argument
        '''Launches New Game with Fighter Class'''
        name : str = generate_name()
        self.attempt_game_launch("Fighter", Fighter(name))

    def do_rogue(self, arg): # pylint: disable=unused-argument
        '''Launches New Game with Rogue Class'''
        name : str = generate_name()
        self.attempt_game_launch("Rogue", Rogue(name))

    def do_wizard(self, arg): # pylint: disable=unused-argument
        '''Launches New Game with Wizard Class'''
        name : str = generate_name()
        self.attempt_game_launch("Wizard", Wizard(name))

    def do_cleric(self, arg): # pylint: disable=unused-argument
        '''Launches New Game with Cleric Class'''
        name : str = generate_name()
        self.attempt_game_launch("Cleric", Cleric(name))

    def do_ranger(self, arg): # pylint: disable=unused-argument
        '''Launches New Game with Ranger Class'''
        name : str = generate_name()
        self.attempt_game_launch("Ranger", Ranger(name))

    def do_back(self, arg): # pylint: disable=unused-argument
        """Back to Main Menu."""
        return True

    do_EOF = do_back
