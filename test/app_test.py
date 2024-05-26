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
        TODO: Set the database to test database
        """
        conn = sqlite3.connect('../db.sqlite3')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM record')
        cursor.execute('DELETE FROM user')
        conn.commit()
        conn.close()

    @pytest.mark.parametrize('test_case_name, user_id, message_text, expected_reply_message', [
        ('create_record', 'test_user_1', '!記帳 20240520 Lunch 10 Food Comment', 'Record created successfully'),
        ('show_recent_record', 'test_user_1', '!最近記帳 最近筆數 10', ['Recent Record:\n', 'date: 20240520\n', 'item: Lunch\n', \
                                                            'cost: 10\n', 'category: Food\n', 'comment: Comment\n']),
        ('search_record', 'test_user_1', '!查詢 20240101 20240531', ['Search Record:\n', 'date: 20240520\n', 'item: Lunch\n', \
                                                                   'cost: 10\n', 'category: Food\n', 'comment: Comment\n']),
        ('update_record', '!修改記帳 12345678 日期 20240101 項目 lunch 金額 200 類別 food 備註 delicious', 'tetst_user_1', 'Record updated successfully'),
        ('delete_record', '!刪除記帳 12345678', 'test_user_1', 'Record deleted successfully'),
        ('export_record', '!匯出 本月', 'test_user_1', ['Export Record:\n'])
    ])
    @patch('main.ApiClient')
    def test_handle_message_integration(
         self, mock_api_client,
         test_case_name, user_id, message_text, expected_reply_message):
        """
        Test the integration of the handle_message function,
        with real MessageParser, accountingFunction, lineFunction objects.

        Give the handle_message fnuction a real message event object,
        and check if the reply message is correct.
        """
        pass