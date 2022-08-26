"""Basic types for pynecraft.

Note on the constants: Many of the defined constants are used in sets as legal arguments to commands. For example, the
list of dimensions is in the ``DIMENSION`` list, which is checked when a dimension is passed. If you use a datapack
that (say) adds a new dimension, it is *expected* that you would add to the ``DIMENSION`` list. That's why it is a list,
not a tuple.
"""

from __future__ import annotations

import copy
import functools
import json
import math
import re
from abc import ABC, abstractmethod
from collections import UserDict, UserList
from html.parser import HTMLParser
from io import StringIO
from json import JSONEncoder
from typing import Any, Iterable, Mapping, Optional, Tuple, TypeVar, Union

_jed_resource = r'a-zA-Z0-9_.-'
_resource_re = re.compile(fr'''(\#)?                          # Allow leading '#' for a tag
                               ([{_jed_resource}]+:)?         # an optional namespace
                               ([/{_jed_resource}]+)          # the resource path
                               (\[[,=\s{_jed_resource}]*])?   # an optional state, such as "[facing=south]"
                            ''', re.VERBOSE)
_name_re = re.compile(r'[\w+.-]+')
_nbt_key_re = re.compile(r'\w+')
_time_re = re.compile(r'([0-9]+(?:\.[0-9]+)?)([dst])?', re.IGNORECASE)
_backslash_re = re.compile(r'[\a\b\f\n\r\t\v]')
_backslash_map = {'\\': '\\', '\a': 'a', '\b': 'b', '\f': 'f', '\n': 'n', '\r': 'r', '\t': 't', '\v': 'v'}

NORTH = 'north'
EAST = 'east'
SOUTH = 'south'
WEST = 'west'
DIRECTIONS = [NORTH, EAST, SOUTH, WEST]

UP = 'up'
DOWN = 'down'
ALL_DIRECTIONS = DIRECTIONS + [UP, DOWN]

S = 's'
SSW = 'ssw'
SW = 'sw'
WSW = 'wsw'
W = 'w'
WNW = 'wnw'
NW = 'nw'
NNW = 'nnw'
N = 'n'
NNE = 'nne'
NE = 'ne'
ENE = 'ene'
E = 'e'
ESE = 'ese'
SE = 'se'
SSE = 'sse'

SIGN_DIRECTIONS = [S, SSW, SW, WSW, W, WNW, NW, NNW, N, NNE, NE, ENE, E, ESE, SE, SSE]

ROTATION_0 = 0
ROTATION_90 = 90
ROTATION_180 = 180
ROTATION_270 = 270
ROTATIONS = [ROTATION_0, ROTATION_90, ROTATION_180, ROTATION_270]

WHITE = 'white'
ORANGE = 'orange'
MAGENTA = 'magenta'
LIGHT_BLUE = 'light_blue'
YELLOW = 'yellow'
LIME = 'lime'
PINK = 'pink'
GRAY = 'gray'
LIGHT_GRAY = 'light_gray'
CYAN = 'cyan'
PURPLE = 'purple'
BLUE = 'blue'
BROWN = 'brown'
GREEN = 'green'
RED = 'red'
BLACK = 'black'
COLORS = [WHITE, ORANGE, MAGENTA, LIGHT_BLUE, YELLOW, LIME, PINK, GRAY, LIGHT_GRAY, CYAN, PURPLE, BLUE, BROWN, GREEN,
          RED, BLACK]
"""Valid colors."""

DARK_BLUE = 'dark_blue'
DARK_GREEN = 'dark_green'
DARK_AQUA = 'dark_aqua'
DARK_RED = 'dark_red'
DARK_PURPLE = 'dark_purple'
GOLD = 'gold'
DARK_GRAY = 'dark_gray'
AQUA = 'aqua'
LIGHT_PURPLE = 'light_purple'
RESET = 'reset'
JSON_COLORS = [BLACK, GRAY, BLUE, GREEN, RED, YELLOW, WHITE, DARK_BLUE, DARK_GREEN, DARK_AQUA, DARK_RED, DARK_PURPLE,
               GOLD, DARK_GRAY, AQUA, LIGHT_PURPLE, RESET]
"""Valid colors for JSON text."""

OVERWORLD = 'overworld'
THE_NETHER = 'the_nether'
THE_END = 'the_end'
DIMENSION = [OVERWORLD, THE_NETHER, THE_END]
"""Valid dimension names."""

DAYTIME = 'daytime'
GAMETIME = 'gametime'
DAY = 'day'
TIME_TYPES = [DAYTIME, GAMETIME, DAY]

NIGHT = 'night'
NOON = 'noon'
MIDNIGHT = 'midnight'
SUNRISE = 'sunrise'
SUNSET = 'sunset'
TIME_SPEC = [DAY, NIGHT, NOON, MIDNIGHT, SUNRISE, SUNSET]


def _quote(value):
    if isinstance(value, str):
        if not re.fullmatch(r'\w+', value):
            value = _backslash_re.sub(lambda x: '\\' + _backslash_map[x.group(0)], value)
            singles = value.count("'")
            doubles = value.count('"')
            if singles < doubles:
                return "'" + value.replace("'", r"\'").replace(r'\"', r'\\"') + "'"
            return '"' + value.replace('"', r'\"').replace(r"\'", r"\\\'") + '"'
    return value


def _to_list(data):
    if isinstance(data, list):
        return data
    if isinstance(data, str):
        return [data]
    if isinstance(data, Iterable) and not isinstance(data, Mapping):
        return list(data)
    return [data]


def _to_tuple(data):
    if isinstance(data, tuple):
        return data
    if isinstance(data, str):
        return data,
    if isinstance(data, Iterable) and not isinstance(data, Mapping):
        return tuple(data)
    return data,


def _strip_namespace(path):
    parts = path.split(':', 1)
    if len(parts) > 1:
        good_resource(parts[0])
        path = parts[1]
    return path


def _strip_not(path):
    if path and path[0] == '!':
        return path[1:]
    return path


def _bool(value: bool | None) -> str | None:
    if value is None:
        return None
    return str(value).lower()


def _float(value: float) -> str:
    return str(round(value, Parameters.float_precision()))


def _not_ify(value: str | Iterable[str]) -> str | Iterable[str]:
    if isinstance(value, str):
        s = str(value)
        if not s.startswith('!'):
            s = '!' + s
        return s
    else:
        return tuple((_not_ify(x) for x in value))


def _ensure_size(lst: Iterable[any, ...], size: int, fill=None) -> list:
    lst = _to_list(lst)
    if len(lst) > size:
        raise ValueError('More than 4 values in sign input')
    lst.extend([fill] * (size - len(lst)))
    return lst


def good_nbt_key(key: str) -> str:
    """Checks if the argument is a good NBT key. If not, it raises KeyError.

    :param key: The (probable) key.
    :return: the original input string.
    """
    if not _nbt_key_re.fullmatch(key):
        raise KeyError(f'{key}: Invalid NBT key')
    return key


def good_resource(name: str | None, allow_namespace=True, allow_not=False) -> str | None:
    """Checks if the argument is a valid resource name, or None. If not, it raises ValueError.

    :param name: The (probable) resource name.
    :param allow_namespace: Whether to allow a resource prefix such as 'minecraft:'..
    :param allow_not: Whether to allow a '!' before the name.
    :return: the input value.
    """
    if name is None:
        return None
    eval_name = name
    if allow_not:
        eval_name = _strip_not(eval_name)
    if allow_namespace:
        eval_name = _strip_namespace(eval_name)
    if not _resource_re.fullmatch(eval_name):
        raise ValueError(f'{eval_name}: Invalid resource')
    return name


def good_resources(*names: str, allow_not=False) -> tuple[str, ...]:
    """Calls good_resource on each name.

    :param names: The (probable) resource names .
    :param allow_not: Whether to allow a '!' before any names.
    :return: the input names
    """
    for t in names:
        good_resource(t, allow_not=allow_not)
    return names


def good_resource_path(path: str | None, allow_not=False) -> str | None:
    """Checks if the argument is a valid resource path, or None.

    :param path: The (probable) path.
    :param allow_not: Whether to allow a '!' before any names.
    :return: the input value.
    """
    if path is None:
        return None
    orig = path
    if allow_not:
        path = _strip_not(path)
    path = _strip_namespace(path)
    path = path.lstrip('/')
    for part in path.split('/'):
        try:
            good_resource(part, allow_namespace=False)
        except ValueError:
            raise ValueError(f'{part}: Invalid resource location in dir {path}')
    return orig


def good_item_stack(item: str):
    """
    Checks if the argument is a valid item stack specification. This only checks the resource part of the item stack.

    :param item: The (probable) item stack.
    :return: the input value
    """
    resource, *_ = item.split('{')
    good_resource(resource)
    return item


def good_name(name: str | None, allow_not=False) -> str | None:
    """Checks if the argument is a valid name, such as for a user, or None.

    :param name: The (probable) name.
    :param allow_not: Whether to allow a '!' before any names.
    :return: the input value.
    """
    if name is None:
        return None
    orig = name
    if allow_not:
        name = _strip_not(name)
    if not _name_re.fullmatch(name):
        raise ValueError(f'{name}: Invalid name')
    return orig


def good_names(*names: str, allow_not=False) -> tuple[str, ...]:
    """Calls good_name on each name

    :param names: The (probable) names.
    :param allow_not: Whether to allow a '!' before any names.
    :return: the input values.
    """
    for t in names:
        good_name(t, allow_not)
    return names


def good_column(col: IntColumn) -> IntColumn:
    """Checks if the argument is a valid column position.

    A valid column position is a tuple or list of two ints and/or IntRelCoords.

    :param col: The (probable) column position.
    :return: The input value.
    """
    if isinstance(col, (tuple, list)):
        if len(col) != 2:
            raise ValueError(f'{col}: Column must have 2 values')
        for c in col:
            if not isinstance(c, (int, IntRelCoord)):
                raise ValueError(f'{c}: not a coordinate')
        return col
    raise ValueError(f'{str(col)}: Invalid column position')


def good_angle(angle: Angle) -> Angle:
    """Checks if the angle is a valid one. "Valid" means a float or a tilde relative coordinate (such as ``~45``).

    :param angle: The (probable) angle.
    :return: The input value.
    """
    if isinstance(angle, (int, float)):
        return angle
    elif isinstance(angle, RelCoord):
        if angle.prefix != '~':
            raise ValueError(f'{angle.prefix}: Invalid angle prefix')
        return angle
    else:
        raise ValueError(f'{angle}: Invalid angle')


def good_yaw(yaw: Angle | str | None) -> Angle | None:
    """Checks if the angle is a valid yaw value, or None.

     "Valid" means a value that good_facing() or good_angle() accepts. If it is a number or RelCoord, it must be in
     the range [-180, 180).

    :param yaw: The (probable) yaw angle.
    :return: The input value.
    """
    if yaw is not None:
        if isinstance(yaw, str):
            yaw = good_facing(yaw).rotation[0]
        else:
            yaw = good_angle(yaw)
            yv = yaw.value if isinstance(yaw, RelCoord) else yaw
            if not -180 <= yv < 180:
                raise ValueError(f'{yv}: must be in range [-180.0, 180.0)')
    return yaw


def good_pitch(pitch: Angle | None) -> Angle | None:
    """Checks if the angle is a valid pitch value, or None.

     "Valid" means a value that good_angle() accepts, and that is the range [-90, 90).

    :param pitch: The (probable) pitch angle.
    :return: The input value.
    """
    if pitch is not None:
        pitch = good_angle(pitch)
        yv = pitch.value if isinstance(pitch, RelCoord) else pitch
        if not -90 <= yv < 90:
            raise ValueError(f'{yv}: must be in range [-90.0, 90.0)')
    return pitch


class JsonHolder(ABC):
    """Base class for a holder of JSON."""

    @abstractmethod
    def content(self):
        """Returns the JSON content to put into a string."""
        pass


class _JsonEncoder(JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, JsonHolder):
            return o.content()
        if isinstance(o, Nbt):
            return dict(o)
        return JSONEncoder.default(self, o)


_VALID_NBT_ARRAY_TYPES = ('I', 'L', 'B')


def _good_array_type(type):
    if not type.upper() in _VALID_NBT_ARRAY_TYPES:
        raise ValueError(f'{type}: Must be one of {_VALID_NBT_ARRAY_TYPES}')
    return type.upper()


class Nbt(UserDict):
    """A simple NBT handling class, that models NBT values as a python dictionary.

    You can set the value of a key directly to any valid value. By default, the value of a key will be an Nbt object.

    The string representation is particularly tricky. Most NBT is simple key/value pairs, where values are booleans,
    ints, floats, strings, or more NBT. A few places use JSON text. These keys (such as a sign's Text fields) must be
    presented as JSON text. Those keys are special-cased in this code. You can also put a JsonText value for a field
    to have it treated as JSON text.

    No attempt is made to validate the NBT against expected values, such as whether a ``Rotation`` value is a list of
    two floats or something else.
    """
    use_spaces = True
    """Whether to put spaces after colons and commas."""
    sort_keys = True
    """Whether to output keys in sorted order."""

    class TypedArray(UserList):
        def __init__(self, type: str, initlist=None):
            super().__init__(initlist)
            self.type = _good_array_type(type)

        def __str__(self):
            sout = StringIO()
            Nbt._to_str(self, sout)
            return str(sout.getvalue())

    _json_tags = tuple([f'Text{x}' for x in range(1, 5)] + ['CustomName', 'Pages'])
    _forced_type_tags = {'Motion': 'd', 'Rotation': 'f',
                         'LeftArm': 'f', 'RightArm': 'f', 'LeftLeg': 'f', 'RightLeg': 'f', 'Head': 'f', 'Body': 'f'}

    def clone(self):
        """Returns a deep copy of this Nbt"""
        return copy.deepcopy(self)

    def __setitem__(self, key, value):
        if isinstance(value, Mapping) and not isinstance(value, (Nbt, JsonHolder)):
            value = Nbt.as_nbt(value)
        super().__setitem__(good_nbt_key(key), value)

    def __str__(self):
        sout = StringIO()
        Nbt._to_str(self, sout)
        return str(sout.getvalue())

    def __missing__(self, key):
        nbt = Nbt()
        self[key] = nbt
        return nbt

    @classmethod
    def to_str(cls, obj) -> str:
        """
        Returns a string version of what is passed, using str() instead of repr() for dict and iterables. Because
        str(dict), str(list), etc., use repr(), not str().
        """
        if isinstance(obj, cls):
            return str(obj)
        if isinstance(obj, Mapping):
            return str(cls.as_nbt(obj))
        sout = StringIO()
        cls._to_str(obj, sout, False)
        return str(sout.getvalue())

    @classmethod
    def as_nbt(cls, nbt: NbtDef):
        """Returns the input parameter as an Nbt, including making a copy of an Nbt object that is passed in."""
        if not isinstance(nbt, cls):
            nbt = cls(nbt)
        for k, v in nbt.items():
            if isinstance(v, (cls, dict)):
                nbt[k] = cls.as_nbt(v)
        return nbt

    @classmethod
    def _regularize(cls, lst: Iterable) -> list:
        """For a list of ints and/or floats, makes sure that if any values are floats, all are floats."""
        types = set()
        lst = _to_list(lst)
        for x in lst:
            t = type(x)
            if t not in (int, float):
                return lst
            if t not in types and len(types) > 0:
                return [float(x) for x in lst]
            else:
                types.add(t)
        return lst

    @classmethod
    def _comma(cls, first, sout):
        if not first:
            sout.write(',')
            cls._space(sout)
        return False

    @classmethod
    def _space(cls, sout):
        if cls.use_spaces:
            sout.write(' ')

    @classmethod
    def _write_key(cls, key, sout):
        sout.write(key)
        sout.write(':')

    @classmethod
    def _to_str(cls, elem, sout, force_type=None):
        if isinstance(elem, (Nbt, dict)):
            sout.write('{')
            keys = elem.keys()
            if Nbt.sort_keys:
                keys = sorted(keys, key=str.casefold)
            first = True
            for key in keys:
                value = elem[key]
                first = cls._comma(first, sout)
                cls._write_key(key, sout)
                cls._space(sout)
                if key in cls._json_tags:
                    sout.write(_quote(json.dumps(value, cls=_JsonEncoder, sort_keys=Nbt.sort_keys)))
                elif key in cls._forced_type_tags:
                    cls._to_str(value, sout, force_type=cls._forced_type_tags[key])
                else:
                    cls._to_str(value, sout, force_type)
            sout.write('}')
        elif isinstance(elem, Nbt.TypedArray):
            sout.write('[')
            sout.write(elem.type)
            sout.write(';')
            first = True
            for e in elem:
                first = cls._comma(first, sout)
                cls._to_str(e, sout)
            sout.write(']')
        elif isinstance(elem, str):
            sout.write(_quote(elem))
        elif isinstance(elem, (list, tuple)):
            elem = cls._regularize(elem)
            sout.write('[')
            first = True
            for e in elem:
                first = cls._comma(first, sout)
                cls._to_str(e, sout, force_type)
            sout.write(']')
        elif isinstance(elem, bool):
            sout.write(_bool(elem))
        elif isinstance(elem, float) or (force_type and isinstance(elem, int)):
            sout.write(_float(elem))
            sout.write(force_type if force_type else 'f')
        elif isinstance(elem, int):
            sout.write(str(elem))
        else:
            sout.write(_quote(str(elem)))

    def merge(self, nbt: NbtDef) -> Nbt:
        """Merge another Nbt into this one.

        For simple key/value pairs with the same key, the value is replaced, absent keys are set from the other nbt.
        If the value is an Nbt, it is treated the same, recursively. Any mutable mapping (such as a typical dict) is
        converted to an Nbt map.

        :param nbt: The Nbt to merge from.
        :return: A new Nbt with the merged results.
        """
        return self._merge(self, nbt)

    def _merge(self, dst, src):
        if src is None:
            src = {}
        result = Nbt(dst)
        for k, v in src.items():
            if k not in result:
                result[k] = v
            else:
                if isinstance(v, Mapping):
                    result[k] = self._merge(result[k], v)
                else:
                    result[k] = v
        return result

    def get_list(self, key: str) -> [object, ...]:
        """Returns the list for the given key, creating an empty list for it if needed.

        :param key: The key for the list.
        :return: the (possibly created) list for the key.
        """
        if key in self:
            value = self[key]
            assert isinstance(value, list), f'{key}: Expected list value, got {value}'
        else:
            value = self[key] = []
        return value

    def get_nbt(self, key: str) -> Nbt:
        """Returns the Nbt under the given key, creating an empty Nbt for it if needed.

        :param key: The key for the Nbt.
        :return: the (possibly created) Nbt for the key.
        """
        if key not in self:
            self[key] = Nbt()
        return self[key]


class _ToMinecraftText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.attr_for = {'b': 'bold', 'i': 'italic', 'u': 'underlined', 'strike': 'strikethrough'}
        self.attrs = []
        self.out = []

    def handle_starttag(self, tag, attrs):
        self.attrs.append(self.attr_for[tag])

    def handle_endtag(self, tag):
        self.attrs.remove(self.attr_for[tag])

    def handle_data(self, data):
        node = {'text': str(data)}
        for a in self.attrs:
            node[a] = 'true'
        self.out.append(node)

    def json(self) -> list:
        return self.out

    def __str__(self):
        return json.dumps(self.out)


class Parameters:
    """Manage general parameters."""

    _float_precision = 3

    @classmethod
    def float_precision(cls):
        """Returns how many decimal places will be shown for floats."""
        return cls._float_precision

    @classmethod
    def set_float_precision(cls, precision: int):
        """Sets how many decimal places will be shown for floats. Must be at least one."""
        if precision < 1:
            raise ValueError(f'{precision}: Precision must be positive')
        cls._float_precision = precision


NbtDef = Union[Nbt, Mapping]


def to_id(name: str) -> str:
    """
    Returns an ID from the passed-in name. If it's already an ID, it is just returned. Otherwise, it lower-cases the
    name, and replaces both ' ' and '| with '_'.
    """
    return re.sub(r'\s+|\|', '_', name.strip().lower())


def to_name(id: str) -> str:
    """
    Returns a user-friendly name from the passed-in ID. It just replaces '_' with spaces and title-cases the result.
    """
    return id.replace('_', ' ').title()


@functools.total_ordering
class RelCoord:
    """A relative coordinate. These are shown in minecraft commands with special annotation, such as '~1' or '^2'."""

    def __init__(self, prefix: str, v: float):
        self.prefix = prefix
        self.value = v
        self._rep = prefix + _float(v)

    def _v(self: U, v: float) -> U:
        if isinstance(v, int):
            return IntRelCoord(self.prefix, v)
        else:
            return RelCoord(self.prefix, v)

    def __str__(self):
        return self._rep

    def __eq__(self, other):
        return self.prefix == other.prefix and self.value == other.value

    def __hash__(self):
        return hash(self._rep)

    def __lt__(self, other):
        return self.prefix < other.prefix or self.prefix == other.prefix and self.value < other.value

    def __add__(self: U, other: float | U) -> U:
        if not isinstance(other, (float, int)):
            assert other.prefix == self.prefix
            other = other.value
        return self._v(self.value + other)

    def __sub__(self: U, other: float | U) -> U:
        if not isinstance(other, (float, int)):
            assert other.prefix == self.prefix
            other = other.value
        return self._v(self.value - other)

    def __mul__(self: U, other: float | U) -> U:
        if not isinstance(other, (float, int)):
            assert other.prefix == self.prefix
            other = other.value
        return self._v(self.value * other)

    def __truediv__(self, other):
        if not isinstance(other, (float, int)):
            assert other.prefix == self.prefix
            other = other.value
        return self._v(self.value / other)

    def __floordiv__(self: U, other: float | U) -> U:
        if not isinstance(other, (float, int)):
            assert other.prefix == self.prefix
            other = other.value
        return self._v(self.value // other)

    def __pow__(self: U, other: float) -> U:
        return self._v(self.value ** other)

    def __abs__(self: U) -> U:
        if self.value >= 0:
            return self
        return self._v(-self.value)

    def __index__(self: U) -> U:
        return self._v(int(self.value))

    def __neg__(self: U) -> U:
        return self._v(-self.value)

    def __pos__(self: U) -> U:
        return self


U = TypeVar('U', bound=RelCoord)


class IntRelCoord(RelCoord):
    """A relative coordinate that has no fractional part."""

    def __init__(self, prefix: str, v: int):
        super().__init__(prefix, int(v))


def _rel_coord(ch, f, v, *others) -> RelCoord | Tuple[RelCoord, ...]:
    if len(others) == 0:
        return IntRelCoord(ch, v) if isinstance(v, int) else RelCoord(ch, v)
    return tuple(f(x) for x in (v, *others))


def r(v: float, *others: float) -> RelCoord | Tuple[RelCoord, RelCoord] | Tuple[IntRelCoord, IntRelCoord] | \
                                   Tuple[RelCoord, RelCoord, RelCoord] | Tuple[RelCoord, ...]:
    """Returns a single or tuple '~' relative coordinate(s) of its input value(s). If all values are integers,
    the value(s) will be IntRelCoords. """
    return _rel_coord('~', r, v, *others)


def d(v: float, *others: float) -> RelCoord | Tuple[RelCoord, RelCoord, RelCoord] | Tuple[RelCoord, ...]:
    """Returns a single or tuple '^' relative coordinate(s) of its input value(s). If all values are integers,
    the value(s) will be IntRelCoords. """
    return _rel_coord('^', d, v, *others)


def days(num: float) -> TimeSpec:
    """Return a specification for the given number of days."""
    return TimeSpec(f'{num}d')


def seconds(num: float) -> TimeSpec:
    """Return a specification for the given number of seconds."""
    return TimeSpec(f'{num}s')


def ticks(num: float) -> TimeSpec:
    """Return a specification for the given number of ticks."""
    return TimeSpec(num)


def _int_or_float(value: int | float) -> int | float:
    if isinstance(value, int) or value.is_integer():
        return int(value)
    return value


class TimeSpec:
    """Represents a time using in-game ticks. Minecraft is sloppy about the distinction between a duration and a
    time(stamp). Both `/time set` and `time add` take this same kind of value as an argument. This class preserves
    that confusion. """

    SCALES = {'d': 24_000, 's': 20, 't': 1}

    def __init__(self, value: float | str):
        """Creates a new TimeSpec. The value is either a float value (which is rounded to the next highest game tick),
        or a string that is a float followed by a scaling suffix, one of 't' (ticks), 's' (seconds), or 'd' (days).

         :param value: A float or a string that is a float with a valid scale suffix.
        """
        self._units = None  # gets set by the 'ticks' property
        self._as_units = None
        self._ticks = None

        if isinstance(value, (int, float)):
            self.ticks = _int_or_float(value)
        else:
            m = _time_re.fullmatch(value)
            if not m:
                raise ValueError(f'{value}: Invalid time specification')
            value = _int_or_float(float(m.group(1)))
            if not m.group(2):
                self.ticks = int(math.ceil(value))
            else:
                suffix = m.group(2).lower()
                if suffix == 't':
                    self.ticks = value
                elif suffix == 's':
                    self.seconds = value
                elif suffix == 'd':
                    self.days = value
                else:
                    raise ValueError(f'{suffix}: Unknown suffix')

    def __str__(self):
        if self._units == 't':
            return f'{self._as_units}'
        else:
            return f'{self._as_units}{self._units}'

    @property
    def ticks(self) -> int:
        """The number of ticks this TimeSpec represents."""
        return self._ticks

    @ticks.setter
    def ticks(self, value: float | int):
        self._ticks = math.ceil(_int_or_float(value))
        self._units = 't'
        self._as_units = self._ticks

    @property
    def seconds(self) -> float:
        """The number of seconds this TimeSpec represents."""
        return self.ticks / TimeSpec.SCALES['s']

    @seconds.setter
    def seconds(self, value: float):
        self.ticks = value * TimeSpec.SCALES['s']
        self._units = 's'
        self._as_units = _int_or_float(value)

    @property
    def days(self) -> float:
        """The number of days this TimeSpec represents."""
        return self.ticks / TimeSpec.SCALES['d']

    @days.setter
    def days(self, value: float):
        self.ticks = value * TimeSpec.SCALES['d']
        self._units = 'd'
        self._as_units = _int_or_float(value)


class Facing:
    """This class represents information about facing in a given direction."""

    def __init__(self, name: str, delta: Tuple[float, float, float], rotation: Tuple[float, float], number: int,
                 sign_rotation: int = 0):
        """Creates a Facing object.

        :param name: The name of the direction, such as ``NORTH`` or ``SW``.
        :param delta: The amount to add to coordinates to move in the direction.
        :param rotation: The values to use as a ``Rotation`` NBT value.
        :param number: The number used by most blocks and entities for this rotation, or NaN if none.
        :param sign_rotation: The number used for rotation for a sign.
        """
        self.delta = delta
        self.name = name
        self.rotation = rotation
        self.number = number
        self.sign_rotation = sign_rotation

    def __str__(self):
        return self.name

    @property
    def yaw(self) -> int | float:
        """Return the yaw (first) value of the rotation."""
        return self.rotation[0]

    @property
    def pitch(self) -> int | float:
        """Return the pitch (second) value of the rotation."""
        return self.rotation[1]

    @property
    def dx(self) -> int | float:
        """Return the X (first) value of the delta."""
        return self.delta[0]

    @property
    def dy(self) -> int | float:
        """Return the Y (second) value of the delta."""
        return self.delta[1]

    @property
    def dz(self) -> int | float:
        """Return the Z (third) value of the delta."""
        return self.delta[2]

    def scale(self, scale: float) -> Tuple[float, float, float]:
        """Return the motion vector scaled by a value."""
        return self.dx * scale, self.dy * scale, self.dz * scale


_facing = {NORTH: Facing(NORTH, (0, 0, -1), (180, 0), 2), EAST: Facing(EAST, (1, 0, 0), (270, 0), 5),
           SOUTH: Facing(SOUTH, (0, 0, 1), (0, 0), 3), WEST: Facing(WEST, (-1, 0, 0), (90, 0), 4),
           UP: Facing(UP, (0, 1, 0), (0, 90), 1), DOWN: Facing(DOWN, (0, -1, 0), (0, 270), 0)}
_facing[ROTATION_0] = _facing[SOUTH]
_facing[ROTATION_90] = _facing[EAST]
_facing[ROTATION_180] = _facing[NORTH]
_facing[ROTATION_270] = _facing[WEST]
_facing[N] = _facing[NORTH]
_facing[E] = _facing[EAST]
_facing[S] = _facing[SOUTH]
_facing[W] = _facing[WEST]
for __i, __r in enumerate(SIGN_DIRECTIONS):
    # One motivation for this logic is to keep deltas as ints where possible.
    if __r in _facing:
        _facing[__r].sign_rotation = __i
        _facing[__i] = _facing[__r]
    elif __i in _facing:
        # This affects only zero.
        _facing[__i].sign_rotation = __i
        _facing[__r] = _facing[__i]
    else:
        __deg = round((90 + __i * 22.5 + 720) % 360, 1)
        __angle = math.radians(__deg)
        # noinspection PyTypeChecker
        _facing[__r] = Facing(__r, (math.cos(__angle), 0, math.sin(__angle)), ((720 + __deg) % 360, 0), math.nan, __i)
        _facing[__i] = _facing[__r]

_facing_info = {NORTH: (0, -1, 0), EAST: (1, 0, 270), SOUTH: (0, 1, 180), WEST: (-1, 0, 90)}


def _in_group(group: list | tuple, name: str | int):
    if name not in group:
        raise ValueError(f'{name}: Not in {group}')
    return name


def rotated_facing(facing: FacingDef, rotated_by: int = None) -> Facing:
    """Returns the value of facing() after rotating by the specified amount.

    For example ``rotated_Facing(NORTH, ROTATION_90)`` is ``EAST``. This allows your code to use relative operations, such as
    placing a sign to the right of an entity, no matter which way it is facing."""
    if rotated_by is not None:
        rot = int(_in_group(ROTATIONS, rotated_by) / 90)
        facing = good_facing(facing)
        if facing.name in DIRECTIONS:
            rotation_aid = DIRECTIONS + DIRECTIONS
        else:
            rotation_aid = SIGN_DIRECTIONS + SIGN_DIRECTIONS
            rot *= 4
        facing = good_facing(rotation_aid[rotation_aid.index(facing.name) + rot])
    return good_facing(facing)


def good_facing(facing: FacingDef) -> Facing:
    """Checks if the argument is a valid 'facing' specification.

    "Valid" means a Facing object, a known direction name, or a valid sign direction (see good_sign_facing()).

    :param facing: The (probable) facing specification.
    :return: the appropriate Facing object.
    """
    if isinstance(facing, Facing):
        return facing
    if isinstance(facing, str):
        return _facing[facing.lower()]
    return _facing[facing]


FacingDef = Union[int, str, Facing]
DurationDef = Union[str, int, TimeSpec]
Coord = Union[float, RelCoord]
Angle = Union[float, RelCoord]
IntCoord = Union[int, IntRelCoord]
Position = Tuple[Coord, Coord, Coord]
XYZ = Tuple[float, float, float]
Column = Tuple[Coord, Coord]
IntColumn = Tuple[IntCoord, IntCoord]


def good_duration(duration: DurationDef) -> TimeSpec | None:
    """Checks if the argument is a valid duration specification, or None.

    If the input is None, it is returned. Otherwise, this returns Duration(duration).
    """
    if duration is None or isinstance(duration, TimeSpec):
        return duration
    return TimeSpec(duration)


Range = Union[float, Tuple[Optional[float], Optional[float]]]


def good_range(spec: Range) -> str:
    """Checks if the argument is a valid numeric range.

     "Valid" means a single number, or a two-element list or tuple that define the endpoints. One of the
     endpoints may be None to define an open end.

    :param spec: The (probable) range.
    :return: A string for the range, either the single number of a range using '..' between the two values.    """

    if isinstance(spec, float) or isinstance(spec, int):
        return str(spec)
    for v in spec:
        if v is not None and not isinstance(v, (float, int)):
            raise ValueError(f'{v}: Not None or a number')
    s = '' if spec[0] is None else spec[0]
    e = '' if spec[1] is None else spec[1]
    if isinstance(s, float) and isinstance(e, float) and s > e:
        raise ValueError('Start is greater than end')
    return str(s) + '..' + str(e)
