#!/usr/bin/env python

"""

Rebuilds pynecraft.all*.txt using current data. This is inherently a bit crufty and sensitive, because it reads data
from a wiki, which may change at any time. If I knew of a better way to get this info, I'd use it.

"""

from __future__ import annotations

import re
import sys
from abc import ABC, abstractmethod
from pathlib import Path

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

    @abstractmethod
    def get_id(self, raw_id: str, raw_desc: str) -> tuple[str, str]:
        pass

    def added(self, things: list[str]):
        return []

    def desc_elem(self):
        return 'li'

    def fetch(self):
        html = requests.get(self.url).text
        page = BeautifulSoup(html, 'html.parser')
        start = self.get_start(page)
        things = []
        for elem in start.find_next_siblings():
            if self.is_end(elem):
                break
            for li in elem.find_all(self.desc_elem()):
                raw_text = li.text.replace(u'\u200c', '')  # Discard the zero-width non-joiners
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


class BlockFetcher(Fetcher):
    def __init__(self):
        super().__init__('blocks', 'https://minecraft.fandom.com/wiki/Block#List_of_blocks')

    def get_start(self, page):
        return page.find('h2', string='List of blocks')

    def is_end(self, elem):
        return elem.name == 'h2' or 'Technical blocks' in elem.text

    def get_id(self, raw_id, raw_desc):
        if 'Ominous' in raw_id or 'Torchflower Crop' in raw_id or 'Pitcher Crop' in raw_id:
            # This is not really a block at all.
            return None, None

        # this appears once randomly, and it shouldn't
        if ' (block)' in raw_id:
            raw_id = re.sub(' \(block\)', '', raw_id)
        id = raw_id
        desc = raw_desc
        if 'upcoming' in id:
            if not re.search(r'\bJ\.*E\.*', id):
                return None, None
            id = re.sub(r'\s*\[*upcoming.*', '', id)
            desc = re.sub(r'\s*\[*upcoming.*', ' [x]', desc)
        if 'Lapis' in id and id != 'Lapis Lazuli':
            id = id.replace('Lapis Lazuli', 'Lapis')
        elif 'Bale' in id:
            id = id.replace('Bale', 'Block')
        elif 'Redstone' in id:
            id = re.sub(r'Redstone (Repeater|Comparator)', r'\1', id)
        elif id == 'Monster Spawner':
            id = 'Spawner'
        elif id == 'Grass':
            id = 'Short Grass'
        if 'Block' in id or 'Crops' in id:
            id = re.sub(r'Block of (.*)', r'\1 Block', id)
            id = re.sub(r'(Jigsaw|Light|Smooth Quartz|Wheat) (Block|Crops)', r'\1', id)
        id = re.sub(r'^(Vine)s', r'\1', id)
        id = re.sub(r'Bamboo Shoot', 'Bamboo Sapling', id)
        return id, desc

    def added(self, _):
        # These should be there, but aren't
        return ['Air', 'Cave Air']


class ItemFetcher(Fetcher):
    must_give = [
        'Knowledge Book',
    ]
    operator_menu = [
        'Barrier',
        'Command Block',
        'Chain Command Block',
        'Repeating Command Block',
        'Minecart with Command Block',
        'Debug Stick',
        'Jigsaw',
        'Light',
        'Structure Block',
        'Structure Void',
    ]

    id_replace = {'Redstone Dust': 'Redstone', 'Book and Quill': 'Writable Book', 'Empty Map': 'Map',
                  'Steak': 'Cooked Beef', 'Turtle Shell': 'Turtle Helmet', 'Disc Fragment': 'Disc Fragment 5',
                  'Nether Quartz': 'Quartz', 'Slimeball': 'Slime Ball'}

    def __init__(self):
        super().__init__('items', 'https://minecraft.fandom.com/wiki/Item?so=search#List_of_items')

    def get_start(self, page):
        return page.find('h2', string='List of items')

    def is_end(self, elem):
        return elem.name == 'h2' or 'Education Edition' in elem.text

    def get_id(self, raw_id, raw_desc):
        #  This is in the list as a way to say "any potion", it's not an item.
        if 'Potions' in raw_id:
            return None, None

        id = raw_id
        desc = raw_desc

        if 'Music Disc' in raw_desc:
            id = desc = raw_desc.replace('(', '').replace(')', '')
        elif 'Banner Pattern ' in raw_desc:
            m = re.fullmatch(r'Banner Pattern \(([^ ]+)( .*)?.*\)', desc)
            id = f'{m.group(1)} Banner Pattern'.replace('Snout', 'Piglin').replace('Thing', 'Mojang')
            desc = m.group(1)
        elif ' Trim' in id:
            id = id.replace(' Trim', ' Trim Smithing Template')
        elif 'Netherite Upgrade' in id:
            id = 'Netherite Upgrade Smithing Template'
        id = re.sub(r'\s*[([].*', '', id)
        desc = re.sub(r'\s*[([].*', '', desc)

        if 'Explorer Map' in id or 'Command Block Minecart' in id:
            # These show up twice
            return None, None
        elif id in self.id_replace:
            id = self.id_replace[id]
        elif 'Bottle o\'' in desc:
            id = 'Experience Bottle'
        elif 'Banner Pattern ' in id:
            m = re.fullmatch(r'Banner Pattern \(([^ ]+)( .*)?.*\)', id)
            id = f'{m.group(1)} Banner Pattern'
            desc = m.group(1)
        elif re.search('(Boat|Raft) with Chest', id):
            id = re.sub(r'(.*) (Boat|Raft) with Chest', r'\1 Chest \2', id)
        elif id == 'Monster Spawner':
            id = 'spawner'
        elif ' with ' in id:
            id = re.sub(r'(.*) with (.*)', r'\2 \1', id)
        elif 'Redstone Dust' in id:
            id = 'Redstone'
        elif 'Book and Quill' in id:
            id = 'Writable Book'
        elif ' Cap' in id:
            id = id.replace('Cap', 'Helmet')
        elif ' Pants' in id:
            id = id.replace('Pants', 'Leggings')
        elif ' Tunic' in id:
            id = id.replace('Tunic', 'Chestplate')
        elif 'Bucket of' in id or 'Eye of' in id:
            id = re.sub(r'(Bucket|Eye) of (.*)', r'\2 \1', id)
        elif ' s ' in id:  # was 's before replacement above
            id = id.replace(" s ", ' ')
        elif 'Raw ' in id:
            m = re.fullmatch('Raw (Copper|Iron|Gold)', id)
            if not m:
                id = id[4:]
        elif id == 'Scute':
            id = 'Turtle Scute'

        return id, desc

    def added(self, things):
        # In this case, some names do show up in the list, and which ones might change.
        return filter(lambda s: s not in things, ItemFetcher.must_give)


class MobFetcher(Fetcher):
    def __init__(self):
        super().__init__('mobs', 'https://minecraft.fandom.com/wiki/Mob?so=search#List_of_mobs')

    def get_start(self, page):
        return page.find('h2', string='List of mobs')

    def is_end(self, elem):
        return elem.name == 'h2' or 'Unused mobs' in elem.text or 'Upcoming' in elem.text

    def desc_elem(self):
        return 'td'

    def get_id(self, raw_id: str, raw_desc: str):
        id = re.sub(r'\s*\(.*', '', raw_id)
        desc = re.sub(r'\s*\(.*', '', raw_desc)
        # Not really mobs, you can't summon them.
        if 'Jockey' in desc or 'Horseman' in desc:
            return None, None
        return id, desc

    def added(self, things: list[str]):
        if 'Breeze' not in things:
            return ['Breeze']
        return super().added(things)


if __name__ == '__main__':
    BlockFetcher().fetch()
    ItemFetcher().fetch()
    MobFetcher().fetch()
