import pytest

import sys

sys.path.append('..')
from line import line
from accounting import accounting
from models import User, Record
from mock_obj import mock_db_conn

import sqlite3

class TestCreateLineUser:
    @pytest.mark.parametrize("test_line_id, expected", [
        ('U123456789', 'U123456789'),
        (123456789, 'invalid line_id parameter')
    ])
    def test_create_line_user_P1(self, test_line_id, expected, mocker):
        # Arrange
        mock_obj = mock_db_conn()
        mock_obj.Cursor.lastrowid = 1
        mock_obj.Cursor.fetchone_results = [None, (1, 'U123456789', '2024-06-01 00:00:00')]
        mock_obj.Cursor.fetchone = lambda: mock_obj.Cursor.fetchone_results.pop(0)

        mocker.patch.object(sqlite3, 'connect', return_value=mock_obj)
        module = line.lineFunction()

        # Act
        success, user, error_message = module.create_line_user(test_line_id)

        # Assert
        if success:
            assert user.line_id == expected
        else:
            assert error_message == expected

        mocker.resetall()

    def test_create_line_user_P2_T1(self, mocker):
        # Arrange
        mock_obj = mock_db_conn()
        mock_obj.Cursor.lastrowid = 1
        mock_obj.Cursor.fetchone_results = [None, (1, 'U123456789', '2024-06-01 00:00:00')]
        mock_obj.Cursor.fetchone = lambda: mock_obj.Cursor.fetchone_results.pop(0)

        mocker.patch.object(sqlite3, 'connect', return_value=mock_obj)
        module = line.lineFunction()

        # Act
        success, user, error_message = module.create_line_user('U123456789')

        # Assert
        assert success
        assert user.line_id == 'U123456789'
        assert error_message == None

        mocker.resetall()

    def test_create_line_user_P2_T2(self, mocker):
        # Arrange
        mock_obj = mock_db_conn()
        mock_obj.Cursor.lastrowid = 1
        mock_obj.Cursor.fetchone_results = [(1, 'U123456789', '2024-06-01 00:00:00')]
        mock_obj.Cursor.fetchone = lambda: mock_obj.Cursor.fetchone_results.pop(0)

        mocker.patch.object(sqlite3, 'connect', return_value=mock_obj)
        module = line.lineFunction()

        # Act
        success, user, error_message = module.create_line_user('U123456789')

        # Assert
        assert not success
        assert user == None
        assert error_message == 'line_id already exists'

        mocker.resetall()

class TestCreateRecord:
    @pytest.mark.parametrize("test_user_id, test_date, test_item, test_cost, test_category, test_comment, expected", [
        (   1 , '20240101', 'apple',  20 , 'food', 'good_to_eat', Record.Record(1, 1, '20240101', 'apple', 20, 'food', 'good_to_eat', '20240101')),
        (  '1', '20240101', 'apple',  20 , 'food', 'good_to_eat', 'invalid line_id parameter'),
        (   1 ,  20240101 , 'apple',  20 , 'food', 'good_to_eat', 'invalid date parameter'),
        (   1 , '20240101',   123  ,  20 , 'food', 'good_to_eat', 'invalid item parameter'),
        (   1 , '20240101', 'apple', '20', 'food', 'good_to_eat', 'invalid cost parameter'),
        (   1 , '20240101', 'apple',  20 ,   123 , 'good_to_eat', 'invalid category parameter'),
        (   1 , '20240101', 'apple',  20 , 'food',          123 , 'invalid comment parameter')
    ])
    def test_create_record_P123456(self, test_user_id, test_date, test_item, test_cost, test_category, test_comment, expected, mocker):
        #Arrange
        mock_obj = mock_db_conn()
        mock_obj.Cursor.lastrowid = 1
        mock_obj.Cursor.fetchone_results = ['None', (1, 1, '20240101', 'apple', 20, 'food', 'good_to_eat', '20240101')]
        mock_obj.Cursor.fetchone = lambda: mock_obj.Cursor.fetchone_results.pop(0)

        mocker.patch.object(sqlite3, 'connect', return_value=mock_obj)
        module = accounting.accountingFunction()

        #Act
        success, record, error_message = module.create_record(test_user_id, test_date, test_item, test_cost, test_category, test_comment)

        #Assert
        if success:
            assert record.user_id == expected.user_id
            assert record.date == expected.date
            assert record.item == expected.item
            assert record.cost == expected.cost
            assert record.category == expected.category
            assert record.comment == expected.comment
            assert record.create_date != None
        else:
            assert error_message == expected

    @pytest.mark.parametrize("test_user_id, test_date, test_item, test_cost, test_category, test_comment, expected", [
        (   2 , '20240101', 'apple',  20 , 'food', 'good_to_eat', 'user_id does not exist')
    ])
    def test_create_record_user_id_not_exist_P7(self, test_user_id, test_date, test_item, test_cost, test_category, test_comment, expected, mocker):
        #Arrange
        mock_obj = mock_db_conn()
        mock_obj.Cursor.lastrowid = 1
        mock_obj.Cursor.fetchone_results = [None]
        mock_obj.Cursor.fetchone = lambda: mock_obj.Cursor.fetchone_results.pop(0)

        mocker.patch.object(sqlite3, 'connect', return_value=mock_obj)
        module = accounting.accountingFunction()

        #Act
        success, record, error_message = module.create_record(test_user_id, test_date, test_item, test_cost, test_category, test_comment)

        #Assert
        assert not success
        assert record == None
        assert error_message == 'user_id does not exist'

class TestShowRecentRecord:
    # def show_recent_record(user_id, count)
    @pytest.mark.parametrize("test_user_id, test_num, test_day, test_type, expected", [
        # assumse today is 20240103
        (   1 ,  3 ,  1 ,  'num', 3 ), # assume there are more than 3 records in the database
        (   1 ,  3 ,  1 ,  'days', 3 ), # assume there are only 2 records in the database
        (  '1',  3 ,  1 ,  'num', 'invalid user_id parameter'),
        (   1 , '3',  1 ,  'num', 'invalid num parameter'),
        (   1 ,  3 , '1',  'num', 'invalid day parameter'),
        (   1 ,  3 ,  1 ,   123 , 'invalid type parameter')
    ])
    def test_show_recent_record_P12345(self, test_user_id, test_num, test_day, test_type, expected, mocker):
        # Arrange
        mock_obj = mock_db_conn()
        mock_obj.Cursor.lastrowid = 1
        mock_obj.Cursor.fetchone_results = [ User.User() ]
        mock_obj.Cursor.fetchone = lambda: mock_obj.Cursor.fetchone_results.pop(0)
        mock_obj.Cursor.fetchall_results = [
            (1, 1, 20240101,   'apple', 20, 'food', 'good_to_eat', '20240101'), 
            (1, 2, 20240102,  'banana', 30, 'food', 'good_to_eat', '20240102'), 
            (1, 3, 20240103, 'coconut', 40, 'food', 'good_to_eat', '20240103')
        ]
        mock_obj.Cursor.fetchall = lambda: mock_obj.Cursor.fetchall_results

        mocker.patch.object(sqlite3, 'connect', return_value=mock_obj)
        module = accounting.accountingFunction()

        # Act
        success, records, error_message = module.show_recent_record(test_user_id, test_num, test_day, test_type)

        # Assert
        if success:
            assert len(records) == expected
        else:
            assert error_message == expected

    
    @pytest.mark.parametrize("test_user_id, test_num, test_day, test_type, expected", [
        (   2,   3 ,  1 , 'num', 'user_id does not exist')
    ])
    def test_show_recent_record_user_id_not_exist(self, test_user_id, test_num, test_day, test_type, expected, mocker):
        # Arrange
        mock_obj = mock_db_conn()
        mock_obj.Cursor.lastrowid = 1
        mock_obj.Cursor.fetchone_results = [None]
        mock_obj.Cursor.fetchone = lambda: mock_obj.Cursor.fetchone_results.pop(0)

        mocker.patch.object(sqlite3, 'connect', return_value=mock_obj)
        module = accounting.accountingFunction()

        # Act
        success, records, error_message = module.show_recent_record(test_user_id, test_num, test_day, test_type)

        # Assert
        assert not success
        assert records == None
        assert error_message == expected

# class TestSearchRecord
class TestSearchRecord:
    @pytest.mark.parametrize("test_user_id, date_from, date_to, expected", [
        (   1 , '20240101', '20240103', 3 ), # assume there are 3 records in the database from 20240101 to 20240103
        (  '1', '20240101', '20240103', 'invalid user_id parameter'),
        (   1 ,  20240101 , '20240103', 'invalid date_from parameter'),
        (   1 , '20240101',  20240103 , 'invalid date_to parameter')
    ])
    def test_search_record_normal_1(self, test_user_id, date_from, date_to, expected, mocker):
        # Arrange
        mock_obj = mock_db_conn()
        mock_obj.Cursor.lastrowid = 1
        mock_obj.Cursor.fetchone_results = [ User.User() ]
        mock_obj.Cursor.fetchone = lambda: mock_obj.Cursor.fetchone_results.pop(0)
        mock_obj.Cursor.fetchall_results = [
            (1, 1, 20240101,   'apple', 20, 'food', 'good_to_eat', '20240101'), 
            (1, 2, 20240102,  'banana', 30, 'food', 'good_to_eat', '20240102'), 
            (1, 3, 20240103, 'coconut', 40, 'food', 'good_to_eat', '20240103')
        ]
        mock_obj.Cursor.fetchall = lambda: mock_obj.Cursor.fetchall_results

        mocker.patch.object(sqlite3, 'connect', return_value=mock_obj)
        module = accounting.accountingFunction()

        # Act
        success, records, error_message = module.search_record(test_user_id, date_from, date_to)

        # Assert
        if success:
            assert len(records) == expected
        else:
            assert error_message == expected

    @pytest.mark.parametrize("test_user_id, date_from, date_to, expected", [
        (   1 , '20240101',       None, 1 ), # assume there are 2 records in the database from 20240101 to 20240102
    ])
    # this test case is to test the case where date_to is None, it suppose to return all records at date_from
    def test_search_record_normal_2(self, test_user_id, date_from, date_to, expected, mocker):
        # Arrange
        mock_obj = mock_db_conn()
        mock_obj.Cursor.lastrowid = 1
        mock_obj.Cursor.fetchone_results = [ User.User() ]
        mock_obj.Cursor.fetchone = lambda: mock_obj.Cursor.fetchone_results.pop(0)
        mock_obj.Cursor.fetchall_results = [
            (1, 1, 20240101,   'apple', 20, 'food', 'good_to_eat', '20240101'),
        ]
        mock_obj.Cursor.fetchall = lambda: mock_obj.Cursor.fetchall_results

        mocker.patch.object(sqlite3, 'connect', return_value=mock_obj)
        module = accounting.accountingFunction()

        # Act
        success, records, error_message = module.search_record(test_user_id, date_from, date_to)

        # Assert
        if success:
            assert len(records) == expected
        else:
            assert error_message == expected

    def test_search_record_normal_no_user(self, mocker):
        # Arrange
        mock_obj = mock_db_conn()
        mock_obj.Cursor.lastrowid = 1
        mock_obj.Cursor.fetchone_results = [ None ]
        mock_obj.Cursor.fetchone = lambda: mock_obj.Cursor.fetchone_results.pop(0)

        mocker.patch.object(sqlite3, 'connect', return_value=mock_obj)
        module = accounting.accountingFunction()

        # Act
        success, records, error_message = module.search_record(2, '20240101', '20240103')

        # Assert
        assert not success
        assert records == None
        assert error_message == 'user_id does not exist'