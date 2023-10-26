#!/usr/bin/env python3
''' Unit testing for FrostElemental '''
import unittest
import unittest.mock
from src.monsters.elemental_src import FrostElemental


class TestFrostElemental(unittest.TestCase):
    ''' Tests FrostElemental class '''

    def setUp(self) -> None:
        self.elemental = FrostElemental(1)

    def test_elemental_attributes(self) -> None:
        ''' Tests FrostElemental attributes '''
        self.assertIsInstance(self.elemental, FrostElemental)
        self.assertEqual(self.elemental.level, 1)
        self.assertEqual(self.elemental.name, "Frost Elemental")
        self.assertEqual(self.elemental.gold, 5)
        self.assertEqual(self.elemental.hit_points, 78)
        self.assertEqual(self.elemental.strength, 5)
        self.assertEqual(self.elemental.agility, 12)
        self.assertEqual(self.elemental.intelligence, 10)
