#!/usr/bin/env python

"""

Rebuilds pynecraft.enum.py using current data. This is inherently a bit crufty and sensitive, because it reads data
from a wiki, which may change at any time. If I knew of a better way to get this info, I'd use it.

"""

from __future__ import annotations

import datetime
import glob
import re
import sys
from abc import ABC, abstractmethod
from contextlib import redirect_stdout
from pathlib import Path

import requests
from bs4 import BeautifulSoup

WIKI = 'https://minecraft.wiki/'
noinspection = '# noinspection SpellCheckingInspection,GrazieInspection'
cwd = Path(sys.path[0])


class EnumDesc(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def generate(self):
        pass

    def added_fields(self):
        return []

    def added_values(self, value):
        return ''

    def pluralize(self):
        return 's'


class PageEnumDesc(EnumDesc):
    """This abstract class is subclassed for each enum whose elements are read from a web page. """

    def __init__(self, name: str | None, url, data_desc: str | None):
        """
        :param name: The enum name.
        :param url: The URL of the page
        :param data_desc: The docstring for the generated enum.
        """
        super().__init__(name)
        self.url = url
        self.data_desc = data_desc

    def fetch(self):
        """
        Fetches the page, using the implemented abstract methods to retrieve the data. If there is an HTML file in
        ``.enum_cache`` for the page, it will be used if it is less than a week old. This speeds up development of
        this program so repeated runs are faster.

        The web pages are pretty inconsistent, though not entirely. But nowhere near enough to share much code in the
        scraping of them.
        """
        cache = cwd / '.enum_cache' / (self.name + '.html')
        cache.parent.mkdir(exist_ok=True)
        html = None
        now = datetime.datetime.now()
        html_time = now
        if cache.exists():
            mtime = datetime.datetime.fromtimestamp(cache.stat().st_mtime)
            if mtime + datetime.timedelta(weeks=1) > now:
                try:
                    with open(cache) as f:
                        html = f.read()
                except IOError:
                    cache.unlink()
                    raise
                html_time = mtime
            else:
                cache.unlink()
                html_time = now
        if not html:
            html = requests.get(self.url).text
            with open(cache, 'w') as f:
                f.write(html)

        return html_time, BeautifulSoup(html, 'html.parser')

    def replace(self, name: str, value: str):
        return name

    @abstractmethod
    def header(self, col: int, text: str):
        """
        Invoked for each header cell so the subclass can note interesting columns.
        :param col: Which column this is for.
        :param text: The header text for the column.
        """

    @abstractmethod
    def extract(self, cols) -> tuple[str, str, str]:
        """
        Extracts the data from the page for a single row of the table.
        :param cols: The HTML elements for the columns.
        :return: The extracted data. This is a three-tuple that has the display name, value, and description.
        """

    def generate(self):
        """
        Invokes fetch(), uses the abstract methods to scrape the relevant content, and then generates the actual enum.
        """
        html_time, soup = self.fetch()
        tables = self.find_tables(soup)
        found = {}
        assert tables, f"No table found: {self.name}, {self.url}"
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                headers = row.find_all('th')
                if headers:
                    for i, th in enumerate(headers):
                        self.header(i, th.text.strip())
                else:
                    cells = row.find_all('td')
                    extracted = self.extract(cells)
                    if not extracted:
                        continue
                    display_name, value, desc = extracted
                    name = re.sub(r'[^\w\s]', '', display_name)
                    name = name.upper().replace(' ', '_')
                    name = self.replace(name, value)
                    if desc:
                        if desc[-1] not in '.?!':
                            desc += '.'
                        desc = re.sub(r'\s+', ' ', desc)
                    if name in found:
                        raise KeyError(f'{name}: Duplicate name: ({value}, {found[name]})')
                    found[name] = (value, desc, display_name)
        return html_time, found

    def find_tables(self, soup):
        return soup.find_all('table', attrs={'data-description': self.data_desc})


def clean(cell) -> str:
    """
    Returns the cleaned-up contents of the cell. This removes unreadable characters, compresses the whitespace into a
    single space, and removes any footnotes.

    :param cell: The contents of the cell, which can be an HTML element or a string. If it is an HTML element,
    its text is used.
    :return:
    """
    if not isinstance(cell, str):
        cell = cell.text
    s = re.sub(r'\s{2,}', ' ', cell.strip())
    s = s.replace(u'\u200c', '').strip()  # Discard the zero-width non-joiners
    return re.sub(r'\s*[\[*].*', '', s, flags=re.DOTALL)  # Discard footnotes


def to_desc(text):
    """
    Returns the description text from the string contents of the cell, removing footnotes and adding a period to the
    end of the sentence if it ends without any punctuation.
    """
    text = re.sub(r'\[[^]]*]', '', text)
    if text[-1] not in '.!?':
        return text + '.'
    return text


def camel_to_name(camel, sep=' ') -> str:
    """
    :return: The input string mapped from "CamelCase" to "Camel Case".
    """
    return re.sub(r'([a-z])([A-Z]+)', r'\1' + sep + r'\2', camel)


rom_val = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
for digit in tuple(rom_val.keys()):
    rom_val[digit.lower()] = rom_val[digit]


def roman_to_int(s):
    """
    Converts a Roman numeral to an int. (Much more than we need, but copy/paste is easier than thinking.)
    """
    int_val = 0
    # Remove anything after the roman numeral
    s = re.sub(fr'[^{"".join(rom_val.keys())}].*', '', s.strip())
    for i in range(len(s)):
        if i > 0 and rom_val[s[i]] > rom_val[s[i - 1]]:
            int_val += rom_val[s[i]] - 2 * rom_val[s[i - 1]]
        else:
            int_val += rom_val[s[i]]
    return int_val


class TeamOptions(PageEnumDesc):
    """Generates the Team Options data. """

    def __init__(self):
        super().__init__('TeamOption', WIKI + 'Commands/team', 'team_options')
        vis = ['never', 'hideForOtherTeams', 'hideForOwnTeam', 'always']
        self.data = {
            "displayName": '"JsonDef"',
            "color": '"JsonDef"',
            "friendlyFire": bool,
            "seeFriendlyInvisibles": bool,
            "nametagVisibility": vis,
            "deathMessageVisibility": vis,
            "collisionRule": ['always', 'never', 'pushOtherTeams', 'pushOwnTeam'],
            "prefix": '"JsonDef"',
            "suffix": '"JsonDef"'}

    def fetch(self):
        tab = '<table>'
        html_time, real = super().fetch()
        arg = real.find('span', id='Arguments')
        for p in arg.find_all_next('p'):
            if p.text == '<option>\n':
                dl = p.find_next('dl')
                for li in dl.find_all('li'):
                    colon = li.text.index(':')
                    name = li.text[:colon]
                    desc = li.text[colon + 1:].strip()
                    tab += f'<tr><td>{name}</td><td>{desc}</td></tr>'
        tab += '</table>'
        return html_time, BeautifulSoup(tab, 'html.parser')

    def find_tables(self, soup):
        return soup.find_all('table')

    def header(self, col: int, text: str):
        pass

    def added_fields(self):
        return ['type']

    def added_values(self, value):
        type = self.data[value]
        type_str = 'str' if type == str else 'bool' if type == bool else type
        return f', {type_str}'

    def extract(self, cols) -> tuple[str, str, str]:
        return camel_to_name(cols[0].text), cols[0].text, cols[1].text


class Advancement(PageEnumDesc):
    """ Generates the 'Advancement' enum. """

    def __init__(self):
        super().__init__('Advancement', WIKI + 'Advancement#List_of_advancements', 'advancements')
        self.value_col = None
        self.desc_col = None
        self.name_col = None

    def header(self, col: int, text: str):
        if text == 'Advancement':
            self.name_col = col
        elif text.startswith('Resource'):
            self.value_col = col
        elif text.find('description') >= 0:
            self.desc_col = col
        else:
            pass

    def extract(self, cols):
        return (clean(x.text) for x in (cols[self.name_col], cols[self.value_col].next, cols[self.desc_col]))

    def replace(self, name, value):
        if name == 'THE_END' and value.startswith('story'):
            return 'ENTER_THE_END'
        return name


class Effect(PageEnumDesc):
    """ Generates the 'Effect' enum. """

    def __init__(self):
        super().__init__('Effect', WIKI + 'Effect?so=search#Effect_list', 'Effects')
        self.id_col = None
        self.desc_col = None
        self.value_col = None
        self.name_col = None
        self.type_col = None
        self.types = {}
        self.ids = {}

    def header(self, col: int, text: str):
        if text == 'Display name':
            self.name_col = col
        elif text.startswith('Name'):
            self.value_col = col
        elif text.find('Effect') >= 0:
            self.desc_col = col
        elif text.find('ID (JE)') >= 0:
            self.id_col = col
        elif text.find('Type') >= 0:
            # Used to generate a method that returns the positive- or negative-ness of the effect.
            self.type_col = col
        else:
            pass

    def extract(self, cols):
        if 'N/A' in cols[self.id_col].text:
            # Filter out non-Java-Edition effects.
            return None
        type_desc = cols[self.type_col].text
        name = clean(cols[self.value_col])
        self.types[name] = True if 'Positive' in type_desc else False if 'Negative' in type_desc else None
        self.ids[name] = int(clean(cols[self.id_col]))
        return (clean(cols[x].text) for x in (self.name_col, self.value_col, self.desc_col))

    def added_fields(self):
        return ['positive', 'id']

    def added_values(self, value):
        return f', "{self.types[value]}", "{self.ids[value]}"'


class Enchantment(PageEnumDesc):
    """ Generates the 'Enchantment' enum. """

    def __init__(self):
        super().__init__('Enchantment', WIKI + 'Enchanting#Summary_of_enchantments',
                         'Summary of enchantments')
        self.max_col = None
        self.name_col = None
        self.desc_col = None
        self.maxes = {}

    def header(self, col: int, text: str):
        if text == 'Name':
            self.name_col = col
        elif text == 'Summary':
            self.desc_col = col
        elif text.startswith('Max'):
            # Used to generate a method that returns the max level of the enchantment.
            self.max_col = col
        else:
            pass

    def extract(self, cols):
        name = clean(cols[self.name_col])
        name = re.sub(r'\s{2,}', ' ', name)
        value = name.lower().replace(' ', '_')
        desc = clean(cols[self.desc_col])
        self.maxes[value] = roman_to_int(clean(cols[self.max_col].text))
        return name, value, desc

    def added_fields(self):
        return ['max_level']

    def added_values(self, value):
        return f', {self.maxes[value]}'


class GameRule(PageEnumDesc):
    """ Generates the 'GameRule' enum. """

    def __init__(self):
        super().__init__('GameRule', WIKI + 'Game_rule?so=search#List_of_game_rules', None)
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

    def header(self, col: int, text: str):
        if text.lower() == 'rule name':
            self.value_col = col
        elif text == 'Description':
            self.desc_col = col
        elif text == 'Type':
            self.type_col = col
        elif text == 'Availability':
            # Filter out unavailable game rules.
            self.filter_col = col
        elif text == 'Java':
            # Yes this is weird. This is in a nested table, which is the original filter_cal
            self.filter_col += col
        else:
            pass

    def extract(self, cols):
        if 'yes' not in cols[self.filter_col].text.lower():
            return None
        value = clean(cols[self.value_col].text)
        name = camel_to_name(value)
        self.types[value] = 'int' if clean(cols[self.type_col]).lower() == 'int' else 'bool'
        return name, value, clean(cols[self.desc_col])

    def added_fields(self):
        return ['rule_type']

    def added_values(self, value):
        return f', {self.types[value]}'


class Particle(PageEnumDesc):
    """ Generates the 'Particle' enum. """

    def __init__(self):
        super().__init__('Particle', WIKI + 'Particles_(Java_Edition)#Types_of_particles', 'Java Particles')
        self.value_col = None
        self.desc_col = None

    def header(self, col: int, text: str):
        if text == 'ID':
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


class PotterySherd(PageEnumDesc):
    """Generates the PotterySherd enum."""

    def __init__(self):
        super().__init__('PotterySherd', WIKI + 'Pottery_Sherd', 'Pottery Sherds')
        self.value_col = None
        self.desc_col = None
        self.done = False

    def find_tables(self, soup):
        v = soup.select('table.sortable')[:1]
        return v

    def header(self, col: int, text: str):
        if text.endswith('Item'):
            self.value_col = col

    def extract(self, cols) -> tuple[str, str, str] | None:
        if self.done:
            return None
        name = clean(cols[self.value_col])
        value = name.lower().replace(' ', '_')
        return name, value, ''


class ScoreCriteria(PageEnumDesc):
    """ Generates the 'ScoreCriteria' enum. """

    def __init__(self):
        super().__init__('ScoreCriteria', WIKI + 'Scoreboard#Criteria', 'Criteria')
        self.desc_col = None
        self.value_col = None

    def pluralize(self):
        return ''

    def header(self, col: int, text: str):
        if text.endswith('name'):
            self.value_col = col
        elif text.startswith('Description'):
            self.desc_col = col
        else:
            pass

    def extract(self, cols):
        value = clean(cols[self.value_col])
        return camel_to_name(value), value, clean(cols[self.desc_col])


class Biome(PageEnumDesc):
    def __init__(self):
        super().__init__('Biome', WIKI + 'Biome/ID', 'Java Biome IDs')
        self.desc_col = None
        self.value_col = None

    def header(self, col: int, text: str):
        if text.find('Resource') >= 0:
            self.value_col = col
        elif text.find('Name') >= 0:
            self.desc_col = col
        else:
            pass

    def extract(self, cols) -> tuple[str, str, str]:
        value = clean(cols[self.value_col])
        desc = clean(cols[self.desc_col])
        return desc, value, desc


class Pattern(PageEnumDesc):
    """Generates the banner pattern enum."""

    def __init__(self):
        super().__init__('Pattern', WIKI + 'Banner/Patterns', 'patterns')
        self.value_col = self.desc_col = self.name_col = None

    def find_tables(self, soup):
        v = soup.select('table.sortable')[:1]
        return v

    def header(self, col: int, text: str):
        if 'In-game' in text:
            self.desc_col = col
        elif text.startswith('Patter'):
            self.name_col = col
        elif text.startswith('Resource'):
            self.value_col = col

    def extract(self, cols):
        name = clean(cols[self.value_col].text).lower().replace('_', ' ').title()
        return name, clean(cols[self.value_col].next.text), clean(cols[self.desc_col].text)


if __name__ == '__main__':
    known = {}


    def add_to_known(v: str, value: str, suffix=None) -> str:
        if v in known and value != known[v]:
            if suffix is None:
                raise ValueError(f'Duplicate: {v}: {known[v]} vs. {value}')
            v = f'{v}_{suffix}'
        known[v] = value
        return v


    dir = Path(__file__).parent.parent
    for f in glob.glob(f'{dir}/*.py'):
        for i, line in enumerate(open(f)):
            m = re.fullmatch(r"([A-Z_0-9]+) = '(.*)'\n", line)
            if m:
                known[m.group(1)] = m.group(2)

    # p = pkgutil.iter_modules(pynecraft.__path__)
    # for module in base, commands, function, simpler:
    #     for v in filter(lambda x: re.fullmatch(r'[A-Z_0-9]+', x), dir(module)):
    #         value = getattr(module, v)
    #         if isinstance(value, str):
    #             v = add_to_known(v, value)
    with open(cwd / '..' / 'values.py', 'r+') as out:
        top = []
        for line in out:
            top.append(line)
            if line.startswith('# Generated values:'):
                break
        out.seek(0, 0)
        out.truncate(0)

        out.writelines(top)
        with redirect_stdout(out):
            print('')
            for tab in (
                    TeamOptions(),
                    Pattern(), Advancement(), Biome(), Effect(), Enchantment(), GameRule(), ScoreCriteria(),
                    Particle(), PotterySherd()):
                html_time, fields = tab.generate()
                print()
                print()
                print(f'# {tab.name}{tab.pluralize()}')
                print(f'# Derived from {tab.url}, {html_time.astimezone().isoformat(timespec="seconds")}')

                value_fields = ['name', 'value', 'desc']
                value_fields.extend(tab.added_fields())
                names = {}
                dups = f'__{tab.name.lower()}_dups'
                print(f'{dups} = {{}}')
                group = []
                for key in fields:
                    value, desc, name = fields[key]
                    k = key
                    if key not in known:
                        k = add_to_known(key, value, tab.name.upper())
                        print(f'{k} = "{value}"')
                        group.append(k)
                    else:
                        print(f'{dups}["{known[k]}"] = "{value}"')
                        group.append(f'"{value}"')
                group_name = f'{camel_to_name(tab.name, "_").upper()}_GROUP'
                print(f'{group_name} = [')
                print(f'    {", ".join(group)}')
                print(f']')

                map_name = camel_to_name(tab.name, '_').lower() + tab.pluralize()
                print('')
                print(f'{tab.name} = namedtuple("{tab.name}", {value_fields})')
                print(f'{map_name} = {{')
                for key in fields:
                    value, desc, name = fields[key]
                    print(f'    "{key}": {tab.name}("""{name}""", "{value}", """{desc}"""{tab.added_values(value)}), ')
                print(f'}}')

                print('')
                print(f'for __k in tuple({map_name}.keys()):')
                print(f'    v = {map_name}[__k]')
                print(f'    {map_name}[v.name] = v')
                print(f'    {map_name}[v.value] = v')

                print('')
                print('')
                print(f'def as_{tab.name.lower()}(*values: StrOrArg) -> str | Tuple[str, ...]:')
                print(f'    return _as_things({group_name}, {dups}, *values)')
                print('')
