'''Main for Dungeon Dudes Game'''
import sys
import platform
from src import MainMenu, save
from src.adventure import Adventure

if platform.system() == "Windows":
    import ctypes

class UnsupportedOSError(Exception):
    '''Exception for Unsupported OS'''

def set_green_text():
    '''Sets Dungeon Dudes Terminal Screen to Green'''
    system = platform.system()
    if system == "Windows":
        std_output_handle = -11
        handle = ctypes.windll.kernel32.GetStdHandle(std_output_handle)
        foreground_green = 0x02
        ctypes.windll.kernel32.SetConsoleTextAttribute(handle, foreground_green)
    elif system == "Linux" or system == "Darwin":
        sys.stdout.write("\033[32m")
    else:
        raise UnsupportedOSError("Unsupported OS")

if __name__ == "__main__":
    set_green_text()
    adventure = Adventure()
    try:
        MainMenu(adventure).cmdloop()
    except KeyboardInterrupt:
        if adventure.character is None:
            print("Game Exited - Play Again Soon!")
        else:
            adventure.character.printer = None
            if not adventure.active_encounter:
                print(save(adventure.character))
            else:
                if adventure.character.scroll_of_escape > 0:
                    adventure.character.scroll_of_escape -= 1
                    print(f'Successfully used a Scroll of Escape to flee the Battle'
                         f'You have {adventure.character.scroll_of_escape} remaining')
                    print(save(adventure.character))
                else:
                    adventure.character.character_death()
                    print(save(adventure.character))
