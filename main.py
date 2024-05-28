from flask import Flask, request, abort

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

import configparser

from line import line
from accounting import accounting
from message_parser import message_parser

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('./config.ini')

configuration = Configuration(access_token = config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """
    Handle user message and reply
        handle the following commands:
            - create_record
            - show_recent_record
            - search_record
            - update_record
            - delete_record
            - export_record
    """

    """
    Create a new user
        - create if the user does not exist
        - get user_id if the user exists
    """
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        my_line = line.lineFunction()
        line_success, line_user, line_error_message = my_line.create_line_user(event.source.user_id)
        if not line_success and line_error_message == 'line_id already exists':
            line_success, line_user, line_error_message = my_line.get_user_by_line_id(event.source.user_id)
        if not line_success:
            reply_message = "Create Line User error: " + line_error_message
            reply_message_request = ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=reply_message)]
            )
            line_bot_api.reply_message_with_http_info(reply_message_request)
            return reply_message_request
        
        user_id = line_user.user_id
        
        """
        Get and parse the user input message
        """
        user_message = event.message.text
        my_parser = message_parser.MessageParser()

        reply_message = None

        parser_success, parser_param_list, parser_error_message = my_parser.parse(user_message)
        if not parser_success:
            reply_message = "Parse error: " + parser_error_message
            reply_message_request = ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=reply_message)]
            )
            line_bot_api.reply_message_with_http_info(reply_message_request)
            return reply_message_request
        else:
            my_line = line.lineFunction()
            my_accounting = accounting.accountingFunction()
            
            command = parser_param_list[0]

            """
            Turn the command string into callable function
            """
            if command == 'create_record':
                """
                Function interface
                    - create_record(user_id, date, item, cost, category, comment)
                Return value
                    - success: True/False
                    - record: Record object
                    - error_message: string
                """
                accounting_success, accounting_record, accounting_error_message = \
                    my_accounting.create_record(user_id = user_id, date = parser_param_list[1], \
                                                item = parser_param_list[2], cost = parser_param_list[3], \
                                                category = parser_param_list[4], comment = parser_param_list[5])
                if accounting_success:
                    reply_message = "Record created successfully"
                else:
                    reply_message = "Create Record error: " + accounting_error_message

            elif command == 'show_recent_record':
                """
                Function interface
                    - show_recent_record(user_id, num=5, days=3, type='num')
                Return value
                    - success: True/False
                    - records: list of Record object
                    - error_message: string
                """
                if len(parser_param_list) == 1:
                    accounting_success, accounting_records, accounting_error_message = \
                        my_accounting.show_recent_record(user_id = user_id)
                elif len(parser_param_list) == 2:
                    if isinstance(parser_param_list[1], int):
                        accounting_success, accounting_records, accounting_error_message = \
                            my_accounting.show_recent_record(user_id = user_id, num = parser_param_list[1])
                    elif isinstance(parser_param_list[1], str):
                        accounting_success, accounting_records, accounting_error_message = \
                            my_accounting.show_recent_record(user_id = user_id, type = parser_param_list[1])
                elif len(parser_param_list) == 3:
                    if parser_param_list[2] == 'num':
                        accounting_success, accounting_records, accounting_error_message = \
                            my_accounting.show_recent_record(user_id = user_id, num = parser_param_list[1], type = parser_param_list[2])
                    elif parser_param_list[2] == 'day':
                        accounting_success, accounting_records, accounting_error_message = \
                            my_accounting.show_recent_record(user_id = user_id, days = parser_param_list[1], type = parser_param_list[2])
                
                if accounting_success:
                    reply_message = "Recent Record:\n"
                    for record in accounting_records:
                        reply_message += str(record)
                else:
                    reply_message = "Show Recent Record error: " + accounting_error_message

            elif command == 'search_record':
                """
                Function interface
                    - search_record(user_id, date_from, date_to=None)
                Return value
                    - success: True/False
                    - records: list of Record object
                    - error_message: string
                """
                if len(parser_param_list) == 2:
                    accounting_success, accounting_records, accounting_error_message = \
                        my_accounting.search_record(user_id = user_id, date_from = parser_param_list[1])
                elif len(parser_param_list) == 3:
                    accounting_success, accounting_records, accounting_error_message = \
                        my_accounting.search_record(user_id = user_id, date_from = parser_param_list[1], date_to = parser_param_list[2])

                if accounting_success:
                    reply_message = "Search Record:\n"
                    for record in accounting_records:
                        reply_message += str(record)
                else:
                    reply_message = "Search Record error: " + accounting_error_message

            elif command == 'update_record':
                """
                Function interface
                    - update_record(user_id, record_id, date=None, item=None, cost=None, category=None, comment=None)
                Return value
                    - success: True/False
                    - record: Record object
                    - error_message: string
                """
                accounting_success, accounting_record, accounting_error_message = \
                    my_accounting.update_record(user_id = user_id, record_id = parser_param_list[1], \
                                                date = parser_param_list[2], item = parser_param_list[3], \
                                                cost = parser_param_list[4], category = parser_param_list[5], \
                                                comment = parser_param_list[6])
                if accounting_success:
                    reply_message = "Record updated successfully"
                else:
                    reply_message = "Update Record error: " + accounting_error_message

            elif command == 'delete_record':
                """
                Function interface
                    - delete_record(user_id, record_id)
                Return value
                    - success: True/False
                    - error_message: string
                """
                accounting_success, _, accounting_error_message = \
                    my_accounting.delete_record(user_id = user_id, record_id = parser_param_list[1])
                if accounting_success:
                    reply_message = "Record deleted successfully"
                else:
                    reply_message = "Delete Record error: " + accounting_error_message

            elif command == 'export_record':
                """
                Function interface
                    - export_record(user_id, method='this_month')
                Return value
                    - success: True/False
                    - link: string
                    - error_message: string
                """
                if len(parser_param_list) == 1:
                    accounting_success, accounting_link, accounting_error_message = \
                        my_accounting.export_record(user_id = user_id)
                elif len(parser_param_list) == 2:
                    accounting_success, accounting_link, accounting_error_message = \
                        my_accounting.export_record(user_id = user_id, method = parser_param_list[1])
                if accounting_success:
                    reply_message = "Export Record:\n" + accounting_link
                else:
                    reply_message = "Export Record error: " + accounting_error_message

            else:
                reply_message = "Invalid command"

            reply_message_request = ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=reply_message)]
            )
            line_bot_api.reply_message_with_http_info(reply_message_request)

            return reply_message_request

if __name__ == "__main__":
    app.run(port=8081, debug=True)