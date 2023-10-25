import unittest

from src.characters.cleric import Cleric
from src.combat_action import CombatAction


class TestCleric(unittest.TestCase):
    def setUp(self) -> None:
        self._cleric = Cleric("test")

    def test_char_creation(self):
        self.assertIsInstance(self._cleric, Cleric)
        self.assertIsNotNone(self._cleric.skills_dict)
        self.assertIsNotNone(self._cleric.passive_skills)
        self.assertFalse(self._cleric._avenged)
        self.assertFalse(self._cleric._nodamage)
        self.assertFalse(self._cleric._halfdamage)
        self.assertFalse(self._cleric._retribution)
        self.assertEqual(self._cleric.hit_points, 85)
        self.assertEqual(self._cleric.special, 50)

    def test_level_up(self):
        for i in range(4):
            self._cleric.level_up()
        self.assertEqual(self._cleric.level, 5)
        self.assertEqual(self._cleric.hit_points, 165)
        self.assertEqual(self._cleric.special, 50)

    # def test_heal_special(self):
    #    exp_bool, exp_act = False, CombatAction([("Heal", 0, "Holy", "")], "")
    #    got_bool, got_act = self._cleric.heal()
    #    self.assertEqual(got_bool, exp_bool)
    #    self.assertEqual(exp_act, got_act)
