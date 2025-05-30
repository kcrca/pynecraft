"""Basic types for pynecraft.

Note on the constants: Many of the defined constants are used in sets as legal arguments to commands. For example, the
list of dimensions is in the ``DIMENSION`` list, which is checked when a dimension is passed. If you use a datapack
that (say) adds a new dimension, it is *expected* that you would add to the ``DIMENSION`` list. That's why it is a list,
not a tuple.
"""

from __future__ import annotations

import copy
import functools
import math
import re
from abc import ABC, abstractmethod
from collections import UserDict, UserList
from html.parser import HTMLParser
from io import StringIO
from typing import Callable, Iterable, List, Mapping, Optional, Sequence, Tuple, TypeVar, Union

import numpy as np

_jed_resource = r'a-zA-Z0-9_.-'
_resource_re = re.compile(fr'''(\#)?                          # Allow leading '#' for a tag
                               ([{_jed_resource}]+:)?         # an optional namespace
                               ([/{_jed_resource}]+)          # the resource path
                               (\[[,=\s{_jed_resource}]*])?   # an optional state, such as "[facing=south]"
                            ''', re.VERBOSE)
_name_re = re.compile(r'[\w+.-]+')
_nbt_key_re = re.compile(r'[a-zA-Z0-9_:]+')
_nbt_path_re = re.compile(r'[-a-zA-Z0-9_.[\]{}:"]+')
_arg_re = re.compile(r'\$\(' + _nbt_path_re.pattern + r'\)')
_float_arg_re = re.compile(r'[-+]?[0-9.]*' + _arg_re.pattern + r'[0-9.]*')
_int_arg_re = re.compile(r'[-+]?[0-9]*' + _arg_re.pattern + r'[0-9]*')
_time_re = re.compile(r'([0-9]+(?:\.[0-9]+)?)([dst])?', re.IGNORECASE)
_backslash_re = re.compile(r'[\a\b\f\n\r\t\v]')
_backslash_map = {'\\': '\\', '\a': 'a', '\b': 'b', '\f': 'f', '\n': 'n', '\r': 'r', '\t': 't', '\v': 'v'}

# This works around a bug that component names _must_ be prefixed with "minecraft:" or another namespace. No other
# key requires this. Mojang thinks this is not a bug, but a "feature request". In either case, it is required. This
# expression is used to fix cases of this in nbt paths.

# Weird expression here, but trying to be clear -- using _jed_resource without using f-str to avoid confusion with
# the curly braces that must be in the pattern itself to allow [{foo:12}] syntax.
_component_fix_re = re.compile(r'(components)\.([REPL]+(\.|\[[0-9]|\[\{[^}]*}+]|$))'.replace('REPL', _jed_resource))

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

NONE = 'none'
CLOCKWISE_90 = 90
COUNTERCLOCKWISE_90 = 270
PLACE_ROTATIONS_GROUP = [NONE, ROTATION_0, CLOCKWISE_90, COUNTERCLOCKWISE_90]

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
TEXT_COLORS = [BLACK, DARK_BLUE, DARK_GREEN, DARK_AQUA, DARK_RED, DARK_PURPLE, GOLD, GRAY, DARK_GRAY, BLUE, GREEN, AQUA,
               RED, LIGHT_PURPLE, YELLOW, WHITE]
"""Valid colors for rich text."""

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

LT = '<'
LE = '<='
EQ = '='
GE = '>='
GT = '>'
RELATION = [LT, LE, EQ, GE, GT]


class Arg:
    """
    An argument for a macro command.
    """

    def __init__(self, name: str):
        if not name:
            raise ValueError('Arg must have actual name')
        self.name = as_nbt_path(name)

    def __str__(self):
        return f'$({self.name})'

    def __eq__(self, other: StrOrArg):
        if isinstance(other, str):
            return str(self) == other
        try:
            return self.name == other.name
        except AttributeError:
            return False

    def __hash__(self):
        return hash(self.name)


def de_arg(v: any) -> any:
    if not isinstance(v, str) and isinstance(v, Sequence):
        c = v.__class__
        # noinspection PyArgumentList
        v = c(de_arg(x) for x in v)
    return str(v) if isinstance(v, Arg) else v


def is_arg(v: any) -> bool:
    return isinstance(v, Arg) or (isinstance(v, str) and _arg_re.search(v))


def is_int_arg(v: any) -> bool:
    """Returns True if the value can be used where a number is needed; that is, either a number, an Arg object, or a string
    that contains a macro expansion that can be used as a number, such as '$(foo)' or ``17.($foo)``."""
    return (isinstance(v, int) and not isinstance(v, bool)) or isinstance(v, Arg) or (
            isinstance(v, str) and _int_arg_re.fullmatch(v) is not None)


def de_int_arg(v: any) -> any:
    """Returns True if the value can be used where a number is needed; that is, either a number, an Arg object, or a string
    that contains a macro expansion that can be used as a number, such as '$(foo)' or ``17.($foo)``."""
    if is_int_arg(v) and not isinstance(v, int):
        return str(v)
    return v


def check_int_arg(v: any) -> None:
    """Validates that ``is_num_arg(v)`` returns True, or if v is a collection, applies this test recursively."""
    if not isinstance(v, str) and isinstance(v, Iterable):
        for x in v:
            check_int_arg(x)
    else:
        if not is_int_arg(v):
            raise ValueError(f'{v}: Not an int or valid macro argument')
    return v


def is_float_arg(v: any) -> bool:
    """Returns True if the value can be used where a number is needed; that is, either a number, an Arg object, or a string
    that contains a macro expansion that can be used as a number, such as '$(foo)' or ``17.($foo)``."""
    return isinstance(v, float) or isinstance(v, Arg) or (isinstance(v, str) and _float_arg_re.fullmatch(v) is not None)


def de_float_arg(v: any) -> any:
    """Returns True if the value can be used where a number is needed; that is, either a number, an Arg object, or a string
    that contains a macro expansion that can be used as a number, such as '$(foo)' or ``17.($foo)``."""
    if is_float_arg(v) and not isinstance(v, float):
        return str(v)
    return v


def check_float_arg(v: any) -> None:
    """Validates that ``is_num_arg(v)`` returns True, or if v is a collection, applies this test recursively."""
    if not isinstance(v, str) and isinstance(v, Iterable):
        for x in v:
            check_float_arg(x)
    else:
        if not is_float_arg(v):
            raise ValueError(f'{v}: Not a float or valid macro argument')
    return v


def _quote(value):
    if isinstance(value, str):
        # If the string is a valid number, it needs to be quoted to be treated as a string
        try:
            float(value)
            return f'"{value}"'
        except ValueError:
            pass

        # If we don't quote these, the string "true" will become a boolean "true", etc.
        if re.fullmatch(r'true|false|\d+\.?\d*|\d*\.?\d+', value):
            return f'"{value}"'
        # $(foo) doesn't need to be quoted either.
        if not re.fullmatch(r'(\w+|\$\(\w+\))', value) or re.match(r'^\d', value):
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
    if is_arg(path):
        return str(path)
    parts = path.split(':', 1)
    if len(parts) > 1:
        as_resource(parts[0])
        path = parts[1]
    return path


def _strip_not(path):
    path = de_arg(path)
    if path and path[0] == '!':
        return path[1:]
    return path


def _not_ify(value: StrOrArg | Iterable[StrOrArg]) -> str | Tuple[str, ...]:
    if isinstance(value, StrOrArg):
        s = str(value)
        if not s.startswith('!'):
            s = '!' + s
        return s
    else:
        return tuple((_not_ify(x) for x in value))


def _bool(value: BoolOrArg | None) -> str | None:
    if value is None:
        return None
    if is_arg(value):
        return str(value)
    return str(value).lower()


def _float(value: FloatOrArg) -> str:
    if not isinstance(value, float) and is_float_arg(value):
        return str(value)
    return str(round(value, settings.float_precision))


def string(obj):
    """Returns the string value of obj. Most significantly, this uses str on iterable elements instead of repr."""
    if isinstance(obj, Iterable) and not isinstance(obj, str):
        return '(' + ', '.join(str(o) for o in obj) + ')'
    return str(obj)


def _ensure_size(lst: Iterable[any], size: int, fill=None) -> list:
    lst = _to_list(lst)
    if len(lst) > size:
        raise ValueError('Too many values in list')
    lst.extend([fill] * (size - len(lst)))
    return lst


def as_nbt_key(key: StrOrArg) -> StrOrArg:
    """Checks if the argument is a good NBT key. If not, it raises KeyError.

    :param key: The (probable) key.
    :return: the original input string.
    """
    if is_arg(key):
        return str(key)
    if not _nbt_key_re.fullmatch(key):
        raise KeyError(f'{key}: Invalid NBT key')
    return key


def as_nbt_path(path: StrOrArg | None) -> str | None:
    """
    Checks if the argument is a valid NBT path. This uses a heuristic that will catch many invalid paths, but by  no
    means all.
    """
    if path is None:
        return None
    if is_arg(path):
        return str(path)
    if not _nbt_path_re.fullmatch(path):
        raise ValueError(f'{path}: Invalid NBT path')
    sub = _component_fix_re.sub(r'\1.minecraft:\2', path)
    return sub


def as_resource(name: StrOrArg | None, allow_namespace=True, allow_not=False, add_namespace=False) -> str | None:
    """Checks if the argument is a valid resource name, or None. If not, it raises ValueError.

    :param name: The (probable) resource name.
    :param allow_namespace: Whether to allow a resource prefix such as 'minecraft:'...
    :param allow_not: Whether to allow a '!' before the name.
    :param: add_namespace: If no namespace is given, prepend 'minecraft:'
    :param add_namespace:
    :return: the input value.
    """
    if is_arg(name):
        return name
    if name is None:
        return None
    eval_name = name
    if allow_not:
        eval_name = _strip_not(eval_name)
    m = _resource_re.fullmatch(eval_name)
    if not m:
        raise ValueError(f'{eval_name}: Invalid resource')
    if not allow_namespace and m.group(2):
        raise ValueError(f'{eval_name}: Namespace given ({m.group(2)} but not allowed')
    if add_namespace and not m.group(2):
        name = f'minecraft:{name}'
    return name


def as_resources(*names: StrOrArg, allow_not=False) -> tuple[str, ...]:
    """Calls as_resource on each name.

    :param names: The (probable) resource names .
    :param allow_not: Whether to allow a '!' before any names.
    :return: the input names
    """
    for t in names:
        as_resource(t, allow_not=allow_not)
    return names


def as_resource_path(path: StrOrArg | None, allow_not=False) -> str | None:
    """Checks if the argument is a valid resource path, or None.

    :param path: The (probable) path.
    :param allow_not: Whether to allow a '!' before any names.
    :return: the input value.
    """
    if is_arg(path):
        return str(path)
    if path is None:
        return None
    orig = path
    if allow_not:
        path = _strip_not(path)
    path = _strip_namespace(path)
    if re.search('^//', path):
        raise ValueError(f'{orig}: Multiple leading "/"s in path')
    path = path.lstrip('/')
    if len(path) == 0:
        raise ValueError(f'{orig}: Invalid empty resource')
    for part in path.split('/'):
        try:
            as_resource(part, allow_namespace=False)
        except ValueError:
            raise ValueError(f'{part}: Invalid resource location in dir {path}')
    return orig


def as_item_stack(item: StrOrArg):
    """
    Checks if the argument is a valid item stack specification. This only checks the resource part of the item stack.

    :param item: The (probable) item stack.
    :return: the input value
    """
    if is_arg(item):
        return item
    resource, *_ = item.split('{')
    as_resource(resource)
    return item


def as_name(name: StrOrArg | None, allow_not=False) -> str | None:
    """Checks if the argument is a valid name, such as for a user, or None.

    :param name: The (probable) name.
    :param allow_not: Whether to allow a '!' before any names.
    :return: the input value.
    """
    if name is None:
        return None
    if is_arg(name):
        return str(name)
    orig = name
    if allow_not:
        name = _strip_not(name)
    if not _name_re.fullmatch(name) and not _arg_re.fullmatch(name):
        raise ValueError(f'{name}: Invalid name')
    return orig


def as_names(*names: StrOrArg, allow_not=False) -> tuple[str, ...]:
    """Calls as_name on each name

    :param names: The (probable) names.
    :param allow_not: Whether to allow a '!' before any names.
    :return: the input values.
    """
    for t in names:
        as_name(t, allow_not)
    return tuple(str(n) for n in names)


def as_column(col: IntColumn | StrOrArg) -> IntColumn | tuple[str]:
    """Checks if the argument is a valid column position.

    A valid column position is a tuple or list of two ints and/or IntRelCoords.

    :param col: The (probable) column position.
    :return: The input value.
    """
    col = de_arg(col)
    if isinstance(col, str):
        return (col,)
    if isinstance(col, (tuple, list)):
        if len(col) != 2:
            raise ValueError(f'{col}: Column must have 2 values')
        for c in col:
            if not isinstance(c, (int, IntRelCoord, Arg)):
                raise ValueError(f'{c}: not a coordinate')
        return col
    raise ValueError(f'{str(col)}: Invalid column position')


def as_angle(angle: Angle) -> Angle:
    """Checks if the angle is a valid one. "Valid" means a float or a tilde relative coordinate (such as ``~45``).

    An Arg is also valid.

    :param angle: The (probable) angle.
    :return: The input value.
    """
    angle = de_float_arg(angle)
    if isinstance(angle, (int, float, str)):
        return angle
    elif isinstance(angle, RelCoord):
        if angle.prefix != '~':
            raise ValueError(f'{angle.prefix}: Invalid angle prefix')
        return angle
    else:
        raise ValueError(f'{angle}: Invalid angle')


def as_yaw(angle: Angle | StrOrArg | None) -> Angle | None:
    # noinspection GrazieInspection
    """Checks if the angle is a valid yaw value, or None.

         "Valid" means a value that as_facing() or as_angle() accepts. If it is a number or RelCoord, it must be in
         the range [-180, 180).

        An Arg is also valid.

        :param angle: The (probable) yaw angle.
        :return: The input value.
        """
    if is_float_arg(angle):
        return de_float_arg(angle)
    if angle is not None:
        if isinstance(angle, str):
            angle = as_facing(angle).rotation[0]
        else:
            angle = as_angle(angle)
            yv = angle.value if isinstance(angle, RelCoord) else angle
            if not -180 <= yv < 180:
                raise ValueError(f'{yv}: must be in range [-180.0, 180.0)')
    return angle


def as_pitch(angle: Angle | None) -> Angle | None:
    """Checks if the angle is a valid pitch value, or None.

     "Valid" means a value that as_angle() accepts, and that is the range [-90, 90).

    An Arg is also valid.

    :param angle: The (probable) pitch angle.
    :return: The input value.
    """
    if is_float_arg(angle):
        return de_float_arg(angle)
    if angle is not None:
        angle = as_angle(angle)
        yv = angle.value if isinstance(angle, RelCoord) else angle
        if not -90 <= yv < 90:
            raise ValueError(f'{yv}: must be in range [-90.0, 90.0)')
    return angle


class TextHolder(ABC):
    """Base class for a holder of rich text."""

    @abstractmethod
    def content(self):
        """Returns the NBT content to put into a string."""
        pass


_VALID_NBT_ARRAY_TYPES = ('I', 'L', 'B')


def _as_array_type(elem_type):
    if not elem_type.upper() in _VALID_NBT_ARRAY_TYPES:
        raise ValueError(f'{elem_type}: Must be one of {_VALID_NBT_ARRAY_TYPES}')
    return elem_type.upper()


class Nbt(UserDict):
    MAX_LONG = 0x7fff_ffff_ffff_ffff
    MIN_LONG = -MAX_LONG - 1
    MAX_INT = 0x7fff_fff
    MIN_INT = -MAX_INT - 1
    MAX_SHORT = 0x7fff
    MIN_SHORT = -MAX_SHORT - 1
    MAX_BYTE = 0x7f
    MIN_BYTE = -MAX_BYTE - 1
    MAX_ULONG = 0xffff_ffff_ffff_ffff
    MIN_ULONG = 0
    MAX_UINT = 0xffff_fff
    MIN_UINT = 0
    MAX_USHORT = 0xffff
    MIN_USHORT = 0
    MAX_UBYTE = 0xff
    MIN_UBYTE = 0

    MAX_FLOAT_VALUE = +3.4e+38
    MIN_FLOAT_VALUE = 1.401298e-45
    MIN_FLOAT_NORMAL = 1.175494e-38
    MAX_FLOAT_EXPONENT = -126
    MIN_FLOAT_EXPONENT = 127
    MAX_DOUBLE_VALUE = 1.797693e+308
    MIN_DOUBLE_VALUE = 4.900000e-324
    MIN_DOUBLE_NORMAL = 2.225074e-308
    MAX_DOUBLE_EXPONENT = -1022
    MIN_DOUBLE_EXPONENT = 1023

    """A simple NBT handling class, that models NBT values as a python dictionary.

    You can set the value of a key directly to any valid value. By default, the value of a key will be an Nbt object.

    The string representation is particularly tricky. Most NBT is simple key/value pairs, where values are booleans,
    ints, floats, strings, or more NBT. A few places use rich text (formerly JSON text). These keys (such as a sign's Text fields) must be
    presented as rich text. Those keys are special-cased in this code. You can also put a Text value for a field
    to have it treated as rich text.

    No attempt is made to validate the NBT against expected values, such as whether a ``Rotation`` value is a list of
    two floats or something else.
    """
    use_spaces = True
    """Whether to put spaces after colons and commas."""
    sort_keys = True
    """Whether to output keys in sorted order."""

    class TypedArray(UserList):
        # noinspection PyShadowingBuiltins
        def __init__(self, type: str, init_list=None):
            super().__init__(init_list)
            self.type = _as_array_type(type)

        def __str__(self):
            sout = StringIO()
            Nbt._to_str(self, sout)
            return str(sout.getvalue())

    _forced_type_tags = {'Motion': 'd', 'Rotation': 'f',
                         'LeftArm': 'f', 'RightArm': 'f', 'LeftLeg': 'f', 'RightLeg': 'f', 'Head': 'f', 'Body': 'f'}

    def clone(self):
        """Returns a deep copy of this Nbt"""
        return copy.deepcopy(self)

    def __setitem__(self, key, value):
        if isinstance(value, tuple):
            value = list(value)
        elif isinstance(value, Mapping) and not isinstance(value, (Nbt, TextHolder)):
            value = Nbt.as_nbt(value)
        super().__setitem__(as_nbt_key(key), value)

    def __str__(self):
        sout = StringIO()
        Nbt._to_str(self, sout)
        return str(sout.getvalue())

    def __missing__(self, key):
        nbt = Nbt()
        self[key] = nbt
        return nbt

    def set_or_clear(self, path: str, v: any) -> Nbt:
        """
        If `v` is `None` or `False`, remove `path` from the nbt; otherwise set the value at `path` to be `v`.
        """
        path = path.split('.')
        if v is None or (isinstance(v, bool) and not v):
            part = self
            for p in path[:-1]:
                if p not in part:
                    return self
                part = part[p]
            part.pop(path[-1])
        else:
            part = self
            for p in path[:-1]:
                part = part[p]
            part[path[-1]] = v
        return self

    def set_if(self, key: str, value: object, *args) -> Nbt:
        """Set values if they aren't None. The first key/value pair is required, more can be given."""
        if value is not None:
            self[key] = value
        for i in range(0, len(args), 2):
            if args[i + 1] is not None:
                self[args[i]] = args[i + 1]
        return self

    @classmethod
    def to_int(cls, string) -> int:
        lc_string = string.lower()
        m = re.fullmatch(r'([-+])?(0[xb])?([0-9a-f_]+)([su])?([bsil])?', lc_string)
        if not m:
            raise ValueError(f'{string}: Not an integer')
        sign, base_spec, num, signed, type = m.groups()
        base = 16 if base_spec == '0x' else 2 if base_spec == '0b' else 10
        num = int(num, base)
        # disambiguation
        if signed == 's' and not type:
            type = 's'
            signed = None
        if sign == '-':
            num = -num
        if signed:
            if not type:
                raise ValueError(f'{string}: Type suffix required after signed-ness suffix')
        if signed == 'u' and num < 0:
            raise ValueError(f'{string}: unsigned ints cannot be negative')
        if not type:
            # without a known type, we can't do any other checks
            return num

        signed_ranges = {'b': (Nbt.MIN_BYTE, Nbt.MAX_BYTE + 1), 's': (Nbt.MIN_SHORT, Nbt.MAX_SHORT + 1),
                         'i': (Nbt.MIN_INT, Nbt.MAX_INT + 1), 'l': (Nbt.MIN_LONG, Nbt.MAX_LONG + 1)}
        unsigned_ranges = {'b': (Nbt.MIN_UBYTE, Nbt.MAX_UBYTE + 1), 's': (Nbt.MIN_USHORT, Nbt.MAX_USHORT + 1),
                           'i': (Nbt.MIN_UINT, Nbt.MAX_UINT + 1), 'l': (Nbt.MIN_ULONG, Nbt.MAX_ULONG + 1)}
        ranges = unsigned_ranges if signed == 'u' else signed_ranges
        if num not in range(*ranges[type]):
            raise ValueError(f'{string}: Outside range of type "{type}"')
        # This is just getting the twos-complement stuff right: An unsigned value above the signed max for a type is
        # a negative value of that type.
        if signed_ranges[type][1] <= num < unsigned_ranges[type][1]:
            num -= unsigned_ranges[type][1]
        return num

    @classmethod
    def to_float(cls, string) -> float:
        lc_string = string.lower()
        m = re.fullmatch(r'([-+]?(?:[0-9_]+)?\.?(?:[0-9_]+)?(?:e-?[0-9]+)?)([df]?)', lc_string)
        if not m:
            raise ValueError(f'{string}: Not a float')
        num, type = m.groups()
        if not num or num == '-':
            raise ValueError(f'{string}: Not a float')
        num = float(num)
        ranges = {'f': (Nbt.MIN_FLOAT_VALUE, Nbt.MAX_FLOAT_VALUE), 'd': (Nbt.MIN_DOUBLE_VALUE, Nbt.MAX_DOUBLE_VALUE)}
        if type and abs(num) not in range(*ranges[type]):
            raise ValueError(f'{string}: Outside range of type "{type}"')
        return num

    @classmethod
    def to_str(cls, obj) -> str:
        """
        Returns a string version of what is passed, using str() instead of repr() for dict and iterables. Because
        str(dict), str(list), etc., use repr(), not str().
        """
        if is_arg(obj):
            return _quote(str(obj))
        if isinstance(obj, cls):
            return str(obj)
        if isinstance(obj, Mapping) and not isinstance(obj, TextHolder):
            return str(cls.as_nbt(obj))
        sout = StringIO()
        cls._to_str(obj, sout, False)
        return str(sout.getvalue())

    @classmethod
    def as_nbt(cls, nbt: NbtDef | str) -> Nbt | str:
        """Returns the input argument as an Nbt, including making a copy of an Nbt object that is passed in."""
        if is_arg(nbt):
            return str(nbt)
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
        quote = ':' in key
        if quote:
            sout.write('"')
        sout.write(key)
        if quote:
            sout.write('"')
        sout.write(':')

    @classmethod
    def _to_str(cls, elem, sout, force_type=None, components_child=False):
        if isinstance(elem, (Nbt, dict)):
            sout.write('{')
            keys = elem.keys()
            if Nbt.sort_keys:
                # noinspection PyTypeChecker
                keys = sorted(keys, key=str.casefold)
            first = True
            for key in keys:
                value = elem[key]
                first = cls._comma(first, sout)
                # See comment for _component_fix_re; this is a different part of that, which works unless the Nbt
                # being stringed will be used as a child of a 'components' that is not present in this Nbt itself.
                if components_child and not re.match('^[a-z_0-9]+:', key):
                    cls._write_key('minecraft:' + key, sout)
                else:
                    cls._write_key(key, sout)
                cls._space(sout)
                is_components = key in ('components', 'minecraft:components')
                # This isn't quite strictly what sort_keys means, but tag order isn't significant, so this is helpful.
                if key == 'Tags' and isinstance(value, list) and Nbt.sort_keys:
                    value.sort()
                if key in cls._forced_type_tags:
                    cls._to_str(value, sout, force_type=cls._forced_type_tags[key],
                                components_child=is_components)
                else:
                    cls._to_str(value, sout, force_type, components_child=is_components)
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
        elif is_arg(elem):
            sout.write(_quote(de_arg(elem)))
        elif isinstance(elem, str):
            sout.write(_quote(elem))
        elif isinstance(elem, (list, tuple, UserList)):
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
            if elem > 0xffff_ffff:
                sout.write('L')
        else:
            sout.write(_quote(str(elem)))

    def merge(self, nbt: NbtDef | None) -> Nbt:
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
            assert isinstance(value, (list, Arg)), f'{key}: Expected list value, got {value}'
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


class _ToText(HTMLParser):
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

    def text(self) -> list:
        return self.out

    def __str__(self):
        return Nbt.to_str(self.out)


class Settings:
    """Manage general settings. Use the 'settings' variable to adjust the settings."""

    def __init__(self):
        self._float_precision = 3
        self._handlers = set()

    @property
    def float_precision(self) -> int:
        """The number of decimal places will be shown for floats."""
        return self._float_precision

    @float_precision.setter
    def float_precision(self, precision: int):
        if precision < 1:
            raise ValueError(f'{precision}: Precision must be positive')
        self._float_precision = precision


settings = Settings()


def to_id(name: StrOrArg) -> str:
    """
    Returns an ID from the passed-in name. If it's already an ID, it is just returned. Otherwise, it lower-cases the
    name, and replaces both ' ' and '| with '_'.
    """
    if is_arg(name):
        return str(name)
    return re.sub(r'\s+|\'|\|', '_', name.strip().lower())


def to_name(id: StrOrArg) -> str:
    """
    Returns a user-friendly name from the passed-in ID. It just replaces '_' with spaces and title-cases the result.
    """
    if is_arg(id):
        return str(id)
    return id.replace('_', ' ').title()


# noinspection PyShadowingNames
@functools.total_ordering
class RelCoord:
    """A relative coordinate. These are shown in minecraft commands with special annotation, such as '~1' or '^2'."""

    def __init__(self, prefix: str, v: FloatOrArg):
        self.prefix = prefix
        self.value = v
        self._rep = prefix + (str(v) if is_arg(v) else _float(v))

    def _v(self: U, v: float) -> U:
        if isinstance(v, int):
            return IntRelCoord(self.prefix, v)
        else:
            return RelCoord(self.prefix, v)

    def __round__(self, n=None):
        return round(self.value, n)

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
            if other.prefix != self.prefix:
                raise ValueError(
                    f'{other}: right hand operator to - must be the same type of coord as the left, or a number')
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

    def __neg__(self: U) -> U:
        return self._v(-self.value)

    def __pos__(self: U) -> U:
        return self

    # The specific tuple sizes help type checking since some things that will consume the output expect specifics
    @classmethod
    def add(cls, v1: Sequence[Coord, ...] | None, v2: Sequence[Coord, ...] | None) -> tuple[Coord, ...] | tuple[
        Coord, Coord] | tuple[Coord, Coord, Coord] | None:
        """Returns ``v1 + v2``. If either is None, the result is the other."""
        return cls.merge(lambda v1, v2: v1 + v2, v1, v2)

    @classmethod
    def sub(cls, v1: Sequence[Coord, ...] | None, v2: Sequence[Coord, ...] | None) -> tuple[Coord, ...] | tuple[
        Coord, Coord] | tuple[Coord, Coord, Coord] | None:
        """Returns ``v1 - v2``. If either is None, the result is the other."""
        return cls.merge(lambda v1, v2: v1 - v2, v1, v2)

    @staticmethod
    def merge(op: Callable[[Coord, Coord], Coord], v1: Sequence[Coord, ...] | None,
              v2: Sequence[Coord, ...] | None) -> tuple[Coord, ...] | tuple[Coord, Coord] | tuple[
        Coord, Coord, Coord] | None:
        """
        Returns the result of invoking op on each element of the vectors. If either vector is None, the result is the
        other.
        """
        if v1 is None:
            return v2
        elif v2 is None:
            return v1
        if len(v1) != len(v2):
            raise ValueError('Not the same length')
        return tuple(op(v1[i], v2[i]) for i in range(len(v1)))

    @staticmethod
    def coords(coord: RelCoord | int | float, *coords: RelCoord | int | float):
        if len(coords) == 0:
            return str(coord)
        s = f'({coord}'
        for c in coords:
            s += f', {c}'
        return s + ')'


U = TypeVar('U', bound=RelCoord)


class IntRelCoord(RelCoord):
    """A relative coordinate that has no fractional part."""

    def __init__(self, prefix: str, v: int):
        super().__init__(prefix, int(v))


def _rel_coord(ch, f, values: Sequence[float]) -> RelCoord | Tuple[RelCoord, ...]:
    if len(values) == 1:
        v = values[0]
        return IntRelCoord(ch, v) if isinstance(v, int) else RelCoord(ch, v)
    return tuple(f(x) for x in values)


def r(*v: FloatOrArg | Iterable[FloatOrArg]) -> RelCoord | IntRelCoord | Tuple[RelCoord, RelCoord] | \
                                                Tuple[IntRelCoord, IntRelCoord] | Tuple[RelCoord, RelCoord, RelCoord] | \
                                                Tuple[RelCoord, ...]:
    """
    Returns a single or tuple '~' relative coordinate(s) of its input value(s). If all values are integers,
    the value(s) will be IntRelCoords.
    """
    return _rel_coord('~', r, tuple(v))


relative = r
"""Verbose name for r()."""


def d(*v: float | Iterable[float]) -> RelCoord | IntCoord | Tuple[RelCoord, RelCoord] | \
                                      Tuple[IntRelCoord, IntRelCoord] | Tuple[RelCoord, RelCoord, RelCoord] | \
                                      Tuple[RelCoord, ...]:
    """
    Returns a single or tuple '^' relative coordinate(s) of its input value(s). If all values are integers,
    the value(s) will be IntRelCoords.
    """
    return _rel_coord('^', d, tuple(v))


delta_from = d
"""Verbose name for d()."""


def days(num: float) -> TimeSpec:
    """Returns a specification for the given number of days."""
    return TimeSpec(f'{num}d')


def seconds(num: float) -> TimeSpec:
    """Returns a specification for the given number of seconds."""
    return TimeSpec(f'{num}s')


def ticks(num: float) -> TimeSpec:
    """Returns a specification for the given number of ticks."""
    return TimeSpec(num)


def _int_or_float(value: int | float) -> int | float:
    """Returns the input value as an int if that looses no information."""
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

    def __eq__(self, other):
        return self.ticks == other.ticks

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


def _sign(v: float | int) -> int:
    return -1 if v < 0 else 0 if v == 0 else 1


class Facing:
    """This class represents information about facing in a given direction."""

    def __init__(self, name: str, delta: Tuple[float, float, float], rotation: Tuple[float, float], number: int,
                 h_number: int = None, painting_number: int = None):
        """Creates a Facing object.

        :param name: The name of the direction, such as ``NORTH`` or ``SW``.
        :param delta: The amount to add to coordinates to move in the direction.
        :param rotation: The values to use as a ``Rotation`` NBT value.
        :param number: The number used by most blocks and entities for this rotation, or NaN if none. 0 is up, etc.
        :param: h_number: The number used by entities that only can be horizontal, that is, paintings. 0 is north, etc.
        :param: painting_number: The number used by paintings.
        """
        self.delta = delta
        self.name = name
        self.rotation = rotation
        self.number = number
        self.h_number = h_number
        self.painting_number = painting_number

    @property
    def sign_rotation(self):
        return self.h_number

    def __str__(self):
        return self.name

    def __eq__(self, other):
        other = as_facing(other)
        return self.rotation == other.rotation

    def __hash__(self):
        return hash(self.name)

    @property
    def yaw(self) -> int | float:
        """The yaw (first) value of the rotation."""
        return self.rotation[0]

    @property
    def pitch(self) -> int | float:
        """The pitch (second) value of the rotation."""
        return self.rotation[1]

    @property
    def dx(self) -> int | float:
        """The X (first) value of the delta."""
        return self.delta[0]

    @property
    def dy(self) -> int | float:
        """The Y (second) value of the delta."""
        return self.delta[1]

    @property
    def dz(self) -> int | float:
        """The Z (third) value of the delta."""
        return self.delta[2]

    def scale(self, scale: float) -> Tuple[float, float, float]:
        """Returns the motion vector scaled by a value."""
        return self.dx * scale, self.dy * scale, self.dz * scale

    def move(self, start: Tuple[Coord, Coord, Coord], distance: int) -> Tuple[Coord, Coord, Coord]:
        return (
            start[0] + distance * self.delta[0],
            start[1] + distance * self.delta[1],
            start[2] + distance * self.delta[2]
        )

    @property
    def block_delta(self) -> list[int]:
        res = []
        for x in self.delta:
            res.append(_sign(x))
        return res

    def turn(self, rotated_by: int):
        """
        Returns a Facing that is this one rotating by the specified amount. Must be a multiple of 90 or one of the
        ROTATION constants.

        For example ``turn(NORTH, ROTATION_90)`` is ``EAST``. This allows your code to use relative operations, such as
        placing a sign to the right of an entity, no matter which way it is facing."""
        rot = int(_in_group(ROTATIONS, rotated_by) / 90)
        if self.name in DIRECTIONS:
            rotation_aid = DIRECTIONS + DIRECTIONS
        else:
            rotation_aid = SIGN_DIRECTIONS + SIGN_DIRECTIONS
            rot *= 4
        return as_facing(rotation_aid[rotation_aid.index(self.name) + rot])


_facing = {
    NORTH: Facing(NORTH, (0, 0, -1), (180.0, 0.0), 2, 0, 2),
    EAST: Facing(EAST, (1, 0, 0), (270.0, 0.0), 5, 1, 3),
    SOUTH: Facing(SOUTH, (0, 0, 1), (0.0, 0.0), 3, 2, 0),
    WEST: Facing(WEST, (-1, 0, 0), (90.0, 0.0), 4, 3, 1),
    UP: Facing(UP, (0, 1, 0), (0.0, 270.0), 1, None),
    DOWN: Facing(DOWN, (0, -1, 0), (0.0, 90.0), 0, None)
}
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
        _facing[__r].h_number = __i
        _facing[__i] = _facing[__r]
    elif __i in _facing:
        # This affects only zero.
        _facing[__i].h_number = __i
        _facing[__r] = _facing[__i]
        if isinstance(__r, (int, float)):
            _facing[int(__r)] = _facing[__i]
    else:
        __deg = round((__i * 22.5 + 720) % 360, 1)
        __angle = math.radians(__deg)
        # noinspection PyTypeChecker
        _facing[__r] = Facing(__r, (-math.sin(__angle), 0, math.cos(__angle)), ((720 + __deg) % 360, 0), math.nan, __i)
        _facing[__i] = _facing[__r]
        _facing[round(2 * __deg) / 2] = _facing[__r]

_facing_info = {NORTH: (0, -1, 0), EAST: (1, 0, 270), SOUTH: (0, 1, 180), WEST: (-1, 0, 90)}


def _in_group(group: list | tuple, name: StrOrArg | int | None, allow_none=True):
    if allow_none and name is None:
        return name
    if is_arg(name):
        return name

    if name not in group:
        raise ValueError(f'{name}: Not in {group}')
    return name


def rotate_facing(facing: FacingDef, rotated_by: int) -> Facing:
    """Returns the value of turn(rotated_by) invoked on facing, or on as_facing(facing).

    For example ``rotated_facing(NORTH, ROTATION_90)`` is ``EAST``. This allows your code to use relative operations,
    such as placing a sign to the right of an entity, no matter which way it is facing."""
    return as_facing(facing).turn(rotated_by)


def as_facing(facing: FacingDef) -> Facing:
    """Checks if the argument is a valid 'facing' specification.

    "Valid" means a Facing object, a known direction name, or a valid sign direction (see as_sign_facing()).

    :param facing: The (probable) facing specification.
    :return: the appropriate Facing object.
    """
    if isinstance(facing, Facing):
        return facing
    if isinstance(facing, str):
        return _facing[facing.lower()]
    return _facing[facing]


def as_duration(duration: DurationDef | None) -> TimeSpec | str | None:
    """Checks if the argument is a valid duration specification, or None.

    If the input is None, it is returned. Otherwise, this returns Duration(duration).
    """
    if is_arg(duration):
        return str(duration)
    if duration is None or isinstance(duration, TimeSpec):
        return duration
    return TimeSpec(duration)


def is_number(v: any) -> bool:
    return isinstance(v, (float, int)) and not isinstance(v, bool)


def as_range(spec: Range) -> str:
    """Checks if the argument is a valid numeric range.

    "Valid" means a single number, or a two-element list or tuple of numbers defining the endpoints. Any of these may
    also be a numeric macro argument, as defined by the is_num_arg() method. One of the endpoints may be None to
    define an open-ended range.

    :param spec: The (probable) range.
    :return: A string for the range, either a single number or a range using '..' between the two numbers, one of which can be None.
    """
    if not isinstance(spec, Sequence) or isinstance(spec, str):
        spec = [spec]

    results = []
    for i, v in enumerate(spec):
        if is_float_arg(v) or is_number(v) or v is None:
            results.append('' if v is None else v)
        else:
            raise ValueError(f'{spec}: Must be a number or a number-valid macro')
    if len(results) == 1:
        return str(results[0])
    if isinstance(results[0], (float, int)) and isinstance(results[1], (float, int)) and results[0] > results[1]:
        raise ValueError('Start is greater than end')
    return f'{results[0]}..{results[1]}'


class Transform:
    # This is overwritten later, but without this Pycharm doesn't know about this class variable
    IDENTITY = None

    class Matrix:
        def __init__(self,
                     value: tuple[
                                float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float] |
                            tuple[
                                tuple[float, float, float, float],
                                tuple[float, float, float, float],
                                tuple[float, float, float, float],
                                tuple[float, float, float, float]]):
            if isinstance(value[0], Sequence):
                value = tuple((i for i in row) for row in value)
            self.value = value

        def nbt(self) -> tuple[
            float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float]:
            return self.value

    class Quaternion:
        @staticmethod
        def _nbt_quat(quat):
            if isinstance(quat[1], tuple):
                return Nbt(angle=quat[0], axis=quat[1])
            return quat

        def __init__(self,
                     right: tuple[float, float, float, float] | tuple[float, tuple[float, float, float]] | FacingDef,
                     scale: float | tuple[float, float, float] = 1,
                     left: tuple[float, float, float, float] | tuple[
                         float, tuple[float, float, float]] | FacingDef = None,
                     translation: tuple[float, float, float] = None):
            self.right = self._canonicalize(right)
            self.scale = scale if isinstance(scale, Sequence) else (scale, scale, scale)
            self.left = self._canonicalize(left)
            self.translation = translation if translation else (0, 0, 0)

        def nbt(self) -> Nbt:
            return Nbt({'right_rotation': self._nbt_quat(self.right), 'scale': self.scale,
                        'left_rotation': self._nbt_quat(self.left), 'translation': self.translation})

        @staticmethod
        def _canonicalize(rot):
            if rot is None:
                return 0, 0, 0, 1
            if isinstance(rot, tuple):
                return rot
            facing = as_facing(rot)
            # Normally you would think of roll as always zero, because that's how the doc describes it. But that's
            # based on a starting posture of being upright facing south, where these terms are usually based on looking
            # down at a plane from above. Given that, these are the correct interpretations of the Rotation attribute.
            # See https://automaticaddison.com/how-to-convert-euler-angles-to-quaternions-using-python/ for the
            # calculations.
            roll = math.radians(facing.rotation[1])
            pitch = math.radians(-facing.rotation[0])
            yaw = 0
            x = np.sin(roll / 2) * np.cos(pitch / 2) * np.cos(yaw / 2) - np.cos(roll / 2) * np.sin(pitch / 2) * np.sin(
                yaw / 2)
            y = np.cos(roll / 2) * np.sin(pitch / 2) * np.cos(yaw / 2) + np.sin(roll / 2) * np.cos(pitch / 2) * np.sin(
                yaw / 2)
            z = np.cos(roll / 2) * np.cos(pitch / 2) * np.sin(yaw / 2) - np.sin(roll / 2) * np.sin(pitch / 2) * np.cos(
                yaw / 2)
            w = np.cos(roll / 2) * np.cos(pitch / 2) * np.cos(yaw / 2) + np.sin(roll / 2) * np.sin(pitch / 2) * np.sin(
                yaw / 2)
            return x, y, z, w

    def __init__(self, transform: Matrix | Quaternion):
        super().__init__()
        self.value = transform

    def nbt(self):
        return self.value.nbt()

    @staticmethod
    def matrix(value: tuple[
                          float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float] |
                      tuple[
                          tuple[float, float, float, float],
                          tuple[float, float, float, float],
                          tuple[float, float, float, float],
                          tuple[float, float, float, float]]):
        return Transform(Transform.Matrix(value))

    @staticmethod
    def quaternion(right: tuple[float, float, float, float] | tuple[float, tuple[float, float, float]] | FacingDef,
                   scale: float | tuple[float, float, float] = 1,
                   left: tuple[float, float, float, float] | tuple[
                       float, tuple[float, float, float]] | FacingDef = None,
                   translation: tuple[float, float, float] = None):
        return Transform(Transform.Quaternion(right, scale, left, translation))


Transform.IDENTITY = Transform.quaternion((0, 0, 0, 1), 1, (0, 0, 0, 1))

BoolOrArg = Union[bool, Arg]
IntOrArg = Union[int, Arg, str]
FloatOrArg = Union[int, float, Arg, str]
StrOrArg = Union[str, Arg]

NbtDef = Union[Nbt, Mapping]
FacingDef = Union[int, float, str, Facing]
DurationDef = Union[StrOrArg, FloatOrArg, TimeSpec]
Coord = Union[FloatOrArg, RelCoord]
Angle = Union[FloatOrArg, StrOrArg, RelCoord]
IntCoord = Union[IntOrArg, IntRelCoord]
Position = Union[Tuple[Coord, Coord, Coord], List[Coord]]
XYZ = Tuple[FloatOrArg, FloatOrArg, FloatOrArg]
Column = Tuple[Coord, Coord]
IntColumn = Tuple[IntCoord, IntCoord]
Range = Union[FloatOrArg, Tuple[Optional[FloatOrArg], Optional[FloatOrArg]]]
