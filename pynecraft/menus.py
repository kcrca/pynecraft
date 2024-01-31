from __future__ import annotations

from typing import Callable, Iterable, Tuple

from pynecraft.base import DOWN, Facing, FacingDef, Position, ROTATION_270, UP, as_facing, r
from pynecraft.commands import BlockDef, Selector, e, execute, fill, function
from pynecraft.function import Function
from pynecraft.simpler import WallSign


class Menu:
    """
    This class gives you a way to build menus. Each menu is a set of signs which perform some user-defined
    action, including possibly bringing up a submenu. Various options allow some control of the presentation.
    See __init__() for details.
    """

    def __init__(self, function_factory: Callable[[str], Function],
                 action_factory: Callable[[str], str], /, wood: BlockDef = 'oak', selected_wood: BlockDef = 'birch',
                 dir: FacingDef = DOWN, close_menus=False, top_row_blank=True):
        """
        Create a Menu object that can provide menus. This class defines the menus contents. The commands to place it
        in the world are returned by the place() method, which allows you to put the same menu in different place in
        the world.

        A placed menu starts with a home target, such as ``e().tag('foo_menu').limit(1)``. All commands are executed
        this place, and the menu is positioned relative to it.

        A menu can contain two kinds of buttons (signs, but in a UI sense they are "buttons"), either simple
        actions, or a submenu. When a non-menu button is selected, it runs a user-generated action, and changes
        from using the default wood type to the "selected" wood type. Selecting a different button deselects this
        sign. The action is defined via the action_factory callback you provide, which can return only a singe
        string command.

        A submenu button brings up the submenu below it (or optionally above). The buttons in this menu behave
        the same as at the top level. You can set it to pull down the submenu when an item is selected if you prefer.

        To do its work, the menu needs to define some functions, so you must provide a factory that will do that. The
        factory is given a function name, and returns a ``Function`` object for it, using whatever path it likes.
        The first function created is the 'init' function for the top-level menu. To instantiate the menu in
        your world, you invoke this function at the menu's home target, such as

            ```
            execute at @e[tag=foo_home,limit=1] run function mypack:foo_menu_init
            ```

        The menu owns the entire space starting at the original position provided to place() to the
        outer boundaries of all the submenus. For example, the init function fills all that space with
        air and puts the op level menu in it. Don't put anything else in this area.

        When the menu has been defined, you use place() to put it in the world. You provide the home entity,
        the starting position, and the direction the signs will face. This generates all the needed functions.
        The same menu can be placed in many places in the same world. Each location needs its own home.
        The factory function can produce unique function names for each placement or not.

        :param function_factory: Returns a function given a name.
        :param action_factory: Returns an action given the text on the button.
        :param wood: Wood used for the buttons (default: 'oak').
        :param selected_wood: Wood used for currently selected buttons (default: 'birch').
        :param dir: Direction the menu grows, either UP or DOWN (default: DOWN).
        :param close_menus: True if submenus should be closed when a selection is made (default: False)
        :param top_row_blank: True if the button's top row should be left blank if there are three or fewer rows of text
               (default: True).
        """
        self.function_factory = function_factory
        self.action_factory = action_factory
        self.wood = wood
        self.selected_wood = selected_wood
        dir = as_facing(dir)
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
        """Returns a function from the given base name, using the factory if it does not yet exist."""
        name = self._func_prefix + name
        try:
            return self.top.__functions[name]
        except KeyError:
            func = self.top.__functions[name] = self.function_factory(name)
            return func

    def add(self, to_add: str | Submenu | Iterable[str | Submenu]):
        """
        Adds a button. For a string, it is split into lines with ``'|'``. The action factory is invoked with the
        original text (during placement).
        """
        if isinstance(to_add, (str, Submenu)):
            self._entries.append(to_add)
        else:
            for item in to_add:
                self.add(item)
        return self

    def place(self, home: str | Selector, pos: Position, facing: FacingDef) -> None:
        """
        Place an instance of the menu using the given home. All the functions are executed at this home,
        and the position is relative, it is relative to the home.

        :param home: The home.
        :param pos: The starting position.
        :param facing: Direction the signs face.
        :return:
        """
        _Placement(self, home, pos, as_facing(facing), self.dir).place()

    def end(self, pos: Position, facing: FacingDef) -> Position:
        facing = as_facing(facing)
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
class _Placement:
    def __init__(self, menu: Menu, home, pos: Position, facing: Facing, dir: Facing):
        if isinstance(home, str):
            home = e().tag(home).limit(1)
        if not home.is_single():
            raise ValueError(f'{home}: Selecting multiple homes not allowed')
        self.home = home
        self.run_at = execute().at(home).run
        self.menu = menu
        self.pos = pos
        self.facing = facing
        self.placing = facing.turn(ROTATION_270)
        self.dir = as_facing(dir)

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
            entry.place(self.home, submenu_pos, self.facing)
            sign = entry._menu_sign(self.facing, self.run_at)
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
        commands = tuple(self.run_at(str(function(self.menu.func('init'))), action)) + (after,)
        return commands


class Submenu(Menu):
    """
    A submenu object. By default, most values are inherited from the parent menu provided here.
    """

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
        super().__init__(function_factory, action_factory, wood, selected_wood)
        name_prefix = name.replace(' ', '_').lower()
        if parent._func_prefix:
            self._func_prefix = f'{parent._func_prefix}_{name_prefix}_'
        else:
            self._func_prefix = f'{name_prefix}_'
        self._name = name

    def _menu_sign(self, facing, run_at):
        sel_sign = WallSign(self.text, (run_at(function(self.parent.func('init'))),), wood=self.selected_wood)
        commands = run_at(
            function(self.parent.func('init')),
            function(self.func('init'))) + (
                       sel_sign.place(r(0, 0, 0), facing, clear=False),)
        return WallSign(self.text, commands, self.wood)

    def _close_menu_command(self):
        return function(self.parent.func('init')) if self._top.close_menus else None
