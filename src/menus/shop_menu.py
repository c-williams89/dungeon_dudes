'''Module for Dungeon Dudes Shop Game Menu'''
import cmd
from ..menu_helpers import banner, clear, line_brackets, format_line
from ..characters import Character

def check_cost(customer : Character, price: int) -> bool:
    '''Checks if Customer can afford an Item at Checkout'''
    if customer.gold >= price:
        return True
    def insufficient_funds():
        print("Insufficient Funds")
        input("Press Enter to Continue...")
        return False
    return insufficient_funds()

def confirm_purchase(item : str, cost: int):
    '''Prompts User to Confirm Purchase'''
    response = input(f"Confirm purchase of {item} for {cost}? y/n: ")
    if len(response) > 0:
        if response[0].lower() == "y":
            return True
    return False

class ShopMenu(cmd.Cmd):
    '''Shop Menu for Dungeon Dudes'''
    prompt : str = 'Select Your Purchase > '
    def __init__(self, adventure):
        super().__init__()
        self._session = adventure
        self._customer : Character = adventure.character
        self._healing_potion_price : int = 7 + self._customer.level * 3
        self._scroll_of_escape_price : int = 15 + self._customer.level * 5
        self._inventory = self._session.shop_inventory
        self._weapon_purchased = False
        self._armor_purchased = False
        self._accessory_purchased = False

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

    def make_greeting(self) -> str:
        '''Formats Greeting Line'''
        greeting_start = "Welcome to the Dungeon Dudes Emporium"
        greeting_end = f"Balance: {self._customer.gold} Gold "
        return line_brackets(f"{greeting_start:55}{greeting_end:>33}")

    def format_item(self, label: str, item) -> list:
        '''Formats Equipment Items for Shop Display'''
        print(format_line)
        print(line_brackets(f"{label}:  "))
        print(item)
        print(format_line)

    def format_consumables(self) -> [str, str]:
        '''Formats healing potions and scroll of escape lines'''
        healing_1 = f"Healing_Potion - {self._healing_potion_price} gold each"
        healing_2 = f"Current Inventory: {self._customer.healing_potion} "
        healing_line = line_brackets(f'{healing_1:50}{healing_2:>38}')
        escape_1 = f"Scroll_of_Escape - {self._scroll_of_escape_price} gold each"
        escape_2 = f"Current Inventory: {self._customer.scroll_of_escape} "
        escape_line = line_brackets(f'{escape_1:50}{escape_2:>38}')
        return healing_line, escape_line

    def display_menu(self):
        '''Prints the Shop Menu for Dungeon Dudes'''
        clear()
        print(banner())
        healing_line, escape_line = self.format_consumables()
        print(format_line)
        print(self.make_greeting())
        print(format_line)
        if not self._weapon_purchased:
            self.format_item("Weapon", self._inventory[0])
        if not self._armor_purchased:
            self.format_item("Armor", self._inventory[1])
        if not self._accessory_purchased:
            self.format_item("Accessory", self._inventory[2])
        print(format_line)
        print(healing_line)
        print(format_line)
        print(escape_line)
        print(format_line)

    def do_weapon(self, arg): # pylint: disable=unused-argument
        '''Attempts to Buy Weapon'''
        weapon = self._inventory[0]
        if check_cost(self._customer, weapon.cost):
            if confirm_purchase(weapon.name, weapon.cost):
                old_price : int = self._customer.weapon_cost
                self._customer.equip(weapon)
                self._customer.gold -= weapon.cost
                self._customer.gold += old_price // 2
                self._weapon_purchased = True
                print(f"Successful Equipped New Weapon,"
                      f" Purchased Previous Weapon for {old_price} Gold")
                input("Press Enter to Continue...")
                self.display_menu()
            else:
                input("Purchased Cancelled - Press Enter to Continue...")
                self.display_menu()
        else:
            self.display_menu()

    def do_armor(self, arg): # pylint: disable=unused-argument
        '''Attempts to Buy Armor'''
        armor = self._inventory[1]
        if check_cost(self._customer, armor.cost):
            if confirm_purchase(armor.name, armor.cost):
                old_price : int = self._customer.armor_cost
                self._customer.equip(armor)
                self._customer.gold -= armor.cost
                self._customer.gold += old_price // 2
                self._armor_purchased = True
                print(f"Successful Equipped New Armor,"
                      f" Purchased Previous Armor for {old_price} Gold")
                input("Press Enter to Continue...")
                self.display_menu()
            else:
                input("Purchased Cancelled - Press Enter to Continue...")
                self.display_menu()
        else:
            self.display_menu()

    def do_accessory(self, arg): # pylint: disable=unused-argument
        '''Attempts to Buy Accessory'''
        accessory = self._inventory[2]
        if check_cost(self._customer, accessory.cost):
            if confirm_purchase(accessory.name, accessory.cost):
                old_price : int = self._customer.accessory_cost
                self._customer.equip(accessory)
                self._customer.gold -= accessory.cost
                self._customer.gold += old_price // 2
                self._accessory_purchased = True
                print(f"Successful Equipped New Accessory,"
                      f" Purchased Previous Accessory for {old_price} Gold")
                input("Press Enter to Continue...")
                self.display_menu()
            else:
                input("Purchased Cancelled - Press Enter to Continue...")
                self.display_menu()
        else:
            self.display_menu()

    def do_healing_potion(self, arg): # pylint: disable=unused-argument
        '''Attempts to Buy Healing Potion'''
        if check_cost(self._customer, self._healing_potion_price):
            if confirm_purchase("Healing Potion", self._healing_potion_price):
                self._customer.healing_potion += 1
                self._customer.gold -= self._healing_potion_price
                input("Purchased Successful - Press Enter to Continue...")
                self.display_menu()
            else:
                input("Purchased Cancelled - Press Enter to Continue...")
                self.display_menu()
        else:
            self.display_menu()


    def do_scroll_of_escape(self, arg): # pylint: disable=unused-argument
        '''Attempts to Buy Scroll of Escape'''
        if check_cost(self._customer, self._scroll_of_escape_price):
            if confirm_purchase("Scroll of Escape", self._scroll_of_escape_price):
                self._customer.scroll_of_escape += 1
                self._customer.gold -= self._scroll_of_escape_price
                input("Purchased Successful - Press Enter to Continue...")
                self.display_menu()
            else:
                input("Purchased Cancelled - Press Enter to Continue...")
                self.display_menu()
        else:
            self.display_menu()

    def do_back(self, arg): # pylint: disable=unused-argument
        """Go Back to Town."""
        return True

    do_EOF = do_back
