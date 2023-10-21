'''Module for Dungeon Dudes Town Menu'''
import cmd
from ..menu_helpers import banner, clear, format_line
from .save_menu import SaveMenu
from .shop_menu import ShopMenu, check_cost, confirm_purchase
from .dungeon_menu import DungeonMenu

class TownMenu(cmd.Cmd):
    '''Town Menu for Dungeon Dudes'''
    prompt = 'Town > '
    def __init__(self, adventure):
        super().__init__()
        self._session = adventure

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
        '''Prints the Town Menu for Dungeon Dudes'''
        name = self._session.character.name
        clear()
        print(banner())
        print(format_line)
        print(f"{'| Welcome to Town '+ name +' - Prepare for Your Adventure Here':90}{'|':>}")
        print(format_line)
        print(f"{'| Adventure - Explore the Dungeon, Fight Monsters, Gain xp/Gold':90}{'|':>}")
        print(f"{'| Shop      - Visit the Shop':90}{'|':>}")
        print(f"{'| Heal      - Restore HP and Class Resources - (3 Gold plus 2/Level)':90}{'|':>}")
        print(f"{'| Character - View Character Sheet':90}{'|':1>}")
        print(f"{'| Save      - Save Your Game':90}{'|':1>}")
        print(f"{'| Back      - Return to New Game Menu':90}{'|':1>}")
        print(format_line)

    def do_adventure(self, arg): # pylint: disable=unused-argument
        '''Launches Dungeon Crawl with 5 Monster Gauntlet'''
        DungeonMenu(self._session).cmdloop()
        self.display_menu()

    def do_shop(self, arg): # pylint: disable=unused-argument
        '''Launches Shop Menu'''
        ShopMenu(self._session).cmdloop()
        self.display_menu()

    def do_heal(self, arg): # pylint: disable=unused-argument
        '''Prompts user to heal in exchange for Gold'''
        character = self._session.character
        price = 3 + character.level * 2
        if check_cost(character, price):
            if confirm_purchase("Full Heal", price):
                character.gold -= price
                character.hit_points = character.max_hit_points
                character.special = character.max_special
                print("Heal Complete")
                input("Press Enter to Continue...")
                self.display_menu()
            else:
                input("Purchased Cancelled - Press Enter to Continue...")
                self.display_menu()
        else:
            self.display_menu()

    def do_character(self, arg):  # pylint: disable=unused-argument
        '''Prints Character Sheet'''
        clear()
        print(self._session.character)
        self.loop_back()

    def do_save(self, arg): # pylint: disable=unused-argument
        '''Launches Save Game Menu'''
        SaveMenu(self._session).cmdloop()
        self.display_menu()

    def do_back(self, arg): # pylint: disable=unused-argument
        """Back to New Game Menu."""
        return True

    do_EOF = do_back
