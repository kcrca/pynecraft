import unittest

from pynecraft.base import EAST, NORTH, SOUTH, WEST, r
from pynecraft.function import Function
from pynecraft.menus import Menu, Submenu


def func(x, **kwargs):
    return Function(x, **kwargs)


def action(x):
    return x


class TestMenu(unittest.TestCase):
    def test_empty_size(self):
        menu = Menu(func, action)
        self.assertEqual((0, 0), menu._dim())

    def test_one_size(self):
        menu = Menu(func, action)
        menu.add('One')
        self.assertEqual((1, 1), menu._dim())

    def test_nosubs_size(self):
        menu = Menu(func, action)
        menu.add(('One', 'Two', 'Three'))
        self.assertEqual((3, 1), menu._dim())

    def test_basic_sub_size(self):
        menu = Menu(func, action)
        submenu = Submenu(menu, 'Sub').add(('1', '2', '3'))
        menu.add(submenu)
        self.assertEqual((3, 2), menu._dim())

    def test_second_sub_size(self):
        menu = Menu(func, action)
        submenu = Submenu(menu, 'Sub').add(('1', '2', '3'))
        menu.add('empty').add(submenu)
        self.assertEqual((4, 2), menu._dim())

    def test_second_area(self):
        menu = Menu(func, action)
        submenu = Submenu(menu, 'Sub').add(('1', '2', '3'))
        menu.add('empty').add(submenu)
        pos = r(1, 2, 3)
        self.assertEqual(r(1, 1, 0), menu.end(pos, NORTH))
        self.assertEqual(r(1, 1, 6), menu.end(pos, SOUTH))
        self.assertEqual(r(4, 1, 3), menu.end(pos, EAST))
        self.assertEqual(r(-2, 1, 3), menu.end(pos, WEST))
