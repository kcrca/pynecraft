from __future__ import annotations

import unittest

from pynecraft.base import DARK_GREEN, GAMETIME, LT, NORTH, THE_NETHER, WEST, d, days, r, seconds, ticks
from pynecraft.commands import *
from pynecraft.commands import AdvancementCriteria, _AttributeMod, _DataMod, _ExecuteMod, _IfClause, \
    _ScoreboardCriteria, _ScoreboardObjectivesMod, _ScoreboardPlayersMod, _StoreClause
from pynecraft.enums import BiomeId
from pynecraft.function import Function


def commands(*cmds: str | Command) -> str:
    """Return a single multiline string for all the commands in the input."""
    return '\n'.join(str(x) for x in cmds)


class TestCommands(unittest.TestCase):

    def test_advancement(self):
        self.assertEqual('advancement grant @s everything', advancement(GIVE, s()).everything())
        self.assertEqual('advancement grant @s only husbandry/balanced_diet pig',
                         advancement(GIVE, s()).only(Advancement.A_BALANCED_DIET, "pig"))
        self.assertEqual('advancement grant @s from husbandry/wax_on', advancement(GIVE, s()).from_(Advancement.WAX_ON))
        self.assertEqual('advancement grant @s through husbandry/wax_on',
                         advancement(GIVE, s()).through(Advancement.WAX_ON))
        self.assertEqual('advancement grant @s until husbandry/wax_on',
                         advancement(GIVE, s()).until(Advancement.WAX_ON))

        self.assertEqual('advancement revoke @s everything', advancement(REVOKE, s()).everything())
        self.assertEqual('advancement revoke @s only husbandry/balanced_diet pig',
                         advancement(REVOKE, s()).only(Advancement.A_BALANCED_DIET,
                                                       "pig"))
        self.assertEqual('advancement revoke @s from husbandry/wax_on',
                         advancement(REVOKE, s()).from_(Advancement.WAX_ON))
        self.assertEqual('advancement revoke @s through husbandry/wax_on',
                         advancement(REVOKE, s()).through(Advancement.WAX_ON))
        self.assertEqual('advancement revoke @s until husbandry/wax_on',
                         advancement(REVOKE, s()).until(Advancement.WAX_ON))

    def test_execute(self):
        self.assertEqual('execute align xz', str(execute().align('xz')))
        with self.assertRaises(ValueError):
            execute().align('foo')

    def test_execute_summon(self):
        self.assertEqual('execute summon cow', str(execute().summon('cow')))

    def test_uuids(self):
        uuid1 = Uuid(-534823299, 1525499658, -1223897314, -535100990)
        self.assertEqual(uuid1, Uuid.from_hex('e01f3e7d-5aed-470a-b70c-cf1ee01b01c2'))
        self.assertEqual(uuid1, Uuid.from_most_least(-2297048576818329846, -5256598933532376638))
        self.assertEqual(uuid1, Uuid.from_most_least_dict(
            {'UUIDMost': -2297048576818329846, 'UUIDLeast': -5256598933532376638}))
        self.assertEqual(
            {'UUIDMost': -2297048576818329846, 'UUIDLeast': -5256598933532376638}, uuid1.most_least_dict)
        self.assertEqual((-534823299, 1525499658, -1223897314, -535100990), uuid1.ints)
        self.assertEqual('e01f3e7d-5aed-470a-b70c-cf1ee01b01c2', uuid1.hex_str)
        self.assertEqual((-2297048576818329846, -5256598933532376638), uuid1.most_least)

        uuid2 = Uuid(14688125, 15550218, 786639, 505086402)
        self.assertEqual(uuid2, Uuid.from_hex("e01f7d-ed-470a-c-cf1e1b01c2"))
        self.assertEqual("00e01f7d-00ed-470a-000c-00cf1e1b01c2", uuid2.hex_str)

        # Checking the signed-int handling explicitly
        uuid3 = Uuid(-1, -1, 1, 1)
        self.assertEqual((-1, -1, 1, 1), uuid3.ints)
        self.assertEqual((-1, 0x100000001), uuid3.most_least)
        self.assertEqual((-1, -2, 3, 4), Uuid.from_most_least(0xfffffffffffffffe, 0x300000004).ints)

    def test_execute_mod(self):
        self.assertEqual('align xz', str(_ExecuteMod().align('xz')))
        self.assertEqual('anchored eyes', str(_ExecuteMod().anchored(EYES)))
        self.assertEqual('positioned 1 ~2 ^3', str(_ExecuteMod().positioned((1, r(2), d(3)))))
        self.assertEqual('positioned as @e[type=bee]', str(_ExecuteMod().positioned_as(e().type('bee'))))
        self.assertEqual('positioned over ocean_floor', str(_ExecuteMod().positioned_over(OCEAN_FLOOR)))
        self.assertEqual('rotated 90.0 22', str(_ExecuteMod().rotated(WEST, 22)))
        self.assertEqual('rotated as @e[tag=foo]', str(_ExecuteMod().rotated_as(e().tag('foo'))))
        self.assertEqual('dimension overworld', str(_ExecuteMod().dimension('overworld')))
        self.assertEqual('on vehicle', str(_ExecuteMod().on(VEHICLE)))
        self.assertEqual('as @s[tag=robin]', str(_ExecuteMod().as_(s().tag('robin'))))
        self.assertEqual('at [1, 3, 5, 7]', str(_ExecuteMod().at(Uuid(1, 3, 5, 7))))
        self.assertEqual('facing 1 ~2 ^3', str(_ExecuteMod().facing((1, r(2), d(3)))))
        self.assertEqual('facing entity robin feet', str(_ExecuteMod().facing_entity(User('robin'), FEET)))
        self.assertEqual('in the_nether', str(_ExecuteMod().in_(THE_NETHER)))
        self.assertEqual('if block 1 ~2 ^3 stone', str(_ExecuteMod().if_().block((1, r(2), d(3)), 'stone')))
        self.assertEqual('unless block 1 ~2 ^3 stone', str(_ExecuteMod().unless().block((1, r(2), d(3)), 'stone')))
        self.assertEqual('if function foo', str(_ExecuteMod().if_().function('foo')))
        self.assertEqual('unless function foo', str(_ExecuteMod().unless().function('foo')))
        self.assertEqual('store result block 1 ~2 ^3 {} short 1.3', str(
            _ExecuteMod().store(RESULT).block((1, r(2), d(3)), '{}', SHORT,
                                              1.3)))
        self.assertEqual('run say hi', str(_ExecuteMod().run(say('hi'))))
        self.assertEqual('entity @p', str(_ExecuteMod().entity(p())))
        with self.assertRaises(ValueError):
            _ExecuteMod().align('foo')
        with self.assertRaises(ValueError):
            _ExecuteMod().anchored('foo')
        with self.assertRaises(ValueError):
            _ExecuteMod().facing_entity(User('robin'), 'foo')
        with self.assertRaises(ValueError):
            _ExecuteMod().in_('foo')
        with self.assertRaises(TypeError):
            _ExecuteMod().store().block((1, r(2), d(3)), '{}', 'foo', 1.3)

    def test_run(self):
        self.assertEqual('execute run foo', str(execute().run('foo')))
        self.assertEqual('execute run execute', str(execute().run(execute())))
        self.assertEqual('execute run time', str(execute().run(time())))
        self.assertEqual(('execute run time', 'execute run say hi'), execute().run((time(), say('hi'))))

    def test_if_clause(self):
        self.assertEqual('blocks 1 2 3 4 5 6 7 8 9 masked',
                         str(_IfClause().blocks((1, 2, 3), (4, 5, 6), (7, 8, 9), MASKED)))
        self.assertEqual('data block 1 ~2 ^3 {}', str(_IfClause().data((1, r(2), d(3)), '{}')))
        self.assertEqual('data entity @a {}', str(_IfClause().data(a(), '{}')))
        self.assertEqual('data storage stone {}', str(_IfClause().data('stone', '{}')))
        self.assertEqual('predicate foo', str(_IfClause().predicate('foo')))
        self.assertEqual('score * bar < up down', str(_IfClause().score(('*', 'bar')).is_(LT, ('up', 'down'))))
        self.assertEqual('score * bar < up down', str(_IfClause().score(('*', 'bar')).is_(LT, Score('up', 'down'))))
        self.assertEqual('score * bar matches ..10', str(_IfClause().score(('*', 'bar')).matches((None, 10))))
        self.assertEqual('score * bar matches 1..', str(_IfClause().score(('*', 'bar')).matches((1, None))))
        self.assertEqual('score * bar matches 3', str(_IfClause().score(('*', 'bar')).matches(3)))
        self.assertEqual('score * bar matches 3', str(_IfClause().score(Score('*', 'bar')).matches(3)))
        self.assertEqual('biome 1 ~2 ^3 desert', str(_IfClause().biome((1, r(2), d(3)), BiomeId.DESERT)))
        self.assertEqual('entity @e[tag=foo]', str(_IfClause().entity(e().tag('foo'))))
        self.assertEqual('loaded 1 ~2 ^3', str(_IfClause().loaded((1, r(2), d(3)))))
        with self.assertRaises(ValueError):
            _IfClause().score(('*', 'bar')).is_('foo', ('up', 'down'))
        with self.assertRaises(ValueError):
            _IfClause().blocks((1, 2, 3), (4, 5, 6), (7, 8, 9), 'foo')

    def test_store_clause(self):
        self.assertEqual('block 1 ~2 ^3 {} short 1.3', str(_StoreClause().block((1, r(2), d(3)), '{}', SHORT, 1.3)))
        self.assertEqual('bossbar stud max', str(_StoreClause().bossbar('stud', MAX)))
        self.assertEqual('entity @p {} float 3.5', str(_StoreClause().entity(p(), '{}', FLOAT, 3.5)))
        self.assertEqual('score @e foo', str(_StoreClause().score((e(), 'foo'))))
        self.assertEqual('score @e foo', str(_StoreClause().score(Score(e(), 'foo'))))
        self.assertEqual('storage foo {} double 1.9', str(_StoreClause().storage('foo', '{}', DOUBLE, 1.9)))
        with self.assertRaises(ValueError):
            _StoreClause().bossbar('stud', 'foo')
        with self.assertRaises(ValueError):
            _StoreClause().entity(p(), '{}', 'foo', 3.5)
        with self.assertRaises(ValueError):
            _StoreClause().storage('bar', '{}', 'foo', 1.9)

    def test_execute_macros(self):
        self.assertEqual('$execute if blocks $(x1) $(y1) $(z1) $(x2) $(y2) $(z2) $(x3) $(y3) $(z3) $(m)',
                         str(execute().if_().blocks(
                             (Arg('x1'), Arg('y1'), Arg('z1')),
                             (Arg('x2'), Arg('y2'), Arg('z2')),
                             (Arg('x3'), Arg('y3'), Arg('z3')),
                             Arg('m'))))
        self.assertEqual('$execute if data storage $(t) $(p)', str(execute().if_().data(storage(Arg('t')), Arg('p'))))
        self.assertEqual('$execute if function $(func)', str(execute().if_().function(Arg('func'))))
        self.assertEqual('$execute if function $(func)', str(execute().if_().function(Arg('func'))))
        self.assertEqual('$execute store result block $(x) $(y) $(z) $(path) short $(scale)',
                         str(execute().store(RESULT).block((Arg('x'), Arg('y'), Arg('z')), Arg('path'), SHORT,
                                                           Arg('scale'))))

    def test_coords(self):
        self.assertEqual('~1', str(r(1)))
        self.assertEqual('~-1.5', str(r(-1.5)))
        self.assertEqual('^1', str(d(1)))
        self.assertEqual('^-1.5', str(d(-1.5)))
        self.assertEqual('~3.3', str(r(1.1) + 2.2))
        self.assertEqual('^3.3', str(d(1.1) + 2.2))
        self.assertEqual((r(1), r(2), r(3)), r(1, 2, 3))
        self.assertEqual((d(1), d(2), d(3)), d(1, 2, 3))

    def test_block(self):
        self.assertEqual('stone', str(Block('stone')))
        self.assertEqual('m:stone', str(Block('m:stone')))

        self.assertEqual('stone[a=17]', str(Block('stone', {'a': 17})))
        self.assertEqual('stone{a: 17}', str(Block('stone', {}, {'a': 17})))
        self.assertEqual('stone{a: 17}', str(Block('stone', nbt={'a': 17})))
        self.assertEqual('stone[b=c]{a: 17}', str(Block('stone', {'b': 'c'}, {'a': 17})))

        self.assertEqual('stone[a=17]', str(Block('stone').merge_state({'a': 17})))
        self.assertEqual('stone{a: 17}', str(Block('stone').merge_state({}).merge_nbt({'a': 17})))
        self.assertEqual('stone{a: 17}', str(Block('stone').merge_nbt({'a': 17})))
        self.assertEqual('stone[b=c]{a: 17}', str(Block('stone').merge_state({'b': 'c'}).merge_nbt({'a': 17})))

        self.assertEqual('stone{a: 16, b: howdy}',
                         str(Block('stone').merge_nbt({'a': 17}).merge_nbt({'a': 16, 'b': 'howdy'})))
        self.assertEqual('stone[a=16, b=howdy]',
                         str(Block('stone').merge_state({'a': 17}).merge_state({'a': 16, 'b': 'howdy'})))
        self.assertEqual('v$(k)', str(Block('v$(k)')))
        self.assertEqual('$(k)', str(Block(Arg('k'))))
        self.assertEqual('$(k)[a=17]{b: foo}', str(Block(Arg('k'), {'a': 17}, {'b': 'foo'})))

    def test_entity(self):
        self.assertEqual('bat', str(Entity('bat')))
        self.assertEqual('m:bat', str(Entity('m:bat')))
        self.assertEqual('bat{a: 17}', str(Entity('bat', nbt={'a': 17})))
        self.assertEqual('bat{a: 17}', str(Entity('bat').merge_nbt({'a': 17})))
        self.assertEqual('bat{a: 16, b: howdy}',
                         str(Entity('bat').merge_nbt({'a': 17}).merge_nbt({'a': 16, 'b': 'howdy'})))
        self.assertEqual('minecraft:bat', Entity('bat').full_id())
        self.assertEqual('minecraft:bat', Entity('minecraft:bat').full_id())
        self.assertEqual('dp:mouse', Entity('dp:mouse').full_id())
        self.assertEqual(Nbt({}), Entity('bat', name='Fred').nbt)
        self.assertEqual(Nbt({'Tags': ['t1', 't2']}), Entity('bat', name='Fred').tag('t1').tag('t2').nbt)
        self.assertEqual(Nbt({'CustomName': 'Fred', 'CustomNameVisible': False}),
                         Entity('bat', name='Fred').custom_name(True).nbt)
        self.assertEqual(Nbt({'CustomName': 'Fred', 'CustomNameVisible': True}),
                         Entity('bat', name='Fred').custom_name(True).custom_name_visible(True).nbt)
        self.assertEqual('summon bat 1 ~2 ^3 {Facing: 2, Rotation: [180.0f, 0.0f]}',
                         Entity('bat', name='Fred').summon((1, r(2), d(3)), facing=NORTH))
        self.assertEqual('$summon $(mob) $(x) $(y) $(z)', Entity(Arg('mob')).summon((Arg('x'), Arg('y'), Arg('z'))))
        self.assertEqual('v$(k)', str(Entity('v$(k)')))
        self.assertEqual('$(k)', str(Entity(Arg('k'))))
        self.assertEqual('$(k){b: foo}', str(Entity(Arg('k'), {'b': 'foo'})))

    def test_json_text(self):
        sort_keys = Nbt.sort_keys
        try:
            Nbt.sort_keys = False
            self.assertEqual('{"text": "hi"}', str(JsonText.text('hi')))
            self.assertEqual('{"text": "hi\\n"}', str(JsonText.text('hi\n')))
            self.assertEqual((
                "[{'text': 'hi', 'bold': 'true', 'italic': 'true'}, {'text': ' there', 'bold': 'true'}, {'text': ' friend'}]"),
                str(JsonText.html_text('<b><i>hi</i> there</b> friend')))
            self.assertEqual('{"translate": "m.id", "with": ["t1", "t2"]}',
                             str(JsonText.translate('m.id', 't1', 't2')))
            self.assertEqual('{"score": {"name": "sc", "objective": "obj"}}', str(JsonText.score(Score('sc', 'obj'))))
            self.assertEqual('{"score": {"name": "sc", "objective": "obj", "value": 17}}',
                             str(JsonText.score(('sc', 'obj'), 17)))
            self.assertEqual('{"selector": "@a"}', str(JsonText.entity(a())))
            self.assertEqual('{"selector": "@a", "separator": {"color": "red", "text": "_"}}',
                             str(JsonText.entity(a(), RED, '_')))
            self.assertEqual('{"keybind": "b.id"}', str(JsonText.keybind('b.id')))
            self.assertEqual('{"nbt": "m:a/b", "entity": "@a"}', str(JsonText.nbt('m:a/b', a())))
            self.assertEqual('{"nbt": "m:a/b", "block": "1 ~2 ^3", "interpret": true, "separator": "_"}',
                             str(JsonText.nbt('m:a/b', (1, r(2), d(3)), interpret=True, separator='_')))
            self.assertEqual('{"text": "boo", "extra": []}', str(JsonText.text('boo').extra()))
            self.assertEqual('{"text": "boo", "extra": ["foo", {"text": "bar"}]}',
                             str(JsonText.text('boo').extra('foo', JsonText.text('bar'))))
            self.assertEqual('{"text": "boo", "color": "dark_green"}', str(JsonText.text('boo').color(DARK_GREEN)))
            self.assertEqual('{"text": "boo", "font": "m:a/b"}', str(JsonText.text('boo').font('m:a/b')))
            self.assertEqual('{"text": "boo", "bold": true}', str(JsonText.text('boo').bold()))
            self.assertEqual('{"text": "boo", "italic": true}', str(JsonText.text('boo').italic()))
            self.assertEqual('{"text": "boo", "underlined": true}', str(JsonText.text('boo').underlined()))
            self.assertEqual('{"text": "boo", "strikethrough": true}', str(JsonText.text('boo').strikethrough()))
            self.assertEqual('{"text": "boo", "obfuscated": true}', str(JsonText.text('boo').obfuscated()))
            self.assertEqual('{"text": "boo", "insertion": "inserted"}',
                             str(JsonText.text('boo').insertion('inserted')))

            self.assertEqual((
                '{"text": "boo", "clickEvent": {"action": "copy_to_clipboard", "value": "ya"}}'),
                str(JsonText.text('boo').click_event().copy_to_clipboard('ya')))
            self.assertEqual((
                '{"text": "boo", "clickEvent": {"action": "open_url", "value": "http: a.com"}}'),
                str(JsonText.text('boo').click_event().open_url('http: a.com')))
            self.assertEqual((
                '{"text": "boo", "clickEvent": {"action": "open_file", "value": "/a/b"}}'),
                str(JsonText.text('boo').click_event().open_file('/a/b')))
            self.assertEqual((
                '{"text": "boo", "clickEvent": {"action": "change_page", "value": "p"}}'),
                str(JsonText.text('boo').click_event().change_page('p')))
            self.assertEqual((
                '{"text": "boo", "clickEvent": {"action": "run_command", "value": "/say hi"}}'),
                str(JsonText.text('boo').click_event().run_command(say('hi'))))
            self.assertEqual((
                '{"text": "boo", "clickEvent": {"action": "run_command", "value": "/say hi there"}}'),
                str(JsonText.text('boo').click_event().run_command(say('hi there'))))
            self.assertEqual((
                '{"text": "boo", "clickEvent": {"action": "suggest_command", "value": "maybe"}}'),
                str(JsonText.text('boo').click_event().suggest_command('maybe')))

            self.assertEqual((
                '{"text": "boo", "hoverEvent": {"action": "show_text", "contents": "maybe"}}'),
                str(JsonText.text('boo').hover_event().show_text('maybe')))
            self.assertEqual((
                ('{"text": "boo", "hoverEvent": {"action": "show_text", "contents": {"text": "not"}}}')),
                str(JsonText.text('boo').hover_event().show_text(JsonText.text('not'))))
            self.assertEqual((
                '{"text": "boo", "hoverEvent": {"action": "show_item", "id": "bundle"}}'),
                str(JsonText.text('boo').hover_event().show_item('bundle')))
            self.assertEqual((
                '{"text": "boo", "hoverEvent": {"action": "show_item", "id": "bundle", "count": 3, "tag": "tag"}}'),
                str(JsonText.text('boo').hover_event().show_item('bundle', count=3, tag='tag')))
            self.assertEqual((
                '{"text": "boo", "hoverEvent": {"action": "show_entity", "type": "m:z", "id": "5-6-a-f"}}'),
                str(JsonText.text('boo').hover_event().show_entity('m:z', '5-6-a-f')))
            self.assertEqual((
                '{"text": "boo", "hoverEvent": {"action": "show_entity", "type": "m:z", "id": "5-6-a-f", "name": "Robin"}}'),
                str(JsonText.text('boo').hover_event().show_entity('m:z', '5-6-a-f', 'Robin')))
            self.assertEqual((
                '{"text": "boo", "hoverEvent": {"action": "show_entity", "type": "m:z", "id": "5-6-a-f",'
                ' "name": {"text": "ooh"}}}'),
                str(JsonText.text('boo').hover_event().show_entity('m:z', '5-6-a-f', JsonText.text("ooh"))))

            self.assertEqual((
                '{"text": "boo", "extra": [], "color": "green", "font": "m:f", "bold": true, '
                '"italic": true, "underlined": true, "strikethrough": true, "obfuscated": '
                'true, "insertion": "i", "clickEvent": {"action": "open_file", "value": "s"}, '
                '"hoverEvent": {"action": "show_item", "id": "bundle"}}'),
                str(JsonText.text('boo').extra().color(BLUE).font('m:f').bold().italic().underlined()
                    .strikethrough().obfuscated().insertion('i').click_event().open_file(
                    's').hover_event()
                    .show_item('bundle').color(GREEN)))

            self.assertEqual('{"text": "$(t)"}', str(JsonText.text(Arg('t'))))
            self.assertEqual('{"text": "z$(t)"}', str(JsonText.text('z$(t)')))
            self.assertEqual('{"translate": "$(t)", "with": ["$(s)"]}', str(JsonText.translate(Arg('t'), Arg('s'))))
            self.assertEqual('{"translate": "$(t)", "with": ["$(s)", "$(v)"]}',
                             str(JsonText.translate(Arg('t'), Arg('s'), Arg('v'))))
            self.assertEqual('{"score": {"name": "$(p)", "objective": "$(o)", "value": "$(v)"}}',
                             str(JsonText.score((Arg('p'), Arg('o')), Arg('v'))))
            self.assertEqual('{"selector": "$(s)", "separator": {"color": "$(c)", "text": "$(t)"}}',
                             str(JsonText.entity(Arg('s'), Arg('c'), Arg('t'))))
            self.assertEqual('{"keybind": "$(s)"}', str(JsonText.keybind(Arg('s'))))
            self.assertEqual('{"nbt": "$(p)", "entity": "@p"}', str(JsonText.nbt(Arg('p'), p())))
            self.assertEqual('{"nbt": "$(p)", "entity": "@p", "interpret": "$(i)", "separator": "$(s)"}',
                             str(JsonText.nbt(Arg('p'), p(), Arg('i'), Arg('s'))))
            self.assertEqual('{"text": "boo", "extra": ["$(e)", {"text": "$(b)"}]}',
                             str(JsonText.text('boo').extra(Arg('e'), JsonText.text(Arg('b')))))
            self.assertEqual('{"text": "foo", "color": "$(c)"}', str(JsonText.text('foo').color(Arg('c'))))
            self.assertEqual('{"text": "foo", "font": "$(f)"}', str(JsonText.text('foo').font(Arg('f'))))
            self.assertEqual('{"text": "boo", "underlined": "$(u)"}', str(JsonText.text('boo').underlined(Arg('u'))))
            self.assertEqual('{"text": "boo", "insertion": "$(i)"}',
                             str(JsonText.text('boo').insertion(Arg('i'))))

        finally:
            Nbt.sort_keys = sort_keys

    def test_known_targets(self):
        self.assertEqual('@p', str(p()))
        self.assertEqual('@r', str(rand()))
        self.assertEqual('@a', str(a()))
        self.assertEqual('@e', str(e()))
        self.assertEqual('*', str(Star()))

    def test_score(self):
        self.assertEqual('* foo', str(Score(Star(), 'foo')))
        self.assertEqual('@a bar', str(Score(a(), 'bar')))
        self.assertEqual('$(name) $(obj)', str(Score(Arg('name'), Arg('obj'))))
        x = Score('x', 'score')
        self.assertEqual(('scoreboard objectives add score dummy', 'scoreboard players set x score 17'), x.init(17))
        self.assertEqual('scoreboard players get x score', x.get())
        self.assertEqual('scoreboard players set x score 17', x.set(17))
        self.assertEqual('scoreboard players add x score 17', x.add(17))
        self.assertEqual('scoreboard players remove x score 17', x.remove(17))
        self.assertEqual('scoreboard players reset x score', x.reset())
        self.assertEqual('scoreboard players enable x score', x.enable())
        self.assertEqual('$scoreboard players add $(x) $(obj) $(v)', Score(Arg('x'), Arg('obj')).add(Arg('v')))
        self.assertEqual('$scoreboard players operation $(x) $(obj) += $(y) $(obj)',
                         Score(Arg('x'), Arg('obj')).operation(PLUS, Score(Arg('y'), Arg('obj'))))

    def test_as_score(self):
        self.assertIsNone(as_score(None))
        self.assertEqual(Score(a(), 'bar'), as_score(Score(a(), 'bar')))
        self.assertEqual(Score(a(), 'bar'), as_score((a(), 'bar')))
        self.assertEqual(Score('foo', 'bar'), as_score(('foo', 'bar')))
        self.assertEqual(Score('v$(k)', 's$(t)'), as_score(('v$(k)', 's$(t)')))
        self.assertEqual(Score('$(k)', '$(t)'), as_score((Arg('k'), Arg('t'))))

    def test_target_pos(self):
        self.assertEqual('@a[x=1,y=2,z=3]', str(a().pos((1, 2, 3))))
        self.assertEqual('@a[x=$(x),y=$(y),z=$(z)]', str(a().pos((Arg('x'), Arg('y'), Arg('z')))))
        with self.assertRaises(KeyError):
            a().pos((1, 2, 3)).pos((4, 5, 6))

    def test_target_distance(self):
        self.assertEqual('@a[distance=3]', str(a().distance(3)))
        self.assertEqual('@a[distance=$(d)]', str(a().distance(Arg('d'))))
        self.assertEqual('@a[distance=1..3]', str(a().distance((1, 3))))
        self.assertEqual('@a[distance=$(x)..$(y)]', str(a().distance((Arg('x'), Arg('y')))))
        self.assertEqual('@a[distance=..3]', str(a().distance((None, 3))))
        self.assertEqual('@a[distance=1..]', str(a().distance((1, None))))
        with self.assertRaises(KeyError):
            a().distance(3).distance(4)

    def test_target_delta(self):
        self.assertEqual('@a[dx=1,dy=2,dz=3]', str(a().volume((1, 2, 3))))
        self.assertEqual('@a[dx=$(x),dy=$(y),dz=$(z)]', str(a().volume((Arg('x'), Arg('y'), Arg('z')))))
        with self.assertRaises(KeyError):
            a().volume((1, 2, 3)).volume((4, 5, 6))

    def test_target_scores(self):
        self.assertEqual('@a[scores={x=1,y=..3}]', str(a().scores({'x': 1, 'y': '..3'})))
        self.assertEqual('@a[scores={$(x)=$(v1),v$(k)=q$(t)}]',
                         str(a().scores({Arg('x'): Arg('v1'), 'v$(k)': 'q$(t)'})))
        with self.assertRaises(KeyError):
            a().scores({'x': 1}).scores({'y': '..3'})

    def test_target_tag(self):
        self.assertEqual('@a[tag=foo]', str(a().tag('foo')))
        self.assertEqual('@a[tag=foo, tag=bar]', str(a().tag('foo', 'bar')))
        self.assertEqual('@a[tag=foo, tag=bar]', str(a().tag('foo').tag('bar')))
        self.assertEqual('@a[tag=!foo]', str(a().not_tag('foo')))
        self.assertEqual('@a[tag=!foo, tag=!bar]', str(a().not_tag('foo', 'bar')))
        self.assertEqual('@a[tag=!foo, tag=bar]', str(a().not_tag('foo').tag('bar')))
        self.assertEqual('@a[tag=!$(f), tag=v$(k)]', str(a().not_tag(Arg('f')).tag('v$(k)')))

    def test_target_literal(self):
        self.assertEqual('@a[blahblah<->]', str(a().literal('blahblah<->')))

    def test_target_team(self):
        self.assertEqual('@a[team=foo]', str(a().team('foo')))
        self.assertEqual('@a[team=v$(k)]', str(a().team('v$(k)')))
        self.assertEqual('@a[team=$(f)]', str(a().team(Arg('f'))))
        with self.assertRaises(KeyError):
            a().team('foo').team('bar')

    def test_target_not_teams(self):
        self.assertEqual('@a[team=!foo]', str(a().not_team('foo')))
        self.assertEqual('@a[team=!foo, team=!bar]', str(a().not_team('foo', 'bar')))
        self.assertEqual('@a[team=!foo, team=!bar]', str(a().not_team('foo', '!bar')))
        self.assertEqual('@a[team=!foo, team=!bar]', str(a().not_team('foo').not_team('bar')))
        self.assertEqual('@a[team=!foo, team=!bar]', str(a().not_team('foo').not_team('!bar')))
        self.assertEqual('@a[team=!$(f), team=!v$(k)]', str(a().not_team(Arg('f')).not_team('!v$(k)')))
        with self.assertRaises(KeyError):
            a().team('foo').not_team('bar')

    def test_target_sort(self):
        self.assertEqual('@a[sort=nearest]', str(a().sort(NEAREST)))
        self.assertEqual('@a[sort=v$(k)]', str(a().sort('v$(k)')))
        self.assertEqual('@a[sort=$(f)]', str(a().sort(Arg('f'))))
        with self.assertRaises(KeyError):
            a().sort(NEAREST).sort(RANDOM)
        with self.assertRaises(ValueError):
            a().sort('foo')

    def test_target_limit(self):
        self.assertEqual('@a[limit=1]', str(a().limit(1)))
        self.assertEqual('@a[limit=$(k)]', str(a().limit(Arg('k'))))
        with self.assertRaises(KeyError):
            a().limit(1).limit(2)

    def test_target_level(self):
        self.assertEqual('@a[level=3]', str(a().level(3)))
        self.assertEqual('@a[level=1..3]', str(a().level((1, 3))))
        self.assertEqual('@a[level=$(k)]', str(a().level(Arg('k'))))
        self.assertEqual('@a[level=$(v)..$(k)]', str(a().level((Arg('v'), Arg('k')))))
        with self.assertRaises(KeyError):
            a().level(3).level(4)
        with self.assertRaises(ValueError):
            a().level('v$(k)')

    def test_target_gamemode(self):
        self.assertEqual('@a[gamemode=survival]', str(a().gamemode(SURVIVAL)))
        self.assertEqual('@a[gamemode=v$(k)]', str(a().gamemode('v$(k)')))
        self.assertEqual('@a[gamemode=$(k)]', str(a().gamemode(Arg('k'))))
        with self.assertRaises(KeyError):
            a().gamemode(CREATIVE).gamemode(ADVENTURE)
        with self.assertRaises(ValueError):
            a().gamemode('foo')

    def test_target_not_gamemodes(self):
        self.assertEqual('@a[gamemode=!survival]', str(a().not_gamemode(SURVIVAL)))
        self.assertEqual('@a[gamemode=!survival, gamemode=!creative]', str(
            a().not_gamemode(SURVIVAL, CREATIVE)))
        self.assertEqual('@a[gamemode=!v$(k), gamemode=!$(k)]', str(
            a().not_gamemode('v$(k)', Arg('k'))))
        with self.assertRaises(KeyError):
            a().gamemode(CREATIVE).not_gamemode(ADVENTURE)
        with self.assertRaises(ValueError):
            a().not_gamemode('foo')

    def test_target_name(self):
        self.assertEqual('@a[name=foo]', str(a().name('foo')))
        self.assertEqual('@a[name=v$(k)]', str(a().name('v$(k)')))
        self.assertEqual('@a[name=$(k)]', str(a().name(Arg('k'))))
        with self.assertRaises(KeyError):
            a().name('foo').name('bar')

    def test_target_not_names(self):
        self.assertEqual('@a[name=!foo]', str(a().not_name('foo')))
        self.assertEqual('@a[name=!foo, name=!bar]', str(a().not_name('foo', 'bar')))
        self.assertEqual('@a[name=!foo, name=!bar]', str(a().not_name('foo', '!bar')))
        self.assertEqual('@a[name=!foo, name=!bar]', str(a().not_name('foo').not_name('bar')))
        self.assertEqual('@a[name=!$(k), name=!v$(k)]', str(a().not_name(Arg('k')).not_name('!v$(k)')))
        with self.assertRaises(KeyError):
            a().name('foo').not_name('bar')

    def test_target_x_rotation(self):
        self.assertEqual('@a[x_rotation=1.5]', str(a().x_rotation(1.5)))
        self.assertEqual('@a[x_rotation=$(v)]', str(a().x_rotation(Arg('v'))))
        with self.assertRaises(KeyError):
            a().x_rotation(1.5).x_rotation(1.5)

    def test_target_y_rotation(self):
        self.assertEqual('@a[y_rotation=1.5]', str(a().y_rotation(1.5)))
        self.assertEqual('@a[y_rotation=$(v)]', str(a().y_rotation(Arg('v'))))
        with self.assertRaises(KeyError):
            a().y_rotation(1.5).y_rotation(1.5)

    def test_target_type(self):
        self.assertEqual('@a[type=creeper]', str(a().type('creeper')))
        self.assertEqual('@a[type=v$(k)]', str(a().type('v$(k)')))
        self.assertEqual('@a[type=$(k)]', str(a().type(Arg('k'))))
        with self.assertRaises(KeyError):
            a().type('creeper').type('bat')

    def test_target_not_types(self):
        self.assertEqual('@a[type=!foo]', str(a().not_type('foo')))
        self.assertEqual('@a[type=!foo, type=!bar]', str(a().not_type('foo', 'bar')))
        self.assertEqual('@a[type=!foo, type=!bar]', str(a().not_type('foo', '!bar')))
        self.assertEqual('@a[type=!foo, type=!bar]', str(a().not_type('foo').not_type('bar')))
        self.assertEqual('@a[type=!foo, type=!bar]', str(a().not_type('foo').not_type('!bar')))
        self.assertEqual('@a[type=!$(k), type=!v$(k)]', str(a().not_type(Arg('k')).not_type('!v$(k)')))
        with self.assertRaises(KeyError):
            a().type('foo').not_type('bar')

    def test_target_nbt(self):
        self.assertEqual('@a[nbt={a: 17}]', str(a().nbt({'a': 17})))
        self.assertEqual('@a[nbt={a: 17}, nbt={b: "hi there"}]', str(a().nbt({'a': 17}, {'b': 'hi there'})))
        self.assertEqual('@a[nbt={a: 17}, nbt={b: "hi there"}]', str(a().nbt({'a': 17}).nbt({'b': 'hi there'})))
        self.assertEqual('@a[nbt=!{a: 17}, nbt=!{b: "hi there"}]',
                         str(a().not_nbt({'a': 17}).not_nbt({'b': 'hi there'})))
        self.assertEqual('@a[nbt=$(k)]', str(a().nbt(Arg('k'))))

    def test_target_advancements(self):
        self.assertEqual('@a[advancements={husbandry/wax_on=true}]', str(a().advancements(
            AdvancementCriteria(Advancement.WAX_ON, True))))
        self.assertEqual('@a[advancements={husbandry/wax_on={stuff=false}}]', str(a().advancements(AdvancementCriteria(
            Advancement.WAX_ON, ('stuff', False)))))
        self.assertEqual('@a[advancements={husbandry/wax_on={stuff=false},story/smelt_iron={stuff=false}}]',
                         str(a().advancements(
                             AdvancementCriteria(Advancement.WAX_ON, ('stuff', False)),
                             AdvancementCriteria(Advancement.ACQUIRE_HARDWARE, ('stuff', False)))))
        self.assertEqual('$advancement grant @s from $(from)', advancement(GRANT, s()).from_(Arg('from')))
        self.assertEqual('@a[advancements={v$(k)=$(k)}]', str(a().advancements(
            AdvancementCriteria('v$(k)', Arg('k')))))

    def test_target_predicate(self):
        self.assertEqual('@a[predicate=foo]', str(a().predicate('foo')))
        self.assertEqual('@a[predicate=foo, predicate=bar]', str(a().predicate('foo', 'bar')))
        self.assertEqual('@a[predicate=foo, predicate=bar]', str(a().predicate('foo').predicate('bar')))
        self.assertEqual('@a[predicate=v$(k), predicate=$(k)]', str(a().predicate('v$(k)').predicate(Arg('k'))))

    def test_target_chainability(self):
        self.assertEqual(
            '@a[x=1,y=2,z=3, distance=..15.5, dx=4.4,dy=5.5,dz=6.6, scores={}, tag=one, team=slug, '
            'sort=arbitrary, limit=15, level=3..15, gamemode=survival, name=Robin, x_rotation=9, '
            'y_rotation=..24, type=cougar, nbt={hi: there}, advancements={husbandry/plant_seed=true}, '
            'predicate=nada]',
            str(a().pos((1, 2, 3)).distance((None, 15.5)).volume((4.4, 5.5, 6.6)).scores({}).tag("one").team(
                'slug').sort(
                ARBITRARY).limit(15).level((3, 15)).gamemode(SURVIVAL).name('Robin').x_rotation(9).y_rotation(
                (None, 24)).type('cougar').nbt({"hi": "there"}).advancements(
                AdvancementCriteria(Advancement.A_SEEDY_PLACE, True)).predicate("nada")))
        self.assertEqual(
            '@a[team=!Raiders, name=!xyzzy, gamemode=!creative, type=!worm]',
            str(a().not_team('Raiders').not_name("xyzzy").not_gamemode(CREATIVE).not_type("worm")))

    def test_comment(self):
        long_line = 'This is a long line of text that would be wrapped if it were asked to be wrapped, and we use it' \
                    ' to test if wrapping does or does not happen.'
        self.assertEqual('# hi', str(comment('hi')))
        self.assertEqual('# hi', str(comment(' hi ')))
        self.assertEqual('# hi\n# there', str(comment('hi\nthere')))
        self.assertEqual('# hi\n# there', str(comment('  hi\nthere  ')))
        self.assertEqual(f'# {long_line}', str(comment(long_line)))
        self.assertEqual(f'# {long_line}\n#\n#\n# {long_line}', str(comment(long_line + '\n\n\n' + long_line)))

        self.assertEqual('# hi', str(comment('hi')))
        self.assertEqual('# hi', str(comment(' hi ')))
        self.assertEqual('# hi\n# there', str(comment('hi\nthere')))
        self.assertEqual('# hi there', str(comment('  hi\nthere  ', wrap=True)))
        self.assertEqual((
            '# This is a long line of text that would be wrapped if it were asked to be\n# wrapped, and we use it to test'
            ' if wrapping does or does not happen.'), str(comment(long_line, wrap=True)))
        self.assertEqual((
            '# This is a long line of text that would be wrapped if it were asked to be\n'
            '# wrapped, and we use it to test if wrapping does or does not happen.\n'
            '#\n'
            '# This is a long line of text that would be wrapped if it were asked to be\n'
            '# wrapped, and we use it to test if wrapping does or does not happen.'),
            str(comment(long_line + '\n\n\n' + long_line, wrap=True)))

    def test_literal(self):
        self.assertEqual('xyzzy', str(literal('xyzzy')))

    def test_attribute(self):
        self.assertEqual('attribute @s foo get', attribute(s(), 'foo').get())
        self.assertEqual('$attribute @s foo modifier add $(uuid) "robin" 1.3',
                         attribute(s(), 'foo').modifier().add(Arg('uuid'), 'robin', 1.3))
        self.assertEqual('$attribute @s x$(k) get', attribute(s(), 'x$(k)').get())
        self.assertEqual('$attribute @s $(f) get', attribute(s(), Arg('f')).get())

    def test_attribute_act(self):
        self.assertEqual('get', str(_AttributeMod().get()))
        self.assertEqual('get 1.2', str(_AttributeMod().get(1.2)))
        self.assertEqual('base get', str(_AttributeMod().base().get()))
        self.assertEqual('base get 1.2', str(_AttributeMod().base().get(1.2)))
        self.assertEqual('base set 1.2', str(_AttributeMod().base().set(1.2)))
        self.assertEqual('modifier add 1-2-3-f "robin" 1.3',
                         str(_AttributeMod().modifier().add('1-2-3-f', 'robin', 1.3)))
        self.assertEqual('modifier remove 1-2-3-f', str(_AttributeMod().modifier().remove('1-2-3-f')))
        self.assertEqual('modifier value get 1-2-3-f', str(_AttributeMod().modifier().value('1-2-3-f')))
        self.assertEqual('modifier value get 1-2-3-f 1.3', str(_AttributeMod().modifier().value('1-2-3-f', 1.3)))

    def test_bossbar(self):
        self.assertEqual('bossbar add foo stud', bossbar().add('foo', 'stud'))
        self.assertEqual('bossbar list', bossbar().list())
        self.assertEqual('bossbar remove foo', bossbar().remove('foo'))

        self.assertEqual('bossbar get foo color', bossbar().get('foo').color())
        self.assertEqual('bossbar get foo max', bossbar().get('foo').max())
        self.assertEqual('bossbar get foo name', bossbar().get('foo').name())
        self.assertEqual('bossbar get foo players', bossbar().get('foo').players())
        self.assertEqual('bossbar get foo style', bossbar().get('foo').style())
        self.assertEqual('bossbar get foo value', bossbar().get('foo').value())
        self.assertEqual('bossbar get foo visible', bossbar().get('foo').visible())

        self.assertEqual('bossbar set foo color blue', bossbar().set('foo').color(BLUE))
        self.assertEqual('bossbar set foo max 17', bossbar().set('foo').max(17))
        self.assertEqual('bossbar set foo name "Libby the Kid"', bossbar().set('foo').name('Libby the Kid'))
        self.assertEqual('bossbar set foo players @s', bossbar().set('foo').players(s()))
        self.assertEqual('bossbar set foo style notched_12', bossbar().set('foo').style(NOTCHED_12))
        self.assertEqual('bossbar set foo value 17', bossbar().set('foo').value(17))
        self.assertEqual('bossbar set foo visible false', bossbar().set('foo').visible(False))

        self.assertEqual('$bossbar set foo max $(v)', bossbar().set('foo').max(Arg('v')))
        self.assertEqual('$bossbar set foo max +$(v).1', bossbar().set('foo').max('+$(v).1'))

    def test_clear(self):
        self.assertEqual('clear @s foo{bar}', clear(s()).item('foo{bar}'))
        self.assertEqual('clear @s foo{bar} 4', clear(s()).item('foo{bar}', 4))

    def test_clone(self):
        self.assertEqual('clone 1 ~2 ^3 4 5 6 7 8 9', str(clone((1, r(2), d(3)), (4, 5, 6), (7, 8, 9))))
        self.assertEqual('clone 1 ~2 ^3 4 5 6 7 8 9 replace', clone((1, r(2), d(3)), (4, 5, 6), (7, 8, 9)).replace())
        self.assertEqual('clone 1 ~2 ^3 4 5 6 7 8 9 masked force',
                         clone((1, r(2), d(3)), (4, 5, 6), (7, 8, 9)).masked(FORCE))
        self.assertEqual('clone 1 ~2 ^3 4 5 6 7 8 9 filtered stone force',
                         clone((1, r(2), d(3)), (4, 5, 6), (7, 8, 9)).filtered('stone', FORCE))

        self.assertEqual('clone 1 ~2 ^3 4 5 6 7 8 9',
                         str(clone((1, r(2), d(3)), (4, 5, 6), (7, 8, 9), LEAST)))
        self.assertEqual('clone 1 2 3 4 5 6 4 5 6', str(clone((1, 2, 3), (4, 5, 6), (7, 8, 9), LAST)))
        self.assertEqual('clone ~1 ~2 ~3 ~4 ~5 ~6 ~4 ~5 ~6', str(clone(r(1, 2, 3), r(4, 5, 6), r(7, 8, 9), LAST)))
        self.assertEqual('clone ~1 ~2 ~3 ~4 ~5 ~6 ~11 ~2 ~13', str(clone(r(1, 2, 3), r(4, 5, 6), (10, 0, 10), DELTA)))
        self.assertEqual('clone from overworld 1 ~2 ^3 4 5 6 to the_end 7 8 9',
                         str(clone().from_('overworld', (1, r(2), d(3)), (4, 5, 6)).to('the_end', (7, 8, 9))))
        self.assertEqual('clone from overworld 1 ~2 ^3 4 5 6 to the_end 7 8 9 replace',
                         str(clone()
                             .from_('overworld', (1, r(2), d(3)), (4, 5, 6))
                             .to('the_end', (7, 8, 9)).replace()))
        self.assertEqual('clone from overworld ~1 ~2 ~3 ~4 ~5 ~6 to the_end ~11 ~2 ~13',
                         str(clone().from_('overworld', r(1, 2, 3), r(4, 5, 6)).to('the_end', (10, 0, 10), DELTA)))
        with self.assertRaises(ValueError):
            clone(r(1, 2, 3))
        with self.assertRaises(ValueError):
            clone(r(1, 2, 3), r(4, 5, 6), d(1, 2, 3), LAST)
        with self.assertRaises(TypeError):
            clone(r(1, 2, 3), d(4, 5, 6), (1, 2, 3), LAST)
        with self.assertRaises(ValueError):
            clone(r(1, 2, 3), d(4, 5, 6), d(1, 2, 3), DELTA)
        with self.assertRaises(ValueError):
            clone(r(1, 2, 3), d(4, 5, 6), r(1, 2, 3), DELTA)

    def test_damage(self):
        self.assertEqual('damage @s 15', str(damage(s(), 15)))
        self.assertEqual('damage @s 15 a:b', str(damage(s(), 15, 'a:b')))
        self.assertEqual('damage @a 27 at 1 ~2 ^3', str(damage(a(), 27).at((1, r(2), d(3)))))
        self.assertEqual('damage @a 27 by @s', str(damage(a(), 27).by(s())))
        self.assertEqual('damage @a 27 by @s from @p', str(damage(a(), 27).by(s()).from_(p())))
        self.assertEqual('$damage $(tgt) $(d) $(w)', str(damage(Arg('tgt'), Arg('d'), Arg('w'))))

    def test_data_target(self):
        self.assertEqual('block 1 ~2 ^3', data_target_str((1, r(2), d(3))))
        self.assertEqual('entity @s', data_target_str(s()))
        self.assertEqual('storage m:/a/b', data_target_str('m:/a/b'))
        with self.assertRaises(ValueError):
            data_target_str('v$(k)')
        with self.assertRaises(ValueError):
            data_target_str(Arg('k'))

    def test_data(self):
        self.assertEqual('data get entity @s', data().get(s()))
        self.assertEqual('data get block ~1 ~2 ~3', data().get(block(r(1, 2, 3))))
        self.assertEqual('data get entity @s', data().get(entity(s())))
        self.assertEqual('$data get entity $(s)', data().get(entity(Arg('s'))))

    def test_effect(self):
        self.assertEqual('effect give @s speed', effect().give(s(), Effect.SPEED))
        self.assertEqual('effect give @s speed 100', effect().give(s(), Effect.SPEED, 100))
        self.assertEqual('effect give @s speed 100 2', effect().give(s(), Effect.SPEED, 100, 2))
        self.assertEqual('effect give @s speed 100 2 true', effect().give(s(), Effect.SPEED, 100, 2, True))
        self.assertEqual('effect give @s speed infinite', effect().give(s(), Effect.SPEED, INFINITE))
        self.assertEqual('effect clear', effect().clear())
        self.assertEqual('effect clear @s', effect().clear(s()))
        self.assertEqual('effect clear @s speed', effect().clear(s(), 'speed'))
        self.assertEqual('effect clear @s speed', effect().clear(s(), Effect.SPEED))
        self.assertEqual('$effect give $(tgt) $(e) $(d) $(a) $(h)',
                         effect().give(Arg('tgt'), Arg('e'), Arg('d'), Arg('a'), Arg('h')))
        self.assertEqual('$effect give $(tgt) $(e) +$(d)1 +$(a)2 $(h)',
                         effect().give(Arg('tgt'), Arg('e'), '+$(d)1', '+$(a)2', Arg('h')))
        with self.assertRaises(ValueError):
            effect().give(s(), Effect.SPEED, -1)
        with self.assertRaises(ValueError):
            effect().give(s(), Effect.SPEED, MAX_EFFECT_SECONDS + 100)
        with self.assertRaises(ValueError):
            effect().give(s(), Effect.SPEED, None, 2)
        with self.assertRaises(ValueError):
            effect().give(s(), Effect.SPEED, None, None, True)
        with self.assertRaises(ValueError):
            effect().give(s(), Effect.SPEED, 100, None, True)
        with self.assertRaises(ValueError):
            effect().clear(None, Effect.SPEED)
        with self.assertRaises(ValueError):
            effect().give(s(), Effect.SPEED, 'foo')

    def test_enchant(self):
        self.assertEqual('enchant @s lure', enchant(s(), Enchantment.LURE))
        self.assertEqual('enchant @s lure', enchant(s(), 'lure'))
        self.assertEqual('enchant @s lure 2', enchant(s(), Enchantment.LURE, 2))
        self.assertEqual('enchant @s 12', enchant(s(), 12))
        self.assertEqual('enchant @s 12 2', enchant(s(), 12, 2))
        with self.assertRaises(ValueError):
            enchant(s(), Enchantment.LURE, 17)

    def test_jfr(self):
        self.assertEqual('jfr start', jfr(START))
        self.assertEqual('jfr stop', jfr(STOP))

    def test_perf(self):
        self.assertEqual('perf start', perf(START))
        self.assertEqual('perf stop', perf(STOP))

    def test_tick(self):
        self.assertEqual('tick query', tick().query())
        self.assertEqual('tick rate 17', tick().rate(17))
        self.assertEqual('tick freeze', tick().freeze())
        self.assertEqual('tick unfreeze', tick().unfreeze())
        self.assertEqual('tick step 17', tick().step(17))
        self.assertEqual('tick step stop', tick().step().stop())
        self.assertEqual('tick sprint 17', tick().sprint(17))
        self.assertEqual('tick sprint stop', tick().sprint().stop())

    def test_return(self):
        self.assertEqual('return 17', return_(17))
        self.assertEqual('return 0', str(return_()))
        self.assertEqual('return run say hi', return_().run(say('hi')))
        self.assertEqual('return run say hi', return_().run('say hi'))

    def test_say(self):
        self.assertEqual('say test', say('test'))
        self.assertEqual('$say v$(test)', say('v$(test)'))
        self.assertEqual('$say $(test)', say(Arg('test')))

    def test_setidletimeout(self):
        self.assertEqual('setidletimeout 17', setidletimeout(17))

    def test_experience(self):
        self.assertEqual('experience add @s 3 levels', experience().add(s(), 3, LEVELS))
        self.assertEqual('experience add @s 3 points', experience().add(s(), 3, POINTS))
        self.assertEqual('experience set @s 3 levels', experience().set(s(), 3, LEVELS))
        self.assertEqual('experience set @s 3 points', experience().set(s(), 3, POINTS))
        self.assertEqual('experience set @s 3', experience().set(s(), 3))
        self.assertEqual('experience query @s points', experience().query(s(), POINTS))
        self.assertEqual('experience query @s levels', experience().query(s(), LEVELS))
        self.assertEqual('experience query @s points', xp().query(s(), POINTS))
        self.assertEqual('$experience add $(tgt) $(amt) $(w)', experience().add(Arg('tgt'), Arg('amt'), Arg('w')))

    def test_fill(self):
        self.assertEqual('fill 1 ~2 ^3 4 5 6 stone', str(fill((1, r(2), d(3)), (4, 5, 6), 'stone')))
        self.assertEqual('fill 1 ~2 ^3 4 5 6 stone replace', str(fill((1, r(2), d(3)), (4, 5, 6), 'stone').replace()))
        self.assertEqual('fill 1 ~2 ^3 4 5 6 stone replace air',
                         fill((1, r(2), d(3)), (4, 5, 6), 'stone').replace('air'))
        self.assertEqual('fill 1 ~2 ^3 4 5 6 stone replace oak_log[axis=y]',
                         fill((1, r(2), d(3)), (4, 5, 6), 'stone').replace(Block('oak_log', {'axis': 'y'})))
        self.assertEqual('fill 1 ~2 ^3 4 5 6 stone hollow', str(fill((1, r(2), d(3)), (4, 5, 6), 'stone').hollow()))
        self.assertEqual('fill 1 ~2 ^3 4 5 6 stone destroy', str(fill((1, r(2), d(3)), (4, 5, 6), 'stone').destroy()))
        self.assertEqual('fill 1 ~2 ^3 4 5 6 stone keep', str(fill((1, r(2), d(3)), (4, 5, 6), 'stone').keep()))
        self.assertEqual('fill 1 ~2 ^3 4 5 6 stone outline', str(fill((1, r(2), d(3)), (4, 5, 6), 'stone').outline()))

    def test_fillbiome(self):
        self.assertEqual('fillbiome 1 ~2 ^3 4 5 6 beach', str(fillbiome((1, r(2), d(3)), (4, 5, 6), BiomeId.BEACH)))
        self.assertEqual('fillbiome 1 ~2 ^3 4 5 6 beach replace m:ice',
                         fillbiome((1, r(2), d(3)), (4, 5, 6), BiomeId.BEACH).replace('m:ice'))

    def test_data_mod(self):
        self.assertEqual('get entity @s', str(_DataMod().get(s())))
        self.assertEqual('merge entity @s {}', str(_DataMod().merge(s(), {})))
        self.assertEqual('modify entity @s a.b', str(_DataMod().modify(s(), 'a.b')))
        self.assertEqual('modify entity @s a.b append from storage m:b name',
                         str(_DataMod().modify(s(), 'a.b').append().from_('m:b', 'name')))
        self.assertEqual('modify entity @s a.b insert 3 value "hi there"',
                         str(_DataMod().modify(s(), 'a.b').insert(3).value('hi there')))
        self.assertEqual('modify entity @s x merge value "hi there"',
                         str(_DataMod().modify(s(), 'x').merge().value('hi there')))
        self.assertEqual('modify entity @s x prepend value "hi there"',
                         str(_DataMod().modify(s(), 'x').prepend().value('hi there')))
        self.assertEqual('modify entity @s x set value "hi there"',
                         str(_DataMod().modify(s(), 'x').set().value('hi there')))
        self.assertEqual('remove entity @s x', str(_DataMod().remove(s(), 'x')))
        with self.assertRaises(ValueError):
            _DataMod().get((1, r(2), d(3)), None, 2.2)

    def test_data_modify(self):
        self.assertEqual('modify entity @p path append from entity @s path2',
                         str(_DataMod().modify(p(), 'path').append().from_(s(), 'path2')))
        self.assertEqual('modify entity @p path append from block ~1 ~2 ~3 path2',
                         str(_DataMod().modify(p(), 'path').append().from_(r(1, 2, 3), 'path2')))
        self.assertEqual('modify entity @p path append from storage store path2',
                         str(_DataMod().modify(p(), 'path').append().from_('store', 'path2')))
        self.assertEqual('modify entity @p path append string entity @s path2',
                         str(_DataMod().modify(p(), 'path').append().string(s(), 'path2')))
        self.assertEqual('modify entity @p path append string entity @s path2 10',
                         str(_DataMod().modify(p(), 'path').append().string(s(), 'path2', 10)))
        self.assertEqual('modify entity @p path append string entity @s path2 10 20',
                         str(_DataMod().modify(p(), 'path').append().string(s(), 'path2', 10, 20)))
        self.assertEqual('modify entity @p path append value 1.9f',
                         str(_DataMod().modify(p(), 'path').append().value(1.9)))
        self.assertEqual('modify entity @p path insert 2 value 1.9f',
                         str(_DataMod().modify(p(), 'path').insert(2).value(1.9)))
        self.assertEqual('modify entity @p path merge value 1.9f',
                         str(_DataMod().modify(p(), 'path').merge().value(1.9)))
        self.assertEqual('modify entity @p path prepend value 1.9f',
                         str(_DataMod().modify(p(), 'path').prepend().value(1.9)))
        self.assertEqual('modify entity @p path set value 1.9f',
                         str(_DataMod().modify(p(), 'path').set().value(1.9)))
        with self.assertRaises(ValueError):
            _DataMod().modify(e().tag('foo'), 'path').append().from_(e().tag('foo'), 'path2')

    def test_datapack(self):
        self.assertEqual('datapack disable robin', str(datapack().disable('robin')))
        self.assertEqual('datapack enable robin', str(datapack().enable('robin')))
        self.assertEqual('datapack enable robin first', datapack().enable('robin').first())
        self.assertEqual('datapack enable robin last', datapack().enable('robin').last())
        self.assertEqual('datapack enable robin before kelly', datapack().enable('robin').before('kelly'))
        self.assertEqual('datapack enable robin after kelly', datapack().enable('robin').after('kelly'))
        self.assertEqual('datapack list', datapack().list())
        self.assertEqual('datapack list enabled', datapack().list(ENABLED))

    def test_forceload(self):
        self.assertEqual('forceload add 1 ~2', forceload().add((1, r(2))))
        self.assertEqual('forceload add 1 ~2 4 5', forceload().add((1, r(2)), (4, 5)))
        self.assertEqual('forceload remove 1 ~2', forceload().remove((1, r(2))))
        self.assertEqual('forceload remove 1 ~2 4 5', forceload().remove((1, r(2)), (4, 5)))
        self.assertEqual('forceload remove all', forceload().remove_all())
        self.assertEqual('forceload query', forceload().query())
        self.assertEqual('forceload query 1 ~2', forceload().query((1, r(2))))

    def test_gamemode(self):
        self.assertEqual('gamemode survival', gamemode(SURVIVAL))
        self.assertEqual('gamemode survival @s', gamemode(SURVIVAL, s()))

    def test_gamerule(self):
        self.assertEqual('gamerule disableRaids', gamerule(GameRule.DISABLE_RAIDS))
        self.assertEqual('gamerule disableRaids true', gamerule(GameRule.DISABLE_RAIDS, True))
        self.assertEqual('gamerule maxCommandChainLength 13', gamerule(GameRule.MAX_COMMAND_CHAIN_LENGTH, 13))
        self.assertEqual('gamerule disableRaids true', gamerule('disableRaids', True))
        self.assertEqual('$gamerule $(r) $(v)', gamerule(Arg('r'), Arg('v')))
        self.assertEqual('$gamerule disableRaids $(v)', gamerule(GameRule.DISABLE_RAIDS, Arg('v')))
        self.assertEqual('$gamerule $(r) 12', gamerule(Arg('r'), 12))
        self.assertEqual('$gamerule $(r) true', gamerule(Arg('r'), True))
        with self.assertRaises(ValueError):
            gamerule(GameRule.DISABLE_RAIDS, 17)
        with self.assertRaises(ValueError):
            gamerule(GameRule.MAX_COMMAND_CHAIN_LENGTH, True)
        with self.assertRaises(ValueError):
            gamerule('nothing', 17)

    def test_give(self):
        self.assertEqual('give @s foo', give(s(), 'foo'))
        self.assertEqual('give @s foo 17', give(s(), 'foo', 17))

    def test_help(self):
        self.assertEqual('help', help())
        self.assertEqual('help foo', help('foo'))

    def test_item(self):
        self.assertEqual('item modify block 1 ~2 ^3 a.17', str(item().modify().block((1, r(2), d(3)), 'a.17')))
        self.assertEqual('item modify block 1 ~2 ^3 a.17 m:a',
                         str(item().modify().block((1, r(2), d(3)), 'a.17', 'm:a')))
        self.assertEqual('item modify entity @s a.17', str(item().modify().entity(s(), 'a.17')))
        self.assertEqual('item modify entity @s a.17 m:a', str(item().modify().entity(s(), 'a.17', 'm:a')))
        self.assertEqual('item replace entity @s a.17 with a{b}',
                         str(item().replace().entity(s(), 'a.17').with_('a{b}')))
        self.assertEqual('item replace entity @s a.17 with a{b} 2',
                         str(item().replace().entity(s(), 'a.17').with_('a{b}', 2)))
        self.assertEqual('item replace entity @s a.17 from block 1 ~2 ^3 a.17',
                         str(item().replace().entity(s(), 'a.17').from_().block((1, r(2), d(3)), 'a.17')))
        self.assertEqual('item replace entity @s a.17 from block 1 ~2 ^3 a.17 m:a',
                         str(item().replace().entity(s(), 'a.17').from_().block((1, r(2), d(3)), 'a.17', 'm:a')))
        self.assertEqual('item replace entity @s a.17 from entity @p a.17',
                         str(item().replace().entity(s(), 'a.17').from_().entity(p(), 'a.17')))
        self.assertEqual('item replace entity @s a.17 from entity @p a.17 m:a',
                         str(item().replace().entity(s(), 'a.17').from_().entity(p(), 'a.17', 'm:a')))
        self.assertEqual('item replace block 1 ~2 ^3 hotbar.0 with air',
                         str(item().replace().block((1, r(2), d(3)), 'hotbar.0').with_('air')))
        self.assertEqual('item replace block 1 ~2 ^3 hotbar.0 from entity @s b',
                         str(item().replace().block((1, r(2), d(3)), 'hotbar.0').from_().entity(s(), 'b')))
        self.assertEqual('$item modify entity @s $(slot) $(mod)',
                         str(item().modify().entity(s(), Arg('slot'), Arg('mod'))))
        with self.assertRaises(ValueError):
            item().replace().block((1, r(2), d(3)), 'a.17', 'm:a')
        with self.assertRaises(ValueError):
            item().replace().entity(s(), 'a.17', 'm:a')

    def test_kill_command(self):
        self.assertEqual('kill', kill())
        self.assertEqual('kill @s', kill(s()))

    def test_list_command(self):
        self.assertEqual('list', str(list_()))
        self.assertEqual('list uuids', list_().uuids())

    def test_locate_command(self):
        self.assertEqual('locate structure foo', locate(STRUCTURE, 'foo'))
        self.assertEqual('locate biome foo', locate(BIOME, 'foo'))
        self.assertEqual('locate poi foo', locate(POI, 'foo'))

    def test_loot_command(self):
        self.assertEqual('loot give @s fish m:/a/b 1 ~2 ^3 stone', loot().give(s()).fish('m:/a/b', (1, r(2), d(3)),
                                                                                         'stone'))
        self.assertEqual('loot insert 1 ~2 ^3 loot m:/a/b', loot().insert((1, r(2), d(3))).loot('m:/a/b'))
        self.assertEqual('loot spawn 1 ~2 ^3 kill @p', loot().spawn((1, r(2), d(3))).kill(p()))
        self.assertEqual((
            'loot replace block 1 ~2 ^3 13 mine 4 ~5 ^6 mainhand'),
            loot().replace().block((1, r(2), d(3)), 13).mine((4, r(5), d(6)), MAINHAND))
        self.assertEqual('loot replace block 1 ~2 ^3 13 2 kill @p',
                         loot().replace().block((1, r(2), d(3)), 13, 2).kill(p()))
        self.assertEqual('loot replace entity @a 12 kill @p',
                         loot().replace().entity(a(), 12).kill(p()))
        self.assertEqual('loot replace entity @a 12 3 kill @p',
                         loot().replace().entity(a(), 12, 3).kill(p()))

    def test_particle_command(self):
        self.assertEqual('particle ash', particle(Particle.ASH))
        self.assertEqual('particle ash 1 ~2 ^3', particle(Particle.ASH, (1, r(2), d(3))))
        self.assertEqual('particle ash 1 ~2 ^3 4 ~5 ^6 2.1 15 force',
                         particle(Particle.ASH, (1, r(2), d(3)), (4, r(5), d(6)), 2.1, 15, FORCE))

    def test_place(self):
        self.assertEqual('place feature m:b', place().feature('m:b'))
        self.assertEqual('place feature m:b 1 ~2 ^3', place().feature('m:b', (1, r(2), d(3))))
        self.assertEqual('place jigsaw m:a m:b 7', place().jigsaw('m:a', 'm:b', 7))
        self.assertEqual('place jigsaw m:a m:b 7 1 ~2 ^3', place().jigsaw('m:a', 'm:b', 7, (1, r(2), d(3))))
        self.assertEqual('place structure m:b', place().structure('m:b'))
        self.assertEqual('place structure m:b 1 ~2 ^3', place().structure('m:b', (1, r(2), d(3))))

    def test_playsound(self):
        self.assertEqual('playsound m:s m:a @s', playsound('m:s', 'm:a', s()))
        self.assertEqual('playsound m:s m:a @s 1 ~2 ^3', playsound('m:s', 'm:a', s(), (1, r(2), d(3))))
        self.assertEqual('playsound m:s m:a @s 1 ~2 ^3 1.2', playsound('m:s', 'm:a', s(), (1, r(2), d(3)), 1.2))
        self.assertEqual('playsound m:s m:a @s 1 ~2 ^3 1.2 17.9', playsound('m:s', 'm:a', s(), (1, r(2), d(3)), 1.2,
                                                                            17.9))
        self.assertEqual('playsound m:s m:a @s 1 ~2 ^3 1.2 17.9 1.0',
                         playsound('m:s', 'm:a', s(), (1, r(2), d(3)), 1.2, 17.9,
                                   1.0))

    def test_recipe(self):
        self.assertEqual('recipe give @s *', recipe(GIVE, s(), '*'))
        self.assertEqual('recipe give @s m:/a/b', recipe(GIVE, s(), 'm:/a/b'))

    def test_ride(self):
        self.assertEqual('ride @s mount @e[tag=vehicle, limit=1]', ride(s()).mount(e().tag('vehicle').limit(1)))
        self.assertEqual('ride @s dismount', ride(s()).dismount())

    def test_debug(self):
        self.assertEqual('debug start', debug().start())
        self.assertEqual('debug stop', debug().stop())
        self.assertEqual('debug function foo', debug().function('foo'))
        self.assertEqual('debug function foo', debug().function(Function('foo')))

    def test_scoreboard_objectives(self):
        self.assertEqual('scoreboard objectives add obj food', scoreboard().objectives().add('obj', ScoreCriteria.FOOD))
        self.assertEqual('scoreboard objectives add obj drink', scoreboard().objectives().add('obj', 'drink'))
        self.assertEqual('list', _ScoreboardObjectivesMod().list())
        self.assertEqual('add obj food', _ScoreboardObjectivesMod().add('obj', ScoreCriteria.FOOD))
        self.assertEqual('add obj food howdy', _ScoreboardObjectivesMod().add('obj', ScoreCriteria.FOOD, 'howdy'))
        self.assertEqual('add obj air', _ScoreboardObjectivesMod().add('obj', ScoreCriteria.AIR))
        self.assertEqual('remove obj', _ScoreboardObjectivesMod().remove('obj'))
        self.assertEqual('setdisplay sidebar', _ScoreboardObjectivesMod().setdisplay(SIDEBAR))
        self.assertEqual('setdisplay sidebar.team.blue obj',
                         _ScoreboardObjectivesMod().setdisplay(SIDEBAR_TEAM + 'blue', 'obj'))
        self.assertEqual('modify obj displayname fred', _ScoreboardObjectivesMod().modify('obj').displayname('fred'))
        self.assertEqual('modify obj rendertype hearts', _ScoreboardObjectivesMod().modify('obj').rendertype(HEARTS))
        self.assertEqual('modify obj numberformat styled {\'bold\': True}',
                         _ScoreboardObjectivesMod().modify('obj').numberformat().styled({'bold': True}))
        self.assertEqual('modify obj numberformat fixed bubble',
                         _ScoreboardObjectivesMod().modify('obj').numberformat().fixed('bubble'))
        self.assertEqual('modify obj numberformat blank',
                         _ScoreboardObjectivesMod().modify('obj').numberformat().blank())

    def test_scoreboard_players(self):
        self.assertEqual('scoreboard players enable * obj', str(scoreboard().players().enable((Star(), 'obj'))))
        self.assertEqual('scoreboard players enable * obj', str(scoreboard().players().enable(Score(Star(), 'obj'))))
        self.assertEqual('list *', _ScoreboardPlayersMod().list(Star()))
        self.assertEqual('get @a obj', _ScoreboardPlayersMod().get((a(), 'obj')))
        self.assertEqual('get @a obj', _ScoreboardPlayersMod().get(Score(a(), 'obj')))
        self.assertEqual('set robin obj 12', _ScoreboardPlayersMod().set((User('robin'), 'obj'), 12))
        self.assertEqual('set robin obj 12', _ScoreboardPlayersMod().set(Score(User('robin'), 'obj'), 12))
        self.assertEqual('add @a obj 12', _ScoreboardPlayersMod().add((a(), 'obj'), 12))
        self.assertEqual('add @a obj 12', _ScoreboardPlayersMod().add(Score(a(), 'obj'), 12))
        self.assertEqual('remove @a obj 12', _ScoreboardPlayersMod().remove((a(), 'obj'), 12))
        self.assertEqual('remove @a obj 12', _ScoreboardPlayersMod().remove(Score(a(), 'obj'), 12))
        self.assertEqual('enable @a obj', _ScoreboardPlayersMod().enable(Score(a(), 'obj')))
        self.assertEqual('operation * obj += @r obj2',
                         _ScoreboardPlayersMod().operation((Star(), 'obj'), PLUS, Score(rand(), 'obj2')))
        self.assertEqual('operation * obj += @r obj2',
                         _ScoreboardPlayersMod().operation(Score(Star(), 'obj'), PLUS, Score(rand(), 'obj2')))
        self.assertEqual('operation * obj > @r obj2',
                         _ScoreboardPlayersMod().operation(Score(Star(), 'obj'), MAX, Score(rand(), 'obj2')))
        self.assertEqual('display name * obj display', _ScoreboardPlayersMod().display().name(Star(), 'obj', 'display'))
        self.assertEqual('display name * obj', _ScoreboardPlayersMod().display().name(Star(), 'obj'))
        self.assertEqual('display numberformat * sc blank',
                         _ScoreboardPlayersMod().display().numberformat(Star(), 'sc').blank())
        self.assertEqual('display numberformat * sc',
                         str(_ScoreboardPlayersMod().display().numberformat(Star(), 'sc')))

        self.assertEqual('reset @a obj', _ScoreboardPlayersMod().reset((a(), 'obj')))
        self.assertEqual('reset @a obj', _ScoreboardPlayersMod().reset(Score(a(), 'obj')))
        self.assertEqual('reset @a', _ScoreboardPlayersMod().reset((a())))
        self.assertEqual('reset @a', _ScoreboardPlayersMod().reset((a(), None)))
        self.assertEqual('reset @a', _ScoreboardPlayersMod().reset(a()))
        self.assertEqual('reset fred', _ScoreboardPlayersMod().reset('fred'))

    def test_scoreboard_criteria(self):
        self.assertEqual('air', str(_ScoreboardCriteria(ScoreCriteria.AIR)))
        self.assertEqual('has.air', str(_ScoreboardCriteria('has', ScoreCriteria.AIR)))
        self.assertEqual('killed_by.m:zombie', str(_ScoreboardCriteria('killed_by', 'm:zombie')))
        self.assertEqual('on.team.purple', str(_ScoreboardCriteria('on', 'team', 'purple')))

    def test_publish_command(self):
        self.assertEqual('publish', publish())
        self.assertEqual('publish true', publish(True))
        self.assertEqual('publish false spectator', publish(False, SPECTATOR))
        self.assertEqual('publish false spectator 106', publish(False, SPECTATOR, 106))

    def test_schedule_command(self):
        self.assertEqual('schedule function m:b/c 1.3d append', schedule().function('m:b/c', days(1.3), APPEND))
        self.assertEqual('schedule function m:b/c 2.3s replace', schedule().function('m:b/c', seconds(2.3), REPLACE))
        self.assertEqual('schedule function m:b/c 9 replace', schedule().function('m:b/c', ticks(9), REPLACE))
        self.assertEqual('schedule function m:b/c 3 replace', schedule().function('m:b/c', 3, REPLACE))
        self.assertEqual('schedule clear m:b/c', schedule().clear('m:b/c'))
        with self.assertRaises(ValueError):
            schedule().function('m:b/c', 'hi', REPLACE)

    def test_setblock_command(self):
        self.assertEqual('setblock 1 ~2 ^3 m:s', str(setblock((1, r(2), d(3)), 'm:s')))
        self.assertEqual('setblock 1 ~2 ^3 m:s replace', str(setblock((1, r(2), d(3)), 'm:s', REPLACE)))
        self.assertEqual('setblock 1 ~2 ^3 stone{foo: bar}',
                         str(setblock((1, r(2), d(3)), 'stone').nbt({'foo': 'bar'})))
        self.assertEqual('setblock 1 ~2 ^3 stone{foo: baz}',
                         str(setblock((1, r(2), d(3)), 'stone').nbt({'foo': 'bar'}).nbt({'foo': 'baz'})))
        self.assertEqual('setblock 1 ~2 ^3 stone[up=down]',
                         str(setblock((1, r(2), d(3)), 'stone').state({'up': 'down'})))
        self.assertEqual(
            'setblock 1 ~2 ^3 stone[up=upper]',
            str(setblock((1, r(2), d(3)), 'stone').state({'up': 'down'}).state({'up': 'upper'})))
        self.assertEqual('setblock 1 ~2 ^3 stone[up=down]{up: upper}',
                         str(setblock((1, r(2), d(3)), 'stone').state({'up': 'down'}).nbt({'up': 'upper'})))
        self.assertEqual('$setblock 0 0 0 v$(b)', str(setblock((0, 0, 0), 'v$(b)')))
        self.assertEqual('$setblock 0 0 0 $(b)', str(setblock((0, 0, 0), Arg('b'))))

    def test_setworldspawn_command(self):
        self.assertEqual('setworldspawn', setworldspawn())
        self.assertEqual('setworldspawn 1 ~2 ^3', setworldspawn((1, r(2), d(3))))
        self.assertEqual('setworldspawn 1 ~2 ^3 9.3', setworldspawn((1, r(2), d(3)), 9.3))
        self.assertEqual('$setworldspawn $(x) $(y) $(z) $(angle)',
                         setworldspawn((Arg('x'), Arg('y'), Arg('z')), Arg('angle')))

    def test_spawnpoint_command(self):
        self.assertEqual('spawnpoint', spawnpoint())
        self.assertEqual('spawnpoint @s', spawnpoint(s()))
        self.assertEqual('spawnpoint @s 1 ~2 ^3', spawnpoint(s(), (1, r(2), d(3))))
        self.assertEqual('spawnpoint @s 1 ~2 ^3 9.3', spawnpoint(s(), (1, r(2), d(3)), 9.3))

    def test_spectate_command(self):
        self.assertEqual('spectate @s', spectate(s()))
        self.assertEqual('spectate @s @r', spectate(s(), rand()))

    def test_spreadplayers_command(self):
        self.assertEqual('spreadplayers 1 ~2 ^3 1.7 15.3 true @a', spreadplayers((1, r(2), d(3)), 1.7, 15.3, True, a()))
        self.assertEqual('spreadplayers 1 ~2 ^3 1.7 15.3 under 150 true @a',
                         spreadplayers((1, r(2), d(3)), 1.7, 15.3, True, a(), 150))

    def test_stopsound_command(self):
        self.assertEqual('stopsound @a', stopsound(a()))
        self.assertEqual('stopsound @a m:/a/b', stopsound(a(), 'm:/a/b'))
        self.assertEqual('stopsound @a m:/a/b m:c', stopsound(a(), 'm:/a/b', 'm:c'))

    def test_summon_command(self):
        self.assertEqual('summon m:z', summon('m:z'))
        self.assertEqual('summon m:z 1 ~2 ^3', summon('m:z', (1, r(2), d(3))))
        self.assertEqual('summon m:z 1 ~2 ^3 {NoAI: true}', summon('m:z', (1, r(2), d(3)), Nbt({'NoAI': True})))
        # The replace() is because the order isn't defined, either way is good
        self.assertEqual('summon m:z 1 ~2 ^3 {Tags: [t1, t2]}',
                         summon(Entity('m:z', {'Tags': ['t1']}), (1, r(2), d(3)), Nbt({'Tags': ['t2']})).replace(
                             't2, t1', 't1, t2'))

    def test_tag_command(self):
        self.assertEqual('tag @s add foo', tag(s()).add('foo'))
        self.assertEqual('tag @s list', tag(s()).list())
        self.assertEqual('tag @s remove foo', tag(s()).remove('foo'))
        self.assertEqual('$tag $(target) list', tag(Arg('target')).list())

    def test_team_command(self):
        self.assertEqual('team list', team().list())
        self.assertEqual('team list foo', team().list('foo'))
        self.assertEqual('team add foo bar', team().add('foo', 'bar'))
        self.assertEqual('team add foo bar', team().add('foo', 'bar'))
        self.assertEqual('team remove foo', team().remove('foo'))
        self.assertEqual('team remove foo', team().remove('foo'))
        self.assertEqual('team empty foo', team().empty('foo'))
        self.assertEqual('team join foo', team().join('foo'))
        self.assertEqual('team join foo @r', team().join('foo', rand()))
        self.assertEqual('team leave foo @r', team().leave('foo', rand()))
        self.assertEqual('team modify foo displayName bar', team().modify('foo', TeamOption.DISPLAY_NAME, 'bar'))
        self.assertEqual('team modify foo friendlyFire true', team().modify('foo', TeamOption.FRIENDLY_FIRE, True))
        self.assertEqual('team modify foo nametagVisibility hideForOwnTeam',
                         team().modify('foo', TeamOption.NAMETAG_VISIBILITY, HIDE_FOR_OWN_TEAM))
        self.assertEqual('team modify foo deathMessageVisibility hideForOtherTeams',
                         team().modify('foo', TeamOption.DEATH_MESSAGE_VISIBILITY, HIDE_FOR_OTHER_TEAMS))
        self.assertEqual('team modify foo collisionRule pushOwnTeam',
                         team().modify('foo', TeamOption.COLLISION_RULE, PUSH_OWN_TEAM))
        self.assertEqual('team modify foo prefix pre', team().modify('foo', TeamOption.PREFIX, 'pre'))
        self.assertEqual('team modify foo suffix post', team().modify('foo', TeamOption.SUFFIX, 'post'))
        self.assertEqual('$team modify $(t) color $(v)', team().modify(Arg('t'), TeamOption.COLOR, Arg('v')))
        self.assertEqual('$team empty $(team)', team().empty(Arg('team')))
        with self.assertRaises(ValueError):
            team().modify('foo', TeamOption.DISPLAY_NAME, True)
        with self.assertRaises(ValueError):
            team().modify('foo', TeamOption.FRIENDLY_FIRE, 'false')
        with self.assertRaises(ValueError):
            team().modify('foo', TeamOption.NAMETAG_VISIBILITY, 'bar')
        with self.assertRaises(ValueError):
            team().modify('foo', TeamOption.DEATH_MESSAGE_VISIBILITY, 'bar')
        with self.assertRaises(ValueError):
            team().modify('foo', TeamOption.COLLISION_RULE, 'bar')
        with self.assertRaises(ValueError):
            team().modify('foo', TeamOption.PREFIX, True)
        with self.assertRaises(ValueError):
            team().modify('foo', TeamOption.SUFFIX, True)

    def test_teleport_commands(self):
        self.assertEqual('tp @r', str(teleport(rand())))
        self.assertEqual('tp @r @s', str(teleport(rand(), s())))
        self.assertEqual('tp 1 ~2 ^3', str(teleport((1, r(2), d(3)))))
        self.assertEqual('tp @r 1 ~2 ^3', str(teleport(rand(), (1, r(2), d(3)))))
        self.assertEqual('tp @r 1 ~2 ^3 3.4', teleport(rand(), (1, r(2), d(3)), 3.4))
        self.assertEqual('tp @r @s facing 1 ~2 ^3', teleport(rand(), s()).facing((1, r(2), d(3))))
        self.assertEqual('tp @r @s facing entity @a', teleport(rand(), s()).facing(a()))
        self.assertEqual('tp @r @s facing entity @a eyes', teleport(rand(), s()).facing(a(), EYES))
        with self.assertRaises(ValueError):
            teleport((1, 2, 3), None, 2.4)
        with self.assertRaises(ValueError):
            # Target must be singleton
            teleport(e())
        with self.assertRaises(ValueError):
            # Target must be singleton
            teleport(s(), e())
        with self.assertRaises(ValueError):
            tp(e().type(Arg('t')))

    def test_as_single(self):
        self.assertTrue(as_single(p()))
        self.assertTrue(as_single(s()))
        self.assertTrue(as_single(e().limit(1)))
        self.assertTrue(as_single(Arg('t')))
        self.assertTrue(as_single('v$(k)'))
        with self.assertRaises(ValueError):
            as_single(e())

    def test_as_data_target(self):
        self.assertIsNone(as_data_target(None))
        self.assertEqual('block 1 2 3', str(as_data_target((1, 2, 3))))
        self.assertEqual('entity @e[tag=foo]', str(as_data_target(e().tag('foo'))))
        self.assertEqual('storage path', str(as_data_target('path')))
        self.assertEqual('block $(k)', str(as_data_target(block(Arg('k')))))
        self.assertEqual('entity $(k)', str(as_data_target(entity(Arg('k')))))
        self.assertEqual('storage $(k)', str(as_data_target(storage(Arg('k')))))
        with self.assertRaises(ValueError):
            as_data_target('v$(k)')
        with self.assertRaises(ValueError):
            as_data_target(Arg('k'))

    def test_as_position(self):
        self.assertEqual(r(1, 2, 3), as_position(r(1, 2, 3)))
        self.assertEqual((1, 2, 3), as_position((1, 2, 3)))
        self.assertEqual('v$(k)', as_position('v$(k)'))
        self.assertEqual('$(k)', as_position(Arg('k')))
        with self.assertRaises(ValueError):
            as_position(r(1, 2))
        with self.assertRaises(Exception):
            as_position(r(1, (), 3))

    def test_as_user(self):
        self.assertEqual('foo', as_user('foo'))
        self.assertEqual('v$(k)', as_user('v$(k)'))
        self.assertEqual('$(k)', as_user(Arg('k')))
        with self.assertRaises(ValueError):
            as_user(',17')

    def test_as_uuid(self):
        self.assertEqual('a-b-c-d', as_uuid('a-b-c-d'))
        self.assertEqual('v$(k)', as_uuid('v$(k)'))
        self.assertEqual('$(k)', as_uuid(Arg('k')))
        with self.assertRaises(ValueError):
            as_uuid(',17')

    def test_as_team(self):
        self.assertEqual('foo1', as_team('foo1'))
        with self.assertRaises(ValueError):
            as_uuid(',17')
        self.assertEqual('v$(t)', as_team('v$(t)'))
        self.assertEqual('$(t)', as_team(Arg('t')))

    def test_as_block(self):
        self.assertIsNone(as_block(None))
        self.assertEqual(Block('foo'), as_block('foo'))
        self.assertEqual(Block('foo'), as_block(Block('foo')))
        self.assertEqual(Block('foo', {'state': True}, {'nbt': 1}), as_block(('foo', {'state': True}, {'nbt': 1})))
        with self.assertRaises(ValueError):
            as_block(',17')

    def test_as_entity(self):
        self.assertIsNone(as_entity(None))
        self.assertEqual(Entity('foo'), as_entity('foo'))
        self.assertEqual(Entity('foo'), as_entity(Entity('foo')))
        self.assertEqual(Entity('foo', {'nbt': 1}), as_entity(('foo', {'nbt': 1})))
        with self.assertRaises(ValueError):
            as_entity(',17')

    def test_nbt_holder(self):
        self.assertEqual('foo', NbtHolder(name='foo').name)
        self.assertEqual({'front_text': {'messages': [{'text': ''}, {'text': 'Foo'}, {'text': 'Bar'}, {'text': ''}]}},
                         NbtHolder(name='Foo|Bar').sign_nbt())
        self.assertEqual({'back_text': {'messages': [{'text': ''}, {'text': 'Foo'}, {'text': 'Bar'}, {'text': ''}]}},
                         NbtHolder(name='Foo|Bar').sign_nbt(front=False))
        self.assertEqual({'front_text': {'messages': [{'text': ''}, {'text': 'Foo'}, {'text': 'Bar'}, {'text': ''}]},
                          'back_text': {'messages': [{'text': ''}, {'text': 'Foo'}, {'text': 'Bar'}, {'text': ''}]}},
                         NbtHolder(name='Foo|Bar').sign_nbt(front=None))
        with self.assertRaises(ValueError):
            NbtHolder()

    def test_as_slot(self):
        self.assertIsNone(as_slot(None))
        self.assertEqual('foo.1', as_slot('foo.1'))
        with self.assertRaises(ValueError):
            as_slot('foo.12.12')

    def test_as_biome(self):
        self.assertEqual('desert', str(as_biome(BiomeId.DESERT)))
        self.assertEqual('dessert', str(as_biome('dessert')))
        self.assertEqual('$(b)', str(as_biome(Arg('b'))))

    def test_time_command(self):
        self.assertEqual('time add 9', time().add(9))
        self.assertEqual('time add 14d', time().add('14d'))
        self.assertEqual('time query gametime', time().query(GAMETIME))
        self.assertEqual('time set 9', time().set(9))
        self.assertEqual('time set 14d', time().set('14d'))

    def test_title_command(self):
        self.assertEqual('title @s clear', title(s()).clear())
        self.assertEqual('title @s reset', title(s()).reset())
        self.assertEqual('title @s title foo', title(s()).title('foo'))
        self.assertEqual('title @s subtitle foo', title(s()).subtitle('foo'))
        self.assertEqual('title @s actionbar foo', title(s()).actionbar('foo'))
        self.assertEqual('title @s times 1 2 3', title(s()).times(1, 2, 3))
        self.assertEqual('$title $(tgt) title $(t)', title(Arg('tgt')).title(Arg('t')))

    def test_trigger_command(self):
        self.assertEqual('trigger foo', str(trigger('foo')))
        self.assertEqual('trigger foo add 17', trigger('foo').add(17))
        self.assertEqual('trigger foo set 17', trigger('foo').set(17))
        self.assertEqual('trigger foo set 17', trigger('foo').set(17))

    def test_weather_command(self):
        self.assertEqual('weather thunder', weather(THUNDER))
        self.assertEqual('weather rain 17', weather(RAIN, 17))

    def test_worldborder_command(self):
        self.assertEqual('worldborder add 17.3', worldborder().add(17.3))
        self.assertEqual('worldborder add 17.3 9', worldborder().add(17.3, 9))
        self.assertEqual('worldborder center ~1 ^2', worldborder().center((r(1), d(2))))
        self.assertEqual('worldborder get', worldborder().get())
        self.assertEqual('worldborder set 9.2', worldborder().set(9.2))
        self.assertEqual('worldborder damage amount 2.3', worldborder().damage().amount(2.3))
        self.assertEqual('worldborder damage buffer 7.2', worldborder().damage().buffer(7.2))
        self.assertEqual('worldborder warning distance 2.3', worldborder().warning().distance(2.3))
        self.assertEqual('worldborder warning time 5', worldborder().warning().time(5))

    def test_simple_commands(self):
        self.assertEqual('defaultgamemode survival', defaultgamemode(SURVIVAL))
        self.assertEqual('deop @s @a', deop(s(), a()))
        self.assertEqual('difficulty peaceful', difficulty(PEACEFUL))
        self.assertEqual('me howdy', me('howdy'))
        self.assertEqual('op @s', op(s()))
        self.assertEqual('reload', reload())
        self.assertEqual('say hi', say('hi'))
        self.assertEqual('seed', seed())
        self.assertEqual('teammsg hi', teammsg('hi'))
        self.assertEqual('teammsg hi', tm('hi'))
        self.assertEqual('tell @s hi', tell(s(), 'hi'))
        self.assertEqual('tell @s hi', msg(s(), 'hi'))
        self.assertEqual('tell @s hi', w(s(), 'hi'))
        self.assertEqual('tellraw @s {"text": "howdy"}', tellraw(s(), JsonText.text('howdy')))
        self.assertEqual('tellraw @s {"text": "howdy"}', tellraw(s(), {'text': 'howdy'}))
        self.assertEqual('tellraw @s {"text": "howdy"}', tellraw(s(), 'howdy'))

    def test_function(self):
        self.assertEqual('function m:b/c', str(function('m:b/c')))
        self.assertEqual('function foo {foo: bar}', str(function('foo', {'foo': 'bar'})))
        self.assertEqual('function foo with block 1 ~2 ^3', str(function('foo').with_().block((1, r(2), d(3)))))
        self.assertEqual('function foo with entity @e', str(function('foo').with_().entity(e())))
        self.assertEqual('function foo with storage m:b', str(function('foo').with_().storage('m:b')))

    def test_resource_checks(self):
        self.assertEqual('xyzzy', as_resource('xyzzy'))
        self.assertEqual('m:xyzzy', as_resource('m:xyzzy'))
        self.assertEqual('xyzzy', as_resource_path('xyzzy'))
        self.assertEqual('m:xyzzy', as_resource_path('m:xyzzy'))
        self.assertEqual('a/b/c', as_resource_path('a/b/c'))
        self.assertEqual('/a/b/c', as_resource_path('/a/b/c'))
        self.assertEqual('m:a/b/c', as_resource_path('m:a/b/c'))
        self.assertEqual('m:/a/b/c', as_resource_path('m:/a/b/c'))
        self.assertEqual('m:/$(k)/b/c', as_resource_path('m:/$(k)/b/c'))
        self.assertEqual('$(k)', as_resource_path(Arg('k')))
        with self.assertRaises(ValueError):
            as_resource('%')
        with self.assertRaises(ValueError):
            as_resource('m:xyzzy', allow_namespace=False)
        with self.assertRaises(ValueError):
            as_resource_path('/')
        with self.assertRaises(ValueError):
            as_resource_path('a//b')
        with self.assertRaises(ValueError):
            as_resource_path('/a/b: c')
        with self.assertRaises(ValueError):
            as_resource_path('//a/b/c')

    def test_tag_checks(self):
        self.assertEqual('xyzzy', as_name('xyzzy'))
        self.assertEqual('a+b', as_name('a+b'))
        self.assertEqual('!a+b', as_name('!a+b', allow_not=True))
        self.assertEqual(('_', 'b-3'), as_names('_', 'b-3'))
        self.assertEqual(('_', '!b-3'), as_names('_', '!b-3', allow_not=True))
        with self.assertRaises(ValueError):
            as_name('x&y')
        with self.assertRaises(ValueError):
            as_name('!foo')
        with self.assertRaises(ValueError):
            as_names('_', '!b-3')

    def test_commands(self):
        self.assertEqual('help\nhelp foo\nfunction m:b/c', commands(help(), help('foo'), function('m:b/c')))

    def test_expressions(self):
        objective = 'scoreboard objectives add __scratch dummy'
        x = Score('x', 'score')
        y = Score('y', 'score')
        z = Score('z', 'score')
        w = Score('w', 'score')
        self.assertEqual(['scoreboard players operation x score = y score',
                          objective, 'scoreboard players set t00 __scratch -1',
                          'scoreboard players operation x score *= t00 __scratch'], x.set(-y))
        self.assertEqual(['scoreboard players add x score 3'], x.set(x + 3))
        self.assertEqual([objective, 'scoreboard players operation t01 __scratch = x score',
                          'scoreboard players set x score 3',
                          'scoreboard players operation x score += t01 __scratch'], x.set(3 + x))
        self.assertEqual(['scoreboard players add x score 3',
                          'scoreboard players add x score 5'], x.set(x + 3 + 5))
        self.assertEqual(['scoreboard players operation x score += y score'], x.set(x + y))
        self.assertEqual([objective,
                          'scoreboard players operation t01 __scratch = x score',
                          'scoreboard players operation x score = y score',
                          'scoreboard players operation x score += t01 __scratch'], x.set(y + x))
        self.assertEqual(['scoreboard players operation x score = y score',
                          'scoreboard players operation x score += z score'], x.set(y + z))
        self.assertEqual(['scoreboard players operation x score = y score',
                          'scoreboard players operation x score -= z score'], x.set(y - z))
        self.assertEqual(['scoreboard players operation x score = y score',
                          'scoreboard players operation x score += z score',
                          'scoreboard players add x score 3'], x.set(y + z + 3))
        self.assertEqual(['scoreboard players operation x score = y score',
                          'scoreboard players operation x score *= z score',
                          objective,
                          'scoreboard players operation t00 __scratch = w score',
                          'scoreboard players set t01 __scratch 3',
                          'scoreboard players operation t00 __scratch /= t01 __scratch',
                          'scoreboard players operation x score += t00 __scratch'], x.set(y * z + w // 3))
        self.assertEqual(['scoreboard players operation x score = y score',
                          'scoreboard players operation x score *= z score',
                          objective,
                          'scoreboard players operation t00 __scratch = w score',
                          'scoreboard players set t01 __scratch 3',
                          'scoreboard players operation t00 __scratch %= t01 __scratch',
                          'scoreboard players operation x score += t00 __scratch'], x.set(y * z + w % 3))
        self.assertEqual([objective,
                          'execute store result score t00 __scratch run some_cmd',
                          'scoreboard players operation x score += t00 __scratch'], x.set(x + "some_cmd"))

        orig = Expression.scratch_objective()
        try:
            Expression.set_scratch_objective('__foo')
            objective = 'scoreboard objectives add __foo dummy'
            self.assertEqual(['scoreboard players operation x score = y score',
                              objective,
                              'scoreboard players set t00 __foo -1',
                              'scoreboard players operation x score *= t00 __foo'], x.set(-y))
        finally:
            Expression.set_scratch_objective(orig)

    def test_execute_if_scores(self):
        self.assertEqual('execute if entity @e[scores={}]', str(execute().if_().entity(e().scores({}))))
        self.assertEqual('execute if entity @e[scores={o=12}]', str(execute().if_().entity(e().scores({'o': 12}))))
        self.assertEqual('execute if entity @e[scores={o=12}]', str(execute().if_().entity(e().scores({'o': (12,)}))))
        self.assertEqual('execute if entity @e[scores={o=-1..1}]',
                         str(execute().if_().entity(e().scores({'o': (-1, 1)}))))
        self.assertEqual('execute if entity @e[scores={o=!12}]', str(execute().if_().entity(e().scores({'o': '!12'}))))
        self.assertEqual('$execute if entity @e[scores={o=$(v)}]',
                         str(execute().if_().entity(e().scores({'o': Arg('v')}))))
        self.assertEqual('$execute if entity @e[scores={o=1.$(v)}]',
                         str(execute().if_().entity(e().scores({'o': '1.$(v)'}))))
        self.assertEqual('$execute if entity @e[scores={$(o)=1.$(v)}]',
                         str(execute().if_().entity(e().scores({Arg('o'): '1.$(v)'}))))

        self.assertEqual('execute if entity @e[scores={}]', str(execute().if_().entity(e().not_scores({}))))
        self.assertEqual('execute if entity @e[scores={o=!12}]', str(execute().if_().entity(e().not_scores({'o': 12}))))
        self.assertEqual('execute if entity @e[scores={o=!12}]',
                         str(execute().if_().entity(e().not_scores({'o': (12,)}))))
        self.assertEqual('execute if entity @e[scores={o=!-1..1}]',
                         str(execute().if_().entity(e().not_scores({'o': (-1, 1)}))))
        self.assertEqual('$execute if entity @e[scores={o=!$(v)}]',
                         str(execute().if_().entity(e().not_scores({'o': Arg('v')}))))
        self.assertEqual('$execute if entity @e[scores={o=!1.$(v)}]',
                         str(execute().if_().entity(e().not_scores({'o': '1.$(v)'}))))
        self.assertEqual('$execute if entity @e[scores={$(o)=!1.$(v)}]',
                         str(execute().if_().entity(e().not_scores({Arg('o'): '1.$(v)'}))))

    def test_random(self):
        self.assertEqual('random value 1..2', random().value((1, 2)))
        self.assertEqual('random value 1..2 fred', random().value((1, 2), 'fred'))
        self.assertEqual('random roll 1..2', random().roll((1, 2)))
        self.assertEqual('random roll 1..2 fred', random().roll((1, 2), 'fred'))
        self.assertEqual('$random value $(v)..$(k)', random().value((Arg('v'), Arg('k'))))
        self.assertEqual('$random value v$(k)', random().value('v$(k)'))
        self.assertEqual('$random value $(k) $(s)', random().value(Arg('k'), Arg('s')))

        self.assertEqual('random reset *', random().reset('*'))
        self.assertEqual('random reset fred', random().reset('fred'))
        self.assertEqual('random reset fred 123', random().reset('fred', 123))
        self.assertEqual('random reset fred 123 true', random().reset('fred', 123, True))
        self.assertEqual('random reset fred 123 false', random().reset('fred', 123, False))
        self.assertEqual('random reset fred 123 true true', random().reset('fred', 123, True, True))
        self.assertEqual('random reset fred 123 true false', random().reset('fred', 123, True, False))
        self.assertEqual('$random reset $(s) $(v) $(w) $(i)', random().reset(Arg('s'), Arg('v'), Arg('w'), Arg('i')))
        self.assertEqual('$random reset s$(k) $(v) $(w) $(i)', random().reset('s$(k)', Arg('v'), Arg('w'), Arg('i')))

    def test_selector_macros(self):
        self.assertEqual('@a[advancements={$(c)=$(b)}]', str(a().advancements(
            AdvancementCriteria(Arg('c'), Arg('b')))))
        self.assertEqual('@a[advancements={husbandry/wax_on={stuff=$(b)}}]', str(a().advancements(AdvancementCriteria(
            Advancement.WAX_ON, ('stuff', Arg('b'))))))
        self.assertEqual('@a[advancements={husbandry/wax_on={stuff=false},story/smelt_iron={stuff=false}}]',
                         str(a().advancements(
                             AdvancementCriteria(Advancement.WAX_ON, ('stuff', False)),
                             AdvancementCriteria(Advancement.ACQUIRE_HARDWARE, ('stuff', False)))))
        self.assertEqual('@a[advancements={$(c)=$(b)}]', str(a().advancements(
            AdvancementCriteria('$(c)', '$(b)'))))
        self.assertEqual('@a[advancements={k$(c)=v$(b)}]', str(a().advancements(
            AdvancementCriteria('k$(c)', 'v$(b)'))))

        self.assertEqual('@a[dx=$(x),dy=$(y),dz=$(z)]', str(a().volume((Arg('x'), Arg('y'), Arg('z')))))
        self.assertEqual('@a[scores={$(x)=$(xv),$(y)=$(yv)}]',
                         str(a().scores({Arg('x'): Arg('xv'), Arg('y'): Arg('yv')})))
        self.assertEqual('@a[tag=$(t1)]', str(a().tag(Arg('t1'))))
        self.assertEqual('@a[tag=$(t1), tag=$(t2)]', str(a().tag(Arg('t1'), Arg('t2'))))
        self.assertEqual('@a[tag=$(t1), tag=$(t2)]', str(a().tag(Arg('t1')).tag(Arg('t2'))))
        self.assertEqual('@a[tag=!$(t1)]', str(a().not_tag(Arg('t1'))))
        self.assertEqual('@a[tag=!$(t1), tag=!$(t2)]', str(a().not_tag(Arg('t1'), Arg('t2'))))
        self.assertEqual('@a[tag=!$(t1), tag=$(t2)]', str(a().not_tag(Arg('t1')).tag(Arg('t2'))))
        self.assertEqual(
            '@a[x=$(x),y=$(y),z=$(z), distance=$(d), dx=$(dx),dy=$(dy),dz=$(dz), scores={$(s)=$(v)}, tag=$(t), '
            'team=$(tm), sort=$(so), limit=$(li), level=$(lvl), gamemode=$(gm), name=$(n), x_rotation=$(xr), '
            'y_rotation=$(yr), type=$(ty), advancements={$(adv)=$(vadv)}, predicate=$(p)]',
            str(a().pos((Arg('x'), Arg('y'), Arg('z'))).distance(Arg('d')).volume(
                (Arg('dx'), Arg('dy'), Arg('dz'))).scores({Arg('s'): Arg('v')}).tag(Arg('t')).team(Arg('tm')).sort(
                Arg('so')).limit(Arg('li')).level(Arg('lvl')).gamemode(Arg('gm')).name(Arg('n')).x_rotation(
                Arg('xr')).y_rotation(Arg('yr')).type(Arg('ty')).advancements(
                AdvancementCriteria(Arg('adv'), Arg('vadv'))).predicate(Arg('p'))))
        self.assertEqual('$(u)', str(User(Arg('u'))))
