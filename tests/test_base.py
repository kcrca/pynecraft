import unittest

from parameterized import parameterized

from pynecraft.base import Arg, COLORS, Coord, EAST, IntRelCoord, NORTH, Nbt, RED, ROTATION_0, ROTATION_180, \
    ROTATION_270, ROTATION_90, RelCoord, SOUTH, TimeSpec, WEST, _bool, _ensure_size, _float, _in_group, _int_or_float, \
    _not_ify, _quote, _strip_namespace, _strip_not, _to_list, _to_tuple, as_angle, as_column, as_duration, as_facing, \
    as_name, \
    as_names, as_nbt_key, as_nbt_path, as_pitch, as_range, as_resource, as_resource_path, as_resources, as_yaw, d, days, \
    de_arg, r, \
    rotate_facing, seconds, settings, string, ticks, to_id
from pynecraft.commands import setblock


def spaceify(s, use_spaces):
    return s.replace(',', ', ').replace(':', ': ') if use_spaces else s


class TestBase(unittest.TestCase):
    def setUp(self) -> None:
        self.orig_spaces = Nbt.use_spaces

    def tearDown(self) -> None:
        Nbt.use_spaces = self.orig_spaces

    def test_quote(self):
        self.assertEqual('foo', _quote('foo'))
        self.assertEqual('"f b"', _quote('f b'))
        self.assertEqual('\'"f b"\'', _quote('"f b"'))
        self.assertEqual('"\'f b\'"', _quote("'f b'"))
        self.assertEqual('"true"', _quote("true"))
        self.assertEqual('"false"', _quote("false"))
        self.assertEqual(1, _quote(1))
        self.assertEqual(0.1, _quote(.1))
        self.assertEqual(1.0, _quote(1.))
        self.assertEqual(1.1, _quote(1.1))
        self.assertEqual('"1."', _quote("1."))
        self.assertEqual('".1"', _quote(".1"))
        self.assertEqual('"1.1"', _quote("1.1"))
        self.assertEqual('t1', _quote("t1"))

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
        self.assertEqual('$(b)', _strip_namespace(Arg('b')))
        self.assertEqual('a$(b)', _strip_namespace('a$(b)'))

    def test_strip_not(self):
        self.assertEqual('foo', _strip_not('!foo'))
        self.assertEqual('foo', _strip_not('foo'))
        self.assertEqual('$(f)', _strip_not(Arg('f')))
        self.assertEqual('b$(f)', _strip_not('b$(f)'))
        self.assertEqual('b$(f)', _strip_not('!b$(f)'))

    def test_bool(self):
        self.assertIsNone(_bool(None))
        self.assertEqual('true', _bool(True))
        self.assertEqual('$(b)', _bool(Arg('b')))

    def test_float(self):
        self.assertEqual('1', _float(1))
        self.assertEqual('1.0', _float(1.0))
        self.assertEqual('1.1', _float(1.1))
        self.assertEqual('1.123', _float(1.12345))
        self.assertEqual('$(f)', _bool(Arg('f')))

    def test_not_ify(self):
        self.assertEqual('!foo', _not_ify('foo'))
        self.assertTupleEqual(('!foo', '!bar', '!baz'), _not_ify(('foo', 'bar', 'baz')))

    def test_ensure_size(self):
        self.assertListEqual([None, None], _ensure_size([], 2))
        self.assertListEqual([None, None], _ensure_size([None], 2))
        self.assertListEqual([None, None], _ensure_size([None, None], 2))
        with self.assertRaises(ValueError):
            _ensure_size([None, None, None], 2)

    def test_as_nbt_key(self):
        self.assertEqual('key', as_nbt_key('key'))
        self.assertEqual('v$(k)', as_nbt_key('v$(k)'))
        self.assertEqual('$(k)', as_nbt_key(Arg('k')))

    def test_de_arg(self):
        self.assertEqual('x', de_arg('x'))
        self.assertEqual('$(x)', de_arg('$(x)'))
        self.assertEqual('$(x)', de_arg(Arg('x')))
        self.assertEqual(('x', 'y'), de_arg(('x', 'y')))
        self.assertEqual(('x', '$(y)'), de_arg(('x', Arg('y'))))
        self.assertEqual(('x', ('$(y)', '$(z)')), de_arg(('x', (Arg('y'), Arg('z')))))

    def test_as_nbt_path(self):
        self.assertEqual('a.b.c', as_nbt_path('a.b.c'))
        self.assertEqual('$(a)', as_nbt_path(Arg('a')))
        self.assertEqual('a.$(b).c', as_nbt_path('a.$(b).c'))
        self.assertEqual('a.b[-1]', as_nbt_path('a.b[-1]'))
        with self.assertRaises(ValueError):
            as_nbt_path('')
        with self.assertRaises(ValueError):
            as_nbt_path('a.b%c')

    def test_as_resource(self):
        self.assertIsNone(as_resource(None))
        self.assertEqual('a', as_resource('a'))
        self.assertEqual('!a', as_resource('!a', allow_not=True))
        self.assertEqual('m:a', as_resource('m:a'))
        self.assertEqual('!m:a', as_resource('!m:a', allow_not=True))
        self.assertEqual('!v$(k)', as_resource('!v$(k)', allow_not=True))
        self.assertEqual('v$(k)', as_resource('v$(k)', allow_not=True))
        self.assertEqual('$(k)', as_resource('$(k)', allow_not=True))
        self.assertEqual('$(k)', as_resource(Arg('k'), allow_not=True))
        with self.assertRaises(ValueError):
            as_resource('!a')
        with self.assertRaises(ValueError):
            as_resource('m:a', allow_namespace=False)

    def test_as_resources(self):
        self.assertTupleEqual((), as_resources())
        self.assertTupleEqual(('a',), as_resources('a'))
        self.assertTupleEqual(('a', '!b'), as_resources('a', '!b', allow_not=True))
        self.assertTupleEqual(('v$(a)', '!v$(b)'), as_resources('v$(a)', '!v$(b)', allow_not=True))
        self.assertTupleEqual(('$(a)', '$(b)'), as_resources(Arg('a'), Arg('b'), allow_not=True))
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
        self.assertEqual('!v$(k)', as_resource_path('!v$(k)', allow_not=True))
        self.assertEqual('v$(k)', as_resource_path('v$(k)', allow_not=True))
        self.assertEqual('$(k)', as_resource_path('$(k)', allow_not=True))
        self.assertEqual('$(k)', as_resource_path(Arg('k'), allow_not=True))
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
        self.assertEqual('v$(a)', as_name('v$(a)'))
        self.assertEqual('$(a)', as_name(Arg('a')))
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
        self.assertEqual(('v$(a)',), as_column('v$(a)'))
        self.assertEqual(('$(a)',), as_column(Arg('a')))
        with self.assertRaises(ValueError):
            as_column((1,))
        with self.assertRaises(ValueError):
            as_column((1, 2, 3))

    def test_as_angle(self):
        self.assertEqual(17, as_angle(17))
        self.assertEqual(17.3, as_angle(17.3))
        self.assertEqual(r(17.3), as_angle(r(17.3)))
        self.assertEqual('v$(a)', as_angle('v$(a)'))
        self.assertEqual('$(a)', as_angle(Arg('a')))
        with self.assertRaises(ValueError):
            as_angle(d(17.3))

    def test_as_yaw(self):
        self.assertIsNone(as_yaw(None))
        self.assertEqual(17.3, as_yaw(17.3))
        self.assertEqual(90, as_yaw(WEST))
        self.assertEqual('-$(a).1', as_yaw('-$(a).1'))
        self.assertEqual('$(a)', as_yaw(Arg('a')))
        with self.assertRaises(ValueError):
            as_yaw(181)
        with self.assertRaises(ValueError):
            as_yaw(-181)
        with self.assertRaises(KeyError):
            as_yaw('v$(k)')

    def test_as_pitch(self):
        self.assertIsNone(as_pitch(None))
        self.assertEqual(17.3, as_pitch(17.3))
        self.assertEqual('-$(a).1', as_pitch('-$(a).1'))
        self.assertEqual('$(a)', as_pitch(Arg('a')))
        with self.assertRaises(ValueError):
            as_pitch(181)
        with self.assertRaises(ValueError):
            as_pitch(-181)
        with self.assertRaises(TypeError):
            as_pitch('v$(k)')
        with self.assertRaises(TypeError):
            as_pitch(WEST)

    def test_in_group(self):
        self.assertIsNone(_in_group(COLORS, None))
        self.assertEqual(RED, _in_group(COLORS, RED))
        self.assertEqual('v$(a)', _in_group(COLORS, 'v$(a)'))
        self.assertEqual('$(a)', _in_group(COLORS, Arg('a')))
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
        self.assertEqual('v$(k)', as_duration('v$(k)'))
        self.assertEqual('$(k)', as_duration(Arg('k')))

    def test_as_range(self):
        self.assertEqual('17', as_range(17))
        self.assertEqual('28.3', as_range(28.3))
        self.assertEqual('5.3..8.4', as_range((5.3, 8.4)))
        self.assertEqual('5.3..', as_range((5.3, None)))
        self.assertEqual('..8.4', as_range((None, 8.4)))
        self.assertEqual('$(k)', as_range('$(k)'))
        self.assertEqual('+$(k).1', as_range('+$(k).1'))
        self.assertEqual('$(k)', as_range(Arg('k')))
        self.assertEqual('$(k)..-2.$(v)3', as_range((Arg('k'), '-2.$(v)3')))
        with self.assertRaises(ValueError):
            as_range((6, 3))
        with self.assertRaises(ValueError):
            as_range(False)
        with self.assertRaises(ValueError):
            as_range('v$(k)')
        with self.assertRaises(ValueError):
            as_range(('v$(k)', 'q$(z)'))

    def test_string(self):
        self.assertEqual('', string(''))
        self.assertEqual('3', string(3))
        self.assertEqual('(1, 2)', string((1, 2)))
        self.assertEqual('(1, ~2, ^3)', string((1, r(2), d(3))))

    def test_to_id(self):
        self.assertEqual('foo', to_id('foo'))
        self.assertEqual('foo_bar', to_id('Foo Bar'))
        self.assertEqual('v$(k)', to_id('v$(k)'))
        self.assertEqual('$(k)', to_id(Arg('k')))

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
        self.assertEqual({'key': 0}, Nbt().set_or_clear('key', 0))
        self.assertEqual({}, Nbt(key=12).set_or_clear('key', None))
        self.assertEqual({'key': 'foo'}, Nbt().set_or_clear('key', 'foo'))
        self.assertEqual({}, Nbt(key=12).set_or_clear('key', None))
        self.assertEqual({'o1': {'o2': {'o3': {'key': True}}}}, Nbt().set_or_clear('o1.o2.o3.key', True))
        self.assertEqual({'o1': {'o2': {'o3': {}}}},
                         Nbt({'o1': {'o2': {'o3': {'key': True}}}}).set_or_clear('o1.o2.o3.key', False))

    def test_nbt_str(self):
        self.assertEqual('{}', Nbt.to_str({}))
        self.assertEqual('{}', Nbt.to_str(Nbt({})))
        self.assertEqual('[]', Nbt.to_str([]))
        self.assertEqual(Nbt(sub=Nbt()), Nbt.as_nbt({'sub': {}}))
        self.assertEqual('$(a)', Nbt.to_str(Arg('a')))

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
        self.assertEqual(Arg('a'), Nbt({'list': Arg('a')}).get_list('list'))

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
        orig = settings.float_precision
        try:
            settings.float_precision = 1
            self.assertEqual('setblock 1.1 2.2 5.6 air', str(setblock((1.111, 2.222, 5.555), 'air')))
            settings.float_precision = 3
            self.assertEqual('setblock 1.111 2.222 5.555 air', str(setblock((1.111, 2.222, 5.555), 'air')))

            with self.assertRaises(ValueError):
                settings.float_precision = 0

        finally:
            settings.float_precision = orig

    def test_rel_coord(self):
        self.assertEqual(IntRelCoord('~', 3), r(3))
        self.assertEqual(RelCoord('~', 3.0), r(3.0))
        self.assertEqual(RelCoord('~', 3.1), r(3.1))
        self.assertEqual(RelCoord('~', Arg('v')), r(Arg('v')))
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
        with self.assertRaises(AssertionError):
            r(Arg('v')) + d(3.5)

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
        with self.assertRaises(TypeError):
            RelCoord.merge(add, r(Arg('a'), 2), r(1, 2))

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
        self.assertEqual(Arg('a'), Arg('a'))
        self.assertEqual(Arg('a'), '$(a)')
        self.assertNotEqual(Arg('a'), 'a')
        self.assertIsNotNone(Arg('a'))
        self.assertEqual(hash(Arg('a')), hash(Arg('a')))
        self.assertNotEqual(hash(Arg('a')), hash(Arg('b')))
        with self.assertRaises(ValueError):
            Arg('')
