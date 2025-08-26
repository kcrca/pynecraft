from __future__ import annotations

import dataclasses
from typing import Callable, Mapping, MutableMapping, Sequence, Tuple, Union

from .base import Arg, FacingDef, IntOrArg, IntRelCoord, NORTH, Nbt, NbtDef, Position, RelCoord, StrOrArg, \
    Transform, _ensure_size, _in_group, _to_list, as_facing, d, de_arg, is_arg, r, to_id
from .commands import Block, BlockDef, COLORS, ClickEvent, Command, Commands, Entity, EntityDef, SignCommand, \
    SignCommands, SignMessage, SignMessages, SomeMappings, Text, TextDef, TextList, a, as_biome, as_block, \
    as_entity, \
    as_text, data, e, execute, fill, fillbiome, n, return_, scoreboard, setblock
from .values import PaintingInfo, as_pattern, paintings

ARMORER = 'armorer'
BUTCHER = 'butcher'
CARTOGRAPHER = 'cartographer'
CLERIC = 'cleric'
FARMER = 'farmer'
FISHERMAN = 'fisherman'
FLETCHER = 'fletcher'
LEATHERWORKER = 'leatherworker'
LIBRARIAN = 'librarian'
MASON = 'mason'
NITWIT = 'nitwit'
SHEPHERD = 'shepherd'
TOOLSMITH = 'toolsmith'
WEAPONSMITH = 'weaponsmith'
NONE = 'none'
CHILD = 'child'
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

DESERT = 'desert'
JUNGLE = 'jungle'
PLAINS = 'plains'
SAVANNA = 'savanna'
SNOW = 'snow'
SWAMP = 'swamp'
TAIGA = 'taiga'
VILLAGER_BIOMES = (DESERT, JUNGLE, PLAINS, SAVANNA, SNOW, SWAMP, TAIGA)
"""Villager biomes / types."""


class Sign(Block):
    """A class that represents a sign. This class is a standing sign, the WallSign subclass is for wall signs."""
    default_wood = 'oak'
    """If not specified in the constructor, this is the default wood for the sign."""
    waxed = False
    """Whether signs are waxed by default."""

    def __init__(self, text: SignMessages = (), /, commands: SignCommands = (), wood=None, state: Mapping = None,
                 nbt: NbtDef = None, hanging=False, front=None):
        """
        Creates a sign object. The text, commands, and front are passed to messages().
        """
        wood = wood if wood else Sign.default_wood
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
    def lines_nbt(cls, messages: SignMessages, commands: SignCommands = ()) -> Nbt:
        """Returns the lines of NBT for sign text.
        :param messages: The sign text, as an iterable of one to four lines of text. Entries that are None will
            generate no NBT, any text will generate a line for the sign.
        :param commands: Commands for the sign, in order.
        :return: The NBT for the combination of text and commands.
        """
        messages = _ensure_size(_to_list(messages), 4)
        commands = _ensure_size(_to_list(commands), 4)
        max_count = max(len(messages), len(commands))
        if max_count > 4:
            raise ValueError(f'{max_count}: Too many values for text and/or commands')
        messages = _ensure_size(messages, 4)
        commands = _ensure_size(commands, 4)

        lines = []
        for i in range(4):
            lines.append(cls.line_nbt(messages[i], commands[i]))

        return Nbt({'messages': lines})

    def _kind_name(self, wood):
        return f'{wood}_hanging_sign' if self.hanging else f'{wood}_sign'

    @classmethod
    def line_nbt(cls, text: SignMessage = None, command: SignCommand = None) -> Nbt:
        orig_text = text
        if text is None:
            text = Text.text('')
        elif is_arg(text) or isinstance(text, str):
            text = Text.text(de_arg(text))
        entry = text
        if isinstance(command, Callable):
            command = command(orig_text)
        if command:
            entry = text.click_event(ClickEvent.run_command(command))
        if len(entry) == 1 and 'text' in entry:
            return entry['text']
        return entry

    @classmethod
    def change(cls, pos: Position, messages: SignMessages = None, commands: SignCommands = None,
               front=None, start=0, blanks=False, min_len: int = None) -> Commands:
        empty_msg = ('',) if blanks else (None,)
        if not messages:
            messages = empty_msg * (4 - start)
        commands = commands if commands else (None,) * (4 - start)
        if min_len is not None:
            messages += (min_len - len(messages)) * ('',)
            commands += (min_len - len(commands)) * (None,)
        if len(messages) > 4:
            raise ValueError(f'More than 4 messages: {messages}')
        if len(commands) > 4:
            raise ValueError(f'More than 4 commands: {commands}')
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
                    data().modify(pos, f'{face}.messages[{i + start}]').set().value(cls.line_nbt(msg, cmd)))
                added += 1
            if added == 4:
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
        :param clear: Set output place to air (or water) before setting the sign
        :return: The commands to place the sign.
        """
        self._orientation(facing)
        if water:
            self.merge_state({'waterlogged': True})
        if nbt:
            self.merge_nbt(nbt)
        if clear and water:
            return (
                setblock(pos, 'water'),
                setblock(pos, self),
            )
        return setblock(pos, self)

    def _orientation(self, facing):
        self.merge_state({'rotation': as_facing(facing).sign_rotation})


class WallSign(Sign):
    """A class for wall signs."""

    def _kind_name(self, wood):
        return f'{wood}_wall_hanging_sign' if self.hanging else f'{wood}_wall_sign'

    def _orientation(self, facing):
        self.merge_state({'facing': as_facing(facing).name})

    def place(self, pos: Position, facing: FacingDef, /, water=False, nbt: NbtDef = None,
              clear=True) -> Commands | Command:
        """When placing a wall sign, the orientations are different, but also can be found in as_facing()."""
        return super().place(pos, facing, water, nbt, clear)


class Book:
    """A class for a book."""

    def __init__(self, title: str = None, author: str = None, display_name: TextDef | Tuple[TextDef, ...] = None):
        """Creates a book object."""
        self.title = title
        self.author = author
        self._display_name = None
        self.display_name = display_name
        self._pages = []
        self._cur_page = TextList()

    @property
    def display_name(self) -> Tuple[Text, ...] | None:
        return self._display_name

    @display_name.setter
    def display_name(self, display_name: TextDef | Tuple[TextDef, ...] = None) -> None:
        if display_name is None:
            self._display_name = None
        else:
            self._display_name = []
            if isinstance(display_name, str):
                self._display_name.append(str(as_text(display_name)))
            else:
                for x in display_name:
                    self._display_name.append(as_text(x))

    # Two kinds of books: Written and signed. In theory, they should hold the same kind
    # of text, but the unsigned book cannot have rich text. Hopefully in the future this _will_ be possible, so
    # this method is kept separate instead of being incorporated into the __init__ of a
    # "signed book" class that is separate from the "unsigned book" class. Or some such design.
    def sign_book(self, title: str, author: str, display_name: str = None):
        """Sign the book. An unsigned book cannot have rich text."""
        self.title = title
        self.author = author
        self.display_name = display_name

    def add(self, *txt: Text | StrOrArg):
        """Add text to the current page of the book."""
        if self.title is None:
            raise ValueError("Cannot add text to unsigned book")
        for t in txt:
            if isinstance(t, str) or is_arg(t):
                t = Text.text(de_arg(t))
            self._cur_page.append(t)

    def next_page(self):
        """Start the next page."""
        self._pages.append(self._cur_page)
        self._cur_page = TextList()

    def as_entity(self):
        """Returns the book as an Entity object. This is useful for a ``give`` command."""
        return Entity('written_book', components=self.nbt())

    def as_item(self):
        """Returns the book as an Item object. This is useful for things like putting the book into a container."""
        nbt = self.nbt()
        item = Item.nbt_for('written_book', {'components': nbt})
        return Nbt({'Book': item})

    def nbt(self):
        """Returns the NBT for the book."""
        cur_page = self._cur_page
        self.next_page()
        components = {'written_book_content': {
            'author': self.author, 'title': self.title, 'pages': [{'raw': x} for x in self._pages[:]]}}
        if self.display_name:
            components['lore'] = self.display_name
        self._cur_page = cur_page
        self._pages.pop()
        return components


class Display(Entity):
    """
    A class for the various "display" objects: text_display, item_display, and block_display. The main feature is that
    it makes transformation modifications work on the summon command; see https://bugs.mojang.com/browse/MC-259838.
    """

    def __init__(self, id: str, *args, **kwargs):
        super().__init__(id, **kwargs)
        # Without this, a simple change to the transform cannot be given at summon time.
        # Crazily, this is "as intended": https://bugs.mojang.com/browse/MC-259838
        # We have to be careful because the supplied nbt may override part of the transformation.
        if 'transformation' not in self.nbt:
            self.transform(Transform.IDENTITY)
        else:
            tr = self.nbt['transformation']
            for t, v in Transform.IDENTITY.nbt().items():
                if t not in tr:
                    tr[t] = v

    def scale(self, value: float | Tuple[float, float, float]) -> Display:
        """
        Sets the scale transformation. If only given one value, it uses that for all three scale values. Otherwise,
        it must be given the three values.
        """
        if 'transformation' not in self.nbt:
            self.transform(Transform.IDENTITY)
        if isinstance(value, (int, float)):
            value = [float(value), float(value), float(value)]
        else:
            value = tuple(float(x) for x in value)
        self.merge_nbt({'transformation': {'scale': list(value)}})
        return self

    def transform(self, transform: Transform) -> Display:
        self.merge_nbt({'transformation': transform.nbt()})
        return self


class ItemDisplay(Display):
    """An object that represent an item_display entity."""

    def __init__(self, item: EntityDef):
        item = as_entity(item)
        nbt = Item.nbt_for(item)
        super().__init__('item_display', {'item': nbt})


def _str_values(state):
    """Convert any non-str primitive values into str, because BlockDisplay requires it (ugh)."""
    if isinstance(state, MutableMapping):
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

    def __init__(self, text: StrOrArg | Text | Sequence[Text] = None, *args, **kwargs):
        """
        Creates a TextDisplay with the given text, if any. The text can be a string, a Text object, or a list or
        tuple of Text objects.
        """
        super().__init__('text_display', *args, **kwargs)
        self.text(text)

    def text(self, text) -> TextDisplay:
        if isinstance(text, str):
            text = Text.text(text)
        if text is not None:
            self.merge_nbt({'text': text})
        return self

    def _simple(self, key, value) -> TextDisplay:
        self.merge_nbt({key: de_arg(value)})
        return self


class Item(Entity):
    """An object that represents an Item."""

    def __init__(self, id: str, count: int = 1, name=None, nbt=None, components=None):
        super().__init__(id, components=components, name=name)
        if count != 1:
            self.merge_nbt({'Count': count})
        if nbt:
            self.merge_nbt(nbt)

    @classmethod
    def nbt_for(cls, item: BlockDef, nbt=None, count=1) -> Nbt:
        """The nbt for this item."""
        item = as_block(item)
        item_id = item.id
        # !! Remove this hack?
        if item_id and item_id.find(':') < 0:
            item_id = 'minecraft:' + item_id
        retval = Nbt({'id': item_id})
        if count != 1:
            retval = retval.merge({'count': count})
        # Filled maps are stored directly, not shunted an inner tag
        if item_id:
            if item_id == 'minecraft:filled_map':
                retval = retval.merge(item.nbt)
                if nbt:
                    retval = retval.merge(nbt)
            elif item.nbt:
                retval['components']['block_entity_data'] = item.nbt
        try:
            block_state = item.state
            if block_state:
                retval['components'] = {'block_entity_data': block_state}
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

    def color(self, color: StrOrArg | None) -> Shield:
        if color:
            self.nbt['components']['base_color'] = de_arg(color)
        else:
            try:
                del self.nbt['components']['base_color']
            except KeyError:
                pass
        return self

    def add_pattern(self, pattern: StrOrArg, color: IntOrArg | StrOrArg) -> Shield:
        """Add a pattern to the shield."""
        color = as_color(color)
        patterns = self.nbt['components'].get_list('banner_patterns')
        if isinstance(pattern, str):
            pattern = as_pattern(pattern)
        patterns.append(Nbt({'pattern': str(pattern), 'color': color}))
        return self

    def clear_patterns(self) -> Shield:
        """Remove all patterns from the shield."""
        try:
            del self.nbt['components']['banner_patterns']
        except KeyError:
            pass
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

    def fillbiome(self, biome: StrOrArg, replace: StrOrArg = None) -> Command:
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
        float, Tuple[float, float], Tuple[int, int], Tuple[float, float, float], Tuple[int, int, int], Tuple[
            float, ...], Tuple[int, ...],
        Tuple[RelCoord, ...]]

    def __init__(self, *position: float):
        """Creates an offsetting object with the given values."""
        if len(position) == 0:
            raise ValueError(f'Must have at least one value in offset')
        # noinspection PyTypeChecker
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
        # noinspection PyTypeChecker
        vals = RelCoord.add(vec, self.position)
        if len(vals) == 1:
            return vals[0]
        return vals


class ItemFrame(Entity):
    """A class for item frames."""

    def __init__(self, facing: FacingDef, *, glowing: bool = False, nbt: NbtDef = None, name: str = None):
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
                del self.nbt['Item']['components']['custom_name']
            except KeyError:
                pass  # Must not be there already, ignore the error
        else:
            if 'Item' not in self.nbt:
                self.item(block)
            nbt = self.nbt
            nbt['Item']['components']['custom_name'] = Text.text(block.name)
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
        for k, v in values.items():
            if k != 'rewardExp' and v['Count'] == 1:
                del v['Count']
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

    def __init__(self, profession: str = NONE, biome: str = PLAINS, nbt: NbtDef = None, /, name=None,
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
        profession = profession.lower()
        if profession == 'child':
            if self.zombie:
                raise ValueError('child: Invalid zombie villager profession')
            profession = NONE
            self.merge_nbt({'Age': -2147483648})
        self.merge_nbt({'VillagerData': {'profession': _in_group(VILLAGER_PROFESSIONS, profession)}})
        return self

    def biome(self, biome: str) -> Villager:
        """Sets the villager's biome."""
        self.merge_nbt({'VillagerData': {'type': _in_group(VILLAGER_BIOMES, biome)}})
        return self

    type = biome
    """Alias for the ``biome`` method, because these two terms are used interchangeably."""

    def add_trade(self, *trades: Trade | NbtDef) -> Villager:
        """Add trades to the villager's list."""
        recipes = self.nbt['Offers'].get_list('Recipes')
        for t in trades:
            if isinstance(t, Trade):
                if len(t.buy) not in (1, 2):
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
            if i[1] != 1:
                item_nbt['Count'] = i[1]
            inventory.append(Nbt(item_nbt))
        return self


class Painting(Entity):
    """
    Represents a painting. This understands its different "facing" numbering, and the PaintingInfo objects
    """

    def __init__(self, variant: str):
        variant = to_id(variant)
        if variant not in paintings:
            raise ValueError(f'{variant}: Unknown painting variant')
        self.variant = variant
        super().__init__('painting', nbt={'variant': variant})

    @property
    def info(self) -> PaintingInfo:
        return paintings[self.variant]

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


def _as_tuple(v):
    if isinstance(v, tuple):
        return v
    if isinstance(v, list):
        return tuple(v)
    return (v,)


class Trigger:
    """
    This class presents a simple model for basic triggers. Given a score, it creates commands for a function that can
    be run in a repeating command block testing for trigger values and acting on them if so,
    then resetting/re-enabling the trigger. It also builds commands for an init function that sets up the objective.

    Specifically, on each tick the first check will be a fast-reject: Does any player have any score in the
    objective? If not, return 0. Otherwise, for each of the values for which a trigger has been defined by calling
    trigger(), if any player has that value in the objective, it will execute the commands for that trigger once (no
    matter how many players have that value). Once these have all been tested, all players' scores are cleared form
    the objective, and the objective is enabled for all players.

    There is an init function defined by the init() method that ensures the objective exists with no scores and all
    players are enabled. You should call this to set (or reset) the triggers.
    """

    def __init__(self, name: str):
        """
        :param name: The objective to use. It must be of type 'trigger', though we cannot validate that here. The
        init_cmds() functions returns commands for initializing it if you need that.
        """
        self.name = name
        self._values = set()
        self._pre = [
            execute().unless().entity(n().scores({self.name: (0, None)})).run(return_(0))
        ]
        self._cmds = []
        self._post = [
            scoreboard().players().reset((a(), self.name)),
            scoreboard().players().enable((a(), self.name)),
        ]

    def trigger(self, cmd: str | Command | Commands, value: int = 1) -> Trigger:
        """Defines an action for a given trigger value."""
        if value in self._values:
            raise ValueError(f'{value}: Duplicate trigger value')
        self._cmds.append(execute().if_().entity(e().scores({self.name: value})).run(cmd))
        self._values.add(value)
        return self

    def commands(self) -> list[str]:
        """Returns the commands that should be run when you want the actions to run."""
        if len(self._values) == 0:
            raise ValueError('No values for trigger')
        return self._pre + self._cmds + self._post

    def init_commands(self) -> Commands:
        """Returns the commands to initialize the objective."""
        return scoreboard().objectives().add(self.name, 'trigger'), self._post
