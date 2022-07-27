import unittest

from parameterized import parameterized

from pynecraft.base import EAST, NORTH, Nbt, ROTATION_0, ROTATION_180, ROTATION_270, ROTATION_90, SOUTH, WEST, \
    rotated_facing


def spaceify(s, use_spaces):
    return s.replace(',', ', ').replace(':', ': ') if use_spaces else s


class TestBase(unittest.TestCase):
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

    @parameterized.expand(((True,), (False,),))
    def test_nbt_format(self, spaces):
        orig = Nbt.use_spaces
        try:
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
        finally:
            Nbt.use_spaces = orig
