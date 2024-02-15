from __future__ import annotations

from typing import Iterable

from pynecraft.commands import lines


def text_lines(*orig: any) -> Iterable[str]:
    """Converts a number of commands and lines into a sequence of single lines, each terminated by newlines."""
    result = []
    for cmd in lines(orig):
        text = str(cmd)
        if len(text) > 0 or not text.endswith('\n'):
            text += '\n'
        result.append(text)
    return result
