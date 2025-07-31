# import mcfonts
#
# font = mcfonts.from_java_font_file(Path('/Users/arnold/clarity/default_resourcepack/assets/minecraft/font/default.json'))
# print('hi')
import re

from PIL import ImageFont

from pynecraft.commands import TextDef, as_text


def _hash(d: dict):
    return tuple(d.items())


fonts = {
    (False, False): ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial", 12),
    (True, False): ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold", 12),
    (False, True): ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Italic", 12),
    (True, True): ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold Italic",
                                     12),
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

    def add(self, *text: TextDef):
        texts = [as_text(t) for t in text]
        while texts:
            t = texts.pop()
            if self._cur_page == len(self._pages):
                self._pages.append([t])
            else:
                self._pages[self._cur_page].append(t)
            types = self._types
            types[0] = t['bold'] if 'bold' in t else False
            types[1] = t['italic'] if 'italic' in t else False
            font = fonts[tuple(types)]
            if 'text' in t:
                txt = t['text']
                pos = 0
                # build a new version of the text with inserted newlines where needed
                new_text = ''
                for token in re.split(r'(\s)', txt):
                    bbox = font.getbbox(token)
                    width = bbox[2] - bbox[0]
                    pos += len(token)
                    if token == '\n':
                        # This is a newline
                        self._cur_width = 0
                        new_text += token
                    elif self._cur_width + width < self._max_width:
                        self._cur_width += width
                        new_text += token
                    else:
                        new_text += '\n'
                        self._cur_width = 0
                        if not re.match(' +', token):
                            new_text += token
                            self._cur_width = width
                # Add lines, and if there are too many, start a new page
                new_lines = new_text.count('\n')
                if self._cur_line + new_lines < self._max_lines:
                    self._cur_line += new_lines
                    t['text'] = new_text
                else:
                    split_pos = -1
                    for i in range(self._max_lines - self._cur_line):
                        split_pos = new_text.find('\n', split_pos + 1)
                    next_text = new_text[split_pos + 1:]
                    t['text'] = new_text[:split_pos]
                    new_node = t.copy()
                    new_node['text'] = next_text
                    self._cur_page += 1
                    texts = [new_node] + texts
        return self


