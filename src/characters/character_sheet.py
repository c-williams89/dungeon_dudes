'''Character Sheet Generator'''
from typing import TYPE_CHECKING
from ..menu_helpers import format_line

if TYPE_CHECKING:
    from .character_abc import Character

def pipe_wrapper(func):
    '''
    Wraps Function in Pipe Formatting
    Does not enforce line length like 
    ..menu_helpers.linebrackets
    '''
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return f'| {result} |'
    return wrapper

def character_sheet(character: 'Character'):
    '''Creates Character Sheet in Human Readable Format'''

    stats_lines = format_stats(character)
    stats_1, stats_2, stats_3, stats_4 = stats_lines

    character_sheet_lines = [
        format_line,
        name_line(character),
        format_line,
        stats_section_headers(),
        format_line,
        stats_1,
        stats_2,
        stats_3,
        stats_4,
        format_line,
        modifiers_section_headers(),
        format_line,
        "\n".join(modifier_lines(character)),
        str(character.weapon_sheet),
        str(character.armor_sheet),
        str(character.accessory_sheet),
        format_line,
        experience_display(character),
        format_line

    ]
    return "\n".join(character_sheet_lines)

@pipe_wrapper
def name_line(character :'Character') -> str:
    '''Name line for Character Sheet'''
    right_aligned = f"{'Level ' + str(character.level) + ' ' + character.char_class}"
    name_string = f"Character Sheet for: {character.name:<36}{right_aligned:>30}"
    return name_string

@pipe_wrapper
def modifiers_section_headers() -> str:
    '''Section Headers for Offensive/Defensive Modifiers and Learned Skills'''
    return f"{'Damage Modifiers:':28}{'| Resists:':22}{'| Skills: ':37}"

def modifier_lines(character: 'Character') -> str:
    '''Formats All Modifier and learned skill information'''
    skills_list : list = character.get_skills_list()
    dam_types : tuple = character.damage_types
    skills_list.extend([''] * (len(dam_types)-(len(skills_list))))
    dam_modifiers : dict = character.damage_modifiers
    def_modifiers : dict = character.defense_modifiers
    modifiers = []
    for i, dam_type in enumerate(dam_types):
        modifiers.append((f'{dam_type}: {dam_modifiers.get(dam_type, 100)}',
                          f'{dam_type}: {100 - def_modifiers.get(dam_type, 100)}',
                          skills_list[i]))
        @pipe_wrapper
        def format_mod_line(modifier: tuple) -> str:
            return f"{modifier[0]:28}{'| ' + modifier[1]:22}{'| '+ modifier[2]:37}"
    return [format_mod_line(modifier) for modifier in modifiers]

@pipe_wrapper
def stats_section_headers() -> str:
    '''Section Headers for Combat Stats, Stats, and Equipment'''
    return f"{'Combat Stats:':28}{'| Ability Scores:':22}{'| Equipment: ':37}"

@pipe_wrapper
def experience_display(character:'Character') -> str:
    '''Formats Experience Display Line'''
    exp_this_level = f"Exp Gained This Level: {character.experience_points}"
    exp_next_level = f"Exp to Next Level: {character.experience_to_next}"
    return f"{exp_this_level:44}{exp_next_level:>43}"

def format_stats(character :'Character'):
    '''Formats Stat Lines for Character Sheet'''
    combat_1 : str = f"{'| Hit Points: '+ f'{character.hit_points}/{character.max_hit_points}':30}"
    stats_1 : str = f"{'| Strength: ' + str(character.strength):22}"
    equipment_1 : str = f"| {'Weapon: ' + character.weapon[:27]:35} |"
    special_label : str = f"{character.special_resource}: "
    special_values : str = f"{character.special}/{character.max_special}"

    combat_2 : str = f"{'| ' + special_label + special_values:30}"
    stats_2 : str = f"{'| Agility: ' + str(character.agility):22}"
    equipment_2 : str = f"| {'Armor: ' + character.armor[:28]:35} |"

    combat_3 : str = f"{'| Attack Power: ' + str(character.attack_power):30}"
    stats_3 : str = f"{'| Intelligence: ' + str(character.intelligence):22}"
    index = 33 - len(character.accessory_type)
    equipment_3 : str = f"| {character.accessory_type + ': ' + character.accessory[:index]:35} |"
    combat_4 : str = f"{'| Defense Power: ' + str(character.defense_power):30}"
    stats_4 : str = f"{'| Battles Won : ' + str(character.battles_won):22}"
    equipment_4 : str = f"| {'Gold: ' + str(character.gold):35} |"

    stat_lines : list = ["".join([combat_1, stats_1, equipment_1]),
                  "".join([combat_2, stats_2, equipment_2]),
                  "".join([combat_3, stats_3, equipment_3]), 
                  "".join([combat_4, stats_4, equipment_4])]

    return stat_lines
