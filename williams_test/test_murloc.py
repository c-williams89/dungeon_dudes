'''Module to test Murloc class'''
import unittest

from src.monsters.humanoid_src import Murloc


class TestMurloc(unittest.TestCase):
    def setUp(self):
        self._murloc = Murloc(1)

    def test_attributes(self):
        self.assertIsInstance(self._murloc, Murloc)
        self.assertEqual(self._murloc.level, 1)
        self.assertEqual(self._murloc.healing_potions, 1)
        self.assertEqual(self._murloc.tribe_size, 4)
        self.assertIsNotNone(self._murloc._hit_points)
        self.assertIsNotNone(self._murloc.damage_type)
        self.assertIsNotNone(self._murloc._dam_modifiers)
        self.assertFalse(self._murloc.poisoned)
        self.assertEqual(self._murloc.damage_type, "Physical")

    def test_additional_level(self):
        self._murloc = Murloc(10)
        self.assertEqual(self._murloc.tribe_size, 5)
