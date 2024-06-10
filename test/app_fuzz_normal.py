import sqlite3
import pytest
import atheris

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
import random
import string


@atheris.instrument_func
@patch('main.ApiClient')
def fuzz_handle_message(data, mock_api_client):
    line_user_id = atheris.FuzzedDataProvider(data).ConsumeString(sys.maxsize)
    message_text = atheris.FuzzedDataProvider(data).ConsumeString(sys.maxsize)

    reply_token_id = 'test_reply_token_id'
    mock_event = mock_message_event(
        reply_token = reply_token_id,
        type = 'message',
        source = mock_source(type='user', group_id=None, user_id=line_user_id),
        message = mock_message(text=message_text)
    )

    with patch('main.MessagingApi') as mock_messaging_api:
        try:
            returned_reply_message_request = handle_message(mock_event)
        except UnicodeEncodeError:
            pass


@atheris.instrument_func
def TestOneInput(data):
    fuzz_handle_message(data)

atheris.Setup(sys.argv, TestOneInput)
atheris.Fuzz()