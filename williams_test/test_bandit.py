'''Module to test Bandit Class'''
import unittest

from src.monsters.humanoid_src import Bandit


class TestBandit(unittest.TestCase):
    def setUp(self) -> None:
        self._bandit = Bandit(1)

    def test_attributes(self):
        self.assertIsInstance(self._bandit, Bandit)
        self.assertEqual(self._bandit.level, 1)
        self.assertEqual(self._bandit.healing_potions, 1)
        self.assertEqual(self._bandit.num_bandits, 3)
        self.assertIsNotNone(self._bandit._hit_points)
        self.assertIsNotNone(self._bandit._damage_type)
        self.assertIsNotNone(self._bandit._dam_modifiers)

    def test_additional_level(self):
        self._bandit = Bandit(9)
        self.assertEqual(self._bandit.num_bandits, 4)
        self.assertEqual(self._bandit.healing_potions, 2)

        self._bandit = Bandit(15)
        self.assertEqual(self._bandit.num_bandits, 5)

    def test_level_up(self):
        for _ in range(9):
            self._bandit.level_up()
        self.assertEqual(self._bandit.level, 10)
