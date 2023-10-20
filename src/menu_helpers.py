'''Menu Helper Functions for Dungeon Dudes'''
import os

format_line : str  = "*" * 91

def singleton(cls):
    '''Singleton Decorator'''
    instances : dict = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

def banner():
    '''Banner for Character Sheet'''
    banner_text = r'''
________                                             ________            .___             
\______ \  __ __  ____    ____   ____  ____   ____   \______ \  __ __  __| _/____   ______
|    |  \|  |  \/    \  / ___\_/ __ \/  _ \ /    \   |    |  \|  |  \/ __ |/ __ \ /  ___/
|    `   \  |  /   |  \/ /_/  >  ___(  <_> )   |  \  |    `   \  |  / /_/ \  ___/ \___ \ 
/_______  /____/|___|  /\___  / \___  >____/|___|  / /_______  /____/\____ |\___  >____  >
        \/           \//_____/      \/           \/          \/           \/    \/     \/ 
'''
    return banner_text

def clear():
    '''Clear the screen'''
    os.system('cls' if os.name == 'nt' else 'clear')

def line_brackets(line: str) -> str:
    '''Puts brackets on a line and makes it 91 characters wide'''
    new_line = f'{line:88}'
    return f'| {new_line}|'
