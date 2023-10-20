'''Random Encounter Constructor for Dungeon Dudes'''
from random import choice
from .characters import Character
from .monsters.beast_src import Drake, Griffon, Chimera
from .monsters.elemental_src import FireElemental, FrostElemental, StormElemental
from .monsters.humanoid_src import Bandit, Ogre, Murloc
from .monsters.golem_src import StoneGolem, TreasureGolem, MetallicGolem
from .monsters.undead_src import Zombie, Vampire, Banshee
from .monsters import Monster
from .encounter import Encounter

def encounter_generator(character : Character) -> Encounter:
    '''Returns Sample Encounter'''
    possible_monsters = [Drake, Griffon, Chimera,
                         FireElemental, FrostElemental, StormElemental,
                         Bandit, Ogre, Murloc,
                         StoneGolem, TreasureGolem, MetallicGolem,
                         Banshee, Vampire, Zombie]
    implemented_monsters = [monster for monster in possible_monsters
                            if issubclass(monster, Monster)]
    return Encounter(character, choice(implemented_monsters)(character.level))
