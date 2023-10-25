'''Module to test Undead monsters; place in top level directory'''
import unittest
from src.monsters.undead_src import Zombie, Vampire, Banshee


class TestZombie(unittest.TestCase):
    '''Class to test Zombie'''
    def setUp(self) -> None:
        self.zombie = Zombie(1)

    def test_type(self):
        '''Test instance'''
        self.assertNotEqual(self.zombie, None)
        self.assertIsInstance(self.zombie, Zombie)

    def test_parent(self):
        '''Test MRO'''
        parent: str = str(Zombie.__mro__[1])
        self.assertIn("monsters", parent)


class TestVampire(unittest.TestCase):
    '''Class to test Vampire'''
    def setUp(self) -> None:
        self.vampire = Vampire(1)

    def test_type(self):
        '''Test instance'''
        self.assertNotEqual(self.vampire, None)
        self.assertIsInstance(self.vampire, Vampire)

    def test_parent(self):
        '''Test MRO'''
        parent: str = str(Vampire.__mro__[1])
        self.assertIn("monsters", parent)


class TestBanshee(unittest.TestCase):
    '''Class to test Banshee'''
    def setUp(self) -> None:
        self.banshee = Banshee(1)

    def test_type(self):
        '''Test instance'''
        self.assertNotEqual(self.banshee, None)
        self.assertIsInstance(self.banshee, Banshee)

    def test_parent(self):
        '''Test MRO'''
        parent: str = str(Banshee.__mro__[1])
        self.assertIn("monsters", parent)


if __name__ == "__main__":
    unittest.main()
