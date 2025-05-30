import shutil
import tempfile
import unittest

from pynecraft.base import CYAN, EAST, N, SOUTH, SW
from pynecraft.commands import *
from pynecraft.function import text_lines
from pynecraft.simpler import *
from pynecraft.simpler import _str_values
from pynecraft.values import BRICKS


class TestSimpler(unittest.TestCase):
    def setUp(self):
        self.tmp_path = Path(tempfile.mkdtemp())

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp_path)

    def test_sign_lines(self):
        self.assertEqual("""{messages: [one, two, three, four]}""",
                         str(Sign.lines_nbt(("one", "two", "three", "four"))))
        self.assertEqual("""{messages: ["", "", "", ""]}""", str(Sign.lines_nbt((None, ''))))
        self.assertEqual(Nbt({'messages': ['', 'foo', 'bar baz', '']}), Sign.lines_nbt((None, 'foo', 'bar baz')))

        self.assertEqual([
            """setblock 1 ~2 ^3 oak_sign[rotation=2]{front_text: {messages: ["", hi, there, ""]}}""" + '\n'],
            text_lines(Sign((None, 'hi', 'there'), front=True).place((1, r(2), d(3)), SW)))
        self.assertEqual([
            """setblock 1 ~2 ^3 oak_sign[rotation=2]{front_text: {messages: ["", hi, there, ""]}, is_waxed: true}""" + '\n'],
            text_lines(Sign((None, 'hi', 'there'), front=True).place((1, r(2), d(3)), SW, nbt={'is_waxed': True})))
        self.assertEqual([
            """setblock 1 ~2 ^3 oak_sign[rotation=2]{back_text: {messages: ["", hi, there, ""]}, front_text: {messages: ["", hi, there, ""]}}""" + '\n'],
            text_lines(Sign((None, 'hi', 'there')).place((1, r(2), d(3)), SW)))
        self.assertEqual([
            """setblock 1 ~2 ^3 oak_sign[rotation=2, waterlogged=true]{back_text: {messages: ["", hi, there, ""]}, front_text: {messages: ["", hi, there, ""]}}""" + '\n'],
            text_lines(Sign((None, 'hi', 'there')).place((1, r(2), d(3)), SW, water=True))[1:])
        self.assertEqual([
            """setblock 1 ~2 ^3 oak_sign[rotation=8]{back_text: {messages: ["", hi, there, ""]}, front_text: {messages: ["", hi, there, ""]}}""" + '\n'],
            text_lines(Sign((None, 'hi', 'there')).place((1, r(2), d(3)), NORTH)))
        self.assertEqual([
            """setblock 1 ~2 ^3 spruce_sign[rotation=8]{back_text: {messages: ["", hi, there, ""]}, front_text: {messages: ["", hi, there, ""]}}""" + '\n'],
            text_lines(Sign((None, 'hi', 'there'), wood='spruce').place((1, r(2), d(3)), N)))

        self.assertEqual(
            {'messages': [{'text': '', 'click_event': {'action': 'run_command', 'command': '/say hi'}}, '', '', '']},
            Sign.lines_nbt((), (say('hi'))))
        self.assertEqual({'messages': [
            {'text': 'hi', 'click_event': {'action': 'run_command', 'command': '/say boo'}}, 'there',
            {'text': '', 'click_event': {'action': 'run_command', 'command': '/tell @a hoo'}}, '']},
            Sign.lines_nbt(('hi', 'there'), (say('boo'), None, tell(a(), 'hoo'))))
        self.assertEqual({'messages': [
            {'text': '', 'click_event': {'action': 'run_command', 'command': '/say hi'}},
            {'text': '', 'click_event': {'action': 'run_command', 'command': '/say there'}}, '',
            '']},
            Sign.lines_nbt((), (say('hi'), lambda x: say('there'))))

        self.assertEqual(
            Nbt({'front_text': {'messages': ['hi', '', '', '']}, 'back_text': {'messages': ['there', '', '', '']},
                 'is_waxed': True}),
            Sign().front(('hi',)).back(('there',)).wax().nbt)

        with self.assertRaises(ValueError):
            Sign.lines_nbt((None, 'foo', 'bar', 'baz', 'bobble'))

    def test_sign_change(self):
        self.assertEqual(["""data modify block ~0 ~0 ~0 front_text.messages[1] set value hi""",
                          """data modify block ~0 ~0 ~0 back_text.messages[1] set value hi"""],
                         Sign.change(r(0, 0, 0), (None, 'hi')))
        self.assertEqual([
            """data modify block ~0 ~0 ~0 front_text.messages[0] set value two""",
            """data modify block ~0 ~0 ~0 front_text.messages[1] set value things"""
        ],
            Sign.change(r(0, 0, 0), ('two', 'things'), front=True))
        self.assertEqual([
            """data modify block ~0 ~0 ~0 front_text.messages[0] set value {click_event: {action: run_command, command: "/say two"}, text: ""}""",
            """data modify block ~0 ~0 ~0 front_text.messages[1] set value {click_event: {action: run_command, command: "/say things"}, text: ""}"""
        ],
            Sign.change(r(0, 0, 0), (), (say('two'), say('things')), front=True))
        self.assertEqual([
            """data modify block ~0 ~0 ~0 front_text.messages[0] set value {click_event: {action: run_command, command: "/say two"}, text: two}""",
            """data modify block ~0 ~0 ~0 front_text.messages[1] set value {click_event: {action: run_command, command: "/say things"}, text: three}"""
        ],
            Sign.change(r(0, 0, 0), ('two', 'three'), (say('two'), say('things')), front=True))

        self.assertEqual(["""data modify block ~0 ~0 ~0 front_text.messages[1] set value hi"""],
                         Sign.change(r(0, 0, 0), (None, 'hi'), front=True))
        self.assertEqual(["""data modify block ~0 ~0 ~0 back_text.messages[1] set value hi"""],
                         Sign.change(r(0, 0, 0), (None, 'hi'), front=False))
        self.assertEqual([
            """data modify block ~0 ~0 ~0 front_text.messages[1] set value hi""",
            """data modify block ~0 ~0 ~0 back_text.messages[1] set value hi"""],
            Sign.change(r(0, 0, 0), (None, 'hi'), front=None))

        self.assertEqual([
            """data merge block ~0 ~0 ~0 {front_text: {messages: [one, two, three, four]}}"""],
            Sign.change(r(0, 0, 0), ("one", "two", "three", "four"), front=True))
        self.assertEqual([
            """data merge block ~0 ~0 ~0 {back_text: {messages: [one, two, three, four]}}"""],
            Sign.change(r(0, 0, 0), ("one", "two", "three", "four"), front=False))
        self.assertEqual([
            """data merge block ~0 ~0 ~0 {back_text: {messages: [one, two, three, four]}, front_text: {messages: [one, two, three, four]}}"""],
            Sign.change(r(0, 0, 0), ("one", "two", "three", "four"), front=None))
        self.assertEqual([
            """data modify block 0 0 0 front_text.messages[2] set value three""",
            """data modify block 0 0 0 front_text.messages[3] set value four""",
            """data modify block 0 0 0 back_text.messages[2] set value three""",
            """data modify block 0 0 0 back_text.messages[3] set value four"""],
            Sign.change((0, 0, 0), ("three", "four"), start=2))
        self.assertEqual([
            '''data modify block 0 0 0 front_text.messages[2] set value three''',
            '''data modify block 0 0 0 front_text.messages[3] set value ""''',
            '''data modify block 0 0 0 back_text.messages[2] set value three''',
            '''data modify block 0 0 0 back_text.messages[3] set value ""'''],
            Sign.change((0, 0, 0), ("three",), start=2, min_len=2))
        self.assertEqual([
            '''data modify block 0 0 0 front_text.messages[2] set value one''',
            '''data modify block 0 0 0 back_text.messages[2] set value one'''],
            Sign.change((0, 0, 0), ('one',), start=2, blanks=True))
        self.assertEqual([
            '''data modify block 0 0 0 front_text.messages[2] set value one''',
            '''data modify block 0 0 0 front_text.messages[3] set value two''',
            '''data modify block 0 0 0 back_text.messages[2] set value one''',
            '''data modify block 0 0 0 back_text.messages[3] set value two'''],
            Sign.change((0, 0, 0), ('one', 'two'), start=2, blanks=True))

    def test_sign(self):
        self.assertEqual(
            {'front_text': {'messages': ['', 'hi', '', '']}, 'back_text': {'messages': ['', 'hi', '', '']}},
            Sign((None, 'hi')).nbt)
        self.assertEqual({'front_text': {'messages': ['', 'hi', '', '']}, 'back_text': {'messages': ['', 'hi', '', '']},
                          'is_waxed': True}, Sign((None, 'hi'), nbt={'is_waxed': True}).nbt)
        self.assertEqual({'back_text': {'messages': ['', '', 'Both Sides', '']},
                          'front_text': {'messages': ['', '', 'Both Sides', '']}},
                         Sign().messages((None, None, 'Both Sides')).nbt)
        self.assertEqual({'back_text': {'messages': ['', '', 'Both Sides', '']},
                          'front_text': {'messages': ['', '', 'Both Sides', '']}},
                         Sign().messages((None, None, 'Both Sides'), front=None).nbt)
        self.assertEqual({'front_text': {'messages': ['', '', 'Both Sides', '']}},
                         Sign().messages((None, None, 'Both Sides'), front=True).nbt)
        self.assertEqual({'back_text': {'messages': ['', '', 'Both Sides', '']}},
                         Sign().messages((None, None, 'Both Sides'), front=False).nbt)
        self.assertEqual({'front_text': {'messages': ['', '', 'Both Sides', '']}},
                         Sign().front((None, None, 'Both Sides')).nbt)
        self.assertEqual({'back_text': {'messages': ['', '', 'Both Sides', '']}},
                         Sign().back((None, None, 'Both Sides')).nbt)

        self.assertEqual({'front_text': {'color': 'blue'}, 'back_text': {'color': 'blue'}}, Sign(()).color(BLUE).nbt)
        self.assertEqual({'front_text': {'color': 'blue'}}, Sign(()).color(BLUE, front=True).nbt)
        self.assertEqual({'back_text': {'color': 'blue'}}, Sign(()).color(BLUE, front=False).nbt)
        self.assertEqual({}, Sign(()).color(None).nbt)
        self.assertEqual({'front_text': {'has_glowing_text': True}, 'back_text': {'has_glowing_text': True}},
                         Sign().glowing(True).nbt)
        self.assertEqual({}, Sign(()).glowing(False).nbt)
        self.assertEqual(
            {'front_text': {'messages': ['hi', '', '', ''], 'color': 'blue'},
             'back_text': {'messages': ['hi', '', '', ''], 'color': 'blue'}},
            Sign(('hi',)).color(BLUE, front=True).nbt)
        self.assertEqual(
            {'front_text': {'messages': ['hi', '', '', '']},
             'back_text': {'messages': ['hi', '', '', '']}},
            Sign(('hi',)).color(BLUE, front=True).color(None, front=True).nbt)
        self.assertEqual(
            {'front_text': {'messages': ['hi', '', '', ''],
                            'has_glowing_text': True},
             'back_text': {'messages': ['hi', '', '', ''],
                           'has_glowing_text': True}},
            Sign(('hi',)).glowing(True, front=True).nbt)
        self.assertEqual(
            {'front_text': {'messages': ['hi', '', '', '']},
             'back_text': {'messages': ['hi', '', '', '']}},
            Sign(('hi',)).glowing(True, front=True).glowing(False, front=True).nbt)

    def test_wall_sign(self):
        self.assertEqual([
            """setblock 1 ~2 ^3 oak_wall_sign[facing=north]{back_text: {messages: ["", hi, there, ""]}, front_text: {messages: ["", hi, there, ""]}}""" + '\n'],
            text_lines(WallSign((None, 'hi', 'there')).place((1, r(2), d(3)), NORTH)))
        self.assertEqual([
            'setblock 1 ~2 ^3 water\n',
            """setblock 1 ~2 ^3 oak_wall_sign[facing=north, waterlogged=true]{front_text: {messages: ["", hi, there, ""]}}""" + '\n'],
            text_lines(WallSign((None, 'hi', 'there'), front=True).place((1, r(2), d(3)), NORTH, water=True)))

    def test_book(self):
        book = Book('My Title', 'Me', 'My Name')
        # self.assertEqual((
        #     'written_book{author: Me, display_name: {Lore: "My Name"}, pages: ["[]"], ' 'title: "My Title"}'),
        #     str(book.as_entity()))
        #
        # book.add(JsonText.text('hi\n').color(DARK_AQUA))
        # self.assertEqual((
        #     'written_book{author: Me, display_name: {Lore: "My Name"}, pages: ' '[\'[{"text": "hi\\n", "color": "dark_aqua"}]\'], title: "My Title"}'),
        #     str(book.as_entity()))
        #
        # book.add("plain")
        # self.assertEqual((
        #     'written_book{author: Me, display_name: {Lore: "My Name"}, pages: ' '[\'[{"text": "hi\\n", "color": "dark_aqua"}, {"text": "plain"}]\'], title: ' '"My Title"}'),
        #     str(book.as_entity()))

    def test_region(self):
        v = Region(r(1, 2, 3), d(4, 5, 6))
        self.assertEqual(['fill ~1 ~2 ~3 ^4 ^5 ^6 stone replace #logs'], lines(v.fill('stone', '#logs')))
        self.assertEqual(['fill ~1 ~2 ~3 ^4 ^5 ^6 stone replace #logs'], lines(v.replace('stone', '#logs')))
        self.assertEqual([
            'fill ~1 ~2 ~3 ^4 ^5 ^6 stone[wl=true] replace #logs[wl=true]'],
            lines(v.replace('stone', '#logs', {'wl': True})))
        self.assertEqual([
            'fill ~1 ~2 ~3 ^4 ^5 ^6 stone[wl=true] replace #logs[wl=true]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 stone[wl=false] replace #logs[wl=false]',
        ], lines(v.replace('stone', '#logs', ({'wl': True}, {'wl': False}))))
        self.assertEqual([
            'fill ~1 ~2 ~3 ^4 ^5 ^6 stone[up=down, wl=true] replace #logs[wl=true]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 stone[up=down, wl=false] replace #logs[wl=false]',
        ], lines(v.replace('stone', '#logs', ({'wl': True}, {'wl': False}), {'up': 'down'})))
        self.assertEqual([
            'fill ~1 ~2 ~3 ^4 ^5 ^6 stone[type=double] replace #slabs[type=double]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 stone[type=top] replace #slabs[type=top]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 stone[type=bottom] replace #slabs[type=bottom]',
        ], lines(v.replace_slabs('stone')))
        self.assertEqual([
            'fill ~1 ~2 ~3 ^4 ^5 ^6 stone[wl=true, type=double] replace #slabs[type=double]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 stone[wl=true, type=top] replace #slabs[type=top]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 stone[wl=true, type=bottom] replace #slabs[type=bottom]',
        ], lines(v.replace_slabs('stone', new_state={'wl': 'true'})))
        self.assertEqual([
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak[half=top, facing=north, shape=straight] replace #stairs[half=top, facing=north, shape=straight]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak[half=top, facing=north, shape=inner_left] replace #stairs[half=top, facing=north, shape=inner_left]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak[half=top, facing=north, shape=inner_right] replace #stairs[half=top, facing=north, shape=inner_right]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak[half=top, facing=north, shape=outer_left] replace #stairs[half=top, facing=north, shape=outer_left]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak[half=top, facing=north, shape=outer_right] replace #stairs[half=top, facing=north, shape=outer_right]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak[half=top, facing=east, shape=straight] replace #stairs[half=top, facing=east, shape=straight]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak[half=top, facing=east, shape=inner_left] replace #stairs[half=top, facing=east, shape=inner_left]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak[half=top, facing=east, shape=inner_right] replace #stairs[half=top, facing=east, shape=inner_right]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak[half=top, facing=east, shape=outer_left] replace #stairs[half=top, facing=east, shape=outer_left]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak[half=top, facing=east, shape=outer_right] replace #stairs[half=top, facing=east, shape=outer_right]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak[half=top, facing=west, shape=straight] replace #stairs[half=top, facing=west, shape=straight]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak[half=top, facing=west, shape=inner_left] replace #stairs[half=top, facing=west, shape=inner_left]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak[half=top, facing=west, shape=inner_right] replace #stairs[half=top, facing=west, shape=inner_right]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak[half=top, facing=west, shape=outer_left] replace #stairs[half=top, facing=west, shape=outer_left]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak[half=top, facing=west, shape=outer_right] replace #stairs[half=top, facing=west, shape=outer_right]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak[half=top, facing=south, shape=straight] replace #stairs[half=top, facing=south, shape=straight]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak[half=top, facing=south, shape=inner_left] replace #stairs[half=top, facing=south, shape=inner_left]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak[half=top, facing=south, shape=inner_right] replace #stairs[half=top, facing=south, shape=inner_right]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak[half=top, facing=south, shape=outer_left] replace #stairs[half=top, facing=south, shape=outer_left]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak[half=top, facing=south, shape=outer_right] replace #stairs[half=top, facing=south, shape=outer_right]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak[half=bottom, facing=north, shape=straight] replace #stairs[half=bottom, facing=north, shape=straight]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak[half=bottom, facing=north, shape=inner_left] replace #stairs[half=bottom, facing=north, shape=inner_left]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak[half=bottom, facing=north, shape=inner_right] replace #stairs[half=bottom, facing=north, shape=inner_right]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak[half=bottom, facing=north, shape=outer_left] replace #stairs[half=bottom, facing=north, shape=outer_left]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak[half=bottom, facing=north, shape=outer_right] replace #stairs[half=bottom, facing=north, shape=outer_right]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak[half=bottom, facing=east, shape=straight] replace #stairs[half=bottom, facing=east, shape=straight]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak[half=bottom, facing=east, shape=inner_left] replace #stairs[half=bottom, facing=east, shape=inner_left]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak[half=bottom, facing=east, shape=inner_right] replace #stairs[half=bottom, facing=east, shape=inner_right]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak[half=bottom, facing=east, shape=outer_left] replace #stairs[half=bottom, facing=east, shape=outer_left]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak[half=bottom, facing=east, shape=outer_right] replace #stairs[half=bottom, facing=east, shape=outer_right]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak[half=bottom, facing=west, shape=straight] replace #stairs[half=bottom, facing=west, shape=straight]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak[half=bottom, facing=west, shape=inner_left] replace #stairs[half=bottom, facing=west, shape=inner_left]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak[half=bottom, facing=west, shape=inner_right] replace #stairs[half=bottom, facing=west, shape=inner_right]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak[half=bottom, facing=west, shape=outer_left] replace #stairs[half=bottom, facing=west, shape=outer_left]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak[half=bottom, facing=west, shape=outer_right] replace #stairs[half=bottom, facing=west, shape=outer_right]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak[half=bottom, facing=south, shape=straight] replace #stairs[half=bottom, facing=south, shape=straight]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak[half=bottom, facing=south, shape=inner_left] replace #stairs[half=bottom, facing=south, shape=inner_left]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak[half=bottom, facing=south, shape=inner_right] replace #stairs[half=bottom, facing=south, shape=inner_right]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak[half=bottom, facing=south, shape=outer_left] replace #stairs[half=bottom, facing=south, shape=outer_left]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak[half=bottom, facing=south, shape=outer_right] replace #stairs[half=bottom, facing=south, shape=outer_right]',
        ], lines(v.replace_stairs('oak')))
        self.assertEqual([
            'fill ~1 ~2 ~3 ^4 ^5 ^6 stone[facing=north, face=ceiling] replace #buttons[facing=north, face=ceiling]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 stone[facing=north, face=floor] replace #buttons[facing=north, face=floor]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 stone[facing=north, face=wall] replace #buttons[facing=north, face=wall]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 stone[facing=east, face=ceiling] replace #buttons[facing=east, face=ceiling]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 stone[facing=east, face=floor] replace #buttons[facing=east, face=floor]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 stone[facing=east, face=wall] replace #buttons[facing=east, face=wall]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 stone[facing=west, face=ceiling] replace #buttons[facing=west, face=ceiling]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 stone[facing=west, face=floor] replace #buttons[facing=west, face=floor]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 stone[facing=west, face=wall] replace #buttons[facing=west, face=wall]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 stone[facing=south, face=ceiling] replace #buttons[facing=south, face=ceiling]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 stone[facing=south, face=floor] replace #buttons[facing=south, face=floor]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 stone[facing=south, face=wall] replace #buttons[facing=south, face=wall]'],
            lines(v.replace_buttons('stone')))
        with self.assertRaises(NotImplementedError):
            self.assertEqual([
                'fill ~1 ~2 ~3 ^4 ^5 ^6 oak_door[half=lower, facing=east, open=false, hinge=left] replace #doors[half=lower, facing=east, open=false, hinge=left]',
                'fill ~1 ~2 ~3 ^4 ^5 ^6 oak_door[half=lower, facing=east, open=false, hinge=right] replace #doors[half=lower, facing=east, open=false, hinge=right]',
                'fill ~1 ~2 ~3 ^4 ^5 ^6 oak_door[half=lower, facing=east, open=true, hinge=left] replace #doors[half=lower, facing=east, open=true, hinge=left]',
                'fill ~1 ~2 ~3 ^4 ^5 ^6 oak_door[half=lower, facing=east, open=true, hinge=right] replace #doors[half=lower, facing=east, open=true, hinge=right]',
                'fill ~1 ~2 ~3 ^4 ^5 ^6 oak_door[half=lower, facing=north, open=false, hinge=left] replace #doors[half=lower, facing=north, open=false, hinge=left]',
                'fill ~1 ~2 ~3 ^4 ^5 ^6 oak_door[half=lower, facing=north, open=false, hinge=right] replace #doors[half=lower, facing=north, open=false, hinge=right]',
                'fill ~1 ~2 ~3 ^4 ^5 ^6 oak_door[half=lower, facing=north, open=true, hinge=left] replace #doors[half=lower, facing=north, open=true, hinge=left]',
                'fill ~1 ~2 ~3 ^4 ^5 ^6 oak_door[half=lower, facing=north, open=true, hinge=right] replace #doors[half=lower, facing=north, open=true, hinge=right]',
                'fill ~1 ~2 ~3 ^4 ^5 ^6 oak_door[half=lower, facing=south, open=false, hinge=left] replace #doors[half=lower, facing=south, open=false, hinge=left]',
                'fill ~1 ~2 ~3 ^4 ^5 ^6 oak_door[half=lower, facing=south, open=false, hinge=right] replace #doors[half=lower, facing=south, open=false, hinge=right]',
                'fill ~1 ~2 ~3 ^4 ^5 ^6 oak_door[half=lower, facing=south, open=true, hinge=left] replace #doors[half=lower, facing=south, open=true, hinge=left]',
                'fill ~1 ~2 ~3 ^4 ^5 ^6 oak_door[half=lower, facing=south, open=true, hinge=right] replace #doors[half=lower, facing=south, open=true, hinge=right]',
                'fill ~1 ~2 ~3 ^4 ^5 ^6 oak_door[half=lower, facing=west, open=false, hinge=left] replace #doors[half=lower, facing=west, open=false, hinge=left]',
                'fill ~1 ~2 ~3 ^4 ^5 ^6 oak_door[half=lower, facing=west, open=false, hinge=right] replace #doors[half=lower, facing=west, open=false, hinge=right]',
                'fill ~1 ~2 ~3 ^4 ^5 ^6 oak_door[half=lower, facing=west, open=true, hinge=left] replace #doors[half=lower, facing=west, open=true, hinge=left]',
                'fill ~1 ~2 ~3 ^4 ^5 ^6 oak_door[half=lower, facing=west, open=true, hinge=right] replace #doors[half=lower, facing=west, open=true, hinge=right]',
                'fill ~1 ~2 ~3 ^4 ^5 ^6 oak_door[half=upper, facing=east, open=false, hinge=left] replace #doors[half=upper, facing=east, open=false, hinge=left]',
                'fill ~1 ~2 ~3 ^4 ^5 ^6 oak_door[half=upper, facing=east, open=false, hinge=right] replace #doors[half=upper, facing=east, open=false, hinge=right]',
                'fill ~1 ~2 ~3 ^4 ^5 ^6 oak_door[half=upper, facing=east, open=true, hinge=left] replace #doors[half=upper, facing=east, open=true, hinge=left]',
                'fill ~1 ~2 ~3 ^4 ^5 ^6 oak_door[half=upper, facing=east, open=true, hinge=right] replace #doors[half=upper, facing=east, open=true, hinge=right]',
                'fill ~1 ~2 ~3 ^4 ^5 ^6 oak_door[half=upper, facing=north, open=false, hinge=left] replace #doors[half=upper, facing=north, open=false, hinge=left]',
                'fill ~1 ~2 ~3 ^4 ^5 ^6 oak_door[half=upper, facing=north, open=false, hinge=right] replace #doors[half=upper, facing=north, open=false, hinge=right]',
                'fill ~1 ~2 ~3 ^4 ^5 ^6 oak_door[half=upper, facing=north, open=true, hinge=left] replace #doors[half=upper, facing=north, open=true, hinge=left]',
                'fill ~1 ~2 ~3 ^4 ^5 ^6 oak_door[half=upper, facing=north, open=true, hinge=right] replace #doors[half=upper, facing=north, open=true, hinge=right]',
                'fill ~1 ~2 ~3 ^4 ^5 ^6 oak_door[half=upper, facing=south, open=false, hinge=left] replace #doors[half=upper, facing=south, open=false, hinge=left]',
                'fill ~1 ~2 ~3 ^4 ^5 ^6 oak_door[half=upper, facing=south, open=false, hinge=right] replace #doors[half=upper, facing=south, open=false, hinge=right]',
                'fill ~1 ~2 ~3 ^4 ^5 ^6 oak_door[half=upper, facing=south, open=true, hinge=left] replace #doors[half=upper, facing=south, open=true, hinge=left]',
                'fill ~1 ~2 ~3 ^4 ^5 ^6 oak_door[half=upper, facing=south, open=true, hinge=right] replace #doors[half=upper, facing=south, open=true, hinge=right]',
                'fill ~1 ~2 ~3 ^4 ^5 ^6 oak_door[half=upper, facing=west, open=false, hinge=left] replace #doors[half=upper, facing=west, open=false, hinge=left]',
                'fill ~1 ~2 ~3 ^4 ^5 ^6 oak_door[half=upper, facing=west, open=false, hinge=right] replace #doors[half=upper, facing=west, open=false, hinge=right]',
                'fill ~1 ~2 ~3 ^4 ^5 ^6 oak_door[half=upper, facing=west, open=true, hinge=left] replace #doors[half=upper, facing=west, open=true, hinge=left]',
                'fill ~1 ~2 ~3 ^4 ^5 ^6 oak_door[half=upper, facing=west, open=true, hinge=right] replace #doors[half=upper, facing=west, open=true, hinge=right]',
            ], sorted(lines(v.replace_doors('oak_door'))))
        self.assertEqual([
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak_trapdoor[half=top, facing=north, open=true] replace #trapdoors[half=top, facing=north, open=true]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak_trapdoor[half=top, facing=north, open=false] replace #trapdoors[half=top, facing=north, open=false]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak_trapdoor[half=top, facing=east, open=true] replace #trapdoors[half=top, facing=east, open=true]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak_trapdoor[half=top, facing=east, open=false] replace #trapdoors[half=top, facing=east, open=false]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak_trapdoor[half=top, facing=west, open=true] replace #trapdoors[half=top, facing=west, open=true]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak_trapdoor[half=top, facing=west, open=false] replace #trapdoors[half=top, facing=west, open=false]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak_trapdoor[half=top, facing=south, open=true] replace #trapdoors[half=top, facing=south, open=true]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak_trapdoor[half=top, facing=south, open=false] replace #trapdoors[half=top, facing=south, open=false]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak_trapdoor[half=bottom, facing=north, open=true] replace #trapdoors[half=bottom, facing=north, open=true]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak_trapdoor[half=bottom, facing=north, open=false] replace #trapdoors[half=bottom, facing=north, open=false]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak_trapdoor[half=bottom, facing=east, open=true] replace #trapdoors[half=bottom, facing=east, open=true]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak_trapdoor[half=bottom, facing=east, open=false] replace #trapdoors[half=bottom, facing=east, open=false]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak_trapdoor[half=bottom, facing=west, open=true] replace #trapdoors[half=bottom, facing=west, open=true]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak_trapdoor[half=bottom, facing=west, open=false] replace #trapdoors[half=bottom, facing=west, open=false]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak_trapdoor[half=bottom, facing=south, open=true] replace #trapdoors[half=bottom, facing=south, open=true]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak_trapdoor[half=bottom, facing=south, open=false] replace #trapdoors[half=bottom, facing=south, open=false]'
        ], lines(v.replace_trapdoors('oak_trapdoor')))
        self.assertEqual([
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak_fence_gate[facing=north] replace #fence_gates[facing=north]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak_fence_gate[facing=east] replace #fence_gates[facing=east]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak_fence_gate[facing=west] replace #fence_gates[facing=west]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak_fence_gate[facing=south] replace #fence_gates[facing=south]',
        ], lines(v.replace_facing('oak_fence_gate', '#fence_gates')))
        self.assertEqual([
            'fill ~1 ~2 ~3 ^4 ^5 ^6 furnace[facing=north] replace observer[facing=north]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 furnace[facing=east] replace observer[facing=east]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 furnace[facing=west] replace observer[facing=west]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 furnace[facing=south] replace observer[facing=south]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 furnace[facing=up] replace observer[facing=up]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 furnace[facing=down] replace observer[facing=down]',
        ], lines(v.replace_facing_all('furnace', 'observer')))
        self.assertEqual(list(
            f'fill ~1 ~2 ~3 ^4 ^5 ^6 oak_sign[rotation={i}] replace #signs[rotation={i}]' for i in range(16)
        ), lines(v.replace_rotation('oak_sign', '#signs')))

        self.assertEqual(['fillbiome ~1 ~2 ~3 ^4 ^5 ^6 plains replace poi'], lines(v.fillbiome(PLAINS, 'poi')))

    def test_offset(self):
        self.assertEqual(r(1, 2, 3), Offset(1, 2, 3).r(0, 0, 0))
        self.assertEqual(d(1, 2, 3), Offset(1, 2, 3).d(0, 0, 0))
        self.assertEqual(r(1, 2, 3), Offset(1, 2, 3).r(*r(0, 0, 0)))
        self.assertEqual(d(1, 2, 3), Offset(1, 2, 3).d(*d(0, 0, 0)))
        self.assertEqual(r(0), Offset(7).r(-7))
        with self.assertRaises(ValueError):
            Offset(1, 2, 3).r(5)
        with self.assertRaises(ValueError):
            Offset(1, 2, 3).r(d(1), 2, 3)

    def test_item_frame(self):
        self.assertEqual('item_frame', ItemFrame(EAST).id)
        self.assertEqual('glow_item_frame', ItemFrame(EAST, glowing=True).id)
        self.assertEqual('Item Frame', ItemFrame(EAST).name)
        self.assertEqual('Fred', ItemFrame(EAST, name='Fred').name)
        self.assertEqual({'Facing': 5, 'Fixed': True}, ItemFrame(EAST).nbt)
        self.assertEqual({'Facing': 5}, ItemFrame(EAST).fixed(False).nbt)
        self.assertEqual(
            {'Facing': 5, 'Fixed': True,
             'Item': {'id': 'minecraft:my_name', 'components': {'custom_name': {'text': 'My Name'}}}},
            ItemFrame(EAST).named('My Name').nbt)
        self.assertEqual({'Facing': 5, 'Fixed': True, 'foo': 12}, ItemFrame(EAST, nbt={'foo': 12}).nbt)
        self.assertEqual({'Facing': 5, 'Fixed': True, 'Item': {'id': 'minecraft:obsidian'}},
                         ItemFrame(EAST).item('obsidian').nbt)

    def test_villager(self):
        self.assertEqual(Nbt({'VillagerData': {'profession': 'mason', 'type': 'jungle', 'xp': 0, 'level': 0}}),
                         Villager(MASON, JUNGLE).nbt)
        self.assertEqual(
            Nbt({'Age': -2147483648, 'VillagerData': {'profession': 'none', 'type': 'plains', 'xp': 0, 'level': 0}}),
            Villager(CHILD, 'plains').nbt)
        self.assertEqual(Nbt({
            'Offers': {'Recipes': [
                {'buy': {'id': 'stone'}, 'rewardExp': True, 'sell': {'id': 'melon'}},
            ]},
            'VillagerData': {'profession': 'mason', 'type': 'jungle', 'xp': 0, 'level': 0}}),
            Villager(MASON, JUNGLE).add_trade(Trade('stone', 'melon')).nbt)
        self.assertEqual(Nbt({
            'Offers': {'Recipes': [{'buy': {'id': 'stone'}, 'buyB': {'id': 'melon'},
                                    'rewardExp': True, 'sell': {'id': 'torch'}}]},
            'VillagerData': {'profession': 'mason', 'type': 'jungle', 'xp': 0, 'level': 0}}),
            Villager(MASON, JUNGLE).add_trade(Trade('stone', 'melon', 'torch')).nbt)
        self.assertEqual(Nbt(
            {'Offers': {'Recipes': [{'buy': {'id': 'stone'},
                                     'rewardExp': True, 'sell': {'id': 'iron_axe', 'Count': {'damage': 12}}}]},
             'VillagerData': {'profession': 'mason', 'type': 'jungle', 'xp': 0, 'level': 0}}),
            Villager(MASON, JUNGLE).add_trade(Trade('stone', ('iron_axe', {'damage': 12}))).nbt)
        self.assertEqual(Nbt({
            'Offers': {'Recipes': [
                {'buy': {'id': 'stone'}, 'rewardExp': True, 'sell': {'id': 'melon'}},
                {'buy': {'id': 'stone'}, 'rewardExp': True, 'sell': {'id': 'melon'}},
            ]},
            'VillagerData': {'profession': 'mason', 'type': 'jungle', 'xp': 0, 'level': 0}}),
            Villager(MASON, JUNGLE).add_trade(Trade('stone', 'melon'), Trade('stone', 'melon').nbt()).nbt)
        self.assertEqual(Nbt({
            'Inventory': [{'id': 'minecraft:iron_hoe'},
                          {'id': 'minecraft:wheat', 'Count': 25}],
            'VillagerData': {'profession': 'mason', 'type': 'jungle', 'xp': 0, 'level': 0}}),
            Villager(MASON, JUNGLE).inventory('iron_hoe', ('wheat', 25)).nbt)

        v = Villager(BUTCHER, SWAMP).xp(175)
        self.assertEqual({'VillagerData': {'profession': 'butcher', 'type': 'swamp', 'xp': 175, 'level': 3}}, v.nbt)
        self.assertEqual(3, v.level)
        self.assertEqual('Expert', v.level_name)

        with self.assertRaises(ValueError):
            Villager(CHILD, JUNGLE, zombie=True)

    def test_display(self):
        self.assertEqual(
            {'text': {'text': 'foo'},
             'transformation': {'left_rotation': [0, 0, 0, 1], 'right_rotation': [0, 0, 0, 1],
                                'scale': [1, 1, 1], 'translation': [0, 0, 0]}},
            TextDisplay('foo').nbt)
        self.assertEqual(
            {'text': {'text': 'foo'},
             'transformation': {'left_rotation': [0.0, 0.0, 0.0, 1.0], 'right_rotation': [0.0, 0.0, 0.0, 1.0],
                                'scale': [0.5, 0.5, 0.5], 'translation': [0.0, 0.0, 0.0]}},
            TextDisplay('foo').scale(0.5).nbt)
        self.assertEqual(
            {'text': {'text': 'foo'},
             'transformation': {'left_rotation': [0.0, 0.0, 0.0, 1.0], 'right_rotation': [0.0, 0.0, 0.0, 1.0],
                                'scale': [1.0, 2.0, 3.0], 'translation': [0.0, 0.0, 0.0]}},
            TextDisplay('foo').scale((1, 2, 3)).nbt)
        self.assertEqual(
            {'text': {'text': 'foo'},
             'transformation': {'left_rotation': [0.0, 0.0, 0.0, 1.0], 'right_rotation': [0.0, 0.0, 0.0, 1.0],
                                'scale': [1.0, 2.0, 3.0], 'translation': [0.0, 0.0, 0.0]}},
            TextDisplay('foo', nbt={'transformation': {'scale': [1.0, 2.0, 3.0]}}).nbt)

    def test_block_display(self):
        self.assertEqual({}, _str_values({}))
        self.assertEqual({'b': 'true', 'i': '12', 'f': '3.7f', 's': 'tr'},
                         _str_values({'b': True, 'i': 12, 'f': 3.7, 's': 'tr'}))
        self.assertEqual({'m1': {'b': 'true', 'i': '12', 'f': '3.7f', 's': 'tr'}},
                         _str_values({'m1': {'b': True, 'i': 12, 'f': 3.7, 's': 'tr'}}))
        self.assertEqual({'m1': ['true', '12', '3.7f', 'tr']}, _str_values({'m1': [True, 12, 3.7, 'tr']}))

    def test_text_display(self):
        self.assertEqual(
            """summon text_display ~0 ~0 ~0 {Facing: 2, Rotation: [180.0f, 0.0f], text: {text: foo}, transformation: {left_rotation: [0, 0, 0, 1], right_rotation: [0, 0, 0, 1], scale: [1, 1, 1], translation: [0, 0, 0]}}""",
            str(TextDisplay('foo').summon(r(0, 0, 0), facing=NORTH)))
        self.assertEqual(
            """summon text_display ~0 ~0 ~0 {Facing: 2, Rotation: [180.0f, 0.0f], text: {text: bar}, transformation: {left_rotation: [0, 0, 0, 1], right_rotation: [0, 0, 0, 1], scale: [1, 1, 1], translation: [0, 0, 0]}}""",
            str(TextDisplay('foo').text('bar').summon(r(0, 0, 0), facing=NORTH)))
        self.assertEqual({'text': [{"text": "foo", "italic": "true"}],
                          'transformation': {'left_rotation': [0.0, 0.0, 0.0, 1.0],
                                             'right_rotation': [0.0, 0.0, 0.0, 1.0],
                                             'scale': [1.0, 1.0, 1.0], 'translation': [0.0, 0.0, 0.0]}},
                         TextDisplay(Text.html_text('<i>foo</i>')).nbt)
        self.assertEqual(
            'text_display{text: $(f), transformation: {left_rotation: [0, 0, 0, 1], right_rotation: [0, 0, 0, 1], scale: [1, 1, 1], translation: [0, 0, 0]}}',
            str(TextDisplay(Arg('f'))))

    def test_item(self):
        self.assertEqual('dirt', Item('dirt').id)
        self.assertEqual({'id': 'minecraft:dirt'}, Item.nbt_for('dirt'))
        self.assertEqual({'id': 'minecraft:dirt', 'Count': 2}, Item.nbt_for('dirt', {'Count': 2}))
        self.assertEqual({'id': 'minecraft:dirt', 'foo': 17}, Item.nbt_for('dirt', nbt={'foo': 17}))
        self.assertEqual({'id': 'minecraft:filled_map'}, Item.nbt_for('filled_map'))

    def test_shield(self):
        shield = Shield()
        self.assertEqual({}, shield.nbt)
        shield.color(WHITE)
        self.assertEqual({'components': {'base_color': 'white'}}, shield.nbt)
        shield.add_pattern('stripe_top', CYAN)
        self.assertEqual(
            {'components': {'base_color': 'white', 'banner_patterns': [{'pattern': 'stripe_top', 'color': 'cyan'}]}},
            shield.nbt)
        shield.add_pattern(BRICKS, PURPLE)
        self.assertEqual(
            {'components': {
                'base_color': 'white',
                'banner_patterns': [{'pattern': 'stripe_top', 'color': 'cyan'},
                                    {'pattern': 'bricks', 'color': 'purple'}]}},
            shield.nbt)
        shield.clear_patterns()
        self.assertEqual({'components': {'base_color': 'white'}}, shield.nbt)
        shield.color(None)
        self.assertEqual({'components': {}}, shield.nbt)

    def test_painting(self):
        self.assertEqual(
            'summon painting ~0 ~0 ~0 {facing: 0, variant: pointer}',
            Painting('pointer').summon(r(0, 0, 0), facing=SOUTH))
        self.assertEqual(
            'summon painting ~-1 ~1 ~0 {facing: 0, variant: pointer}',
            Painting('pointer').summon(r(0, 0, 0), facing=SOUTH, lower_left=True))
        self.assertEqual(
            'summon painting ~1 ~1 ~0 {facing: 8, variant: pointer}',
            Painting('pointer').summon(r(0, 0, 0), lower_left=True))
        self.assertEqual(
            'summon painting ~0 ~0 ~0 {facing: 0, foo: 12, variant: pointer}',
            Painting('pointer').summon(r(0, 0, 0), nbt={'foo': 12}, facing=SOUTH))
        with self.assertRaises(ValueError):
            Painting('foo')

    def test_as_color_num(self):
        self.assertIsNone(as_color_num(None))
        self.assertEqual(15, as_color_num(15))
        self.assertEqual(15, as_color_num('black'))
        self.assertEqual(15, as_color_num('Black'))
        with self.assertRaises(ValueError):
            as_color_num(16)
        with self.assertRaises(ValueError):
            as_color_num('ecru')

    def test_as_color(self):
        self.assertIsNone(as_color(None))
        self.assertEqual('black', as_color(15))
        self.assertEqual('black', as_color('black'))
        self.assertEqual('black', as_color('Black'))
        with self.assertRaises(ValueError):
            as_color(16)
        with self.assertRaises(ValueError):
            as_color('ecru')

    def test_macro(self):
        shield = Shield().add_pattern(Arg('pat'), Arg('c'))
        self.assertEqual(
            {'components': {'banner_patterns': [{'pattern': '$(pat)', 'color': '$(c)'}]}}, shield.nbt)
        self.assertEqual('$(c)', as_color(Arg('c')))
        self.assertEqual('$(c)', as_color_num(Arg('c')))
