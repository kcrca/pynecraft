from __future__ import annotations

import tempfile
import unittest

from pynecraft.function import *


def loop_func(step):
    return f'{step.loop.score.target}[{step.i}] = {str(step.elem)}'


class TestFunctions(unittest.TestCase):

    def __init__(self, methodName: str = ...):
        super().__init__(methodName)
        self.tmp_path: Path = Path('/xyzzy')  # Gets overridden in setUp, but this makes the checker happier

    def setUp(self) -> None:
        self.tmp_path = Path(tempfile.mkdtemp())

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp_path)

    def test_lines(self):
        self.assertEqual([], (list(lines())))
        self.assertEqual(['a'], (list(lines('a'))))
        self.assertEqual(['  a'], (list(lines('  a'))))
        self.assertEqual(['a'], (list(lines('a\n'))))
        self.assertEqual(['  a'], (list(lines('  a\n'))))
        self.assertEqual(['a', 'b'], (list(lines('a\nb'))))
        self.assertEqual(['  a', '  b'], (list(lines('  a\n  b'))))
        self.assertEqual(['a'], (list(lines((), 'a'))))
        self.assertEqual(['a', 'b', 'c'], (list(lines(('a', 'b'), 'c'))))
        self.assertEqual(['a', 'b', 'c'], (list(lines(([['a', 'b']]), 'c'))))

    def test_loop(self):
        try:
            # Reduces the length of matching strings
            Loop.test_controls().set_prefix_override(lambda i: f'{i}:')
            Loop.test_controls().set_setup_override(lambda: 'setup')

            score = Score('foo', 'obj')

            self.check_loop(Loop(score), [], [], [], [], looped=False)
            self.check_loop(Loop(score).add('before'), [], ['before'], [], [], looped=False)
            self.check_loop(Loop(score).loop(loop_func, ()), ['setup'], [], [], [])
            self.check_loop(Loop(score).loop(loop_func, (1,)), ['setup'], [], ['0: foo[0] = 1'], [])
            self.check_loop(Loop(score).loop(loop_func, (1,)), ['setup'], [], ['0: foo[0] = 1'], [])
            self.check_loop(Loop(score).loop(loop_func, range(1, 4)), ['setup'], [],
                            ['0: foo[0] = 1', '1: foo[1] = 2', '2: foo[2] = 3'], [])
            self.check_loop(Loop(score).loop(loop_func, (1,)), ['setup'], [], ['0: foo[0] = 1'], [])
            self.check_loop(Loop(score).add('before', 'and then').loop(loop_func, (1,)), ['setup'],
                            ['before', 'and then'],
                            ['0: foo[0] = 1'], [])
            self.check_loop(Loop(score).loop(loop_func, (1,)).add('and then', 'after'), ['setup'], [],
                            ['0: foo[0] = 1'],
                            ['and then', 'after'])
            self.check_loop(Loop(score).add('before', 'and then').loop(loop_func, (1,)).add('and then', 'after'),
                            ['setup'],
                            ['before', 'and then'], ['0: foo[0] = 1'], ['and then', 'after'])
            self.check_loop(Loop(score).loop(loop_func, (), bounce=True), ['setup'], [], [], [])
            self.check_loop(Loop(score).loop(loop_func, (1,), bounce=True), ['setup'], [], ['0: foo[0] = 1'], [])
            self.check_loop(Loop(score).loop(loop_func, range(1, 5), bounce=True), ['setup'], [],
                            ['0: foo[0] = 1', '1: foo[1] = 2', '2: foo[2] = 3', '3: foo[3] = 4', '4: foo[4] = 3',
                             '5: foo[5] = 2'], [])
            self.check_loop(Loop(score).add('before').loop(loop_func, range(1, 5), bounce=True).add('after'), ['setup'],
                            ['before'],
                            ['0: foo[0] = 1', '1: foo[1] = 2', '2: foo[2] = 3', '3: foo[3] = 4', '4: foo[4] = 3',
                             '5: foo[5] = 2'], ['after'])

            self.check_loop(Loop(score).loop(loop_func, ()).loop(loop_func, range(1, 3), replace=True), ['setup'], [],
                            ['0: foo[0] = 1', '1: foo[1] = 2'], [])

            with self.assertRaises(AssertionError):
                Loop(score).loop(loop_func, ()).loop(loop_func, range(1, 3))

        finally:
            Loop.test_controls().set_prefix_override(None)
            Loop.test_controls().set_setup_override(None)

    def check_loop(self, loop, setup, before, body, after, looped=True):
        self.assertEqual(looped, loop.looped)
        # Do this in one compare so we can see easily if a line is moved from one group to another.
        self.assertEqual((tuple(setup), before, tuple(body), after), (loop.setup, loop.before, loop.body, loop.after))
        self.assertEqual(setup + before + body + after, loop.commands())

    def test_loop_cur(self):
        loop = Loop(('foo', 'obj')).loop(loop_func, range(1, 4))
        cur = lines(loop.cur())
        self.assertGreaterEqual(cur[0].find('_to_incr'), 0)
        self.assertTrue(cur[1].index(loop.name))
        self.assertGreaterEqual(cur[2].index('_to_incr'), 0)

    def library_setup(self):
        save_dir = self.tmp_path / 'saves/NewWorld'
        save_dir.mkdir(parents=True, exist_ok=True)
        self.assertTrue(os.path.exists(save_dir))
        return save_dir

    def test_as_function(self):
        self.assertEqual('foo', as_function_name('foo'))
        with self.assertRaises(ValueError):
            as_function_name('++')

    def test_function(self):
        pack = DataPack('pack')
        self.assertEqual(('say hi',), tuple(Function('foo').add(say('hi')).commands()))
        self.assertEqual('foo', Function('foo').full_name)
        with self.assertRaises(ValueError):
            function('++')

    def test_function_save(self):
        os.chdir(self.tmp_path)
        self.check_save(None, 'b1', 'b1.mcfunction')
        self.check_save('.', 'b2', 'b2.mcfunction')
        self.check_save('foo', 'bar', 'foo.mcfunction')
        self.check_save('dir/foo', 'bar', 'dir/foo.mcfunction')
        self.check_save(None, 'dir/bar', 'dir/bar.mcfunction')
        dir = Path('just_dir')
        dir.mkdir()
        self.check_save(dir, 'flip', dir / 'flip.mcfunction')

    def test_loop_iteration_save(self):
        orig = Loop.iterate_at
        try:
            Loop.iterate_at = 2

            def loop_func(step):
                return (
                    say(f'Step {step.i}'),
                    say(f'Color: {step.elem}'),
                )

            os.chdir(self.tmp_path)
            loop = Loop(('foo', 'obj')).add('before').loop(loop_func, COLORS).add('after')
            loop.save(self.tmp_path)
            foo = (self.tmp_path / 'foo.mcfunction').read_text().rstrip().split('\n')
            self.assertEqual(len(COLORS),
                             len([x for x in filter(lambda x: x.find('if score foo obj matches') > 0, foo)]))
            for i, c in enumerate(COLORS):
                iter = (self.tmp_path / f'foo__{i:02d}.mcfunction').read_text().rstrip().split('\n')
                self.assertEqual(2 + 1, len(iter))  # The +1 is for the trailing info
                self.assertGreater(iter[1].find(c), 0)

            loaded = Function.load('foo')
            self.assertEqual(loop.commands(), loaded.commands())

        finally:
            Loop.iterate_at = orig

    def test_function_load(self):
        os.chdir(self.tmp_path)
        saved = Function('foo', 'f').add('line1', 'line2')
        saved.save('foo')
        loaded = Function.load('foo')
        self.assertEqual(saved.name, loaded.name)
        self.assertEqual(saved.base_name, loaded.base_name)
        self.assertEqual(saved.commands(), loaded.commands())

    def test_loop_load(self):
        os.chdir(self.tmp_path)
        score = Score('foo', 'obj')

        try:
            # Reduces the length of matching strings
            Loop.test_controls().set_prefix_override(lambda i: f'{i}:')
            Loop.test_controls().set_setup_override(lambda: 'setup')

            saved = Loop(score, 'f')
            saved.save('foo')
            loaded = Function.load('foo')
            self.assertEqual(saved.name, loaded.name)
            self.assertEqual(saved.base_name, loaded.base_name)
            self.assertEqual(saved.commands(), loaded.commands())

            saved = Loop(score).add('before').loop(loop_func, range(0, 3)).add('after')
            saved.save('foo')
            loaded = Loop.load('foo')
            self.check_loop(loaded, ['setup'], ['before'], ['0: foo[0] = 0', '1: foo[1] = 1', '2: foo[2] = 2'],
                            ['after'])
            loaded.add('and then')
            self.check_loop(loaded, ['setup'], ['before'], ['0: foo[0] = 0', '1: foo[1] = 1', '2: foo[2] = 2'],
                            ['after', 'and then'])
            loaded.before.append('that')
            self.check_loop(loaded, ['setup'], ['before', 'that'], ['0: foo[0] = 0', '1: foo[1] = 1', '2: foo[2] = 2'],
                            ['after', 'and then'])
            loaded.after.append('finally')
            self.check_loop(loaded, ['setup'], ['before', 'that'], ['0: foo[0] = 0', '1: foo[1] = 1', '2: foo[2] = 2'],
                            ['after', 'and then', 'finally'])

        finally:
            Loop.test_controls().set_prefix_override(None)
            Loop.test_controls().set_setup_override(None)

    def test_adjuster_load(self):
        os.chdir(self.tmp_path)
        score = Score('foo', 'obj')

        saved = Loop(score, 'loop').add('before').loop(loop_func, range(0, 3)).add('after')
        saved.save('foo')
        loaded = Loop.load('foo')
        self.assertEqual(saved.adjuster, loaded.adjuster)

        saved = Loop(score, 'loop').adjust('adjuster').add('before').loop(loop_func, range(0, 3)).add('after')
        saved.save('foo')
        loaded = Loop.load('foo')
        self.assertEqual(saved.adjuster, loaded.adjuster)

        saved = Loop(score, 'loop').adjust(('adj1', 'adj2', 'adj23')).add('before').loop(loop_func, range(0, 3)).add(
            'after')
        saved.save('foo')
        loaded = Loop.load('foo')
        self.assertEqual(saved.adjuster, loaded.adjuster)

    def check_save(self, save_path: str | Path | None, func_name: str, expected: str | Path):
        expected = expected if isinstance(expected, Path) else Path(expected)
        path = Function(func_name).add('say hi').save(save_path)
        self.assertTrue(path.exists())
        self.assertEqual(expected, path)
        text = path.read_text()
        self.assertGreaterEqual(text.find('say hi'), 0)

    def test_function_set_save(self):
        os.chdir(self.tmp_path)
        fs = FunctionSet('my_set')
        f1 = Function('f1')
        fs.add(f1.add('say hi'))
        fs.add(Function('f2').add('say there'))
        expected = Path('my_set')
        self.assertFalse(expected.exists())
        fs.save(self.tmp_path)
        self.assertTrue(expected.is_dir())
        self.assertTrue((expected / 'f1.mcfunction').exists())
        self.assertTrue((expected / 'f2.mcfunction').exists())
        self.assertEqual('my_set/f1', f1.full_name)

        # Now replace the set with an overlapping set. Old stuff should vanish, and new stuff appear
        fs = FunctionSet('my_set')
        fs.add(Function('f1').add('say hi'))
        fs.add(Function('f3').add('say friend'))
        self.assertTrue(expected.exists())
        fs.save(self.tmp_path)
        self.assertTrue(expected.is_dir())
        self.assertTrue((expected / 'f1.mcfunction').exists())
        self.assertTrue(not (expected / 'f2.mcfunction').exists())
        self.assertTrue((expected / 'f3.mcfunction').exists())

    def test_function_subset_save(self):
        os.chdir(self.tmp_path)
        top = FunctionSet('top')
        fs = FunctionSet('sub', top)
        fs.add(Function('f1').add('say hi'))
        fs.add(Function('f2').add('say there'))
        expected = Path('top') / 'sub'
        self.assertFalse(expected.exists())
        fs.save(self.tmp_path)
        self.assertTrue(expected.is_dir())
        self.assertTrue((expected / 'f1.mcfunction').exists())
        self.assertTrue((expected / 'f2.mcfunction').exists())

    def test_function_heirarchy(self):
        """
        pack -> [internal set] -----> func
                                \---> sub_set -----> sub_func
        :return:
        """
        pack = DataPack('packer')
        set = pack.function_set
        func = Function('func')
        sub_set = FunctionSet('dir')
        sub_func = Function('sub_func')

        self.assertIs(set.pack, pack)
        self.assertIsNone(func.pack)
        self.assertIsNone(sub_set.pack)
        self.assertIsNone(sub_func.pack)

        self.assertIsNone(set.parent)
        self.assertIsNone(func.parent)
        self.assertIsNone(sub_set.parent)
        self.assertIsNone(sub_func.parent)

        set.add_child(sub_set)
        set.add(func)
        sub_set.add(sub_func)

        self.assertIs(pack, set.pack)
        self.assertIs(pack, func.pack)
        self.assertIs(pack, sub_set.pack)
        self.assertIs(pack, sub_func.pack)

        self.assertIsNone(set.parent)
        self.assertIs(set, func.parent)
        self.assertIs(set, sub_set.parent)
        self.assertIs(sub_set, sub_func.parent)

        self.assertEqual('packer:', set.full_name)
        self.assertEqual('packer:func', func.full_name)
        self.assertEqual('packer:dir', sub_set.full_name)
        self.assertEqual('packer:dir/sub_func', sub_func.full_name)
        self.assertEqual('sub_func', sub_func.name)

    def test_function_datapack_save_and_load(self):
        pack = DataPack('packer')
        top = pack.function_set
        fs = FunctionSet('sub', top)
        fs.add(Function('f1').add('say packer'))
        fs.add(Function('f2').add('say there'))
        (self.tmp_path / 'datapacks').mkdir()
        expected = self.tmp_path / 'datapacks' / 'packer' / 'data' / 'packer' / 'functions' / 'sub'
        self.assertFalse(expected.exists())
        pack.save(self.tmp_path)
        self.assertTrue(expected.is_dir())
        self.assertTrue((expected / 'f1.mcfunction').exists())
        self.assertTrue((expected / 'f2.mcfunction').exists())
        with open(expected / 'f1.mcfunction') as fp:
            self.assertIn('packer', fp.read())

        blocks = pack.tags(BLOCKS)
        blocks['air'] = {'values': ['air', 'cave_air']}
        blocks['stoneish'] = ['stone', 'slate']
        pack.save(self.tmp_path)
        tags_dir = self.tmp_path / 'datapacks' / 'packer' / 'data' / 'packer' / 'tags' / 'blocks'
        self.assertTrue(tags_dir.exists())
        with open(tags_dir / 'air.json') as fp:
            written_air= json.load(fp)
        self.assertEqual({'values': ['air', 'cave_air']}, written_air)
        with open(tags_dir / 'stoneish.json') as fp:
            written_air= json.load(fp)
        self.assertEqual({'values': ['stone', 'slate']}, written_air, 'List not expanded to dict')

        pack1 = pack
        pack2 = DataPack.load(self.tmp_path, 'packer')
        self.assertEqual(pack1.name, pack2.name)
        self.assertEqual(pack1.mcmeta, pack2.mcmeta)
        self.assertEqual(tuple(x.name for x in pack1.function_set.children),
                         tuple(x.name for x in pack2.function_set.children))
        sub1 = pack1.function_set.child('sub')
        sub2 = pack2.function_set.child('sub')
        self.assertEqual(sorted(sub1.functions.keys()), sorted(sub2.functions.keys()))
        for func_name in sub2.functions:
            f1 = sub1.functions[func_name]
            f2 = sub2.functions[func_name]
            self.assertEqual(f2.name, f1.name)
            self.assertEqual(f2.commands()[:-1], f1.commands()[:-1])

    def test_datapack_filter(self):
        pack = DataPack('packer')
        pack.add_filter('f1', r'.*')
        self.assertEqual([{'namespace': 'f1', 'path': r'.*'}], pack.filter)
