import sqlite3
import pytest
import os

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
    def setup(self, request):
        """
        Create a temporary database before testing
        and remove it after testing
        """
        # Create a temporary database file in the temporary directory
        db_file = os.path.join('../', 'test_db.sqlite3')
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE record (user_id INTEGER, record_id INTEGER PRIMARY KEY, date TEXT, item TEXT, cost INTEGER, category TEXT, comment TEXT, create_date DATE)')
        cursor.execute('CREATE TABLE user (user_id INTEGER PRIMARY KEY, line_id TEXT, create_date DATE)')
        conn.commit()
        conn.close()

        # Set the db_file attribute in the test class instance
        request.cls.db_file = db_file

        yield

        # remove the temporary database file
        os.remove(self.db_file)

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

            returned_reply_message_request = handle_message(mock_event, self.db_file)

            if 'show_recent_record' in test_case_name or 'search_record' in test_case_name or 'export_record' in test_case_name:
                for expected_reply_message_part in expected_reply_message:
                    assert expected_reply_message_part in returned_reply_message_request.messages[0].text
            else:
                assert returned_reply_message_request.messages[0].text == \
                    expected_reply_message