from __future__ import annotations

import datetime
import re
from abc import ABC, abstractmethod

import requests
from bs4 import BeautifulSoup


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

    def added(self):
        return []

    def fetch(self):
        html = requests.get(self.url).text
        page = BeautifulSoup(html, 'html.parser')
        start = self.get_start(page)
        things = []
        for elem in start.find_next_siblings():
            if self.is_end(elem):
                break
            for li in elem.find_all('li'):
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
        for to_add in self.added():
            assert to_add not in things
            things.append(to_add)

        with open(f'../all_{self.which}.txt', 'w') as fp:
            fp.write(f'# Fetched at {datetime.datetime.now()} from {self.url}\n')
            fp.write('\n'.join(sorted(things)))
            fp.write('\n')


class BlockFetcher(Fetcher):
    block_items = {
        'Bamboo Shoot': 'Bamboo',
        'Cave Vines': 'Glow Berries',
        'Cocoa': 'Cocoa Beans',
        'Fire': 'Campfire',
        'Lava': 'Lava Bucket',
        'Melon Stem': 'Melon Seeds',
        'Pumpkin Stem': 'Pumpkin Seeds',
        'Potatoes': 'Potato',
        'Powder Snow': 'Powder Snow Bucket',
        'Redstone Wire': 'Redstone',
        'Soul Fire': 'Soul Campfire',
        'Sweet Berry Bush': 'Sweet Berries',
        'Tall Seagrass': 'Seagrass',
        'Tripwire': 'String',
        'Water': 'Water Bucket',
        'Air': None,
        'Cave Air': None,
    }

    def __init__(self):
        super().__init__('blocks', 'https://minecraft.fandom.com/wiki/Block#List_of_blocks')

    def get_start(self, page):
        return page.find('h2', text='List of blocks')

    def is_end(self, elem):
        return elem.name == 'h2' or 'Technical blocks' in elem.text

    def get_id(self, raw_id, raw_desc):
        if 'Ominous' in raw_id:
            # This is not really a block at all.
            return None, None

        id = raw_id
        desc = raw_desc
        if 'Lapis' in id and id != 'Lapis Lazuli':
            id = id.replace('Lapis Lazuli', 'Lapis')
        elif 'Bale' in id:
            id = id.replace('Bale', 'Block')
        elif 'Redstone' in id:
            id = re.sub(r'Redstone (Repeater|Comparator)', r'\1', id)
        if 'Block' in id or 'Crops' in id:
            id = re.sub(r'Block of (.*)', r'\1 Block', id)
            id = re.sub(r'(Jigsaw|Light|Smooth Quartz|Wheat) (Block|Crops)', r'\1', id)
        id = re.sub(r'^(Beetroot|Carrot|Vine)s', r'\1', id)
        return id, desc

    def added(self):
        # These should be there, but aren't
        return ['Air', 'Cave Air']


class ItemFetcher(Fetcher):
    id_replace = {'Redstone Dust': 'Redstone', 'Book and Quill': 'Writable Book', 'Empty Map': 'Map',
                  'Steak': 'Cooked Beef', 'Turtle Shell': 'Turtle Helmet', 'Disc Fragment': 'Disc Fragment 5',
                  'Nether Quartz': 'Quartz', 'Slimeball': 'Slime Ball'}

    def __init__(self):
        super().__init__('items', 'https://minecraft.fandom.com/wiki/Item?so=search#List_of_items')

    def get_start(self, page):
        return page.find('h2', text='List of items')

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
        id = re.sub(r'\s*[([].*', '', id)
        desc = re.sub(r'\s*[([].*', '', desc)

        if 'Explorer Map' in id:
            # This shows up twice
            return None, None
        elif id in self.id_replace:
            id = self.id_replace[id]
        elif 'Bottle o\'' in desc:
            id = 'Experience Bottle'
        elif 'Banner Pattern ' in id:
            m = re.fullmatch(r'Banner Pattern \(([^ ]+)( .*)?.*\)', id)
            id = f'{m.group(1)} Banner Pattern'
            desc = m.group(1)
        elif 'Boat with Chest' in id:
            id = re.sub(r'(.*) Boat with Chest', r'\1 Chest Boat', id)
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
        elif ' s ' in id:
            id = id.replace(" s ", ' ')
        elif 'Raw ' in id:
            m = re.fullmatch('Raw (Copper|Iron|Gold)', id)
            if not m:
                id = id[4:]

        return id, desc


BlockFetcher().fetch()
ItemFetcher().fetch()
