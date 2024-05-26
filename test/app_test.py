import sqlite3
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

class TestApp:

    @pytest.fixture(autouse = True, scope='class')
    def setup(self):
        """
        Clear database before testing
        TODO: Set new database for each testing
        """
        conn = sqlite3.connect('../db.sqlite3')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM record')
        cursor.execute('DELETE FROM user')
        conn.commit()
        conn.close()

    @pytest.mark.parametrize('test_case_name, line_user_id, message_text, expected_reply_message', [
        ('create_record', 'test_line_user_1', '!記帳 20240520 Lunch 10 Food Comment', 'Record created successfully'),
        ('show_recent_record', 'test_line_user_1', '!最近記帳 最近筆數 10', ['Recent Record:\n', 'date: 20240520\n', 'item: Lunch\n', \
                                                            'cost: 10\n', 'category: Food\n', 'comment: Comment\n']),
        ('search_record', 'test_line_user_1', '!查詢 20240101 20240531', ['Search Record:\n', 'date: 20240520\n', 'item: Lunch\n', \
                                                                   'cost: 10\n', 'category: Food\n', 'comment: Comment\n']),
        ('update_record', 'test_line_user_1', '!修改記帳 1 日期 20240101 項目 lunch 金額 200 類別 food 備註 delicious', 'Record updated successfully'),
        ('delete_record', 'test_line_user_1', '!刪除記帳 1', 'Record deleted successfully'),
        ('export_record', 'test_line_user_1', '!匯出 本月', ['Export Record:\n'])
    ])
    @patch('main.ApiClient')
    def test_handle_message_integration(
         self, mock_api_client,
         test_case_name, line_user_id, message_text, expected_reply_message):
        """
        Test the integration of the handle_message function,
        with real MessageParser, accountingFunction, lineFunction objects.

        Give the handle_message fnuction a real message event object,
        and check if the reply message is correct.
        """
        reply_token_id = 'test_reply_token_id'
        mock_event = mock_message_event(
            reply_token = reply_token_id,
            type = 'message',
            source = mock_source(type='user', group_id=None, user_id=line_user_id),
            message = mock_message(text=message_text)
        )

        with patch('main.MessagingApi') as mock_messaging_api:

            returned_reply_message_request = handle_message(mock_event)

            if 'show_recent_record' in test_case_name or 'search_record' in test_case_name or 'export_record' in test_case_name:
                for expected_reply_message_part in expected_reply_message:
                    assert expected_reply_message_part in returned_reply_message_request.messages[0].text
            else:
                assert returned_reply_message_request.messages[0].text == \
                    expected_reply_message