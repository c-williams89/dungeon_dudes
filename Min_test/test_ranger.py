'''Need to Run the Unit Test from the Top level directory,
Not the test folder'''

import unittest
from src.characters.ranger import Ranger

class TestRanger(unittest.TestCase):
    '''Test Ranger Class'''
    def setUp(self) -> None:
        self.character = Ranger("Ranger")

    def test_base_stat(self):
        self.assertEqual(self.character._hit_points, 90)
        self.assertEqual(self.character.strength, 7)
        self.assertEqual(self.character.agility, 14)
        self.assertEqual(self.character.intelligence, 5)
        self.assertEqual(self.character._special, 2)

    def test_base_att_def_power(self):
        self.character.base_att_def_power()
        self.assertEqual(self.character._attack_power,
                         (self.character.strength +\
                          self.character.agility // 2))
        self.assertEqual(self.character._defense_power,
                         self.character.agility // 2)

    def test_equipment_weapon(self):
        '''Check if the weapon stat increases as character levels up'''
        weapon = self.character._weapon
        weapon_name = weapon._name
        print(weapon_name)
        # Check the modifier of the bow
        if "Wrath" in weapon_name.split() or "Defense" in weapon_name.split():
            self.assertEqual(len(weapon._dam_modifiers), 1)
            self.assertEqual(weapon._dam_modifiers[0][1] <=\
                             self.character._level + 10, True)

    def test_equipment_armor(self):
        '''Check if the Armor Resist is set correctly'''
        armor = self.character._armor
        armor_modifier = armor._def_modifiers
        total_resist = 0
        for resist in armor_modifier:
            total_resist += resist[1]
        self.assertEqual(total_resist, (self.character._level * 3) + 30)


    def test_active_skill(self):
        '''Test to check if the Ranger learn skills correctly'''
        # Test when character level is 1
        skills_list = self.character.get_skills_list()
        skills_dict = self.character.get_skills()
        print(f"Skills available at level 1: {skills_list}")
        self.assertEqual(self.character._level, 1)
        self.assertEqual(self.character.summon_wolf,
                         skills_dict["Summon Wolf Companion"])
        self.assertTrue("Summon Wolf Companion" in skills_list, True)

        # Test when character level is 10
        for _ in range(9):
            self.character.level_up()
        skills_list = self.character.get_skills_list()
        skills_dict = self.character.get_skills()
        print(f"Skills available at level 10: {skills_list}")
        self.assertEqual(self.character._level, 10)
        self.assertEqual(self.character.take_aim,
                         skills_dict["Take Aim"])
        self.assertTrue("Take Aim" in skills_list, True)
        self.assertEqual(self.character.summon_bear,
                         skills_dict["Summon Bear Companion"])
        self.assertTrue("Summon Bear Companion" in skills_list, True)
        self.assertEqual(self.character.steel_trap,
                         skills_dict["Steel Trap"])
        self.assertTrue("Steel Trap" in skills_list, True)

        # Test when character level is 20
        for _ in range(10):
            self.character.level_up()
        skills_list = self.character.get_skills_list()
        skills_dict = self.character.get_skills()
        print(f"Skills available at level 10: {skills_list}")
        self.assertEqual(self.character._level, 20)
        self.assertEqual(self.character.summon_cat,
                         skills_dict["Summon Cat Companion"])
        self.assertTrue("Summon Cat Companion" in skills_list, True)

    def test_attack(self):
        '''Test to check if the Ranger and companions attack correctly'''
        damage = 10
        # Test with no companion
        combat = self.character.modify_damage(damage)
        self.assertEqual(len(combat), 1)
        # With one companion
        self.character._companion["Wolf"][0] = True
        combat = self.character.modify_damage(damage)
        self.assertEqual(len(combat), 2)
        # With two companions
        self.character._companion["Bear"][0] = True
        combat = self.character.modify_damage(damage)
        self.assertEqual(len(combat), 3)
        # With two companions and trap on
        self.character._trap[0] = True
        combat = self.character.modify_damage(damage)
        self.assertEqual(len(combat), 4)

    def test_max_stat(self):
        self.character.gain_experience(10000000)
        self.assertEqual(self.character._hit_points, 1168)
        self.assertEqual(self.character.strength, 56)
        self.assertEqual(self.character.agility, 112)
        self.assertEqual(self.character.intelligence, 5)
        self.assertEqual(self.character._special, 51)


if __name__ == "__main__":
    unittest.main()