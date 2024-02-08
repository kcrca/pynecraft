from __future__ import annotations

import dataclasses
from typing import Callable, Mapping, Sequence, Tuple, Union

from .base import Arg, FacingDef, IntOrArg, IntRelCoord, NORTH, Nbt, NbtDef, Position, RelCoord, StrOrArg, \
    _ensure_size, _in_group, _quote, _to_list, as_facing, d, de_arg, r, to_id
from .commands import Biome, Block, BlockDef, COLORS, Command, Commands, Entity, EntityDef, JsonList, JsonText, \
    SignCommand, SignCommands, SignMessage, SignMessages, SomeMappings, as_biome, as_block, as_entity, data, fill, \
    fillbiome, setblock
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
WEAPONSMITH = 'Weaponsmith'
NONE = 'None'
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
    NONE,
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

    waxed = False
    """Whether signs are waxed by default."""

    def __init__(self, text: SignMessages = (), /, commands: SignCommands = (), wood='oak', state: Mapping = None,
                 nbt: NbtDef = None, hanging=False, front=True):
        """
        Creates a sign object. The text and commands are passed to front().
        """
        self.hanging = hanging
        wood = to_id(wood)
        super().__init__(self._kind_name(wood), state=state, nbt=nbt)
        self.wood = wood
        if text or commands:
            self.messages(text, commands, front=front)
        self.wax(Sign.waxed)
        if nbt:
            self.merge_nbt(nbt)

    def front(self, text: SignMessages, /, commands: SignCommands = ()) -> Sign:
        """Sets the text attributes for the front of the sign."""
        self.messages(text, commands, front=True)
        return self

    def back(self, text: SignMessages, /, commands: SignCommands = ()) -> Sign:
        """Sets the text attributes for the back of the sign."""
        self.messages(text, commands, front=False)
        return self

    def messages(self, texts: SignMessages, commands: SignCommands = (), front: bool = None) -> Sign:
        """Set the text for the front, back, or both if ``front`` is None."""
        messages = self.lines_nbt(texts, commands)
        if front or front is None:
            self.merge_nbt({'front_text': messages})
        if front is False or front is None:
            self.merge_nbt({'back_text': messages})
        return self

    def glowing(self, v: bool, front: bool = None) -> Sign:
        """Set whether the text will be glowing for the front, back, or both if ``front`` is None."""
        if front or front is None:
            self.nbt.set_or_clear('front_text.has_glowing_text', v)
        if front is False or front is None:
            self.nbt.set_or_clear('back_text.has_glowing_text', v)
        return self

    def color(self, color: str = None, front: bool = None) -> Sign:
        """Set the text will color for the front, back, or both if ``front`` is None."""
        color = _in_group(COLORS, color)
        if front or front is None:
            self.nbt.set_or_clear('front_text.color', color)
        if front is False or front is None:
            self.nbt.set_or_clear('back_text.color', color)
        return self

    def wax(self, on=True):
        """Sets the sign to be waxed or not. The default is True (ignores ``Sign.waxed``)"""
        self.nbt.set_or_clear('is_waxed', on)
        return self

    @classmethod
    def lines_nbt(cls, texts: SignMessages, commands: SignCommands = ()) -> Nbt:
        """Returns the lines of NBT for sign text.
        :param texts: The sign text, as an iterable of one to four lines of text. Entries that are None will generate no
        NBT, any text will generate a line for the sign.
        :param commands: Commands for the sign, in order.
        :return: The NBT for the combination of text and commands.
        """
        texts = _ensure_size(_to_list(texts), 4)
        commands = _ensure_size(_to_list(commands), 4)
        max_count = max(len(texts), len(commands))
        if max_count > 4:
            raise ValueError(f'{max_count}: Too many values for text and/or commands')
        texts = _ensure_size(texts, 4)
        commands = _ensure_size(commands, 4)

        messages = []
        for i in range(4):
            messages.append(cls.line_nbt(texts[i], commands[i]))

        return Nbt({'messages': messages})

    def _kind_name(self, wood):
        return f'{wood}_hanging_sign' if self.hanging else f'{wood}_sign'

    @classmethod
    def line_nbt(cls, text: SignMessage = None, command: SignCommand = None) -> Nbt:
        orig_text = text
        if text is None:
            text = JsonText.text('')
        elif isinstance(text, str):
            text = JsonText.text(text)
        entry = text
        if isinstance(command, Callable):
            command = command(orig_text)
        if command:
            entry = text.click_event().run_command(command)
        return entry

    @classmethod
    def change(cls, pos: Position, messages: SignMessages = None, commands: SignCommands = None,
               front=True, start=0) -> Commands:
        messages = messages if messages else (None, None, None, None)
        commands = commands if commands else (None, None, None, None)
        cmds = []
        for f in ('front', 'back'):
            if f == 'front' and front is False:
                continue
            elif f == 'back' and front is True:
                continue
            face = f'{f}_text'
            added = 0
            for i, desc in enumerate(zip(messages, commands)):
                msg, cmd = desc
                if msg is None and cmd is None:
                    continue
                cmds.append(
                    data().modify(pos, f'{face}.messages[{i + start}]').set().value(str(cls.line_nbt(msg, cmd))))
                added += 1
            if added == 4 and start == 0:
                # If everything is being changed, this is much more efficient
                change_all = (cls.lines_nbt(messages, commands))
                to_merge = Nbt()
                if front is None:
                    to_merge['front_text'] = change_all
                    to_merge['back_text'] = change_all
                else:
                    to_merge[face] = change_all
                cmds = [data().merge(pos, to_merge)]
                break
        return cmds

    def place(self, pos: Position, facing: FacingDef, /, water=False, nbt: NbtDef = None,
              clear=True) -> Commands | Command:
        """
        Place the sign.

        :param pos: The position.
        :param facing: The direction the sign if facing. See as_facing() for useful parameters.
        :param water: Whether the sign is waterlogged.
        :param nbt: Any extra NBT for the sign.
        :param clear: Clear out the block before placing
        :return: The commands to place the sign.
        """
        self._orientation(facing)
        if water:
            self.merge_state({'waterlogged': True})
        if nbt:
            self.merge_nbt(nbt)
        if clear:
            return (
                setblock(pos, 'water' if water else 'air'),
                setblock(pos, self),
            )
        else:
            return setblock(pos, self)

    def _orientation(self, facing):
        self.merge_state({'rotation': as_facing(facing).sign_rotation})


class WallSign(Sign):
    """A class for wall signs."""

    def _kind_name(self, wood):
        return f'{wood}_wall_hanging_sign' if self.hanging else f'{wood}_wall_sign'

    def _orientation(self, facing):
        self.merge_state({'facing': as_facing(facing).name})

    def place(self, pos: Position, facing: FacingDef, /, water=False, nbt: NbtDef = None, clear=True) -> Commands:
        """When placing a wall sign, the orientations are different, but also can be found in as_facing()."""
        return super().place(pos, facing, water, nbt, clear)


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


class Display(Entity):
    """
    A class for the various "display" objects: text_display, item_display, and block_display. The main feature is that
    it makes transformation modifications work on the summon command; see https://bugs.mojang.com/browse/MC-259838.
    """
    INIT_TRANSFORMATION = Nbt(
        {'transformation': {'left_rotation': [0.0, 0.0, 0.0, 1.0], 'translation': [0.0, 0.0, 0.0],
                            'right_rotation': [0.0, 0.0, 0.0, 1.0], 'scale': [1.0, 1.0, 1.0]}})

    def __init__(self, id: str, nbt=None, name=None):
        super().__init__(id, nbt, name)
        # Without this, a simple change to the transform cannot be given at summon time.
        # Crazily, this is "as intended": https://bugs.mojang.com/browse/MC-259838
        self.merge_nbt(Display.INIT_TRANSFORMATION)

    def scale(self, value: float | Tuple[float, float, float]) -> Display:
        """
        Sets the scale transformation. If only given one value, it uses that for all three scale values. Otherwise,
        it must be given the three values.
        """
        if isinstance(value, float):
            value = [float(value), float(value), float(value)]
        else:
            value = tuple(float(x) for x in value)
        self.merge_nbt({'transformation': {'scale': value}})
        return self


class ItemDisplay(Display):
    """An object that represent an item_display entity."""

    def __init__(self, item: EntityDef):
        item = as_entity(item)
        nbt = Item.nbt_for(item)
        super().__init__('item_display', {'item': nbt})


def _str_values(state):
    """Convert any non-str primitive values into str, because BlockDisplay requires it (ugh)."""
    if isinstance(state, Mapping):
        for k, v in state.items():
            state[k] = _str_values(v)
        return state
    elif isinstance(state, str):
        return state
    elif isinstance(state, Sequence):
        values = []
        for v in state:
            values.append(_str_values(v))
        return values
    else:
        return Nbt.to_str(state)


class BlockDisplay(Display):
    """An object that represents a block_display entity."""

    def __init__(self, block: BlockDef):
        block = as_block(block)
        super().__init__('block_display', {'block_state': {'Name': block.id, 'Properties': _str_values(block.state)}})


class TextDisplay(Display):
    """An object that represents a text_display entity."""

    def __init__(self, text: str | JsonText | Sequence[JsonText] = None, nbt: NbtDef = None):
        """
        Creates a TextDisplay with the given text, if any. The text can be a string, a JsonText object, or a list or
        tuple of JsonText objects.
        """
        super().__init__('text_display', nbt)
        self.text(text)

    def text(self, text) -> TextDisplay:
        if isinstance(text, str):
            text = JsonText.text(text)
        elif isinstance(text, (JsonText, Sequence)):
            text = str(text).replace("'", '"')
        if text is not None:
            self.merge_nbt({'text': text})
        return self

    def _simple(self, key, value) -> TextDisplay:
        self.merge_nbt({key: de_arg(value)})
        return self


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
        item = as_block(item)
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

    def add_pattern(self, pattern: StrOrArg | Pattern, color: IntOrArg | StrOrArg) -> Shield:
        """Add a pattern to the shield."""
        color = as_color_num(color)
        patterns = self.nbt['tag']['BlockEntityTag'].get_list('Patterns')
        if isinstance(pattern, str):
            pattern = Pattern(pattern)
        patterns.append(Nbt({'Pattern': str(pattern), 'Color': color}))
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
        f = fill(self.start, self.end, as_block(new))
        if replace:
            f = f.replace(replace)
        yield f

    def fillbiome(self, biome: Biome, replace: Biome = None) -> Command:
        f = fillbiome(self.start, self.end, as_biome(biome))
        if replace:
            f = f.replace(as_biome(replace))
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
        new = as_block(new)
        old = as_block(old)

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
        """
        Replaces doors in the region using all the relevant states.
        N.B.: Not implemented, doors cannot be replaced generically, https://bugs.mojang.com/browse/MC-192791
        """
        raise NotImplementedError('Fill does not replace doors, sorry. https://bugs.mojang.com/browse/MC-192791')
        # yield from self.replace(new, old, Region.door_states, new_state, shared_states)

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
    # This is so complicated because some functions take specific-length tuples, so we want to declare that we produce
    # them to make the type checker happier.
    CoordsOut = Union[
        RelCoord, Tuple[RelCoord, RelCoord], Tuple[IntRelCoord, IntRelCoord], Tuple[RelCoord, RelCoord, RelCoord],
        float, Tuple[float, float], Tuple[int, int], Tuple[float, float, float], Tuple[int, int, int],
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

    def p(self, *values: CoordsIn) -> CoordsOut:
        """ Returns the result of offsetting the input, with each return value added to this object's coordinates. """
        return tuple(sum(i) for i in zip(values, self.position))

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

    def __init__(self, facing: int | str, *, glowing: bool = False, nbt: NbtDef = None, name: str = None):
        """Creates an ItemFrame object facing in the given direction. See as_facing() for useful values."""
        nbt = Nbt.as_nbt(nbt) if nbt else Nbt({})
        nbt = nbt.merge({'Facing': as_facing(facing).number, 'Fixed': True})
        super().__init__('glow_item_frame' if glowing else 'item_frame', nbt=nbt, name=name)

    def item(self, item: BlockDef | Entity) -> ItemFrame:
        """Sets the item that is in the frame."""
        block = as_block(item)
        self.merge_nbt({'Item': Item.nbt_for(block)})
        return self

    def fixed(self, value: bool) -> ItemFrame:
        self.nbt.set_or_clear('Fixed', value)
        return self

    def named(self, name: BlockDef = None) -> ItemFrame:
        """Sets the name displayed for the item in the frame."""
        block = as_block(name)
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
        values = Nbt({
            'buy': {'id': self.buy[0][0], 'Count': self.buy[0][1]},
            'sell': {'id': self.sell[0], 'Count': self.sell[1]},
            'rewardExp': self.reward_exp
        })
        if len(self.buy) > 1:
            values['buyB'] = {'id': self.buy[1][0], 'Count': self.buy[1][1]}
        values.set_or_clear('maxUses', self.max_uses)
        return values


def _to_def(block) -> tuple[Block, int]:
    if isinstance(block, tuple):
        return as_block(block[0]).id, block[1]
    return as_block(block).id, 1


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
        self.xp(0)
        self._trades: list[Trade] = []

    def xp(self, xp: int) -> Villager:
        """Sets the villager's experience."""
        self.nbt['VillagerData']['xp'] = xp
        self.merge_nbt({'VillagerData': {'xp': xp, 'level': self.level}})
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
            xp = self.nbt['VillagerData']['xp']
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
            profession = NONE
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
            item_nbt = Item.nbt_for(as_block(i[0]))
            item_nbt['Count'] = i[1]
            inventory.append(Nbt(item_nbt))
        return self


@dataclasses.dataclass
class PaintingInfo:
    """
    Class that holds detailed information on each painting, available from a Painting object's ``info`` field, or the
    Painting.INFO map.
    """
    id: str
    name: str
    size: Tuple[int, int]
    added: str
    desc: str
    original_artist: str = 'None'
    based_on: str = None
    source: str = None
    artist: str = 'Kristoffer Zetterstrand'
    used: bool = True


#         'stage': PaintingInfo('stage', 'The Stage is Set', (2, 2), 'Indev 20100223 / Alpha v1.1.1',
#                               """Scenery from Space Quest I, with the character Graham from the video game series
#                               King's Quest.""",
#                               source='Space Quest I / King\'s Quest'),

class Painting(Entity):
    """
    Represents a painting. This understands its different "facing" numbering, and the PaintingInfo objects
    """
    INFO = {
        'alban': PaintingInfo('alban', 'Albanian', (1, 1), 'Indev 20100223',
                              """A man wearing a fez next to a house and a bush. As the name of the painting
                              suggests, it may be a landscape in Albania"""),
        'aztec': PaintingInfo('aztec', 'de_aztec', (1, 1), 'Indev 20100223',
                              """Free-look perspective of the map 'de_aztec' from the video game 
                              <i>Counter-Strike.</i>""",
                              based_on='de_aztec', source='Counter-Strike'),
        'aztec2': PaintingInfo('aztec', 'de_aztec', (1, 1), 'Indev 20100223',
                               """Free-look perspective of the map 'de_aztec' from the video game 
                               <i>Counter-Strike.</i>""",
                               based_on='de_aztec', source='Counter-Strike'),
        'bomb': PaintingInfo('bomb', 'Target Successfully Bombed', (1, 1), 'Indev 20100223',
                             """The map 'de_dust2' from the video game <i>Counter-Strike,</i> named “target 
                             successfully bombed" in reference to the game.""",
                             based_on='de_dust2', source='Counter-Strike'),
        'kebab': PaintingInfo('kebab', 'Kebab med tre pepperoni', (1, 1), 'Indev 20100223',
                              """A kebab with three green chili peppers."""),
        'plant': PaintingInfo('plant', 'Paradisträd', (1, 1), 'Indev 20100223',
                              """Still life of two plants in pots. "Paradisträd" is Swedish for "money tree",
                              which is a common name for the depicted species in Scandinavia."""),
        'wasteland': PaintingInfo('wasteland', 'Wasteland', (1, 1), 'Indev 20100223',
                                  """Some wastelands; a small animal (presumably a rabbit) is sitting on the window
                                  ledge."""),
        'courbet': PaintingInfo('courbet', 'Bonjour Monsieur Courbet', (2, 1), 'Indev 20100223',
                                """Two hikers with pointy beards seemingly greeting each other. This painting is
                                based on Gustave Courbet's painting <i>The Meeting</i> or <i>"Bonjour,
                                Monsieur Courbet"</i>.""",
                                based_on='Bonjour Monsieur Courbet', original_artist='Gustave Courbet'),
        'pool': PaintingInfo('pool', 'The Pool', (2, 1), 'Indev 20100223',
                             """Some men and women skinny-dipping in a pool over a cube of sorts. Also there is an
                             old man resting in the lower-right edge."""),
        'sea': PaintingInfo('sea', 'Seaside', (2, 1), 'Indev 20100223 / Alpha v1.1.1',
                            """Mountains and a lake, with a small photo of a mountain and a bright-colored plant on
                            the window ledge."""),
        'creebet': PaintingInfo("creebet", 'Creebet', (2, 1), 'Alpha v1.1.1',
                                """Mountains and a lake, with a small photo of a mountain and a creeper looking at
                                the viewer through a window."""),
        'sunset': PaintingInfo('sunset', 'Sunset Dense', (2, 1), 'Indev 20100223', """Mountains at sunset."""),
        'graham': PaintingInfo('graham', 'Graham', (1, 2), 'Alpha v1.1.1',
                               """King Graham, the player character in the video game series <i>King's Quest<i>.""",
                               based_on='Still Life with Quince, Cabbage, Melon, and Cucumber',
                               original_artist='Juan Sánchez Cotán', source='King\'s Quest'),
        'wanderer': PaintingInfo('wanderer', 'Wanderer', (1, 2), 'Indev 20100223',
                                 """A version of Caspar David Friedrich's famous painting Wanderer above the Sea of 
                                 Fog.""",
                                 based_on='Wanderer above the Sea of Fog', original_artist='Caspar David Friedrich'),
        'bust': PaintingInfo('bust', 'Bust', (2, 2), 'Indev 20100223',
                             """Bust of Marcus Aurelius surrounded by fire."""),
        'match': PaintingInfo('match', 'Match', (2, 2), 'Indev 20100223',
                              """A hand holding a match, causing fire on a white cubic gas fireplace."""),
        'skull_and_roses': PaintingInfo('skull_and_roses', 'Skull and Roses', (2, 2), 'Indev 20100223',
                                        """A skeleton at night with red flowers in the foreground."""),
        'stage': PaintingInfo('stage', 'The Stage is Set', (2, 2), 'Indev 20100223 / Alpha v1.1.1',
                              """Scenery from Space Quest I, with the character Graham from the video game series
                              King's Quest.""",
                              source='Space Quest I / King\'s Quest'),
        'void': PaintingInfo('void', 'The void', (2, 2), 'Indev 20100223',
                             """An angel praying into a void with fire below."""),
        'wither': PaintingInfo('wither', 'Wither', (2, 2), 'Java Edition 1.4.2',
                               """The creation of a wither. This is the only painting not based on a real painting.""",
                               artist='Jens Bergensten'),
        'fighters': PaintingInfo('fighters', 'Fighters', (4, 2), 'Indev 20100223',
                                 """Two men poised to fight. Paper versions of fighters from the game
                                 <i>International Karate +</i>.""",
                                 source='International Karate +'),
        'donkey_kong': PaintingInfo('donkey_kong', 'Kong', (4, 3), 'Alpha v1.1.1',
                                    """Level 100 from the arcade game <i>Donkey Kong.</i>""", source='Donkey Kong'),
        'skeleton': PaintingInfo('skeleton', 'Mortal Coil', (4, 3), 'Alpha v1.1.1',
                                 """Bruno Martinez from the adventure game <i>Grim Fandango.</i>""",
                                 source='Grim Fandango'),
        'burning_skull': PaintingInfo('burning_skull', 'Skull on Fire', (4, 4), 'Beta 1.2_01 / Beta 1.3',
                                      """A Skull on fire; in the background there is a moon in a clear night sky.
                                      Based on a <i>Minecraft</i> screenshot, with grass blocks and a 3D skull added
                                      on top.""",
                                      source='Minecraft'),
        'pigscene': PaintingInfo('pigscene', 'Pigscene', (4, 4), 'Alpha v1.1.1',
                                 """A girl pointing to a pig on a canvas.""", based_on='The Artist\'s Studio',
                                 original_artist='Jacob van Oost'),
        'pointer': PaintingInfo('pointer', 'Pointer', (4, 4), 'Indev 20100223',
                                """The main character of the game <i>International Karate +</i> in a fighting stance
                                touching a large hand. It can be interpreted as a play on Michelangelo's famous
                                painting "The Creation of Adam".""",
                                source='International Karate +'),
        'earth': PaintingInfo('earth', 'Earth', (2, 2), '22w16a', """The classical element Earth""", used=False),
        'fire': PaintingInfo('fire', 'Fire', (2, 2), '22w16a', """The classical element Fire""", used=False),
        'water': PaintingInfo('water', 'Water', (2, 2), '22w16a', """The classical element Water""", used=False),
        'wind': PaintingInfo('wind', 'Wind', (2, 2), '22w16a', """The classical element Wind""", used=False),
    }
    """PaintingInfo objects for paintings"""

    def __init__(self, variant: str):
        variant = to_id(variant)
        if variant not in self.INFO:
            raise ValueError(f'{variant}: Unknown painting variant')
        self.variant = variant
        super().__init__('painting', nbt={'variant': variant})

    @property
    def info(self):
        return Painting.INFO[self.variant]

    def summon(self, pos: Position, nbt: NbtDef = None, facing: FacingDef = NORTH, lower_left=False) -> str:
        """
        Overrides to add ``ll`` parameter which, if true, uses the lower-left corner consistently for all sizes of
        paintings.
        """
        nbt, facing = self._summon_clean(nbt, facing)
        if facing:
            nbt['facing'] = facing.h_number
        del nbt['Facing']
        del nbt['Rotation']
        nbt['variant'] = self.variant
        if lower_left:
            movement = facing.turn(90)
            x, y = self.info.size
            pos = _to_list(pos)
            if x > 2:
                adj = x - 3
                pos[0] += adj * movement.dx
                pos[2] += adj * movement.dz
            if y > 2:
                pos[1] += 1
        return super().summon(pos, nbt)


def as_color(color: IntOrArg | StrOrArg | None) -> str | None:
    """Checks if the argument is a valid color name, or None.

    "Valid" means one of the 16 known colors, such as those used for wool. These are stored in the
    ``COLORS`` array.

    An Arg is also valid.

    :param color: The ((probable) color name.
    :return: The color name, in lower case.
    """
    if isinstance(color, Arg):
        return str(color)
    if color is None:
        return None
    color_num = as_color_num(color)
    return COLORS[color_num]


def as_color_num(color: IntOrArg | StrOrArg | None) -> int | str | None:
    """Checks if the argument is a valid color number specification, or None.

    "Valid" means an int, or a string that names a known color from which a color number can be inferred.
    Color numbers range from 0 to 15. (See as_color() for a documentation on color names.)

    An Arg is also valid.

    :param color:
    :return:
    """
    if isinstance(color, Arg):
        return str(color)
    if color is None:
        return None
    if isinstance(color, str):
        color_num = COLORS.index(to_id(color))
        if color_num < 0:
            raise ValueError(f'{color}: Unknown color')
        return color_num
    if color not in range(len(COLORS)):
        raise ValueError(f'{color}: Unknown color')
    return color
