"""Functionality related to functions."""

from __future__ import annotations

import math
import os
import shutil
from re import Pattern
from typing import Any, MutableMapping

from .base import _JsonEncoder, _in_group, _to_list, _to_tuple
from .commands import *

BLOCKS = 'blocks'
FLUIDS = 'fluids'
ITEMS = 'items'
ENTITIES = 'entity_types'
EVENTS = 'game_events'
TAG_SETS = [BLOCKS, FLUIDS, ITEMS, ENTITIES, EVENTS]

ADVENTURE = 'adventure'
END = 'end'
HUSBANDRY = 'husbandry'
NETHER = 'nether'
RECIPES = 'recipes'
STORY = 'story'
ADVANCEMENT_SETS = [ADVENTURE, END, HUSBANDRY, NETHER, RECIPES, STORY]

NOISE_SETTINGS = 'noise_settings'
BIOME = 'biome'
CONFIGURED_CARVER = 'configured_carver'
CONFIGURED_SURFACE_BUILDER = 'configured_surface_builder'
CONFIGURED_FEATURE = 'configured_feature'
CONFIGURED_STRUCTURE_FEATURE = 'configured_structure_feature'
STRUCTURE_SET = 'structure_set'
TEMPLATE_POOL = 'template_pool'
PROCESSOR_LIST = 'processor_list'
WORLDGEN_SETS = [NOISE_SETTINGS, BIOME, CONFIGURED_CARVER, CONFIGURED_SURFACE_BUILDER, CONFIGURED_FEATURE,
                 CONFIGURED_STRUCTURE_FEATURE, STRUCTURE_SET, TEMPLATE_POOL, PROCESSOR_LIST]


def text_lines(*orig: any) -> Iterable[str]:
    """Converts a number of commands and lines into a sequence of single lines, each terminated by newlines."""
    result = []
    for cmd in lines(orig):
        text = str(cmd)
        if len(text) > 0 or not text.endswith('\n'):
            text += '\n'
        result.append(text)
    return result


def as_function_name(name: str):
    """
    Checks if the name is a valid function name.

    :param name: The (probable) function name.
    :return: the input value.
    """
    m = re.fullmatch(r'(\w+:)?(\w+/)?(\w+)', name)
    if not m:
        raise ValueError(f'{name}: Invalid function name')
    return name


def _write_json(values: Mapping, path: Path):
    with open(path, 'w') as fp:
        json.dump(values, fp, cls=_JsonEncoder, indent=4, ensure_ascii=False)
        fp.write('\n')


class Function:
    """A class that represents a function."""
    SUFFIX = '.mcfunction'

    _LOAD_INFO = '# __internal_load: '

    def __init__(self, name: str, base_name: str = None):
        self.name = as_function_name(name)
        self.base_name = base_name if base_name else name
        self._add_to = []
        self.parent = None

    @property
    def full_name(self) -> str:
        """The full name of the function, including datapack name and path."""
        if self.parent:
            parent_name = self.parent.full_name
            if not parent_name.endswith(':'):
                parent_name += '/'
            return parent_name + self.name
        return self.name

    @property
    def pack(self):
        """The pack this function is in."""
        ancestor = self.parent
        while ancestor is not None and ancestor.pack is None:
            ancestor = ancestor.parent
        if ancestor and ancestor.pack:
            return ancestor.pack
        return None

    def __str__(self):
        return self.name + ':' + str('\n'.join(self.commands()) + '\n')

    @classmethod
    def load(cls, path: Path | str) -> Function:
        if isinstance(path, str):
            path = Path(path)
        if path.suffix != Function.SUFFIX:
            if path.suffix:
                raise ValueError(f'{path}: Invalid function suffix')
            path = path.with_suffix(Function.SUFFIX)
        with open(path) as fp:
            lines = fp.readlines()
            if len(lines) == 0 or not lines[-1].startswith(Function._LOAD_INFO):
                return Function._load(lines, path, {})
            spec = lines.pop()
            load_info = json.loads(spec[len(Function._LOAD_INFO):])
            if load_info['type'] == 'Function':
                return Function._load(lines, path, load_info)
            elif load_info['type'] == 'Loop':
                # noinspection PyProtectedMember
                return Loop._load(lines, path, load_info)
            else:
                raise SyntaxError(f'{load_info["type"]}: Invalid LOAD_INFO type')

    @classmethod
    def _load(cls, lines, path, load_info):
        func = Function(load_info.get('name', path.stem), load_info.get('base_name', None))
        func.add(lines)
        return func

    def _load_info(self) -> dict:
        return {'type': self.__class__.__name__, 'name': self.name, 'base_name': self.base_name}

    def save(self, path: Path | str = None) -> Path:
        """Saves the function to a file.

        If the path is not given, it is derived from this function's full path name, using the Minecraft file layout.
        If the path is a directory, the function is written into a file with the name of the function followed by
        ``.mcfunction``. If the path is to a file, it must end in ``.mcfunction`` or have no suffix, in which case
        ``.mcfunction`` will be added.
        """
        path = self._path_for(path)
        path.parent.mkdir(exist_ok=True, parents=True)
        with open(path, 'w') as out:
            out.writelines(text_lines(self.commands()))
            out.write(Function._LOAD_INFO)
            out.write(json.dumps(self._load_info()))
            out.write('\n')
        return path

    def _path_for(self, path):
        if path is None:
            path = Path(self.name.split(':')[-1])
        path = path if isinstance(path, Path) else Path(path)
        if path.is_dir():
            path = path / self.name
        if path.suffix:
            if path.suffix != Function.SUFFIX:
                raise ValueError(f'{path.suffix}: Suffix must be absent or "{Function.SUFFIX}"')
        else:
            path = path.with_suffix(Function.SUFFIX)
        return path

    def add(self: T, *cmds: [Command | str]) -> T:
        """Adds commands to the function.

        You can provide a list of strings or Command objects, or any un-flat iterables of them. They will be flattened
        into a set of strings for the function's commands.
        """
        cmds = lines(cmds)
        self._add_to.extend(cmds)
        return self

    def commands(self) -> list[str]:
        """Returns the commands in the function."""
        return self._add_to


class Loop(Function):
    """
    A loop function. This does the following:

    * Creates a score that is incremented each time the function is called.
    * Executes a series of commands for each iteration of the loop, only running those for the specific iteration value.
    * Generates commands for a "cur" function that will execute the code without iteration, which is useful when the
      commands are conditional on something else that may have changed.

    The loop body is provided with the loop() function. It is given a function that returns the commands for a given
    iteration of the loop, and then makes those commands run only when the score has that iteration's value. The
    commands can be as similar or dissimilar for each iteration as your loop function makes it. The other parameter
    to loop() is the list of things that are the values for each step. This could be a simple range() command,
    or a list of names, or whatever.

    As an example, you could have the following:

    ```
    Loop(('foo', 'funcs')).loop(lambda step: say(f'{step.i}: {step.elem}, ('Red', 'Green', 'Blue'))
    ```

    The lambda will be invoked three times. The ``step`` argument defines the data for the specific iteration; ``i``
    is the iteration number, and ``elem`` is the value for from the list for that iteration. This will produce a
    function that looks something like this:

    ```
    # ...increment Score('foo', 'funcs') for the loop...
    execute if score foo funcs matches 0 run say 0: Red
    execute if score foo funcs matches 1 run say 1: Green
    execute if score foo funcs matches 2 run say 2: Blue
    ```

    You can have a function that is much more complicated than this lambda, one that might (for example) use
    ``step.i`` to craft each loop iteration. It's up to you.

    The loop has four parts: ``setup`` which handles the loop increments; ``before`` which is run before the loop body;
    ``body`` which is the loop body; and ``after`` which is run after the rest. These parts are available as
    fields, though ``setup`` and ``loop`` are read-only, and created  automatically when you invoke loop().
    You can call loop() at most once unless you
    force it with the 'replace' parameter.

    Commands that are added using add() will be executed before or after the loop every time the function is invoked,
    depending on whether you call add() before or after loop().
    """

    iterate_at = 10
    """The threshold for breaking the loop out into iterations. A negative value disables this feature. 
    
    It is easy to see that there is one comparison per line of the iterations. When iterations have a lot of lines, 
    this results in long scripts with lots of tests. This value says that when any iteration is over this number of 
    lines, each iteration will be broken out into a separate function, which will be invoked with one test. So 
    instead of (say) 12 iterations of 10 lines each giving one function with 120 tests, there will be 12 tests, 
    each of which invokes a separate 10 line function. This give more functions, but fewer tests. 
    
    Benchmarking is hard with Minecraft on this point. This is our (rather random) guess at the tradeoff for this value.
    """

    @dataclasses.dataclass
    class Step:
        """Data about a specific step in the iteration."""
        i: int
        stage: int
        count: int
        elem: any
        last: any
        loop: Loop

    class TestControls:
        """Controls that are useful to simplify behavior for testing Loop. You should not otherwise use this code."""

        @staticmethod
        def set_prefix_override(func):
            Loop._prefix_override = func

        @staticmethod
        def set_setup_override(lines: tuple[str]):
            Loop._setup_override = lines

    _prefix_override = None
    _setup_override = None

    @classmethod
    def test_controls(cls):
        return Loop.TestControls()

    def __init__(self, score: ScoreName, name=None, base_name=None):
        """
        Creates a Loop function that uses the specified score for its iteration counter.

        :param score: The score to use for the iteration number.
        :param name: The loop name, if not give, it will be the 'target' part of the score.
        :param base_name: The base name for the function. It can be useful to name the function 'foo_main' to run the
        function on the "main" clock, for example. If so, the base name would typically be 'foo'.
        """
        score = as_score(score)
        if not name:
            if isinstance(score.target, (str, User)):
                name = str(score.target)
            else:
                raise ValueError(f'{score.target}: Not a valid name, and no name specified')
        super().__init__(name, base_name)
        self.score = score
        self.looped = False
        self.to_incr = Score('_to_incr', score.objective)
        self.max_score = Score(self.score.target, f'{self.score.objective}_max')
        self.setup = ()
        self.adjuster = ()
        self.before = []
        self.body = ()
        self.after = []
        self._iterations = []
        self._add_to = self.before

    @classmethod
    def _load(cls, lines, path, load_info):
        loop = Loop(load_info['score'], load_info.get('name', None), load_info.get('base_name', None))
        loop.looped = load_info['looped']

        lines = [x.rstrip() for x in lines]
        loop.setup = tuple(cls._pop_lines(lines, load_info['setup_len']))
        adjuster_len = load_info['adjuster_len']
        if not adjuster_len:
            loop.adjuster = ()
        else:
            adjuster_pos = -1 - adjuster_len
            loop.adjuster = loop.setup[adjuster_pos:-1]
            loop.setup = loop.setup[0:adjuster_pos] + loop.setup[-1:-1]
        loop.before = cls._pop_lines(lines, load_info['before_len'])
        loop.body = tuple(cls._pop_lines(lines, load_info['body_len']))
        loop.after = lines
        loop._iterations = load_info['iterations']

        if load_info.get('as_iterations', True) and loop.body:
            new_body = []
            for i, it in enumerate(loop._iterations):
                iter_suffix = loop._iter_suffix(i)
                prefix = str(loop._prefix_for(i)) + ' '
                name = loop.name + iter_suffix
                func = Function.load(path.parent / name)
                lines = func.commands()
                assert len(lines) == it
                for line in lines:
                    new_body.append(prefix + line)
            loop.body = tuple(new_body)

        loop._add_to = loop.before if not loop.looped else loop.after
        return loop

    @classmethod
    def _pop_lines(cls, lines, pos):
        return [lines.pop(0) for _ in range(pos)]

    def _load_info(self):
        info = super()._load_info()
        info.update({
            'looped': self.looped,
            'score': (str(self.score.target), self.score.objective),
            'before_len': len(self.before),
            'adjuster_len': len(self.adjuster),
            'setup_len': len(self.setup),
            'body_len': len(self.body),
            'iterations': self._iterations,
            'as_iterations': self._as_iteration(),
        })
        return info

    def save(self, path: Path | str = None) -> Path:
        as_iteration = self._as_iteration()
        orig_body = self.body
        try:
            # Clear out old iteration files if they exist
            full_path = self._path_for(path)
            for f in full_path.parent.glob(full_path.name + '__[0-9]*' + Function.SUFFIX):
                f.unlink()

            if as_iteration:
                new_body = []
                pos = 0
                for i in range(0, len(self._iterations)):
                    iter_suffix = self._iter_suffix(i)
                    prefix = str(self._prefix_for(i)) + ' '
                    new_body.append(prefix + str(function(self.full_name + iter_suffix)))
                    iter_name = self.name + iter_suffix
                    func = Function(iter_name)
                    func.add(x[len(prefix):] for x in self.body[pos:pos + self._iterations[i]])
                    pos += self._iterations[i]
                    func.save(full_path.parent / iter_name)
                self.body = new_body
            return super().save(path)
        finally:
            if as_iteration:
                self.body = orig_body

    def _as_iteration(self):
        return len(self._iterations) > 0 and 0 <= Loop.iterate_at <= max(self._iterations)

    def _iter_suffix(self, i):
        width = int(math.log(len(self._iterations), 10)) + 1
        return f'__{i:0{width}}'

    def commands(self) -> list[str]:
        return list(self.setup) + self.before + list(self.body) + self.after

    def _setup_for(self, loop_size: int):
        if Loop._setup_override:
            return _to_tuple(Loop._setup_override())
        setup = [
            execute().unless().score(self.score).matches((0, None)).run(str(function(
                f'{self.score.target}_init'))),
            self.max_score.set(loop_size),
            execute().if_().score(self.to_incr).matches((1, None)).run(literal(self.score.add(1)))]
        setup.extend(self.adjuster)
        setup.append(self.score.operation(MOD, self.max_score))
        return tuple(setup)

    def _prefix_for(self, i):
        if Loop._prefix_override:
            return Loop._prefix_override(i)
        return execute().if_().score(self.score).matches(i).run('')

    def loop(self,
             body_func: Callable[[Step], Union[Commands, Command, str, Iterable[Union[Commands, Command, str]]]] | None,
             items: Iterable[Any],
             bounce: object = False, replace: object = False) -> Loop:
        """
        Define the loop itself.

        :param body_func: The function to call for each iteration of the loop. This returns the same kind of values
                          that add() will take.
        :param items: The items that will be iterated over. Can be a simple range or any other iterable.
        :param bounce: If True, the loop will "bounce" between the list values. A loop with range(0, 4) and bounce True
                       will go through the values (0, 1, 2, 3, 2, 1) instead of (0, 1, 2, 3).
        :param replace: If True, will replace the loops contents; otherwise you will get an AssertionError.
        :return: the Loop object.
        """
        if not replace:
            assert not self.looped, 'loop() invoked more than once'

        items = _to_list(items)
        last = items[-1] if len(items) > 0 else None
        count = len(items)
        stages = tuple(range(count))
        if bounce and count > 2:
            items = items + list(reversed(items[1:-1]))
            stages = stages + tuple(reversed(stages[1:-1]))

        self.setup = self._setup_for(len(items))
        self._add_to = []

        self._iterations = []
        if body_func:
            for i, elem in enumerate(items):
                # noinspection PyArgumentList
                once = lines(body_func(Loop.Step(i, stages[i], count, elem, last, self)))
                self._iterations.append(len(once))
                prefix = str(self._prefix_for(i)) + ' '
                for line in lines(once):
                    self.add(str(prefix) + line)

        self.body = tuple(self._add_to)
        self._add_to = self.after

        self.looped = True
        return self

    def cur(self) -> Commands:
        """Return commands for a "cur" function that will run the function without incrementing the score."""
        return lines(
            self.to_incr.set(0),
            function(self.full_name),
            self.to_incr.set(1),
        )

    def adjust(self, *adjuster: [Command | str]) -> Loop:
        """
        Execute a command or commands after the loop value is incremented but before it is constrained to the max
        value. This can be used, for example, to skip a value in the middle if it is not compatible with another
        loop's value.
        """
        self.adjuster = tuple(lines(adjuster))
        return self


LATEST_PACK_VERSION = 18


class DataPack:
    """
    A datapack. This maintains a datapack directory. If it is being stored in a world save, it knows how to find its
    location therein.
    """

    def __init__(self, name: str, format_version: int = LATEST_PACK_VERSION, /,
                 mcmeta: Mapping = None):
        self._name = name
        self.function_set = FunctionSet('functions', self)
        self._json = {}
        self._mcmeta = {'pack': {'pack_format': format_version, 'description': JsonText.text(name)}}
        self._description = None
        if mcmeta:
            self._mcmeta.update(mcmeta)

    @classmethod
    def path_for(cls, path: Path | str, name: str = None) -> tuple[Path, str]:
        path = path if isinstance(path, Path) else Path(path)
        if not name:
            name = path.name
        else:
            datapack_path = path / 'datapacks'
            if datapack_path.exists():
                path = datapack_path / name
                path.mkdir(exist_ok=True)
            elif path.name != name:
                path /= name
        return path, name

    @classmethod
    def load(cls, path: Path | str, name: str = None) -> DataPack:
        """Loads a datapack from the files in the path.

        If not specified, the name of the pack will be the final path component."""
        path, name = cls.path_for(path, name)
        if not path.exists():
            raise ValueError(f'{path}: No such directory')
        pack = DataPack(name)
        pack.function_set = FunctionSet.load(path / pack._data_dir(), pack, 'functions')
        pack._json = pack._load_dict(pack._data_dir())
        with open(path / 'pack.mcmeta') as fp:
            pack._mcmeta = json.load(fp)
        return pack

    def _load_dict(self, path: Path) -> dict:
        contents = {}
        for entry in path.glob('*'):
            path = Path(entry)
            if path.is_file():
                if path.suffix != '.json':
                    print(f'Warning: {path} ignored: not a .json file')
                    continue
                with open(path) as fp:
                    contents[path.stem] = json.load(fp)
            else:
                if entry.stem == 'functions' and path.stem == self.name:
                    continue
                contents[path.stem + '/'] = self._load_dict(path)
        return contents

    def save(self, path: Path | str):
        """Saves all the files in the datapack. This first removes the path, if it exists, to clean out any old
        files. It then writes all the new files, as well as the ``pack.mcmeta`` file and a warning ``README`` file.
        """
        path, _ = self.path_for(path, self._name)
        if path.exists():
            shutil.rmtree(path)
        path.mkdir(parents=True)
        self._cleanup()
        self.function_set.save(path / self._data_dir())
        self._save_dict(self._json, path / self._data_dir())
        _write_json(self._mcmeta, path / 'pack.mcmeta')
        with open(path / 'README', 'w') as fp:
            fp.write("Files in this tree were auto-generated using pynecraft. Hand modifications will be lost!")

    def _cleanup(self) -> None:
        if 'tags/' in self._json:
            self._cleanup_values(self._json['tags/'])

    def _cleanup_values(self, values: MutableMapping) -> None:
        for k, v in values.items():
            if isinstance(v, MutableMapping):
                if 'values' not in v:
                    self._cleanup_values(v)
            elif isinstance(v, Iterable):
                values[k] = {'values': _to_list(v)}

    def _save_dict(self, d: dict, path: Path):
        for k, v in d.items():
            if k.endswith('/'):
                subdir = path / k[:-1]
                subdir.mkdir(exist_ok=True, parents=True)
                self._save_dict(v, subdir)
            else:
                _write_json(v, (path / k).with_suffix('.json'))

    @property
    def name(self):
        """The data pack name."""
        return self._name

    @property
    def description(self) -> JsonText | None:
        """The data pack description, stored in the ``pack.mcmeta`` file."""
        try:
            return self._mcmeta['pack']['description']
        except KeyError:
            return None

    @description.setter
    def description(self, text: JsonDef):
        if isinstance(text, str):
            text = JsonText.text(text)
        self._mcmeta['pack']['description'] = text

    @property
    def filter(self) -> list[Mapping[str, str]] | None:
        """The filter listing, stored in the ``pack.mcmeta`` file."""
        try:
            return self._mcmeta['pack']['filter']
        except KeyError:
            return None

    @filter.setter
    def filter(self, value: Iterable[tuple[str, str]]):
        self._mcmeta['pack']['filter'] = _to_list(value)

    @property
    def mcmeta(self) -> dict:
        """The dict for the ``pack.mcmeta`` file."""
        return self._mcmeta

    @property
    def functions(self):
        """The FunctionSet for the top-level functions in this data pack."""
        return self.function_set.functions

    def _data_dir(self):
        return Path('data') / self.name

    def add_filter(self, namespace: str = None, pattern: str | Pattern = None):
        """Adds a new filter for the pack."""
        f = {}
        if namespace is not None:
            f['namespace'] = namespace
        if pattern is not None:
            if isinstance(pattern, str):
                re.compile(pattern)
            else:
                pattern = pattern.pattern
            f['path'] = str(pattern)
        # noinspection PyTypeChecker
        self._mcmeta['pack'].setdefault('filter', []).append(f)

    def tags(self, tag_set: str) -> dict:
        """
        Returns defined tags. You can add to this dict to add tags to the datapack. As a convenience, if a tag's
        value is a list (or tuple), it is replaced with {'values': *tag_value*}, so you don't have to remember that.
        So saying ``tags(BLOCKS)['hard'] = ['stone', 'slate']`` is the same as saying  ``tags(BLOCKS)['hard'] = {
        'values': ['stone', 'slate']}``. And it's easier.
        """
        return self._get_json('tags', TAG_SETS, tag_set)

    def advancements(self, advancement_set: str) -> dict[str, dict]:
        """Returns defined advancements. You can add to this dict to add advancements to the datapack. Keys that end in
        '/' define directories. Keys underneath them (which do not end in '/') define files, whose contents are the JSON
        defined by the dict such keys map to."""
        return self._get_json('advancements', ADVANCEMENT_SETS, advancement_set)

    def dimensions(self, dimension: str) -> dict[str, dict]:
        """Returns the defined dimensions. You can add to this dict to add advancements to the datapack. """
        return self._get_json('dimension', None, dimension)

    def dimension_types(self, dimension_type: str) -> dict[str, dict]:
        """Returns defined dimension_types. You can add to this dict to add advancements to the datapack. """
        return self._get_json('dimension_type', None, dimension_type)

    def loot_tables(self, loot_table: str) -> dict[str, dict]:
        """Returns defined loot_tables. You can add to this dict to add advancements to the datapack. """
        return self._get_json('loot_tables', None, loot_table)

    def predicates(self) -> dict[str, dict]:
        """Returns defined predicates. You can add to this dict to add advancements to the datapack. """
        return self.json_directory('predicates')

    def recipes(self) -> dict[str, dict]:
        """Returns defined recipes. You can add to this dict to add advancements to the datapack. """
        return self.json_directory('recipes')

    def structures(self, structure: str) -> dict[str, dict]:
        """Returns defined structures. You can add to this dict to add advancements to the datapack. """
        return self._get_json('structures', None, structure)

    def worldgen(self, worldgen_set: str) -> dict[str, dict]:
        """Returns defined worldgen settings. You can add to this dict to add worldgen settings to the datapack. """
        return self._get_json('worldgen', WORLDGEN_SETS, worldgen_set)

    def json_directory(self, name: str) -> dict[str, dict]:
        """Returns an arbitrary directory at the top level of the data pack's JSON directory."""
        return self._get_json(name)

    def _get_json(self, directory, valid=None, which=None) -> dict:
        if valid:
            _in_group(valid, which)
        if not directory.endswith('/'):
            directory += '/'
        if not which.endswith('/'):
            which += '/'
        if directory not in self._json:
            self._json[directory] = {}
        if valid is None:
            return self._json[directory]
        return self._json[directory].setdefault(which, {})


class FunctionSet:
    """A set of functions. This corresponds to the top-level ``functions`` field in the datapack, and any of
    its child subdirectories. It enforces this maximum-two-level structure.

    The defined functions are available via the ``functions`` property. Typically, you will add functions via
    the add() method, which protects against duplicate functions. You can add, replace, or remove functions
    using the returned dict as well.
    """

    class _Functions(UserDict):
        """Dict that sets the added functions' parent."""

        def __init__(self, functions: FunctionSet):
            super().__init__()
            self.functions = functions

        def __setitem__(self, key: str, value: Function):
            ret = super().__setitem__(key, value)
            if not isinstance(value, Function):
                raise ValueError(f'{value.name}: Not a Function')
            value.parent = self.functions
            return ret

    def __init__(self, name: str, pack_or_parent: DataPack | FunctionSet = None):
        """Creates a function set.

        :param name: The set name. For the top level directory this is notional. For subdirectories, it is the
        directory name. The parent can be either a DataPack (for the top-level function directory) or that pack's
        FunctionSet.
        :param pack_or_parent: The parent of this set.
        """
        self.name = as_name(name)
        if isinstance(pack_or_parent, FunctionSet):
            # self.pack = pack_or_parent.pack
            self.parent = pack_or_parent
            self.parent.add_child(self)
            if self.parent.parent:
                raise ValueError(f'Only two levels of groups (sigh): {pack_or_parent.name} has a parent')
        elif isinstance(pack_or_parent, DataPack):
            self._pack = pack_or_parent
            self.parent = None
        else:
            self._pack = None
            self.parent = None

        self._functions = FunctionSet._Functions(self)
        self._kids: list[FunctionSet] = []

    @property
    def pack(self):
        if self._pack:
            return self._pack
        elif self.parent:
            return self.parent.pack
        return None

    @pack.setter
    def pack(self, pack: DataPack | None):
        self._pack = pack

    @property
    def full_name(self):
        if self.parent:
            parent_name = self.parent.full_name
            if not parent_name.endswith(':'):
                parent_name += '/'
            return f'{parent_name}{self.name}'
        if self.pack:
            return f'{self.pack.name}:'
        return self.name

    @classmethod
    def load(cls, path: Path | str, pack_or_parent: DataPack | FunctionSet = None, name=None) -> FunctionSet:
        """Loads the functions from the directory. Files that do not end in .mcfunction are skipped with a warning.
        If there are subdirectories, they will be loaded as well."""
        if not isinstance(path, Path):
            path = Path(path)
        if name is None:
            name = path.name
        elif path.name != name:
            path /= name
        fs = FunctionSet(name, pack_or_parent)
        if not path.exists():
            return fs
        for root, dirs, files in os.walk(path):
            for f in files:
                if not f.endswith(Function.SUFFIX):
                    print(f'Warning: {f} ignored: suffix required: {Function.SUFFIX}')
                    continue
                func = Function.load(Path(root) / f)
                fs.add(func)
            for d in dirs:
                FunctionSet.load(path / d, fs)
            # We're doing our own recursion, so just look at the top level
            break
        return fs

    def save(self, path: Path):
        """Saves the functions to the directory."""
        full_dir = self.path(path)
        if full_dir.exists():
            shutil.rmtree(full_dir)
        full_dir.mkdir(parents=True, exist_ok=True)
        for func in self.functions.values():
            func.save(full_dir / func.name)
        for child in self._kids:
            child.save(path)

    @property
    def functions(self) -> Mapping[str, Function]:
        """The functions in this set"""
        return self._functions

    @property
    def children(self) -> tuple[FunctionSet]:
        """The child FunctionSets of this set. This is read-only"""
        return tuple(self._kids)

    def path(self, path) -> Path:
        """The path to this function set."""
        return path / self._path_for()

    def _path_for(self) -> Path:
        if self.parent:
            return Path(self.parent.name) / self.name
        return Path(self.name)

    def add(self, function: Function) -> Function:
        """Adds a function to this set."""
        if function.name in self._functions:
            raise ValueError(f'{function.name}: duplicate function in {self.name}')
        self._functions[function.name] = function
        return function

    def child(self, name: str) -> FunctionSet | None:
        """Returns the named child FunctionSet of this function set."""
        for fs in self._kids:
            if fs.name == name:
                return fs
        return None

    def add_child(self, child: FunctionSet):
        """Adds a child FunctionSet."""
        self._kids.append(child)
        child.parent = self
