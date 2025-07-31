import unittest

from pynecraft.commands import Text
from pynecraft.fonts import *


class TestFonts(unittest.TestCase):
    def test_simple(self):
        simple = Text.text('foo').bold()
        self.assertEqual([simple], BookWrap().add(simple).pages()[0])

    def test_page_break(self):
        s = ''
        for i in range(50):
            s += f'{i}\n'
        self.assertEqual([[Text('0\n1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n11\n12\n13')],
                          [Text('14\n15\n16\n17\n18\n19\n20\n21\n22\n23\n24\n25\n26\n27')],
                          [Text('28\n29\n30\n31\n32\n33\n34\n35\n36\n37\n38\n39\n40\n41')],
                          [Text('42\n43\n44\n45\n46\n47\n48\n49\n')]], BookWrap().add(s).pages())
