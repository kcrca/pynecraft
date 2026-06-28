"""Implementation code for wrapping text into a given width."""

from __future__ import annotations

import re
import textwrap
import unicodedata
from dataclasses import dataclass

from pynecraft._font_data import CHAR_WIDTHS, MISSING
from pynecraft.commands import Text


@dataclass
class _Span:
    text: str
    bold: bool = False
    italic: bool = False
    color: str | None = None
    underlined: bool = False
    strikethrough: bool = False
    click_event: dict | None = None

    def same_fmt(self, other: '_Span') -> bool:
        return (self.bold == other.bold and self.italic == other.italic and self.color == other.color
                and self.underlined == other.underlined and self.strikethrough == other.strikethrough
                and self.click_event == other.click_event)


def _char_advance(ch: str, bold: bool) -> float:
    if not ch.isascii():
        # Non-ASCII: wide (CJK etc.) = 8px, narrow = 4px, bold adds nothing.
        return 8.0 if unicodedata.east_asian_width(ch) in ('W', 'F') else 4.0
    normal, bold_adv = CHAR_WIDTHS.get(ch, MISSING)
    return bold_adv if bold else normal


def _str_advance(s: str, bold: bool) -> float:
    return sum(_char_advance(ch, bold) for ch in s)


def _spans_from_item(item: str | Text, *, _bold: bool = False, _italic: bool = False, _color: str | None = None,
                     _underlined: bool = False, _strikethrough: bool = False, _click_event: dict | None = None) -> list[_Span]:
    if isinstance(item, str):
        s = textwrap.dedent(item)
        s = re.sub(r'\n\n+', '\x00', s)
        s = s.replace('\n', ' ')
        s = s.replace('\x00', '\n')
        return [_Span(s, _bold, _italic, _color, _underlined, _strikethrough, _click_event)]
    text = item.get('text', '')
    if not isinstance(text, str):
        text = str(text)
    item_bold = item['bold'] if 'bold' in item else _bold
    item_italic = item['italic'] if 'italic' in item else _italic
    item_color = item.get('color') or _color
    item_underlined = item['underlined'] if 'underlined' in item else _underlined
    item_strikethrough = item['strikethrough'] if 'strikethrough' in item else _strikethrough
    item_click_event = item.get('click_event') or _click_event
    spans = [_Span(text, item_bold, item_italic, item_color, item_underlined, item_strikethrough, item_click_event)] if text else []
    for child in item.get('extra', []):
        if isinstance(child, str):
            if child:
                spans.append(_Span(child, item_bold, item_italic, item_color, item_underlined, item_strikethrough, item_click_event))
        else:
            spans.extend(_spans_from_item(child, _bold=item_bold, _italic=item_italic, _color=item_color,
                                          _underlined=item_underlined, _strikethrough=item_strikethrough,
                                          _click_event=item_click_event))
    return spans


def _line_to_text(spans: list[_Span]) -> Text:
    if not spans:
        return Text.text('')
    merged = [_Span(spans[0].text, spans[0].bold, spans[0].italic, spans[0].color,
                    spans[0].underlined, spans[0].strikethrough, spans[0].click_event)]
    for span in spans[1:]:
        last = merged[-1]
        if span.same_fmt(last):
            last.text += span.text
        else:
            merged.append(_Span(span.text, span.bold, span.italic, span.color,
                                span.underlined, span.strikethrough, span.click_event))

    def _to_text(s: _Span) -> Text:
        t = Text.text(s.text)
        if s.bold:
            t = t.bold()
        if s.italic:
            t = t.italic()
        if s.underlined:
            t = t.underlined()
        if s.strikethrough:
            t = t.strikethrough()
        if s.color:
            t = t.color(s.color)
        if s.click_event:
            t['click_event'] = s.click_event
        return t

    texts = [_to_text(s) for s in merged]
    if len(texts) == 1:
        return texts[0]
    result = Text.text('')
    result.extra(*texts)
    return result


def wrap(width: int, lines: int, *items: str | Text) -> list[list[Text]]:
    """Wrap items into pages of lines fit to width pixels.

    Strings are plain text (like Text.text(s)). Use Text.from_html() for formatted input.
    Single newlines are soft breaks (spaces); blank lines (\\n\\n) are hard breaks.
    Common leading whitespace is stripped (triple-quoted strings work naturally).
    Text objects pass through using their bold/italic/color/extra fields.

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

    pending_newlines = 0

    for span in all_spans:
        for token in re.split(r'(\n|[^\S\xa0])', span.text):
            if not token:
                continue
            if token == '\n':
                pending_newlines += 1
                continue
            if pending_newlines:
                if cur_line:
                    _flush_line()
                for _ in range(pending_newlines - 1):
                    _flush_line()
                pending_newlines = 0
            if cur_width == 0.0 and not token.strip():
                continue
            token_advance = _str_advance(token, span.bold)
            if cur_width + token_advance <= width:
                cur_line.append(_Span(token, span.bold, span.italic, span.color, span.underlined, span.strikethrough, span.click_event))
                cur_width += token_advance
            else:
                if cur_line:
                    _flush_line()
                if token.strip():
                    cur_line.append(_Span(token, span.bold, span.italic, span.color, span.underlined, span.strikethrough, span.click_event))
                    cur_width = token_advance

    if cur_line:
        _flush_line()
    if cur_page:
        _flush_page()

    return pages