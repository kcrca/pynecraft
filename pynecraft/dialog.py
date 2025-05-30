import string
from typing import Iterable, Self, Sequence, Tuple

from .base import Nbt, NbtDef, _in_group, to_id
from .commands import ClickEvent, TextDef, as_text
from .simpler import Item, _as_tuple

PLAIN_MESSAGE = 'plain_message'
ITEM = 'item'
ELEMENT_TYPES = [PLAIN_MESSAGE, ITEM]

NOTICE = 'notice'
CONFIRMATION = 'confirmation'
MULTI_ACTION = 'multi_action'
SERVER_LINKS = 'server_links'
DIALOG_LIST = 'dialog_list'
DIALOG_TYPES = [NOTICE, CONFIRMATION, MULTI_ACTION, SERVER_LINKS, DIALOG_LIST]

TEXT = 'text'
BOOLEAN = 'boolean'
SINGLE_OPTION = 'single_option'
NUMBER_RANGE = 'number_range'
INPUT_TYPES = [TEXT, BOOLEAN, SINGLE_OPTION, NUMBER_RANGE]

COMMAND_TEMPLATE = 'command_template'
CUSTOM_TEMPLATE = 'custom_template'
CUSTOM_FORM = 'custom_form'
SUBMIT_TYPES = [COMMAND_TEMPLATE, CUSTOM_TEMPLATE, CUSTOM_FORM]

CLOSE = 'close'
NONE = 'none'
WAIT_FOR_RESPONSE = 'wait_for_response'
AFTER_ACTIONS = [CLOSE, NONE, WAIT_FOR_RESPONSE]


class Element(Nbt):
    def __init__(self, type: str, width: int = None):
        super().__init__()
        self['type'] = _in_group(ELEMENT_TYPES, type)
        self.set_if('width', width)

    @classmethod
    def from_nbt(cls, nbt: NbtDef, allow_none=True) -> Self | None:
        if isinstance(nbt, Element) or (allow_none and nbt is None):
            return nbt
        elem = Element(_in_group(SUBMIT_TYPES, nbt.pop('type'), nbt.pop('width', None)))
        elem.update(nbt)
        return elem


def plain_message(contents: TextDef, *, width: int = None) -> Element:
    """Factory method for a plain_message body element."""
    elem = Element(PLAIN_MESSAGE, width)
    elem['contents'] = as_text(contents)
    elem.set_if('width', width)
    return elem


def item(item: NbtDef | Item | str, *, description: TextDef = None, show_decoration: bool = None,
         show_tooltip: bool = None, width: int = None, height: int = None) -> Element:
    """Factory method for an item body component."""
    if isinstance(item, str):
        item = Item.nbt_for(item)
    elif isinstance(item, Item):
        item = Item.nbt_for(item.id)
    elem = Element(ITEM)
    elem['item'] = item
    elem.set_if('description', as_text(description), 'show_decoration', show_decoration, 'show_tooltip', show_tooltip,
                'width', width, 'height', height)
    return elem


def _default_from_label(key, label):
    if key:
        return key
    return to_id(label.translate(str.maketrans('', '', string.punctuation)))


class Input(Nbt):
    def __init__(self, type: str, label: str, key: str = None):
        super().__init__()
        self['type'] = _in_group(INPUT_TYPES, type)
        self['label'] = label
        self['key'] = _default_from_label(key, label)

    @classmethod
    def from_nbt(cls, nbt: NbtDef, allow_none=True) -> Self | None:
        if isinstance(nbt, Input) or (allow_none and nbt is None):
            return nbt
        input = Input(_in_group(INPUT_TYPES, nbt.pop('type')), nbt.pop('label'), nbt.pop('key', None))
        input.update(nbt)
        return input


def boolean(label: str, initial: bool = None, key: str = None, *, on_true: str = None, on_false: str = None) -> Input:
    """Factory method for a boolean (checkbox) input component. Key is handled the same as with text()."""
    input = Input(BOOLEAN, label, key)
    input.set_if('on_true', on_true, 'on_false', on_false, 'initial', initial)
    return input


def single_option(label: str, options: Iterable[NbtDef | str | int | float], key: str = None, *,
                  initial: str | int | float = None, width: int = None, label_visible: bool = None,
                  default_ids=True) -> Input:
    """
    Factory method for a single option input widget. Key is handled the same as with text().

    If an option is a str or number, it becomes an option with the display being that value, but has no ID.

    If an option has no provided ID, it is an error unless default_ids is True, when the ID will be generated
    by running to_id() on the display, after stripping punctuation. If there is no display, it will be "option_N"
    where N is its index in the option list.

    :param label:
    :param options:
    :param key:
    :param initial: The initial value. Formally you would identify an initial value by creating NBT with 'initial': True.
            this parameter lets you set it by putting in the value here instead.
    :param width:
    :param label_visible:
    :param default_ids:
    """

    # Validate / transmogrify options
    def to_nbt_opt(opt):
        if isinstance(opt, (str, int, float)):
            nbt = Nbt(display=str(opt), id=to_id(str(opt)))
            if opt == initial:
                nbt['initial'] = True
            return nbt
        else:
            return Nbt.as_nbt(opt)

    options = tuple(map(to_nbt_opt, _as_tuple(options)))
    if not len(options):
        raise ValueError('options are required')
    found = None
    if isinstance(initial, (int, float)):
        initial = str(initial)
    for i, v in enumerate(options):
        if 'id' not in v:
            try:
                if default_ids:
                    v['id'] = _default_from_label(None, v['display'])
            except KeyError:
                v['id'] = f'option_{i}'
        elif not default_ids:
            raise ValueError(f'id required for {v}')
        try:
            if 'initial' in v and v['initial']:
                if found:
                    raise ValueError(f'only one option can be the initial one: {found, v["display"]}')
                found = v['display']
        except KeyError:
            pass
    if len(set(map(lambda x: x['display'], options))) != len(options):
        raise ValueError('Duplicate options')

    # Build the widget
    input = Input(SINGLE_OPTION, label, key)
    input['options'] = options
    input.set_if('width', width, 'label_visible', label_visible)
    return input


def number_range(label: str, start: int, end: int, step: int = None, key: str = None, *, initial: int = None,
                 width: int = None, label_format: str = None) -> Input:
    """Factory method for a number range component. Key is handled the same as with text()."""
    input = Input(NUMBER_RANGE, label, key)
    input['start'] = start
    input['end'] = end
    input.set_if('step', step, 'initial', initial, 'width', width, 'label_format', label_format)
    return input


def _as_inputs(inputs):
    if isinstance(inputs, NbtDef):
        inputs = (inputs,)
    return tuple(map(lambda x: Input.from_nbt(x), inputs))


def text(label: str, initial: str = None, key: str = None, *, width: int = None, label_visible: bool = None,
         max_length: int = None, multiline: Tuple[int, int] | Tuple[int] | int = None) -> Input:
    """
    Factory method for a text input component.

    :param label:
    :param initial:
    :param key: If not provided, the key will be generated invoking to_id on the label after stripping the punctuation.
    :param width:
    :param max_length:
    :param label_visible:
    :param multiline: If a single int, or a list with a single value, it is used as the height. The second value
    from a list will be max_lines.
    """
    input = Input(TEXT, label, key)
    input.set_if('initial', initial, 'width', width, 'label_visible', label_visible, 'max_length', max_length)
    ml = Nbt()
    if isinstance(multiline, int):
        ml['height'] = multiline
    elif isinstance(multiline, Sequence):
        if len(multiline):
            ml.set_if('height', multiline[0])
            if len(multiline) == 2:
                ml.set_if('max_lines', multiline[1])
            elif len(multiline) > 2:
                raise ValueError('multiline value has at most two values')
    if ml:
        input['multiline'] = ml
    return input


class SubmitType(Nbt):
    def __init__(self, type: str, id: str = None):
        super().__init__()
        self['type'] = _in_group(SUBMIT_TYPES, type)
        self['id'] = _default_from_label(id, type)

    @classmethod
    def from_nbt(cls, nbt: NbtDef, allow_none=True) -> Self | None:
        if isinstance(nbt, SubmitType) or (allow_none and nbt is None):
            return nbt
        submit = SubmitType(_in_group(SUBMIT_TYPES, nbt.pop('type')))
        submit.update(nbt)
        return submit


def command_template(template: str) -> SubmitType:
    """Factory method for a command_template submit action, part of the full submit_action()."""
    action = SubmitType(COMMAND_TEMPLATE)
    action['template'] = template
    return action


def custom_template(template: str, namespace_id: str) -> SubmitType:
    """Factory method for a custom_template submit action, part of the full submit_action()."""
    action = SubmitType(CUSTOM_TEMPLATE)
    action['template'] = template
    action['id'] = namespace_id
    return action


def custom_form(namespace_id: str) -> SubmitType:
    """Factory method for a custom_form submit action, part of the full submit_action()."""
    action = SubmitType(CUSTOM_FORM)
    action['id'] = namespace_id
    return action


def submit_action(label: TextDef, on_submit: SubmitType = None, *, id: str = None, tooltip: str = None,
                  width: int = None) -> Nbt:
    """Factory method for a submit action"""
    id = _default_from_label(id, label)
    nbt = Nbt(label=label, id=id)
    nbt.set_if('tooltip', tooltip, 'width', width, 'on_submit', SubmitType.from_nbt(on_submit))
    return nbt


class ClickAction(Nbt):
    def __init__(self, label: TextDef, on_click: ClickEvent = None, tooltip: str = None, width: int = None):
        super().__init__()
        self['label'] = label
        self.set_if('on_click', on_click, 'tooltip', tooltip, 'width', width)

    @classmethod
    def from_nbt(cls, nbt: NbtDef, allow_none=True) -> Self | None:
        if isinstance(nbt, ClickAction) or (allow_none and nbt is None):
            return nbt
        action = ClickAction(nbt.pop('label'), nbt.pop('on_click', None), nbt.pop('tooltip', None),
                             nbt.pop('width', None))
        action.update(nbt)
        return action


class Dialog(Nbt):
    """
    This class helps you build custom dialog boxes. You generally use one of the factory methods named for the
    possible types (notice, confirmation, etc.).

    Other factory methods build inputs, actions, etc.

    The result is an Nbt object, so if you want to set values this does not provide, you can
    put in any NBT you want.

    Throughout, whenever a text component is needed, a simple string will be handled a text component with that text.
    """

    def __init__(self, type: str, title: TextDef, external_title: TextDef = None):
        """
        Creates a new custom dialog. Typically, you will use one of the factory methods instead of
        invoking this directly. They in turn invoke this with the right type, passing through the
        other parameters to this method.

        :param type: The dialog type.
        :param title: The dialog title.
        :param external_title: The external title, if different from "title"
        """
        super().__init__(type=_in_group(DIALOG_TYPES, type), title=as_text(title))
        self.set_if('external_title', as_text(external_title))

    @classmethod
    def from_nbt(cls, nbt: NbtDef, allow_none=True) -> Self:
        if isinstance(nbt, Dialog) or (allow_none and nbt is None):
            return nbt
        d = Dialog(nbt.pop('type'), nbt.pop('title'), nbt.pop('external_title', None))
        d.update(nbt)
        return d

    def _seq(self, key, value) -> Self:
        if value is None:
            if key in self:
                del self[key]
        else:
            if not isinstance(value, list):
                value = list(value)
            self[key] = value
        return self

    def _prim(self, key, value) -> Self:
        if value is None:
            if key in self:
                del self[key]
        else:
            self[key] = value
        return self

    def body(self, *body: Element | NbtDef) -> Self:
        return self._seq('body', body)

    def inputs(self, *inputs: Input | NbtDef) -> Self:
        return self._seq('inputs', inputs)

    def actions(self, *actions: ClickAction | NbtDef) -> Self:
        return self._seq('actions', actions)

    def pause(self, val: bool | None) -> Self:
        return self._prim('pause', val)

    def after_action(self, val: bool | None) -> Self:
        return self._prim('after_action', _in_group(AFTER_ACTIONS, val))

    def exit_action(self, val: bool | None) -> Self:
        return self._prim('exit_action', val)

    def can_close_with_escape(self, val: bool | None) -> Self:
        return self._prim('can_close_with_escape', val)


def notice(title: TextDef, *, click_action: NbtDef = None, external_title: TextDef = None) -> Dialog:
    """Factory method for a notice dialog."""
    return Dialog(NOTICE, title, external_title).set_if('action', ClickAction.from_nbt(click_action))


def confirmation(title: TextDef, yes_click_action: NbtDef, no_click_action: NbtDef, *,
                 external_title: TextDef = None) -> Dialog:
    """Factory method for a confirmation dialog."""
    d = Dialog(CONFIRMATION, title, external_title)
    d['yes'] = ClickAction.from_nbt(yes_click_action, False)
    d['no'] = ClickAction.from_nbt(no_click_action, False)
    return d


def multi_action(title: TextDef, click_actions: NbtDef | Iterable[NbtDef], *, columns: int = None,
                 exit_action: ClickAction | NbtDef = None, external_title: TextDef = None) -> Dialog:
    """Factory method for a multi_action dialog."""
    d = Dialog(MULTI_ACTION, title, external_title)
    if isinstance(click_actions, Nbt):
        click_actions = (click_actions,)
    d.actions(*tuple(map(lambda x: ClickAction.from_nbt(x), click_actions)))
    d.set_if('columns', columns)
    d.set_if('exit_action', exit_action)
    return d


def server_links(title: TextDef, *, on_click: ClickEvent = None, exit_action: ClickEvent = None,
                 columns: int = None, button_width: int = None, external_title: TextDef = None) -> Dialog:
    """Factory method for a server_links dialog."""
    d = Dialog(SERVER_LINKS, title, external_title)
    d.set_if('on_click', on_click)
    d.set_if('exit_action', exit_action)
    d.set_if('columns', columns)
    d.set_if('button_width', button_width)
    return d


def dialog_list(title: TextDef, dialogs: NbtDef | Iterable[NbtDef], *, exit_action: ClickEvent = None,
                columns: int = None, button_width: int = None, external_title: TextDef = None) -> Dialog:
    """Factory method for a dialog_list dialog."""
    d = Dialog(DIALOG_LIST, title, external_title)
    if isinstance(dialogs, NbtDef):
        dialogs = (dialogs,)
    d['dialogs'] = tuple(map(lambda x: Nbt.as_nbt(x), dialogs))
    d.set_if('exit_action', exit_action, 'columns', columns, 'button_width', button_width)
    return d
