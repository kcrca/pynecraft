from __future__ import annotations

"""

builds pynecraft.all_*.txt using current data. all_blocks and all_items are built from en_us.json, which some tweaking.

Unfortunately there is no list anywhere in the minecraft data of which entities are mobs, vs. thrown bottles, boats, 
etc. So reading the wiki is still (currently) the best source of mob data.This is inherently a bit crufty and 
sensitive, because it reads data from a wiki, which may change at any time. If I knew of a better way to get this 
info, I'd use it.

"""

from pynecraft.base import to_name

import json
import re
import sys
from abc import ABC, abstractmethod
from pathlib import Path

import regex
import requests
from bs4 import BeautifulSoup

cwd = Path(sys.path[0])


class Fetcher(ABC):
    def __init__(self, which: str, url: str):
        self.which = which
        self.url = url

    @abstractmethod
    def get_start(self, page):
        pass

    @abstractmethod
    def is_end(self, elem) -> bool:
        pass

    def is_ignore(self, elem) -> bool:
        return False

    @abstractmethod
    def get_id(self, raw_id: str, raw_desc: str) -> tuple[str, str]:
        pass

    def added(self, things: list[str]):
        return []

    def find_desc(self, elem):
        for d in elem.find_all('li'):
            if 'Lodestone Compass' not in str(d):
                yield d

    def fetch(self):
        html = requests.get(self.url).text
        page = BeautifulSoup(html, 'html.parser')
        start = self.get_start(page)
        things = []
        for elem in start.find_next_siblings():
            if self.is_end(elem):
                break
            if self.is_ignore(elem):
                continue
            for li in self.find_desc(elem):
                raw_text = strip_spaces(li.text)  # Discard the zero-width non-joiners
                m = re.search(r'\[(.*) only]', raw_text, re.IGNORECASE)
                if m and not ('Java' in m.group(1) or 'JE' in m.group(1)):
                    continue

                raw_desc = raw_text.strip()
                raw_id = re.sub(r'\s+', ' ', raw_desc.replace("'", " "))
                id, desc = self.get_id(raw_id, raw_desc)
                if id:
                    row = desc if id == desc else f'{desc} / {id}'
                    things.append(row)

        for to_add in self.added(things):
            assert to_add not in things
            things.append(to_add)

        with open(cwd / f'../all_{self.which}.txt', 'w') as fp:
            fp.write('\n'.join(sorted(things)))
            fp.write('\n')


def strip_spaces(raw):
    return regex.sub(r'\p{Default_Ignorable_Code_Point}', '', raw).strip()


class MobFetcher(Fetcher):
    def __init__(self):
        super().__init__('mobs', 'https://minecraft.wiki/Mob?so=search#List_of_mobs')

    def get_start(self, page):
        return page.find('h2', string='List of mobs')

    def is_end(self, elem):
        return elem.name == 'h2' or 'Unused mobs' in elem.text or 'Upcoming' in elem.text

    def is_ignore(self, elem) -> bool:
        return 'NPC' in str(elem)

    def find_desc(self, elem):
        return elem.find_all(class_='mob-name')

    def get_id(self, raw_id: str, raw_desc: str):
        id = re.sub(r'\s*\(.*', '', raw_id)
        desc = re.sub(r'\s*\(.*', '', raw_desc)
        return id, desc

    def added(self, things: list[str]):
        if 'Breeze' not in things:
            return ['Breeze']
        return super().added(things)


if __name__ == '__main__':
    MobFetcher().fetch()

    with open(Path.home() / 'clarity' / 'default_resourcepack' / 'assets' / 'minecraft' / 'lang' / 'en_us.json') as fp:
        lang = json.load(fp)

    unholdable_items_re = re.compile('|'.join((
        r'Filled Map',
        r'Lodestone Compass',  # This is really a variant of Compass
        r'Brewing Stand',  # These are blocks but are in here too, though the rest of the blocks aren't
        r'Cauldron',
        r'Flower Pot',
        r'Pitcher Plant',
        r'^Sign$',  # Don't know why these are here
        r'^Scute',
        r'^Smithing Template',
        r'^Harness$',
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
        r'^Grass$',  # generic grass, which isn't a specific thing
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
