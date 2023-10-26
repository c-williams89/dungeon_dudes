#!/usr/bin/env python3
''' Unit testing for FireElemental '''
import unittest
import unittest.mock
from src.monsters.elemental_src import FireElemental


class TestFireElemental(unittest.TestCase):
    ''' Tests FireElemental class '''

    def setUp(self) -> None:
        self.elemental = FireElemental(1)

    def test_elemental_attributes(self) -> None:
        ''' Tests FireElemental attributes '''
        self.assertIsInstance(self.elemental, FireElemental)
        self.assertEqual(self.elemental.level, 1)
        self.assertEqual(self.elemental.name, "Lesser Fire Elemental")
        self.assertEqual(self.elemental.gold, 5)
        self.assertEqual(self.elemental.hit_points, 65)
        self.assertEqual(self.elemental.strength, 10)
        self.assertEqual(self.elemental.agility, 10)
        self.assertEqual(self.elemental.intelligence, 5)
