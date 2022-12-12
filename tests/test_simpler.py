import shutil
import tempfile
import unittest

from pynecraft.base import DARK_AQUA, N, NORTH, ROTATION_180, SW
from pynecraft.commands import *
from pynecraft.enums import BiomeId
from pynecraft.function import text_lines
from pynecraft.simpler import *


class TestSimpler(unittest.TestCase):
    def setUp(self):
        self.tmp_path = Path(tempfile.mkdtemp())

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp_path)

    def test_sign(self):
        self.assertEqual(r'"\"foo\""', Sign.text("foo"))
        self.assertEqual('''{Text2: '""'}''', str(Sign.lines_nbt((None, ''))))
        self.assertEqual(Nbt({'Text2': 'foo', 'Text3': 'bar baz'}), Sign.lines_nbt((None, 'foo', 'bar baz')))

        self.assertEqual([
            'setblock 1 ~2 ^3 air\n', 'setblock 1 ~2 ^3 oak_sign[rotation=2]{Text2: \'"hi"\', Text3: \'"there"\'}\n'],
            text_lines(Sign((None, 'hi', 'there')).place((1, r(2), d(3)), SW)))
        self.assertEqual([
            'setblock 1 ~2 ^3 oak_sign[rotation=2, waterlogged=true]{Text2: \'"hi"\', Text3: \'"there"\'}\n'],
            text_lines(Sign((None, 'hi', 'there')).place((1, r(2), d(3)), SW, water=True))[1:])
        self.assertEqual([
            'setblock 1 ~2 ^3 oak_sign[rotation=8]{Text2: \'"hi"\', Text3: \'"there"\'}\n'],
            text_lines(Sign((None, 'hi', 'there')).place((1, r(2), d(3)), NORTH))[1:])
        self.assertEqual([
            'setblock 1 ~2 ^3 spruce_sign[rotation=8]{Text2: \'"hi"\', Text3: \'"there"\'}\n'],
            text_lines(Sign((None, 'hi', 'there'), wood='spruce').place((1, r(2), d(3)), N))[1:])
        self.assertEqual([
            'setblock 1 ~2 ^3 oak_sign[rotation=8]{Text2: \'"hi"\', Text3: \'"there"\'}\n'],
            text_lines(Sign((None, 'hi', 'there')).place((1, r(2), d(3)), 8))[1:])

    def test_wall_sign(self):
        self.assertEqual([
            'setblock 1 ~2 ^3 air\n',
            'setblock 1 ~2 ^3 oak_wall_sign[facing=north]{Text2: \'"hi"\', Text3: \'"there"\'}\n'],
            text_lines(WallSign((None, 'hi', 'there')).place((1, r(2), d(3)), NORTH)))
        self.assertEqual([
            'setblock 1 ~2 ^3 oak_wall_sign[facing=north, waterlogged=true]{Text2: \'"hi"\', Text3: \'"there"\'}\n'],
            text_lines(WallSign((None, 'hi', 'there')).place((1, r(2), d(3)), NORTH, water=True))[1:])
        self.assertEqual([
            'setblock 1 ~2 ^3 oak_wall_sign[facing=north]{Text2: \'"hi"\', Text3: \'"there"\'}\n'],
            text_lines(WallSign((None, 'hi', 'there')).place((1, r(2), d(3)), NORTH))[1:])
        self.assertEqual(['setblock 1 ~2 ^3 spruce_wall_sign[facing=north]{Text2: \'"hi"\', Text3: \'"there"\'}\n'],
                         text_lines(WallSign((None, 'hi', 'there'), wood='spruce').place(
                             (1, r(2), d(3)), NORTH))[1:])
        self.assertEqual([
            'setblock 1 ~2 ^3 oak_wall_sign[facing=north]{Text2: \'"hi"\', Text3: \'"there"\'}\n'],
            text_lines(WallSign((None, 'hi', 'there')).place((1, r(2), d(3)), ROTATION_180))[1:])
        self.assertEqual([
            'setblock 1 ~2 ^3 oak_wall_sign[facing=north]{Text1: \'{"clickEvent": ' '{"action": "run_command", "value": "/say hi"}, "text": ""}\', Text2: ' '\'"hi"\', Text3: \'"there"\'}\n'],
            text_lines(WallSign((None, 'hi', 'there'), (say('hi'),)).place((1, r(2), d(3)), NORTH))[1:])
        self.assertEqual([
            'setblock 1 ~2 ^3 oak_wall_sign[facing=north]{Text1: \'{"clickEvent": ' '{"action": "run_command", "value": "/data merge entity @s {Command: \\\\"say ' 'hi\\\\"}"}, "text": ""}\', Text2: \'"hi"\', Text3: \'"there"\'}\n'],
            text_lines(WallSign(
                (None, 'hi', 'there'), (data().merge(s(), {'Command': 'say hi'}),)).place((1, r(2), d(3)), NORTH))[1:])

    def test_book(self):
        book = Book('My Title', 'Me', 'My Name')
        self.assertEqual((
            'written_book{author: Me, display_name: {Lore: "My Name"}, pages: ["[]"], ' 'title: "My Title"}'),
            str(book.as_entity()))

        book.add(JsonText.text('hi\n').color(DARK_AQUA))
        self.assertEqual((
            'written_book{author: Me, display_name: {Lore: "My Name"}, pages: ' '[\'[{"text": "hi\\n", "color": "dark_aqua"}]\'], title: "My Title"}'),
            str(book.as_entity()))

        book.add("plain")
        self.assertEqual((
            'written_book{author: Me, display_name: {Lore: "My Name"}, pages: ' '[\'[{"text": "hi\\n", "color": "dark_aqua"}, {"text": "plain"}]\'], title: ' '"My Title"}'),
            str(book.as_entity()))

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

        orig_version = parameters.version
        try:
            parameters.version = Parameters.VERSION_1_19_3
            self.assertEqual(['fillbiome ~1 ~2 ~3 ^4 ^5 ^6 plains replace poi'],
                             lines(v.fillbiome(BiomeId.PLAINS, 'poi')))
        finally:
            parameters.version = orig_version

    def test_offset(self):
        self.assertEqual(r(1, 2, 3), Offset(1, 2, 3).r(0, 0, 0))
        self.assertEqual(d(1, 2, 3), Offset(1, 2, 3).d(0, 0, 0))
        self.assertEqual(r(1, 2, 3), Offset(1, 2, 3).r(*r(0, 0, 0)))
        self.assertEqual(d(1, 2, 3), Offset(1, 2, 3).d(*d(0, 0, 0)))
        with self.assertRaises(ValueError):
            Offset(1, 2, 3).r(5)
            Offset(1, 2, 3).r(d(1), 2, 3)

    def test_villager(self):
        self.assertEqual(Nbt({'VillagerData': {'profession': 'mason', 'type': 'jungle'}}),
                         Villager(MASON, JUNGLE).nbt)
        self.assertEqual(Nbt({'Age': -2147483648, 'VillagerData': {'profession': 'unemployed', 'type': 'plains'}}),
                         Villager(CHILD, 'plains').nbt)
        self.assertEqual(Nbt({
            'Offers': {'Recipes': [
                {'buy': {'Count': 1, 'id': 'stone'}, 'rewardExp': True, 'sell': {'Count': 1, 'id': 'melon'}},
            ]},
            'VillagerData': {'profession': 'mason', 'type': 'jungle'}}),
            Villager(MASON, JUNGLE).add_trade(Trade('stone', 'melon')).nbt)
        self.assertEqual(Nbt({
            'Offers': {'Recipes': [
                {'buy': {'Count': 1, 'id': 'stone'}, 'rewardExp': True, 'sell': {'Count': 1, 'id': 'melon'}},
                {'buy': {'Count': 1, 'id': 'stone'}, 'rewardExp': True, 'sell': {'Count': 1, 'id': 'melon'}},
            ]},
            'VillagerData': {'profession': 'mason', 'type': 'jungle'}}),
            Villager(MASON, JUNGLE).add_trade(Trade('stone', 'melon'), Trade('stone', 'melon').nbt()).nbt)
        self.assertEqual(Nbt({
            'Inventory': [{'id': 'minecraft:iron_hoe', 'Count': 1},
                          {'id': 'minecraft:wheat', 'Count': 25}],
            'VillagerData': {'profession': 'mason', 'type': 'jungle'}}),
            Villager(MASON, JUNGLE).inventory('iron_hoe', ('wheat', 25)).nbt)

        with self.assertRaises(ValueError):
            Villager(CHILD, JUNGLE, zombie=True)
