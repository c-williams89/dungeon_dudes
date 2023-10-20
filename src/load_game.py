'''Module for Loading Saved Games'''
import pickle
import os
import sys
from .characters import Character
from .dd_data import LimitedDict, CombatPrint

def override():
    '''Prompts User to Verify an Action'''
    response = input("Are you sure you want to continue? y/n: ")
    if len(response) > 0:
        if response[0].lower() == "y":
            return True
    return False

def load_file(file_name) -> [dict, str]:
    '''Loads Pickle File to Dictionary'''
    allowed_keys = ("autosave", "save_1", "save_2", "save_3")
    if os.path.exists(file_name):
        with open(file_name, "rb") as file:
            try:
                saved_games = pickle.load(file)
                if not isinstance(saved_games, LimitedDict):
                    return (LimitedDict(allowed_keys),
                            f"\nError: Invalid file for {file_name}", False)
                return (saved_games, "\n", True)
            except pickle.UnpicklingError:
                return (LimitedDict(allowed_keys),
                        f"\nError: Failed to load saved games from {file_name}", False)
    else:
        default_data = LimitedDict(allowed_keys)
        try:
            with open(file_name, 'wb') as file:
                pickle.dump(default_data, file)
            return (default_data,
                "\nSave File Didn't Exist.  Creating New. - ", True)
        except FileNotFoundError:
            print("Path to directory incurred a File Not Found Error. Check Directory Path.")
            print("Exiting")
            sys.exit()

def save(character: Character, slot = "autosave"):
    '''Auto Saves Character on Keyboard Interrupt'''
    file_name = "src/dd_data/saved_games.pkl"
    saved_games, message, should_continue = load_file(file_name)
    character.printer = None
    if should_continue:
        character.printer = None
        saved_games[slot] = character
        with open(file_name, "wb") as file:
            pickle.dump(saved_games, file)
            character.printer = CombatPrint()
        return f"{message}Autosave complete."
    return message

def load_saves() -> LimitedDict:
    '''Loads the Saved Games for the Load Game Menu'''
    file_name = "src/dd_data/saved_games.pkl"
    return load_file(file_name)[0]
