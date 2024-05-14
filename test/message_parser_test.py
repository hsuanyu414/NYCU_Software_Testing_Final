import pytest
import unittest

class MessageParserTest(unittest.TestCase):

    """
    Including following tests:
        - test_message_parser_full_info
        - test_message_parser_optional_info
        - test_message_parser_invalid_pattern
    """

    @pytest.mark.parametrize("test_line_id, expected", [
        ('!記帳 20240101 breakfast 100 food delicious'  , ['create_record', '20240101', 'breakfast', '100', 'food', 'delicious']),
        ('!最近記帳 最近筆數 10'                         , ['show_recent_record', 'num', 10]),
        ('!查詢 20240101 20240102'                      , ['search_record', '20240101', '20240102']),
        ('!修改記帳 12345678 日期 20240101 項目 lunch 金額 200 類別 food 備註 delicious'  \
                                                        , ['update_record', '12345678', 'lunch', '200', 'food', 'delicious']),
        ('!刪除記帳 12345678'                           , ['delete_record', '12345678']),
        ('!匯出 本月'                                   , ['export_record', 'this_month'])
    ])
    def test_message_parser_full_info(self, test_line_id, expected):
        """
        Test message with full information
        """
        pass

    @pytest.mark.parametrize("test_line_id, expected", [
        ('!最近記帳'                                    , ['show_recent_record', 'num']),
        ('!最近記帳 最近筆數'                            , ['show_recent_record', 'num']),
        ('!最近記帳 最近天數'                            , ['show_recent_record', 'days']),
        ('!查詢 20240101'                               , ['search_record', '20240101']),
        ('!匯出'                                        , ['export_record', 'this_month'])
    ])
    def test_message_parser_optional_info(self):
        """
        Test message with missing information
            - valid missing information (fill with default value)
            - invalid missing information (raise error)
        """
        pass

    @pytest.mark.parametrize("test_line_id, expected", [
        ('記帳 20240101 breakfast 100 food delicious'                       , 'invalid command'),
        ('!繼障 20240101 breakfast 100 food delicious'                      , 'invalid pattern'),
        ('!記帳 20240101 breakfast not_string food delicious'               , 'invalid pattern'),
        ('!記帳 breakfast 100 food delicious'                               , 'invalid pattern'),
        ('!最近記帳 呵呵'                                                    , 'invalid pattern'),
        ('!最近記帳 最近筆數 最近天數'                                        , 'invalid pattern'),
        ('!查詢 20240101 20240102 dummy_info'                               , 'invalid pattern'),
        ('!修改記帳 12345678 項目 lunch 金額 200 類別 food 貝柱 delicious'    , 'invalid pattern'),
        ('!修改記帳 12345678 項目 lunch 金額 200 類別 food 貝柱 delicious'    , 'invalid pattern'),
        ('!刪除記帳'                                                         , 'invalid pattern'),
        ('!刪除記帳 12345678 dummy_info'                                     , 'invalid pattern'),
        ('!匯出 本月 dummy_info'                                             , 'invalid pattern'),
    ])
    def test_message_parser_invalid_pattern(self):
        """
        Test message with invalid pattern
            - invalid command
            - missing required parameter
            - too many parameters
            - invalid parameter type
        """
        pass