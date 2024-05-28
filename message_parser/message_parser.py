import re
import datetime

class MessageParser:
    def __init__(self):
        self.command_map = {
            '!記帳': "create_record",
            '!最近記帳': "show_recent_record",
            '!查詢': "search_record",
            '!修改記帳': "update_record",
            '!刪除記帳': "delete_record",
            '!匯出': "export_record",
        }

        self.command_pattern = {
            'create_record': r'^!記帳\s+(\d{8})\s+(\w+)\s+(\d+)\s+(\w+)\s+(.*)$',
            'show_recent_record': r'^!最近記帳(?:\s+(?P<method>最近筆數|最近天數))?(?:\s+(?P<value>\d+))?$',
            'search_record': r'^!查詢 (?P<date_from>\d{8})(?:\s+(?P<date_to>\d{8})?)?$',
            'update_record': r'^!修改記帳 (?P<record_id>\d+)(?:\s+(?P<key>日期|項目|金額(?=\s+\d+)|類別|備註) (?P<value>\w+))*$',
            'update_record_key_value': r'(?P<key>日期|項目|金額(?=\s+\d+)|類別|備註) (?P<value>\w+)',
            'delete_record': r'^!刪除記帳 (?P<record_id>\d+)$',
            'export_record': r'^!匯出(?:\s+(本月|本年|全部))?$'
        }

        self.show_recent_record_type_map = {
            '最近筆數': 'num',
            '最近天數': 'day'
        }

        self.export_method_map = {
            '本月': 'this month',
            '本年': 'this year',
            '全部': 'all'
        }

    def parse(self, user_message):
        """
        Parse user message to command and parameters
            Args:
                user_message (str): user message
            Returns:
                success (bool): if the message is parsed successfully
                param_list (list): list of command and parameters
                error message (str): error message 
        """
        success = False
        param_list = []
        error_message = None

        """
        Check if the message is string and not empty
        """
        if not isinstance(user_message, str):
            error_message = 'wrong type'
            return success, param_list, error_message
        elif user_message == '':
            error_message = 'empty message'
            return success, param_list, error_message
        
        """
        Split the message by space and check if the command is valid
        """
        message_list = user_message.split(' ')
        message_command = message_list[0]
        if message_command not in self.command_map:
            error_message = 'invalid command'
            return success, param_list, error_message
        
        """
        Handle different commands
        """
        command = self.command_map[message_command]
        if command == 'create_record':
            match = re.match(self.command_pattern[command], user_message)
            if match:
                date = match.group(1)
                item = match.group(2)
                cost = int(match.group(3))
                category = match.group(4)
                comment = match.group(5)
                param_list = [command, date, item, cost, category, comment]
                success = True
            else:
                error_message = 'invalid pattern'
        elif command == 'show_recent_record':
            match = re.match(self.command_pattern[command], user_message)
            if match:
                method = match.group('method')
                value = match.group('value')
                if method is None and value is None:
                    param_list = [command]
                elif method is not None and value is None:
                    param_list = [command, self.show_recent_record_type_map[method]]
                elif method is None and value is not None:
                    param_list = [command, int(value)]
                elif method is not None and value is not None:
                    param_list = [command, int(value), self.show_recent_record_type_map[method]]
                success = True
            else:
                error_message = 'invalid pattern'
        elif command == 'search_record':
            match = re.match(self.command_pattern[command], user_message)
            if match:
                date_from = match.group('date_from')
                date_to = match.group('date_to')
                if date_to is None:
                    param_list = [command, date_from]
                else:
                    param_list = [command, date_from, date_to]
                success = True
            else:
                error_message = 'invalid pattern'
        elif command == 'update_record':
            match = re.match(self.command_pattern[command], user_message)
            if match:
                record_id = int(match.group('record_id'))
                pairs = [(m.group('key'), m.group('value')) for m in re.finditer(self.command_pattern[command+"_key_value"], user_message)]
                print(pairs)
                date = item = cost = category = comment = None
                for key, value in pairs:
                    if key == '日期':
                        date = value
                    elif key == '項目':
                        item = value
                    elif key == '金額':
                        cost = int(value)
                    elif key == '類別':
                        category = value
                    elif key == '備註':
                        comment = value
                param_list = [command, record_id, date, item, cost, category, comment]
                success = True
            else:
                error_message = 'invalid pattern'
        elif command == 'delete_record':
            match = re.match(self.command_pattern[command], user_message)
            if match:
                record_id = int(match.group('record_id'))
                param_list = [command, record_id]
                success = True
            else:
                error_message = 'invalid pattern'
        elif command == 'export_record':
            match = re.match(self.command_pattern[command], user_message)
            if match:
                method = match.group(1) if match.group(1) is not None else '本月'
                param_list = [command, self.export_method_map[method]]
                success = True
            else:
                error_message = 'invalid pattern'
        else:
            error_message = 'invalid command'

        return success, param_list, error_message