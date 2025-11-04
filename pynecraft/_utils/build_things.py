import json
import re
from pathlib import Path

from pynecraft.base import to_name

with open(Path.home() / 'clarity' / 'default_resourcepack' / 'assets' / 'minecraft' / 'lang' / 'en_us.json') as fp:
    lang = json.load(fp)

unholdable_items_re = re.compile('|'.join((
    r'Filled Map',
    r'Brewing Stand', # These are blocks but are in here too, though the rest of the blocks aren't
    r'Cauldron',
    r'Flower Pot',
    r'Pitcher Plant',
    r'^Sign$',  # Don't know why this is here
    r'Pottery Shard',  # Old names (why is it still here?)
)))
unholdable_blocks_re = re.compile('|'.join((
    r' Wall ',  # Oak Wall Sign, etc.
    r' Cake$',  # Cake with candles
    r'(Melon|Pumpkin|Dripleaf) Stem',
    r'Bubble Column',
    r'Cave Vine',
    r'\bAir\b',  # Any kind of air
    r'Gateway',  # The shimmery gateways
    r'Portal$',  # The shimmery portals
    '^Moving ',  # Moving Piston
    r'Piston Head',  # The piston head
    r'Frosted Ice',  # Only from enchantment
    r'(?<!Pitcher) Plant',  # All plants but pitcher plant
    r' Cauldron',  # The specific cauldrons (water, lava, ...)
    r'^Potted',  # Potted plants
    r'Ominous Banner',
    r' Crop$',
    'Wall Torch',
    r'^Chain$',  # Old name for "Iron Chain", still there
    'Set Spawn',  # This seems like a mistake, it isn't a block
)))


def build_list(which, unholdable_re):
    full_prefix = f'{which}.minecraft.'
    holdable = set()
    things = {}
    for k, v in lang.items():
        if not k.startswith(full_prefix):
            continue
        parts = k.split('.')
        if len(parts) == 3 or (len(parts) > 3 and parts[3] == 'new'):
            id = parts[2]
            name = to_name(id)
            if not unholdable_re.search(name):
                holdable.add(id)
            # The names for music discs are all wonky, this works best
            things[id] = name if id.startswith('music_disc_') else v

    path = f'../all_{which}s.txt'
    with open(path, 'w') as fp:
        for k, v in filter(lambda x: x[0] in holdable, sorted(things.items(), key=lambda x: x[1])):
            if k in holdable:
                name = to_name(k)
                if name != v:
                    print(f'{v} / {name}', file=fp)
                else:
                    print(v, file=fp)


build_list('item', unholdable_items_re)
build_list('block', unholdable_blocks_re)
