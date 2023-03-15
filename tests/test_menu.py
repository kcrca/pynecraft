import unittest

from pynecraft.base import r, NORTH, SOUTH, EAST, WEST
from restworld.menus import Menu, Submenu

dummy = lambda x: x


class TestMenu(unittest.TestCase):
    def test_empty_size(self):
        menu = Menu('base', dummy, dummy)
        self.assertEqual((0, 0), menu._dim())

    def test_one_size(self):
        menu = Menu('base', dummy, dummy)
        menu.add('One')
        self.assertEqual((1, 1), menu._dim())

    def test_nosubs_size(self):
        menu = Menu('base', dummy, dummy)
        menu.add(('One', 'Two', 'Three'))
        self.assertEqual((3, 1), menu._dim())

    def test_basic_sub_size(self):
        menu = Menu('base', dummy, dummy)
        submenu = Submenu('Sub', menu).add(('1', '2', '3'))
        menu.add(submenu)
        self.assertEqual((3, 2), menu._dim())

    def test_second_sub_size(self):
        menu = Menu('base', dummy, dummy)
        submenu = Submenu('Sub', menu).add(('1', '2', '3'))
        menu.add('empty').add(submenu)
        self.assertEqual((4, 2), menu._dim())

    def test_second_area(self):
        menu = Menu('base', dummy, dummy)
        submenu = Submenu('Sub', menu).add(('1', '2', '3'))
        menu.add('empty').add(submenu)
        pos = r(1, 2, 3)
        self.assertEquals(r(1, 1, 0), menu.end(pos, NORTH))
        self.assertEquals(r(1, 1, 6), menu.end(pos, SOUTH))
        self.assertEquals(r(4, 1, 3), menu.end(pos, EAST))
        self.assertEquals(r(-2, 1, 3), menu.end(pos, WEST))
