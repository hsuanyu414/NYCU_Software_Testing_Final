class mock_db_conn:
    def __init__(self):
        self.Cursor = self.Cursor()

    class Cursor:
        def __init__(self):
            pass

        def execute(self, *args):
            pass

        def fetchone(self):
            pass

    def cursor(self):
        return self.Cursor

    def commit(self):
        pass

    def rollback(self):
        pass

    def close(self):
        pass


class mock_message:
    def __init__(self, text):
        self.text = text


class mock_source:
    def __init__(self, type, group_id, user_id):
        self.type = type
        self.group_id = group_id
        self.user_id = user_id


class mock_message_event:
    """
    Mock the object of linebot.models.MessageEvent
    https://developers.line.biz/en/reference/messaging-api/#message-event
    """

    def __init__(self, reply_token, type, source, message):
        self.reply_token = reply_token
        self.type = type
        self.source = source
        self.message = message


class mock_configparser:
    def __init__(self):
        pass

    def read(self, filename):
        return 'test_file'

    def get(self, section, option):
        return 'test_value'
