import unittest
from src.characters.wizard import Wizard

"""This test needs to be ran int the top level directory in order for it to
properly execute without import errors"""

class TestWizard(unittest.TestCase):
    def setUp(self):
        # Create an instance of the Wizard class for testing
        self.wizard = Wizard("TestWizard")  
        
    def test_attributes(self):
        # Test Wizard's attributes
        self.assertEqual(self.wizard.name, "TestWizard")
        self.assertEqual(self.wizard.char_class, "Wizard")

    def test_level_up(self):
        # Test the level_up method
        initial_level = self.wizard.level
        self.wizard.level_up()
        self.assertEqual(self.wizard.level, initial_level + 1)

    def test_attack(self):
        # Test the attack method
        action = self.wizard.attack()
        self.assertEqual(len(action.actions), 1)
        self.assertEqual(action.message, "")
        
    def test_fire_ball(self):
        # Test the fire_ball method
        can_cast, action = self.wizard.fire_ball()
        # Verify that the Wizard can cast fire_ball
        self.assertTrue(can_cast)  
        # Check that two actions are returned
        self.assertEqual(len(action.actions), 1)  

    def test_blink(self):
        # Test the blink method
        can_cast, action = self.wizard.blink()
        # Verify that the Wizard can cast blink
        self.assertTrue(can_cast)  
        # Check that one action is returned
        self.assertEqual(len(action.actions), 1)  
        
    def test_blizzard(self):
        # Test the blizzard method
        can_cast, action = self.wizard.blizzard()
        # Verify that the Wizard can cast blizzard
        self.assertTrue(can_cast)
        # Check that one action is returned
        self.assertEqual(len(action.actions), 1)  

    def test_lightning_bolt(self):
        # Test the lightning_bolt method
        can_cast, action = self.wizard.lightning_bolt()
        # Verify that the Wizard can cast lightning_bolt
        self.assertTrue(can_cast)  
        # Check that one action is returned
        self.assertEqual(len(action.actions), 1)  

    def test_reflect_damage(self):
        # Test the reflect_damage method
        can_cast, action = self.wizard.reflect_damage()
        # Verify that the Wizard can cast reflect_damage
        self.assertTrue(can_cast)  
        # Check that one action is returned
        self.assertEqual(len(action.actions), 1) 
         
    
if __name__ == '__main__':
    unittest.main()
