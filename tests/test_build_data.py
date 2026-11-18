import json
import unittest
from unittest.mock import MagicMock, patch

from pynecraft._utils import build_data
from pynecraft._values import game_rules, sulfur_cube_archetypes, team_options


def _arg(arg_type: str, **extra) -> dict:
    return {'type': 'argument', 'argument': {'type': arg_type, **extra}, 'executable': True}


def _literal(**children) -> dict:
    return {'type': 'literal', 'children': children}


def _tree(path: str, leaves: dict) -> dict:
    node = {'children': leaves}
    for name in reversed(path.split()):
        node = {'children': {name: node}}
    return node


class TestBuildData(unittest.TestCase):
    def test_arg_types(self):
        children = {'value': _arg('minecraft:integer', min=0), 'on': {'type': 'literal'}}
        self.assertEqual(['minecraft:integer'], build_data._arg_types(children))
        self.assertEqual([], build_data._arg_types({}))

    def test_gamerules(self):
        commands = _tree('gamerule', {
            'random_tick_speed': _literal(value=_arg('minecraft:integer', min=0)),
            'keep_inventory': _literal(value=_arg('minecraft:bool')),
            'minecraft:keep_inventory': _literal(value=_arg('minecraft:bool')),
        })
        lang = {'gamerule.randomTickSpeed': 'Random tick speed rate'}
        with patch.object(build_data, '_commands', return_value=commands), \
                patch.object(build_data, '_lang', return_value=lang):
            rules = build_data._gamerules()
        self.assertEqual({'RANDOM_TICK_SPEED', 'KEEP_INVENTORY'}, set(rules))
        self.assertEqual('int', rules['RANDOM_TICK_SPEED'][3])
        self.assertEqual('Random tick speed rate', rules['RANDOM_TICK_SPEED'][1])
        self.assertEqual('bool', rules['KEEP_INVENTORY'][3])

    def test_sulfur_cube_archetypes(self):
        data = MagicMock()
        files = []
        for name, items in (('bouncy', '#minecraft:sulfur_cube_archetype/bouncy'), ('hot', 'minecraft:magma_block'),
                            ('mixed', ['minecraft:tnt', '#minecraft:wool'])):
            f = MagicMock(stem=name)
            f.read_text.return_value = json.dumps({'items': items})
            files.append(f)
        data.glob.return_value = files
        tags = {'item': {'sulfur_cube_archetype/bouncy': ['oak_planks', 'oak_log'], 'wool': ['red_wool']}}
        with patch.object(build_data, '_get_data', return_value=data), \
                patch.object(build_data, '_build_tags', return_value=tags):
            archetypes = build_data._sulfur_cube_archetypes()
        self.assertEqual({'bouncy': ['oak_log', 'oak_planks'], 'hot': ['magma_block'], 'mixed': ['red_wool', 'tnt']},
                         archetypes)

    def test_team_options(self):
        commands = _tree('team modify team', {
            'friendlyFire': _literal(allowed=_arg('minecraft:bool')),
            'prefix': _literal(prefix=_arg('minecraft:component')),
            'color': _literal(red={'type': 'literal'}, blue={'type': 'literal'}),
            'bare': {'type': 'literal'},
        })
        with patch.object(build_data, '_commands', return_value=commands):
            opts = build_data._team_options()
        self.assertIs(bool, opts['FRIENDLY_FIRE'][3])
        self.assertEqual('Nbt', opts['PREFIX'][3])
        self.assertEqual(['blue', 'red'], opts['COLOR'][3])
        self.assertIs(str, opts['BARE'][3])

    def test_generated_values(self):
        self.assertIs(int, game_rules['random_tick_speed'].rule_type)
        self.assertIs(bool, game_rules['keep_inventory'].rule_type)
        self.assertIs(bool, team_options['friendlyFire'].type)
        self.assertEqual(['tnt'], sulfur_cube_archetypes['explosive'])
        self.assertIn('oak_planks', sulfur_cube_archetypes['bouncy'])
        self.assertIn('oak_log', sulfur_cube_archetypes['bouncy'])
