import unittest

from pynecraft._font_data import MISSING
from pynecraft.commands import Text
from pynecraft.wrap import _char_advance, _Span, _str_advance, BookWrap, wrap


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
        self.assertEqual(MISSING[0], _char_advance('', False))
        self.assertEqual(MISSING[1], _char_advance('', True))

    def test_cyrillic_narrow_4px(self):
        # Cyrillic: east_asian_width Ambiguous → 4px, bold unchanged
        self.assertEqual(4.0, _char_advance('Я', False))
        self.assertEqual(4.0, _char_advance('Я', True))

    def test_cjk_wide_8px(self):
        # CJK: east_asian_width Wide → 8px, bold unchanged
        self.assertEqual(8.0, _char_advance('中', False))
        self.assertEqual(8.0, _char_advance('中', True))

    def test_latin_extension_narrow_4px(self):
        # Latin extensions (é): east_asian_width Ambiguous → 4px, bold unchanged
        self.assertEqual(4.0, _char_advance('é', False))
        self.assertEqual(4.0, _char_advance('é', True))


class TestWrap(unittest.TestCase):
    def test_fits_single_line(self):
        # 'hello world' = 24 + 4 + 27 = 55px exactly
        self.assertEqual([[Text.text('hello world')]], wrap(55, 1, 'hello world'))

    def test_wraps_to_next_line(self):
        # width 54: 'hello'(24) + ' '(4) + 'world'(27) = 55 > 54 → wrap
        self.assertEqual([[Text.text('hello')], [Text.text('world')]], wrap(54, 1, 'hello world'))

    def test_paragraph_break_one_blank_line(self):
        result = wrap(100, 10, *Text.from_html('hello<p>world'))
        page = result[0]
        self.assertEqual(['hello', '', 'world'], [t.get('text', '') for t in page])

    def test_no_double_blank_when_last_word_fills_line(self):
        # When trailing space after last word overflows the line, cur_line is empty before <p>.
        # Should still produce exactly one blank line, not two.
        a_width = int(_str_advance('A', False))  # width that exactly fits 'A'; space overflows
        result = wrap(a_width, 10, *Text.from_html('A <p>B'))
        page = result[0]
        empty_lines = [t for t in page if not t.get('text', 'x')]
        self.assertEqual(1, len(empty_lines))

    def test_no_leading_space_after_paragraph_break(self):
        result = wrap(100, 10, *Text.from_html('hello<p>world'))
        page = result[0]
        last = [t for t in page if t.get('text') == 'world']
        self.assertFalse(last[0]['text'].startswith(' '))

    def test_explicit_newline(self):
        # \n\n is a hard line break; single \n is soft (treated as space)
        self.assertEqual([[Text.text('hello'), Text.text('world')]], wrap(100, 3, 'hello\n\nworld'))

    def test_soft_newline(self):
        # single \n in a string is a soft break — treated as a space
        self.assertEqual([[Text.text('hello world')]], wrap(100, 3, 'hello\nworld'))

    def test_page_overflow(self):
        result = wrap(100, 2, 'line1\n\nline2\n\nline3')
        self.assertEqual([[Text.text('line1'), Text.text('line2')], [Text.text('line3')]], result)

    def test_bold_html(self):
        self.assertEqual([[Text.text('hello').bold()]], wrap(100, 2, *Text.from_html('<b>hello</b>')))

    def test_italic_html(self):
        self.assertEqual([[Text.text('hi').italic()]], wrap(100, 2, *Text.from_html('<i>hi</i>')))

    def test_color_html(self):
        self.assertEqual([[Text.text('hello').color('red')]], wrap(100, 2, *Text.from_html('<font color="red">hello</font>')))

    def test_text_object_passthrough(self):
        t = Text.text('pass').bold()
        self.assertEqual([[t]], wrap(100, 2, t))

    def test_empty_items(self):
        self.assertEqual([], wrap(100, 2))

    def test_trailing_space_stripped(self):
        # leading/trailing spaces on a wrapped line are dropped
        pages = wrap(30, 2, 'hi there')
        for page in pages:
            for line in page:
                self.assertFalse(line['text'].startswith(' '))
                self.assertFalse(line['text'].endswith(' '))

    def test_nbsp_preserved_through_from_html(self):
        result = Text.from_html('hello&nbsp;world')
        self.assertIn('\xa0', result[0]['text'])

    def test_nbsp_not_split_in_wrap(self):
        # \xa0 must stay as part of the word token, not be split as whitespace
        result = wrap(200, 2, *Text.from_html('hello&nbsp;world'))
        self.assertEqual('hello\xa0world', result[0][0]['text'])

    def test_regular_spaces_still_collapse(self):
        result = Text.from_html('a   b')
        self.assertEqual('a b', result[0]['text'])

    def test_underlined_preserved(self):
        result = wrap(100, 2, *Text.from_html('<u>hello</u>'))
        self.assertTrue(result[0][0].get('underlined'))

    def test_strikethrough_preserved(self):
        result = wrap(100, 2, *Text.from_html('<s>hello</s>'))
        self.assertTrue(result[0][0].get('strikethrough'))

    def test_link_preserved(self):
        result = wrap(100, 2, *Text.from_html('<a href="https://example.com">click</a>'))
        line = result[0][0]
        self.assertTrue(line.get('underlined'))
        self.assertEqual({'action': 'open_url', 'url': 'https://example.com'}, line.get('click_event'))

    def test_link_underline_does_not_bleed_to_adjacent_text(self):
        # underline must cover only the link, not adjacent plain text on the same line
        result = wrap(200, 2, *Text.from_html('<a href="https://example.com">click</a> here'))
        line = result[0][0]
        # neutral root; formatting isolated in extra
        self.assertEqual('', line['text'])
        extra = line.get('extra', [])
        link = extra[0]
        plain = extra[1]
        self.assertTrue(link.get('underlined'))
        self.assertFalse(plain.get('underlined', False))

    def test_text_extra_field_included(self):
        # extra components on a Text object must not be silently dropped
        t = Text.text('A').bold().extra(Text.text('B').color('red'))
        result = wrap(100, 2, t)
        self.assertEqual(1, len(result))
        self.assertEqual(1, len(result[0]))
        line = result[0][0]
        # neutral root prevents formatting inheritance across spans
        self.assertEqual('', line['text'])
        extra = line.get('extra', [])
        self.assertEqual(2, len(extra))
        self.assertEqual('A', extra[0]['text'])
        self.assertTrue(extra[0].get('bold'))
        self.assertEqual('B', extra[1]['text'])
        self.assertEqual('red', extra[1]['color'])


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
