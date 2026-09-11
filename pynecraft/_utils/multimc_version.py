#!/usr/bin/env python3

"""
Sets the Minecraft version in data.cfg from a local MultiMC install.

Usage: python multimc_version.py [-n]

This is a convenience for one particular setup: it reads the version out of the mmc-pack.json of the MultiMC instance
that ~/clean/home points into. Editing data.cfg by hand does the same job anywhere else.

It rebuilds nothing. Run build_data.py afterwards to regenerate the data for the new version.
"""

from __future__ import annotations

import configparser
import json
import sys
from pathlib import Path

_utils_dir = Path(__file__).parent
_CONFIG_FILE = _utils_dir / 'data.cfg'
_HOME_LINK = Path.home() / 'clean/home'


def _multimc_version() -> str:
    pack = _HOME_LINK.resolve().parent / 'mmc-pack.json'
    if not pack.exists():
        raise FileNotFoundError(f'No MultiMC pack file at {pack}')
    data = json.loads(pack.read_text())
    for comp in data.get('components', []):
        if comp.get('uid') == 'net.minecraft':
            return comp['version']
    raise ValueError(f'No net.minecraft component in {pack}')


def _update(dry_run: bool) -> None:
    version = _multimc_version()
    config = configparser.ConfigParser()
    if not config.read(_CONFIG_FILE):
        raise FileNotFoundError(f'Cannot read {_CONFIG_FILE}')
    was = config['minecraft']['version']
    if was == version:
        print(f'version already {version}')
        return
    change = f'{_CONFIG_FILE.name}: version {was!r} -> {version!r}'
    if dry_run:
        print(f'{change} (not written)')
        return
    config['minecraft']['version'] = version
    with open(_CONFIG_FILE, 'w') as out:
        config.write(out)
    print(change)
    print('next: python -m pynecraft._utils.build_data')


if __name__ == '__main__':
    _args = sys.argv[1:]
    _dry_run = bool(_args) and _args[0] in ('-n', '--dry-run')
    if _dry_run:
        _args.pop(0)
    if _args:
        print(f'Usage: {Path(__file__).name} [-n]', file=sys.stderr)
        sys.exit(2)
    try:
        _update(_dry_run)
    except (FileNotFoundError, ValueError) as _e:
        print(_e, file=sys.stderr)
        sys.exit(1)
