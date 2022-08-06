"""Contains various data about vanilla Minecraft."""

from .base import Nbt, to_id
from .commands import Block, Entity


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
    Color("White", 0xf9fffe),
    Color("Orange", 0xf9801d),
    Color("Magenta", 0xc74ebd),
    Color("Light Blue", 0x3ab3da),
    Color("Yellow", 0xfed83d),
    Color("Lime", 0x80c71f),
    Color("Pink", 0xf38baa),
    Color("Gray", 0x474f52),
    Color("Light Gray", 0x9d9d97),
    Color("Cyan", 0x169c9c),
    Color("Purple", 0x8932b8),
    Color("Blue", 0x3c44aa),
    Color("Brown", 0x835432),
    Color("Green", 0x5e7c16),
    Color("Red", 0xb02e26),
    Color("Black", 0x1d1d21),
)
"""The standard colors."""


class Instrument:
    """Data about a note block instrument."""

    def __init__(self, id, name, exemplar):
        """
        Creates a new instrument.
        :param id: The ID used in the note block's NBT
        :param name: The human-friendly name for the instrument.
        :param exemplar: One block you can put under the note block to get this instrument. Some instruments have several.
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
    Instrument('didgeridoo', 'Digeridoo', Block('Pumpkin')),
    Instrument('bit', 'Bit', Block('Emerald Block')),
    Instrument('banjo', 'Banjo', Block('Hay Block')),
    Instrument('pling', 'Pling', Block('Glowstone')),
)
"""The instruments note blocks can play."""

villager_professions = (
    "Armorer",
    "Butcher",
    "Cartographer",
    "Cleric",
    "Farmer",
    "Fisherman",
    "Fletcher",
    "Leatherworker",
    "Librarian",
    "Mason",
    "Nitwit",
    "Shepherd",
    "Toolsmith",
    "Weaponsmith",
    "Unemployed",
)
villager_types = ("Desert", "Jungle", "Plains", "Savanna", "Snow", "Swamp", "Taiga")
"""The (biome) types of villagers."""


class Horse(Entity):
    """Data about a horse."""

    def __init__(self, name: str, variant=None):
        if variant is None:
            super().__init__(name)
            self.tag = f'{self.id}s'
        else:
            super().__init__('horse', name=name)
            self.tag = f'{to_id(name)}_horses'
        self.variant = variant


horses = (
    Horse("White", 0),
    Horse("Creamy", 1),
    Horse("Chestnut", 2),
    Horse("Brown", 3),
    Horse("Black", 4),
    Horse("Gray", 5),
    Horse("Dark Brown", 6),
)
"""The horses."""
other_horses = (
    Horse("Mule"),
    Horse("Donkey"),
    Horse("Skeleton Horse"),
    Horse("Zombie Horse"),
)
"""The non-horse horses."""
woods = ("Acacia", "Birch", "Jungle", "Mangrove", "Oak", "Dark Oak", "Spruce")
"""The kinds of wood."""
stems = ("Warped", "Crimson")
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

    def __init__(self, name: str, desc: str, variant: int):
        super().__init__('tropical_fish', name=name, nbt=Nbt(Variant=variant))
        self.name = name
        self.desc = desc
        self.variant = variant


tropical_fish = {
    'Flopper': (
        Fish('Black Tang', 'Gray Flopper', 117899265),
        Fish('Blue Tang', 'Gray-Blue Flopper', 185008129),
        Fish('Yellow Tang', 'Yellow Flopper', 67371009),
        Fish('Threadfin', 'White-Yellow Flopper', 67108865)),
    'Stripey': (
        Fish('Anemone', 'Orange-Gray Stripey', 117506305),),
    'Glitter': (
        Fish('Moorish Idol', 'White-Gray Glitter', 117441025),),
    'Blockfish': (
        Fish('Dottyback', 'Purple-Yellow Blockfish', 67764993),
        Fish('Red Snapper', 'Red-White Blockfish', 918273)),
    'Betty': (
        Fish('Red Cichlid', 'Red-White Betty', 918529),),
    'Clayfish': (
        Fish('Emperor Red Snapper', 'White-Red Clayfish', 234882305),
        Fish('Butterflyfish', 'White-Gray Clayfish', 117441793),
        Fish('Ornate Butterflyfish', 'White-Orange Clayfish', 16778497)),
    'Kob': (
        Fish('Tomato Clownfish', 'Red-White Kob', 917504),
        Fish('Clownfish', 'Orange-White Kob', 65536)),
    'Sunstreak': (
        Fish('Triggerfish', 'Gray-White Sunstreak', 50790656),
        Fish('Cichlid', 'Blue-Gray Sunstreak', 118161664)),
    'Snooper': (
        Fish('Red Lipped Blenny', 'Gray-Red Snooper', 235340288),),
    'Dasher': (
        Fish('Yellowtail Parrotfish', 'Cyan-Yellow Dasher', 67699456),
        Fish('Parrotfish', 'Cyan-Pink Dasher', 101253888)),
    'Brinely': (
        Fish('Queen Angelfish', 'Lime-Light Blue Dasher', 50660352),),
    'Spotty': (
        Fish('Goatfish', 'White-Yellow Spotter', 67110144),
        Fish('Cotton Candy Betta', 'Pink-Light Blue Spotty', 50726144)),
}
"""The data for the predefined naturally-occurring tropical fish."""
