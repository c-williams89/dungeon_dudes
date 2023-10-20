'''Module for Dungeon Dudes Save Game Menu'''
import cmd
from ..menu_helpers import banner, clear, line_brackets, format_line
from ..load_game import load_saves, save, override
from ..characters import Character
from ..dd_data import LimitedDict

class SaveMenu(cmd.Cmd):
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

    def attempt_save(self, key: str):
        '''Saves Character and Prompts if Slot not EMPTY'''
        if isinstance(self._saves[key], str):
            save(self._session.character, key)
            input(f"Save to {key.capitalize()} Successful Press Enter to go back to Town...")
            return True
        elif isinstance(self._saves[key], Character):
            rep_char : Character = self._saves[key]
            name : str = rep_char.name
            char_class : str= rep_char.char_class
            level : int = rep_char.level
            warning = f"This would save over {name}, Level: {level} {char_class}!"
            print(warning)
            if override():
                save(self._session.character, key)
                input("Saved Successfully Press Enter to Continue")
                return True
            else:
                input("Save Aborted Press Enter to Continue...")
                return False

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
        '''Prints the Save Menu for Dungeon Dudes'''
        clear()
        self.get_saves()
        print(banner())
        print(format_line)
        print(*self._formatted_saves[1:], sep="\n")
        print(line_brackets('Back - Go Back'))
        print(format_line)

    def do_save_1(self, arg): # pylint: disable=unused-argument
        '''Attempts to Save Slot 1'''
        if self.attempt_save("save_1"):
            return True
        self.display_menu()

    def do_save_2(self, arg): # pylint: disable=unused-argument
        '''Attempts to Save Slot 2'''
        if self.attempt_save("save_2"):
            return True
        self.display_menu()

    def do_save_3(self, arg): # pylint: disable=unused-argument
        '''Attempts to Save Slot 3'''
        if self.attempt_save("save_3"):
            return True
        self.display_menu()

    def do_back(self, arg): # pylint: disable=unused-argument
        """Exit the program."""
        return True

    do_EOF = do_back