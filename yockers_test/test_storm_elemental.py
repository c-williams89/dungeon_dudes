''' Unit testing for StormElemental '''
import unittest
import unittest.mock
from src.monsters.elemental_src import StormElemental


class TestStormElemental(unittest.TestCase):
    ''' Tests StormElemental class '''

    def setUp(self) -> None:
        self.elemental = StormElemental(1)

    def test_elemental_attributes(self) -> None:
        ''' Tests StormElemental attributes '''
        self.assertIsInstance(self.elemental, StormElemental)
        self.assertEqual(self.elemental.level, 1)
        self.assertEqual(self.elemental.name, "Storm Elemental")
        self.assertEqual(self.elemental.gold, 5)
        self.assertEqual(self.elemental.hit_points, 60)
        self.assertEqual(self.elemental.strength, 5)
        self.assertEqual(self.elemental.agility, 12)
        self.assertEqual(self.elemental.intelligence, 10)
