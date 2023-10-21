# Summary of Changes 20 October 2023

## Bug Fixes

`None`

## Formatting Changes

Updated `dungeon_menu.py` and `town_menu.py` to use `line_brackets` instead of manual string formatting.

## Flavor Changes

Introduction for "Golems" paragraph has been added to `manual_dungeon_dudes.adoc`

## Shop Prices:

Healing Potion Price:  _Old: 7 + (3*character.level)_, **New: 9 + character.level** 

Scroll of Escape: _Old: 15 + (5*character.level)_, **New: 13 + (2*character.level)**

## Town Menu Changes:

Healing:  _Old: 5*character.level_, **New: 3+(2*character.level)**

## Dungeon Crawl Changes:

Number of battles before automatically returning to town reduced from 5 to 4.

## Class Changes:

### Fighter:

* Shield Slam Removed
* **New Skill:** Whirlwind, level 3 - deals damage based on 75% `attack_power` to all enemies. 
* Added Combat Print message for Critical Hits

### Wizard:

* `Magic` armor now offers a `Physical` damage reduction when above 50% `max_mana`
* Wizard `hit_point` growth is now 12 per turn (up from 10)
* **New Skill:** Blink, level 2 - Wizard Escapes to town

_Wizard balance changes to address the reality they often times find it impossible to get pass level 1-2.  Early Wizard leveling should be very challenging still,but hopefully should not feel impossible_

## Monster Changes:

`Monster` Non-Physical Damage decreased approximately 20-30% across the board.  This is reflected in the `manual_dungeon_dudes.adoc` and in the `Beast` Monster type in the code base.  

# Summary of Changes 21 October 2023

## Manual

### Hit Point Growth Adjustments

* Hit Point growth for both Ogre types has been lowered (initial `hit_points` unchanged)
* Hit Point growth for Banshees has been lowered (initial `hit_points` unchanged)

## Accessory Power

* Accessory Relative Attack/Defense power bonuses have been increased across the board.
  * This is a change in the manual for all classes
  * This is a code base change for the `Fighter` class
  
## Bug Fixes

Fixed bug where damage could be negative in the face of sufficient defense power/mitigation and enemy damage variance.  

Fixed bug where Monsters were surprise attacking in combat when player won the initiative roll.  

## Reverted Changes:

## Dungeon Crawl Changes:

Number of battles before automatically returning to town reduced from 5 to 4.

Now reverted back to 5.

