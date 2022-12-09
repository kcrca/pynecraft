import unittest

from parameterized import parameterized

from pynecraft.base import Coord, EAST, IntRelCoord, NORTH, Nbt, ROTATION_0, ROTATION_180, ROTATION_270, \
    ROTATION_90, RelCoord, SOUTH, \
    TimeSpec, WEST, \
    parameters, r, rotated_facing
from pynecraft.commands import setblock


def spaceify(s, use_spaces):
    return s.replace(',', ', ').replace(':', ': ') if use_spaces else s


class TestBase(unittest.TestCase):
    def setUp(self) -> None:
        self.orig_spaces = Nbt.use_spaces

    def tearDown(self) -> None:
        Nbt.use_spaces = self.orig_spaces

    def test_rotated_facing(self):
        self.assertEqual((0, 0, -3), rotated_facing(NORTH).scale(3))
        self.assertEqual(rotated_facing(NORTH), rotated_facing(NORTH, ROTATION_0))
        self.assertEqual(rotated_facing(NORTH), rotated_facing(EAST, ROTATION_270))
        self.assertEqual(rotated_facing(NORTH), rotated_facing(SOUTH, ROTATION_180))
        self.assertEqual(rotated_facing(NORTH), rotated_facing(WEST, ROTATION_90))

    def test_nbt(self):
        self.assertEqual({'key': 1}, Nbt().merge(Nbt(key=1)))
        self.assertEqual({'key': 1, 'key2': 2}, Nbt(key=1).merge(Nbt(key2=2)))
        self.assertEqual({'key': 2}, Nbt(key=1).merge(Nbt(key=2)))
        self.assertEqual({'key': 1, 'key2': 3}, Nbt(key=1, key2=2).merge(Nbt(key2=3)))
        self.assertEqual({'key': (2, 4, 6)}, Nbt(key=(1, 3, 5)).merge(Nbt(key=(2, 4, 6))))

    def test_nbt_regularize(self):
        self.assertEqual('{key: [1, 2]}', str(Nbt(key=[1, 2])))
        self.assertEqual('{key: [1.0f, 2.0f]}', str(Nbt(key=[1, 2.0])))
        self.assertEqual('{key: [1.0f, 2.0f]}', str(Nbt(key=[1.0, 2.0])))

    def test_nbt_forced_types(self):
        self.assertEqual('{Text2: \'"hi"\'}', str(Nbt(Text2='hi')))
        for key in ('Rotation', 'LeftArm', 'RightArm', 'LeftLeg', 'RightLeg', 'Head', 'Body'):
            self.assertEqual(f'{{{key}: [1f, 2f]}}', str(Nbt({key: [1, 2]})))
        self.assertEqual('{Motion: [1d, 2d]}', str(Nbt(Motion=[1, 2])))

    def test_nbt_get_list(self):
        self.assertEqual([], Nbt().get_list('key'))
        self.assertEqual([1, 2], Nbt(key=[1, 2]).get_list('key'))

    def test_nbt_get_nbt(self):
        self.assertEqual(Nbt(), Nbt().get_nbt('key'))
        self.assertEqual(Nbt(good=True), Nbt(key={'good': True}).get_nbt('key'))

    @parameterized.expand(((True,), (False,),))
    def test_nbt_format(self, spaces):
        Nbt.use_spaces = spaces
        self.assertEqual(spaceify('{}', spaces), str(Nbt()))
        self.assertEqual(spaceify('{key:true}', spaces), str(Nbt(key=True)))
        self.assertEqual(spaceify('{key:1}', spaces), str(Nbt(key=1)))
        # Could be either order
        self.assertIn(str(Nbt(key='value', key2=2)), (
            spaceify('{key:value,key2:2}', spaces), spaceify('{key2:2,key:value}', spaces)))
        self.assertEqual(spaceify('{key:"val ue"}', spaces), str(Nbt(key='val ue')))
        self.assertEqual(spaceify('{key:{num:17}}', spaces), str(Nbt(key={'num': 17})))
        self.assertEqual(spaceify('{key:{nums:[1,2,3]}}', spaces), str(Nbt(key={'nums': [1, 2, 3]})))

        with self.assertRaises(KeyError):
            Nbt({'k-ey': 13})

    @parameterized.expand(((True,), (False,),))
    def test_nbt_array(self, spaces):
        Nbt.use_spaces = spaces
        self.assertEqual(spaceify('[B;123]', spaces), str(Nbt.TypedArray('b', (123,))))
        self.assertEqual(spaceify('[B;123,4,5,6]', spaces), str(Nbt.TypedArray('B', (123, 4, 5, 6))))
        self.assertEqual(spaceify('[I;123]', spaces), str(Nbt.TypedArray('i', (123,))))
        self.assertEqual(spaceify('[I;123,4,5,6]', spaces), str(Nbt.TypedArray('I', (123, 4, 5, 6))))
        self.assertEqual(spaceify('[L;123]', spaces), str(Nbt.TypedArray('l', (123,))))
        self.assertEqual(spaceify('[L;123,4,5,6]', spaces), str(Nbt.TypedArray('L', (123, 4, 5, 6))))

        with self.assertRaises(ValueError):
            Nbt.TypedArray('d', ())

    def test_precision(self):
        orig = parameters.float_precision
        try:
            parameters.float_precision = 1
            self.assertEqual('setblock 1.1 2.2 5.6 air', str(setblock((1.111, 2.222, 5.555), 'air')))
            parameters.float_precision = 3
            self.assertEqual('setblock 1.111 2.222 5.555 air', str(setblock((1.111, 2.222, 5.555), 'air')))

            with self.assertRaises(ValueError):
                parameters.float_precision = 0

        finally:
            parameters.float_precision = orig

    def test_rel_coord(self):
        self.assertEqual(IntRelCoord('~', 3), r(3))
        self.assertEqual(RelCoord('~', 3.0), r(3.0))
        self.assertEqual(RelCoord('~', 3.1), r(3.1))
        self.assertEqual(r(5.5), r(2) + r(3.5))
        self.assertEqual(r(5.5), r(2) + 3.5)
        self.assertEqual(r(3.5), r(5.5) - r(2))
        self.assertEqual(r(3.5), r(5.5) - 2)
        self.assertEqual(r(7.2), r(4) * r(1.8))
        self.assertEqual(r(7.2), r(4) * 1.8)
        self.assertEqual(r(5.5), r(11) / r(2))
        self.assertEqual(r(5.5), r(11) / 2)
        self.assertEqual(r(5), r(11) // r(2))
        self.assertEqual(r(5), r(11) // 2)
        self.assertEqual(r(9), r(3) ** 2)
        self.assertEqual(r(4), abs(r(-4)))
        self.assertEqual(r(4), abs(r(4)))
        self.assertTrue(r(3) < r(3.1))
        self.assertFalse(r(3) > r(3.1))
        self.assertFalse(r(-3.5) > -r(3.5))
        self.assertFalse(r(3.5) > -r(-3.5))

    def test_rel_coord_merge(self):
        def add(v1: Coord, v2: Coord):
            return v1 + v2

        self.assertEqual(None, RelCoord.merge(add, None, None))
        self.assertEqual((1, 2, 3), RelCoord.merge(add, (1, 2, 3), None))
        self.assertEqual((1, 2, 3), RelCoord.merge(add, None, (1, 2, 3)))
        self.assertEqual((2, 4, 6), RelCoord.merge(add, (1, 2, 3), (1, 2, 3)))
        self.assertEqual(r(1, 2, 3), RelCoord.merge(add, r(1, 2, 3), None))
        self.assertEqual(r(1, 2, 3), RelCoord.merge(add, None, r(1, 2, 3)))
        self.assertEqual(r(2, 4, 6), RelCoord.merge(add, r(1, 2, 3), r(1, 2, 3)))

    def test_time_spec(self):
        self.assertEqual(0, TimeSpec(0).ticks)
        self.assertEqual(1, TimeSpec(0.9).ticks)
        self.assertEqual(1, TimeSpec(1).ticks)
        self.assertEqual(1, TimeSpec(20).seconds)
        self.assertEqual(1, TimeSpec(24_000).days)
        self.assertEqual(20, TimeSpec('1s').ticks)
        self.assertEqual(24_000, TimeSpec('1d').ticks)
