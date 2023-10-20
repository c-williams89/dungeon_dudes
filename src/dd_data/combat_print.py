'''Combat Terminal Print Function for Dungeon Dudes'''
from ..menu_helpers import line_brackets, clear

def singleton(cls):
    '''Singleton Decorator for CombatPrint Class'''
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singleton
class CombatPrint:
    '''Combat Print Class for Dungeon Dudes'''
    def __init__(self,
                 limit : int =8, line_size : int =87):
        self._limit = limit
        self._history = []
        self._line_size = line_size
        self._encounter = None
        self._format_line = "*" * (line_size + 4)

    def format_combat_log(self) -> str:
        '''Ensures Combat Log takes up self._limit lines'''
        return "\n".join([line_brackets(message) for message
                     in self._history] + [line_brackets('')]
                     * (self._limit - len(self._history)))

    def __call__(self, *args, menu=None, **kwargs):
        '''
        Clears Screen
        Prints Encounter Title Pane,
        Prints Message in Line_Size Chucks up to Max Lines and saves history
        Prints Encounter Menu Pane
        '''

        if args:
            full_message = " ".join(map(str, args))
            chunks = [full_message[i:i+self._line_size]
                    for i in range(0, len(full_message), self._line_size)]

            for message in chunks:
                self._history.append(message)
                if len(self._history) > self._limit:
                    self._history.pop(0)
        clear()
        original_print = print
        if not menu:
            original_print(self._encounter, self.format_combat_log(), self._format_line,
                    self._encounter.menu(), self._format_line, sep="\n", **kwargs)
        else:
            original_print(self._encounter, self.format_combat_log(), self._format_line,
                    menu, self._format_line, sep="\n", **kwargs)

    def clear_history(self):
        '''
        Clears History so Subsequent Encounters 
        don't have the same combat text
        '''
        self._history = []

    def set_encounter(self, encounter: 'Encounter'):
        '''Sets Current Encounter'''
        self._encounter = encounter

    @property
    def get_history(self):
        '''Getter for History'''
        return self._history
