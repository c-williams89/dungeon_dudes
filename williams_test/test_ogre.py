'''Module to test Ogre Class'''
import unittest

from src.monsters.humanoid_src import Ogre


class TestOgre(unittest.TestCase):
    def setUp(self) -> None:
        self._ogre = Ogre(1)

    def test_attributes(self):
        self.assertIsInstance(self._ogre, Ogre)
        self.assertEqual(self._ogre.level, 1)
        self.assertFalse(self._ogre._two_minds)
