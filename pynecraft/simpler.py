from __future__ import annotations

import dataclasses
from typing import Callable, Iterable, Mapping, Tuple, Union

from .base import FacingDef, IntRelCoord, Nbt, NbtDef, Position, RelCoord, _ensure_size, _in_group, _quote, \
    _to_list, d, good_facing, r, to_id
from .commands import Biome, Block, BlockDef, COLORS, Command, Commands, Entity, JsonList, JsonText, SignCommands, \
    SignText, SomeMappings, fill, fillbiome, good_biome, good_block, good_color_num, setblock, Target, execute, data, s, \
    e
from .enums import Pattern

ARMORER = 'Armorer'
BUTCHER = 'Butcher'
CARTOGRAPHER = 'Cartographer'
CLERIC = 'Cleric'
FARMER = 'Farmer'
FISHERMAN = 'Fisherman'
FLETCHER = 'Fletcher'
LEATHERWORKER = 'Leatherworker'
LIBRARIAN = 'Librarian'
MASON = 'Mason'
NITWIT = 'Nitwit'
SHEPHERD = 'Shepherd'
TOOLSMITH = 'Toolsmith'
UNEMPLOYED = 'Unemployed'
WEAPONSMITH = 'Weaponsmith'
CHILD = 'Child'
VILLAGER_PROFESSIONS = (
    ARMORER,
    BUTCHER,
    CARTOGRAPHER,
    CLERIC,
    FARMER,
    FISHERMAN,
    FLETCHER,
    LEATHERWORKER,
    LIBRARIAN,
    MASON,
    NITWIT,
    SHEPHERD,
    TOOLSMITH,
    WEAPONSMITH,
    UNEMPLOYED,
)
"""Villager professions."""

DESERT = 'Desert'
JUNGLE = 'Jungle'
PLAINS = 'Plains'
SAVANNA = 'Savanna'
SNOW = 'Snow'
SWAMP = 'Swamp'
TAIGA = 'Taiga'
VILLAGER_BIOMES = (DESERT, JUNGLE, PLAINS, SAVANNA, SNOW, SWAMP, TAIGA)
"""Villager biomes / types."""


class Sign(Block):
    """A class that represents a sign. This class is a standing sign, the WallSign subclass is for wall signs."""

    def __init__(self, text: SignText, /, commands: SignCommands = (), wood='oak', state: Mapping = None,
                 nbt: NbtDef = None):
        """
        Creates a sign object.
        :param text:
        :param commands:
        :param wood:
        :param state:
        :param nbt:
        """
        wood = to_id(wood)
        super().__init__(self._kind_name(wood), state=state, nbt=nbt)
        self.wood = wood
        text = _ensure_size(text, 4)
        commands = _ensure_size(commands, 4)
        lines_nbt = Sign.lines_nbt(text, commands)
        self.merge_nbt(lines_nbt)
        if nbt:
            self.merge_nbt(nbt)

    @classmethod
    def lines_nbt(cls, text: SignText, commands: SignCommands = ()) -> Nbt:
        """Returns the lines of NBT for sign text.
        :param text: The sign text, as an iterable of one to four lines of text. Entries that are None will generate no
        NBT, any text will generate a line for the sign.
        :param commands: Commands for the sign, in order.
        :return: The NBT for the combination of text and commands.
        """
        text = _to_list(text)
        commands = _to_list(commands)
        max_count = max(len(text), len(commands))
        if max_count > 4:
            raise ValueError(f'{max_count}: Too many values for text and/or commands')
        text = _ensure_size(text, 4)
        commands = _ensure_size(commands, 4)

        nbt = Nbt()
        for i, entry in enumerate(zip(text, commands)):
            if entry == (None, None):
                continue
            txt, cmd = entry
            if txt is None:
                txt = ''
            key = f'Text{i + 1}'
            if isinstance(txt, str):
                if not cmd:
                    nbt[key] = txt
                    continue
                txt = JsonText.text(txt)
            txt = JsonText.as_json(txt)
            if cmd:
                if isinstance(cmd, Callable):
                    txt = cmd(txt)
                else:
                    txt = txt.click_event().run_command(cmd)
            nbt[key] = txt

        return nbt

    @classmethod
    def text(cls, txt: str) -> str:
        """
        Text fit for a sign's ``Text`` fields  It simply puts double quotes around the text, and escapes pre-existing
        double quotes. This is simple text values, not for full JSON text options; for that see the JsonText class.
        """
        return r'"\"%s\""' % txt.replace('"', r'\\"')

    def _kind_name(self, wood):
        return wood + '_sign'

    def glowing(self, v: bool) -> Sign:
        """Set the text will be glowing or not."""
        self.nbt['GlowingText'] = v
        return self

    def color(self, color: str) -> Sign:
        """Set the overall text color."""
        if color is None:
            del self.nbt['Color']
        else:
            self.nbt['Color'] = _in_group(COLORS, color)
        return self

    def place(self, pos: Position, facing: FacingDef, /, water=False, nbt: NbtDef = None,
              clear_out=True) -> Commands | Command:
        """
        Place the sign.

        :param pos: The position.
        :param facing: The direction the sign if facing. See good_facing() for useful parameters.
        :param water: Whether the sign is waterlogged.
        :param nbt: Any extra NBT for the sign.
        :return: The commands to place the sign.
        """
        self._orientation(facing)
        if water:
            self.merge_state({'waterlogged': True})
        if nbt:
            self.merge_nbt(nbt)
        if clear_out:
            return (
                setblock(pos, 'water' if water else 'air'),
                setblock(pos, self),
            )
        else:
            return setblock(pos, self)

    def _orientation(self, facing):
        self.merge_state({'rotation': good_facing(facing).sign_rotation})


class WallSign(Sign):
    """A class for wall signs."""

    def _kind_name(self, wood):
        return wood + '_wall_sign'

    def _orientation(self, facing):
        self.merge_state({'facing': good_facing(facing).name})

    def place(self, pos: Position, facing: FacingDef, /, water=False, nbt: NbtDef = None, clear_out=True) -> Commands:
        """When placing a wall sign, the orientations are different, but also can be found in good_facing()."""
        return super().place(pos, facing, water, nbt, clear_out)


class Book:
    """A class for a book."""

    def __init__(self, title: str = None, author: str = None, display_name: str = None):
        """Creates a book object."""
        self.title = title
        self.author = author
        self.display_name = display_name
        self._pages = []
        self._cur_page = JsonList()

    # Two kinds of books: Written and signed. In theory, they should hold the same kind
    # of text, but the unsigned book cannot have rich text. Hopefully in the future this _will_ be possible, so
    # this method is kept separate instead of being incorporated into the __init__ of a
    # "signed book" class that is separate from the "unsigned book" class. Or some such design.
    def sign_book(self, title: str, author: str, display_name: str = None):
        """Sign the book. An unsigned book cannot have rich text."""
        self.title = title
        self.author = author
        self.display_name = display_name

    def add(self, *txt: JsonText | str):
        """Add text to the current page of the book."""
        if self.title is None:
            raise ValueError("Cannot add Json text to unsigned book")
        for t in txt:
            if isinstance(t, str):
                t = JsonText.text(t)
            self._cur_page.append(t)

    def next_page(self):
        """Start the next page."""
        self._pages.append(self._cur_page)
        self._cur_page = JsonList()

    def as_entity(self):
        """Returns the book as an Entity object. This is useful for a ``give`` command."""
        return Entity('written_book', nbt=self.nbt())

    def as_item(self):
        """Returns the book as an Item object. This is useful for things like putting the book into a container."""
        item = Item.nbt_for('written_book')
        nbt = self.nbt()
        try:
            pages = nbt['pages']
            if pages:
                nbt['pages'] = _quote(pages)
        except KeyError:
            pass

        return Nbt({'Book': item.merge({'tag': nbt})})

    def nbt(self):
        """Returns the NBT for the book."""
        cur_page = self._cur_page
        self.next_page()
        jt = Nbt()
        jt['title'] = self.title
        jt['author'] = self.author
        if self.display_name:
            jt['display_name'] = {'Lore': self.display_name}
        jt['pages'] = [JsonList(x) for x in self._pages[:]]
        self._cur_page = cur_page
        self._pages.pop()
        return jt


class TextDisplay(Entity):
    """An object that represents a text_display entity."""

    def __init__(self, text: str | None, nbt: NbtDef = None):
        super().__init__('text_display', nbt)
        if text is not None:
            self.merge_nbt({'text': JsonText.text(text)})
        self._tags = []

    def tag(self, *tags: str) -> Entity:
        self._tags.extend(tags)
        return super().tag(*tags)

    def scale(self, value: float) -> TextDisplay:
        self.merge_nbt({'transformation': {'scale': [value, value, value]}})
        return self

    def transform(self, target: Target) -> str | None:
        if 'transformation' not in self.nbt:
            return None
        return execute().as_(target).run(data().merge(s(), {'transformation': self.nbt['transformation']}))

    def summon(self, pos: Position, nbt=None, facing: str = None) -> Tuple[str, ...]:
        summon = super().summon(pos, nbt, facing)
        if len(self._tags) == 0:
            return (summon,)
        return (
            summon,
            self.transform(e().tag(*self._tags))
        )


class Item(Entity):
    """An object that represents an Item."""

    def __init__(self, id: str, count: int = 1, name=None, nbt=None):
        super().__init__(id, name=name)
        self.merge_nbt({'id': id, 'Count': count})
        if nbt:
            self.merge_nbt(nbt)

    @classmethod
    def nbt_for(cls, item: BlockDef, nbt=None) -> Nbt:
        """The nbt for this item."""
        item = good_block(item)
        item_id = item.id
        if item_id.find(':') < 0:
            item_id = 'minecraft:' + item_id
        retval = Nbt({'id': item_id, 'Count': 1})
        # Filled maps are stored directly, not shunted an inner tag
        if item_id:
            if item_id == 'minecraft:filled_map':
                retval = retval.merge(item.nbt)
                if nbt:
                    retval = retval.merge(nbt)
            elif item.nbt:
                retval['tag']['BlockEntityTag'] = item.nbt
        try:
            block_state = item.state
            if block_state:
                retval['tag']['BlockStateTag'] = block_state
        except AttributeError:
            pass
        if nbt:
            return retval.merge(nbt)
        return retval


class Shield(Item):
    """A shield object."""

    def __init__(self):
        """Creates a new shield."""
        super().__init__('shield')
        self.merge_nbt({'tag': {'BlockEntityTag': {'Patterns': []}}})

    def add_pattern(self, pattern: str, color: int | str) -> Shield:
        """Add a pattern to the shield."""
        color = good_color_num(color)
        patterns = self.nbt['tag']['BlockEntityTag'].get_list('Patterns')
        patterns.append(Nbt({'Pattern': Pattern(pattern), 'Color': color}))
        return self

    def clear_patterns(self) -> Shield:
        """Remove all patterns from the shield."""
        self.nbt['tag']['BlockEntityTag']['Patterns'] = []
        return self


class Region:
    """Represents a region of space, and gives tools for changing items within it."""
    __slab_states = []
    __stair_states = []
    __door_states = []
    __trapdoor_states = []
    __button_states = []
    __slab_states.append(Nbt({'type': 'double'}))
    __dirs = ("north", "east", "west", "south")
    for __h in ('top', 'bottom'):
        __slab_states.append(Nbt({'type': __h}))
        for __f in __dirs:
            for __s in ('straight', "inner_left", "inner_right", "outer_left", "outer_right"):
                __stair_states.append(Nbt({'half': __h, 'facing': __f, 'shape': __s}))
            for __o in (True, False):
                __trapdoor_states.append(Nbt({'half': __h, 'facing': __f, 'open': __o}))
                for __g in ('left', 'right'):
                    __door_states.append(
                        Nbt({'half': 'upper' if __h == 'top' else 'lower', 'facing': __f, 'open': __o, 'hinge': __g}))
    for __f in __dirs:
        for __t in ('ceiling', 'floor', 'wall'):
            __button_states.append({'facing': __f, 'face': __t})
    slab_states = tuple(__slab_states)
    """The block states that a slab can have related to its placements."""
    stair_states = tuple(__stair_states)
    """The block states that stairs can have related to its placements."""
    door_states = tuple(__door_states)
    """The block states that a door can have related to its placements."""
    trapdoor_states = tuple(__trapdoor_states)
    """The block states that a trapdoor can have related to its placements."""
    button_states = tuple(__button_states)
    """The block states that a button can have related to its placements."""
    facing_states = tuple(Nbt({'facing': x}) for x in __dirs)
    """North, east, west, and south."""
    facing_all_states = tuple(Nbt({'facing': x}) for x in __dirs + ('up', 'down'))
    """North, east, west, south, up, and down."""
    rotation_states = tuple(Nbt({'rotation': x}) for x in range(16))
    """16 sign direction rotations."""
    axes_states = tuple(Nbt({'axis': x}) for x in ('x', 'y', 'z'))
    """X, y, and z. Pillars and logs use this, for example."""
    rail_states = tuple(Nbt({'shape': x}) for x in ('east_west', 'north_south') + tuple(
        f'ascending_{x}' for x in ('east', 'west', 'north', 'south')))
    """The block states that rails can have related to its placements."""
    curved_rail_states = tuple(Nbt({'shape': x}) for x in ('north_east', 'north_west', 'south_east', 'south_west'))
    """The block states that curved rails can have related to its placements."""

    def __init__(self, start: Position, end: Position):
        """Creates a new region object. Any two opposite corners will do."""
        self.start = start
        self.end = end

    def fill(self, new: BlockDef, replace: BlockDef = None) -> Command:
        """
        Returns a command that will fill the region with a block. If a second block is given, it will be the filter;
        only this kind of block will be replaced. This can, of course, be a tag.
        """
        f = fill(self.start, self.end, good_block(new))
        if replace:
            f = f.replace(replace)
        yield f

    def fillbiome(self, biome: Biome, replace: Biome = None) -> Command:
        f = fillbiome(self.start, self.end, good_biome(biome))
        if replace:
            f = f.replace(good_biome(replace))
        yield f

    def replace(self, new: BlockDef, old: BlockDef, states: SomeMappings = None,
                new_states: SomeMappings = None, shared_states: SomeMappings = None) -> Commands:
        """Returns commands that will replace one with block with another. If states are given, commands will be
        generated for each state, applied to both the fill block and the filter block. States are specified by a map,
        and can be passed as a single state, or an Iterable of them. States in new_states will only be applied to the
        new blocks. One command will be generated for each combination of the two sets of states. """
        states = _to_list(states) if states else [{}]
        new_states = _to_list(new_states) if new_states else [{}]
        if not shared_states:
            shared_states = {}
        new = good_block(new)
        old = good_block(old)

        if not states and not new_states and not shared_states:
            yield from self.fill(new, old)
        else:
            for new_added in new_states:
                n = new.clone().merge_state(new_added).merge_state(shared_states)
                o = old.clone().merge_state(shared_states)
                for s in states:
                    yield from self.fill(n.clone().merge_state(s), o.clone().merge_state(s))

    def replace_slabs(self, new: BlockDef, old: BlockDef = '#slabs', new_state: Mapping = None,
                      shared_states: SomeMappings = None) -> Commands:
        """Replaces slabs in the region using all the relevant states."""
        yield from self.replace(new, old, Region.slab_states, new_state, shared_states)

    def replace_stairs(self, new: BlockDef, old: BlockDef = '#stairs', new_state: Mapping = None,
                       shared_states: SomeMappings = None) -> Commands:
        """Replaces stairs in the region using all the relevant states."""
        yield from self.replace(new, old, Region.stair_states, new_state, shared_states)

    def replace_buttons(self, new: BlockDef, old: BlockDef = '#buttons', new_state: Mapping = None,
                        shared_states: SomeMappings = None) -> Commands:
        """Replaces buttons in the region using all the relevant states."""
        yield from self.replace(new, old, Region.button_states, new_state, shared_states)

    def replace_doors(self, new: BlockDef, old: BlockDef = '#doors', new_state: Mapping = None,
                      shared_states: SomeMappings = None) -> Commands:
        """Replaces doors in the region using all the relevant states."""
        yield from self.replace(new, old, Region.door_states, new_state, shared_states)

    def replace_trapdoors(self, new: BlockDef, old: BlockDef = '#trapdoors', new_state: Mapping = None,
                          shared_states: SomeMappings = None) -> Commands:
        """Replaces trapdoors in the region using all the relevant states."""
        yield from self.replace(new, old, Region.trapdoor_states, new_state, shared_states)

    def replace_facing(self, new: BlockDef, old: BlockDef, new_state: Mapping = None,
                       shared_states: SomeMappings = None) -> Commands:
        """Replaces blocks in the region using all the "facing" states."""
        yield from self.replace(new, old, Region.facing_states, new_state, shared_states)

    def replace_facing_all(self, new: BlockDef, old: BlockDef, new_state: Mapping = None,
                           shared_states: SomeMappings = None) -> Commands:
        """Replaces blocks in the region using all the "all_facing" states."""
        yield from self.replace(new, old, Region.facing_all_states, new_state, shared_states)

    def replace_rotation(self, new: BlockDef, old: BlockDef, new_state: Mapping = None,
                         shared_states: SomeMappings = None) -> Commands:
        """Replaces blocks in the region using all the "rotation" states."""
        yield from self.replace(new, old, Region.rotation_states, new_state, shared_states)

    def replace_axes(self, new: BlockDef, old: BlockDef, new_state: Mapping = None,
                     shared_states: SomeMappings = None) -> Commands:
        """Replaces blocks in the region using all the "axes"" states."""
        yield from self.replace(new, old, Region.axes_states, new_state, shared_states)

    def replace_straight_rails(self, new: BlockDef, old: BlockDef = '#rails', new_state: Mapping = None,
                               shared_states: SomeMappings = None) -> Commands:
        """Replaces straight rails in the region using all the relevant states."""
        yield from self.replace(new, old, Region.rail_states, new_state, shared_states)

    def replace_curved_rails(self, new: BlockDef = "rail", old: BlockDef = '#rails',
                             new_state: Mapping = None, shared_states: SomeMappings = None) -> Commands:
        """Replaces curved rails in the region using all the relevant states."""
        yield from self.replace(new, old, Region.curved_rail_states, new_state, shared_states)


class Offset:
    """
    This provides a tool for offsetting relative coordinates. This allows you to write code placed in a way that may
    be more convenient, such as if a command block is hidden in a convenient place, but wants to operate relative to
    a different base location. Given an initial offset of a given number of coordinates, coordinates generated
    through the object's r() and d() methods will be adjusted by that location. The values passed to r() and () must
    be the same length as the initial offset.
    """

    CoordsIn = Union[float, RelCoord]
    # This is so complicated because some functions take specific-length tuples so we want to declare that we produce
    # them to make the type checker happier.
    CoordsOut = Union[
        RelCoord, Tuple[RelCoord, RelCoord], Tuple[IntRelCoord, IntRelCoord], Tuple[RelCoord, RelCoord, RelCoord],
        Tuple[RelCoord, ...]]

    def __init__(self, *position: float):
        """Creates an offsetting object with the given values."""
        if len(position) == 0:
            raise ValueError(f'Must have at least one value in offset')
        self.position: tuple[float] = position

    def r(self, *values: CoordsIn) -> CoordsOut:
        """ Returns the result of base.r() with the input, with each return value added to this object's offset. """
        return self._rel_coord(r, *values)

    def d(self, *values: CoordsIn) -> CoordsOut:
        """ Returns the result of base.d() with the input, with each return value added to this object's offset. """
        return self._rel_coord(d, *values)

    def abs(self, *values: float | int | Iterable[float | int]) -> float | int | Iterable[float | int]:
        if len(values) != len(self.position):
            raise ValueError(f'{len(values)}: Expected {len(self.position)} values')
        result = tuple(sum(p) for p in zip(values, self.position))
        if len(values) == 1:
            return result[0]
        return result

    def _rel_coord(self, f, *values: CoordsIn) -> RelCoord | Tuple[RelCoord, ...]:
        if len(values) != len(self.position):
            raise ValueError(f'{len(values)} != position length ({len(self.position)})')
        vec = []
        exemplar = f(0)
        for v in values:
            if isinstance(v, (float, int)):
                vec.append(f(v))
            elif v.prefix != exemplar.prefix:
                raise ValueError(f'{f}: incompatible RelCoord type')
            else:
                vec.append(v)
        vals = RelCoord.add(vec, self.position)
        if len(vals) == 1:
            return vals[0]
        return vals


class ItemFrame(Entity):
    """A class for item frames."""

    def __init__(self, facing: int | str, *, glowing: bool = None, nbt: NbtDef = None, name: str = None):
        """Creates an ItemFrame object facing in the given direction. See good_facing() for useful values."""
        nbt = Nbt.as_nbt(nbt) if nbt else Nbt({})
        nbt = nbt.merge({'Facing': good_facing(facing).number, 'Fixed': True})
        super().__init__('glow_item_frame' if glowing else 'item_frame', nbt=nbt, name=name)

    def item(self, item: BlockDef) -> ItemFrame:
        """Sets the item that is in the frame."""
        block = good_block(item)
        self.merge_nbt({'Item': Item.nbt_for(block)})
        return self

    def fixed(self, value: bool) -> ItemFrame:
        self.nbt['Fixed'] = value
        return self

    def named(self, name: BlockDef = None) -> ItemFrame:
        """Sets the name displayed for the item in the frame."""
        block = good_block(name)
        if block is None:
            try:
                del self.nbt['Item']['tag']['display']['Name']
            except KeyError:
                pass  # Must not be there already, ignore the error
        else:
            if 'Item' not in self.nbt:
                self.item(block)
            nbt = self.nbt
            nbt['Item']['tag']['display']['Name'] = JsonText.text(block.name)
        return self


@dataclasses.dataclass
class Trade:
    """Represents a single trade a villager can make."""
    max_uses = 12
    uses = 0
    xp = 1
    buy: tuple[tuple[BlockDef, int]] | tuple[tuple[BlockDef, int], tuple[BlockDef, int]]
    sell: tuple[BlockDef, int]
    reward_exp = True

    def __init__(self, buy1: BlockDef | tuple[BlockDef, int], thing1: BlockDef | tuple[BlockDef, int],
                 thing2: BlockDef | tuple[BlockDef, int] = None, /, max_uses=None, uses=0, xp=1, reward_exp=True):
        """
        Creates a Trade object. The first block or item is the price. If thing2 is present, then it is the block or item
        being sold, and thing1 is the second part of the price. Otherwise, thing1 is the block or item being sold.
        """
        if thing2:
            self.buy = (_to_def(buy1), _to_def(thing1))
            self.sell = _to_def(thing2)
        else:
            self.buy = (_to_def(buy1),)
            self.sell = _to_def(thing1)
        self.max_uses = max_uses
        self.uses = uses
        self.xp = xp
        self.reward_exp = reward_exp

    def nbt(self):
        """Returns the nbt for this trade."""
        values = {
            'buy': {'id': self.buy[0][0], 'Count': self.buy[0][1]},
            'sell': {'id': self.sell[0], 'Count': self.sell[1]},
            'rewardExp': self.reward_exp
        }
        if len(self.buy) > 1:
            values['buyB'] = {'id': self.buy[1][0], 'Count': self.buy[1][1]}
        if self.max_uses:
            values['maxUses'] = self.max_uses
        return values


def _to_def(block) -> tuple[Block, int]:
    if isinstance(block, tuple):
        return good_block(block[0]).id, block[1]
    return good_block(block).id, 1


class Villager(Entity):
    """Convenience class for a villager or zombie villager. This presents simpler mechanisms for profession,
    biome, experience, levels, and trades."""
    level_xp = {
        'Novice': range(0, 10),
        'Apprentice': range(10, 70),
        'Journeyman': range(70, 150),
        'Expert': range(150, 250),
        'Master': range(250, 2147483647),
    }
    """The range of experience for each level."""

    def __init__(self, profession: str = 'Unemployed', biome: str = 'Plains', nbt: NbtDef = None, /, name=None,
                 zombie: bool = False):
        """Creates a villager."""
        super().__init__('zombie_villager' if zombie else 'villager', nbt=nbt, name=name)
        self.zombie = zombie
        self.profession(profession)
        self.biome(biome)
        self._trades: list[Trade] = []

    def xp(self, xp: int) -> Villager:
        """Sets the villager's experience."""
        self.merge_nbt({'VillagerData': {'Xp': xp, 'level': self.level}})
        return self

    @property
    def level(self) -> int:
        """The villager's level as a number."""
        i, _ = self._lookup_level()
        return i

    @property
    def level_name(self) -> str:
        """The villager's level as a name."""
        _, n = self._lookup_level()
        return n

    def _lookup_level(self):
        try:
            xp = self.nbt()['VillagerData']['Xp']
        except KeyError:
            xp = 0
        for i, (n, r) in enumerate(Villager.level_xp.items()):
            if xp in r:
                return i, n
        raise ValueError(f'{xp}: Invalid experience value')

    def profession(self, profession: str) -> Villager:
        """Sets the villager's profession. The profession can also be 'child' for non-zombie villagers."""
        profession = profession.title()
        if profession == 'Child':
            if self.zombie:
                raise ValueError('Child: Invalid zombie villager profession')
            profession = UNEMPLOYED
            self.merge_nbt({'Age': -2147483648})
        self.merge_nbt({'VillagerData': {'profession': _in_group(VILLAGER_PROFESSIONS, profession).lower()}})
        return self

    def biome(self, biome: str) -> Villager:
        """Sets the villager's biome."""
        biome = biome.title()
        self.merge_nbt({'VillagerData': {'type': _in_group(VILLAGER_BIOMES, biome).lower()}})
        return self

    type = biome
    """Alias for the ``biome`` method, because these two terms are used interchangeably."""

    def add_trade(self, *trades: Trade | NbtDef) -> Villager:
        """Add trades to the villager's list."""
        recipes = self.nbt['Offers'].get_list('Recipes')
        for t in trades:
            if isinstance(t, Trade):
                if len(t.buy) not in range(1, 3):
                    raise ValueError(f'{len(t.buy)}: Invalid buy length (must be 1 or 2)')
                t = t.nbt()
            recipes.append(t)
        return self

    def inventory(self, *items: BlockDef | tuple[BlockDef, int]) -> Villager:
        """Sets the villager's inventory."""
        inventory = self.nbt.get_list('Inventory')
        for i in items:
            if not isinstance(i, tuple):
                i = (i, 1)
            item_nbt = Item.nbt_for(good_block(i[0]))
            item_nbt['Count'] = i[1]
            inventory.append(Nbt(item_nbt))
        return self
