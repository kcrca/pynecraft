from __future__ import annotations

import unittest

from pynecraft.base import DARK_GREEN, GAMETIME, THE_NETHER, d, days, r, seconds, ticks
from pynecraft.commands import *
from pynecraft.commands import _AdvancementCriteria, _AttributeMod, _DataMod, _ExecuteMod, _IfClause, \
    _ScoreboardCriteria, _ScoreboardObjectivesMod, _ScoreboardPlayersMod, _StoreClause


def commands(*cmds: str | Command) -> str:
    """Return a single multiline string for all the commands in the input."""
    return '\n'.join(str(x) for x in cmds)


class TestCommands(unittest.TestCase):

    def test_advancement(self):
        self.assertEqual(advancement(GIVE, s()).everything(), 'advancement grant @s everything')
        self.assertEqual(advancement(GIVE, s()).only(Advancement.A_BALANCED_DIET,
                                                     "pig"), 'advancement grant @s only husbandry/balanced_diet pig')
        self.assertEqual(advancement(GIVE, s()).from_(Advancement.WAX_ON),
                         'advancement grant @s from husbandry/wax_on')
        self.assertEqual(advancement(GIVE, s()).through(Advancement.WAX_ON),
                         'advancement grant @s through husbandry/wax_on')
        self.assertEqual(advancement(GIVE, s()).until(Advancement.WAX_ON),
                         'advancement grant @s until husbandry/wax_on')

        self.assertEqual(advancement(REVOKE, s()).everything(), 'advancement revoke @s everything')
        self.assertEqual(advancement(REVOKE, s()).only(Advancement.A_BALANCED_DIET,
                                                       "pig"),
                         'advancement revoke @s only husbandry/balanced_diet pig')
        self.assertEqual(advancement(REVOKE, s()).from_(Advancement.WAX_ON),
                         'advancement revoke @s from husbandry/wax_on')
        self.assertEqual(advancement(REVOKE, s()).through(Advancement.WAX_ON),
                         'advancement revoke @s through husbandry/wax_on')
        self.assertEqual(advancement(REVOKE, s()).until(Advancement.WAX_ON),
                         'advancement revoke @s until husbandry/wax_on')

    def test_execute(self):
        self.assertEqual(str(execute().align('xz')), 'execute align xz')
        with self.assertRaises(ValueError):
            execute().align('foo')

    def test_uuids(self):
        uuid1 = Uuid(-534823299, 1525499658, -1223897314, -535100990)
        self.assertEqual(Uuid.from_hex('e01f3e7d-5aed-470a-b70c-cf1ee01b01c2'), uuid1)
        self.assertEqual(Uuid.from_most_least(-2297048576818329846, -5256598933532376638), uuid1)
        self.assertEqual(Uuid.from_most_least_dict(
            {'UUIDMost': -2297048576818329846, 'UUIDLeast': -5256598933532376638}), uuid1)
        self.assertEqual(uuid1.ints, (-534823299, 1525499658, -1223897314, -535100990))
        self.assertEqual(uuid1.hex_str, 'e01f3e7d-5aed-470a-b70c-cf1ee01b01c2')
        self.assertEqual(uuid1.most_least, (-2297048576818329846, -5256598933532376638))

        uuid2 = Uuid(14688125, 15550218, 786639, 505086402)
        self.assertEqual(Uuid.from_hex("e01f7d-ed-470a-c-cf1e1b01c2"), uuid2)
        self.assertEqual(uuid2.hex_str, "00e01f7d-00ed-470a-000c-00cf1e1b01c2")

        # Checking the signed-int handling explicitly
        uuid3 = Uuid(-1, -1, 1, 1)
        self.assertEqual(uuid3.ints, (-1, -1, 1, 1))
        self.assertEqual(uuid3.most_least, (-1, 0x100000001))
        self.assertEqual(Uuid.from_most_least(0xfffffffffffffffe, 0x300000004).ints, (-1, -2, 3, 4))

    def test_execute_mod(self):
        self.assertEqual(str(_ExecuteMod().align('xz')), 'align xz')
        self.assertEqual(str(_ExecuteMod().anchored(EYES)), 'anchored eyes')
        self.assertEqual(str(_ExecuteMod().as_(s().tag('robin'))), 'as @s[tag=robin]')
        self.assertEqual(str(_ExecuteMod().at(Uuid(1, 3, 5, 7))), 'at [1, 3, 5, 7]')
        self.assertEqual(str(_ExecuteMod().facing((1, r(2), d(3)))), 'facing 1 ~2 ^3')
        self.assertEqual(str(_ExecuteMod().facing_entity(User('robin'), FEET)), 'facing entity robin feet')
        self.assertEqual(str(_ExecuteMod().in_(THE_NETHER)), 'in the_nether')
        self.assertEqual(str(_ExecuteMod().if_().block((1, r(2), d(3)), 'stone')), 'if block 1 ~2 ^3 stone')
        self.assertEqual(str(_ExecuteMod().unless().block((1, r(2), d(3)), 'stone')), 'unless block 1 ~2 ^3 stone')
        self.assertEqual(str(
            _ExecuteMod().store(RESULT).block((1, r(2), d(3)), '{}', SHORT,
                                              1.3)), 'store result block 1 ~2 ^3 {} short 1.3')
        self.assertEqual(str(_ExecuteMod().run(say('hi'))), 'run say hi')
        with self.assertRaises(ValueError):
            _ExecuteMod().align('foo')
            _ExecuteMod().anchored('foo')
            _ExecuteMod().facing_entity(User('robin'), 'foo')
            _ExecuteMod().in_('foo')
            _ExecuteMod().store().block((1, r(2), d(3)), '{}', 'foo', 1.3)

    def test_run(self):
        self.assertEqual(str(execute().run('foo')), 'execute run foo')
        self.assertEqual(str(execute().run(execute())), 'execute run execute')
        self.assertEqual(str(execute().run(time())), 'execute run time')

    def test_if_clause(self):
        self.assertEqual(str(_IfClause().blocks((1, 2, 3), (4, 5, 6), (7, 8, 9), MASKED)),
                         'blocks 1 2 3 4 5 6 7 8 9 masked')
        self.assertEqual(str(_IfClause().data_block((1, r(2), d(3)), '{}')), 'data block 1 ~2 ^3 {}')
        self.assertEqual(str(_IfClause().data_entity(a(), '{}')), 'data entity @a {}')
        self.assertEqual(str(_IfClause().data_storage('stone', '{}')), 'data storage stone {}')
        self.assertEqual(str(_IfClause().predicate('foo')), 'predicate foo')
        self.assertEqual(str(_IfClause().score(('*', 'bar')).is_(LT, ('up', 'down'))), 'score * bar < up down')
        self.assertEqual(str(_IfClause().score(('*', 'bar')).is_(LT, Score('up', 'down'))), 'score * bar < up down')
        self.assertEqual(str(_IfClause().score(('*', 'bar')).matches((None, 10))), 'score * bar matches ..10')
        self.assertEqual(str(_IfClause().score(('*', 'bar')).matches((1, None))), 'score * bar matches 1..')
        self.assertEqual(str(_IfClause().score(('*', 'bar')).matches(3)), 'score * bar matches 3')
        self.assertEqual(str(_IfClause().score(Score('*', 'bar')).matches(3)), 'score * bar matches 3')
        with self.assertRaises(ValueError):
            _IfClause().score(('foo', 'bar')).matches((None, 10))
            _IfClause().score(('*', 'bar')).is_('foo', ('up', 'down'))
            _IfClause().blocks((1, 2, 3), (4, 5, 6), (7, 8, 9), 'foo')

    def test_store_clause(self):
        self.assertEqual(str(_StoreClause().block((1, r(2), d(3)), '{}', SHORT, 1.3)), 'block 1 ~2 ^3 {} short 1.3')
        self.assertEqual(str(_StoreClause().bossbar('stud', MAX)), 'bossbar stud max')
        self.assertEqual(str(_StoreClause().entity(p(), '{}', FLOAT, 3.5)), 'entity @p {} float 3.5')
        self.assertEqual(str(_StoreClause().score((e(), 'foo'))), 'score @e foo')
        self.assertEqual(str(_StoreClause().score(Score(e(), 'foo'))), 'score @e foo')
        self.assertEqual(str(_StoreClause().storage(s(), '{}', DOUBLE, 1.9)), 'storage @s {} double 1.9')
        with self.assertRaises(ValueError):
            _StoreClause().bossbar('stud', 'foo')
            _StoreClause().entity(p(), '{}', 'foo', 3.5)
            _StoreClause().storage(s(), '{}', 'foo', 1.9)

    def test_range(self):
        self.assertEqual(good_range(3), '3')
        self.assertEqual(good_range((1, 3)), '1..3')
        self.assertEqual(good_range((None, 3)), '..3')
        self.assertEqual(good_range((1, None)), '1..')
        self.assertEqual(good_range((0, None)), '0..')
        self.assertEqual(good_range((None, 0)), '..0')
        self.assertEqual(good_range(0), '0')
        self.assertEqual(good_range(2), '2')

    def test_coords(self):
        self.assertEqual(str(r(1)), '~1')
        self.assertEqual(str(r(-1.5)), '~-1.5')
        self.assertEqual(str(d(1)), '^1')
        self.assertEqual(str(d(-1.5)), '^-1.5')
        self.assertEqual(str(r(1.1) + 2.2), '~3.3')
        self.assertEqual(str(d(1.1) + 2.2), '^3.3')
        self.assertEqual(r(1, 2, 3), (r(1), r(2), r(3)))
        self.assertEqual(d(1, 2, 3), (d(1), d(2), d(3)))

    def test_block(self):
        self.assertEqual(str(Block('stone')), 'stone')
        self.assertEqual(str(Block('m:stone')), 'm:stone')

        self.assertEqual(str(Block('stone', {'a': 17})), 'stone[a=17]')
        self.assertEqual(str(Block('stone', {}, {'a': 17})), 'stone{a: 17}')
        self.assertEqual(str(Block('stone', nbt={'a': 17})), 'stone{a: 17}')
        self.assertEqual(str(Block('stone', {'b': 'c'}, {'a': 17})), 'stone[b=c]{a: 17}')

        self.assertEqual(str(Block('stone').merge_state({'a': 17})), 'stone[a=17]')
        self.assertEqual(str(Block('stone').merge_state({}).merge_nbt({'a': 17})), 'stone{a: 17}')
        self.assertEqual(str(Block('stone').merge_nbt({'a': 17})), 'stone{a: 17}')
        self.assertEqual(str(Block('stone').merge_state({'b': 'c'}).merge_nbt({'a': 17})), 'stone[b=c]{a: 17}')

        self.assertEqual(str(Block('stone').merge_nbt({'a': 17}).merge_nbt({'a': 16, 'b': 'howdy'})),
                         'stone{a: 16, b: howdy}')
        self.assertEqual(str(Block('stone').merge_state({'a': 17}).merge_state({'a': 16, 'b': 'howdy'})),
                         'stone[a=16, b=howdy]')

    def test_entity(self):
        self.assertEqual(str(Entity('bat')), 'bat')
        self.assertEqual(str(Entity('m:bat')), 'm:bat')
        self.assertEqual(str(Entity('bat', nbt={'a': 17})), 'bat{a: 17}')
        self.assertEqual(str(Entity('bat').merge_nbt({'a': 17})), 'bat{a: 17}')
        self.assertEqual(str(Entity('bat').merge_nbt({'a': 17}).merge_nbt({'a': 16, 'b': 'howdy'})),
                         'bat{a: 16, b: howdy}')
        self.assertEqual(Entity('bat').full_id(), 'minecraft:bat')
        self.assertEqual(Entity('minecraft:bat').full_id(), 'minecraft:bat')
        self.assertEqual(Entity('dp:mouse').full_id(), 'dp:mouse')

    def test_json_text(self):
        sort_keys = Nbt.sort_keys
        try:
            Nbt.sort_keys = False
            self.assertEqual(str(JsonText.text('hi')), '{"text": "hi"}')
            self.assertEqual(str(JsonText.text('hi\n')), '{"text": "hi\\n"}')
            self.assertEqual(str(JsonText.html_text('<b><i>hi</i> there</b> friend')), (
                '{"text": [{"text": "hi", "bold": "true", "italic": "true"}, {"text": " there", "bold": "true"},'
                ' {"text": " friend"}]}'))
            self.assertEqual(str(JsonText.translate('m.id', 't1', 't2')),
                             ('{"translate": "m.id", "with": ["t1", "t2"]}'))
            self.assertEqual(str(JsonText.score(Score('sc', 'obj'))), '{"score": {"name": "sc", "objective": "obj"}}')
            self.assertEqual(str(JsonText.score(('sc', 'obj'), 17)),
                             ('{"score": {"name": "sc", "objective": "obj", "value": 17}}'))
            self.assertEqual(str(JsonText.entity(a())), '{"selector": "@a"}')
            self.assertEqual(str(JsonText.entity(a(), RED, '_')), (
                '{"selector": "@a", "separator": {"color": "red", "text": "_"}}'))
            self.assertEqual(str(JsonText.keybind('b.id')), '{"keybind": "b.id"}')
            self.assertEqual(str(JsonText.nbt('m:a/b', a())), '{"nbt": "m:a/b", "entity": "@a"}')
            self.assertEqual(str(JsonText.nbt('m:a/b', (1, r(2), d(3)), interpret=True, separator='_')), (
                '{"nbt": "m:a/b", "block": "1 ~2 ^3", "interpret": true, "separator": "_"}'))
            self.assertEqual(str(JsonText.text('boo').extra()), '{"text": "boo", "extra": []}')
            self.assertEqual(str(JsonText.text('boo').extra('foo', JsonText.text('bar'))), (
                '{"text": "boo", "extra": ["foo", {"text": "bar"}]}'))
            self.assertEqual(str(JsonText.text('boo').color(DARK_GREEN)), '{"text": "boo", "color": "dark_green"}')
            self.assertEqual(str(JsonText.text('boo').font('m:a/b')), '{"text": "boo", "font": "m:a/b"}')
            self.assertEqual(str(JsonText.text('boo').bold()), '{"text": "boo", "bold": true}')
            self.assertEqual(str(JsonText.text('boo').italic()), '{"text": "boo", "italic": true}')
            self.assertEqual(str(JsonText.text('boo').underlined()), '{"text": "boo", "underlined": true}')
            self.assertEqual(str(JsonText.text('boo').strikethrough()), '{"text": "boo", "strikethrough": true}')
            self.assertEqual(str(JsonText.text('boo').obfuscated()), '{"text": "boo", "obfuscated": true}')
            self.assertEqual(str(JsonText.text('boo').insertion('inserted')),
                             '{"text": "boo", "insertion": "inserted"}')

            self.assertEqual(str(JsonText.text('boo').click_event().copy_to_clipboard('ya')), (
                '{"text": "boo", "clickEvent": {"action": "copy_to_clipboard", "value": "ya"}}'))
            self.assertEqual(str(JsonText.text('boo').click_event().open_url('http: a.com')), (
                '{"text": "boo", "clickEvent": {"action": "open_url", "value": "http: a.com"}}'))
            self.assertEqual(str(JsonText.text('boo').click_event().open_file('/a/b')), (
                '{"text": "boo", "clickEvent": {"action": "open_file", "value": "/a/b"}}'))
            self.assertEqual(str(JsonText.text('boo').click_event().change_page('p')), (
                '{"text": "boo", "clickEvent": {"action": "change_page", "value": "p"}}'))
            self.assertEqual(str(JsonText.text('boo').click_event().run_command(say('hi'))), (
                '{"text": "boo", "clickEvent": {"action": "run_command", "value": "/say hi"}}'))
            self.assertEqual(str(JsonText.text('boo').click_event().run_command(say('hi there'))), (
                '{"text": "boo", "clickEvent": {"action": "run_command", "value": "/say hi there"}}'))
            self.assertEqual(str(JsonText.text('boo').click_event().suggest_command('maybe')), (
                '{"text": "boo", "clickEvent": {"action": "suggest_command", "value": "maybe"}}'))

            self.assertEqual(str(JsonText.text('boo').hover_event().show_text('maybe')), (
                '{"text": "boo", "hoverEvent": {"action": "show_text", "contents": "maybe"}}'))
            self.assertEqual(str(JsonText.text('boo').hover_event().show_text(JsonText.text('not'))), (
                ('{"text": "boo", "hoverEvent": {"action": "show_text", "contents": {"text": "not"}}}')))
            self.assertEqual(str(JsonText.text('boo').hover_event().show_item('bundle')), (
                '{"text": "boo", "hoverEvent": {"action": "show_item", "id": "bundle"}}'))
            self.assertEqual(str(JsonText.text('boo').hover_event().show_item('bundle', count=3, tag='tag')), (
                '{"text": "boo", "hoverEvent": {"action": "show_item", "id": "bundle", "count": 3, "tag": "tag"}}'))
            self.assertEqual(str(JsonText.text('boo').hover_event().show_entity('m:z', '5-6-a-f')), (
                '{"text": "boo", "hoverEvent": {"action": "show_entity", "type": "m:z", "id": "5-6-a-f"}}'))
            self.assertEqual(str(JsonText.text('boo').hover_event().show_entity('m:z', '5-6-a-f', 'Robin')), (
                '{"text": "boo", "hoverEvent": {"action": "show_entity", "type": "m:z", "id": "5-6-a-f", "name": "Robin"}}'))
            self.assertEqual(
                str(JsonText.text('boo').hover_event().show_entity('m:z', '5-6-a-f', JsonText.text("ooh"))), (
                    '{"text": "boo", "hoverEvent": {"action": "show_entity", "type": "m:z", "id": "5-6-a-f",'
                    ' "name": {"text": "ooh"}}}'))

            self.assertEqual(str(JsonText.text('boo').extra().color(BLUE).font('m:f').bold().italic().underlined()
                                 .strikethrough().obfuscated().insertion('i').click_event().open_file(
                's').hover_event()
                                 .show_item('bundle').color(GREEN)), (
                                 '{"text": "boo", "extra": [], "color": "green", "font": "m:f", "bold": true, '
                                 '"italic": true, "underlined": true, "strikethrough": true, "obfuscated": '
                                 'true, "insertion": "i", "clickEvent": {"action": "open_file", "value": "s"}, '
                                 '"hoverEvent": {"action": "show_item", "id": "bundle"}}'))

            # The sign's Text1, etc., keys always contain json text, check that this works
            self.assertEqual(str(Nbt({'Text2': 'howdy'})), '{Text2: \'"howdy"\'}')
            self.assertEqual(str(Nbt({'Text2': {'text': 'boo'}})), '{Text2: \'{"text": "boo"}\'}')
        finally:
            Nbt.sort_keys = sort_keys

    def test_known_targets(self):
        self.assertEqual(str(p()), '@p')
        self.assertEqual(str(random()), '@r')
        self.assertEqual(str(a()), '@a')
        self.assertEqual(str(e()), '@e')
        self.assertEqual(str(Star()), '*')

    def test_score(self):
        self.assertEqual(str(Score(Star(), 'foo')), '* foo')
        self.assertEqual(str(Score(a(), 'bar')), '@a bar')

    def test_good_score(self):
        self.assertIsNone(good_score(None))
        self.assertEqual(good_score(Score(a(), 'bar')), Score(a(), 'bar'))
        self.assertEqual(good_score((a(), 'bar')), Score(a(), 'bar'))
        self.assertEqual(good_score(('foo', 'bar')), Score('foo', 'bar'))

    def test_target_pos(self):
        self.assertEqual(str(a().pos((1, 2, 3))), '@a[x=1,y=2,z=3]')
        with self.assertRaises(KeyError):
            a().pos((1, 2, 3)).pos((4, 5, 6))

    def test_target_distance(self):
        self.assertEqual(str(a().distance(3)), '@a[distance=3]')
        self.assertEqual(str(a().distance((1, 3))), '@a[distance=1..3]')
        self.assertEqual(str(a().distance((None, 3))), '@a[distance=..3]')
        self.assertEqual(str(a().distance((1, None))), '@a[distance=1..]')
        with self.assertRaises(KeyError):
            a().distance(3).distance(4)

    def test_target_delta(self):
        self.assertEqual(str(a().volume((1, 2, 3))), '@a[dx=1,dy=2,dz=3]')
        with self.assertRaises(KeyError):
            a().volume((1, 2, 3)).volume((4, 5, 6))

    def test_target_scores(self):
        self.assertEqual(str(a().scores('x=1', 'y=..3')), '@a[score_specs={x=1,y=..3}]')
        with self.assertRaises(KeyError):
            a().scores('x=1').scores('y=..3')

    def test_target_tag(self):
        self.assertEqual(str(a().tag('foo')), '@a[tag=foo]')
        self.assertEqual(str(a().tag('foo', 'bar')), '@a[tag=foo, tag=bar]')
        self.assertEqual(str(a().tag('foo').tag('bar')), '@a[tag=foo, tag=bar]')

    def test_target_team(self):
        self.assertEqual(str(a().team('foo')), '@a[team=foo]')
        with self.assertRaises(KeyError):
            a().team('foo').team('bar')

    def test_target_not_teams(self):
        self.assertEqual(str(a().not_team('foo')), '@a[team=!foo]')
        self.assertEqual(str(a().not_team('foo', 'bar')), '@a[team=!foo, team=!bar]')
        self.assertEqual(str(a().not_team('foo', '!bar')), '@a[team=!foo, team=!bar]')
        self.assertEqual(str(a().not_team('foo').not_team('bar')), '@a[team=!foo, team=!bar]')
        self.assertEqual(str(a().not_team('foo').not_team('!bar')), '@a[team=!foo, team=!bar]')
        with self.assertRaises(KeyError):
            a().team('foo').not_team('bar')

    def test_target_sort(self):
        self.assertEqual(str(a().sort(NEAREST)), '@a[sort=nearest]')
        with self.assertRaises(KeyError):
            a().sort(NEAREST).sort(RANDOM)
            a().sort('foo')

    def test_target_limit(self):
        self.assertEqual(str(a().limit(1)), '@a[limit=1]')
        with self.assertRaises(KeyError):
            a().limit(1).limit(2)

    def test_target_level(self):
        self.assertEqual(str(a().level(3)), '@a[level=3]')
        self.assertEqual(str(a().level((1, 3))), '@a[level=1..3]')
        with self.assertRaises(KeyError):
            a().level(3).level(4)

    def test_target_gamemode(self):
        self.assertEqual(str(a().gamemode(SURVIVAL)), '@a[gamemode=survival]')
        with self.assertRaises(KeyError):
            a().gamemode(CREATIVE).gamemode(ADVENTURE)
            a().gamemode('foo')

    def test_target_not_gamemodes(self):
        self.assertEqual(str(a().not_gamemode(SURVIVAL)), '@a[gamemode=!survival]')
        self.assertEqual(str(
            a().not_gamemode(SURVIVAL,
                             CREATIVE)), '@a[gamemode=!survival, gamemode=!creative]')
        with self.assertRaises(KeyError):
            a().gamemode(CREATIVE).not_gamemode(ADVENTURE)
            a().not_gamemode('foo')

    def test_target_name(self):
        self.assertEqual(str(a().name('foo')), '@a[name=foo]')
        with self.assertRaises(KeyError):
            a().name('foo').name('bar')

    def test_target_not_names(self):
        self.assertEqual(str(a().not_name('foo')), '@a[name=!foo]')
        self.assertEqual(str(a().not_name('foo', 'bar')), '@a[name=!foo, name=!bar]')
        self.assertEqual(str(a().not_name('foo', '!bar')), '@a[name=!foo, name=!bar]')
        self.assertEqual(str(a().not_name('foo').not_name('bar')), '@a[name=!foo, name=!bar]')
        self.assertEqual(str(a().not_name('foo').not_name('!bar')), '@a[name=!foo, name=!bar]')
        with self.assertRaises(KeyError):
            a().name('foo').not_name('bar')

    def test_target_x_rotation(self):
        self.assertEqual(str(a().x_rotation(1.5)), '@a[x_rotation=1.5]')
        with self.assertRaises(KeyError):
            a().x_rotation(1.5).x_rotation(1.5)

    def test_target_y_rotation(self):
        self.assertEqual(str(a().y_rotation(1.5)), '@a[y_rotation=1.5]')
        with self.assertRaises(KeyError):
            a().y_rotation(1.5).y_rotation(1.5)

    def test_target_type(self):
        self.assertEqual(str(a().type('creeper')), '@a[type=creeper]')
        with self.assertRaises(KeyError):
            a().type('creeper').type('bat')

    def test_target_not_types(self):
        self.assertEqual(str(a().not_type('foo')), '@a[type=!foo]')
        self.assertEqual(str(a().not_type('foo', 'bar')), '@a[type=!foo, type=!bar]')
        self.assertEqual(str(a().not_type('foo', '!bar')), '@a[type=!foo, type=!bar]')
        self.assertEqual(str(a().not_type('foo').not_type('bar')), '@a[type=!foo, type=!bar]')
        self.assertEqual(str(a().not_type('foo').not_type('!bar')), '@a[type=!foo, type=!bar]')
        with self.assertRaises(KeyError):
            a().type('foo').not_type('bar')

    def test_target_nbt(self):
        self.assertEqual(str(a().nbt({'a': 17})), '@a[nbt={a: 17}]')
        self.assertEqual(str(a().nbt({'a': 17}, {'b': 'hi there'})), '@a[nbt={a: 17}, nbt={b: "hi there"}]')
        self.assertEqual(str(a().nbt({'a': 17}).nbt({'b': 'hi there'})), '@a[nbt={a: 17}, nbt={b: "hi there"}]')

    def test_target_advancements(self):
        self.assertEqual(str(a().advancements(
            _AdvancementCriteria(Advancement.WAX_ON, True))), '@a[advancements={husbandry/wax_on=true}]')
        self.assertEqual(str(a().advancements(_AdvancementCriteria(
            Advancement.WAX_ON, ('stuff', False)))), '@a[advancements={husbandry/wax_on={stuff=false}}]')

    def test_target_predicate(self):
        self.assertEqual(str(a().predicate('foo')), '@a[predicate=foo]')
        self.assertEqual(str(a().predicate('foo', 'bar')), '@a[predicate=foo, predicate=bar]')
        self.assertEqual(str(a().predicate('foo').predicate('bar')), '@a[predicate=foo, predicate=bar]')

    def test_target_chainability(self):
        self.assertEqual(str(
            a().pos((1, 2, 3)).distance((None, 15.5)).volume((4.4, 5.5, 6.6)).scores().tag("one").team('slug').sort(
                ARBITRARY).limit(15).level((3, 15)).gamemode(SURVIVAL).name('Robin').x_rotation(
                9).y_rotation((None, 24)).type('cougar').nbt({"hi": "there"}).advancements(
                _AdvancementCriteria(Advancement.A_SEEDY_PLACE, True)).predicate(
                "nada")), '@a[x=1,y=2,z=3, distance=..15.5, dx=4.4,dy=5.5,dz=6.6, score_specs={}, tag=one, team=slug, '
                          'sort=arbitrary, limit=15, level=3..15, gamemode=survival, name=Robin, x_rotation=9, '
                          'y_rotation=..24, type=cougar, nbt={hi: there}, advancements={husbandry/plant_seed=true}, '
                          'predicate=nada]')
        self.assertEqual(str(a().not_team('Raiders').not_name("GRBX").not_gamemode(CREATIVE)
                             .not_type("worm")), '@a[team=!Raiders, name=!GRBX, gamemode=!creative, type=!worm]')

    def test_comment(self):
        long_line = 'This is a long line of text that would be wrapped if it were asked to be wrapped, and we use it to' \
                    ' test if wrapping does or does not happen.'
        self.assertEqual(str(comment('hi')), '# hi')
        self.assertEqual(str(comment(' hi ')), '# hi')
        self.assertEqual(str(comment('hi\nthere')), '# hi\n# there')
        self.assertEqual(str(comment('  hi\nthere  ')), '# hi\n# there')
        self.assertEqual(str(comment(long_line)), f'# {long_line}')
        self.assertEqual(str(comment(long_line + '\n\n\n' + long_line)), f'# {long_line}\n#\n#\n# {long_line}')

        self.assertEqual(str(comment('hi')), '# hi')
        self.assertEqual(str(comment(' hi ')), '# hi')
        self.assertEqual(str(comment('hi\nthere')), '# hi\n# there')
        self.assertEqual(str(comment('  hi\nthere  ', wrap=True)), '# hi there')
        self.assertEqual(str(comment(long_line, wrap=True)), (
            '# This is a long line of text that would be wrapped if it were asked to be\n# wrapped, and we use it to test'
            ' if wrapping does or does not happen.'))
        self.assertEqual(str(comment(long_line + '\n\n\n' + long_line, wrap=True)), (
            '# This is a long line of text that would be wrapped if it were asked to be\n'
            '# wrapped, and we use it to test if wrapping does or does not happen.\n'
            '#\n'
            '# This is a long line of text that would be wrapped if it were asked to be\n'
            '# wrapped, and we use it to test if wrapping does or does not happen.'))

    def test_literal(self):
        self.assertEqual(str(literal('xyzzy')), 'xyzzy')

    def test_attribute(self):
        self.assertEqual(attribute(s(), 'foo').get(), 'attribute @s foo get')

    def test_attribute_act(self):
        self.assertEqual(str(_AttributeMod().get()), 'get')
        self.assertEqual(str(_AttributeMod().get(1.2)), 'get 1.2')
        self.assertEqual(str(_AttributeMod().base().get()), 'base get')
        self.assertEqual(str(_AttributeMod().base().get(1.2)), 'base get 1.2')
        self.assertEqual(str(_AttributeMod().base().set(1.2)), 'base set 1.2')
        self.assertEqual(str(_AttributeMod().modifier().add('1-2-3-f', 'robin', 1.3)),
                         'modifier add 1-2-3-f "robin" 1.3')
        self.assertEqual(str(_AttributeMod().modifier().remove('1-2-3-f')), 'modifier remove 1-2-3-f')
        self.assertEqual(str(_AttributeMod().modifier().value('1-2-3-f')), 'modifier value get 1-2-3-f')
        self.assertEqual(str(_AttributeMod().modifier().value('1-2-3-f', 1.3)), 'modifier value get 1-2-3-f 1.3')

    def test_bossbar(self):
        self.assertEqual(bossbar().add('foo', 'stud'), 'bossbar add foo stud')
        self.assertEqual(bossbar().list(), 'bossbar list')
        self.assertEqual(bossbar().remove('foo'), 'bossbar remove foo')

        self.assertEqual(bossbar().get('foo').color(), 'bossbar get foo color')
        self.assertEqual(bossbar().get('foo').max(), 'bossbar get foo max')
        self.assertEqual(bossbar().get('foo').name(), 'bossbar get foo name')
        self.assertEqual(bossbar().get('foo').players(), 'bossbar get foo players')
        self.assertEqual(bossbar().get('foo').style(), 'bossbar get foo style')
        self.assertEqual(bossbar().get('foo').value(), 'bossbar get foo value')
        self.assertEqual(bossbar().get('foo').visible(), 'bossbar get foo visible')

        self.assertEqual(bossbar().set('foo').color(BLUE), 'bossbar set foo color blue')
        self.assertEqual(bossbar().set('foo').max(17), 'bossbar set foo max 17')
        self.assertEqual(bossbar().set('foo').name('Libby the Kid'), 'bossbar set foo name "Libby the Kid"')
        self.assertEqual(bossbar().set('foo').players(s()), 'bossbar set foo players @s')
        self.assertEqual(bossbar().set('foo').style(NOTCHED_12), 'bossbar set foo style notched_12')
        self.assertEqual(bossbar().set('foo').value(17), 'bossbar set foo value 17')
        self.assertEqual(bossbar().set('foo').visible(False), 'bossbar set foo visible false')

    def test_clear(self):
        self.assertEqual(clear(s()).item('foo{bar}'), 'clear @s foo{bar}')
        self.assertEqual(clear(s()).item('foo{bar}', 4), 'clear @s foo{bar} 4')

    def test_clone(self):
        self.assertEqual(clone((1, r(2), d(3)), (4, 5, 6), (7, 8, 9)).replace(), 'clone 1 ~2 ^3 4 5 6 7 8 9 replace')
        self.assertEqual(clone((1, r(2), d(3)), (4, 5, 6), (7, 8, 9)).masked(FORCE),
                         'clone 1 ~2 ^3 4 5 6 7 8 9 masked force')
        self.assertEqual(clone((1, r(2), d(3)), (4, 5, 6), (7, 8, 9)).filtered('stone', FORCE),
                         'clone 1 ~2 ^3 4 5 6 7 8 9 filtered stone force')

    def test_data_target(self):
        self.assertEqual(data_target_str((1, r(2), d(3))), 'block 1 ~2 ^3')
        self.assertEqual(data_target_str(s()), 'entity @s')
        self.assertEqual(data_target_str('m:/a/b'), 'storage m:/a/b')

    def test_data(self):
        self.assertEqual(data().get(s()), 'data get entity @s')

    def test_effect(self):
        self.assertEqual(effect().give(s(), Effect.SPEED), 'effect give @s speed')
        self.assertEqual(effect().give(s(), Effect.SPEED, 100), 'effect give @s speed 100')
        self.assertEqual(effect().give(s(), Effect.SPEED, 100, 2), 'effect give @s speed 100 2')
        self.assertEqual(effect().give(s(), Effect.SPEED, 100, 2, True), 'effect give @s speed 100 2 true')
        self.assertEqual(effect().clear(), 'effect clear')
        self.assertEqual(effect().clear(s()), 'effect clear @s')
        self.assertEqual(effect().clear(s(), Effect.SPEED), 'effect clear @s speed')
        with self.assertRaises(ValueError):
            effect().give(s(), Effect.SPEED, -1)
            effect().give(s(), Effect.SPEED, MAX_EFFECT_SECONDS + 100)
            effect().give(s(), Effect.SPEED, None, 2)
            effect().give(s(), Effect.SPEED, None, None, True)
            effect().give(s(), Effect.SPEED, 100, None, True)
            effect().clear(None, Effect.SPEED)

    def test_enchant(self):
        self.assertEqual(enchant(s(), Enchantment.LURE), 'enchant @s lure')
        self.assertEqual(enchant(s(), Enchantment.LURE, 2), 'enchant @s lure 2')
        self.assertEqual(enchant(s(), 12), 'enchant @s 12')
        self.assertEqual(enchant(s(), 12, 2), 'enchant @s 12 2')
        with self.assertRaises(ValueError):
            enchant(s(), Enchantment.LURE, 17)

    def test_experience(self):
        self.assertEqual(experience().add(s(), 3, LEVELS), 'experience add @s 3 levels')
        self.assertEqual(experience().add(s(), 3, POINTS), 'experience add @s 3 points')
        self.assertEqual(experience().set(s(), 3, LEVELS), 'experience set @s 3 levels')
        self.assertEqual(experience().set(s(), 3, POINTS), 'experience set @s 3 points')
        self.assertEqual(experience().query(s(), POINTS), 'experience query @s points')
        self.assertEqual(xp().query(s(), POINTS), 'experience query @s points')

    def test_fill(self):
        self.assertEqual(str(fill((1, r(2), d(3)), (4, 5, 6), 'stone').hollow()), 'fill 1 ~2 ^3 4 5 6 stone hollow')
        self.assertEqual(str(fill((1, r(2), d(3)), (4, 5, 6), 'stone').replace()), 'fill 1 ~2 ^3 4 5 6 stone replace')
        self.assertEqual(fill((1, r(2), d(3)), (4, 5, 6), 'stone').replace('air'),
                         'fill 1 ~2 ^3 4 5 6 stone replace air')

    def test_data_mod(self):
        self.assertEqual(str(_DataMod().get(a())), 'get entity @a')
        self.assertEqual(str(_DataMod().merge(a(), {})), 'merge entity @a {}')
        self.assertEqual(str(_DataMod().modify(a(), 'a.b')), 'modify entity @a a.b')
        self.assertEqual(str(_DataMod().modify(a(), 'a.b').append().from_(
            'm:b', 'Name')), 'modify entity @a a.b append from storage m:b Name')
        self.assertEqual(str(
            _DataMod().modify(a(), 'a.b').insert(3).value(
                'hi there')), 'modify entity @a a.b insert 3 value "hi there"')
        self.assertEqual(str(
            _DataMod().modify(a(), 'x').merge().value('hi there')), 'modify entity @a x merge value "hi there"')
        self.assertEqual(str(
            _DataMod().modify(a(), 'x').prepend().value(
                'hi there')), 'modify entity @a x prepend value "hi there"')
        self.assertEqual(str(
            _DataMod().modify(a(), 'x').set().value('hi there')), 'modify entity @a x set value "hi there"')
        self.assertEqual(str(_DataMod().remove(a(), 'x')), 'remove entity @a x')
        with self.assertRaises(ValueError):
            _DataMod().get((1, r(2), d(3)), None, 2.2)

    def test_datapack(self):
        self.assertEqual(str(datapack().disable('robin')), 'datapack disable robin')
        self.assertEqual(str(datapack().enable('robin')), 'datapack enable robin')
        self.assertEqual(datapack().enable('robin').first(), 'datapack enable robin first')
        self.assertEqual(datapack().enable('robin').before('kelly'), 'datapack enable robin before kelly')

    def test_forceload(self):
        self.assertEqual(forceload().add((1, r(2))), 'forceload add 1 ~2')
        self.assertEqual(forceload().add((1, r(2)), (4, 5)), 'forceload add 1 ~2 4 5')
        self.assertEqual(forceload().remove((1, r(2))), 'forceload remove 1 ~2')
        self.assertEqual(forceload().remove((1, r(2)), (4, 5)), 'forceload remove 1 ~2 4 5')
        self.assertEqual(forceload().remove_all(), 'forceload remove all')
        self.assertEqual(forceload().query(), 'forceload query')
        self.assertEqual(forceload().query((1, r(2))), 'forceload query 1 ~2')

    def test_gamemode(self):
        self.assertEqual(gamemode(SURVIVAL), 'gamemode survival')
        self.assertEqual(gamemode(SURVIVAL, s()), 'gamemode survival @s')

    def test_gamerule(self):
        self.assertEqual(gamerule(GameRule.DISABLE_RAIDS), 'gamerule disableRaids')
        self.assertEqual(gamerule(GameRule.DISABLE_RAIDS, True), 'gamerule disableRaids true')
        self.assertEqual(gamerule(GameRule.MAX_COMMAND_CHAIN_LENGTH, 13), 'gamerule maxCommandChainLength 13')
        self.assertEqual(gamerule('disableRaids', True), 'gamerule disableRaids true')
        with self.assertRaises(ValueError):
            gamerule(GameRule.DISABLE_RAIDS, 17)
            gamerule(GameRule.MAX_COMMAND_CHAIN_LENGTH, True)
            gamerule('nothing', 17)

    def test_give(self):
        self.assertEqual(give(s(), 'foo'), 'give @s foo')
        self.assertEqual(give(s(), 'foo', 17), 'give @s foo 17')

    def test_help(self):
        self.assertEqual(help(), 'help')
        self.assertEqual(help('foo'), 'help foo')

    def test_item(self):
        self.assertEqual(str(item().modify().block((1, r(2), d(3)), 'a.17')), 'item modify block 1 ~2 ^3 a.17')
        self.assertEqual(str(item().modify().block((1, r(2), d(3)), 'a.17', 'm:a')),
                         'item modify block 1 ~2 ^3 a.17 m:a')
        self.assertEqual(str(item().modify().entity(s(), 'a.17')), 'item modify entity @s a.17')
        self.assertEqual(str(item().modify().entity(s(), 'a.17', 'm:a')), 'item modify entity @s a.17 m:a')
        self.assertEqual(str(item().replace().entity(s(), 'a.17').with_('a{b}')),
                         'item replace entity @s a.17 with a{b}')
        self.assertEqual(str(
            item().replace().entity(s(), 'a.17').with_('a{b}', 2)), 'item replace entity @s a.17 with a{b} 2')
        self.assertEqual(str(item().replace().entity(s(), 'a.17').from_().block((1, r(2), d(3)),
                                                                                'a.17')),
                         'item replace entity @s a.17 from block 1 ~2 ^3 a.17')
        self.assertEqual(str(item().replace().entity(s(), 'a.17').from_().block((1, r(2), d(3)), 'a.17',
                                                                                'm:a')),
                         'item replace entity @s a.17 from block 1 ~2 ^3 a.17 m:a')
        self.assertEqual(str(item().replace().entity(s(), 'a.17').from_().entity(p(),
                                                                                 'a.17')),
                         'item replace entity @s a.17 from entity @p a.17')
        self.assertEqual(str(item().replace().entity(s(), 'a.17').from_().entity(p(), 'a.17',
                                                                                 'm:a')),
                         'item replace entity @s a.17 from entity @p a.17 m:a')
        self.assertEqual(str(item().replace().block((1, r(2), d(3)), 'a:b')), 'item replace block 1 ~2 ^3 a:b')
        self.assertEqual(str(
            item().replace().block((1, r(2), d(3)), 'a:b').with_('air')), 'item replace block 1 ~2 ^3 a:b with air')
        self.assertEqual(str(item().replace().block
                             ((1, r(2), d(3)), 'a:b').from_().entity(s(),
                                                                     'b')),
                         'item replace block 1 ~2 ^3 a:b from entity @s b')
        with self.assertRaises(ValueError):
            item().replace().block((1, r(2), d(3)), 'a.17', 'm:a')
            item().replace().entity(s(), 'a.17', 'm:a')

    def test_kill_command(self):
        self.assertEqual(kill(), 'kill')
        self.assertEqual(kill(s()), 'kill @s')

    def test_list_command(self):
        self.assertEqual(str(list_()), 'list')
        self.assertEqual(list_().uuids(), 'list uuids')

    def test_locate_command(self):
        self.assertEqual(locate(STRUCTURE, 'foo'), 'locate structure foo')
        self.assertEqual(locate(BIOME, 'foo'), 'locate biome foo')
        self.assertEqual(locate(POI, 'foo'), 'locate poi foo')

    def test_loot_command(self):
        self.assertEqual(loot().give(a()).fish('m:/a/b', (1, r(2), d(3)),
                                               'stone'), 'loot give @a fish m:/a/b 1 ~2 ^3 stone')
        self.assertEqual(loot().insert((1, r(2), d(3))).loot('m:/a/b'), 'loot insert 1 ~2 ^3 loot m:/a/b')
        self.assertEqual(loot().spawn((1, r(2), d(3))).kill(p()), 'loot spawn 1 ~2 ^3 kill @p')
        self.assertEqual(loot().replace().block((1, r(2), d(3)), 13).mine((4, r(5), d(6)), MAINHAND), (
            'loot replace block 1 ~2 ^3 13 mine 4 ~5 ^6 mainhand'))
        self.assertEqual(loot().replace().block((1, r(2), d(3)), 13, 2).kill(
            p()), 'loot replace block 1 ~2 ^3 13 2 kill @p')
        self.assertEqual(loot().replace().entity(a(), 12).kill(
            p()), 'loot replace entity @a 12 kill @p')
        self.assertEqual(loot().replace().entity(a(), 12, 3).kill(
            p()), 'loot replace entity @a 12 3 kill @p')

    def test_particle_command(self):
        self.assertEqual(particle(Particle.ASH), 'particle ash')
        self.assertEqual(particle(Particle.ASH, (1, r(2), d(3))), 'particle ash 1 ~2 ^3')
        self.assertEqual(particle(Particle.ASH, (1, r(2), d(3)), (4, r(5), d(6)), 2.1, 15, FORCE), (
            'particle ash 1 ~2 ^3 4 ~5 ^6 2.1 15 force'))

    def test_place(self):
        self.assertEqual(place().feature('m:b'), 'place feature m:b')
        self.assertEqual(place().feature('m:b', (1, r(2), d(3))), 'place feature m:b 1 ~2 ^3')
        self.assertEqual(place().jigsaw('m:a', 'm:b', 7), 'place jigsaw m:a m:b 7')
        self.assertEqual(place().jigsaw('m:a', 'm:b', 7, (1, r(2), d(3))), 'place jigsaw m:a m:b 7 1 ~2 ^3')
        self.assertEqual(place().structure('m:b'), 'place structure m:b')
        self.assertEqual(place().structure('m:b', (1, r(2), d(3))), 'place structure m:b 1 ~2 ^3')

    def test_playsound(self):
        self.assertEqual(playsound('m:s', 'm:a', s()), 'playsound m:s m:a @s')
        self.assertEqual(playsound('m:s', 'm:a', s(), (1, r(2), d(3))), 'playsound m:s m:a @s 1 ~2 ^3')
        self.assertEqual(playsound('m:s', 'm:a', s(), (1, r(2), d(3)), 1.2), 'playsound m:s m:a @s 1 ~2 ^3 1.2')
        self.assertEqual(playsound('m:s', 'm:a', s(), (1, r(2), d(3)), 1.2,
                                   17.9), 'playsound m:s m:a @s 1 ~2 ^3 1.2 17.9')
        self.assertEqual(playsound('m:s', 'm:a', s(), (1, r(2), d(3)), 1.2, 17.9,
                                   1.0), 'playsound m:s m:a @s 1 ~2 ^3 1.2 17.9 1.0')

    def test_recipe(self):
        self.assertEqual(recipe(GIVE, s(), '*'), 'recipe give @s *')
        self.assertEqual(recipe(GIVE, s(), 'm:/a/b'), 'recipe give @s m:/a/b')

    def test_scoreboard(self):
        self.assertEqual(scoreboard().objectives().add('obj', ScoreCriteria.FOOD),
                         'scoreboard objectives add obj food')
        self.assertEqual(_ScoreboardObjectivesMod().list(), 'list')
        self.assertEqual(_ScoreboardObjectivesMod().add('obj', ScoreCriteria.FOOD), 'add obj food')
        self.assertEqual(_ScoreboardObjectivesMod().add('obj', ScoreCriteria.FOOD, 'howdy'), 'add obj food howdy')
        self.assertEqual(_ScoreboardObjectivesMod().add('obj', ScoreCriteria.AIR), 'add obj air')
        self.assertEqual(_ScoreboardObjectivesMod().remove('obj'), 'remove obj')
        self.assertEqual(_ScoreboardObjectivesMod().setdisplay(SIDEBAR), 'setdisplay sidebar')
        self.assertEqual(_ScoreboardObjectivesMod().setdisplay(SIDEBAR_TEAM + 'blue', 'obj'),
                         'setdisplay sidebar.team.blue obj')
        self.assertEqual(_ScoreboardObjectivesMod().modify('obj', DISPLAY_NAME, 'fred'), 'modify obj displayname fred')
        self.assertEqual(_ScoreboardObjectivesMod().modify('obj', RENDER_TYPE, HEARTS), 'modify obj rendertype hearts')
        self.assertEqual(str(scoreboard().players().enable((Star(), 'obj'))), 'scoreboard players enable * obj')
        self.assertEqual(str(scoreboard().players().enable(Score(Star(), 'obj'))), 'scoreboard players enable * obj')
        self.assertEqual(_ScoreboardPlayersMod().list(Star()), 'list *')
        self.assertEqual(_ScoreboardPlayersMod().get((a(), 'obj')), 'get @a obj')
        self.assertEqual(_ScoreboardPlayersMod().get(Score(a(), 'obj')), 'get @a obj')
        self.assertEqual(_ScoreboardPlayersMod().set((User('robin'), 'obj'), 12), 'set robin obj 12')
        self.assertEqual(_ScoreboardPlayersMod().set(Score(User('robin'), 'obj'), 12), 'set robin obj 12')
        self.assertEqual(_ScoreboardPlayersMod().add((a(), 'obj'), 12), 'add @a obj 12')
        self.assertEqual(_ScoreboardPlayersMod().add(Score(a(), 'obj'), 12), 'add @a obj 12')
        self.assertEqual(_ScoreboardPlayersMod().remove((a(), 'obj'), 12), 'remove @a obj 12')
        self.assertEqual(_ScoreboardPlayersMod().remove(Score(a(), 'obj'), 12), 'remove @a obj 12')
        self.assertEqual(_ScoreboardPlayersMod().enable(Score(a(), 'obj')), 'enable @a obj')
        self.assertEqual(_ScoreboardPlayersMod().operation((Star(), 'obj'), PLUS,
                                                           Score(random(), 'obj2')), 'operation * obj += @r obj2')
        self.assertEqual(_ScoreboardPlayersMod().operation(Score(Star(), 'obj'), PLUS,
                                                           Score(random(), 'obj2')), 'operation * obj += @r obj2')

        self.assertEqual(_ScoreboardPlayersMod().reset((a(), 'obj')), 'reset @a obj')
        self.assertEqual(_ScoreboardPlayersMod().reset(Score(a(), 'obj')), 'reset @a obj')
        self.assertEqual(_ScoreboardPlayersMod().reset((a())), 'reset @a')
        self.assertEqual(_ScoreboardPlayersMod().reset((a(), None)), 'reset @a')
        self.assertEqual(_ScoreboardPlayersMod().reset(a()), 'reset @a')
        self.assertEqual(_ScoreboardPlayersMod().reset('fred'), 'reset fred')

    def test_scoreboard_criteria(self):
        self.assertEqual(str(_ScoreboardCriteria(ScoreCriteria.AIR)), 'air')
        self.assertEqual(str(_ScoreboardCriteria('has', ScoreCriteria.AIR)), 'has.air')
        self.assertEqual(str(_ScoreboardCriteria('killed_by', 'm:zombie')), 'killed_by.m:zombie')
        self.assertEqual(str(_ScoreboardCriteria('on', 'team', 'purple')), 'on.team.purple')

    def test_publish_command(self):
        self.assertEqual(publish(), 'publish')
        self.assertEqual(publish(17), 'publish 17')

    def test_schedule_command(self):
        self.assertEqual(schedule().function('m:b/c', days(1.3), APPEND), 'schedule function m:b/c 1.3d append')
        self.assertEqual(schedule().function('m:b/c', seconds(2.3), REPLACE), 'schedule function m:b/c 2.3s replace')
        self.assertEqual(schedule().function('m:b/c', ticks(9), REPLACE), 'schedule function m:b/c 9 replace')
        self.assertEqual(schedule().function('m:b/c', 3, REPLACE), 'schedule function m:b/c 3 replace')
        self.assertEqual(schedule().clear('m:b/c'), 'schedule clear m:b/c')
        with self.assertRaises(ValueError):
            schedule().function('m:b/c', 'hi', REPLACE)

    def test_setblock_command(self):
        self.assertEqual(str(setblock((1, r(2), d(3)), 'm:s')), 'setblock 1 ~2 ^3 m:s')
        self.assertEqual(str(setblock((1, r(2), d(3)), 'm:s', REPLACE)), 'setblock 1 ~2 ^3 m:s replace')
        self.assertEqual(str(setblock((1, r(2), d(3)), 'stone').nbt({'foo': 'bar'})),
                         'setblock 1 ~2 ^3 stone{foo: bar}')
        self.assertEqual(str(setblock((1, r(2), d(3)), 'stone').nbt({'foo': 'bar'}).nbt(
            {'foo': 'baz'})), 'setblock 1 ~2 ^3 stone{foo: baz}')
        self.assertEqual(str(setblock((1, r(2), d(3)), 'stone').state({'up': 'down'})),
                         'setblock 1 ~2 ^3 stone[up=down]')
        self.assertEqual(str(setblock((1, r(2), d(3)), 'stone').state({'up': 'down'}).state(
            {'up': 'upper'})), 'setblock 1 ~2 ^3 stone[up=upper]')
        self.assertEqual(str(setblock((1, r(2), d(3)), 'stone').state({'up': 'down'}).nbt(
            {'up': 'upper'})), 'setblock 1 ~2 ^3 stone[up=down]{up: upper}')

    def test_setworldspawn_command(self):
        self.assertEqual(setworldspawn(), 'setworldspawn')
        self.assertEqual(setworldspawn((1, r(2), d(3))), 'setworldspawn 1 ~2 ^3')
        self.assertEqual(setworldspawn((1, r(2), d(3)), 9.3), 'setworldspawn 1 ~2 ^3 9.3')

    def test_spawnpoint_command(self):
        self.assertEqual(spawnpoint(), 'spawnpoint')
        self.assertEqual(spawnpoint(s()), 'spawnpoint @s')
        self.assertEqual(spawnpoint(s(), (1, r(2), d(3))), 'spawnpoint @s 1 ~2 ^3')
        self.assertEqual(spawnpoint(s(), (1, r(2), d(3)), 9.3), 'spawnpoint @s 1 ~2 ^3 9.3')

    def test_spectate_command(self):
        self.assertEqual(spectate(s()), 'spectate @s')
        self.assertEqual(spectate(s(), random()), 'spectate @s @r')

    def test_spreadplayers_command(self):
        self.assertEqual(spreadplayers((1, r(2), d(3)), 1.7, 15.3, True, a()),
                         'spreadplayers 1 ~2 ^3 1.7 15.3 true @a')
        self.assertEqual(spreadplayers((1, r(2), d(3)), 1.7, 15.3, True, a(),
                                       150), 'spreadplayers 1 ~2 ^3 1.7 15.3 under 150 true @a')

    def test_stopsound_command(self):
        self.assertEqual(stopsound(a()), 'stopsound @a')
        self.assertEqual(stopsound(a(), 'm:/a/b'), 'stopsound @a m:/a/b')
        self.assertEqual(stopsound(a(), 'm:/a/b', 'm:c'), 'stopsound @a m:/a/b m:c')

    def test_summon_command(self):
        self.assertEqual(summon('m:z'), 'summon m:z')
        self.assertEqual(summon('m:z', (1, r(2), d(3))), 'summon m:z 1 ~2 ^3')
        self.assertEqual(summon('m:z', (1, r(2), d(3)), Nbt({'NoAI': True})), 'summon m:z 1 ~2 ^3 {NoAI: true}')

    def test_tag_command(self):
        self.assertEqual(tag(s()).add('foo'), 'tag @s add foo')
        self.assertEqual(tag(s()).list(), 'tag @s list')
        self.assertEqual(tag(s()).remove('foo'), 'tag @s remove foo')

    def test_team_command(self):
        self.assertEqual(team().list(), 'team list')
        self.assertEqual(team().list('foo'), 'team list foo')
        self.assertEqual(team().add('foo', 'bar'), 'team add foo bar')
        self.assertEqual(team().add('foo', 'bar'), 'team add foo bar')
        self.assertEqual(team().remove('foo'), 'team remove foo')
        self.assertEqual(team().remove('foo'), 'team remove foo')
        self.assertEqual(team().empty('foo'), 'team empty foo')
        self.assertEqual(team().join('foo'), 'team join foo')
        self.assertEqual(team().join('foo', random()), 'team join foo @r')
        self.assertEqual(team().leave('foo', random()), 'team leave foo @r')
        self.assertEqual(team().modify('foo', TeamOption.DISPLAY_NAME, 'bar'), 'team modify foo displayName bar')
        self.assertEqual(team().modify('foo', TeamOption.FRIENDLY_FIRE, True), 'team modify foo friendlyFire true')
        self.assertEqual(team().modify('foo', TeamOption.NAMETAG_VISIBILITY,
                                       HIDE_FOR_OWN_TEAM), 'team modify foo nametagVisibility hideForOwnTeam')
        self.assertEqual(team().modify('foo', TeamOption.DEATH_MESSAGE_VISIBILITY,
                                       HIDE_FOR_OTHER_TEAMS),
                         'team modify foo deathMessageVisibility hideForOtherTeams')
        self.assertEqual(team().modify('foo', TeamOption.COLLISION_RULE,
                                       PUSH_OWN_TEAM), 'team modify foo collisionRule pushOwnTeam')
        self.assertEqual(team().modify('foo', TeamOption.PREFIX, 'pre'), 'team modify foo prefix pre')
        self.assertEqual(team().modify('foo', TeamOption.SUFFIX, 'post'), 'team modify foo suffix post')
        with self.assertRaises(ValueError):
            team().modify('foo', TeamOption.DISPLAY_NAME, True)
            team().modify('foo', TeamOption.FRIENDLY_FIRE, 'false')
            team().modify('foo', TeamOption.NAMETAG_VISIBILITY, 'bar')
            team().modify('foo', TeamOption.DEATH_MESSAGE_VISIBILITY, 'bar')
            team().modify('foo', TeamOption.COLLISION_RULE, 'bar')
            team().modify('foo', TeamOption.PREFIX, True)
            team().modify('foo', TeamOption.SUFFIX, True)

    def test_teleport_commands(self):
        self.assertEqual(str(teleport(random())), 'tp @r')
        self.assertEqual(str(teleport(random(), s())), 'tp @r @s')
        self.assertEqual(str(teleport((1, r(2), d(3)))), 'tp 1 ~2 ^3')
        self.assertEqual(str(teleport(random(), (1, r(2), d(3)))), 'tp @r 1 ~2 ^3')
        self.assertEqual(teleport(random(), (1, r(2), d(3)), 3.4), 'tp @r 1 ~2 ^3 3.4')
        self.assertEqual(teleport(random(), s()).facing((1, r(2), d(3))), 'tp @r @s facing 1 ~2 ^3')
        self.assertEqual(teleport(random(), s()).facing(a()), 'tp @r @s facing entity @a')
        self.assertEqual(teleport(random(), s()).facing(a(), EYES), 'tp @r @s facing entity @a eyes')
        with self.assertRaises(ValueError):
            teleport((1, 2, 3), None, 2.4)

    def test_time_command(self):
        self.assertEqual(time().add(9), 'time add 9')
        self.assertEqual(time().add('14d'), 'time add 14d')
        self.assertEqual(time().query(GAMETIME), 'time query gametime')
        self.assertEqual(time().set(9), 'time set 9')
        self.assertEqual(time().set('14d'), 'time set 14d')

    def test_title_command(self):
        self.assertEqual(title(s()).clear(), 'title @s clear')
        self.assertEqual(title(s()).reset(), 'title @s reset')
        self.assertEqual(title(s()).title('foo'), 'title @s title foo')
        self.assertEqual(title(s()).subtitle('foo'), 'title @s subtitle foo')
        self.assertEqual(title(s()).actionbar('foo'), 'title @s actionbar foo')
        self.assertEqual(title(s()).times(1, 2, 3), 'title @s times 1 2 3')

    def test_trigger_command(self):
        self.assertEqual(str(trigger('foo')), 'trigger foo')
        self.assertEqual(trigger('foo').add(17), 'trigger foo add 17')
        self.assertEqual(trigger('foo').set(17), 'trigger foo set 17')
        self.assertEqual(trigger('foo').set(17), 'trigger foo set 17')

    def test_weather_command(self):
        self.assertEqual(weather(THUNDER), 'weather thunder')
        self.assertEqual(weather(RAIN, 17), 'weather rain 17')

    def test_worldborder_command(self):
        self.assertEqual(worldborder().add(17.3), 'worldborder add 17.3')
        self.assertEqual(worldborder().add(17.3, 9), 'worldborder add 17.3 9')
        self.assertEqual(worldborder().center((r(1), d(2))), 'worldborder center ~1 ^2')
        self.assertEqual(worldborder().get(), 'worldborder get')
        self.assertEqual(worldborder().set(9.2), 'worldborder set 9.2')
        self.assertEqual(worldborder().damage().amount(2.3), 'worldborder damage amount 2.3')
        self.assertEqual(worldborder().damage().buffer(7.2), 'worldborder damage buffer 7.2')
        self.assertEqual(worldborder().warning().distance(2.3), 'worldborder warning distance 2.3')
        self.assertEqual(worldborder().warning().time(5), 'worldborder warning time 5')

    def test_simple_commands(self):
        self.assertEqual(defaultgamemode(SURVIVAL), 'defaultgamemode survival')
        self.assertEqual(deop(s(), a()), 'deop @s @a')
        self.assertEqual(difficulty(PEACEFUL), 'difficulty peaceful')
        self.assertEqual(function('m:b/c'), 'function m:b/c')
        self.assertEqual(me('howdy'), 'me howdy')
        self.assertEqual(op(s()), 'op @s')
        self.assertEqual(reload(), 'reload')
        self.assertEqual(say('hi'), 'say hi')
        self.assertEqual(seed(), 'seed')
        self.assertEqual(teammsg('hi'), 'teammsg hi')
        self.assertEqual(tm('hi'), 'teammsg hi')
        self.assertEqual(tell(s(), 'hi'), 'tell @s hi')
        self.assertEqual(msg(s(), 'hi'), 'tell @s hi')
        self.assertEqual(w(s(), 'hi'), 'tell @s hi')
        self.assertEqual(tellraw(s(), JsonText.text('howdy')), 'tellraw @s {"text": "howdy"}')
        self.assertEqual(tellraw(s(), {'text': 'howdy'}), 'tellraw @s {"text": "howdy"}')
        self.assertEqual(tellraw(s(), 'howdy'), 'tellraw @s {"text": "howdy"}')

    def test_resource_checks(self):
        self.assertEqual(good_resource('xyzzy'), 'xyzzy')
        self.assertEqual(good_resource('m:xyzzy'), 'm:xyzzy')
        self.assertEqual(good_resource_path('xyzzy'), 'xyzzy')
        self.assertEqual(good_resource_path('m:xyzzy'), 'm:xyzzy')
        self.assertEqual(good_resource_path('a/b/c'), 'a/b/c')
        self.assertEqual(good_resource_path('/a/b/c'), '/a/b/c')
        self.assertEqual(good_resource_path('m:a/b/c'), 'm:a/b/c')
        self.assertEqual(good_resource_path('m:/a/b/c'), 'm:/a/b/c')
        with self.assertRaises(ValueError):
            good_resource('%')
            good_resource('m:xyzzy', allow_namespace=False)
            good_resource_path('/')
            good_resource_path('a//b')
            good_resource_path('/a/b: c')
            good_resource_path('//a/b/c')

    def test_tag_checks(self):
        self.assertEqual(good_name('xyzzy'), 'xyzzy')
        self.assertEqual(good_name('a+b'), 'a+b')
        self.assertEqual(good_name('!a+b', allow_not=True), '!a+b')
        self.assertEqual(good_names('_', 'b-3'), ('_', 'b-3'))
        self.assertEqual(good_names('_', '!b-3', allow_not=True), ('_', '!b-3'))
        with self.assertRaises(ValueError):
            good_name('x&y')
            good_name('!foo')
            good_names('_', '!b-3')

    def test_commands(self):
        self.assertEqual(commands(help(), help('foo'), function('m:b/c')), 'help\nhelp foo\nfunction m:b/c')
