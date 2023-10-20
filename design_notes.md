# Dungeon Dudes Project Notes

## Key Objects/Systems

### Key Objects/Data Structures

The following Custom Objects are important to systems of the game and your project will need to interact with them.  Understanding what they do and how they work is important:

* CombatPrint located in `src/dd_data/combat_print.py`
* LimitedDict located in `src/dd_data/limited_dict.py`
* CombatAction located in `src/combat_action.py`

* Offensive and Defensive modifiers (Character sheet)
    * Out of combat static modifiers to Damage types (both offensively and defensively) - it is important to understand how these values are constructed, the ranges they can have, and what they do. 

* You should understand why `Monster` Actions return a `CombatAction` and Character actions return a `Tuple`[`bool`, `CombatAction`]

**Note:** Out of combat static modifiers should be capped at doubling the damage taken/done by a type of damage, and reducing damage taken/done to 10% of base damage (10-200% range).  The `Fighter` class `Unbound Modifiers` passive makes this not apply to them (their is not code example for the implementation of this range in the `Fighter` class.)

* In-Combat Modifiers to offensive and defensive damage types are handled by the `Battle Cries` and `Aura` system in the `Encounter` class.  Understanding how these work is important.

### Shop/Combat AI

A critical difference between the `Monster` classes and the the `Character` classes is construction of the Turn AI for `Monsters` and the `Equipment` generation for `Characters`.  Understanding how th `ShopMenu` works and understanding how the `EncounterMenu` and Combat flow work are important to both these tasks.   

### Game Mechanics

#### Turns:

Many things may happen during a `Combatant` turn, but there is only 1 `Action`.  Everything else is triggering off the attack occurring.  (See Ranger animal companion attacks as an example.)

#### Damage and Defense Power:

Defense Power reduces damage of types that Defense Power mitigates against using the formula:  `damage = damage - (self._defense_power // 2)`

In combat defense mods and damage adjustments are handled by the `Encounter` class.  Static mods to offensive and defensive damage types are handled within the your module.  

## Requirements for Smooth Game Play

* Every Action your Combatant does during combat should print a message to the Combatant terminal.  Study the `CombatPrint` object for insight here.  

* No `Floats` are ever passed between modules, or output from `Getters`.  If you're using `Floats` within your module that's fine, but not data can leave a module as a `Float`.  There is no need for the `Decimal` built-in in this assignment.

* All weapon, armor, and accessory items should be priced in the shop using the same formula to calculate cost as the Fighter equipment.  


