import unittest

from pynecraft.commands import s
from pynecraft.utils import strcmp


class TestUtils(unittest.TestCase):

    def test_strcmp(self):
        self.assertEqual(
            ('data modify storage pynecraft strcmp.value set value a',
             'execute store success score strcmp_differ pynecraft'
             ' run data modify storage pynecraft strcmp.value set value b'),
            strcmp('a', 'b'))
        self.assertEqual(
            ('data modify storage pynecraft strcmp.value set from entity @s CustomName',
             'execute store success score strcmp_differ pynecraft'
             ' run data modify storage pynecraft strcmp.value set from storage stored value'),
            strcmp((s(), 'CustomName'), ('stored', 'value')))
