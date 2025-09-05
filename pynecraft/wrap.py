# import mcfonts
#
# font = mcfonts.from_java_font_file(Path('/Users/arnold/clarity/default_resourcepack/assets/minecraft/font/default.json'))
# print('hi')
from __future__ import annotations

import re

from PIL import ImageFont

from pynecraft.commands import TextDef, as_text


def _hash(d: dict):
    return tuple(d.items())


fonts = {
    (False, False): ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial", 12),
    (True, False): ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold", 12),
    (False, True): ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Italic", 12),
    (True, True): ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold Italic", 12),
}


class BookWrap:
    def __init__(self):
        self._types = [False, False]
        self._pages = []
        self._cur_page = 0
        self._cur_line = 0
        self._cur_width = 0
        self._max_width = 114
        self._max_lines = 14

    def pages(self):
        return self._pages

    def add(self, *text: TextDef) -> BookWrap:
        texts = [as_text(t) for t in text]
        pos = 0
        while texts:
            node = texts.pop()
            if self._cur_page == len(self._pages):
                # We need to start a new page
                self._pages.append([])
            self._pages[self._cur_page].append(node)
            types = self._types
            types[0] = bool(node['bold']) if 'bold' in node else False
            types[1] = bool(node['italic']) if 'italic' in node else False
            font = fonts[tuple(types)]
            if 'text' in node:
                txt = node['text']
                # build a new version of the text with inserted newlines where needed
                new_text = ''
                for token in re.split(r'(\s)', txt):
                    width = self._get_width(font, token)
                    pos += len(token)
                    if token == '\n':
                        # This is a newline
                        self._cur_width = 0
                        new_text += token
                    elif self._cur_width + width < self._max_width:
                        self._cur_width += width
                        new_text += token
                    else:
                        for m in reversed(tuple(x for x in re.finditer(r'[-/]+', token))):
                            sep_pos = m.regs[0][1]
                            subtoken = token[:sep_pos]
                            subwidth = self._get_width(font, subtoken)
                            if self._cur_width + subwidth < self._max_width:
                                self._cur_width += subwidth
                                new_text += subtoken
                                token = token[sep_pos:]
                                width = self._get_width(font, token)
                                break

                        new_text = new_text.rstrip() + '\n'
                        self._cur_width = 0
                        if not re.match(r'\s+', token):
                            new_text += token
                            self._cur_width = width
                # Add lines, and if there are too many, start a new page
                new_lines = new_text.count('\n')
                if self._cur_line + new_lines < self._max_lines:
                    self._cur_line += new_lines
                    node['text'] = new_text
                else:
                    split_pos = -1
                    for i in range(self._max_lines - self._cur_line):
                        split_pos = new_text.find('\n', split_pos + 1)
                    next_text = new_text[split_pos + 1:]
                    node['text'] = new_text[:split_pos]
                    new_node = node.copy()
                    new_node['text'] = next_text
                    self._cur_page += 1
                    texts = [new_node] + texts
        return self

    def _get_width(self, font, token):
        bbox = font.getbbox(token)
        width = bbox[2] - bbox[0]
        return width
