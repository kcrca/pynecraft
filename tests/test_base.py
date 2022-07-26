import unittest

from parameterized import parameterized

from pynecraft.base import EAST, NORTH, Nbt, ROTATION_0, ROTATION_180, ROTATION_270, ROTATION_90, SOUTH, WEST, \
    rotated_facing


def spaceify(s, use_spaces):
    return s.replace(',', ', ').replace(':', ': ') if use_spaces else s


class TestBase(unittest.TestCase):
    def test_rotated_facing(self):
        self.assertEqual(rotated_facing(NORTH).scale(3), (0, 0, -3))
        self.assertEqual(rotated_facing(NORTH, ROTATION_0), rotated_facing(NORTH))
        self.assertEqual(rotated_facing(EAST, ROTATION_270), rotated_facing(NORTH))
        self.assertEqual(rotated_facing(SOUTH, ROTATION_180), rotated_facing(NORTH))
        self.assertEqual(rotated_facing(WEST, ROTATION_90), rotated_facing(NORTH))

    def test_nbt(self):
        self.assertEqual(Nbt().merge(Nbt(key=1)), {'key': 1})
        self.assertEqual(Nbt(key=1).merge(Nbt(key2=2)), {'key': 1, 'key2': 2})
        self.assertEqual(Nbt(key=1).merge(Nbt(key=2)), {'key': 2})
        self.assertEqual(Nbt(key=1, key2=2).merge(Nbt(key2=3)), {'key': 1, 'key2': 3})
        self.assertEqual(Nbt(key=(1, 3, 5)).merge(Nbt(key=(2, 4, 6))), {'key': (2, 4, 6)})

    @parameterized.expand(((True,), (False,),))
    def test_nbt_format(self, spaces):
        orig = Nbt.use_spaces
        try:
            Nbt.use_spaces = spaces
            self.assertEqual(str(Nbt()), spaceify('{}', spaces))
            self.assertEqual(str(Nbt(key=True)), spaceify('{key:true}', spaces))
            self.assertEqual(str(Nbt(key=1)), spaceify('{key:1}', spaces))
            # Could be either order
            self.assertIn(str(Nbt(key='value', key2=2)), (
                spaceify('{key:value,key2:2}', spaces), spaceify('{key2:2,key:value}', spaces)))
            self.assertEqual(str(Nbt(key='val ue')), spaceify('{key:"val ue"}', spaces))
            self.assertEqual(str(Nbt(key={'num': 17})), spaceify('{key:{num:17}}', spaces))
            self.assertEqual(str(Nbt(key={'nums': [1, 2, 3]})), spaceify('{key:{nums:[1,2,3]}}', spaces))

            with self.assertRaises(KeyError):
                Nbt({'k-ey': 13})
        finally:
            Nbt.use_spaces = orig
