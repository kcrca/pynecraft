from __future__ import annotations

from typing import Callable, Iterable, Tuple

from pynecraft.base import FacingDef, good_facing, Position, Facing, ROTATION_270, DOWN
from pynecraft.commands import fill, BlockDef, function, execute, Selector, e
from pynecraft.function import Function
from pynecraft.simpler import WallSign


class Menu:

    def __init__(self, home: str | Selector, function_factory: Callable[[str], Function], action: Callable[[str], str],
                 /, wood: BlockDef = 'oak', selected_wood: BlockDef = 'birch', top_blank=True):
        self._home = home if isinstance(home, Selector) else e().tag(home).limit(1)
        if not self._home.is_single():
            raise ValueError(f'{home}: Selecting multiple not allowed')
        self._function_factory = function_factory
        self._action = action
        self._wood = wood
        self._selected_wood = selected_wood
        self._top_blank = top_blank
        self._entries = []
        self.__functions = {}
        self._func_prefix = ''

    def func(self, name):
        name = self._func_prefix + name
        try:
            return self._funcs()[name]
        except KeyError:
            func = self._funcs()[name] = self._function_factory(name)
            return func

    def _funcs(self):
        return self.__functions

    def add(self, to_add: str | Submenu | Iterable[str | Submenu]):
        if isinstance(to_add, (str, Submenu)):
            self._entries.append(to_add)
        else:
            for item in to_add:
                self.add(item)
        return self

    def place(self, pos: Position, facing: FacingDef) -> None:
        Placement(self, pos, good_facing(facing)).place()

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
            if isinstance(e, Submenu):
                subdim = e._dim()
                w = max(w, i + subdim[0])
                h = max(h, 1 + subdim[1])
        return w, h

    def _to_text(self, entry: str):
        text = tuple(x.strip() for x in entry.split('|'))
        if self._top_blank and len(text) < 4:
            text = (None,) + text
        return text


class Placement:
    def __init__(self, menu: Menu, pos: Position, facing: Facing):
        self.menu = menu
        self.pos = pos
        self.facing = facing
        self.placing = facing.turn(ROTATION_270)
        self.down = good_facing(DOWN)

    def place(self):
        if not self.menu._entries:
            return
        init = self.menu.func('init')
        init.add(fill(self.pos, self.menu.end(self.pos, self.placing), 'air'))
        for i, e in enumerate(self.menu._entries):
            init.add(self.place_sign(i, e))

    def place_sign(self, offset, entry):
        if isinstance(entry, Submenu):
            submenu_pos = self.down.move(self.placing.move(self.pos, offset), 1)
            entry.place(submenu_pos, self.facing)
            sign = entry._menu_sign(submenu_pos, self.facing)
        else:
            text = self.menu._to_text(entry)
            sign = WallSign(text, self.commands(entry), wood=self.menu._wood)
        yield sign.place(self.placing.move(self.pos, offset), self.facing, clear=False)

    def commands(self, entry) -> Tuple[str, ...]:
        return execute().at(self.menu._home).run(
            function(self.menu.func('init')),
            self.menu._action(entry))


class Submenu(Menu):
    def __init__(self, parent: Menu, name: str, function_factory: Callable[[str], Function] = None,
                 action: Callable[[str], str] = None, /, text: str = None, wood: BlockDef = None,
                 selected_wood: BlockDef = None):
        self.parent = parent
        if not function_factory:
            function_factory = parent._function_factory
        if not action:
            action = parent._action
        if not text:
            text = parent._to_text(name.title())
        self.text = text
        if not wood:
            wood = parent._wood
        if not selected_wood:
            selected_wood = parent._selected_wood
        super().__init__(parent._home, function_factory, action, wood, selected_wood)
        name_prefix = name.replace(' ', '_').lower()
        if parent._func_prefix:
            self._func_prefix = f'{parent._func_prefix}_{name_prefix}_'
        else:
            self._func_prefix = f'{name_prefix}_'
        self._name = name

    def _funcs(self):
        return self.parent._funcs()

    def _menu_sign(self, pos, facing):
        return WallSign(self.text, (
            execute().at(self._home).run(function(self.func('init')), )))
