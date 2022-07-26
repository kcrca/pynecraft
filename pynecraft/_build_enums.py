from __future__ import annotations

import datetime
import re
from abc import ABC, abstractmethod
from contextlib import redirect_stdout
from pathlib import Path

import requests
from bs4 import BeautifulSoup


class EnumDesc(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def generate(self):
        pass

    def supplement_class(self):
        pass


class PageEnumDesc(EnumDesc):
    def __init__(self, name: str | None, url, data_desc: str | None):
        super().__init__(name)
        self.url = url
        self.data_desc = data_desc

    def fetch(self):
        cache = Path('.enum_cache') / (self.name + '.html')
        cache.parent.mkdir(exist_ok=True)
        if cache.exists():
            mtime = datetime.datetime.fromtimestamp(cache.stat().st_mtime)
            if mtime + datetime.timedelta(weeks=1) > datetime.datetime.now():
                try:
                    with open(cache) as f:
                        html = f.read()
                except IOError as e:
                    cache.unlink()
                    raise e
            else:
                cache.unlink()
        if not cache.exists():
            html = requests.get(self.url).text
            with open(cache, 'w') as f:
                f.write(html)

        return BeautifulSoup(html, 'html.parser')

    def replace(self, name: str, value: str):
        return name

    @abstractmethod
    def note_header(self, col: int, text: str):
        pass

    @abstractmethod
    def extract(self, cols):
        pass

    def generate(self):
        soup = self.fetch()
        tables = self.find_tables(soup)
        found = {}
        assert tables
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                headers = row.find_all('th')
                if headers:
                    for i in range(0, len(headers)):
                        th = headers[i]
                        text = th.text.strip()
                        self.note_header(i, text)
                else:
                    cells = row.find_all('td')
                    extracted = self.extract(cells)
                    if not extracted:
                        continue
                    display_name, value, desc = extracted
                    name = re.sub(junk, '', display_name).upper().replace(' ', '_')
                    name = self.replace(name, value)
                    if desc[-1] not in '.?!':
                        desc += '.'
                    desc = re.sub(r'\s+', ' ', desc)
                    if name in found:
                        raise KeyError(f'{name}: Duplicate name: ({value}, {found[name]})')
                    found[name] = (value, desc, display_name)
        return found

    def find_tables(self, soup):
        return soup.find_all('table', attrs={'data-description': self.data_desc})


def clean(cell) -> str:
    if not isinstance(cell, str):
        cell = cell.text
    return re.sub(r'\[.*', '', re.sub(r'\s{2,}', ' ', cell.strip()).replace(u'\u200c', ''), flags=re.DOTALL).strip()


def to_desc(text):
    text = re.sub(r'\[[^]]*]', '', text)
    if text[-1] not in '.!?':
        return text + '.'
    return text


class Advancement(PageEnumDesc):
    def __init__(self):
        super().__init__('Advancement', 'https://minecraft.fandom.com/wiki/Advancement#List_of_advancements',
                         'advancements')
        self.value_col = None
        self.desc_col = None
        self.name_col = None

    def note_header(self, col: int, text: str):
        if text == 'Advancement':
            self.name_col = col
        elif text.startswith('Resource'):
            self.value_col = col
        elif text.find('description') >= 0:
            self.desc_col = col

    def extract(self, cols):
        return (clean(x.text) for x in (cols[self.name_col], cols[self.value_col], cols[self.desc_col]))

    def replace(self, name, value):
        if name == 'THE_END' and value.startswith('story'):
            return 'ENTER_THE_END'
        return name


class Effect(PageEnumDesc):
    def __init__(self):
        super().__init__('Effect', 'https://minecraft.fandom.com/wiki/Effect?so=search#Effect_list', 'Effects')
        self.filter_col = None
        self.desc_col = None
        self.value_col = None
        self.name_col = None
        self.type_col = None
        self.negatives = set()

    def note_header(self, col: int, text: str):
        if text == 'Display name':
            self.name_col = col
        elif text.startswith('Name'):
            self.value_col = col
        elif text.find('Effect') >= 0:
            self.desc_col = col
        elif text.find('ID (J.E.)') >= 0:
            self.filter_col = col
        elif text.find('Type') >= 0:
            self.type_col = col

    def extract(self, cols):
        if 'N/A' in cols[self.filter_col].text:
            return None
        if cols[self.type_col].text.startswith('Negative'):
            self.negatives.add(clean(cols[self.value_col]))
        return (clean(x.text) for x in (cols[self.name_col], cols[self.value_col], cols[self.desc_col]))

    def supplement_class(self):
        print()
        print('    @staticmethod')
        print('    def negative(effect):')
        print(f'      return effect.value in {sorted(self.negatives)}')


class Enchantment(PageEnumDesc):
    def __init__(self):
        super().__init__('Enchantment', 'https://minecraft.fandom.com/wiki/Enchanting#Summary_of_enchantments',
                         'Summary of enchantments')
        self.max_col = None
        self.name_col = None
        self.desc_col = None
        self.maxes = {}

    def note_header(self, col: int, text: str):
        if text == 'Name':
            self.name_col = col
        elif text == 'Summary':
            self.desc_col = col
        elif text.startswith('Max'):
            self.max_col = col

    def extract(self, cols):
        name = clean(cols[self.name_col])
        name = re.sub(r'\s{2,}', ' ', name)
        value = name.lower().replace(' ', '_')
        desc = clean(cols[self.desc_col])
        self.maxes[value] = roman_to_int(clean(cols[self.max_col].text))
        return name, value, desc

    def supplement_class(self):
        print()
        print('    @staticmethod')
        print('    def max_level(ench):')
        print(f'      return {self.maxes}[ench.value]')


class GameRule(PageEnumDesc):
    def __init__(self):
        super().__init__('GameRule', 'https://minecraft.fandom.com/wiki/Game_rule?so=search#List_of_game_rules', None)
        self.types = {}
        self.filter_col = None
        self.type_col = None
        self.desc_col = None
        self.value_col = None

    def find_tables(self, soup):
        tables = []
        for t in soup.select('table'):
            caption = t.find('caption')
            if caption and 'List of game rules' in caption.text:
                tables.append(t)
        return tables

    def note_header(self, col: int, text: str):
        if text.lower() == 'rule name':
            self.value_col = col
        elif text == 'Description':
            self.desc_col = col
        elif text == 'Type':
            self.type_col = col
        elif text == 'Availability':
            self.filter_col = col
        elif text == 'Java':
            # Yes this is weird. This is in a nested table, which is the original filter_cal
            self.filter_col += col

    def extract(self, cols):
        if 'yes' not in cols[self.filter_col].text.lower():
            return None
        value = clean(cols[self.value_col].text)
        name = camel_to_name(value)
        self.types[value] = 'int' if clean(cols[self.type_col]).lower() == 'int' else 'bool'
        return name, value, clean(cols[self.desc_col])

    def supplement_class(self):
        print()
        print('    @staticmethod')
        print('    def rule_type(rule):')
        print(f'      return {self.types}[rule.value]')


def camel_to_name(camel):
    return re.sub(r'([a-z])([A-Z]+)', r'\1 \2', camel)


class Particle(PageEnumDesc):
    def __init__(self):
        super().__init__('Particle', 'https://minecraft.fandom.com/wiki/Particles#Types_of_particles', 'Particles')
        self.value_col = None
        self.desc_col = None

    def note_header(self, col: int, text: str):
        if text.startswith('Java Edition'):
            self.value_col = col
        elif text == 'Description':
            self.desc_col = col

    def extract(self, cols):
        if len(cols) != 4:
            return None
        value = clean(cols[self.value_col].text)
        if value == '—':
            return None
        if value[-1] == '*':
            value = value[:-1]
        name = value.replace('_', ' ').title()
        desc = clean(cols[self.desc_col])
        return name, value, desc


class ScoreCriteria(PageEnumDesc):
    def __init__(self):
        super().__init__('ScoreCriteria', 'https://minecraft.fandom.com/wiki/Scoreboard#Criteria', 'Criteria')
        self.desc_col = None
        self.value_col = None

    def note_header(self, col: int, text: str):
        if text.endswith('name'):
            self.value_col = col
        elif text.startswith('Description'):
            self.desc_col = col

    def extract(self, cols):
        value = clean(cols[self.value_col])
        return camel_to_name(value), value, clean(cols[self.desc_col])


def roman_to_int(s):
    rom_val = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    int_val = 0
    for i in range(len(s)):
        if i > 0 and rom_val[s[i]] > rom_val[s[i - 1]]:
            int_val += rom_val[s[i]] - 2 * rom_val[s[i - 1]]
        else:
            int_val += rom_val[s[i]]
    return int_val


if __name__ == '__main__':
    junk = re.compile(r'[^\w\s]')
    with open('enums.py', 'r+') as out:
        top = []
        for line in out:
            top.append(line)
            if line.startswith('# Generated enums:'):
                break
        out.seek(0, 0)
        out.truncate(0)

        out.writelines(top)
        with redirect_stdout(out):
            for tab in (
                    Advancement(), Effect(), Enchantment(), GameRule(), ScoreCriteria(), Particle()):
                fields = tab.generate()
                print('\n')
                print('# noinspection SpellCheckingInspection')
                print('@enum.unique')
                print(f'class {tab.name}(ValueEnum):')
                names = {}
                for key in fields:
                    value, desc, name = fields[key]
                    names[key] = name
                    print(f'    {key} = "{value}"\n    """{desc}"""')

                print()
                print('    @staticmethod')
                print('    def display_name(elem) -> str:')
                print('        return {' + (', '.join('%s.%s: "%s"' % (tab.name, k, v.replace('"', r'\"')) for k, v in
                                                      names.items())) + '}[elem]')
                tab.supplement_class()
