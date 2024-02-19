"""Contains various data about vanilla Minecraft."""
from __future__ import annotations

import re
from collections import UserDict
from enum import Enum
from importlib.resources import files

from ._utils.fetch_things import ItemFetcher
from .base import COLORS, Nbt, NbtDef, to_id, to_name
from .commands import Block, Entity
from .enums import PotterySherd
from .simpler import Item, as_color_num

blocks: dict[str, Block] = {}
"""All blocks by name. See ``block_items`` if you want an item for a block."""
blocks_by_id: dict[str, Block] = {}
"""All blocks by ID."""
items: dict[str, Item] = {}
"""All items by name. Does not include items for blocks, but see ``block_items``."""
items_by_id: dict[str, Item] = {}
"""All items by ID."""
mobs: dict[str, Entity] = {}
mobs_by_id: dict[str, Entity] = {}

must_give_items: dict[str, Item] = {}
"""Items that are not in the creative inventory, by name."""
must_give_items_by_id: dict[str, Item] = {}
"""Items that are not in the creative inventory, by ID."""
operator_menu: dict[str, Item] = {}
"""Items that are only in the creative inventory if the 'Operator Menu' option is turned on."""


def __read_things(which: str, ctor):
    all_things = {}
    with (files(__package__).joinpath(f'all_{which}.txt')).open() as fp:
        for name in fp.readlines():
            name = name.strip()
            if not name or name[0] == '#':
                continue
            try:
                desc, id = re.split(r'\s*/\s*', name)
            except ValueError:
                id = desc = name
            thing = ctor(to_id(id), name=desc)
            all_things[desc] = thing

    return all_things, dict((t.id, t) for t in sorted(all_things.values(), key=lambda t: t.id))


def __read_lists():
    global blocks, blocks_by_id, items, items_by_id, must_give_items, must_give_items_by_id, mobs, mobs_by_id, \
        operator_menu
    blocks, blocks_by_id = __read_things('blocks', Block)
    items, items_by_id = __read_things('items', Block)
    mobs, mobs_by_id = __read_things('mobs', Entity)

    for item_name in ItemFetcher.must_give:
        item = must_give_items[item_name] = items[item_name]
        must_give_items_by_id[item.id] = item
        if item_name in ItemFetcher.operator_menu:
            operator_menu[item_name] = items[item_name]


__read_lists()


class _ItemForBlockDict(UserDict):
    """
    Dict that will return an Item(foo) for any foo that is a block, but does _not_ consider these in the dict. This
    lets the user say ``block_items['Oak Planks']`` and get a value, but also to ask if there is a special item for
    oak planks by testing ``'Oak Planks' in block_items``, which will be False. This works for the block names and
    block IDs.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        bi = args[0]
        for k, v in bi.items():
            try:
                block = blocks[k]
                self[block.id] = v
            except KeyError:
                pass

    def __getitem__(self, item):
        if item not in self:
            if item in blocks:
                return Item(item)


block_items = _ItemForBlockDict({
    'Bamboo Shoot': Item('Bamboo'),
    'Beetroots': Item('Beetroot Seeds'),
    'Carrots': Item('Carrot'),
    'Cave Vines': Item('Glow Berries'),
    'Cocoa': Item('Cocoa Beans'),
    'Fire': Item('Campfire'),
    'Lava': Item('Lava Bucket'),
    'Melon Stem': Item('Melon Seeds'),
    'Pumpkin Stem': Item('Pumpkin Seeds'),
    'Potatoes': Item('Potato'),
    'Powder Snow': Item('Powder Snow Bucket'),
    'Redstone Wire': Item('Redstone'),
    'Soul Fire': Item('Soul Campfire'),
    'Sweet Berry Bush': Item('Sweet Berries'),
    'Tall Seagrass': Item('Seagrass'),
    'Tripwire': Item('String'),
    'Water': Item('Water Bucket'),
})
"""Items for each kind of block. By default, this is simply ``Item(key)``, but there are some special cases where
there is no item for a block. This map takes a reasonable guess at the most reasonable item."""


class Color:
    """Represents a Minecraft color."""
    _num = 0

    def __init__(self, name: str, leather: int):
        self.name = name
        self.id = to_id(name)
        self.leather = leather
        self.num = Color._num
        Color._num += 1

    def __str__(self):
        return self.name


colors = (
    Color('White', 0xf9fffe),
    Color('Orange', 0xf9801d),
    Color('Magenta', 0xc74ebd),
    Color('Light Blue', 0x3ab3da),
    Color('Yellow', 0xfed83d),
    Color('Lime', 0x80c71f),
    Color('Pink', 0xf38baa),
    Color('Gray', 0x474f52),
    Color('Light Gray', 0x9d9d97),
    Color('Cyan', 0x169c9c),
    Color('Purple', 0x8932b8),
    Color('Blue', 0x3c44aa),
    Color('Brown', 0x835432),
    Color('Green', 0x5e7c16),
    Color('Red', 0xb02e26),
    Color('Black', 0x1d1d21),
)
"""The standard colors."""


class Instrument:
    """Data about a note block instrument."""

    def __init__(self, id, name, exemplar):
        """
        Creates a new instrument.

        :param id: The ID used in the note block's NBT
        :param name: The human-friendly name for the instrument.
        :param exemplar: One block you can put under the note block to get this instrument. Some instruments have
            several.
        """
        self.id = id
        self.name = name
        self.exemplar = exemplar


instruments = (
    Instrument('hat', 'High Hat', Block('Glass')),
    Instrument('basedrum', 'Base Drum', Block('Stone')),
    Instrument('snare', 'Snare Drum', Block('Sand')),
    Instrument('xylophone', 'Xylophone', Block('Bone Block')),
    Instrument('chime', 'Chime', Block('Packed Ice')),
    Instrument('harp', 'Harp', Block('grass_block', name='Other')),
    Instrument('guitar', 'Guitar', Block('white_wool', name='Wool')),
    Instrument('bass', 'Bass', Block('oak_planks', name='Wood')),
    Instrument('flute', 'Flute', Block('Clay')),
    Instrument('bell', 'Bell', Block('Gold Block')),
    Instrument('iron_xylophone', 'Iron Xylophone', Block('Iron Block')),
    Instrument('cow_bell', 'Cow Bell', Block('Soul Sand')),
    Instrument('didgeridoo', 'Didgeridoo', Block('Pumpkin')),
    Instrument('bit', 'Bit', Block('Emerald Block')),
    Instrument('banjo', 'Banjo', Block('Hay Block')),
    Instrument('pling', 'Pling', Block('Glowstone')),
)
"""The instruments note blocks can play."""


class Horse(Entity):
    """Data about a horse."""

    class Color(Enum):
        WHITE = 0
        CREAMY = 1
        CHESTNUT = 2
        BROWN = 3
        BLACK = 4
        GRAY = 5
        DARK_BROWN = 6

        def __int__(self):
            return self.value

    class Markings(Enum):
        NONE = 0 * 256
        WHITE = 1 * 256
        WHITE_FIELD = 2 * 256
        WHITE_SPOTS = 3 * 256
        BLACK_DOTS = 4 * 256

        def __int__(self):
            return self.value

    # Variants

    def __init__(self, name: str = None, color: int | Color = Color.WHITE, markings: int | Markings = Markings.NONE,
                 nbt: NbtDef = None):
        self.color = Horse.Color(color)
        self.markings = Horse.Markings(markings)
        self.variant = int(color) + int(markings)
        super().__init__('horse', name=name, nbt={'Variant': self.variant})
        if nbt:
            self.merge_nbt(nbt)
        self.tag_name = f'{to_id(name)}_horses'


horses = (
    Horse('White', Horse.Color.WHITE),
    Horse('Creamy', Horse.Color.CREAMY),
    Horse('Chestnut', Horse.Color.CHESTNUT),
    Horse('Brown', Horse.Color.BROWN),
    Horse('Black', Horse.Color.BLACK),
    Horse('Gray', Horse.Color.GRAY),
    Horse('Dark Brown', Horse.Color.DARK_BROWN),
)
"""The non-horse horses."""
other_horses = (
    Entity('Mule'),
    Entity('Donkey'),
    Entity('Skeleton Horse'),
    Entity('Zombie Horse'),
)
"""The non-horse horses."""
woods = ('Acacia', 'Bamboo', 'Birch', 'Cherry', 'Jungle', 'Mangrove', 'Oak', 'Dark Oak', 'Spruce')
"""The kinds of wood."""
stems = ('Warped', 'Crimson')
"""The kinds of stems."""
corals = ('Horn', 'Tube', 'Fire', 'Bubble', 'Brain')
"""The kinds of coral."""
tulips = ('Red', 'Orange', 'Pink', 'White')
"""The colors of tulips."""
small_flowers = ('Allium', 'Azure Bluet', 'Blue Orchid', 'Dandelion', 'Oxeye Daisy', 'Poppy')
"""The small flowers."""

moon_phases = (
    (206000, 'Full'),
    (38000, 'Waning Gibbous'),
    (62000, 'Three Quarters'),
    (86000, 'Waning Crescent'),
    (110000, 'New'),
    (134000, 'Waxing Crescent'),
    (158000, 'First Quarter'),
    (182000, 'Waxing Gibbous'),
)
"""The phases of the moon and the time for each."""

axolotls = ('Lucy', 'Wild', 'Gold', 'Cyan', 'Blue')
"""The kinds of axolotls."""

# noinspection SpellCheckingInspection
music_discs = (
    'music_disc_13',
    'music_disc_cat',
    'music_disc_blocks',
    'music_disc_chirp',
    'music_disc_far',
    'music_disc_mall',
    'music_disc_mellohi',
    'music_disc_stal',
    'music_disc_strad',
    'music_disc_ward',
    'music_disc_11',
    'music_disc_wait',
    'music_disc_otherside',
    'music_disc_pigstep',
    'music_disc_5',
)
"""The music discs."""


class Fish(Entity):
    """Data about a tropical fish."""
    _kinds = []

    def __init__(self, variant: int, name: str = None):
        """
        Creates a new fish with the given variant, and (if present) name. If not given, the desc() will be used as
        the name.
        """
        super().__init__('tropical_fish', name=name, nbt=Nbt(Variant=variant))
        self.variant = variant
        self.name = name if name else self.desc()

    @classmethod
    def _fish_kinds(cls):
        if not cls._kinds:
            cls._kinds = tuple(tropical_fish.keys())
        return cls._kinds

    @classmethod
    def variant(cls, kind: int | str, body_color: int | str, pattern_color: int | str) -> int:
        """
        Returns a variant for the described fish, to be used as a parameter to the Fish constructor.
        :param kind: The kind of fish, as either a name of a key in the ``tropical_fish`` dict, or an index of a key.
        :param body_color: The body color, as either a name or an index in the COLORS tuple.
        :param pattern_color: The pattern color, as either a name or an index in the COLORS tuple.
        """
        kind = Fish._to_kind(kind)

        return cls.spec_variant(kind < 6, kind % 6, body_color, pattern_color)

    @classmethod
    def spec_variant(cls, small: bool, which_body: int, body_color: int | str, pattern_color: int | str) -> int:
        """
        Returns a variant for the described fish, to be used as a parameter to the Fish constructor.
        :param small: Whether the fish is small.
        :param which_body: Which body type in the size, as a number from 0-5.
        :param body_color: The body color, as either a name or an index in the COLORS tuple.
        :param pattern_color: The pattern color, as either a name or an index in the COLORS tuple.
        """

        return int(small) | which_body << 8 | as_color_num(body_color) << 16 | as_color_num(pattern_color) << 24

    @classmethod
    def _to_kind(cls, kind):
        if isinstance(kind, str):
            kind = cls._fish_kinds().index(kind)
        return kind

    def is_small(self) -> bool:
        """Return whether this fish is small."""
        return self.variant & 0xff != 0

    def which_body(self) -> int:
        """Return which of the body types is used for this fish, in the range (0-5]."""
        return (self.variant & 0xff00) >> 8

    def kind(self) -> str:
        """Returns the name of the kind of fish."""
        return self._fish_kinds()[self.kind_num()]

    def kind_num(self) -> int:
        """Returns the number of this kind of fish. This is an index into ``tropical_fish.keys()``."""
        if self.is_small():
            return self.which_body()
        else:
            return self.which_body() + 6

    def body_color(self) -> str:
        """Returns the body color of the fish."""
        return COLORS[self.body_color_num()]

    def body_color_num(self) -> int:
        """Returns the number of the body color of the fish as an index into ``COLORS``."""
        return (self.variant & 0xff0000) >> 16

    def pattern_color(self) -> str:
        """Returns the pattern color of the fish."""
        return COLORS[self.pattern_color_num()]

    def pattern_color_num(self) -> int:
        """Returns the number of the pattern color of the fish as an index into ``COLORS``."""
        return (self.variant & 0xff000000) >> 24

    def desc(self) -> str:
        """
        Returns the description of this fish, which includes its body and pattern color (or just one if they are the
        same) and the body kind name.
        """
        body_color = to_name(self.body_color())
        pattern_color = to_name(self.pattern_color())
        if body_color == pattern_color:
            return f'{body_color} {self.kind()}'
        else:
            return f'{body_color}-{pattern_color} {self.kind()}'


tropical_fish = {
    'Spotty': (
        Fish(67110144, 'Goatfish'),
        Fish(50726144, 'Cotton Candy Betta')),
    'Brinely': (
        Fish(50660352, 'Queen Angelfish'),),
    'Dasher': (
        Fish(67699456, 'Yellowtail Parrotfish'),
        Fish(101253888, 'Parrotfish')),
    'Snooper': (
        Fish(235340288, 'Red Lipped Blenny'),),
    'Sunstreak': (
        Fish(50790656, 'Triggerfish'),
        Fish(118161664, 'Cichlid')),
    'Kob': (
        Fish(917504, 'Tomato Clownfish'),
        Fish(65536, 'Clownfish')),
    'Clayfish': (
        Fish(234882305, 'Emperor Red Snapper'),
        Fish(117441793, 'Butterflyfish'),
        Fish(16778497, 'Ornate Butterflyfish')),
    'Betty': (
        Fish(918529, 'Red Cichlid'),),
    'Blockfish': (
        Fish(67764993, 'Dottyback'),
        Fish(918273, 'Red Snapper')),
    'Glitter': (
        Fish(117441025, 'Moorish Idol'),),
    'Stripey': (
        Fish(117506305, 'Anemone'),),
    'Flopper': (
        Fish(117899265, 'Black Tang'),
        Fish(185008129, 'Blue Tang'),
        Fish(67371009, 'Yellow Tang'),
        Fish(67108865, 'Threadfin')),
}
"""The data for the predefined naturally-occurring tropical fish."""

trim_materials = sorted((
    'emerald', 'redstone', 'lapis', 'amethyst', 'quartz', 'netherite', 'diamond', 'gold', 'iron', 'copper'))

trim_patterns = sorted(
    ('coast', 'dune', 'eye', 'host', 'raiser', 'rib', 'sentry', 'shaper', 'silence', 'snout', 'spire', 'tide', 'vex',
     'ward', 'wayfinder', 'wild'))

armors = ('leather', 'chainmail', 'iron', 'golden', 'diamond', 'netherite')

sherds = tuple(x.value for x in PotterySherd)
