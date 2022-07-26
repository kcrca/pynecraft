from __future__ import annotations

from typing import Callable, Mapping

from .base import FacingDef, Nbt, NbtDef, Position, _ensure_size, _in_group, _quote, _to_list, good_facing, to_id
from .commands import Block, BlockDef, COLORS, Command, Commands, Entity, JsonList, JsonText, SignCommands, \
    SignText, \
    SomeMappings, fill, good_block, good_color_num, setblock
from .enums import Pattern


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
            raise ValueError('%d: Too many values for text and/or commands' % max_count)
        text = _ensure_size(text, 4)
        commands = _ensure_size(commands, 4)

        nbt = Nbt()
        for i, entry in enumerate(tuple(zip(text, commands))):
            if entry == (None, None):
                continue
            txt, cmd = entry
            if txt is None:
                txt = ''
            key = 'Text%d' % (i + 1)
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
        """The sign's text"""
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

    def place(self, pos: Position, facing: FacingDef, /, water=False, nbt: NbtDef = None) -> Commands:
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
        return (
            setblock(pos, 'water' if water else 'air'),
            setblock(pos, self),
        )

    def _orientation(self, facing):
        self.merge_state({'rotation': good_facing(facing).sign_rotation})


class WallSign(Sign):
    """A class for wall signs."""

    def _kind_name(self, wood):
        return wood + '_wall_sign'

    def _orientation(self, facing):
        self.merge_state({'facing': good_facing(facing).name})

    def place(self, pos: Position, facing: FacingDef, /, water=False, nbt: NbtDef = None) -> Commands:
        """When placing a wall sign, the orientations are different, but also can be found in good_facing()."""
        return super().place(pos, facing, water, nbt)


_backslash_map = {'"': '"', '\\': '\\', '\a': 'a', '\b': 'b', '\f': 'f', '\n': 'n', '\r': 'r', '\t': 't', '\v': 'v'}

_fm = {}
for k, v in _backslash_map.items():
    _fm[v] = k


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
        jt['pages'] = list(JsonList(x) for x in self._pages[:])
        self._cur_page = cur_page
        self._pages.pop()
        return jt


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
            else:
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


class Volume:
    """Represents a volume of space, and gives tools for changing items within it."""
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
    axes_states = tuple(Nbt({'axis': x}) for x in ('x', 'y', 'z'))
    """X, y, and z. Pillars and logs use this, for example."""
    rail_states = tuple(Nbt({'shape': x}) for x in ('east_west', 'north_south') + tuple(
        'ascending_%s' % x for x in ('east', 'west', 'north', 'south')))
    """The block states that rails can have related to its placements."""
    curved_rail_states = tuple(Nbt({'shape': x}) for x in ('north_east', 'north_west', 'south_east', 'south_west'))
    """The block states that curved rails can have related to its placements."""

    def __init__(self, start: Position, end: Position):
        """Creates a new volume object. Any two opposite corners will do."""
        self.start = start
        self.end = end

    def fill(self, new: BlockDef, replace: BlockDef = None) -> Command:
        """Returns a command that will the volume with a block. If a second block is given, it will be the filter; only this kind of block
        will be replaced. This can, of course, be a tag."""
        f = fill(self.start, self.end, good_block(new))
        if replace:
            f = f.replace(replace)
        yield f

    def replace(self, new: BlockDef, old: BlockDef, states: SomeMappings = None,
                added_states: SomeMappings = None) -> Commands:
        """Returns commands that will replace one with block with another. If states are given, commands will be
        generated for each state, applied to both the fill block and the filter block. States are specified by a map,
        and can be passed as a single state, or an Iterable of them. One command will be generated for each combination
        of the two sets of states."""
        states = _to_list(states) if states else [{}]
        added_states = _to_list(added_states) if added_states else [{}]
        new = good_block(new)
        old = good_block(old)

        if not states and not added_states:
            yield from self.fill(new, old)
        else:
            for added in added_states:
                n = new.clone().merge_state(added)
                o = old.clone().merge_state(added)
                for s in states:
                    yield from self.fill(n.clone().merge_state(s), o.clone().merge_state(s))

    def replace_slabs(self, new: BlockDef, old: BlockDef = '#slabs', added_state: Mapping = None) -> Commands:
        """Replaces slabs in the volume using all the relevant states."""
        yield from self.replace(new, old, Volume.slab_states, added_state)

    def replace_stairs(self, new: BlockDef, old: BlockDef = '#stairs', added_state: Mapping = None) -> Commands:
        """Replaces stairs in the volume using all the relevant states."""
        yield from self.replace(new, old, Volume.stair_states, added_state)

    def replace_buttons(self, new: BlockDef, old: BlockDef = '#buttons', added_state: Mapping = None) -> Commands:
        """Replaces buttons in the volume using all the relevant states."""
        yield from self.replace(new, old, Volume.button_states, added_state)

    def replace_doors(self, new: BlockDef, old: BlockDef = '#doors', added_state: Mapping = None) -> Commands:
        """Replaces doors in the volume using all the relevant states."""
        yield from self.replace(new, old, Volume.door_states, added_state)

    def replace_trapdoors(self, new: BlockDef, old: BlockDef = '#trapdoors', added_state: Mapping = None) -> Commands:
        """Replaces trapdoors in the volume using all the relevant states."""
        yield from self.replace(new, old, Volume.trapdoor_states, added_state)

    def replace_facing(self, new: BlockDef, old: BlockDef, added_state: Mapping = None) -> Commands:
        """Replaces blocks in the volume using all the "facing"" states."""
        yield from self.replace(new, old, Volume.facing_states, added_state)

    def replace_facing_all(self, new: BlockDef, old: BlockDef, added_state: Mapping = None) -> Commands:
        """Replaces blocks in the volume using all the "all_facing"" states."""
        yield from self.replace(new, old, Volume.facing_all_states, added_state)

    def replace_axes(self, new: BlockDef, old: BlockDef, added_state: Mapping = None) -> Commands:
        """Replaces blocks in the volume using all the "axes"" states."""
        yield from self.replace(new, old, Volume.axes_states, added_state)

    def replace_straight_rails(self, new: BlockDef, old: BlockDef = '#rails', added_state: Mapping = None) -> Commands:
        """Replaces straight rails in the volume using all the relevant states."""
        yield from self.replace(new, old, Volume.rail_states, added_state)

    def replace_curved_rails(self, new: BlockDef = "rail", old: BlockDef = '#rails',
                             added_state: Mapping = None) -> Commands:
        """Replaces curved rails in the volume using all the relevant states."""
        yield from self.replace(new, old, Volume.curved_rail_states, added_state)


class ItemFrame(Entity):
    """A class for item frames."""

    def __init__(self, facing: int | str, glowing: bool = None, nbt=None):
        """Creates an ItemFrame object facing in the given direction. See good_facing() for useful values."""
        nbt = Nbt.as_nbt(nbt) if nbt else Nbt({})
        nbt = nbt.merge({'Facing': good_facing(facing).number, 'Fixed': True})
        super().__init__('glow_item_frame' if glowing else 'item_frame', nbt=nbt)

    def item(self, item: BlockDef) -> ItemFrame:
        """Sets the item that is in the frame."""
        block = good_block(item)
        self.merge_nbt({'Item': Item.nbt_for(block)})
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
