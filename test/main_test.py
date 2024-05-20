import pytest

from unittest.mock import patch
from linebot.v3.messaging import TextMessage, ReplyMessageRequest

from mock_obj import mock_message_event, mock_source, mock_message

import sys
sys.path.append('..')

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

        pass