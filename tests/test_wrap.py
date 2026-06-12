import unittest

from pynecraft._font_data import MISSING
from pynecraft.commands import Text
from pynecraft.wrap import _char_advance, _parse_markdown, _Span, _str_advance, BookWrap, wrap


class TestStrAdvance(unittest.TestCase):
    def test_hello_normal(self):
        self.assertEqual(24.0, _str_advance('hello', False))

    def test_hello_bold(self):
        self.assertEqual(29.0, _str_advance('hello', True))

    def test_space(self):
        self.assertEqual(4.0, _str_advance(' ', False))

    def test_empty(self):
        self.assertEqual(0.0, _str_advance('', False))

    def test_missing_char(self):
        self.assertEqual(MISSING[0], _char_advance('', False))
        self.assertEqual(MISSING[1], _char_advance('', True))


class TestParseMarkdown(unittest.TestCase):
    def test_plain(self):
        self.assertEqual([_Span('hello')], _parse_markdown('hello'))

    def test_bold(self):
        self.assertEqual([_Span('bold', bold=True)], _parse_markdown('**bold**'))

    def test_italic(self):
        self.assertEqual([_Span('italic', italic=True)], _parse_markdown('*italic*'))

    def test_bold_italic(self):
        self.assertEqual([_Span('both', bold=True, italic=True)], _parse_markdown('***both***'))

    def test_heading(self):
        self.assertEqual([_Span('hi\n', bold=True)], _parse_markdown('# hi\n'))

    def test_mixed(self):
        self.assertEqual(
            [_Span('plain '), _Span('bold', bold=True), _Span(' end')],
            _parse_markdown('plain **bold** end'),
        )

    def test_color(self):
        self.assertEqual([_Span('hello', color='red')], _parse_markdown('[hello]{red}'))

    def test_color_stray_bracket(self):
        # stray '[' not followed by ']{color}' is treated as plain text (split at '[')
        self.assertEqual([_Span('['), _Span('hello')], _parse_markdown('[hello'))


class TestWrap(unittest.TestCase):
    def test_fits_single_line(self):
        # 'hello world' = 24 + 4 + 27 = 55px exactly
        self.assertEqual([[Text.text('hello world')]], wrap(55, 1, 'hello world'))

    def test_wraps_to_next_line(self):
        # width 54: 'hello'(24) + ' '(4) + 'world'(27) = 55 > 54 → wrap
        self.assertEqual([[Text.text('hello')], [Text.text('world')]], wrap(54, 1, 'hello world'))

    def test_explicit_newline(self):
        self.assertEqual([[Text.text('hello'), Text.text('world')]], wrap(100, 3, 'hello\nworld'))

    def test_page_overflow(self):
        result = wrap(100, 2, 'line1\nline2\nline3')
        self.assertEqual([[Text.text('line1'), Text.text('line2')], [Text.text('line3')]], result)

    def test_bold_markdown(self):
        self.assertEqual([[Text.text('hello').bold()]], wrap(100, 2, '**hello**'))

    def test_italic_markdown(self):
        self.assertEqual([[Text.text('hi').italic()]], wrap(100, 2, '*hi*'))

    def test_text_object_passthrough(self):
        t = Text.text('pass').bold()
        self.assertEqual([[t]], wrap(100, 2, t))

    def test_empty_items(self):
        self.assertEqual([], wrap(100, 2))

    def test_color_markdown(self):
        self.assertEqual([[Text.text('hello').color('red')]], wrap(100, 2, '[hello]{red}'))

    def test_trailing_space_stripped(self):
        # leading/trailing spaces on a wrapped line are dropped
        pages = wrap(30, 2, 'hi there')
        for page in pages:
            for line in page:
                self.assertFalse(line['text'].startswith(' '))
                self.assertFalse(line['text'].endswith(' '))


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
            'Lorem ipsum dolor sit amet, consecte-tur adipiscing elit. Donec condimentum aliquet nisl. Phasellus non '
            'tincidunt nibh, vel aliquam turpis. Proin sit amet libero nec nunc efficitur egestas. Phasellus sed mi '
            'dictum, mattis est eu, molestie dolor. Mauris sodales in erat iaculis molestie. Donec tempor vitae '
            'turpis et gravida. Duis et ornare orci, vitae lacinia sapien. Sed congue justo vel dapibus porta. Nulla '
            'pretium sollicitudin odio, quis eleifend metus molestie ac. Vivamus convallis augue nec ex dictum '
            'tristique. Donec porttitor magna ac purus laoreet, ac eleifend dui hendrerit.')).pages()
        self.assertLess(1, len(pages))
        # Check for breaking at hyphen
        self.assertIn('cte-\ntur', pages[0][0]['text'], 'No break at hyphen')
