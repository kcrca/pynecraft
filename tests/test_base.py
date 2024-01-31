import unittest

from parameterized import parameterized

from pynecraft.base import Coord, EAST, IntRelCoord, NORTH, Nbt, ROTATION_0, ROTATION_180, ROTATION_270, \
    ROTATION_90, RelCoord, SOUTH, \
    TimeSpec, WEST, \
    parameters, r, rotate_facing, as_facing, string, d, _to_list, _to_tuple, _strip_namespace, _strip_not, _bool, \
    _float, _not_ify, _ensure_size, as_nbt_path, as_resource, as_resources, as_resource_path, as_name, as_names, \
    as_column, as_angle, as_yaw, as_pitch, to_id, days, seconds, ticks, _int_or_float, _in_group, COLORS, RED, \
    as_duration, as_range, Arg
from pynecraft.commands import setblock


def spaceify(s, use_spaces):
    return s.replace(',', ', ').replace(':', ': ') if use_spaces else s


class TestBase(unittest.TestCase):
    def setUp(self) -> None:
        self.orig_spaces = Nbt.use_spaces

    def tearDown(self) -> None:
        Nbt.use_spaces = self.orig_spaces

    def test_to_list(self):
        self.assertListEqual([], _to_list(()))
        self.assertListEqual([], _to_list([]))
        self.assertListEqual([None], _to_list(None))
        self.assertListEqual([1], _to_list((1,)))
        self.assertListEqual([1], _to_list([1, ]))
        self.assertListEqual(['a'], _to_list('a'))
        self.assertListEqual([1], _to_list(1))
        self.assertListEqual([0, 1, 2], _to_list(range(3)))

    def test_to_tuple(self):
        self.assertTupleEqual((), _to_tuple(()))
        self.assertTupleEqual((), _to_tuple([]))
        self.assertTupleEqual((None,), _to_tuple(None))
        self.assertTupleEqual((1,), _to_tuple((1,)))
        self.assertTupleEqual((1,), _to_tuple([1, ]))
        self.assertTupleEqual(('a',), _to_tuple('a'))
        self.assertTupleEqual((1,), _to_tuple(1))
        self.assertTupleEqual((0, 1, 2), _to_tuple(range(3)))

    def test_strip_namespace(self):
        self.assertEqual('foo', _strip_namespace('m:foo'))
        self.assertEqual('foo', _strip_namespace('foo'))

    def test_strip_not(self):
        self.assertEqual('foo', _strip_not('!foo'))
        self.assertEqual('foo', _strip_not('foo'))

    def test_bool(self):
        self.assertIsNone(_bool(None))
        self.assertEqual('true', _bool(True))

    def test_float(self):
        self.assertEqual('1', _float(1))
        self.assertEqual('1.0', _float(1.0))
        self.assertEqual('1.1', _float(1.1))
        self.assertEqual('1.123', _float(1.12345))

    def test_not_ify(self):
        self.assertEqual('!foo', _not_ify('foo'))
        self.assertTupleEqual(('!foo', '!bar', '!baz'), _not_ify(('foo', 'bar', 'baz')))

    def test_ensure_size(self):
        self.assertListEqual([None, None], _ensure_size([], 2))
        self.assertListEqual([None, None], _ensure_size([None], 2))
        self.assertListEqual([None, None], _ensure_size([None, None], 2))
        with self.assertRaises(ValueError):
            _ensure_size([None, None, None], 2)

    def test_as_nbt_path(self):
        self.assertEqual('', as_nbt_path(''))
        self.assertEqual('a.b.c', as_nbt_path('a.b.c'))
        with self.assertRaises(ValueError):
            as_nbt_path('a.b%c')

    def test_as_resource(self):
        self.assertIsNone(as_resource(None))
        self.assertEqual('a', as_resource('a'))
        self.assertEqual('!a', as_resource('!a', allow_not=True))
        self.assertEqual('m:a', as_resource('m:a'))
        self.assertEqual('!m:a', as_resource('!m:a', allow_not=True))
        with self.assertRaises(ValueError):
            as_resource('!a')
        with self.assertRaises(ValueError):
            as_resource('m:a', allow_namespace=False)

    def test_as_resources(self):
        self.assertTupleEqual((), as_resources())
        self.assertTupleEqual(('a',), as_resources('a'))
        self.assertTupleEqual(('a', '!b'), as_resources('a', '!b', allow_not=True))
        with self.assertRaises(ValueError):
            as_resources('!a')
        with self.assertRaises(ValueError):
            as_resources('a', '!b')

    def test_as_resource_path(self):
        self.assertIsNone(as_resource_path(None))
        self.assertEqual('a', as_resource_path('a'))
        self.assertEqual('/a', as_resource_path('/a'))
        self.assertEqual('/a/b/c', as_resource_path('/a/b/c'))
        self.assertEqual('!/a/b/c', as_resource_path('!/a/b/c', allow_not=True))
        with self.assertRaises(ValueError):
            as_resource_path('')
        with self.assertRaises(ValueError):
            as_resource_path('!/a/b/c')
        with self.assertRaises(ValueError):
            as_resource_path('//a/b/c')

    def test_as_name(self):
        self.assertIsNone(as_name(None))
        self.assertEqual('a', as_name('a'))
        self.assertEqual('!a', as_name('!a', allow_not=True))
        with self.assertRaises(ValueError):
            as_name('!a')
        with self.assertRaises(ValueError):
            as_name('a%b')

    def test_as_names(self):
        self.assertTupleEqual((), as_names())
        self.assertTupleEqual(('a',), as_names('a'))
        self.assertTupleEqual(('!a',), as_names('!a', allow_not=True))
        self.assertTupleEqual(('!a', 'b', 'c'), as_names('!a', 'b', 'c', allow_not=True))
        with self.assertRaises(ValueError):
            as_names('!a')

    def test_as_column(self):
        self.assertEqual((1, 2), as_column((1, 2)))
        self.assertEqual(r(1, 2), as_column(r(1, 2)))
        self.assertEqual((1, r(2)), as_column((1, r(2))))
        with self.assertRaises(ValueError):
            as_column((1,))
        with self.assertRaises(ValueError):
            as_column((1, 2, 3))

    def test_as_angle(self):
        self.assertEqual(17, as_angle(17))
        self.assertEqual(17.3, as_angle(17.3))
        self.assertEqual(r(17.3), as_angle(r(17.3)))
        with self.assertRaises(ValueError):
            as_angle(d(17.3))

    def test_as_yaw(self):
        self.assertIsNone(as_yaw(None))
        self.assertEqual(17.3, as_yaw(17.3))
        self.assertEqual(90, as_yaw(WEST))
        with self.assertRaises(ValueError):
            as_yaw(181)
        with self.assertRaises(ValueError):
            as_yaw(-181)

    def test_as_pitch(self):
        self.assertIsNone(as_pitch(None))
        self.assertEqual(17.3, as_pitch(17.3))
        with self.assertRaises(ValueError):
            as_pitch(181)
        with self.assertRaises(ValueError):
            as_pitch(-181)
        with self.assertRaises(ValueError):
            as_pitch(WEST)

    def test_in_group(self):
        self.assertIsNone(_in_group(COLORS, None))
        self.assertEqual(RED, _in_group(COLORS, RED))
        with self.assertRaises(ValueError):
            _in_group(COLORS, None, allow_none=False)
        with self.assertRaises(ValueError):
            _in_group(COLORS, 'ecru')

    def test_as_facing(self):
        self.assertEqual(90, as_facing(WEST).yaw)
        self.assertEqual(0, as_facing(WEST).pitch)
        self.assertEqual('ese', as_facing(13).name)

    def test_rotated_facing(self):
        self.assertEqual((0, 0, -3), as_facing(NORTH).scale(3))
        self.assertEqual(as_facing(NORTH), rotate_facing(NORTH, ROTATION_0))
        self.assertEqual(as_facing(NORTH), rotate_facing(EAST, ROTATION_270))
        self.assertEqual(as_facing(NORTH), rotate_facing(SOUTH, ROTATION_180))
        self.assertEqual(as_facing(NORTH), rotate_facing(WEST, ROTATION_90))

    def test_as_duration(self):
        self.assertIsNone(as_duration(None))
        self.assertEqual(TimeSpec('15s'), as_duration(TimeSpec('15s')))
        self.assertEqual(TimeSpec(15), as_duration(15))

    def test_as_range(self):
        self.assertEqual('0', as_range(False))
        self.assertEqual('17', as_range(17))
        self.assertEqual('28.3', as_range(28.3))
        self.assertEqual('5.3..8.4', as_range((5.3, 8.4)))
        self.assertEqual('5.3..', as_range((5.3, None)))
        self.assertEqual('..8.4', as_range((None, 8.4)))
        with self.assertRaises(ValueError):
            as_range((6, 3))

    def test_string(self):
        self.assertEqual('', string(''))
        self.assertEqual('3', string(3))
        self.assertEqual('(1, 2)', string((1, 2)))
        self.assertEqual('(1, ~2, ^3)', string((1, r(2), d(3))))

    def test_to_id(self):
        self.assertEqual('foo', to_id('foo'))
        self.assertEqual('foo_bar', to_id('Foo Bar'))

    def test_nbt(self):
        self.assertEqual({'key': 1}, Nbt().merge(Nbt(key=1)))
        self.assertEqual({'key': 1}, Nbt(key=1).merge(None))
        self.assertEqual({'key': 1, 'key2': 2}, Nbt(key=1).merge(Nbt(key2=2)))
        self.assertEqual({'key': 2}, Nbt(key=1).merge(Nbt(key=2)))
        self.assertEqual({'key': 1, 'key2': 3}, Nbt(key=1, key2=2).merge(Nbt(key2=3)))
        self.assertEqual({'key': (2, 4, 6)}, Nbt(key=(1, 3, 5)).merge(Nbt(key=(2, 4, 6))))
        self.assertEqual({'key': '➝'}, Nbt(key='➝'), 'Non-ascii unicode should be unchanged')
        simple_nbt = Nbt(One=2)
        self.assertIs(simple_nbt, Nbt.as_nbt(simple_nbt))
        self.assertIsNot(simple_nbt, simple_nbt.clone())
        self.assertEqual(simple_nbt, simple_nbt.clone())
        self.assertEqual(Nbt(), Nbt()['One'])

    def test_set_or_clear(self):
        self.assertEqual({'key': 12}, Nbt().set_or_clear('key', 12))
        self.assertEqual({}, Nbt(key=12).set_or_clear('key', 0))
        self.assertEqual({'o1': {'o2': {'o3': {'key': True}}}}, Nbt().set_or_clear('o1.o2.o3.key', True))
        self.assertEqual({'o1': {'o2': {'o3': {}}}},
                         Nbt({'o1': {'o2': {'o3': {'key': True}}}}).set_or_clear('o1.o2.o3.key', False))

    def test_nbt_str(self):
        self.assertEqual('{}', Nbt.to_str({}))
        self.assertEqual('{}', Nbt.to_str(Nbt({})))
        self.assertEqual('[]', Nbt.to_str([]))
        self.assertEqual(Nbt(sub=Nbt()), Nbt.as_nbt({'sub': {}}))

    def test_nbt_regularize(self):
        self.assertEqual('{key: [1, 2]}', str(Nbt(key=[1, 2])))
        self.assertEqual('{key: [1.0f, 2.0f]}', str(Nbt(key=[1, 2.0])))
        self.assertEqual('{key: [1.0f, 2.0f]}', str(Nbt(key=[1.0, 2.0])))

    def test_nbt_forced_types(self):
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
        self.assertEqual(r(-3.5), -r(3.5))
        self.assertEqual(r(3.5), +r(3.5))
        self.assertEqual(r(4, 6), RelCoord.add(r(1, 2), r(3, 4)))
        self.assertEqual(r(-2, -2), RelCoord.sub(r(1, 2), r(3, 4)))

        with self.assertRaises(AssertionError):
            r(3.5) + d(3.5)

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
        self.assertEqual(2, TimeSpec(1.2).ticks)
        self.assertEqual(1, TimeSpec(20).seconds)
        self.assertEqual(1, TimeSpec(24_000).days)
        self.assertEqual(20, TimeSpec('1s').ticks)
        self.assertEqual(24_000, TimeSpec('1d').ticks)
        self.assertEqual(TimeSpec('15d'), days(15))
        self.assertEqual(TimeSpec('15s'), seconds(15))
        self.assertEqual(TimeSpec('15t'), ticks(15))
        self.assertEqual(TimeSpec(15), ticks(15))
        self.assertEqual('15d', str(TimeSpec('15d')))
        self.assertEqual('15s', str(TimeSpec('15s')))
        self.assertEqual('15', str(TimeSpec('15t')))
        self.assertEqual('15', str(TimeSpec('15')))
        with self.assertRaises(ValueError):
            TimeSpec('5q')

    def test_int_or_float(self):
        self.assertTrue(isinstance(_int_or_float(1), int))
        self.assertTrue(isinstance(_int_or_float(1.0), int))
        self.assertTrue(isinstance(_int_or_float(1.5), float))

    def test_arg(self):
        self.assertEqual('$(foo)', str(Arg('foo')))
        self.assertTrue(Arg('a') == Arg('a'))
        self.assertTrue(Arg('a') == '$(a)')
        self.assertFalse(Arg('a') == 'a')
        self.assertFalse(Arg('a') == None)
        self.assertEqual(hash(Arg('a')), hash(Arg('a')))
        self.assertNotEqual(hash(Arg('a')), hash(Arg('b')))

    def test_macro(self):
        self.assertEqual('$(a)', str(as_yaw(Arg('a'))))
        self.assertEqual('$(a)', str(as_pitch(Arg('a'))))
        self.assertEqual('$(a)', Nbt.to_str(Arg('a')))
        self.assertEqual(Arg('a'), Nbt({'list': Arg('a')}).get_list('list'))
        self.assertEqual(Arg('d'), as_duration(Arg('d')))
        self.assertEqual('$(r)', as_range(Arg('r')))
        self.assertEqual('$(b)..$(e)', as_range((Arg('b'), Arg('e'))))
