from __future__ import annotations

import re
from dataclasses import dataclass

from PIL import ImageFont

from pynecraft._font_data import CHAR_WIDTHS, MISSING
from pynecraft.commands import as_text, Text, TextDef


fonts = {
    (False, False): ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial', 12),
    (True, False): ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold', 12),
    (False, True): ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Italic', 12),
    (True, True): ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold Italic', 12),
}

# Regex for markdown: [text]{color}, ***both***, **bold**, *italic*, plain
_MD_RE = re.compile(
    r'\[([^\]]+)\]\{([a-z_#][a-z_0-9]*)\}'
    r'|\*\*\*(.+?)\*\*\*'
    r'|\*\*(.+?)\*\*'
    r'|\*(.+?)\*'
    r'|([^*\[]+|\*|\[)'
)


@dataclass
class _Span:
    text: str
    bold: bool = False
    italic: bool = False
    color: str | None = None


def _char_advance(ch: str, bold: bool) -> float:
    normal, bold_adv = CHAR_WIDTHS.get(ch, MISSING)
    return bold_adv if bold else normal


def _str_advance(s: str, bold: bool) -> float:
    return sum(_char_advance(ch, bold) for ch in s)


def _parse_markdown(text: str) -> list[_Span]:
    spans = []
    for line in text.splitlines(keepends=True):
        m = re.match(r'^#{1,6}\s+', line)
        if m:
            spans.append(_Span(line[m.end():], bold=True))
            continue
        for m in _MD_RE.finditer(line):
            if m.group(1) is not None:
                spans.append(_Span(m.group(1), color=m.group(2)))
            elif m.group(3) is not None:
                spans.append(_Span(m.group(3), bold=True, italic=True))
            elif m.group(4) is not None:
                spans.append(_Span(m.group(4), bold=True))
            elif m.group(5) is not None:
                spans.append(_Span(m.group(5), italic=True))
            elif m.group(6) is not None:
                spans.append(_Span(m.group(6)))
    return spans


def _spans_from_item(item: str | Text) -> list[_Span]:
    if isinstance(item, str):
        return _parse_markdown(item)
    text = item.get('text', '')
    if not isinstance(text, str):
        text = str(text)
    bold = bool(item.get('bold', False))
    italic = bool(item.get('italic', False))
    color = item.get('color') or None
    return [_Span(text, bold, italic, color)] if text else []


def _line_to_text(spans: list[_Span]) -> Text:
    if not spans:
        return Text.text('')
    merged = [_Span(spans[0].text, spans[0].bold, spans[0].italic, spans[0].color)]
    for span in spans[1:]:
        last = merged[-1]
        if span.bold == last.bold and span.italic == last.italic and span.color == last.color:
            last.text += span.text
        else:
            merged.append(_Span(span.text, span.bold, span.italic, span.color))

    def _to_text(s: _Span) -> Text:
        t = Text.text(s.text)
        if s.bold:
            t = t.bold()
        if s.italic:
            t = t.italic()
        if s.color:
            t = t.color(s.color)
        return t

    texts = [_to_text(s) for s in merged]
    if len(texts) == 1:
        return texts[0]
    result = texts[0]
    result.extra(*texts[1:])
    return result


def wrap(width: int, lines: int, *items: str | Text) -> list[list[Text]]:
    """Wrap items into pages of lines fit to width pixels.

    Strings are parsed as a markdown subset:
    - ``**text**`` → bold
    - ``*text*`` → italic
    - ``***text***`` → bold + italic
    - ``# text`` (at start of line) → bold heading
    - ``[text]{color}`` → MC text color (black, dark_green, red, etc.; see TEXT_COLORS)

    Text objects pass through as-is, using their bold/italic/color fields.
    Inline color overrides any dye color set on a sign face.

    Returns a list of pages; each page is a list of Text objects, one per line.
    Words wider than width are placed on their own line rather than split.
    Characters not in the Minecraft font fall back to the missing-glyph advance width.
    """
    all_spans: list[_Span] = []
    for item in items:
        all_spans.extend(_spans_from_item(item))

    pages: list[list[Text]] = []
    cur_page: list[Text] = []
    cur_line: list[_Span] = []
    cur_width = 0.0

    def _flush_page():
        nonlocal cur_page
        pages.append(cur_page)
        cur_page = []

    def _flush_line():
        nonlocal cur_line, cur_width
        while cur_line and not cur_line[-1].text.strip():
            cur_line.pop()
        cur_page.append(_line_to_text(cur_line))
        cur_line = []
        cur_width = 0.0
        if len(cur_page) >= lines:
            _flush_page()

    for span in all_spans:
        for token in re.split(r'(\n|\s)', span.text):
            if not token:
                continue
            if token == '\n':
                _flush_line()
                continue
            token_advance = _str_advance(token, span.bold)
            if cur_width == 0.0 and not token.strip():
                continue
            if cur_width + token_advance <= width:
                cur_line.append(_Span(token, span.bold, span.italic, span.color))
                cur_width += token_advance
            else:
                if cur_line:
                    _flush_line()
                if token.strip():
                    cur_line.append(_Span(token, span.bold, span.italic, span.color))
                    cur_width = token_advance

    if cur_line:
        _flush_line()
    if cur_page:
        _flush_page()

    return pages


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
            # noinspection PyTypeChecker
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

    @staticmethod
    def _get_width(font, token):
        bbox = font.getbbox(token)
        width = bbox[2] - bbox[0]
        return width
