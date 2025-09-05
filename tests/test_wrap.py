import unittest

from pynecraft.commands import Text
from pynecraft.wrap import *


class TestFonts(unittest.TestCase):
    def test_simple(self):
        simple = Text.text('foo').bold()
        pages = BookWrap().add(simple).pages()
        self.assertEqual([simple], pages[0])

    def test_page_break(self):
        test_text = ''
        for i in range(50):
            test_text += f'{i}\n'
        self.assertEqual([[Text('0\n1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n11\n12\n13')],
                          [Text('14\n15\n16\n17\n18\n19\n20\n21\n22\n23\n24\n25\n26\n27')],
                          [Text('28\n29\n30\n31\n32\n33\n34\n35\n36\n37\n38\n39\n40\n41')],
                          [Text('42\n43\n44\n45\n46\n47\n48\n49\n')]], BookWrap().add(test_text).pages())

    def test_wrapping(self):
        # We don't yet have the right font, so the right count isn't known
        pages = BookWrap().add(Text(
            'Lorem ipsum dolor sit amet, consecte-tur adipiscing elit. Donec condimentum aliquet nisl. Phasellus non tincidunt nibh, vel aliquam turpis. Proin sit amet libero nec nunc efficitur egestas. Phasellus sed mi dictum, mattis est eu, molestie dolor. Mauris sodales in erat iaculis molestie. Donec tempor vitae turpis et gravida. Duis et ornare orci, vitae lacinia sapien. Sed congue justo vel dapibus porta. Nulla pretium sollicitudin odio, quis eleifend metus molestie ac. Vivamus convallis augue nec ex dictum tristique. Donec porttitor magna ac purus laoreet, ac eleifend dui hendrerit.')).pages()
        self.assertLess(1, len(pages))
        # Check for breaking at hyphen
        self.assertIn('cte-\ntur', pages[0][0]['text'], 'No break at hyphen')
