from __future__ import annotations

from typing import Callable, Iterable, Tuple

from pynecraft.base import FacingDef, good_facing, Position, Facing, ROTATION_270, DOWN, r, UP
from pynecraft.commands import fill, BlockDef, function, execute, Selector, e
from pynecraft.function import Function
from pynecraft.simpler import WallSign


class Menu:

    def __init__(self, home: str | Selector, function_factory: Callable[[str], Function],
                 action_factory: Callable[[str], str], /, wood: BlockDef = 'oak', selected_wood: BlockDef = 'birch',
                 dir: FacingDef = DOWN, close_menus=False, top_row_blank=True):
        self._home = home if isinstance(home, Selector) else e().tag(home).limit(1)
        if not self._home.is_single():
            raise ValueError(f'{home}: Selecting multiple not allowed')
        self._run_at = execute().at(self._home).run
        self.function_factory = function_factory
        self.action_factory = action_factory
        self.wood = wood
        self.selected_wood = selected_wood
        dir = good_facing(dir)
        if dir not in (UP, DOWN):
            raise ValueError(f'{dir}: only UP and DOWN are allowed')
        self.dir = dir
        self.top_row_blank = top_row_blank
        self.close_menus = close_menus
        self._entries = []
        self.__functions = {}
        self._func_prefix = ''
        self.top = self

    def func(self, name):
        name = self._func_prefix + name
        try:
            return self.top.__functions[name]
        except KeyError:
            func = self.top.__functions[name] = self.function_factory(name)
            return func

    def add(self, to_add: str | Submenu | Iterable[str | Submenu]):
        if isinstance(to_add, (str, Submenu)):
            self._entries.append(to_add)
        else:
            for item in to_add:
                self.add(item)
        return self

    def place(self, pos: Position, facing: FacingDef) -> None:
        Placement(self, pos, good_facing(facing), self.dir, self._run_at).place()

    def end(self, pos: Position, facing: FacingDef) -> Position:
        facing = good_facing(facing)
        dim = self._dim()
        return (pos[0] + (dim[0] - 1) * facing.dx,
                pos[1] + (dim[1] - 1) * self.dir.dy,
                pos[2] + (dim[0] - 1) * facing.dz)

    def _dim(self) -> Tuple[int, int]:
        if not self._entries:
            return 0, 0
        w, h = (len(self._entries), 1)
        for i, e in enumerate(self._entries):
            if isinstance(e, Submenu):
                sub_dim = e._dim()
                w = max(w, i + sub_dim[0])
                h = max(h, 1 + sub_dim[1])
        return w, h

    def _to_text(self, entry: str):
        text = tuple(x.strip() for x in entry.split('|'))
        if self.top_row_blank and len(text) < 4:
            text = (None,) + text
        return text

    def _close_menu_command(self) -> str | None:
        return None


# noinspection PyProtectedMember
class Placement:
    def __init__(self, menu: Menu, pos: Position, facing: Facing, dir: Facing, run_at):
        self.menu = menu
        self.pos = pos
        self.facing = facing
        self.placing = facing.turn(ROTATION_270)
        self.dir = good_facing(dir)
        self.run_at = run_at

    def place(self):
        if not self.menu._entries:
            return
        init = self.menu.func('init')
        init.add(fill(self.pos, self.menu.end(self.pos, self.placing), 'air'))
        for i, e in enumerate(self.menu._entries):
            init.add(self.place_sign(i, e))

    def place_sign(self, offset, entry):
        if isinstance(entry, Submenu):
            submenu_pos = self.dir.move(self.placing.move(self.pos, offset), 1)
            entry.place(submenu_pos, self.facing)
            sign = entry._menu_sign(self.facing)
        else:
            text = self.menu._to_text(entry)
            sign = WallSign(text, self.commands(entry, text), wood=self.menu.wood)
        yield sign.place(self.placing.move(self.pos, offset), self.facing, clear=False)

    def commands(self, entry, text) -> Tuple[str, ...]:
        action = self.menu.action_factory(entry)
        sel_sign = WallSign(text, (
            action
        ), self.menu.selected_wood)
        close_menu = self.menu._close_menu_command()
        if close_menu:
            after = self.run_at(close_menu)
        else:
            after = sel_sign.place(r(0, 0, 0), self.facing, clear=False)
        commands = tuple(self.run_at(function(self.menu.func('init')), action)) + (after,)
        return commands


class Submenu(Menu):
    def __init__(self, parent: Menu, name: str, function_factory: Callable[[str], Function] = None,
                 action_factory: Callable[[str], str] = None, /, text: str = None, wood: BlockDef = None,
                 selected_wood: BlockDef = None):
        self.parent = parent
        if isinstance(parent, Submenu):
            self._top = parent._top
        else:
            self._top = parent
        if not function_factory:
            function_factory = parent.function_factory
        if not action_factory:
            action_factory = parent.action_factory
        if not text:
            text = parent._to_text(name.title())
        self.text = text
        if not wood:
            wood = parent.wood
        if not selected_wood:
            selected_wood = parent.selected_wood
        super().__init__(parent._home, function_factory, action_factory, wood, selected_wood)
        name_prefix = name.replace(' ', '_').lower()
        if parent._func_prefix:
            self._func_prefix = f'{parent._func_prefix}_{name_prefix}_'
        else:
            self._func_prefix = f'{name_prefix}_'
        self._name = name

    def _menu_sign(self, facing):
        sel_sign = WallSign(self.text, (self._run_at(function(self.parent.func('init'))),), wood=self.selected_wood)
        commands = self._run_at(
            function(self.parent.func('init')),
            function(self.func('init'))) + (
                       sel_sign.place(r(0, 0, 0), facing, clear=False),)
        return WallSign(self.text, commands, self.wood)

    def _close_menu_command(self):
        return function(self.parent.func('init')) if self._top.close_menus else None
