#!/usr/bin/env python

"""
Rebuilds pynecraft/values.py from Minecraft client jar data reports.

Usage: python build_values.py [version]

If version is omitted, reads it from ~/clean/home/../mmc-pack.json.
The client jar is expected at:
  /Applications/MultiMC.app/Data/libraries/com/mojang/minecraft/{version}/minecraft-{version}-client.jar
"""

from __future__ import annotations

import datetime
import glob
import unicodedata
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from contextlib import redirect_stdout
from pathlib import Path

import requests

_utils_dir = Path(__file__).parent
_HOME_LINK = Path.home() / 'clean/home'
_SERVER_JAR_PATTERN = Path.home() / 'clean/default_resourcepack/versions/{v}/server-{v}.jar'
_CLIENT_JAR_PATTERN = Path('/Applications/MultiMC.app/Data/libraries/com/mojang/minecraft/{v}/minecraft-{v}-client.jar')


def _mc_version() -> str:
    pack = _HOME_LINK.resolve().parent / 'mmc-pack.json'
    if pack.exists():
        data = json.loads(pack.read_text())
        for comp in data.get('components', []):
            if comp.get('uid') == 'net.minecraft':
                return comp['version']
    raise FileNotFoundError(f'Cannot determine Minecraft version from {pack}')


class _McData:
    """Holds generated reports and lang data from a Minecraft jar run."""

    def __init__(self, version: str):
        server_jar = self._get_cached_server_jar(version)
        client_jar = Path(str(_CLIENT_JAR_PATTERN).replace('{v}', version))
        if not server_jar.exists():
            raise FileNotFoundError(f'Server jar not found: {server_jar}')
        if not client_jar.exists():
            raise FileNotFoundError(f'Client jar not found: {client_jar}')
        self._tmp = tempfile.mkdtemp(prefix='pynecraft_build_')
        tmp = Path(self._tmp)
        shutil.copy2(server_jar, tmp)

        cmd = ['java', '-DbundlerMainClass=net.minecraft.data.Main', '-jar', str(server_jar.name), '--output', '.',
               '--all']
        try:
            subprocess.run(cmd, cwd=tmp, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            print(f'Failed to generate data: {e.stderr}')
            raise e

        with zipfile.ZipFile(client_jar) as zf:
            lang_bytes = zf.read('assets/minecraft/lang/en_us.json')
        self.lang: dict = json.loads(lang_bytes)

        self._generated = tmp

    def _get_cached_server_jar(self, version_id):
        # 1. Use the correct Mojang API endpoint
        manifest_url = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"
        manifest = requests.get(manifest_url).json()

        version_entry = next((v for v in manifest['versions'] if v['id'] == version_id), None)
        if not version_entry:
            raise ValueError(f"Version {version_id} not found in Mojang manifest.")

        version_meta = requests.get(version_entry['url']).json()

        server_data = version_meta['downloads']['server']
        server_url = server_data['url']
        expected_sha1 = server_data['sha1']

        cache_dir = _utils_dir / '.pynecraft_cache'
        cache_dir.mkdir(exist_ok=True)
        jar_path = cache_dir / f'server-{version_id}.jar'

        if jar_path.exists():
            file_hash = hashlib.sha1(jar_path.read_bytes()).hexdigest()
            if file_hash == expected_sha1:
                print(f'Using cached JAR: {jar_path.name}')
                return jar_path

        print(f'Downloading server JAR for {version_id}...')
        response = requests.get(server_url, stream=True, verify=False)
        response.raise_for_status()
        with open(jar_path, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        return jar_path

    def load(self, *parts) -> dict:
        return json.loads((self._generated / Path(*parts)).read_text())

    def registries(self) -> dict:
        return self.load('reports/registries.json')

    def commands(self) -> dict:
        return self.load('reports/commands.json')

    def glob(self, pattern: str):
        return sorted((self._generated / 'data/minecraft').glob(pattern))


_data: _McData | None = None


def _get_data() -> _McData:
    global _data
    if _data is None:
        raise RuntimeError('_McData not initialized; run as __main__')
    return _data


def _lang() -> dict:
    return _get_data().lang


def _registries() -> dict:
    return _get_data().registries()


def _commands() -> dict:
    return _get_data().commands()


noinspection = '# noinspection SpellCheckingInspection,GrazieInspection'

_camel_re = re.compile(r'([a-z])([A-Z]+)')


def _camel_to_name(camel, sep=' '):
    return _camel_re.sub(r'\1' + sep + r'\2', camel)


def _snake_to_camel(s):
    parts = s.split('_')
    return parts[0] + ''.join(p.capitalize() for p in parts[1:])


def _titlecase(s):
    return ' '.join(w.capitalize() for w in s.split())


def _load(path: Path) -> dict:
    return json.loads(path.read_text())


def _registry_stems(reg, key):
    return sorted(k.replace('minecraft:', '') for k in reg[key]['entries'])


def _key_from_name(name, value=None, suffix=None):
    normalized = unicodedata.normalize('NFD', name).encode('ascii', 'ignore').decode()
    k = re.sub(r'[^\w\s]', '', normalized).upper().replace(' ', '_')
    return k


# ---- per-category data builders ----

def _team_options():
    d = _commands()
    opts = d['children']['team']['children']['modify']['children']['team']['children']
    fields = {}
    for opt_name in sorted(opts):
        opt = opts[opt_name]
        children = opt.get('children', {})
        literal_keys = sorted(k for k, v in children.items() if v.get('type') == 'literal')
        arg_parsers = [v.get('parser') for v in children.values() if v.get('type') == 'argument']
        if arg_parsers:
            if 'brigadier:bool' in arg_parsers:
                opt_type = bool
            else:
                opt_type = 'Nbt'
        elif literal_keys:
            opt_type = literal_keys
        else:
            opt_type = str
        display_name = _camel_to_name(opt_name)
        key = _key_from_name(display_name)
        fields[key] = (opt_name, '', display_name, opt_type)
    return fields


def _patterns():
    lang = _lang()
    fields = {}
    for f in _get_data().glob('banner_pattern/*.json'):
        stem = f.stem
        d = _load(f)
        tk = d.get('translation_key', '')
        # translation_key is like 'block.minecraft.banner.stripe_bottom'; no bare display name
        name = _titlecase(stem.replace('_', ' '))
        key = _key_from_name(name)
        fields[key] = (stem, name, name)
    return fields


def _advancements():
    lang = _lang()
    fields = {}
    adv_root = _get_data()._generated / 'data/minecraft/advancement'
    for cat_dir in sorted(adv_root.iterdir()):
        cat = cat_dir.name
        if cat == 'recipes':
            continue
        for f in sorted(cat_dir.glob('*.json')):
            stem = f.stem
            value = f'{cat}/{stem}'
            d = _load(f)
            display = d.get('display', {})
            title_tk = display.get('title', {}).get('translate', '')
            desc_tk = display.get('description', {}).get('translate', '')
            title = lang.get(title_tk, '')
            if not title:
                continue
            desc = lang.get(desc_tk, '')
            key = _key_from_name(title)
            if key in fields:
                key = f'{key}_{cat.upper()}'
            fields[key] = (value, desc, title)
    return fields


def _biomes():
    lang = _lang()
    fields = {}
    for f in _get_data().glob('worldgen/biome/*.json'):
        stem = f.stem
        name = lang.get(f'biome.minecraft.{stem}', _titlecase(stem.replace('_', ' ')))
        key = _key_from_name(name)
        fields[key] = (stem, name, name)
    return fields


def _effects():
    lang = _lang()
    reg = _registries()
    fields = {}
    for stem in _registry_stems(reg, 'minecraft:mob_effect'):
        name = lang.get(f'effect.minecraft.{stem}', _titlecase(stem.replace('_', ' ')))
        key = _key_from_name(name)
        fields[key] = (stem, '', name)
    return fields


def _enchantments():
    lang = _lang()
    fields = {}
    for f in _get_data().glob('enchantment/*.json'):
        stem = f.stem
        d = _load(f)
        tk = d.get('description', {}).get('translate', '')
        name = lang.get(tk, _titlecase(stem.replace('_', ' ')))
        max_level = d.get('max_level', 1)
        key = _key_from_name(name)
        fields[key] = (stem, '', name, max_level)
    return fields


def _gamerules():
    lang = _lang()
    d = _commands()
    gr_children = d['children']['gamerule']['children']
    fields = {}
    for snake in sorted(gr_children):
        if ':' in snake:
            continue
        camel = _snake_to_camel(snake)
        desc = lang.get(f'gamerule.{camel}.description', lang.get(f'gamerule.{camel}', ''))
        children = gr_children[snake].get('children', {})
        parsers = [v.get('parser') for v in children.values() if v.get('type') == 'argument']
        rule_type = 'int' if 'brigadier:integer' in parsers else 'bool'
        name = _camel_to_name(camel)
        key = _key_from_name(name)
        fields[key] = (snake, desc, name, rule_type)
    return fields


def _particles():
    reg = _registries()
    fields = {}
    for stem in _registry_stems(reg, 'minecraft:particle_type'):
        name = _titlecase(stem.replace('_', ' '))
        key = _key_from_name(name)
        fields[key] = (stem, '', name)
    return fields


def _pottery_sherds():
    lang = _lang()
    reg = _registries()
    fields = {}
    for stem in _registry_stems(reg, 'minecraft:decorated_pot_pattern'):
        item_id = f'{stem}_pottery_sherd'
        name = lang.get(f'item.minecraft.{item_id}')
        if not name:
            continue
        key = _key_from_name(name)
        fields[key] = (item_id, None, name)
    return fields


_DISC_NUMBERS = {13: 'thirteen', 11: 'eleven', 5: 'five'}


def _discs():
    lang = _lang()
    fields = {}
    for f in _get_data().glob('jukebox_song/*.json'):
        stem = f.stem
        d = _load(f)
        tk = d.get('description', {}).get('translate', '')
        full_name = lang.get(tk, '')
        if ' - ' in full_name:
            composer, title = full_name.split(' - ', 1)
        else:
            composer, title = '', full_name
        # numbered discs: convert digit title to word
        try:
            num = int(stem)
            title = _DISC_NUMBERS.get(num, str(num))
        except ValueError:
            pass
        value = f'music_disc_{stem}'
        key = _key_from_name(title if title else stem)
        fields[key] = (value, None, title if title else stem, composer)
    return fields


def _paintings():
    lang = _lang()
    fields = {}
    seen_titles = {}
    for f in _get_data().glob('painting_variant/*.json'):
        stem = f.stem
        d = _load(f)
        tk_title = d.get('title', {}).get('translate', '')
        tk_author = d.get('author', {}).get('translate', '')
        base_title = lang.get(tk_title, _titlecase(stem.replace('_', ' ')))
        artist = lang.get(tk_author, '')
        size = (d.get('width', 1), d.get('height', 1))
        if base_title in seen_titles:
            seen_titles[base_title] += 1
            title = f'{base_title} {seen_titles[base_title]}'
        else:
            seen_titles[base_title] = 1
            title = base_title
        key = _key_from_name(title)
        fields[key] = (stem, None, title, artist, size)
    return fields


# ---- output helpers ----

def _type_str(t):
    if t is bool:
        return 'bool'
    if t is str:
        return 'str'
    return repr(t)


def _section(out_name, plural, extra_fields, builder, known, added_values_fn=None):
    print()
    print()
    print(f'# {out_name}{plural}')
    _emit_section(out_name, plural, extra_fields, builder(), known, added_values_fn=added_values_fn)


def _emit_section(out_name, plural, extra_fields, fields, known, added_values_fn=None):
    """Emit one section of values.py for the given category."""
    dups_name = f'__{out_name.lower()}_dups'
    group_name = f'{_camel_to_name(out_name, "_").upper()}_GROUP'
    map_name = _camel_to_name(out_name, '_').lower() + plural
    value_fields = ['name', 'value', 'desc'] + list(extra_fields)

    print(f'{dups_name} = {{}}')

    group = []
    for key in sorted(fields.keys()):
        row = fields[key]
        value = row[0]
        k = key
        if key not in known:
            k = _add_to_known(known, key, value, out_name.upper())
            print(f'{k} = "{value}"')
            group.append(k)
        else:
            if known[k] != value:
                print(f'{dups_name}["{known[k]}"] = "{value}"')
            group.append(f'"{value}"')

    print(f'{group_name} = [')
    print(f'    {", ".join(group)}')
    print(f']')

    print()
    print(f'{out_name}Info = namedtuple("{out_name}", {value_fields})')
    print(f'{map_name} = {{')
    for key, row in sorted(fields.items()):
        value = row[0]
        desc = row[1]
        display_name = row[2]
        extras = row[3:]
        desc_str = f'"""{desc}"""' if desc else 'None'
        extra_str = ''
        if added_values_fn:
            extra_str = added_values_fn(value, extras)
        print(f'    "{key}": {out_name}Info("""{display_name}""", "{value}", {desc_str}{extra_str}),')
    print(f'}}')

    print()
    print(f'for __k in tuple({map_name}.keys()):')
    print(f'    v = {map_name}[__k]')
    print(f'    {map_name}[v.name] = v')
    print(f'    {map_name}[v.value] = v')

    print()
    print()
    print(f'def as_{out_name.lower()}(*values: StrOrArg) -> str | Tuple[str, ...]:')
    print(f'    return _as_things({group_name}, {dups_name}, *values)')
    print()


def _add_to_known(known, k, value, suffix=None):
    if k in known and value != known[k]:
        if suffix is None:
            raise ValueError(f'Duplicate: {k}: {known[k]} vs. {value}')
        k = f'{k}_{suffix}'
    known[k] = value
    return k


if __name__ == '__main__':
    _version = sys.argv[1] if len(sys.argv) > 1 else _mc_version()
    _data = _McData(_version)

    known = {}

    dir_ = _utils_dir.parent
    for f in glob.glob(f'{dir_}/*.py'):
        for line in open(f):
            m = re.fullmatch(r"([A-Z_0-9]+) = '(.*)'\n", line)
            if m:
                known[m.group(1)] = m.group(2)

    timestamp = datetime.datetime.now().astimezone().isoformat(timespec='seconds')

    with open(_utils_dir / '..' / 'values.py', 'r+') as out:
        top = []
        for line in out:
            top.append(line)
            if line.startswith('# Generated values:'):
                break
        out.seek(0, 0)
        out.truncate(0)
        out.writelines(top)

        with redirect_stdout(out):
            print()
            print(f'# Generated from Minecraft {_version} jar data, {timestamp}')

            _section('TeamOption', 's', ['type'], _team_options, known,
                     added_values_fn=lambda v, extras: f', {_type_str(extras[0])}')
            _section('Pattern', 's', [], _patterns, known)
            _section('Advancement', 's', [], _advancements, known)
            _section('Biome', 's', [], _biomes, known)
            _section('Effect', 's', [], _effects, known)
            _section('Enchantment', 's', ['max_level'], _enchantments, known,
                     added_values_fn=lambda v, extras: f', {extras[0]}')
            _section('GameRule', 's', ['rule_type'], _gamerules, known,
                     added_values_fn=lambda v, extras: f', {extras[0]}')
            _section('Particle', 's', [], _particles, known)
            _section('PotterySherd', 's', [], _pottery_sherds, known)
            _section('Disc', 's', ['composer'], _discs, known,
                     added_values_fn=lambda v, extras: f', "{extras[0]}"')
            _section('Painting', 's', ['artist', 'size'], _paintings, known,
                     added_values_fn=lambda v, extras: f', "{extras[0]}", {extras[1]}')
