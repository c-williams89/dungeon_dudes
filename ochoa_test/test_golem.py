'''unit tests for golem modules'''
import unittest
from src.monsters.golem_src import StoneGolem, TreasureGolem, MetallicGolem

class TestStoneGolem(unittest.TestCase):
    '''Class to test stone golems'''
    def setUp(self) -> None:
        self._golem = StoneGolem(1)

    def test_attributes(self):
        self.assertNotEqual(self._golem, None)
        self.assertIsInstance(self._golem, StoneGolem)
        self.assertEqual(self._golem.level, 1)
        self.assertEqual(self._golem._damage_type, "Physical")
        self.assertIsNotNone(self._golem._hit_points)
        self.assertIsNotNone(self._golem._dam_modifiers)

class TestTreasureGolem(unittest.TestCase):
    '''Class to test treasure golems'''
    def setUp(self) -> None:
        self._golem = TreasureGolem(1)

    def test_attributes(self):
        self.assertNotEqual(self._golem, None)
        self.assertIsInstance(self._golem, TreasureGolem)
        self.assertEqual(self._golem.level, 1)
        self.assertIsNotNone(self._golem._hit_points)
        self.assertIsNotNone(self._golem._dam_modifiers)

class TestMetallicGolem(unittest.TestCase):
    '''Class to test metallic golems'''
    def setUp(self) -> None:
        self._golem = MetallicGolem(1)

    def test_attributes(self):
        self.assertNotEqual(self._golem, None)
        self.assertIsInstance(self._golem, MetallicGolem)
        self.assertEqual(self._golem.level, 1)
        self.assertEqual(self._golem._damage_type, "Physical")
        self.assertIsNotNone(self._golem._hit_points)
        self.assertIsNotNone(self._golem._dam_modifiers)

if __name__ == "__main__":
    unittest.main()
