import pytest

from unittest.mock import patch
from linebot import WebhookHandler
from linebot.v3.messaging import TextMessage, ReplyMessageRequest

from mock_obj import mock_message_event, mock_source, mock_message, mock_configparser

import sys
sys.path.append('..')

MagicMock = patch('configparser.ConfigParser', side_effect=mock_configparser)
MagicMock.start()

from main import handle_message
from models import Record, User

test_cases_full_info = [
    (
        'create_record',                                                # test case name
        'test_reply_token_id',                                          # reply_token_id
        '!記帳 20240520 Lunch 10 Food Comment',                          # message_text
        True,                                                           # parser_success
        ['create_record', '20240520', 'Lunch', 10, 'Food', 'Comment'],  # parser_output
        None,                                                           # parser_error_message
        True,                                                           # accounting_success
        Record.Record(user_id='1', date='20240520', item='Lunch', cost=10, \
               category='Food', comment='Comment'),                     # accounting_record
        None,                                                           # accounting_error_message
        True,                                                           # line_success
        mock_source(type='user', group_id=None, user_id='1'),           # line_user_record
        None,                                                           # line_error_message
        None,                                                           # messaging_api_response
        'Record created successfully'                                   # reply_message_text
    ),
    (
        'show_recent_record',
        'test_reply_token_id',
        '!最近記帳 最近筆數 10',
        True,
        ['show_recent_record', 10, 'num'],
        None, True,
        [Record.Record(user_id='1', date='20240520', item='Lunch', cost=10, category='Food', comment='Comment')],
        None, True,
        mock_source(type='user', group_id=None, user_id='1'),
        None, None,
        'Recent Record:\n' + Record.Record(user_id='1', date='20240520', item='Lunch', cost=10, category='Food', comment='Comment').__str__(),
    ),
    (
        'search_record',
        'test_reply_token_id',
        '!查詢 20240101 20240531',
        True,
        ['search_record', '20240101', '20240531'],
        None, True,
        [Record.Record(user_id='1', date='20240520', item='Lunch', cost=10, category='Food', comment='Comment')],
        None, True,
        mock_source(type='user', group_id=None, user_id='1'),
        None, None,
        'Search Record:\n' + Record.Record(user_id='1', date='20240520', item='Lunch', cost=10, category='Food', comment='Comment').__str__(),
    ),
    (
        'update_record',
        'test_reply_token_id',
        '!修改記帳 12345678 日期 20240101 項目 lunch 金額 200 類別 food 備註 delicious',
        True,
        ['update_record', '12345678', '20240101', 'lunch', 200, 'food', 'delicious'],
        None, True,
        [Record.Record(user_id='1', date='20240520', item='Lunch', cost=10, category='Food', comment='Comment')],
        None, True,
        mock_source(type='user', group_id=None, user_id='1'),
        None, None,
        'Record updated successfully',
    ),
    (
        'delete_record',
        'test_reply_token_id',
        '!刪除記帳 12345678',
        True,
        ['delete_record', '12345678'],
        None, True, None,
        None, True,
        mock_source(type='user', group_id=None, user_id='1'),
        None, None,
        'Record deleted successfully',
    ),
    (
        'export_record',
        'test_reply_token_id',
        '!匯出 本月',
        True,
        ['export_record', 'this_month'],
        None, True,
        "link_to_export_record",
        None, True,
        mock_source(type='user', group_id=None, user_id='1'),
        None, None,
        'Export Record:\n' + "link_to_export_record"
    )
]

class TestMain():

    @pytest.mark.parametrize(
        "test_case_name, reply_token_id, message_text, "
        "parser_success, parser_output, parser_error_message, "
        "accounting_success, accounting_record, accounting_error_message, "
        "line_success, line_user_record, line_error_message, "
        "messaging_api_response, reply_message_text",
        test_cases_full_info
    )
    # @patch('configparser.ConfigParser', side_effect=mock_configparser)
    @patch('main.ApiClient')
    @patch('main.line.lineFunction')
    @patch('main.accounting.accountingFunction')
    @patch('main.message_parser.MessageParser')
    def test_handle_message_full_info(
        self,
        mock_parser, mock_accounting, mock_line, mock_api_client,
        test_case_name, reply_token_id, message_text, 
        parser_success, parser_output, parser_error_message,
        accounting_success, accounting_record, accounting_error_message,
        line_success, line_user_record, line_error_message,
        messaging_api_response, reply_message_text
    ):
        """
        First create a fake message event object with the given test case parameters.
        Then stub the functions:
            - MessageParser.parse
            - accountingFunction.*
            - lineFunction.*
            - MessagingApi.reply_message_with_http_info
        The tests will check if the functions are called with the correct parameters.
        """

        mock_event = mock_message_event(
            reply_token = reply_token_id,
            type = 'message',
            source = mock_source(type='user', group_id=None, user_id='1'),
            message = mock_message(text=message_text)
        )

        with patch('main.MessagingApi') as mock_messaging_api:
            mock_parser_instance = mock_parser.return_value
            mock_parser_instance.parse.return_value = (parser_success, parser_output, parser_error_message)

            mock_line_instance = mock_line.return_value
            mock_line_instance.create_line_user.return_value = (line_success, line_user_record, line_error_message)

            if test_case_name == 'create_record':
                mock_accounting_instance = mock_accounting.return_value
                mock_accounting_instance.create_record.return_value = (accounting_success, accounting_record, accounting_error_message)
            elif test_case_name == 'show_recent_record':
                mock_accounting_instance = mock_accounting.return_value
                mock_accounting_instance.show_recent_record.return_value = (accounting_success, accounting_record, accounting_error_message)
            elif test_case_name == 'search_record':
                mock_accounting_instance = mock_accounting.return_value
                mock_accounting_instance.search_record.return_value = (accounting_success, accounting_record, accounting_error_message)
            elif test_case_name == 'update_record':
                mock_accounting_instance = mock_accounting.return_value
                mock_accounting_instance.update_record.return_value = (accounting_success, accounting_record, accounting_error_message)
            elif test_case_name == 'delete_record':
                mock_accounting_instance = mock_accounting.return_value
                mock_accounting_instance.delete_record.return_value = (accounting_success, accounting_record, accounting_error_message)
            elif test_case_name == 'export_record':
                mock_accounting_instance = mock_accounting.return_value
                mock_accounting_instance.export_record.return_value = (accounting_success, accounting_record, accounting_error_message)

            mock_messaging_api_instance = mock_messaging_api.return_value
            mock_messaging_api_instance.reply_message_with_http_info.return_value = messaging_api_response

            handle_message(mock_event)

            mock_line_instance.create_line_user.assert_called_once_with('1')
            mock_parser_instance.parse.assert_called_once_with(message_text)

            if test_case_name == 'create_record':
                mock_accounting_instance.create_record.assert_called_once_with(
                    user_id = line_user_record.user_id,
                    date = parser_output[1],
                    item = parser_output[2],
                    cost = parser_output[3],
                    category = parser_output[4],
                    comment = parser_output[5]
                )
            elif test_case_name == 'show_recent_record':
                mock_accounting_instance.show_recent_record.assert_called_once_with(
                    user_id = line_user_record.user_id,
                    num = parser_output[1],
                    type = parser_output[2]
                )
            elif test_case_name == 'search_record':
                mock_accounting_instance.search_record.assert_called_once_with(
                    user_id = line_user_record.user_id,
                    date_from = parser_output[1],
                    date_to = parser_output[2]
                )
            elif test_case_name == 'update_record':
                mock_accounting_instance.update_record.assert_called_once_with(
                    user_id = line_user_record.user_id,
                    record_id = parser_output[1],
                    date = parser_output[2],
                    item = parser_output[3],
                    cost = parser_output[4],
                    category = parser_output[5],
                    comment = parser_output[6]
                )
            elif test_case_name == 'delete_record':
                mock_accounting_instance.delete_record.assert_called_once_with(
                    user_id = line_user_record.user_id,
                    record_id = parser_output[1]
                )
            elif test_case_name == 'export_record':
                mock_accounting_instance.export_record.assert_called_once_with(
                    user_id = line_user_record.user_id,
                    method = parser_output[1]
                )
                
            expected_reply_message_request = ReplyMessageRequest(
                reply_token = reply_token_id,
                messages = [TextMessage(text=reply_message_text)]
            )
            mock_messaging_api_instance.reply_message_with_http_info.assert_called_once_with(expected_reply_message_request)