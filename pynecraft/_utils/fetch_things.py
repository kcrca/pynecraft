#!/usr/bin/env python

"""

Rebuilds pynecraft.all_mobs.txt using current data. It used to build all_blocks and all_items also, but those are now
built from build_things.py, which reads en_us.json to find all the blocks and items. Unfortunately there is no list
anywhere in the minecraft data of which entities are mobs, vs. thrown bottles, boats, etc. So reading the wiki is
still (currently) the best source of data.

This is inherently a bit crufty and sensitive, because it reads data from a wiki, which may change at any time. If I
knew of a better way to get this info, I'd use it.

"""

from __future__ import annotations

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
