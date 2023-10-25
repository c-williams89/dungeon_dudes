#!/usr/bin/env python3
'''Need to run the test from the top directory'''

import unittest
from src.characters import Rogue


class TestRogue(unittest.TestCase):
    '''Basic test class for Rogue'''
    # Setup
    def setUp(self):
        self.rogue = Rogue("Rogue")

    def tearDown(self):
        del self.rogue

    def test_base_stat(self):
        '''Test for rogue's level 1 base stat'''
        self.assertEqual(self.rogue.level, 1)
        self.assertEqual(self.rogue.hit_points, 75)
        self.assertEqual(self.rogue.strength, 10)
        self.assertEqual(self.rogue.agility, 12)
        self.assertEqual(self.rogue.intelligence, 5)
        self.assertEqual(self.rogue.special, 1)

    def test_max_stat(self):
        '''Test for rogue's level 50 stat'''
        self.rogue.gain_experience(10000000)
        self.assertEqual(self.rogue.level, 50)
        self.assertEqual(self.rogue.hit_points, 957)
        self.assertEqual(self.rogue.strength, 59)
        self.assertEqual(self.rogue.agility, 110)
        self.assertEqual(self.rogue.intelligence, 54)
        self.assertEqual(self.rogue.special, 26)

    def test_base_skills(self):
        '''Test for rogue's level 1 skills''' \
            '''Should have *Luck* and Passive *Theives Tricks*'''
        self.assertEqual(self.rogue.get_skills_list()[0], "Luck")
        self.assertEqual(self.rogue.passive_skills[1][0], "Theives Tricks")

    def test_luck_skill(self):
        '''Test if luck skill turns the empower flag on'''
        self.assertEqual(self.rogue.empowered, False)
        try:
            self.rogue.luck()
        except AttributeError as exc:
            print(f"Exception {exc} occured")
        self.assertEqual(self.rogue.empowered, True)

    def test_preparation_skill(self):
        '''Test for Preparation Skill'''
        for _ in range(2):
            self.rogue.level_up()
        self.assertEqual(self.rogue.level, 3)
        self.assertEqual(self.rogue.get_skills_list()[-1], "Preparation")
        self.assertEqual(self.rogue.poison_coated, False)
        try:
            self.rogue.preparation()
        except AttributeError as exc:
            print(exc)
        self.assertEqual(self.rogue.poison_coated, True)

    def test_evasion_skill(self):
        '''Test for evasion skill'''
        for _ in range(9):
            self.rogue.level_up()
        self.assertEqual(self.rogue.level, 10)
        self.assertEqual(self.rogue.get_skills_list()[-1], "Evasion")
        self.assertEqual(self.rogue.evasion_active, False)
        try:
            self.rogue.evasion()
        except AttributeError as exc:
            print(exc)
        self.assertEqual(self.rogue.evasion_active, True)
        self.assertEqual(self.rogue.evasion_count, 2)
        self.assertEqual(self.rogue.evasion_chance, 50)

    def test_ambush_skill(self):
        '''Test for ambush skill'''
        for _ in range(12):
            self.rogue.level_up()
        self.assertEqual(self.rogue.level, 13)
        self.assertEqual(self.rogue.get_skills_list()[-1], "Ambush")

    def test_increase_luck_skill(self):
        '''Test for Increase Luck skill'''
        for _ in range(16):
            self.rogue.level_up()
        self.assertEqual(self.rogue.level, 17)
        self.assertEqual(self.rogue.get_skills_list()[-1], "Increase Luck")

    def test_auto_potion_skill(self):
        '''Test for Auto Potion Skill'''
        self.assertEqual(self.rogue.auto_potion_active, False)
        for _ in range(19):
            self.rogue.level_up()
        self.assertEqual(self.rogue.level, 20)
        self.assertEqual(self.rogue.auto_potion_active, True)

    def test_enhanced_abilities_skill(self):
        '''Test for Enhanced Abilities skill'''
        self.assertEqual(self.rogue.enhanced_abilities_on, False)
        for _ in range(24):
            self.rogue.level_up()
        self.assertEqual(self.rogue.level, 25)
        self.assertEqual(self.rogue.enhanced_abilities_on, True)

    def test_weapon(self):
        '''Test for Rogue's weapon'''
        self.rogue.generate_weapon()
        self.assertEqual(self.rogue.weapon_sheet.equipment_type, "Weapon")
        self.assertEqual(self.rogue.weapon_sheet.damage_type, "Physical")
        self.assertEqual(self.rogue.weapon_sheet.subtype, "Dagger")

    def test_armor(self):
        '''Test for Rogue's Armor'''
        self.rogue.generate_armor()
        self.assertEqual(self.rogue.armor_sheet.equipment_type, "Armor")
        self.assertEqual(self.rogue.armor_sheet.subtype, "Medium")

    def test_accessory(self):
        '''Test for Rogue's Accessory'''
        self.rogue.generate_accessory()
        self.assertEqual(self.rogue.accessory_sheet.equipment_type, "Accessory")
        self.assertEqual(self.rogue.accessory_sheet.subtype, "Thieves Tools")


if __name__ == "__main__":
    unittest.main()
