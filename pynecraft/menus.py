from __future__ import annotations

import re
from typing import Callable, Iterable, Tuple, Mapping

from pynecraft.base import FacingDef, good_facing, Position, Facing, ROTATION_270, DOWN
from pynecraft.commands import fill, BlockDef, function
from pynecraft.function import Function
from pynecraft.simpler import WallSign


class Menu:
    def __init__(self, tag_base: str, function_factory: Callable[[str], Function], action: Callable[[str], str],
                 /, wood: BlockDef = 'oak', selected_wood: BlockDef = 'birch', top_blank=True):
        self._tag_base = tag_base
        self._function_factory = function_factory
        self._action = action
        self._wood = wood
        self._selected_wood = selected_wood
        self._top_blank = top_blank
        self._entries = []
        # noinspection PyArgumentList
        self.reset = function_factory('reset', home=False)
        self.init = function_factory('init')

    def add(self, to_add: str | Submenu | Iterable[str | Menu]):
        if isinstance(to_add, (str, Submenu)):
            self._entries.append(to_add)
        else:
            for item in to_add:
                self.add(item)
        return self

    def place(self, pos: Position, facing: FacingDef) -> Mapping[str, Function]:
        _Placement(self, pos, good_facing(facing)).place()
        return {'init': self.init, 'reset': self.reset}

    def end(self, pos: Position, facing: FacingDef) -> Position:
        facing = good_facing(facing)
        dim = self._dim()
        return (pos[0] + (dim[0] - 1) * facing.dx, pos[1] - (dim[1] - 1),
                pos[2] + (dim[0] - 1) * facing.dz)

    def _dim(self) -> Tuple[int, int]:
        if not self._entries:
            return (0, 0)
        w, h = (len(self._entries), 1)
        for i, e in enumerate(self._entries):
            if isinstance(e, Menu):
                subdim = e._dim()
                w = max(w, i + subdim[0])
                h = max(h, 1 + subdim[1])
        return w, h


class _Placement:
    def __init__(self, menu: Menu, pos: Position, facing: Facing):
        self.menu = menu
        self.pos = pos
        self.facing = facing
        self.place_in = facing.turn(ROTATION_270)
        self.down = good_facing(DOWN)

        # Just to keep the checker happy, so it knows these exist
        self.top_blank = None
        self.entries = None
        self.action = None
        self.wood = None
        self.selected_wood = None
        self.init = None
        self.reset = None

        for k, v in menu.__dict__.items():
            self.__dict__[re.sub('^_', '', k)] = v

    def place(self):
        if not self.entries:
            return
        self.reset.add(fill(self.pos, self.menu.end(self.pos, self.facing), 'air'))

        self.init.add(function(self.reset))
        for i, e in enumerate(self.entries):
            self.init.add(self.place_sign(i, e))

    def place_sign(self, offset, entry):
        if isinstance(entry, Submenu):
            sign = entry._menu_sign()
        else:
            text = tuple(x.strip() for x in entry.split('|'))
            if self.top_blank and len(text) < 4:
                text = (None,) + text
            sign = WallSign(text, self.commands(entry), wood=self.wood)
        yield sign.place(self.place_in.move(self.pos, offset), self.facing)

    def commands(self, entry) -> Tuple[str, ...]:
        return (str(self.action(entry)),)


class Submenu(Menu):
    def __init__(self, name: str, parent: Menu, function_factory: Callable[[str], Function] = None,
                 action: Callable[[str], str] = None, /, wood: BlockDef = None, selected_wood: BlockDef = None):
        if not function_factory:
            function_factory = parent._function_factory
        if not action:
            action = parent._action
        if not wood:
            wood = parent._wood
        if not selected_wood:
            wood = parent._selected_wood
        super().__init__(parent._tag_base, function_factory, action, wood, selected_wood)
        self._name = name

    def _menu_sign(self):
        return WallSign((None, self._name))
