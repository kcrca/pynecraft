import unittest

from pynecraft.dialog import *


class TestSimpler(unittest.TestCase):

    def test_dialog_misc(self):
        self.assertEqual({'label': 'Click'}, ClickAction('Click'))
        self.assertEqual(
            {'label': 'Click', 'on_click': {'action': 'open_url', 'url': 'https://myspace.com'}, 'tooltip': '<click>',
             'width': 15},
            ClickAction('Click', on_click=ClickEvent.open_url('https://myspace.com'), tooltip='<click>',
                        width=15))

    def test_dialog_body_parts(self):
        self.assertEqual({'type': 'plain_message', 'contents': {'text': 'howdy'}},
                         plain_message('howdy'))
        self.assertEqual({'type': 'plain_message', 'contents': {'text': 'howdy'}, 'width': 15},
                         plain_message('howdy', width=15))
        self.assertEqual({'type': 'item', 'item': {'id': 'minecraft:cake'}},
                         item('cake'))
        self.assertEqual({'type': 'item', 'item': {'id': 'minecraft:cake'}},
                         item(Item('cake')))
        self.assertEqual({'type': 'item', 'item': {'id': 'minecraft:cake'}},
                         item(Item.nbt_for('cake')))
        self.assertEqual(
            {'type': 'item', 'item': {'id': 'minecraft:cake'}, 'description': {'text': 'yummy'},
             'show_decoration': True, 'show_tooltip': True, 'width': 9, 'height': 15},
            item('cake', description="yummy", show_decoration=True, show_tooltip=True, width=9, height=15))

    def test_dialog_inputs(self):
        self.assertEqual({'type': 'text', 'label': 'No Way!', 'key': 'no_way'}, text('No Way!'))
        self.assertEqual({'type': 'text', 'label': 'No Way!', 'key': 'my_key'}, text('No Way!', key='my_key'))
        self.assertEqual(
            {'type': 'text', 'label': 'No Way!', 'key': 'no_way', 'initial': 'Yup', 'width': 3, 'max_length': 20,
             'label_visible': False},
            text('No Way!', initial='Yup', width=3, max_length=20, label_visible=False))
        self.assertEqual(
            {'type': 'text', 'label': 'No Way!', 'key': 'no_way', 'multiline': {'height': 17, 'max_lines': 12}},
            text('No Way!', multiline={'height': 17, 'max_lines': 12}))
        self.assertEqual({'type': 'text', 'label': 'No Way!', 'key': 'no_way'}, text('No Way!', multiline={}))
        self.assertEqual({'type': 'boolean', 'label': 'Maybe', 'key': 'maybe'}, boolean('Maybe'))
        self.assertEqual(
            {'type': 'boolean', 'label': 'Maybe', 'key': 'uh', 'initial': True, 'on_true': 'oui', 'on_false': 'non'},
            boolean('Maybe', True, key='uh', on_true='oui', on_false='non'))
        self.assertEqual(
            {'type': 'single_option', 'label': 'Name', 'key': 'name',
             'options': [{'display': '1', 'id': '1'}, {'display': '2', 'id': '2'},
                         {'display': '3', 'id': '3'}]},
            single_option('Name', (1, 2, 3)))
        self.assertEqual(
            {'type': 'single_option', 'label': 'Name', 'key': 'name',
             'options': [{'display': '1', 'id': '1'}, {'display': '2', 'id': '2'}, {'display': '3', 'id': '3'}]},
            single_option('Name', (1, 2, 3)))
        self.assertEqual(
            {'type': 'single_option', 'label': 'Name', 'key': 'name',
             'options': [{'display': '1', 'id': '1'}, {'display': '2', 'id': '2', 'initial': True},
                         {'display': '3', 'id': '3'}]},
            single_option('Name', (1, 2, 3), initial=2))
        self.assertEqual(
            {'type': 'single_option', 'label': 'Name', 'key': 'name',
             'options': [{'display': 'Pat', 'id': 'pat'}, {'display': 'Engel', 'id': 'engel'},
                         {'display': 'Yuki', 'id': 'yuki', 'initial': True}]},
            single_option('Name', ('Pat', 'Engel', 'Yuki'), initial='Yuki'))
        self.assertEqual(
            {'type': 'single_option', 'label': 'Name', 'key': 'name',
             'options': [{'display': 'Pat', 'id': 'pat'}, {'display': 'Engel', 'id': 'engel'},
                         {'display': 'Yuki', 'id': 'yuki', 'initial': True}]},
            single_option('Name', ('Pat', 'Engel', {'display': 'Yuki', 'initial': True}), initial='Yuki'))
        self.assertEqual(
            {'type': 'single_option', 'label': 'Name', 'key': 'name', 'width': 5, 'label_visible': False,
             'options': [{'display': '1', 'id': '1'}, {'display': '2', 'id': '2'}, {'display': '3', 'id': '3'}]},
            single_option('Name', (1, 2, 3), width=5, label_visible=False))

        self.assertEqual(
            {'type': 'number_range', 'label': 'Count', 'key': 'count', 'start': -5, 'end': 5},
            number_range('Count', -5, 5))
        self.assertEqual(
            {'type': 'number_range', 'label': 'Count', 'key': 'my_key', 'start': -5, 'end': 5, 'step': 2, 'initial': 3,
             'width': 8, 'label_format': 'fmt'},
            number_range('Count', -5, 5, 2, 'my_key', initial=3, width=8, label_format='fmt'))

    def test_dialog_body(self):
        self.assertEqual(
            {'type': 'notice', 'title': {'text': 'howdy'},
             'body': [{'type': 'plain_message', 'contents': {'text': 'hello'}}]},
            notice('howdy').body(plain_message('hello')))
        self.assertEqual(
            {'type': 'notice', 'title': {'text': 'howdy'},
             'body': [{'type': 'plain_message', 'contents': {'text': 'hello'}},
                      {'type': 'plain_message', 'contents': {'text': 'goodbye'}}]},
            notice('howdy').body(plain_message('hello'), plain_message('goodbye')))

    def test_dialog_can_close(self):
        self.assertEqual({'type': 'notice', 'title': {'text': 'howdy'}, 'can_close_with_escape': False},
                         notice('howdy').can_close_with_escape(False))

        self.assertEqual({'type': 'notice', 'title': {'text': 'howdy'}, 'external_title': {'text': 'uhh'}},
                         notice('howdy', external_title='uhh'))

    def test_dialog_notice(self):
        self.assertEqual({'type': 'notice', 'title': {'text': 'howdy'}}, notice('howdy'))
        self.assertEqual(
            {'type': 'notice', 'title': {'text': 'howdy'}, 'body': [{'type': 'item', 'item': {'id': 'minecraft:cake'}}],
             'external_title': {'text': 'ext'}},
            notice('howdy', external_title='ext').body(item('cake')))

    def test_dialog_confirmation(self):
        self.assertEqual(
            {'type': 'confirmation', 'title': {'text': 'howdy'}, 'yes': {'label': 'hi'}, 'no': {'label': 'bye'}},
            confirmation('howdy', ClickAction("hi"), ClickAction("bye")))

    def test_dialog_multi_action(self):
        self.assertEqual(
            {'type': 'multi_action', 'title': {'text': 'multi'}, 'actions': [{'label': 'now'}]},
            multi_action('multi', ClickAction('now')))
        self.assertEqual(
            {'type': 'multi_action', 'title': {'text': 'multi'}, 'actions': [{'label': 'now'}]},
            multi_action('multi', ClickAction('now')))
        self.assertEqual(
            {'type': 'multi_action', 'title': {'text': 'multi'}, 'actions': [{'label': 'now'}], 'columns': 3,
             'exit_action': {'label': 'cancel'}},
            multi_action('multi', ClickAction('now'), columns=3,
                         exit_action=ClickAction('cancel')))

    def test_dialog_server_links(self):
        self.assertEqual({'type': 'server_links', 'title': {'text': 'sly'}}, server_links('sly'))
        self.assertEqual(
            {'type': 'server_links', 'title': {'text': 'sly'}, 'on_click': {'action': 'change_page', 'page': 5},
             'exit_action': {'action': 'change_page', 'page': -5}, 'columns': 3, 'button_width': 7},
            server_links('sly', on_click=ClickEvent.change_page(5), exit_action=ClickEvent.change_page(-5),
                         columns=3, button_width=7))

    def test_dialog_dialog_list(self):
        self.assertEqual(
            {'type': 'dialog_list', 'title': {'text': 'the_dl'},
             'dialogs': [{'type': 'notice', 'title': {'text': 'n1'}}]},
            dialog_list('the_dl', notice("n1")))
        self.assertEqual(
            {'type': 'dialog_list', 'title': {'text': 'the_dl'},
             'dialogs': [{'type': 'notice', 'title': {'text': 'n1'}}]},
            dialog_list('the_dl', [notice("n1")]))
        self.assertEqual(
            {'type': 'dialog_list', 'title': {'text': 'the_dl'},
             'dialogs': [{'type': 'notice', 'title': {'text': 'n1'}}],
             'exit_action': {'action': 'change_page', 'page': -5}, 'columns': 3, 'button_width': 7},
            dialog_list('the_dl', notice("n1"), exit_action=ClickEvent.change_page(-5), columns=3,
                        button_width=7))

    def test_dialog_submit_actions(self):
        self.assertEqual({'type': 'command_template', 'template': 'foo', 'id': 'commandtemplate'},
                         command_template('foo')),
        self.assertEqual({'type': 'custom_template', 'template': 'foo', 'id': 'ns'},
                         custom_template('foo', 'ns')),
        self.assertEqual({'type': 'custom_form', 'id': 'ns'}, custom_form('ns')),
        self.assertEqual(
            {'label': 'Sub', 'id': 'sub', 'on_submit': {'type': 'custom_form', 'id': 'ns'}, 'tooltip': 'tp',
             'width': 5},
            submit_action('Sub', on_submit=custom_form('ns'), tooltip='tp', width=5))
