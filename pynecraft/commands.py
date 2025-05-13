"""
Mechanisms for writing Minecraft commands in python. The idea is twofold:

1. To allow syntax checking and other regular language tooling for checking the commands.
2. To provide simplified syntax. Some of that is here, and some in the simpler package.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from urllib.parse import urlparse

from .values import DUMMY, SCORE_CRITERIA_GROUP, as_advancement, as_enchantment, as_gamerule, as_particle, \
    as_teamoption, enchantments, game_rules, team_options

if TYPE_CHECKING:
    pass

import copy
import dataclasses
import functools
import re
import struct
import textwrap
from abc import ABC
from collections import UserList
from functools import wraps
from pathlib import Path
from typing import Callable, Iterable, Mapping, Tuple, TypeVar, Union

from .base import Angle, BLUE, CLOCKWISE_90, COLORS, COUNTERCLOCKWISE_90, Column, DIMENSION, DurationDef, EQ, GREEN, \
    IntColumn, IntRelCoord, \
    NONE, Nbt, NbtDef, PINK, PURPLE, Position, RED, RELATION, Range, RelCoord, TEXT_COLORS, TIME_SPEC, TIME_TYPES, \
    TextHolder, \
    WHITE, \
    YELLOW, \
    _ToText, _bool, _ensure_size, _float, _in_group, _not_ify, _quote, _to_list, as_column, \
    as_duration, as_facing, as_item_stack, as_name, as_names, as_nbt_path, as_pitch, as_range, as_resource, \
    as_resource_path, as_resources, as_yaw, de_arg, de_float_arg, de_int_arg, is_arg, is_int_arg, to_id, to_name, \
    FacingDef, Facing, \
    Arg, \
    StrOrArg, IntOrArg, \
    BoolOrArg, FloatOrArg, _arg_re


def _fluent(method):
    @wraps(method)
    def inner(self, *args, **kwargs):
        obj = copy.deepcopy(self)
        return method(obj, *args, **kwargs)

    return inner


def as_biome(biome: StrOrArg, allow_not: bool = False) -> str:
    """
    Returns a string version of the given biome. A string version is preferred because new biome types can be added
    by datapacks.
    """
    if is_arg(biome):
        return de_arg(biome)
    return as_resource(biome, allow_not=allow_not)


def as_single(target: Target) -> TargetSpec | str | None:
    orig = target
    if target is None:
        return None
    target = as_target(target)
    if isinstance(target, TargetSpec) and not target.is_single():
        raise ValueError(f'{str(orig)}: Not a single target')
    return target


def as_target(target: Target) -> TargetSpec | str | None:
    """
    Checks if the argument is a valid target for commands, such as (the equivalent of) '@p' or usernames,
    or None. If not, it raises a ValueError.

    Valid targets are subclasses of TargetSpec, a '*', or a user name.

    :param target: The (probable) target.
    :return: a TargetSpec object, created if need be, or None.
    """
    if target is None:
        return None
    if is_arg(target):
        return str(target)
    if isinstance(target, TargetSpec):
        return target
    elif target == '*':
        return Star()
    else:
        try:
            return User(target)
        except TypeError:
            raise ValueError(f'{target}: Invalid target')


def as_data_target(target: DataTarget | None) -> DataTargetBase | None:
    """
    Checks if the argument is a valid data target for commands like ``data merge``, or None. If not,
    it raises ValueError.

    A tuple or list argument is presumed to be intended as a position on which as_position will be called; a
    TargetSpec is an entity target, and a string is presumed to be intended as a resource path.

    :param target: The (probable) data target.
    :return: A tuple, whose first value is 'block', 'entity', or 'storage', and whose second element is an appropriate
        object: the result of as_position for 'block', the TargetSpec input for 'entity', the result of
        as_resource_path() on a string. A None argument returns None.
    """
    return _as_data_target(target, as_target)


def as_data_single(target: DataTarget | None) -> DataTargetBase | None:
    """Like as_data_target, but an entity target must be a single target"""
    return _as_data_target(target, as_single)


def _as_data_target(target: DataTarget | None, validater: Callable) -> DataTargetBase | None:
    if target is None:
        return None
    if isinstance(target, DataTargetBase):
        return target
    if isinstance(target, (tuple, list)):
        return block(target)
    if isinstance(target, TargetSpec):
        return entity(validater(target))
    if isinstance(target, str) and not is_arg(target):
        return storage(target)
    raise ValueError(f'{target}: Invalid data target (must be position, entity selector, or resource name)')


def data_target_str(data_target: DataTarget) -> str:
    """Returns a single string for a target, as returned by as_data_target.

    :param data_target: The data target.
    :return: A single string, such as 'block 1 2 3'.
    """
    target = as_data_target(data_target)
    return str(target)


def data_single_str(data_target: DataTarget) -> str:
    """Like data_target_str(), but requires a single target."""
    target = as_data_single(data_target)
    return str(target)


def _as_target_spec(target: DataTarget, single=False) -> str:
    if not isinstance(target, DataTargetBase):
        if isinstance(target, tuple):
            target = block(target)
        elif isinstance(target, TargetSpec):
            target = entity(target, single=single)
        elif isinstance(target, str) and not is_arg(str):
            target = storage(target)
        else:
            raise TypeError(f'Data Target cannot be deduced: Invalid type: {type(target)}')
    return str(target)


def as_position(pos: Position | StrOrArg) -> Position | str:
    """Checks if the argument is a valid position.

    A valid position is a tuple or list of three numbers and/or RelCoords.

    :param pos: The (probable) position.
    :return: The input value.
    """
    if is_arg(pos):
        return str(pos)
    if isinstance(pos, tuple):
        if len(pos) != 3:
            raise ValueError(f'{pos}: Position must have 3 values')
        for c in pos:
            if not isinstance(c, (int, float, IntRelCoord, RelCoord)) and not is_arg(c):
                raise ValueError(f'{c}: not a coordinate')
        return pos
    raise ValueError(f'{str(pos)}: Invalid position')


def as_user(name: StrOrArg) -> str:
    """Checks if the argument is a valid username.

    :param name: The (probable) user name.
    :return: The input value.
    """
    if is_arg(name):
        return str(name)
    if not re.fullmatch(r'\w+', name):
        raise ValueError(f'{name}: Invalid user name')
    return name


def as_uuid(uuid: StrOrArg) -> str:
    """Checks if the string is a valid UUID as four numbers separated by dashes.

    :param uuid: The (probable) uuid.
    :return: the input value.
    """
    if is_arg(uuid):
        return str(uuid)
    if not re.fullmatch(r'(?:[a-fA-F0-9]+-){3}[a-fA-F0-9]+', uuid):
        raise ValueError(f'{uuid}: Invalid UUID string')
    return uuid


def as_team(team: StrOrArg) -> str | None:
    """Checks if the argument is a valid team name, or None.

    :param team: The (probable) team name.
    :return: The input value.
    """
    if is_arg(team):
        return str(team)
    if team is None:
        return team
    if not re.fullmatch(r'[\w+.-]{1,16}', team):
        raise ValueError(f'{team}: Invalid team name')
    return team


def as_block(block: BlockDef | None) -> Block | str | None:
    """Checks if the argument is a valid block specification, or None.

    "Valid" means a string block name, or valid arguments to the Block constructor.

    An Arg is also valid.

    :param block: The (probable) block.
    :return: A Block object for the argument, or None.
    """
    if is_arg(block):
        return str(block)
    if block is None:
        return None
    if isinstance(block, str):
        return Block(block)
    if isinstance(block, Iterable):
        return Block(*block)
    return block


def as_entity(entity: EntityDef | None) -> Entity | Arg | None:
    """Checks if the argument is a valid entity specification, or None.

    "Valid" means a string entity name, or valid arguments to the Entity constructor.

    An Arg is also valid.

    :param entity: The (probable) entity
    :return: an Entity object for the argument, or None.
    """
    if is_arg(entity):
        return entity
    if entity is None:
        return None
    if isinstance(entity, str):
        return Entity(entity)
    if isinstance(entity, Iterable):
        return Entity(*entity)
    return entity


def as_score(score: ScoreName | None) -> Score | None:
    """Checks if the argument is a valid score, or None.

    "Valid" means a Score object, or a target/objective pair in a tuple or list.

    :param score: The (probable) score.
    :return: A Score object, or None.
    """
    if score is None:
        return None
    if isinstance(score, Score):
        return score
    if not isinstance(score, str):
        return Score(score[0], score[1])
    raise ValueError(f'{str(score)}: Invalid score')


_single_slot_re = r'[a-z]+(\.([a-z]+))*(\.[0-9]+|\.\*)?'
_SLOT_RE = re.compile(_single_slot_re + rf'(-{_single_slot_re})?')


def as_slot(slot: StrOrArg | None) -> str | None:
    """Checks if the argument is a valid slot specification, or None.

    "Valid" means valid for the ``item`` command.

    An Arg is also valid.

    :param slot: The (probable) slot name.
    :return: The input value.
    """
    if is_arg(slot):
        return str(slot)
    if slot is None:
        return None
    if not _SLOT_RE.fullmatch(slot):
        raise ValueError(f'{slot}: Bad slot specification')
    return slot


def as_criteria(criteria):
    if re.fullmatch(r'(teamkill|killedByTeam)\.[a-z_]+', criteria):
        return criteria
    return _in_group(SCORE_CRITERIA_GROUP, criteria)


NEAREST = 'nearest'
FURTHEST = 'furthest'
RANDOM = 'random'
ARBITRARY = 'arbitrary'
SORT = [NEAREST, FURTHEST, RANDOM, ARBITRARY]
"""Valid ways to sort target specifications."""

SURVIVAL = 'survival'
CREATIVE = 'creative'
ADVENTURE = 'adventure'
SPECTATOR = 'spectator'
GAMEMODE = [SURVIVAL, CREATIVE, ADVENTURE, SPECTATOR]
"""Valid game modes."""

EYES = 'eyes'
FEET = 'feet'
ENTITY_ANCHOR = [EYES, FEET]
"""Valid entity anchors."""

ALL = 'all'
MASKED = 'masked'
SCAN_MODE = [ALL, MASKED]
"""Valid scan modes for blocks subpart of ``/execute`` commands."""

FORCE = 'force'
MOVE = 'move'
NORMAL = 'normal'
CLONE_FLAGS = [FORCE, MOVE, NORMAL]
"""Valid clone flags."""

RESULT = 'result'
SUCCESS = 'success'
STORE_WHAT = [RESULT, SUCCESS]
"""Valid things to store from ``/execute`` commands."""

BYTE = 'byte'
SHORT = 'short'
INT = 'int'
LONG = 'long'
FLOAT = 'float'
DOUBLE = 'double'
DATA_TYPE = [BYTE, SHORT, INT, LONG, FLOAT, DOUBLE]
"""Valid data types."""

EVERYTHING = 'everything'
ONLY = 'only'
FROM = 'from'
THROUGH = 'through'
UNTIL = 'until'
ADVANCEMENT = [EVERYTHING, ONLY, FROM, THROUGH, UNTIL]
"""Valid behavior specifications for the ``/advancement`` command."""

VALUE = 'value'
MAX = 'max'
BOSSBAR_STORE = [VALUE, MAX]
"""Valid bossbar values for storage."""

BOSSBAR_COLORS = [BLUE, GREEN, PINK, PURPLE, RED, WHITE, YELLOW]

NOTCHED_6 = 'notched_6'
NOTCHED_10 = 'notched_10'
NOTCHED_12 = 'notched_12'
NOTCHED_20 = 'notched_20'
PROGRESS = 'progress'
BOSSBAR_STYLES = [NOTCHED_6, NOTCHED_10, NOTCHED_12, NOTCHED_20, PROGRESS]
"""Valid bossbar styles."""

ENABLE = 'enable'
DISABLE = 'disable'
DATAPACK_ACTIONS = [ENABLE, DISABLE]
"""Valid actions on a datapack."""

FIRST = 'first'
LAST = 'last'
BEFORE = 'before_cmds'
AFTER = 'after_cmds'
ORDER = [FIRST, LAST, BEFORE, AFTER]
"""Valid command order specifications."""

AVAILABLE = 'available'
ENABLED = 'enabled'
DATAPACK_FILTERS = [AVAILABLE, ENABLED]
"""Valid data filter specifications."""

EASY = 'easy'
HARD = 'hard'
NORMAL = 'normal'
PEACEFUL = 'peaceful'
DIFFICULTIES = [EASY, HARD, NORMAL, PEACEFUL]
"""Valid difficulty levels."""

LEVELS = 'levels'
POINTS = 'points'
EXPERIENCE_POINTS = [LEVELS, POINTS]
"""Valid experience specifications for the ``/experience`` command."""

START = 'start'
STOP = 'stop'
START_STOP = [START, STOP]

STRUCTURE = 'structure'
BIOME = 'biome'
POI = 'poi'
LOCATABLE = [STRUCTURE, BIOME, POI]
"""Valid categories of things for the ``/locate`` command."""

MAINHAND = 'mainhand'
OFFHAND = 'offhand'
HANDS = [MAINHAND, OFFHAND]
"""Valid hand names."""

DISPLAY_NAME = 'displayname'
RENDER_TYPE = 'rendertype'
NUMBER_FORMAT = 'numberformat'
SCOREBOARD_OBJECTIVES_MODIFIABLE = [DISPLAY_NAME, RENDER_TYPE, NUMBER_FORMAT]
"""Valid modifiable scoreboard objective values."""

HEARTS = 'hearts'
INTEGER = 'integer'
SCOREBOARD_RENDER_TYPES = [HEARTS, INTEGER]
"""Valid scoreboard render values."""

LIST = 'list'
SIDEBAR = 'sidebar'
BELOW_NAME = 'below_name'
DISPLAY_SLOTS = [LIST, SIDEBAR, BELOW_NAME]
"""Valid scoreboard display slots."""

SIDEBAR_TEAM = 'sidebar.team.'

PLUS = '+='
MINUS = '-='
MULT = '*='
DIV = '/='
MOD = '%='
MIN = '<'
# 'MAX' has another value, so special casing required
SWAP = '><'
SCORE_OPERATIONS = [PLUS, MINUS, MULT, DIV, MOD, EQ, MIN, MAX, SWAP]

ATTACKER = 'attacker'
CONTROLLER = 'controller'
LEASHER = 'leasher'
OWNER = 'owner'
PASSENGERS = 'passengers'
TARGET = 'target'
VEHICLE = 'vehicle'
ORIGIN = 'origin'
RELATIONSHIPS = [ATTACKER, CONTROLLER, LEASHER, OWNER, PASSENGERS, TARGET, VEHICLE, ORIGIN]

PARTICLE_MODES = [FORCE, NORMAL]

REPLACE = 'replace'
APPEND = 'append'
SCHEDULE_ACTIONS = [APPEND, REPLACE]

DESTROY = 'destroy'
KEEP = 'keep'
STRICT = 'strict'
SETBLOCK_ACTIONS = [DESTROY, KEEP, REPLACE, STRICT]

NEVER = 'never'
HIDE_FOR_OTHER_TEAMS = 'hideForOtherTeams'
HIDE_FOR_OWN_TEAM = 'hideForOwnTeam'
ALWAYS = 'always'
NAMETAG_VISIBILITY_VALUES = [NEVER, HIDE_FOR_OTHER_TEAMS, HIDE_FOR_OWN_TEAM, ALWAYS]
DEATH_MESSAGE_VISIBILITY_VALUES = NAMETAG_VISIBILITY_VALUES

WORLD_SURFACE = 'world_surface'
MOTION_BLOCKING = 'motion_blocking'
MOTION_BLOCKING_NO_LEAVES = 'motion_blocking_no_leaves'
OCEAN_FLOOR = 'ocean_floor'
HEIGHTMAP = [WORLD_SURFACE, MOTION_BLOCKING, MOTION_BLOCKING_NO_LEAVES, OCEAN_FLOOR]

PUSH_OTHER_TEAMS = 'pushOtherTeams'
PUSH_OWN_TEAM = 'pushOwnTeam'
COLLISION_RULE_VALUES = [NEVER, PUSH_OTHER_TEAMS, PUSH_OWN_TEAM, ALWAYS]

CLEAR = 'clear'
RESET = 'reset'
TITLE = 'title'
SUBTITLE = 'subtitle'
ACTION_BAR = 'actionbar'
TITLE_GIVEN = [TITLE, SUBTITLE, ACTION_BAR]
TITLE_ACTIONS = [CLEAR, RESET] + TITLE_GIVEN

INFINITE = 'infinite'

HEX = 'hex'

RAIN = 'rain'
THUNDER = 'thunder'
WEATHER_TYPES = [CLEAR, RAIN, THUNDER]

ADD_VALUE = 'add_value'
ADD_MULTIPLIED_BASE = 'add_multiplied_base'
ADD_MULTIPLIED_TOTAL = 'add_multiplied_total'
ATTRIBUTE_MODIFIER_ACTION_GROUP = [ADD_VALUE, ADD_MULTIPLIED_BASE, ADD_MULTIPLIED_TOTAL]

BLOCK = 'block'
BLOCK_MARKER = 'block_marker'
DUST_PILLAR = 'dust_pillar'
FALLING_DUST = 'falling_dust'
BLOCK_PARTICE_TYPES = [BLOCK, BLOCK_MARKER, DUST_PILLAR, FALLING_DUST]

FRONT_BACK = 'front_back'
LEFT_RIGHT = 'left_right'
MIRROR_GROUP = [NONE, FRONT_BACK, LEFT_RIGHT]

GIVE = 'give'
GIVE_CLEAR = [GIVE, CLEAR]

TAKE = 'take'
GIVE_TAKE = [GIVE, TAKE]

GRANT = 'grant'
REVOKE = 'revoke'
GRANT_REVOKE = [GRANT, REVOKE]

_GIVELIKE = [GIVE, GRANT]
_CLEARLIKE = [CLEAR, REVOKE, TAKE]

_GIVE_GRANT = GIVE_CLEAR + GRANT_REVOKE

MAX_EFFECT_SECONDS = 1000000
"""Maximum number of seconds an effect can be specified for"""


def _to_donate(action: StrOrArg, group_list: list[str]):
    if is_arg(action):
        return str(action)
    if action in _GIVELIKE:
        return group_list[0]
    elif action in _CLEARLIKE:
        return group_list[1]
    return _in_group(group_list, action)


class Command:
    """
    Base class for all command parts. It builds up the string version of the command through the various calls.
    """

    def __init__(self):
        self._rep = ''

    def __str__(self):
        s = self._rep.strip()
        if s[0] == '$' and not _arg_re.search(s):
            s = s[1:]
        return s

    def __repr__(self):
        return f'<{self.__class__.__name__}:{self}>'

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return str(self) == str(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(str(self))

    def clone(self: T) -> T:
        """Returns a deep copy of this object."""
        return copy.deepcopy(self)

    def _add(self, *objs: any, space: object = True):
        to_add = ' '.join(str(x) for x in
                          map(lambda x: _float(x) if isinstance(x, float) else _bool(x) if isinstance(x, bool) else x,
                              objs))
        if not self._rep:
            self._rep = ''
        elif space and not self._rep.endswith(' '):
            self._rep += ' '
        self._rep += to_add

    def _add_str(self, *args) -> str:
        self._add(*args)
        return str(self)

    def _add_if(self, to_add):
        if self._rep:
            self._rep += str(to_add)

    def _add_opt(self, *objs: any):
        for o in objs:
            if o is not None:
                self._add(o)

    def _add_opt_pos(self, pos: Position | Column = None):
        if pos is not None:
            self._add_opt(*pos)

    def _start(self, start: T) -> T:
        start._rep = self._rep + ' '
        return start


T = TypeVar('T', bound=Command)


class _ScoreClause(Command):
    @_fluent
    def is_(self, relation: StrOrArg, score: ScoreName) -> _ExecuteMod:
        self._add(_in_group(RELATION, relation), as_score(score))
        return self._start(_ExecuteMod())

    @_fluent
    def matches(self, range: Range | bool) -> _ExecuteMod:
        self._add('matches')
        if isinstance(range, bool):
            self._add(int(range))
        else:
            self._add(as_range(range))
        return self._start(_ExecuteMod())


class AdvancementCriteria(Command):
    def __init__(self, advancement: StrOrArg, criteria: BoolOrArg | StrOrArg | tuple[StrOrArg, BoolOrArg]):
        super().__init__()
        advancement = as_advancement(advancement)
        if is_arg(criteria):
            self._add(f'{advancement}={str(criteria)}')
        elif isinstance(criteria, BoolOrArg):
            self._add(f'{advancement}={_bool(criteria)}')
        else:
            self._add(f'{advancement}={{{as_resource_path(criteria[0])}={_bool(criteria[1])}}}')


class _TextMod(Nbt):
    def __init__(self, parent: Text):
        super().__init__()
        self.parent = parent


class _TextHoverAction(_TextMod):
    def show_text(self, txt: Text | str) -> Text:
        self['action'] = 'show_text'
        self['value'] = txt
        return self.parent

    def show_item(self, id: str, count: int = None, tag: str = None) -> Text:
        self['action'] = 'show_item'
        self['id'] = as_resource(id)
        if count is not None:
            self['count'] = count
        if tag is not None:
            self['tag'] = tag
        return self.parent

    def show_entity(self, type: str, uuid: StrOrArg, name: Text | str = None) -> Text:
        self['action'] = 'show_entity'
        self['id'] = as_resource(type)
        self['uuid'] = as_uuid(uuid)
        if name is not None:
            self['name'] = name
        return self.parent


class _TextClickEventAction(_TextMod):
    def open_url(self, url: str) -> Text:
        result = urlparse(url)
        if result.scheme not in ('http', 'https'):
            raise ValueError(f'URL must be http or https: {result.scheme}')
        self.update({'action': 'open_url', 'url': url})
        return self.parent

    def open_file(self, path: str) -> Text:
        Path(path)
        self.update({'action': 'open_file', 'value': path})
        return self.parent

    @staticmethod
    def _as_command(command):
        if not isinstance(command, str):
            command = str(command)
        return command.strip()

    def run_command(self, command: str | Command) -> Text:
        command = self._as_command(command)
        # The '/' is optional for signs, but required every else, so this is safest
        if command[0] != '/':
            command = '/' + command
        self.update({'action': 'run_command', 'command': command})
        return self.parent

    def suggest_command(self, chat: str | Command) -> Text:
        self._as_command(chat)
        self.update({'action': 'suggest_command', 'command': chat})
        return self.parent

    def change_page(self, page: str) -> Text:
        self.update({'action': 'change_page', 'page': page})
        return self.parent

    def copy_to_clipboard(self, txt: str) -> Text:
        self.update({'action': 'copy_to_clipboard', 'value': txt})
        return self.parent


class TargetSpec(Command, ABC):
    """Superclass of all target specification root classes."""

    def is_single(self):
        return False


class User(TargetSpec):
    """A named user as a target."""

    def __init__(self, name: StrOrArg):
        super().__init__()
        self.name = as_user(name)
        self._add(name)

    def is_single(self):
        return True


class Uuid(TargetSpec):
    """A uuid as a target."""

    _UUID_GROUP_SIZES = (8, 4, 4, 4, 12)

    def __init__(self, u1: int, u2: int, u3: int, u4: int):
        """Creates a UUID from the four int components."""
        super().__init__()
        self._ints = (Uuid._signed_32(u1), Uuid._signed_32(u2), Uuid._signed_32(u3), Uuid._signed_32(u4))
        self._add(list(self._ints))

    def is_single(self):
        return True

    @classmethod
    def _signed_32(cls, value):
        iv = value & 0xffffffff
        if iv & 0x80000000:
            iv = -0x100000000 + iv
        return iv

    @property
    def ints(self) -> tuple[int, int, int, int]:
        """The four int components of the UUID."""
        return self._ints

    @property
    def hex_str(self) -> str:
        """The hex string for the UUID."""
        as_hex = '%08x%08x%08x%08x' % tuple(x & 0xffffffff for x in self._ints)
        result = ''
        pos = 0
        for i in Uuid._UUID_GROUP_SIZES:
            result += as_hex[pos:pos + i] + '-'
            pos += i
        return result[:-1]

    @property
    def most_least_dict(self) -> dict[str, int]:
        """The most/least dict for the UUID."""
        most, least = self.most_least
        return {'UUIDMost': most, 'UUIDLeast': least}

    @property
    def most_least(self) -> (int, int):
        """The most/least values for the UUID."""
        return self._ints[0] << 32 | (0xffffffff & self._ints[1]), self._ints[2] << 32 | (0xffffffff & self._ints[3])

    @classmethod
    def from_hex(cls, uuid_str: str) -> Uuid:
        """Returns a UUID from the hex string."""
        as_hex = ''
        for i, part in enumerate(uuid_str.split('-')):
            as_hex += part.zfill(Uuid._UUID_GROUP_SIZES[i])
        return Uuid(Uuid._to_int(as_hex[0:8]), Uuid._to_int(as_hex[8:16]), Uuid._to_int(as_hex[16:24]),
                    Uuid._to_int(as_hex[24:32]))

    @classmethod
    def _to_int(cls, as_hex: str) -> int:
        """Convert the hex string to a signed 32 bit int."""
        return struct.unpack('>i', bytes.fromhex(as_hex))[0]

    @classmethod
    def from_most_least_dict(cls, most_least: dict[str, int]) -> Uuid:
        """Returns a UUID from the most/least pair."""
        return Uuid.from_most_least(most_least['UUIDMost'], most_least['UUIDLeast'])

    @classmethod
    def from_most_least(cls, most: int, least: int) -> Uuid:
        """Returns a UUID from the most/least pair."""
        return Uuid(most >> 32, most & 0xffffffff, least >> 32, least & 0xffffffff)


class Star(TargetSpec):
    """The ``*`` target selector. This is not valid in all commands, but it is in many."""

    def __init__(self):
        super().__init__()
        self._add('*')


# noinspection PyProtectedMember
def p():
    """A target selector for ``@p``."""
    return Selector(Selector._create_key, '@p')


player = p
"""Equivalent to p()."""


# noinspection PyProtectedMember
def rand():
    """A target selector for ``@r``. [No single-character version of this exists because it interferes with the r()
    function that returns relative coordinates.] """
    return Selector(Selector._create_key, '@r')


# noinspection PyProtectedMember
def a():
    """A target selector for ``@a``."""
    return Selector(Selector._create_key, '@a')


all_ = a
"""Equivalent to a()."""


# noinspection PyProtectedMember
def e():
    """A target selector for ``@e``."""
    return Selector(Selector._create_key, '@e')


# noinspection PyProtectedMember
def s():
    """A target selector for ``@s``."""
    return Selector(Selector._create_key, '@s')


def n():
    return Selector(Selector._create_key, '@n')


self = s
"""Equivalent to s()."""


def _as_score_spec(v):
    if is_arg(v) or isinstance(v, (str, int, float)):
        return de_arg(v)
    return as_range(v)


class Selector(TargetSpec):
    """This class represents a target selector. You start with one of the selector methods p(), random(), s(), a(),
    and e(), and then possibly add qualifiers from the methods here. These can be chained, so for example,
    ``e().tag('foo').limit(1)`` is equivalent to the minecraft target selector ``@e[tag=foo,limit=1]``. """

    _create_key = object()

    def __init__(self, create_key, selector: str):
        super().__init__()
        assert (create_key == Selector._create_key), 'Private __init__, use creation methods'
        self._selector = selector
        self._single = selector in ('@s', '@p', '@r', '@n')
        self._args = {}

    def is_single(self):
        return self._single

    def __str__(self):
        if not self._rep:
            return self._selector
        return self._selector + '[' + super().__str__() + ']'

    def _add_arg(self, key: str, value: any):
        v = str(value)
        if v.find('=') < 0 or v[0] == '{':
            v = f'{key}={v}'
        if key in self._args:
            self._args[key] += ',' + v
        else:
            self._args[key] = v
        self._append(v)
        return self

    def _append(self, v):
        self._add_if(',')
        self._add(v)

    def _unique_arg(self, key: str, value: any):
        if key in self._args:
            raise KeyError(f'{key}: Already set in target')
        self._add_arg(key, value)
        return self

    def _multi_args(self, key: str, value: any, values):
        self._add_arg(key, value)
        for v in values:
            self._add_arg(key, v)
        return self

    def _not_args(self, key: StrOrArg, value, values):
        self._add_arg(key, _not_ify(value))
        for v in values:
            self._add_arg(key, _not_ify(v))
        result = self._args[key]
        value_count = result.count('=')
        neg_count = result.count('!')
        # noinspection PyChainedComparisons
        if value_count > 1 and neg_count != value_count:
            raise KeyError(f'{key}: Cannot repeat unless all are negated: {result}')
        return self

    @_fluent
    def pos(self, pos: Position) -> Selector:
        """Add an x,y,z position to the selector."""
        return self._unique_arg('pos', f'x={pos[0]},y={pos[1]},z={pos[2]}')

    @_fluent
    def literal(self, string: str):
        """Allow user to add literal text in the selector arguments. No checks."""
        self._append(string)
        return self

    @_fluent
    def distance(self, distance: Range) -> Selector:
        """Add a distance (radius) to the selector."""
        return self._unique_arg('distance', as_range(distance))

    @_fluent
    def volume(self, deltas: Tuple[FloatOrArg, FloatOrArg, FloatOrArg]) -> Selector:
        """Add a volume to the selector. Must have three values in the list or tuple."""
        dx, dy, dz = deltas
        return self._unique_arg('delta', f'dx={_float(dx)},dy={_float(dy)},dz={_float(dz)}')

    @_fluent
    def scores(self, score_specs: Mapping) -> Selector:
        """Add one or more score criteria to the selector. The objective is the mapping's key, and can be a string or
        an Arg. The score value can be a value, a range, an Arg, or a str."""
        s = '{' + ','.join(f'{de_arg(k)}={_as_score_spec(v)}' for k, v in score_specs.items()) + '}'
        return self._unique_arg('scores', s)

    @_fluent
    def not_scores(self, score_specs: Mapping) -> Selector:
        """Add one or more score criteria to the selector, each of which is negated. The objective is the mapping's
        key, and can be a string or an Arg. The score value can be a value, a range, an Arg, or a str."""
        s = '{' + ','.join(f'{de_arg(k)}=!{_as_score_spec(v)}' for k, v in score_specs.items()) + '}'
        return self._unique_arg('scores', s)

    @_fluent
    def tag(self, tag: StrOrArg, *tags: StrOrArg) -> Selector:
        """Add one or more tags to the selector. You can use '!' for 'not'."""
        return self._multi_args('tag', as_name(tag, allow_not=True), as_names(*tags, allow_not=True))

    @_fluent
    def not_tag(self, tag: StrOrArg, *tags: StrOrArg) -> Selector:
        """Add one or more 'not' tags to the selector. You need not specify the '!' in the string."""
        return self.tag(_not_ify(as_name(tag, allow_not=True)), *_not_ify(as_names(*tags, allow_not=True)))

    @_fluent
    def team(self, team: StrOrArg) -> Selector:
        """Add a team to the selector."""
        return self._unique_arg('team', as_name(team, allow_not=True))

    @_fluent
    def not_team(self, team: StrOrArg, *teams) -> Selector:
        """Add one or more 'not' teams to the selector. You need not specify the '!' in the string."""
        return self._not_args('team', as_name(team, allow_not=True), as_names(*teams, allow_not=True))

    @_fluent
    def sort(self, sorting: StrOrArg) -> Selector:
        """Add a sort criteria to the selector."""
        return self._unique_arg('sort', _in_group(SORT, sorting))

    @_fluent
    def limit(self, limit: IntOrArg) -> Selector:
        """Add a result count limit to the selector."""
        self._single = limit == 1
        return self._unique_arg('limit', de_int_arg(limit))

    @_fluent
    def level(self, level_range: Range) -> Selector:
        """Add a level range to the selector."""
        return self._unique_arg('level', as_range(level_range))

    @_fluent
    def gamemode(self, mode: StrOrArg) -> Selector:
        """Add a gamemode to the selector."""
        return self._unique_arg('gamemode', _in_group(GAMEMODE, mode))

    @_fluent
    def not_gamemode(self, mode: StrOrArg, *modes: StrOrArg) -> Selector:
        """Add one or more 'not' gamemodes to the selector. You need to specify the '!' in the string."""
        _in_group(GAMEMODE, mode)
        for g in modes:
            _in_group(GAMEMODE, g)
        return self._not_args('gamemode', mode, modes)

    @_fluent
    def name(self, name: StrOrArg) -> Selector:
        """Add a name criteria to the selector."""
        return self._unique_arg('name', as_name(name, allow_not=True))

    @_fluent
    def not_name(self, name: StrOrArg, *names: StrOrArg) -> Selector:
        """Add one or more 'not' names to the selector. You need to specify the '!' in the string."""
        return self._not_args('name', as_name(name, allow_not=True), as_names(*names, allow_not=True))

    @_fluent
    def x_rotation(self, rot_range: Range) -> Selector:
        """Add an X rotation to the selector."""
        return self._unique_arg('x_rotation', as_range(rot_range))

    @_fluent
    def y_rotation(self, rot_range: Range) -> Selector:
        """Add a Y rotation to the selector."""
        self._unique_arg('y_rotation', as_range(rot_range))
        return self

    @_fluent
    def type(self, type_: StrOrArg) -> Selector:
        """Add a type to the selector."""
        return self._unique_arg('type', as_resource(type_, allow_not=True))

    @_fluent
    def not_type(self, type_: StrOrArg, *types: StrOrArg):
        """Add one or more 'not' types to the selector. You need to specify the '!' in the string."""
        return self._not_args('type', as_resource(type_, allow_not=True), as_resources(*types, allow_not=True))

    @_fluent
    def nbt(self, nbt: NbtDef, *nbts: NbtDef) -> Selector:
        """Add NBT criteria to the selector."""
        return self._multi_args('nbt', Nbt.as_nbt(nbt), (Nbt.as_nbt(x) for x in nbts))

    @_fluent
    def not_nbt(self, nbt: NbtDef, *nbts: NbtDef) -> Selector:
        """Add NBT criteria to the selector."""
        return self._multi_args('nbt', f'!{Nbt.as_nbt(nbt)}', (Nbt.as_nbt(x) for x in nbts))

    @_fluent
    def advancements(self, advancement: AdvancementCriteria, *advancements: AdvancementCriteria) -> Selector:
        """Add advancements to the selector."""
        adv = [advancement]
        for a in advancements:
            adv.append(a)
        values = tuple(str(x) for x in adv)
        return self._unique_arg('advancements', '{' + ','.join(values) + '}')

    @_fluent
    def predicate(self, predicate: StrOrArg, *predicates: StrOrArg) -> Selector:
        """Add a predicate to the selector."""
        return self._multi_args('predicate', predicate, predicates)


class DataTargetBase(Command):
    pass


class BlockDataTarget(DataTargetBase):
    def __init__(self, pos: Position | StrOrArg):
        super().__init__()
        self._add('block')
        if is_arg(pos):
            self._add(pos)
        else:
            self._add(' '.join(str(x) for x in as_position(pos)))


class EntityDataTarget(DataTargetBase):
    def __init__(self, target: TargetSpec | StrOrArg, single=False):
        super().__init__()
        self._add('entity', (as_single if single else as_target)(target))


class StorageDataTarget(DataTargetBase):
    def __init__(self, store: StrOrArg):
        super().__init__()
        self._add('storage', as_resource_path(store))


def block(pos: Position | StrOrArg) -> BlockDataTarget:
    return BlockDataTarget(pos)


def entity(target: TargetSpec | StrOrArg, single=False) -> EntityDataTarget:
    return EntityDataTarget(target, single)


def storage(store: StrOrArg) -> StorageDataTarget:
    return StorageDataTarget(store)


class _IfClause(Command):
    @_fluent
    def biome(self, pos: Position, biome: StrOrArg) -> _ExecuteMod:
        self._add('biome', *pos, as_biome(biome))
        return self._start(_ExecuteMod())

    @_fluent
    def block(self, pos: Position, block: BlockDef) -> _ExecuteMod:
        self._add('block', *pos, as_block(block))
        return self._start(_ExecuteMod())

    @_fluent
    def blocks(self, start_pos: Position, end_pos: Position, dest_pos: Position, mode: StrOrArg) -> _ExecuteMod:
        self._add('blocks', *start_pos, *end_pos, *dest_pos, _in_group(SCAN_MODE, mode))
        return self._start(_ExecuteMod())

    @_fluent
    def data(self, data_target: DataTarget, nbt_path: StrOrArg) -> _ExecuteMod:
        self._add('data', data_target_str(data_target), as_nbt_path(nbt_path))
        return self._start(_ExecuteMod())

    @_fluent
    def items(self, item_target: ItemTarget, slot: StrOrArg, item: StrOrArg) -> _ExecuteMod:
        # data target is a superset of item target
        self._add('items', as_data_target(item_target), as_slot(slot), de_arg(item))
        return self._start(_ExecuteMod())

    @_fluent
    def entity(self, target: Target) -> _ExecuteMod:
        self._add('entity', as_target(target))
        return self._start(_ExecuteMod())

    @_fluent
    def function(self, function: StrOrArg) -> _ExecuteMod:
        self._add('function', function)
        return self._start(_ExecuteMod())

    @_fluent
    def predicate(self, predicate: StrOrArg) -> _ExecuteMod:
        self._add('predicate', predicate)
        return self._start(_ExecuteMod())

    @_fluent
    def score(self, score: ScoreName) -> _ScoreClause:
        self._add('score', as_score(score))
        return self._start(_ScoreClause())

    @_fluent
    def loaded(self, pos: Position) -> _ExecuteMod:
        self._add('loaded', *pos)
        return self._start(_ExecuteMod())


class _StoreClause(Command):
    @_fluent
    def block(self, pos: Position, nbt_path: StrOrArg, data_type: str, scale: FloatOrArg = 1) -> _ExecuteMod:
        self._add('block', *pos, as_nbt_path(nbt_path), _in_group(DATA_TYPE, data_type), de_float_arg(scale))
        return self._start(_ExecuteMod())

    @_fluent
    def entity(self, target: Target, nbt_path: StrOrArg, data_type: str, scale: FloatOrArg = 1) -> _ExecuteMod:
        self._add('entity', as_target(target), as_nbt_path(nbt_path), _in_group(DATA_TYPE, data_type),
                  de_float_arg(scale))
        return self._start(_ExecuteMod())

    @_fluent
    def storage(self, target: StrOrArg, nbt_path: StrOrArg, data_type: str, scale: FloatOrArg = 1) -> _ExecuteMod:
        self._add('storage', as_resource(target), as_nbt_path(nbt_path), _in_group(DATA_TYPE, data_type),
                  de_float_arg(scale))
        return self._start(_ExecuteMod())

    @_fluent
    def bossbar(self, id: StrOrArg, where: str) -> _ExecuteMod:
        self._add('bossbar', id, _in_group(BOSSBAR_STORE, where))
        return self._start(_ExecuteMod())

    @_fluent
    def score(self, score: ScoreName) -> _ExecuteMod:
        self._add('score', as_score(score))
        return self._start(_ExecuteMod())


class _ReturnMod(Command):
    def __init__(self):
        super().__init__()
        self._used = False

    @_fluent
    def run(self, cmd: StrOrArg | Command) -> str:
        if not isinstance(cmd, str):
            cmd = str(cmd)
        self._add('run', cmd)
        self._used = True
        return str(self)

    @_fluent
    def fail(self) -> str:
        self._add('fail')
        return str(self)

    def __str__(self):
        if not self._used:
            return 'return 0'
        return super().__str__()


class _ExecuteMod(Command):
    @_fluent
    def align(self, axes: str) -> _ExecuteMod:
        if not re.fullmatch(r'[xyz]+', axes):
            raise ValueError(f'{axes}: Must be combination of x, y, and/or z')
        self._add('align', axes)
        return self

    @_fluent
    def anchored(self, anchor: StrOrArg) -> _ExecuteMod:
        self._add('anchored', _in_group(ENTITY_ANCHOR, anchor))
        return self

    @_fluent
    def as_(self, target: Target) -> _ExecuteMod:
        self._add('as', as_target(target))
        return self

    @_fluent
    def at(self, target: Target) -> _ExecuteMod:
        self._add('at', as_target(target))
        return self

    @_fluent
    def entity(self, target: EntityDef) -> _ExecuteMod:
        self._add('entity', as_target(target))
        return self

    @_fluent
    def facing(self, pos: Position) -> _ExecuteMod:
        self._add('facing', *pos)
        return self

    @_fluent
    def facing_entity(self, target: Target, anchor: StrOrArg) -> _ExecuteMod:
        self._add('facing entity', as_target(target), _in_group(ENTITY_ANCHOR, anchor))
        return self

    @_fluent
    def in_(self, dimension: StrOrArg) -> _ExecuteMod:
        self._add('in', _in_group(DIMENSION, dimension))
        return self

    @_fluent
    def positioned(self, pos: Position) -> _ExecuteMod:
        self._add('positioned', *pos)
        return self

    @_fluent
    def positioned_as(self, target: Target) -> _ExecuteMod:
        self._add('positioned as', as_target(target))
        return self

    @_fluent
    def positioned_over(self, heightmap: StrOrArg) -> _ExecuteMod:
        self._add('positioned over', _in_group(HEIGHTMAP, heightmap))
        return self

    @_fluent
    def rotated(self, yaw: Angle, pitch: Angle) -> _ExecuteMod:
        self._add('rotated', as_yaw(yaw), as_pitch(pitch))
        return self

    @_fluent
    def rotated_as(self, target: Target) -> _ExecuteMod:
        self._add('rotated as', as_target(target))
        return self

    @_fluent
    def if_(self) -> _IfClause:
        self._add('if')
        return self._start(_IfClause())

    @_fluent
    def unless(self) -> _IfClause:
        self._add('unless')
        return self._start(_IfClause())

    @_fluent
    def store(self, what: StrOrArg) -> _StoreClause:
        self._add('store', _in_group(STORE_WHAT, what))
        return self._start(_StoreClause())

    @_fluent
    def dimension(self, dimension: StrOrArg) -> _ExecuteMod:
        self._add('dimension', dimension)
        return self

    @_fluent
    def on(self, relationship: StrOrArg) -> _ExecuteMod:
        self._add('on', _in_group(RELATIONSHIPS, relationship))
        return self

    @_fluent
    def summon(self, entity: EntityDef) -> _ExecuteMod:
        self._add('summon', as_entity(entity))
        return self

    @_fluent
    def run(self, cmd: str | Command | Commands, *other_cmds: str | Command | Commands) -> str | tuple[str]:
        """
        If cmds is empty, expect the command to follow.
        Otherwise, return an 'execute' command for each element of cmds.
        If there is only one element, return a single string, otherwise return a tuple of them.
        """
        cmds = _to_list(cmd)
        cmds.extend(other_cmds)
        self._add('run')
        cmds = lines(*cmds)
        results = []
        for c in cmds:
            selfish = self.clone()
            s = str(c)
            if len(s) > 0 and s[0] == '$':
                s = s[1:]
            selfish._add(s)
            results.append(str(selfish))
        if len(cmds) == 1:
            return results[0]
        return tuple(results)


class _AttributeBaseAct(Command):
    @_fluent
    def get(self, scale: float = None) -> str:
        self._add('get')
        if scale:
            self._add(scale)
        return str(self)

    @_fluent
    def set(self, value: float) -> str:
        self._add('set', value)
        return str(self)

    @_fluent
    def reset(self) -> str:
        self._add('reset')
        return str(self)


class _AttributeModifierAct(Command):
    @_fluent
    def add(self, uuid: StrOrArg | Uuid, name: StrOrArg, value: FloatOrArg, op: str = None) -> str:
        self._add('add', as_uuid(uuid), f'"{name}"', de_float_arg(value))
        self._add_opt(_in_group(ATTRIBUTE_MODIFIER_ACTION_GROUP, op))
        return str(self)

    @_fluent
    def remove(self, uuid: StrOrArg) -> str:
        self._add('remove', as_uuid(uuid))
        return str(self)

    @_fluent
    def value(self, uuid: StrOrArg, scale: float = None) -> str:
        self._add('value get', as_uuid(uuid))
        if scale:
            self._add(scale)
        return str(self)


class _AttributeMod(Command):
    @_fluent
    def get(self, scale: float = None) -> str:
        self._add('get')
        if scale:
            self._add(scale)
        return str(self)

    @_fluent
    def base(self) -> _AttributeBaseAct:
        self._add('base')
        return self._start(_AttributeBaseAct())

    @_fluent
    def modifier(self) -> _AttributeModifierAct:
        self._add('modifier')
        return self._start(_AttributeModifierAct())


class _BossbarGet(Command):
    @_fluent
    def color(self) -> str:
        self._add('color')
        return str(self)

    @_fluent
    def max(self) -> str:
        self._add('max')
        return str(self)

    @_fluent
    def name(self) -> str:
        self._add('name')
        return str(self)

    @_fluent
    def players(self) -> str:
        self._add('players')
        return str(self)

    @_fluent
    def style(self) -> str:
        self._add('style')
        return str(self)

    @_fluent
    def value(self) -> str:
        self._add('value')
        return str(self)

    @_fluent
    def visible(self) -> str:
        self._add('visible')
        return str(self)


class _BossbarSet(Command):
    @_fluent
    def color(self, color: StrOrArg) -> str:
        self._add('color', _in_group(BOSSBAR_COLORS, color))
        return str(self)

    @_fluent
    def max(self, value: IntOrArg) -> str:
        self._add('max', de_int_arg(value))
        return str(self)

    @_fluent
    def name(self, name: StrOrArg) -> str:
        self._add('name', _quote(name))
        return str(self)

    @_fluent
    def players(self, *targets: Target) -> str:
        targets = (as_target(x) for x in targets)
        self._add('players', *targets)
        return str(self)

    @_fluent
    def style(self, style: StrOrArg) -> str:
        self._add('style', _in_group(BOSSBAR_STYLES, style))
        return str(self)

    @_fluent
    def value(self, value: int) -> str:
        self._add('value', value)
        return str(self)

    @_fluent
    def visible(self, visible: bool) -> str:
        self._add('visible', _bool(visible))
        return str(self)


class _BossbarMod(Command):
    @_fluent
    def add(self, id: StrOrArg, name: StrOrArg) -> str:
        self._add('add', as_resource(id), _quote(name))
        return str(self)

    @_fluent
    def get(self, id: StrOrArg) -> _BossbarGet:
        self._add('get', as_resource(id))
        return self._start(_BossbarGet())

    @_fluent
    def list(self) -> str:
        self._add('list')
        return str(self)

    @_fluent
    def remove(self, id: StrOrArg) -> str:
        self._add('remove', as_resource(id))
        return str(self)

    @_fluent
    def set(self, id: StrOrArg) -> _BossbarSet:
        self._add('set', as_resource(id))
        return self._start(_BossbarSet())


class _ClearClause(Command):
    @_fluent
    def item(self, item: StrOrArg, max_count: int = None) -> str:
        self._add(item)
        if max_count:
            self._add(max_count)
        return str(self)


class _CloneClause(Command):
    def _flag(self, flag):
        if flag:
            self._add(_in_group(CLONE_FLAGS, flag))

    @_fluent
    def replace(self, flag: str = None) -> str:
        self._add('replace')
        self._flag(flag)
        return str(self)

    @_fluent
    def masked(self, flag: str = None) -> str:
        self._add('masked')
        self._flag(flag)
        return str(self)

    @_fluent
    def filtered(self, block: BlockDef, flag: str = None) -> str:
        self._add('filtered', as_block(block))
        self._flag(flag)
        return str(self)

    @_fluent
    def strict(self) -> _CloneClause:
        self._add('strict')
        return self.clone()


# noinspection PyAttributeOutsideInit
class _CloneFromDimMod(Command):
    def __init__(self, config: str = None):
        super().__init__()
        self.config = config

    @_fluent
    def from_(self, dimension: StrOrArg, start_pos: Position, end_pos: Position) -> _CloneToDimMod:
        self.dimension = dimension
        self.start_pos = start_pos
        self.end_pos = end_pos
        return _CloneToDimMod(self)


class _CloneToDimMod(Command):
    def __init__(self, from_: _CloneFromDimMod):
        super().__init__()
        self._from_ = from_

    @_fluent
    def to(self, dimension: StrOrArg, dest_pos: Position, config: str = None) -> _CloneClause:
        f = self._from_
        dest_pos = dest_pos
        self._add('clone', 'from', f.dimension, *f.start_pos, *f.end_pos, 'to', dimension, *dest_pos)
        if config is None:
            config = self._from_.config
        self._add_opt(config)
        return self._start(_CloneClause())


class _End(Command):
    pass


class _DataSource(Command):
    @_fluent
    def from_(self, data_target: DataTarget, nbt_path: StrOrArg) -> str:
        self._add('from', data_single_str(data_target), as_nbt_path(nbt_path))
        return str(self)

    @_fluent
    def value(self, v: StrOrArg | float | Nbt | Iterable[StrOrArg | float | Mapping]) -> str:
        if not isinstance(v, Mapping):
            v = Nbt.to_str(v)
        else:
            v = Nbt.as_nbt(v)
        self._add('value', v)
        return str(self)

    @_fluent
    def string(self, data_target: DataTarget, nbt_path: StrOrArg = None, start: IntOrArg = None,
               end: IntOrArg = None) -> str:
        self._add('string', data_single_str(data_target))
        self._add_opt(as_nbt_path(nbt_path), de_int_arg(start), de_int_arg(end))
        return str(self)


class _DamageByMod(Command):
    @_fluent
    def from_(self, target: Target) -> str:
        self._add('from', as_target(target))
        return str(self)


class _DamageMod(Command):
    @_fluent
    def at(self, pos: Position) -> str:
        self._add('at', *pos)
        return str(self)

    @_fluent
    def by(self, target: Target) -> _DamageByMod:
        self._add('by', as_target(target))
        return self._start(_DamageByMod())


class _DataModifyClause(Command):
    def _keyword(self, keyword: str) -> _DataSource:
        self._add(keyword)
        return self._start(_DataSource())

    @_fluent
    def append(self) -> _DataSource:
        return self._keyword('append')

    @_fluent
    def insert(self, index: int) -> _DataSource:
        self._add('insert', index)
        return self._start(_DataSource())

    @_fluent
    def merge(self) -> _DataSource:
        return self._keyword('merge')

    @_fluent
    def prepend(self) -> _DataSource:
        return self._keyword('prepend')

    @_fluent
    def set(self) -> _DataSource:
        return self._keyword('set')


class _DataMod(Command):
    @_fluent
    def get(self, data_target: DataTarget, nbt_path: StrOrArg = None, scale: FloatOrArg = None, /) -> str:
        self._add('get', data_single_str(data_target))
        if not nbt_path and scale is not None:
            raise ValueError('Must give dir to use scale')
        self._add_opt(as_nbt_path(nbt_path), de_float_arg(scale))
        return str(self)

    @_fluent
    def merge(self, data_target: DataTarget, nbt: NbtDef | StrOrArg) -> str:
        self._add('merge', data_single_str(data_target), Nbt.as_nbt(nbt))
        return str(self)

    @_fluent
    def modify(self, data_target: DataTarget, nbt_path: StrOrArg) -> _DataModifyClause:
        self._add('modify', data_single_str(data_target), as_nbt_path(nbt_path))
        return self._start(_DataModifyClause())

    @_fluent
    def remove(self, data_target: DataTarget, nbt_path: StrOrArg) -> str:
        self._add('remove', data_single_str(data_target), as_nbt_path(nbt_path))
        return str(self)


class _RandomMod(Command):
    @_fluent
    def roll(self, range: tuple[IntOrArg, IntOrArg] | StrOrArg, sequence: StrOrArg = None, /,
             in_chat: bool = True) -> str:
        self._add('roll' if in_chat else 'value')
        if is_arg(range):
            self._add(range)
        else:
            self._add(f'{de_int_arg(range[0])}..{de_int_arg(range[1])}')
        self._add_opt(as_name(sequence))
        return str(self)

    @_fluent
    def value(self, range: (IntOrArg, IntOrArg), sequence: StrOrArg = None, /, in_chat: bool = False) -> str:
        return self.roll(range, sequence, in_chat)

    @_fluent
    def reset(self, sequence: StrOrArg, seed: IntOrArg = None, include_world_seed: BoolOrArg = None,
              include_sequence_id: BoolOrArg = None, /) -> str:
        self._add('reset')
        if sequence != '*':
            sequence = as_name(sequence)
        self._add(sequence)
        self._add_opt(de_int_arg(seed), de_arg(include_world_seed), de_arg(include_sequence_id))
        return str(self)


class _DatapackOrder(Command):
    @_fluent
    def first(self) -> str:
        self._add('first')
        return str(self)

    @_fluent
    def last(self) -> str:
        self._add('last')
        return str(self)

    @_fluent
    def before(self, other_datapack: StrOrArg) -> str:
        self._add('before', other_datapack)
        return str(self)

    @_fluent
    def after(self, other_datapack: StrOrArg) -> str:
        self._add('after', other_datapack)
        return str(self)


class _DatapackMod(Command):
    @_fluent
    def disable(self, name: StrOrArg) -> str:
        self._add('disable', as_name(name))
        return str(self)

    @_fluent
    def enable(self, name) -> _DatapackOrder:
        self._add('enable', name)
        return self._start(_DatapackOrder())

    @_fluent
    def list(self, filter_spec: StrOrArg = None) -> str:
        self._add('list')
        self._add_opt(_in_group(DATAPACK_FILTERS, filter_spec))
        return str(self)


class _DebugMod(Command):
    @_fluent
    def start(self) -> str:
        self._add('start')
        return str(self)

    @_fluent
    def stop(self) -> str:
        self._add('stop')
        return str(self)

    @_fluent
    def function(self, path: StrOrArg | object) -> str:
        self._add('function', as_resource_path(_as_function_path(path)))
        return str(self)


class _DialogPart(Command):
    @_fluent
    def show(self, target: TargetSpec, dialog: StrOrArg):
        self._add('show', as_target(target), as_resource(dialog))
        return str(self)

    @_fluent
    def clear(self, target: TargetSpec):
        self._add('clear', as_target(target))
        return str(self)


class _EffectAction(Command):
    @_fluent
    def give(self, target: Target, effect: StrOrArg, seconds: IntOrArg | str = None,
             amplifier: IntOrArg = None, hide_particles: BoolOrArg = None) -> str:
        if amplifier is not None and seconds is None:
            raise ValueError('must give seconds to use amplifier')
        if hide_particles is not None and amplifier is None:
            amplifier = 1
        if isinstance(seconds, str) and not is_int_arg(seconds):
            if seconds != INFINITE:
                raise ValueError(f'{seconds}: Invalid duration')
        elif isinstance(seconds, int):
            seconds_range = range(MAX_EFFECT_SECONDS + 1)
            if seconds not in seconds_range:
                raise ValueError(f'{seconds}: Not in range {seconds_range}')
        effect = as_resource(effect)
        self._add('give', as_target(target), effect)
        self._add_opt(de_int_arg(seconds), de_int_arg(amplifier), _bool(hide_particles))
        return str(self)

    @_fluent
    def clear(self, target: Target = None, effect: StrOrArg = None) -> str:
        if effect is not None and target is None:
            raise ValueError('must give target to use effect')
        self._add('clear')
        effect = as_resource(effect)
        self._add_opt(as_target(target), effect)
        return str(self)


class _ExperienceMod(Command):
    @_fluent
    def add(self, target: Target, amount: IntOrArg, which: StrOrArg = None) -> str:
        self._add('add', as_target(target), de_int_arg(amount))
        self._add_opt(_in_group(EXPERIENCE_POINTS, which))
        return str(self)

    @_fluent
    def set(self, target: Target, amount: IntOrArg, which: StrOrArg = None) -> str:
        self._add('set', as_target(target), de_int_arg(amount))
        self._add_opt(_in_group(EXPERIENCE_POINTS, which))
        return str(self)

    @_fluent
    def query(self, target: Target, which: StrOrArg) -> str:
        self._add('query', as_single(target), _in_group(EXPERIENCE_POINTS, which))
        return str(self)


class _FilterModifier(Command):

    @_fluent
    def destroy(self) -> str:
        self._add('destroy')
        return str(self)

    @_fluent
    def hollow(self) -> str:
        self._add('hollow')
        return str(self)

    @_fluent
    def outline(self) -> str:
        self._add('outline')
        return str(self)

    @_fluent
    def strict(self) -> str:
        self._add('strict')
        return str(self)


class _FilterClause(_FilterModifier):
    @_fluent
    def replace(self, block: BlockDef = None) -> _FilterModifier:
        self._add('replace')
        self._add_opt(block)
        return self._start(_FilterModifier())

    @_fluent
    def keep(self) -> str:
        self._add('keep')
        return str(self)


class _BiomeFilterClause(Command):
    @_fluent
    def replace(self, biome: StrOrArg) -> str:
        self._add('replace', as_biome(biome))
        return str(self)


class _ForceloadMod(Command):
    def _from_to(self, action: str, start: IntColumn, end: IntColumn) -> str:
        self._add(action, *start)
        if end:
            self._add(*end)
        return str(self)

    @_fluent
    def add(self, start: IntColumn, end: IntColumn = None) -> str:
        return self._from_to('add', start, end)

    @_fluent
    def remove(self, start: IntColumn, end: IntColumn = None) -> str:
        return self._from_to('remove', start, end)

    @_fluent
    def remove_all(self) -> str:
        self._add('remove', 'all')
        return str(self)

    @_fluent
    def query(self, pos: IntColumn = None) -> str:
        self._add('query')
        if pos:
            self._add(*pos)
        return str(self)


class _FunctionWith(Command):
    @_fluent
    def block(self, pos: Position) -> str:
        self._add('block', *pos)
        return str(self)

    @_fluent
    def entity(self, target: Target) -> str:
        self._add('entity', as_target(target))
        return str(self)

    @_fluent
    def storage(self, source: StrOrArg, nbt_path: StrOrArg = None) -> str:
        self._add('storage', source)
        self._add_opt(as_resource_path(nbt_path))
        return str(self)


class _FunctionMod(Command):
    @_fluent
    def with_(self) -> _FunctionWith:
        self._add('with')
        return self._start(_FunctionWith())


class _ItemTarget(Command):
    def __init__(self, follow: T, allow_modifier=False):
        super().__init__()
        self.follow = follow
        self.allow_modifier = allow_modifier

    @_fluent
    def block(self, pos: Position, slot: StrOrArg, modifier: StrOrArg = None) -> T:
        self._add('block', *pos, as_slot(slot))
        self._modifier(modifier)
        return self._start(self.follow)

    @_fluent
    def entity(self, target: Target, slot: StrOrArg, modifier: StrOrArg = None) -> T:
        self._add('entity', as_target(target), as_slot(slot))
        self._modifier(modifier)
        return self._start(self.follow)

    def _modifier(self, modifier: StrOrArg):
        if modifier and not self.allow_modifier:
            raise ValueError('Modifier not allowed here')
        if isinstance(modifier, Arg):
            modifier = str(modifier)
        self._add_opt(modifier)


class _ItemReplace(Command):
    @_fluent
    def with_(self, item: EntityDef, count: int = None) -> str:
        self._add('with', as_entity(item))
        self._add_opt(count)
        return str(self)

    @_fluent
    def from_(self) -> _ItemTarget:
        self._add('from')
        return self._start(_ItemTarget(_End(), True))


class _ItemMod(Command):
    @_fluent
    def modify(self) -> _ItemTarget:
        self._add('modify')
        return self._start(_ItemTarget(_End(), True))

    @_fluent
    def replace(self) -> _ItemTarget:
        self._add('replace')
        return self._start(_ItemTarget(_ItemReplace()))


class _LootSource(Command):
    @_fluent
    def fish(self, loot_table: StrOrArg, pos: Position, thing: StrOrArg) -> str:
        # the 'hand' keywords are also valid resource names, so no separate test is meaningful
        self._add('fish', as_resource_path(loot_table), *pos, as_resource(thing))
        return str(self)

    @_fluent
    def loot(self, loot_table: StrOrArg) -> str:
        self._add('loot', as_resource_path(loot_table))
        return str(self)

    @_fluent
    def kill(self, target: Target) -> str:
        self._add('kill', as_target(target))
        return str(self)

    @_fluent
    def mine(self, pos: Position, tool: EntityDef = None) -> str:
        # the 'hand' keywords are also valid resource names, so no separate test is meaningful
        self._add('mine', *pos)
        self._add_opt(as_entity(as_entity(tool)))
        return str(self)


class _LootReplaceTarget(Command):
    @_fluent
    def block(self, pos: Position, slot: IntOrArg | StrOrArg, count: IntOrArg = None) -> _LootSource:
        self._add('block', *pos, de_arg(slot))
        self._add_opt(de_int_arg(count))
        return self._start(_LootSource())

    @_fluent
    def entity(self, target: Target, slot: IntOrArg | StrOrArg, count: IntOrArg = None) -> _LootSource:
        self._add('entity', as_target(target), slot)
        self._add_opt(de_int_arg(count))
        return self._start(_LootSource())


class _LootTarget(Command):
    @_fluent
    def give(self, target: Target) -> _LootSource:
        self._add('give', as_single(target))
        return self._start(_LootSource())

    @_fluent
    def insert(self, pos: Position) -> _LootSource:
        self._add('insert', *pos)
        return self._start(_LootSource())

    @_fluent
    def spawn(self, pos: Position) -> _LootSource:
        self._add('spawn', *pos)
        return self._start(_LootSource())

    @_fluent
    def replace(self) -> _LootReplaceTarget:
        self._add('replace')
        return self._start(_LootReplaceTarget())


class _ScoreboardObjectivesMod(Command):
    @_fluent
    def list(self) -> str:
        self._add('list')
        return str(self)

    @_fluent
    def add(self, objective: str, score_criteria: StrOrArg, display_name: str = None) -> str:
        score_criteria = as_criteria(score_criteria)
        self._add('add', as_name(objective), as_criteria(score_criteria))
        self._add_opt(as_name(display_name))
        return str(self)

    @_fluent
    def remove(self, objective: StrOrArg) -> str:
        self._add('remove', as_name(objective))
        return str(self)

    @_fluent
    def setdisplay(self, slot: StrOrArg, objective: StrOrArg = None) -> str:
        if not slot.startswith(SIDEBAR_TEAM):
            _in_group(DISPLAY_SLOTS, slot)
        self._add('setdisplay', slot)
        self._add_opt(as_name(objective))
        return str(self)

    @_fluent
    def modify(self, objective: StrOrArg) -> str | _ScoreboardObjectivesModifyMod:
        self._add('modify', objective)
        return self._start(_ScoreboardObjectivesModifyMod())


class _ScoreboardObjectivesModifyMod(Command):
    @_fluent
    def displayname(self, name: StrOrArg | Text) -> str:
        self._add('displayname', name)
        return str(self)

    @_fluent
    def rendertype(self, type: StrOrArg) -> str:
        self._add('rendertype', _in_group(SCOREBOARD_RENDER_TYPES, type))
        return str(self)

    @_fluent
    def numberformat(self) -> _NumberFormatMod:
        self._add('numberformat')
        return self._start(_NumberFormatMod())


class _NumberFormatMod(Command):
    @_fluent
    def styled(self, style: NbtDef) -> str:
        self._add('styled', style)
        return str(self)

    @_fluent
    def fixed(self, text: StrOrArg) -> str:
        self._add('fixed', text)
        return str(self)

    @_fluent
    def blank(self) -> str:
        self._add('blank')
        return str(self)


# Changes to these methods should be reflected in the Score class.
class _ScoreboardPlayersMod(Command):
    @_fluent
    def list(self, target: Target = None) -> str:
        self._add('list')
        self._add_opt(as_target(target))
        return str(self)

    @_fluent
    def get(self, score: ScoreName) -> str:
        self._add('get', as_score(score))
        return str(self)

    @_fluent
    def set(self, score: ScoreName, value: IntOrArg) -> str:
        self._add('set', as_score(score), de_int_arg(value))
        return str(self)

    @_fluent
    def add(self, score: ScoreName, value: IntOrArg) -> str:
        self._add('add', as_score(score), de_int_arg(value))
        return str(self)

    @_fluent
    def remove(self, score: ScoreName, value: IntOrArg) -> str:
        self._add('remove', as_score(score), de_int_arg(value))
        return str(self)

    @_fluent
    def reset(self, score: ScoreName | Target | tuple[Target, None]) -> str:
        self._add('reset')
        try:
            score = as_score(score)
            self._add(score)
        except (TypeError, ValueError):
            # if not a valid full score name, it must be just a target
            if isinstance(score, (str, TargetSpec)):
                self._add(as_target(score))
            else:
                if len(score) == 1 or (len(score) == 2 and score[1] is None):
                    self._add(as_target(score[0]))
                else:
                    # An invalid argument to as_score will be most descriptive
                    raise
        return str(self)

    @_fluent
    def enable(self, score: ScoreName) -> str:
        self._add('enable', as_score(score))
        return str(self)

    @_fluent
    def operation(self, score: ScoreName, op: str, source: ScoreName) -> str:
        _in_group(SCORE_OPERATIONS, op)
        # 'MAX' is used elsewhere, this special-cases it
        if op == MAX:
            op = '>'
        self._add('operation', as_score(score), op, as_score(source))
        return str(self)

    @_fluent
    def display(self) -> _DisplayNameMod:
        self._add('display')
        return self._start(_DisplayNameMod())


class _DisplayNameMod(Command):
    @_fluent
    def name(self, targets: TargetSpec, objective: StrOrArg, display_name: StrOrArg = None) -> str:
        self._add('name', as_target(targets), objective)
        self._add_opt(display_name)
        return str(self)

    @_fluent
    def numberformat(self, targets: TargetSpec, score: StrOrArg) -> _NumberFormatMod:
        self._add('numberformat', as_target(targets), score)
        return self._start(_NumberFormatMod())


class _ScoreboardMod(Command):
    @_fluent
    def objectives(self) -> _ScoreboardObjectivesMod:
        self._add('objectives')
        return self._start(_ScoreboardObjectivesMod())

    @_fluent
    def players(self) -> _ScoreboardPlayersMod:
        self._add('players')
        return self._start(_ScoreboardPlayersMod())


class _PlaceMod(Command):
    @_fluent
    def feature(self, feature: StrOrArg, pos: Position = None) -> str:
        self._add('feature', as_resource(feature))
        self._add_opt_pos(pos)
        return str(self)

    @_fluent
    def jigsaw(self, pool: StrOrArg, target_pool: StrOrArg, max_depth: IntOrArg, pos: Position = None) -> str:
        self._add('jigsaw', as_resource(pool), as_resource(target_pool), max_depth)
        self._add_opt_pos(pos)
        return str(self)

    @_fluent
    def structure(self, structure: StrOrArg, /, pos: Position = None) -> str:
        self._add('structure', as_resource(structure))
        self._add_opt_pos(pos)
        return str(self)

    @_fluent
    def template(self, template: StrOrArg, pos: Position = None, rotation: IntOrArg | str = None,
                 mirror: StrOrArg = None, integrity: FloatOrArg = None, seed: IntOrArg = None,
                 action: StrOrArg = None) -> str:
        self._add('template', as_resource(template))
        self._add_opt_pos(pos)
        rotations = {0: NONE, CLOCKWISE_90: 'clockwise_90', COUNTERCLOCKWISE_90: 'counterclockwise_90', 180: '180'}
        if is_arg(rotation):
            rotation = de_arg(rotation)
        elif isinstance(rotation, int):
            try:
                rotation = rotations[rotation]
            except KeyError:
                raise ValueError('Invalid number for rotation')
        self._add_opt(rotation)
        self._add_opt(_in_group(MIRROR_GROUP, mirror))
        if isinstance(integrity, (int, float)) and not (0 <= integrity <= 1):
            raise ValueError(f'integrity must be range [0.0, 1.0] {integrity}')
        self._add_opt(de_float_arg(integrity))
        self._add_opt(de_int_arg(seed))
        self._add_opt(_in_group([STRICT], action))
        return str(self)


class _RideMod(Command):
    @_fluent
    def mount(self, target: Target) -> str:
        self._add('mount', as_single(target))
        return str(self)

    @_fluent
    def dismount(self) -> str:
        self._add('dismount')
        return str(self)


class _ScheduleMod(Command):
    @_fluent
    def function(self, path: StrOrArg | object, time: DurationDef, action: str) -> str:
        try:
            # noinspection PyUnresolvedReferences
            path = path.full_name
        except AttributeError:
            path = de_arg(path)
        self._add('function', as_resource_path(path), as_duration(time), _in_group(SCHEDULE_ACTIONS, action))
        return str(self)

    @_fluent
    def clear(self, path: StrOrArg) -> str:
        self._add('clear', as_resource_path(path))
        return str(self)


class _TagMod(Command):
    @_fluent
    def add(self, tag: StrOrArg) -> str:
        self._add('add', as_name(tag))
        return str(self)

    @_fluent
    def list(self) -> str:
        self._add('list')
        return str(self)

    @_fluent
    def remove(self, tag: StrOrArg) -> str:
        self._add('remove', as_name(tag))
        return str(self)


class _TeamMod(Command):
    @_fluent
    def list(self, team: StrOrArg = None) -> str:
        self._add('list')
        self._add_opt(as_team(team))
        return str(self)

    @_fluent
    def add(self, team: StrOrArg, display_name: StrOrArg = None) -> str:
        self._add('add', as_team(team))
        self._add_opt(as_name(display_name))
        return str(self)

    @_fluent
    def remove(self, team: StrOrArg) -> str:
        self._add('remove', as_team(team))
        return str(self)

    @_fluent
    def empty(self, team: StrOrArg) -> str:
        self._add('empty', as_team(team))
        return str(self)

    @_fluent
    def join(self, team: StrOrArg, target: Target = None) -> str:
        self._add('join', as_team(team))
        self._add_opt(as_target(target))
        return str(self)

    @_fluent
    def leave(self, team: StrOrArg, target: Target = None) -> str:
        self._add('leave', as_team(team), as_target(target))
        return str(self)

    @_fluent
    def modify(self, team: StrOrArg, option: StrOrArg, value: StrOrArg | BoolOrArg) -> str:
        option = as_teamoption(option)
        value_type = team_options[option].type
        if value_type == bool:
            if not isinstance(value, (bool, Arg)):
                raise ValueError(f'{value}: Must be bool')
            value = _bool(value)
        elif value_type == str:
            if not isinstance(value, (str, Arg)):
                raise ValueError(f'{value}: Must be str')
        elif value_type == 'Nbt':
            if not isinstance(value, (str, Nbt, Arg)):
                raise ValueError(f'{value}: Must be NBT or str')
        else:
            if not is_arg(value) and value not in value_type:
                raise ValueError(f'{value}: Must be one of {value_type}')
        self._add('modify', as_team(team), option, value)
        return str(self)


class _TeleportMod(Command):
    @_fluent
    def facing(self, facing: Target | Position, anchor: StrOrArg = None) -> str:
        self._add('facing')
        is_entity = False
        try:
            facing = as_target(facing)
            is_entity = True
            self._add('entity', facing)
            if anchor:
                self._add(_in_group(ENTITY_ANCHOR, anchor))
        except ValueError:
            # Check if the error was from the entity or the anchor
            if is_entity:
                raise
            self._add(*as_position(facing))
            if anchor is not None:
                raise ValueError('anchor not allowed when facing coordinates')
        return str(self)


class _RotateMod(Command):
    @_fluent
    def facing(self, location: Position = None) -> str | _RotateToMod:
        self._add('facing')
        if location is not None:
            self._add(*as_position(location))
            return str(self)
        return self._start(_RotateToMod())


class _RotateToMod(Command):
    @_fluent
    def entity(self, target: Target, anchor: StrOrArg = None) -> str:
        self._add('entity', as_target(target))
        self._add_opt(_in_group(ENTITY_ANCHOR, anchor))
        return str(self)


class _TimeMod(Command):
    @_fluent
    def add(self, amount: DurationDef) -> str:
        self._add('add', as_duration(amount))
        return str(self)

    @_fluent
    def query(self, which: StrOrArg) -> str:
        self._add('query', _in_group(TIME_TYPES, which))
        return str(self)

    @_fluent
    def set(self, new_time: DurationDef) -> str:
        try:
            _in_group(TIME_SPEC, new_time)
        except ValueError:
            new_time = as_duration(new_time)
        self._add('set', new_time)
        return str(self)


class _TestMod(Command):
    _seg_re = r'[a-zA-Z0-9*?]+'
    _selector_re = re.compile(f'{_seg_re}(:{_seg_re})?')

    @classmethod
    def _as_selector(cls, selector: StrOrArg | None, allow_none=True) -> StrOrArg | None:
        if is_arg(selector):
            return de_arg(selector)
        if selector is None:
            if allow_none:
                return selector
            raise ValueError(f'Selector missing')
        if not cls._selector_re.fullmatch(selector):
            raise ValueError(f'Invalid test selector: {selector}')
        return selector

    @_fluent
    def clearall(self, radius: FloatOrArg = None) -> str:
        self._add('clearall')
        self._add_opt(de_float_arg(radius))
        return str(self)

    @_fluent
    def clearthat(self) -> str:
        self._add('clearthat')
        return str(self)

    @_fluent
    def clearthese(self) -> str:
        self._add('clearthese')
        return str(self)

    @_fluent
    def create(self, namespace: StrOrArg, width: IntOrArg = None, height: IntOrArg = None,
               depth: IntOrArg = None) -> str:
        self._add('create', as_resource(namespace))
        self._add_opt(de_int_arg(width), de_int_arg(height), de_int_arg(depth))
        return str(self)

    @_fluent
    def locate(self, selector: StrOrArg) -> str:
        self._add('locate', _TestMod._as_selector(selector))
        return str(self)

    def resetall(self, radius: FloatOrArg = None) -> str:
        self._add('resetall')
        self._add_opt(de_float_arg(radius))
        return str(self)

    @_fluent
    def resetthat(self) -> str:
        self._add('resetthat')
        return str(self)

    @_fluent
    def resetthese(self) -> str:
        self._add('resetthese')
        return str(self)

    def pos(self, variable: StrOrArg) -> str:
        self._add('pos', variable)
        return str(self)

    def run(self, selector: StrOrArg, count: IntOrArg = None, until_failed: BoolOrArg = None,
            rotation_steps: IntOrArg = None, tests_per_row: IntOrArg = None) -> str:
        self._add('run', _TestMod._as_selector(selector))
        self._add_opt(de_int_arg(count), de_arg(until_failed), de_int_arg(rotation_steps), de_int_arg(tests_per_row))
        return str(self)

    def runclosest(self, count: IntOrArg = None, until_failed: BoolOrArg = None) -> str:
        self._add('runclosest')
        self._add_opt(de_int_arg(count), de_arg(until_failed))
        return str(self)

    def runfailed(self, count: IntOrArg = None, until_failed: BoolOrArg = None, rotation_steps: IntOrArg = None,
                  tests_per_row: IntOrArg = None) -> str:
        self._add('runfailed')
        self._add_opt(de_int_arg(count), de_arg(until_failed), de_int_arg(rotation_steps), de_int_arg(tests_per_row))
        return str(self)

    def runmultiple(self, selector: StrOrArg, count: IntOrArg) -> str:
        self._add('runmultiple', _TestMod._as_selector(selector))
        self._add_opt(de_int_arg(count))
        return str(self)

    def runthat(self, count: IntOrArg = None, until_failed: BoolOrArg = None) -> str:
        self._add('runthat')
        self._add_opt(de_int_arg(count), de_arg(until_failed))
        return str(self)

    def runthese(self, count: IntOrArg = None, until_failed: BoolOrArg = None) -> str:
        self._add('runthese')
        self._add_opt(de_int_arg(count), de_arg(until_failed))
        return str(self)

    def stop(self):
        self._add('stop')
        return str(self)

    def verify(self, selector: str) -> str:
        self._add('verify', _TestMod._as_selector(selector))
        return str(self)


class _TickMod(Command):
    @_fluent
    def query(self) -> str:
        self._add('query')
        return str(self)

    @_fluent
    def rate(self, rate: int) -> str:
        self._add('rate', rate)
        return str(self)

    @_fluent
    def freeze(self) -> str:
        self._add('freeze')
        return str(self)

    @_fluent
    def unfreeze(self) -> str:
        self._add('unfreeze')
        return str(self)

    @_fluent
    def step(self, time: int = None) -> str | _TickStopMod:
        self._add('step')
        if time is None:
            return self._start(_TickStopMod())
        self._add(time)
        return str(self)

    @_fluent
    def sprint(self, time: int = None) -> str | _TickStopMod:
        self._add('sprint')
        if time is None:
            return self._start(_TickStopMod())
        self._add(time)
        return str(self)


class _TickStopMod(Command):
    @_fluent
    def __init__(self):
        super().__init__()
        self._used = False

    @_fluent
    def stop(self) -> str:
        self._add('stop')
        self._used = True
        return str(self)

    def __str__(self):
        if not self._used:
            self._add('1')
            return super().__str__()
        return super().__str__()


class _TitleMod(Command):
    @_fluent
    def clear(self) -> str:
        return self._add_str('clear')

    @_fluent
    def reset(self) -> str:
        return self._add_str('reset')

    @_fluent
    def title(self, msg: StrOrArg) -> str:
        return self._add_str('title', _quote(msg))

    @_fluent
    def subtitle(self, msg: StrOrArg) -> str:
        return self._add_str('subtitle', _quote(msg))

    @_fluent
    def actionbar(self, msg: StrOrArg) -> str:
        return self._add_str('actionbar', _quote(msg))

    @_fluent
    def times(self, fade_in: DurationDef, stay: DurationDef, fade_out: DurationDef) -> str:
        self._add('times', as_duration(fade_in), as_duration(stay), as_duration(fade_out))
        return str(self)


class _TriggerMod(Command):
    @_fluent
    def add(self, value: int) -> str:
        self._add('add', value)
        return str(self)

    @_fluent
    def set(self, value: int) -> str:
        self._add('set', value)
        return str(self)


class _WaypointMod(Command):
    @_fluent
    def list(self) -> str:
        self._add('list')
        return str(self)

    @_fluent
    def modify(self, target: Target):
        self._add('modify', as_single(target))
        return self._start(_WaypointModifyMod())


class _WaypointModifyMod(Command):
    @_fluent
    def color(self, color_or_reset: StrOrArg | int, hex_value: IntOrArg = None) -> str:
        """
        Valid invocations include:
        * color('blue')
        * color(Arg('color_name'))
        * color(0xffeeff)  # same as color('hex', 0xffeeff)
        * color('hex', 0xffeeff)
        * color('hex', Arg(rgb))
        * color(RESET)
        """
        self._add('color')
        num = None
        if isinstance(color_or_reset, int):
            num = color_or_reset
        elif color_or_reset == HEX:
            if hex_value is None:
                raise ValueError('hex color not provided')
            elif isinstance(hex_value, int):
                num = hex_value
            else:
                self._add(HEX, de_arg(hex_value))
        else:
            self._add(de_arg(_in_group(TEXT_COLORS + [RESET], color_or_reset)))
        if num is not None:
            num_str = re.sub(r'^000(...)$', '$1', f'{num:06x}')
            if len(num_str) not in (3, 6):
                raise ValueError(f'Invalid hex color: {num_str} ({num}): Must have 3 or 6 digits')
            self._add(HEX, num_str)
        return str(self)

    @_fluent
    def style(self, style_or_reset: StrOrArg = None) -> str | _WaypointStyleSet:
        self._add('style')
        if style_or_reset:
            if style_or_reset != 'reset':
                self._add('set')
            self._add(de_arg(style_or_reset))
            return str(self)
        else:
            return self._start(_WaypointStyleSet())


class _WaypointStyleSet(Command):
    @_fluent
    def set(self, style: StrOrArg) -> str:
        self._add('set', de_arg(style))
        return str(self)


class _WorldBorderWarningMod(Command):
    @_fluent
    def distance(self, distance: float) -> str:
        self._add('distance', distance)
        return str(self)

    @_fluent
    def time(self, time_sec: int) -> str:
        self._add('time', time_sec)
        return str(self)


class _WorldBorderDamageMod(Command):
    @_fluent
    def amount(self, value: float) -> str:
        self._add('amount', value)
        return str(self)

    @_fluent
    def buffer(self, distance: float) -> str:
        self._add('buffer', distance)
        return str(self)


class _WorldBorderMod(Command):
    @_fluent
    def add(self, distance: float, duration_secs: int = None) -> str:
        self._add('add', distance)
        self._add_opt(duration_secs)
        return str(self)

    @_fluent
    def center(self, pos: IntColumn) -> str:
        self._add('center', *as_column(pos))
        return str(self)

    @_fluent
    def damage(self) -> _WorldBorderDamageMod:
        self._add('damage')
        return self._start(_WorldBorderDamageMod())

    @_fluent
    def get(self) -> str:
        self._add('get')
        return str(self)

    @_fluent
    def set(self, diameter: float) -> str:
        self._add('set', diameter)
        return str(self)

    @_fluent
    def warning(self) -> _WorldBorderWarningMod:
        self._add('warning')
        return self._start(_WorldBorderWarningMod())


class _BlockMod(Command):
    def __init__(self):
        super().__init__()
        self._nbt = Nbt()
        self._state = {}

    def __str__(self):
        added = ''
        if self._state:
            added = '[' + ','.join(f'{k}={_quote(v)}' for k, v in self._state.items()) + ']'
        if self._nbt:
            added += str(self._nbt)
        return super().__str__() + added

    @_fluent
    def nbt(self, nbt: NbtDef) -> _BlockMod:
        self._nbt = self._nbt.merge(nbt)
        return self

    @_fluent
    def state(self, state: dict) -> _BlockMod:
        self._state.update(state)
        return self

    @_fluent
    def destroy(self) -> str:
        # Use this, not ._add(): the order of state() and nbt() isn't defined, this makes sure the keyword's after
        return str(self) + ' destroy'

    @_fluent
    def keep(self) -> str:
        return str(self) + ' keep'

    @_fluent
    def replace(self) -> str:
        return str(self) + ' replace'

    @_fluent
    def strict(self) -> str:
        return str(self) + ' strict'


class _ListMod(Command):
    @_fluent
    def uuids(self) -> str:
        self._add('uuids')
        return str(self)


class _AdvancementMod(Command):
    def everything(self):
        self._add('everything')
        return str(self)

    @_fluent
    def only(self, advancement: StrOrArg, criterion: StrOrArg = None) -> str:
        advancement = as_advancement(advancement)
        self._add('only', advancement)
        self._add_opt(criterion)
        return str(self)

    @_fluent
    def from_(self, advancement: StrOrArg) -> str:
        return self._setup('from', advancement)

    @_fluent
    def through(self, advancement: StrOrArg) -> str:
        return self._setup('through', advancement)

    @_fluent
    def until(self, advancement: StrOrArg) -> str:
        return self._setup('until', advancement)

    def _setup(self, param, advancement):
        self._add(param, as_advancement(advancement))
        return str(self)


def advancement(action: StrOrArg, target: Selector) -> _AdvancementMod:
    """Gives or takes an advancement from one or more players.

    :param action: GRANT or REVOKE.
    :param target: The targets.
    """
    cmd = Command()
    action = _to_donate(action, GRANT_REVOKE)
    cmd._add('$advancement', action, target)
    return cmd._start(_AdvancementMod())


def attribute(target: Target, attribute: StrOrArg) -> _AttributeMod:
    """Queries, adds, removes, or sets an entity attribute."""
    cmd = Command()
    cmd._add('$attribute', as_single(target), as_resource(attribute, add_namespace=True))
    return cmd._start(_AttributeMod())


def bossbar() -> _BossbarMod:
    """Creates and modifies a bossbar."""
    cmd = Command()
    cmd._add('$bossbar')
    return cmd._start(_BossbarMod())


def clear(target: Target) -> _ClearClause:
    """Clears items from player inventory."""
    cmd = Command()
    cmd._add('$clear', as_target(target))
    return cmd._start(_ClearClause())


def clone(start_pos: Position = None, end_pos: Position = None,
          dest_pos: Position = None, config: str = None) -> _CloneClause | _CloneFromDimMod:
    """
    Copies blocks from one place to another.

    The dest_type says how to interpret dest_coords, and is one of the following:

    LEAST (default): dest_coords are the lowest coordinates of the destination region. This matches the clone
    command.

    LAST: dest_coords are where the old region's end_pos should be in the new region. That is, the copy of
    the block at end_pos will be placed at these coordinates.

    DELTA: dest_coords is the amount ot shift the whole region. So (10, 0, 0) means to clone the region 10 blocks
    away along the X axis.

    To use the 1.19.4+ syntax, use "clone().from_(...).to(...)". In this form it is the "to" method that takes the
    optional dest_coords interpretation parameter.

    Currently, the only valid config value is "strict". This
    """
    cmd = Command()

    if start_pos is None:
        return cmd._start(_CloneFromDimMod(config))
    if end_pos is None or dest_pos is None:
        raise ValueError('Must give all positions or none of them')

    dest_pos = dest_pos
    cmd._add('$clone', *start_pos, *end_pos, *dest_pos)
    cmd._add_opt(config)
    return cmd._start(_CloneClause())


def damage(target: Target, amount: IntOrArg, type: StrOrArg = None) -> _DamageMod:
    """Applies a set amount of damage to the specified entities."""
    cmd = Command()
    cmd._add('$damage', as_target(target), amount)
    cmd._add_opt(as_resource(type))
    return cmd._start(_DamageMod())


def data() -> _DataMod:
    """Gets, merges, modifies and removes block entity and entity NBT data."""
    cmd = Command()
    cmd._add('$data')
    return cmd._start(_DataMod())


def datapack() -> _DatapackMod:
    """Controls loaded data packs."""
    cmd = Command()
    cmd._add('$datapack')
    return cmd._start(_DatapackMod())


def debug() -> _DebugMod:
    cmd = Command()
    cmd._add('$debug')
    return cmd._start(_DebugMod())


def defaultgamemode(gamemode: StrOrArg) -> str:
    """Sets the default game mode."""
    cmd = Command()
    cmd._add('$defaultgamemode', _in_group(GAMEMODE, gamemode))
    return str(cmd)


def deop(*targets: Target) -> str:
    """Revokes operator status from a player."""
    cmd = Command()
    cmd._add('$deop', *targets)
    return str(cmd)


def dialog() -> _DialogPart:
    """Manages custom dialogs."""
    cmd = Command()
    cmd._add('$dialog')
    return cmd._start(_DialogPart())


def difficulty(difficulty: StrOrArg = None) -> str:
    """Sets the difficulty level."""
    cmd = Command()
    cmd._add('$difficulty')
    if difficulty:
        cmd._add(_in_group(DIFFICULTIES, difficulty))
    return str(cmd)


def effect() -> _EffectAction:
    """Adds or removes status effects."""
    cmd = Command()
    cmd._add('$effect')
    return cmd._start(_EffectAction())


def enchant(target: Target, enchantment: StrOrArg | IntOrArg, level: IntOrArg = None) -> str:
    """Adds an enchantment to a player's selected item."""
    cmd = Command()
    cmd._add('$enchant', as_target(target))
    enchantment = as_enchantment(as_resource(enchantment))
    cmd._add(enchantment)
    if level is not None and enchantment in enchantments:
        max_level = enchantments[enchantment].max_level
        if level not in range(max_level + 1):
            raise ValueError(f'Level not in range [0..{max_level}]')
        cmd._add_opt(level)
    return str(cmd)


def execute() -> _ExecuteMod:
    """Executes a command."""
    cmd = Command()
    cmd._add('$execute')
    return cmd._start(_ExecuteMod())


def experience() -> _ExperienceMod:
    """Adds or removes player experience."""
    cmd = Command()
    cmd._add('$experience')
    return cmd._start(_ExperienceMod())


xp = experience


def fill(start_pos: Position, end_pos: Position, block: BlockDef) -> _FilterClause | str:
    """Fills a region with a specific block."""
    cmd = Command()
    cmd._add('$fill', *start_pos, *end_pos, as_block(block))
    return cmd._start(_FilterClause())


def fillbiome(start_pos: Position, end_pos: Position, biome: StrOrArg) -> _BiomeFilterClause:
    cmd = Command()
    cmd._add('$fillbiome', *start_pos, *end_pos, as_biome(biome))
    return cmd._start(_BiomeFilterClause())
    pass


def forceload() -> _ForceloadMod:
    """Forces chunks to constantly be loaded or not."""
    cmd = Command()
    cmd._add('$forceload')
    return cmd._start(_ForceloadMod())


# We use 'object' here because importing Function would create a circular dependency.
def function(path: StrOrArg | object, arguments: NbtDef = None) -> _FunctionMod:
    """Runs a function."""
    cmd = Command()
    cmd._add('$function', _as_function_path(path))
    if arguments is not None:
        cmd._add_opt(Nbt(arguments))
    return cmd._start(_FunctionMod())


def _as_function_path(path: StrOrArg | object) -> str:
    try:
        # This will work if it is a Function, but I can't import Function, so we just duck type it
        # noinspection PyUnresolvedReferences
        path = path.full_name
    except AttributeError:
        pass
    path = as_resource_path(path)
    return path


def gamemode(gamemode: StrOrArg, target: Target = None) -> str:
    """Sets the gamemode for some set of players."""
    cmd = Command()
    cmd._add('$gamemode', _in_group(GAMEMODE, gamemode))
    cmd._add_opt(as_target(target))
    return str(cmd)


def gamerule(rule: StrOrArg | IntOrArg, value: BoolOrArg | IntOrArg = None) -> str:
    """Sets or queries a game rule value."""
    cmd = Command()
    rule = as_gamerule(rule)
    cmd._add('$gamerule', rule)
    if is_arg(value) or is_arg(rule):
        cmd._add(de_arg(value))
    elif value is not None:
        rule_type = game_rules[rule].rule_type
        if rule_type == int:
            if type(value) != int:
                raise ValueError(f'{rule}: int value required')
            cmd._add(int(value))
        elif rule_type == bool:
            if type(value) != bool:
                raise ValueError(f'{rule}: bool value required')
            cmd._add(_bool(value))
        else:
            raise ValueError(f'{rule_type}: Unexpected rule type {rule_type} (gamerule "{rule}")')
    return str(cmd)


def give(target: Target, item: BlockDef, count: int = None) -> str:
    """Gives an item to a player."""
    cmd = Command()
    cmd._add('$give', as_target(target), item)
    cmd._add_opt(count)
    return str(cmd)


def help(command: StrOrArg = None) -> str:
    """Provides help for commands."""
    cmd = Command()
    cmd._add('$help')
    cmd._add_opt(command)
    return str(cmd)


def item() -> _ItemMod:
    """Manipulates items in inventories."""
    cmd = Command()
    cmd._add('$item')
    return cmd._start(_ItemMod())


def jfr(action: StrOrArg) -> str:
    cmd = Command()
    cmd._add('$jfr', _in_group(START_STOP, action))
    return str(cmd)


def kill(target: Target = None) -> str:
    """Kills entities (players, mobs, items, etc.)."""
    cmd = Command()
    cmd._add('$kill')
    cmd._add_opt(as_target(target))
    return str(cmd)


def list_() -> _ListMod:
    """Lists players on the server."""
    cmd = Command()
    cmd._add('$list')
    return cmd._start(_ListMod())


def locate(kind: StrOrArg, name: StrOrArg) -> str:
    """Locates closest thing of some kind."""
    cmd = Command()
    cmd._add('$locate', _in_group(LOCATABLE, kind), name)
    return str(cmd)


def loot() -> _LootTarget:
    """Drops items from an inventory slot onto the ground."""
    cmd = Command()
    cmd._add('$loot')
    return cmd._start(_LootTarget())


def me(msg: StrOrArg, *msgs: StrOrArg) -> str:
    """Displays a message about the sender."""
    cmd = Command()
    cmd._add('$me', msg, *msgs)
    return str(cmd)


def op(target: Target) -> str:
    """Grants operator status to a player."""
    cmd = Command()
    cmd._add('$op', as_target(target))
    return str(cmd)


def particle(
        particle: ParticleDef, pos: Position = None, delta: Tuple[FloatOrArg, FloatOrArg, FloatOrArg] = None,
        speed: FloatOrArg = None, count: IntOrArg = None, mode: StrOrArg = None, *viewers: EntityDef) -> str:
    """Creates particles."""
    cmd = Command()
    cmd._add('$particle')
    if is_arg(particle):
        particle = de_arg(particle)
    elif isinstance(particle, str):
        particle = Particle(particle)
    elif isinstance(particle, Iterable):
        particle = Particle(*particle)
    else:
        if not isinstance(particle, Particle):
            raise TypeError(f'Unexpected particle def: {particle}')
    cmd._add(particle)
    cmd._add_opt_pos(pos)
    cmd._add_opt_pos(delta)
    if mode and not is_arg(mode):
        mode = _in_group(PARTICLE_MODES, mode)
    cmd._add_opt(speed, count, mode)
    for v in viewers:
        cmd._add(v)
    return str(cmd)


def perf(action: str) -> str:
    """Captures information and metrics about the game for ten seconds."""
    cmd = Command()
    cmd._add('$perf', _in_group(START_STOP, action))
    return str(cmd)


def place() -> _PlaceMod:
    """Used to place a configured feature, jigsaw, or structure at a given location."""
    cmd = Command()
    cmd._add('$place')
    return cmd._start(_PlaceMod())


def playsound(sound: str, source: str, target: Target = None, pos: Position = None, /,
              volume: float = None, pitch: float = None, min_volume: float = None) -> str:
    """Plays a sound."""
    cmd = Command()
    cmd._add('$playsound', as_resource_path(sound), as_resource_path(source))
    cmd._add_opt(as_target(target))
    cmd._add_opt_pos(pos)
    cmd._add_opt(volume, pitch, min_volume)
    return str(cmd)


def publish(allow_commands: BoolOrArg = None, gamemode: StrOrArg = None, port: StrOrArg | IntOrArg = None) -> str:
    cmd = Command()
    cmd._add('$publish')
    cmd._add_opt(_bool(allow_commands), _in_group(GAMEMODE, gamemode, allow_none=True), port)
    return str(cmd)


def random() -> _RandomMod:
    """Randomizing values and controlling random sequences."""
    cmd = Command()
    cmd._add('$random')
    return cmd._start(_RandomMod())


def recipe(action: str, target: Target, recipe_name: StrOrArg) -> str:
    """Gives or takes player recipes."""
    action = _to_donate(action, GIVE_TAKE)
    if recipe_name != '*':
        recipe_name = as_resource_path(recipe_name)
    cmd = Command()
    cmd._add('$recipe', action, as_target(target), recipe_name)
    return str(cmd)


def reload() -> str:
    """Reloads loot tables, advancements, and functions from disk."""
    cmd = Command()
    cmd._add('$reload')
    return str(cmd)


def return_(value: int = None) -> _ReturnMod | str:
    """Returns from a function (stop executing it) with a given result. If non provided, 0 is returned."""
    cmd = Command()
    cmd._add('$return')
    if value is None:
        return cmd._start(_ReturnMod())
    # False is an int, apparently, so we force it to be an actual int
    cmd._add(int(value))
    return str(cmd)


def ride(target: Target) -> _RideMod:
    """Allows entities to mount or dismount other entities. """
    cmd = Command()
    cmd._add('$ride', as_single(target))
    return cmd._start(_RideMod())


def rotate(target: Target, rotation: tuple[FloatOrArg | RelCoord, FloatOrArg | RelCoord] = None) -> str | _RotateMod:
    cmd = Command()
    cmd._add('$rotate', as_single(target))
    if rotation is not None:
        cmd._add(*rotation)
        return str(cmd)
    return cmd._start(_RotateMod())


def say(msg: object, *msgs: object) -> str:
    """Displays a message to multiple players."""
    cmd = Command()
    cmd._add('$say', msg, *msgs)
    return str(cmd)


def schedule() -> _ScheduleMod:
    """Delays the execution of a dir."""
    cmd = Command()
    cmd._add('$schedule')
    return cmd._start(_ScheduleMod())


def scoreboard() -> _ScoreboardMod:
    """Manages scoreboard objectives and players."""
    cmd = Command()
    cmd._add('$scoreboard')
    return cmd._start(_ScoreboardMod())


def seed() -> str:
    """Displays the dir seed."""
    cmd = Command()
    cmd._add('$seed')
    return str(cmd)


def setblock(pos: Position, block: BlockDef, action: StrOrArg = None) -> _BlockMod:
    """Changes a block to another block."""
    if isinstance(block, str) and str(block)[0] == '#':
        raise ValueError(f'{block}: Block tag not allowed here')
    block = as_block(block)
    cmd = Command()
    cmd._add('$setblock', *pos, block)
    if action:
        cmd._add_opt(_in_group(SETBLOCK_ACTIONS, action))
    return cmd._start(_BlockMod())


def setidletimeout(minutes: int) -> str:
    """Sets the time before idle players are kicked from the server."""
    cmd = Command()
    cmd._add('$setidletimeout', minutes)
    return str(cmd)


def setworldspawn(pos: Position = None, yaw: FloatOrArg = None) -> str:
    """Sets the dir spawn."""
    cmd = Command()
    cmd._add('$setworldspawn')
    cmd._add_opt_pos(pos)
    cmd._add_opt(as_yaw(yaw))
    return str(cmd)


def spawnpoint(target: Target = None, pos: Position = None, yaw: Angle | StrOrArg = None) -> str:
    """Sets the spawn point for a player."""
    cmd = Command()
    cmd._add('$spawnpoint')
    cmd._add_opt(as_target(target))
    cmd._add_opt_pos(pos)
    cmd._add_opt(as_yaw(yaw))
    return str(cmd)


def spectate(target: Target = None, watched: Target = None) -> str:
    """Make one player in spectator mode spectate an entity."""
    cmd = Command()
    cmd._add('$spectate', as_single(target))
    cmd._add_opt(as_target(watched))
    return str(cmd)


def spreadplayers(center: Position, distance: float, max_range: float, respect_teams: bool, target: Target,
                  max_height: int = None) -> str:
    """Teleports entities to random locations. This doesn't quite follow the minecraft command syntax because that
    has a weird optional ``under <num>`` parameter in the middle, which is hard to model and, well, weird. As an
    optional value, it appears at the last parameter."""
    cmd = Command()
    cmd._add('$spreadplayers', *center, distance, max_range)
    if max_height is not None:
        cmd._add_opt('under', max_height)
    cmd._add(_bool(respect_teams), as_target(target))
    return str(cmd)


def stopsound(target: Target, /, source: StrOrArg = None, sound: StrOrArg = None) -> str:
    """Stops a sound."""
    cmd = Command()
    cmd._add('$stopsound', as_target(target))
    cmd._add_opt(as_resource_path(source), as_resource_path(sound))
    return str(cmd)


def summon(entity: EntityDef, /, pos: Position = None, nbt: NbtDef | StrOrArg = None) -> str:
    """Summons an entity."""
    entity = as_entity(entity)
    if is_arg(entity):
        entity = Entity(de_arg(entity))
    cmd = Command()
    cmd._add('$summon', entity.id)
    cmd._add_opt_pos(pos)
    if is_arg(nbt):
        cmd._add_opt(de_arg(nbt))
    else:
        e_nbt = Nbt(entity.nbt) if entity.nbt else Nbt()
        tags = e_nbt['Tags'] if 'Tags' in e_nbt else ()
        e_nbt = e_nbt.merge(nbt)
        # Merge tags
        if 'Tags' in e_nbt:
            e_nbt['Tags'] = list(set(e_nbt['Tags']) | set(tags))
        if len(e_nbt) > 0:
            cmd._add_opt(e_nbt)
    return str(cmd)


def tag(target: Target) -> _TagMod:
    """Controls entity tags."""
    cmd = Command()
    cmd._add('$tag', as_target(target))
    return cmd._start(_TagMod())


def team() -> _TeamMod:
    """Controls teams."""
    cmd = Command()
    cmd._add('$team')
    return cmd._start(_TeamMod())


def teammsg(msg: StrOrArg, *msgs: StrOrArg) -> str:
    """An alias of ``/tm``. Specifies the message to send to team."""
    cmd = Command()
    cmd._add('$teammsg', msg, *msgs)
    return str(cmd)


tm = teammsg


def teleport(who_or_to: Target | Position, to: Target | Position = None,
             rotation: float = None) -> str | _TeleportMod:
    """An alias of ``/tp``. Teleports entities."""
    cmd = Command()
    cmd._add('$tp')
    try:
        if to is None:
            cmd._add(as_single(who_or_to))
        else:
            cmd._add(as_target(who_or_to))
    except ValueError:
        cmd._add(*as_position(who_or_to))
    if to is None:
        if rotation is not None:
            raise ValueError('Rotation not allowed without two arguments')
    else:
        try:
            cmd._add(as_single(to))
        except ValueError:
            cmd._add(*as_position(to))
        if rotation is not None:
            cmd._add(_float(rotation))
            return str(cmd)
    return cmd._start(_TeleportMod())


tp = teleport


def tell(target: Target, message: StrOrArg, *msgs: StrOrArg) -> str:
    """Displays a private message to other players."""
    cmd = Command()
    cmd._add('$tell', as_target(target), message, *msgs)
    return str(cmd)


msg = tell
w = tell


def tellraw(target: Target, *message: NbtDef | StrOrArg) -> str:
    """Displays a text message to players."""
    cmd = Command()
    cmd._add('$tellraw', target)
    jl = TextList()
    first = True
    for m in message:
        if first:
            first = False
        else:
            jl.append(Text.as_text(' '))
        jl.append(Text.as_text(m))
    if len(jl) == 1:
        jl = jl[0]
    cmd._add(jl)
    return str(cmd)


def test() -> _TestMod:
    """Run tests"""
    cmd = Command()
    cmd._add('$test')
    return cmd._start(_TestMod())


def tick() -> _TickMod:
    cmd = Command()
    cmd._add('$tick')
    return cmd._start(_TickMod())


def time() -> _TimeMod:
    """Changes or queries the game time."""
    cmd = Command()
    cmd._add('$time')
    return cmd._start(_TimeMod())


def title(target: Target) -> _TitleMod:
    """Manages screen titles."""
    cmd = Command()
    cmd._add('$title', as_target(target))
    return cmd._start(_TitleMod())


def trigger(objective: StrOrArg):
    """Sets a trigger to be activated."""
    cmd = Command()
    cmd._add('$trigger', as_name(objective))
    return cmd._start(_TriggerMod())


def waypoint():
    cmd = Command()
    cmd._add('$waypoint')
    return cmd._start(_WaypointMod())


def weather(weather_name: StrOrArg, duration: DurationDef = None) -> str:
    """Sets the weather."""
    cmd = Command()
    cmd._add('$weather', _in_group(WEATHER_TYPES, weather_name))
    cmd._add_opt(as_duration(duration))
    return str(cmd)


def worldborder() -> _WorldBorderMod:
    """Manages the dir border."""
    cmd = Command()
    cmd._add('$worldborder')
    return cmd._start(_WorldBorderMod())


def comment(text: str, wrap=False):
    """
    Inserts a comment.

    :param text: The text of the comment
    :param wrap: If False, the comment will be the text with each line prepended by a '# '. Otherwise, the text will
     be broken into paragraphs by blank lines, each paragraph will be formatted by textwrap.fill() (to 78 columns),
     and before_cmds each line is prepended by a '# '.
    """
    text = text.strip()
    if wrap:
        orig_paras = re.split(r'\n\s*\n', text)
        new_paras = (textwrap.fill(x, width=78) for x in orig_paras)
        text = '\n\n'.join(new_paras)
    text = text.replace('\n', '\n# ').replace('# \n', '#\n')
    return f'# {text}'


def literal(text: str):
    """Puts the text in as a command without modification or checks."""
    cmd = Command()
    cmd._add(text)
    return cmd


@functools.total_ordering
class Block(Command):
    """This class represents a thing that has NBT values. These include blocks and entities."""

    def __init__(self, id: StrOrArg = None, state=None, nbt=None, *, name: StrOrArg = None):
        """Creates a holder.

        Typically, the ID is an in-game ID, such as 'air' or 'minecraft:smooth_stone', and the name is derived
        from it, such as 'Air' or 'Smooth Stone'. Or the other way around. You could pass 'Smooth Stone' as either the
        ID _or_ the name and get the same result: The ID is checked for being a valid name and if it is not,
        we try to see if we can derive an ID from it, and if so, we use that (id, name) combination.

        The name can include '|' characters, which are used to split it into a tuple of multiple lines for a sign.
        (Unfortunately it is not possible to calculate where such breaks need to happen.) After those splits, the '|' is
        replaced with ' ' for the actual name.

        The possibly-split version of the name is used to set two fields: ``sign_text`` is the tuple resulting from the
        split, and ``full_text`` is that list regularized text for a sign that shows just the name, preferring to
        skip the first line if there are fewer than four lines.

        :param id: The ID of the holder.
        :param name: The name to display to your user, derived from ID if not provided.
        """
        super().__init__()
        id = de_arg(id)
        if (id, name) == (None, None):
            raise ValueError('Must specify at least one of id or name')
        if isinstance(id, str):
            id = id.strip()
        if isinstance(name, str):
            name = name.strip()
        if isinstance(id, str) and not name:
            if re.search('[A-Z |]', id):
                name = id
                id = None
            else:
                name = to_name(id)
        if isinstance(name, str) and not id:
            id = to_id(name)

        self.id = as_item_stack(id)
        self.nbt = Nbt()
        self._add(id)
        if isinstance(id, str):
            self.sign_text = tuple(name.split('|'))
            t = self.sign_text
            if len(t) < 4:
                t = ('',) + t
            t = _ensure_size(t, 4, '')
            self.full_text = tuple(t)
            self.name = name.replace('|', ' ')
        else:
            self.sign_text = name
            self.full_text = name

        if state is None:
            state = {}
        self.merge_nbt(nbt)
        self.state = Nbt()
        self.merge_state(state)

    def __lt__(self, other):
        return self.name < other.name

    @property
    def name(self):
        """The object's name."""
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    def sign_nbt(self, front=True) -> Nbt:
        """The NBT you would use in a sign describing this entity, based on ``full_text``."""
        messages = []
        for i in range(4):
            messages.append(Text.text(self.full_text[i]))
        msgs = {'messages': messages}
        nbt = Nbt()
        if front is not False:
            nbt = nbt.merge({'front_text': msgs})
        if front is not True:
            nbt = nbt.merge({'back_text': msgs})
        return nbt

    def __str__(self):
        added = ''
        if len(self.nbt) > 0:
            added = str(self.nbt)
        s = super().__str__() + added
        if self.state:
            at = len(self.id)
            s = s[:at] + self._state_str() + s[at:]
        return s

    def merge_nbt(self, nbt: NbtDef) -> Block:
        """Merge NBT into our nbt."""
        self.nbt = self.nbt.merge(Nbt.as_nbt(nbt))
        return self

    def merge_state(self, state: Mapping) -> Block:
        """Merge state into our state."""
        self.state = self.state.merge(Nbt.as_nbt(state))
        return self

    @staticmethod
    def _state_value(v):
        if isinstance(v, bool):
            return _bool(v)
        return str(v)

    def _state_str(self):
        return self.__class__.state_str(self.state)

    @classmethod
    def state_str(cls, nbt: NbtDef):
        nbt = Nbt.as_nbt(nbt)
        comma = ', ' if Nbt.use_spaces else ','
        return '[' + comma.join((k + '=' + cls._state_value(v)) for k, v in nbt.items()) + ']'


class Entity(Block):
    """This class supports operations useful for an entity. """

    def __init__(self, id: StrOrArg = None, nbt: NbtDef = None, components: NbtDef = None, *, name: StrOrArg = None,
                 state: NbtDef = None):
        """
        Creates a new entity object. See ``NbtHolder.__init__()`` for interpretation of ``id`` and ``name``.

        Note that the nbt comes before the components, but that "components" is just another name for "state",
        which comes before nbt in the Block superclass. This is because for entities, components (state) are much
        rarer than nbt, but for blocks it is the other way around. Although functionally "components" and "state" are
        the same thing in pynecraft -- that is, they behave the same, yield the same strings, etc. -- they are
        different in Minecraft terminology. You can ignore this and treat an Entity has having state, or you can
        respect it and treat it as having components. It's up to you.

        :param id: The entity ID.
        :param nbt: Any NBT for the entity.
        :param components: Any component data for the entity. This just an alias for Block's state field, to
                        be compatible with terminology. But syntacitically they behave the same.
        :param name: The entity's human-friendly name.
        :param state: Can be used instead of 'components', but you can't specify both
        """
        if state:
            if components:
                raise ValueError('Specify either state or components, not both')
            components = state
        self._custom_name = False
        self._custom_name_visible = False
        self._attributes = Nbt()
        id = de_arg(id)
        super().__init__(id, components, nbt, name=name)

    @property
    def components(self):
        """The object's name."""
        return self.state

    def merge_components(self, components: NbtDef) -> Entity:
        super().merge_state(components)
        return self

    @Block.name.setter
    def name(self, name: str):
        """Sets the entity name and, if we're managing it, the custom name."""
        Block.name.fset(self, name)
        self._update_custom_name()

    def custom_name(self, manage: bool = True) -> Entity:
        """Sets whether to manage the 'CustomName' NBT tag along with the name. Default value is True. """
        self._custom_name = manage
        self._update_custom_name()
        return self

    def custom_name_visible(self, v: bool) -> Entity:
        """Sets whether the custom name is visible. If so, this implies ``custom_name(True)``."""
        self._custom_name_visible = v
        if v:
            self.custom_name(v)
        self._update_custom_name()
        return self

    def _update_custom_name(self):
        if self._custom_name:
            self.merge_nbt({'CustomName': self.name})
            self.merge_nbt({'CustomNameVisible': self._custom_name_visible})
        else:
            self.nbt.pop('CustomName')
            self.nbt.pop('CustomNameVisible')

    def tag(self, *tags: StrOrArg) -> Entity:
        """Add one or more tags."""
        self.nbt.get_list('Tags').extend(tags)
        return self

    def passenger(self, entity: EntityDef) -> Entity:
        """Adds a passenger."""
        passengers = self.nbt.get_list('Passengers')
        e_nbt = entity.nbt
        e_nbt['id'] = entity.id
        passengers.append(e_nbt)
        return self

    @staticmethod
    def _summon_clean(nbt: NbtDef, facing: FacingDef) -> Tuple[Nbt, Facing]:
        if not nbt:
            nbt = Nbt()
        else:
            nbt = Nbt.as_nbt(nbt)
        if facing:
            facing = as_facing(facing)
            # Item frames use 'facing' instead of rotation, which they use for something else (natch).
            nbt = nbt.merge({'Rotation': facing.rotation, 'Facing': facing.number})
        return nbt, facing

    def summon(self, pos: Position, nbt: NbtDef = None, facing: FacingDef = None) -> str:
        """Summons an instance of this entity, optionally with added NBT and a specified facing direction."""
        nbt, facing = self._summon_clean(nbt, facing)
        return summon(self, pos, nbt)

    def full_id(self) -> str:
        """Returns a qualified id, adding 'minecraft:' if no namespace was given at construction."""
        if isinstance(id, Arg):
            return str(self.id)
        if self.id.find(':') >= 0:
            return self.id
        return 'minecraft:' + self.id


class Particle(Command):
    def __init__(self, id: StrOrArg, state: NbtDef = None):
        super().__init__()
        self.id = de_arg(id)
        if isinstance(self.id, str):
            self.id = as_particle(id)
        self.state = Nbt.as_nbt(state) if state else Nbt()
        self._add(self.id)

    def __str__(self):
        s = super().__str__()
        if self.state:
            s += str(self.state)
        return s

    @classmethod
    def _3_color(cls, color):
        if is_arg(color):
            return de_arg(color)
        else:
            return (de_float_arg(color[0]), de_float_arg(color[1]), de_float_arg(color[2]))

    @classmethod
    def _4_color(cls, color):
        if is_int_arg(color):
            return de_int_arg(color)
        else:
            return (de_float_arg(color[0]), de_float_arg(color[1]), de_float_arg(color[2]), de_float_arg(color[3]))

    @classmethod
    def block(cls, block: BlockDef, type: StrOrArg = BLOCK, state: Arg | NbtDef = None) -> Particle:
        p = Particle(_in_group(BLOCK_PARTICE_TYPES, type))
        if (is_arg(block) or isinstance(block, str)) and state is None:
            p.state['block_state'] = de_arg(block)
        else:
            block = as_block(block)
            block_state = Nbt(block.state)
            if state:
                if is_arg(state):
                    if block_state:
                        raise ValueError('Block state exists, but provided state is Arg()')
                    block_state = de_arg(state)
                else:
                    block_state.update(state)
            p.state['block_state'] = {'Name': block.id, 'Properties': block_state}
        return p

    @classmethod
    def dust(cls, color: Tuple[FloatOrArg, FloatOrArg, FloatOrArg] | Arg, scale: FloatOrArg = 1) -> Particle:
        p = Particle('dust')
        p.state['color'] = cls._3_color(color)
        p.state['scale'] = de_int_arg(scale)
        return p

    @classmethod
    def dust_color_transition(cls, from_color: Tuple[FloatOrArg, FloatOrArg, FloatOrArg] | Arg,
                              to_color: Tuple[FloatOrArg, FloatOrArg, FloatOrArg] | Arg,
                              scale: FloatOrArg = 1) -> Particle:
        p = Particle('dust_color_transition')
        p.state['from_color'] = cls._3_color(from_color)
        p.state['to_color'] = cls._3_color(to_color)
        p.state['scale'] = de_int_arg(scale)
        return p

    @classmethod
    def entity_effect(cls, color: Tuple[FloatOrArg, FloatOrArg, FloatOrArg, FloatOrArg] | IntOrArg) -> Particle:
        p = Particle('entity_effect')
        p.state['color'] = cls._4_color(color)
        return p

    @classmethod
    def item(cls, item: EntityDef) -> Particle:
        p = Particle('item')
        if is_arg(item) or isinstance(item, str):
            p.state['item'] = de_arg(item)
        else:
            item = as_entity(item)
            p.state['item'] = {'id': item.id, 'components': item.components}
        return p

    @classmethod
    def sculk_charge(cls, roll: FloatOrArg) -> Particle:
        p = Particle('sculk_charge')
        p.state['roll'] = de_float_arg(roll)
        return p

    @classmethod
    def shriek(cls, delay: FloatOrArg) -> Particle:
        p = Particle('shriek')
        p.state['delay'] = de_float_arg(delay)
        return p

    @classmethod
    def vibration(cls, destination: Arg | NbtDef, arrival_in_ticks: IntOrArg) -> Particle:
        p = Particle('vibration')
        if is_arg(destination):
            p.state['destination'] = de_arg(destination)
        else:
            p.state['destination'] = Nbt.as_nbt(destination)
        p.state['arrival_in_ticks'] = de_int_arg(arrival_in_ticks)
        return p


class _Evaluate:
    """Internal class used to turn expressions involving scores into a series of commands."""
    _scratch_objective = '__scratch'

    _constant_ops = {
        PLUS: lambda x, y: x + y,
        MINUS: lambda x, y: x - y,
        DIV: lambda x, y: x // y,  # This is how the "/=" operator works with scores, so we keep it for the constants.
        MOD: lambda x, y: x % y,
    }

    def __init__(self, score: Score, top: BinaryOp):
        self.score = score
        self.top = top
        self.commands: list[Command | str] = []
        self.scratches = set()
        self.scratches_used = False
        self.score_scratch = None
        self.at_left = True
        self._generate(score, top)

    def _generate(self, score, node) -> ScoreValue:
        """Generates the commands needed by this node. Evaluates lhs and rhs recursively."""
        lhs = self._resolve(score, node.lhs)
        scratch = self._next_scratch()
        try:
            self.at_left = False
            rhs = self._resolve(scratch, node.rhs)
            if isinstance(lhs, (int, float)) and isinstance(rhs, (int, float)):
                return self._as_constant(node)
            if isinstance(lhs, (int, float)) or score is not lhs:
                self.append(score.set(lhs))
            if isinstance(rhs, (int, float)):
                if node.op == PLUS:
                    self.append(score.add(rhs))
                elif node.op == MINUS:
                    self.append(score.remove(rhs))
                else:
                    self.append(scratch.set(rhs))
                    self.append(score.operation(node.op, scratch))
            else:
                self.append(score.operation(node.op, rhs))
            return score
        finally:
            self._free_scratch(scratch)

    def _resolve(self, score: Score, node: ScoreValue | BinaryOp) -> int | float | Score:
        """Turns a node (either lhs or rhs) into a value or a Score. Recurses if needed into _generate() for nodes."""
        if isinstance(node, (int, float)):
            return node
        if isinstance(node, Score):
            # If the value of the final target score is used in the expression, and this expression isn't the left-most
            # node, we must store the value before assigning to the variable. For example, with x = 3 + x, we need a
            # scratch variable to hold the value of 'x', because the operation resolves into "x = 3, x += x" otherwise.
            # But x = x + 3 has x at the leftmost side, and it resolves to "x += 3", so x doesn't need to be saved.
            if node is not self.score or self.at_left:
                return node
            if self.score_scratch is None:
                self.score_scratch = self._next_scratch()
                self.append(self.score_scratch.set(self.score))
            return self.score_scratch
        if isinstance(node, (str, Command)):
            node = str(node)
            self.append(score.set(node))
            return score
        return self._generate(score, node)

    def append(self, command):
        if re.search(fr'\bt[0-9]{{2}} {self._scratch_objective}', command):
            if not self.scratches_used:
                # noinspection PyArgumentList
                self.append(scoreboard().objectives().add(self._scratch_objective, DUMMY))
                self.scratches_used = True
        self.commands.append(command)

    def _as_constant(self, node) -> int | float:
        """Turns an operation on a pair of values into a value."""
        return self._constant_ops[node.op](node.lhs, node.rhs)

    def _next_scratch(self) -> Score:
        """Returns the next unused scratch value."""
        for i in range(0, 100):
            name = f't{i:02d}'
            if name not in self.scratches:
                self.scratches.add(name)
                return Score(name, self._scratch_objective)
        raise ValueError('Expression requires more than 100 scratch values')

    def _free_scratch(self, scratch: Score):
        """Removes scratch variable from the 'used' set."""
        assert isinstance(scratch.target, User)
        self.scratches.remove(scratch.target.name)


class Expression:
    """Represents an expression of scores, or a single score, and operations upon it that can be used to generate a
    series of commands that will evaluate it.

    Evaluating expressions often require some intermediate scratch values. These will be created in "the scratch
    objective", which by default is '__scratch', though you can change that. They will be reused where possible.

    The operators supported are ``+``, ``-``, ``*``, ``//``, and ``%``, and are supported against scores and
    constants in any order, and the assignment versions as well (``+=``, etc.). Unary ``+`` and ``-`` are also
    supported. Floor division (``//``) is supported because that is the definition of the division in the
    ``scoreboard players operation`` command.
    """

    @staticmethod
    def scratch_objective() -> str:
        """Returns the objective in which scratch variables will be created. By default, this is '__scratch'"""
        return _Evaluate._scratch_objective

    @staticmethod
    def set_scratch_objective(objective: str) -> None:
        """Sets the objective in which scratch variables will be created."""
        _Evaluate._scratch_objective = objective

    def __add__(self, other: ScoreValue) -> BinaryOp:
        return BinaryOp(self, PLUS, other)

    def __sub__(self, other: ScoreValue) -> BinaryOp:
        return BinaryOp(self, MINUS, other)

    def __mul__(self, other: ScoreValue) -> BinaryOp:
        return BinaryOp(self, MULT, other)

    def __floordiv__(self, other: ScoreValue) -> BinaryOp:
        return BinaryOp(self, DIV, other)

    def __mod__(self, other: ScoreValue) -> BinaryOp:
        return BinaryOp(self, MOD, other)

    def __radd__(self, other: ScoreValue) -> BinaryOp:
        return BinaryOp(other, PLUS, self)

    def __rsub__(self, other: ScoreValue) -> BinaryOp:
        return BinaryOp(other, MINUS, self)

    def __rmul__(self, other: ScoreValue) -> BinaryOp:
        return BinaryOp(other, MULT, self)

    def __rfloordiv__(self, other: ScoreValue) -> BinaryOp:
        return BinaryOp(other, DIV, self)

    def __rmod__(self, other: ScoreValue) -> BinaryOp:
        return BinaryOp(other, MOD, self)

    def __iadd__(self, other: ScoreValue) -> BinaryOp:
        return BinaryOp(self, PLUS, other)

    def __isub__(self, other: ScoreValue) -> BinaryOp:
        return BinaryOp(self, MINUS, other)

    def __imul__(self, other: ScoreValue) -> BinaryOp:
        return BinaryOp(self, MULT, other)

    def __ifloordiv__(self, other: ScoreValue) -> BinaryOp:
        return BinaryOp(self, DIV, other)

    def __imod__(self, other: ScoreValue) -> BinaryOp:
        return BinaryOp(self, MOD, other)

    def __neg__(self):
        return self * -1

    def __pos__(self):
        return self


@dataclasses.dataclass
class BinaryOp(Expression):
    """A binary expression involving scores values, or other expressions."""
    lhs: ScoreValue | Expression
    op: str
    rhs: ScoreValue | Expression


class Score(Command, Expression):
    """
    This class represents a score, and provides simpler mechanisms for generating commands to use and manipulate it.
    """

    # noinspection PyArgumentList
    _cmd_base = scoreboard().players()

    def __init__(self, target: Target, objective: StrOrArg):
        """Creates a new score.

        :param target: The score's name.
        :param objective: The score's objective name.
        """
        super().__init__()
        if target is None or objective is None:
            raise ValueError('Must give both target and objective')
        self.target = as_target(target)
        self.objective = as_name(objective)
        self._add(target, objective)

    def __eq__(self, other: Score) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.target == other.target and self.objective == other.objective

    def __hash__(self):
        return hash((self.target, self.objective))

    def init(self, value: IntOrArg = 0) -> Iterable[str]:
        """Initializes the score by ensuring the objective exists, and setting its value to the provided value."""
        # noinspection PyArgumentList
        return (scoreboard().objectives().add(self.objective, DUMMY)), (self.set(de_int_arg(value)))

    def get(self) -> str:
        """Return a 'get' command for the score."""
        return self._cmd().get(self)

    def set(self, value: IntOrArg | Command | Score | Expression) -> str | list[Command]:
        """
        Returns a 'set' command for the score. If the value is a command, returns a command that sets the value to
        the result of that command. If the value is an expression, returns the commands required to set this score to
        the value of that expression.
        """
        if isinstance(value, int) or is_int_arg(value):
            return self._cmd().set(self, de_int_arg(value))
        elif isinstance(value, Score):
            return self._cmd().operation(self, EQ, value)
        elif isinstance(value, BinaryOp):
            return _Evaluate(self, value).commands
        else:
            return str(execute().store(RESULT).score(self).run(value))

    def add(self, value: IntOrArg) -> str:
        """Returns an 'add' command for the score."""
        return self._cmd().add(self, de_int_arg(value))

    def remove(self, value: IntOrArg) -> str:
        """Return sa 'remove' command for the score."""
        return self._cmd().remove(self, de_int_arg(value))

    def reset(self) -> str:
        """Returns a 'reset' command for the score."""
        return self._cmd().reset(self)

    def enable(self) -> str:
        """Returns an 'enable' command for the score."""
        return self._cmd().enable(self)

    def operation(self, op: str, source: ScoreName) -> str:
        """Returns an 'operation' command for the score. The operation must be in ``SCORE_OPERATION``."""
        return self._cmd().operation(self, op, source)

    @staticmethod
    def _cmd():
        return Score._cmd_base


ScoreValue = Union[str, int, float, Command, Score, BinaryOp]


class TextList(UserList, TextHolder):
    """A list as part of as TextHolder structure,"""

    def content(self):
        return self

    def __str__(self):
        comma = ', ' if Nbt.use_spaces else ','
        return '[' + comma.join(str(x) for x in self) + ']'


class Text(Nbt, TextHolder):
    """This class represents TextHolder.

    You should mostly use the various static factory methods to get a well-formed TextHolder component.
    """

    def __init__(self, txt: StrOrArg | Mapping = None):
        if isinstance(txt, str) and not is_arg(txt):
            super().__init__({'text': de_arg(txt)})
        else:
            super().__init__(txt)

    def __str__(self):
        if len(self) == 1 and 'text' in self:
            to_str = Nbt.to_str(self['text'])
            return to_str
        return super().__str__()

    @classmethod
    def text(cls, txt: StrOrArg) -> Text:
        """Returns a TextHolder node."""
        return cls({'text': de_arg(txt)})

    @classmethod
    def html_text(cls, html: str) -> TextList[Text]:
        """Returns a TextHolder node populated from some HTML."""
        parser = _ToText()
        parser.feed(html)
        parser.close()
        return parser.text()

    @classmethod
    def translate(cls, translation_id: StrOrArg, *texts: StrOrArg, fallback: StrOrArg = None) -> Text:
        """Returns a rich text translation node."""
        if not isinstance(texts, list):
            texts = list(texts)
        else:
            texts = texts[:]
        elem = {'translate': de_arg(translation_id), 'with': de_arg(texts)}
        if fallback:
            elem['fallback'] = de_arg(fallback)
        return cls(elem)

    @classmethod
    def score(cls, score: ScoreName) -> Text:
        """Returns a TextHolder score node. Cannot use macro for the entire score, though you can for the components."""
        score = as_score(score)
        return cls({'score': {'name': str(score.target), 'objective': de_arg(score.objective)}})

    @classmethod
    def selector(cls, target: Target | StrOrArg, sep_color: StrOrArg = None, sep_text: StrOrArg = None) -> Text:
        """Returns a TextHolder selector node."""
        jt = cls()
        jt['selector'] = str(as_target(target))
        if sep_color:
            jt.setdefault('separator', {}).update({'color': _in_group(COLORS, de_arg(sep_color))})
        if sep_text is not None:
            jt.setdefault('separator', {}).update({'text': de_arg(sep_text)})
        return jt

    @classmethod
    def keybind(cls, keybind_id: StrOrArg) -> Text:
        """Returns a TextHolder keybinding node."""
        return cls({'keybind': de_arg(keybind_id)})

    @classmethod
    def nbt(cls, data_target: DataTarget, resource_path: StrOrArg, interpret: BoolOrArg = None,
            separator: StrOrArg = None) -> Text:
        """Returns a TextHolder NBT node."""
        target_key, target_value = data_target_str(data_target).split(' ', 1)
        jt = cls({'nbt': as_resource_path(resource_path), target_key: target_value})
        jt['source'] = target_key
        jt[target_key] = target_value
        if interpret is not None:
            jt['interpret'] = de_arg(interpret)
        if separator is not None:
            jt['separator'] = de_arg(separator)
        return jt

    def content(self):
        return dict(self)

    def extra(self, *extras: Text | StrOrArg) -> Text:
        """Adds an ``extra`` field to rich text."""
        if 'extra' not in self:
            self['extra'] = []
        cur = self['extra']
        cur.extend(de_arg(extras))
        return self

    def color(self, color: StrOrArg) -> Text:
        """Adds a ``color`` field to rich text."""
        if not (isinstance(color, str) and color[0] == '#'):
            color = _in_group(TEXT_COLORS, de_arg(color))
        self['color'] = color
        return self

    def font(self, font: StrOrArg) -> Text:
        """Adds a ``font`` field to rich text."""
        self['font'] = de_arg(as_resource_path(font))
        return self

    def bold(self, v: BoolOrArg = True) -> Text:
        """Adds a ``bold`` field to rich text."""
        self['bold'] = de_arg(v)
        return self

    def italic(self, v: BoolOrArg = True) -> Text:
        """Adds a ``italic`` field to rich text."""
        self['italic'] = de_arg(v)
        return self

    def underlined(self, v: BoolOrArg = True) -> Text:
        """Adds an ``underline`` field to rich text."""
        self['underlined'] = de_arg(v)
        return self

    def strikethrough(self, v: BoolOrArg = True) -> Text:
        """Adds a ``strikethrough`` field to rich text."""
        self['strikethrough'] = de_arg(v)
        return self

    def obfuscated(self, v: BoolOrArg = True) -> Text:
        """Adds an ``obfuscated`` field to rich text."""
        self['obfuscated'] = de_arg(v)
        return self

    def plain(self) -> Text:
        """Resets all text attributes in this node."""
        for v in 'italic', 'bold', 'underlined', 'strikethrough', 'obfuscated':
            self[v] = False
        return self

    def insertion(self, to_insert: StrOrArg) -> Text:
        """Adds an ``insertion`` field to rich text."""
        self['insertion'] = de_arg(to_insert)
        return self

    def click_event(self) -> _TextClickEventAction:
        """Adds a ``click_event`` field to rich text."""
        v = self['click_event'] = _TextClickEventAction(self)
        return v

    def hover_event(self) -> _TextHoverAction:
        """Adds a ``hover_event`` field to rich text."""
        v = self['hover_event'] = _TextHoverAction(self)
        return v

    @classmethod
    def as_text(cls, text: Mapping | str | Text) -> Mapping:
        """Returns a Text object built from the given mapped values."""
        if text is None or isinstance(text, Text):
            return text
        if is_arg(text):
            return de_arg(text)
        if isinstance(text, str):
            return Text.text(text)
        elif isinstance(text, Mapping):
            return cls(text)
        else:
            raise ValueError(f'{text}: Not a dictionary')


MappingOrArg = Union[Mapping, StrOrArg]
Target = Union[StrOrArg, TargetSpec]
ScoreName = Union[Score, Tuple[Target, StrOrArg]]
BlockDef = Union[StrOrArg, Block, Tuple[StrOrArg, MappingOrArg], Tuple[StrOrArg, MappingOrArg, MappingOrArg]]
EntityDef = Union[StrOrArg, Entity, Tuple[StrOrArg, MappingOrArg]]
ParticleDef = Union[StrOrArg, Particle, Tuple[StrOrArg, MappingOrArg]]
TextDef = Union[Text, dict, StrOrArg]
SignMessage = Union[StrOrArg, NbtDef, None]
SignMessages = Iterable[SignMessage]
SignCommand = Union[StrOrArg, Command, NbtDef, Callable[[Union[Text]], Text], None]
SignCommands = Iterable[SignCommand]
Commands = Iterable[Union[Command, str]]
RawDataTarget = Union[Position, TargetSpec, StrOrArg]
DataTarget = Union[RawDataTarget, DataTargetBase]
ItemTarget = Union[Position | EntityDef]
SomeBlockDefs = Union[BlockDef, Iterable[BlockDef]]
SomeMappings = Union[Mapping, Iterable[Mapping]]


def lines(*orig: any) -> list[str]:
    """Flatten a tree of commands into a one-line-per-command flat list."""
    return _lines([], orig)


def _lines(result: list[str], orig: any) -> list[str]:
    for item in orig:
        if isinstance(item, str):
            item = item.rstrip()
            if item.find('\n') >= 0:
                result.extend(item.split('\n'))
            else:
                result.append(item)
        elif isinstance(item, Iterable):
            _lines(result, item)
        elif item is not None:
            result.append(str(item))
    return result
