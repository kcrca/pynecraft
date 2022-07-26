import shutil
import tempfile
import unittest

from pynecraft.base import DARK_AQUA, N, NORTH, ROTATION_180, SW, d, r
from pynecraft.commands import *
from pynecraft.function import text_lines
from pynecraft.simpler import *


class TestSimpler(unittest.TestCase):
    def setUp(self):
        self.tmp_path = Path(tempfile.mkdtemp())

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp_path)

    def test_sign(self):
        self.assertEqual(Sign.text("foo"), r'"\"foo\""')
        self.assertEqual(str(Sign.lines_nbt((None, ''))), '{Text2: \'""\'}')
        self.assertEqual(Sign.lines_nbt((None, 'foo', 'bar baz')), Nbt({'Text2': 'foo', 'Text3': 'bar baz'}))

        self.assertEqual(text_lines(Sign((None, 'hi', 'there')).place((1, r(2), d(3)), SW)), [
            'setblock 1 ~2 ^3 air\n', 'setblock 1 ~2 ^3 oak_sign[rotation=2]{Text2: \'"hi"\', Text3: \'"there"\'}\n'])
        self.assertEqual(text_lines(Sign((None, 'hi', 'there')).place((1, r(2), d(3)), SW, water=True))[1:], [
            'setblock 1 ~2 ^3 oak_sign[rotation=2, waterlogged=true]{Text2: \'"hi"\', Text3: \'"there"\'}\n'])
        self.assertEqual(text_lines(Sign((None, 'hi', 'there')).place((1, r(2), d(3)), NORTH))[1:], [
            'setblock 1 ~2 ^3 oak_sign[rotation=8]{Text2: \'"hi"\', Text3: \'"there"\'}\n'])
        self.assertEqual(text_lines(Sign((None, 'hi', 'there'), wood='spruce').place((1, r(2), d(3)), N))[1:], [
            'setblock 1 ~2 ^3 spruce_sign[rotation=8]{Text2: \'"hi"\', Text3: \'"there"\'}\n'])
        self.assertEqual(text_lines(Sign((None, 'hi', 'there')).place((1, r(2), d(3)), 8))[1:], [
            'setblock 1 ~2 ^3 oak_sign[rotation=8]{Text2: \'"hi"\', Text3: \'"there"\'}\n'])

    def test_wall_sign(self):
        self.assertEqual(text_lines(WallSign((None, 'hi', 'there')).place((1, r(2), d(3)), NORTH)), [
            'setblock 1 ~2 ^3 air\n',
            'setblock 1 ~2 ^3 oak_wall_sign[facing=north]{Text2: \'"hi"\', Text3: \'"there"\'}\n'])
        self.assertEqual(text_lines(WallSign((None, 'hi', 'there')).place((1, r(2), d(3)), NORTH, water=True))[1:], [
            'setblock 1 ~2 ^3 oak_wall_sign[facing=north, waterlogged=true]{Text2: \'"hi"\', Text3: \'"there"\'}\n'])
        self.assertEqual(text_lines(WallSign((None, 'hi', 'there')).place((1, r(2), d(3)), NORTH))[1:], [
            'setblock 1 ~2 ^3 oak_wall_sign[facing=north]{Text2: \'"hi"\', Text3: \'"there"\'}\n'])
        self.assertEqual(text_lines(WallSign((None, 'hi', 'there'), wood='spruce').place(
            (1, r(2), d(3)), NORTH))[1:],
                          ['setblock 1 ~2 ^3 spruce_wall_sign[facing=north]{Text2: \'"hi"\', Text3: \'"there"\'}\n'])
        self.assertEqual(text_lines(WallSign((None, 'hi', 'there')).place((1, r(2), d(3)), ROTATION_180))[1:], [
            'setblock 1 ~2 ^3 oak_wall_sign[facing=north]{Text2: \'"hi"\', Text3: \'"there"\'}\n'])
        self.assertEqual(text_lines(WallSign((None, 'hi', 'there'), (say('hi'),)).place((1, r(2), d(3)), NORTH))[1:], [
            'setblock 1 ~2 ^3 oak_wall_sign[facing=north]{Text1: \'{"clickEvent": ' '{"action": "run_command", "value": "/say hi"}, "text": ""}\', Text2: ' '\'"hi"\', Text3: \'"there"\'}\n'])
        self.assertEqual(text_lines(
            WallSign((None, 'hi', 'there'),
                     (data().merge(s(), {'Command': 'say hi'}),)).place((1, r(2), d(3)), NORTH))[1:], [
                              'setblock 1 ~2 ^3 oak_wall_sign[facing=north]{Text1: \'{"clickEvent": ' '{"action": "run_command", "value": "/data merge entity @s {Command: \\\\"say ' 'hi\\\\"}"}, "text": ""}\', Text2: \'"hi"\', Text3: \'"there"\'}\n'])

    def test_book(self):
        book = Book('My Title', 'Me', 'My Name')
        self.assertEqual(str(book.as_entity()), (
            'written_book{author: Me, display_name: {Lore: "My Name"}, pages: ["[]"], ' 'title: "My Title"}'))

        book.add(JsonText.text('hi\n').color(DARK_AQUA))
        self.assertEqual(str(book.as_entity()), (
            'written_book{author: Me, display_name: {Lore: "My Name"}, pages: ' '[\'[{"text": "hi\\n", "color": "dark_aqua"}]\'], title: "My Title"}'))

        book.add("plain")
        self.assertEqual(str(book.as_entity()), (
            'written_book{author: Me, display_name: {Lore: "My Name"}, pages: ' '[\'[{"text": "hi\\n", "color": "dark_aqua"}, {"text": "plain"}]\'], title: ' '"My Title"}'))

    def test_volume(self):
        v = Volume(r(1, 2, 3), d(4, 5, 6))
        self.assertEqual(lines(v.fill('stone', '#logs')), ['fill ~1 ~2 ~3 ^4 ^5 ^6 stone replace #logs'])
        self.assertEqual(lines(v.replace('stone', '#logs')), ['fill ~1 ~2 ~3 ^4 ^5 ^6 stone replace #logs'])
        self.assertEqual(lines(v.replace('stone', '#logs', {'wl': True})), [
            'fill ~1 ~2 ~3 ^4 ^5 ^6 stone[wl=true] replace #logs[wl=true]'])
        self.assertEqual(lines(v.replace('stone', '#logs', ({'wl': True}, {'wl': False}))), [
            'fill ~1 ~2 ~3 ^4 ^5 ^6 stone[wl=true] replace #logs[wl=true]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 stone[wl=false] replace #logs[wl=false]',
        ])
        self.assertEqual(lines(v.replace('stone', '#logs', ({'wl': True}, {'wl': False}), {'up': 'down'})), [
            'fill ~1 ~2 ~3 ^4 ^5 ^6 stone[up=down, wl=true] replace #logs[up=down, wl=true]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 stone[up=down, wl=false] replace #logs[up=down, wl=false]',
        ])
        self.assertEqual(lines(v.replace_slabs('stone')), [
            'fill ~1 ~2 ~3 ^4 ^5 ^6 stone[type=double] replace #slabs[type=double]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 stone[type=top] replace #slabs[type=top]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 stone[type=bottom] replace #slabs[type=bottom]',
        ])
        self.assertEqual(lines(v.replace_slabs('stone', added_state={'wl': 'true'})), [
            'fill ~1 ~2 ~3 ^4 ^5 ^6 stone[wl=true, type=double] replace #slabs[wl=true, type=double]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 stone[wl=true, type=top] replace #slabs[wl=true, type=top]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 stone[wl=true, type=bottom] replace #slabs[wl=true, type=bottom]',
        ])
        self.assertEqual(lines(v.replace_stairs('oak')), [
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
        ])
        self.assertEqual(sorted(lines(v.replace_doors('oak_door'))), [
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
        ])
        self.assertEqual(lines(v.replace_trapdoors('oak_trapdoor')), [
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
        ])
        self.assertEqual(lines(v.replace_facing('oak_fence_gate', '#fence_gates')), [
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak_fence_gate[facing=north] replace #fence_gates[facing=north]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak_fence_gate[facing=east] replace #fence_gates[facing=east]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak_fence_gate[facing=west] replace #fence_gates[facing=west]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 oak_fence_gate[facing=south] replace #fence_gates[facing=south]',
        ])
        self.assertEqual(lines(v.replace_facing_all('furnace', 'observer')), [
            'fill ~1 ~2 ~3 ^4 ^5 ^6 furnace[facing=north] replace observer[facing=north]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 furnace[facing=east] replace observer[facing=east]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 furnace[facing=west] replace observer[facing=west]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 furnace[facing=south] replace observer[facing=south]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 furnace[facing=up] replace observer[facing=up]',
            'fill ~1 ~2 ~3 ^4 ^5 ^6 furnace[facing=down] replace observer[facing=down]',
        ])
