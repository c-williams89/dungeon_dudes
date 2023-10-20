'''Character Equipment management for Dungeon Dudes'''
from typing import Tuple, List
from collections import defaultdict
from ...menu_helpers import line_brackets

def can_equip(item_compatibility : list, item_type : str) -> bool:
    '''Returns if Item can be Equipped by Class'''
    if item_type in item_compatibility:
        return True
    return False

class Equipment:
    '''Equipment class for Dungeon Dudes'''
    def __init__(self, equipment_type : Tuple, name: str, attack : int = 0,
                 armor : int = 0, cost : int = 0):
        self._name : str = name
        self._equipment_type : str = equipment_type[0]
        self._equipment_subtype : str = equipment_type[1]
        self.item_stats = (attack, armor)
        self._cost = cost

    @property
    def name(self) -> str:
        '''Getter for Equipment Name'''
        return self._name

    @property
    def equipment_type(self) -> str:
        '''Getter for Equipment Type'''
        return self._equipment_type

    @property
    def subtype(self) -> str:
        '''Getter for Weapon Subtype'''
        return self._equipment_subtype

    @property
    def item_stats(self) -> Tuple[int, int]:
        '''Getter for Equipment Item Stats'''
        return self._item_stats

    @item_stats.setter
    def item_stats(self, att_arm : Tuple[int, int]):
        attack, armor = att_arm
        self._item_stats = (attack, armor)

    @property
    def cost(self):
        '''Getter for Equipment Value'''
        return self._cost

class Weapon(Equipment):
    '''Weapon Equipment Type'''
    def __init__(self, equipment_type : str, name: str, attack : int, special: dict,
                 armor : int = 0, dmg_type : str = "Physical", cost=0):
        self._dam_modifiers : List[Tuple[str, int]] = special["Offensive"]
        super().__init__(("Weapon", equipment_type), name, attack=attack,
                         armor=armor, cost=cost)
        self._damage_type : str = dmg_type

    @property
    def damage_type(self):
        '''Damage Type Getter'''
        return self._damage_type

    @property
    def damage_modifiers(self) -> List[Tuple[str, int]]:
        '''Getter for attack modifiers'''
        return self._dam_modifiers

    def __str__(self):
        format_line = "*"*91
        lines :list = [format_line]
        column_1 : list = ["Attack", "Armor"]
        column_2 : list = self._dam_modifiers
        title_1a = f"{f'{self.name} (Weapon):':55}"
        title_1b = f"{f'Price: {self.cost} Gold ':>33}"
        lines.append(line_brackets(f'{title_1a}{title_1b}'))
        lines.append(format_line)
        lines.append(line_brackets(
            f'{"Attack and Armor: ":26}{"| Damage Modifiers: ":31}{"| Defense Modifiers: ":31}'))
        lines.append(format_line)
        rows : int = max(len(column_1), len(column_2))
        column_1.extend([""] * (rows - len(column_1)))
        column_2.extend([("","")] * (rows - len(column_2)))

        for i, dam_type in enumerate(column_1):
            col_2 = column_2[i]
            col_2 = f"{col_2[0]}{':' if col_2[0] else ''} {col_2[1]}"
            if i < 2:
                lines.append(line_brackets(
                    f"{f'{dam_type}: {self.item_stats[i]}':26}"+
                    f"{f'| {col_2}':31}{f'| '}"
                ))
            else:
                lines.append(line_brackets(
                    f"{f'':26}{f'| {col_2}':31}{f'| '}"
                ))
        return "\n".join(lines)

class Armor(Equipment):
    '''Armor Equipment Type'''
    def __init__(self, equipment_type : str, name: str, armor : int,
                 special: dict, attack : int = 0, cost : int = 0):
        self._def_modifiers : List[Tuple[str, int]] = special["Defensive"]
        super().__init__(("Armor", equipment_type), name, attack=attack,
                         armor=armor, cost=cost)

    @property
    def defense_modifiers(self) -> List[Tuple[str, int]]:
        '''Getter for Defense Modifiers'''
        return self._def_modifiers

    def __str__(self):
        format_line = "*"*91
        lines :list = [format_line]
        column_1 : list = ["Attack", "Armor"]
        column_3 : list = self._def_modifiers
        title_1a = f"{f'{self.name} (Armor):':55}"
        title_1b = f"{f'Price: {self.cost} Gold ':>33}"
        lines.append(line_brackets(f'{title_1a}{title_1b}'))
        lines.append(format_line)
        lines.append(line_brackets(
            f'{"Attack and Armor: ":26}{"| Damage Modifiers: ":31}{"| Defense Modifiers: ":31}'))
        lines.append(format_line)
        rows : int = max(len(column_1), len(column_3))
        column_1.extend([""] * (rows - len(column_1)))
        column_3.extend([("", "")] * (rows - len(column_3)))

        for i, dam_type in enumerate(column_1):
            col_3 = column_3[i]
            col_3 = f"{col_3[0]}{':' if col_3[0] else ''} {col_3[1]}"
            if i < 2:
                lines.append(line_brackets(
                    f"{f'{dam_type}: {self.item_stats[i]}':26}"+
                    f"{f'| ':31}{f'| {col_3}'}"
                ))
            else:
                lines.append(line_brackets(
                    f"{f'':26}{f'| ':31}{f'| {col_3}'}"
                ))
        return "\n".join(lines)

class Accessory(Equipment):
    '''Accessory Equipment'''
    def __init__(self, equipment_type : str, name: str, special: dict, cost : int = 0):
        attack : int = special["Attack"]
        armor : int = special["Armor"]
        self._dam_modifiers : List[Tuple[str, int]] = special["Offensive"]
        self._def_modifiers : List[Tuple[str, int]] = special["Defensive"]
        super().__init__(("Accessory", equipment_type), name, attack=attack,
                         armor=armor, cost=cost)

    @property
    def damage_modifiers(self) -> List[Tuple[str, int]]:
        '''Getter for damage modifiers'''
        return self._dam_modifiers

    @property
    def defense_modifiers(self) -> List[Tuple[str, int]]:
        '''Getter for Defense Modifiers'''
        return self._def_modifiers

    def __str__(self):
        format_line = "*"*91
        lines :list = [format_line]
        column_1 : list = ["Attack", "Armor"]
        column_2 : list = self._dam_modifiers
        column_3 : list = self._def_modifiers
        title_1a = f"{f'{self.name} (Accessory):':55}"
        title_1b = f"{f'Price: {self.cost} Gold ':>33}"
        lines.append(line_brackets(f'{title_1a}{title_1b}'))
        lines.append(format_line)
        lines.append(line_brackets(
            f'{"Attack and Armor: ":26}{"| Damage Modifiers: ":31}{"| Defense Modifiers: ":31}'))
        lines.append(format_line)
        rows : int = max(len(column_1), len(column_2), len(column_3))
        column_1.extend([""] * (rows - len(column_1)))
        column_2.extend([("","")] * (rows - len(column_2)))
        column_3.extend([("", "")] * (rows - len(column_3)))

        for i, dam_type in enumerate(column_1):
            col_2 = column_2[i]
            col_3 = column_3[i]
            col_2 = f"{col_2[0]}{':' if col_2[0] else ''} {col_2[1]}"
            col_3 = f"{col_3[0]}{':' if col_3[0] else ''} {col_3[1]}"
            if i < 2:
                lines.append(line_brackets(
                    f"{f'{dam_type}: {self.item_stats[i]}':26}"+
                    f"{f'| {col_2}':31}{f'| {col_3}'}"
                ))
            else:
                lines.append(line_brackets(
                    f"{f'':26}{f'| {col_2}':31}{f'| {col_3}'}"
                ))
        return "\n".join(lines)
