import unittest
from unittest.mock import patch

from pynecraft._utils import build_data
from pynecraft._values import game_rules, team_options


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
