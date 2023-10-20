'''Meta Data Variables for Dungeon Dudes'''
from typing import Tuple, Dict

damage_types : Tuple[str] = ("Physical", "Poison", "Lightning",
                    "Ice", "Fire", "Holy")

supported_actions : tuple = ("Attack", "Heal", "Aura",
                             "Battle Cry", "Hex", "Escape", "Identify")

defensive_suffix_mapping : Dict[tuple, str]= {
        ("Fire", "Ice"): "the Elements ",
        ("Fire", "Lightning"): "Storm Ward",
        ("Fire", "Holy"): "Sacred Flame",
        ("Fire", "Poison"): "Toxic Ember",
        ("Ice", "Lightning"): "Frostvolt",
        ("Ice", "Holy"): "Divine Frost",
        ("Ice", "Poison"): "Venomous Chill",
        ("Lightning", "Holy"): "Holy Thunder",
        ("Lightning", "Poison"): "Toxic Shock",
        ("Holy", "Poison"): "Blessed Venom"
        }