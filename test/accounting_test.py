import pytest
import sys
from fileio_wrapper import Fileio
sys.path.append('..')
from accounting import accounting
from models import User, Record
from mock_obj import mock_db_conn

import sqlite3

class TestCreateRecord:
    # def create_record(user_id, date, item, cost, category, comment)
    @pytest.mark.parametrize("test_user_id, test_date, test_item, test_cost, test_category, test_comment, expected", [
        (   1 , '20240101', 'apple',  20 , 'food', 'good_to_eat', Record.Record(1, 1, '20240101', 'apple', 20, 'food', 'good_to_eat', '20240101')),
        (  '1', '20240101', 'apple',  20 , 'food', 'good_to_eat', 'invalid line_id parameter'),
        (   1 ,  20240101 , 'apple',  20 , 'food', 'good_to_eat', 'invalid date parameter'),
        (   1 , '20240101',   123  ,  20 , 'food', 'good_to_eat', 'invalid item parameter'),
        (   1 , '20240101', 'apple', '20', 'food', 'good_to_eat', 'invalid cost parameter'),
        (   1 , '20240101', 'apple',  20 ,   123 , 'good_to_eat', 'invalid category parameter'),
        (   1 , '20240101', 'apple',  20 , 'food',          123 , 'invalid comment parameter')
    ])
    def test_create_record(self, test_user_id, test_date, test_item, test_cost, test_category, test_comment, expected, mocker):
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
    def test_create_record_user_id_not_exist(self, test_user_id, test_date, test_item, test_cost, test_category, test_comment, expected, mocker):
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

    def test_create_record_error_while_creating(self, mocker):
        #Arrange
        mock_obj = mock_db_conn()
        mock_obj.Cursor.lastrowid = 1
        mock_obj.Cursor.fetchone_results = [1]
        mock_obj.Cursor.fetchone = lambda: mock_obj.Cursor.fetchone_results.pop(0)
        exec_count = 0
        def raiseExceptionsWhileSecondExecute(*args):
            nonlocal exec_count
            exec_count += 1
            if exec_count == 2:
                raise sqlite3.Error('Error while creating record')
        mock_obj.Cursor.execute = raiseExceptionsWhileSecondExecute

        mocker.patch.object(sqlite3, 'connect', return_value=mock_obj)
        
        module = accounting.accountingFunction()

        
        #Act
        success, record, error_message = module.create_record(1, '20240101', 'apple', 20, 'food', 'good_to_eat')

        #Assert
        assert error_message != None

class TestShowRecentRecord:
    # def show_recent_record(user_id, count)
    @pytest.mark.parametrize("test_user_id, test_num, test_day, test_type, expected", [
        # assumse today is 20240103
        (   1 ,  3 ,  1 ,  'num', 3 ), # assume there are more than 3 records in the database
        (  '1',  3 ,  1 ,  'num', 'invalid user_id parameter'),
        (   1 , '3',  1 ,  'num', 'invalid num parameter'),
        (   1 ,  3 , '1',  'num', 'invalid day parameter'),
        (   1 ,  3 ,  1 ,   123 , 'invalid type parameter')
    ])
    def test_show_recent_record(self, test_user_id, test_num, test_day, test_type, expected, mocker):
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
        (   1 ,  3 ,  1 , 'days', 1 ), # assume there is only 1 record in the database which is created today
    ])
    def test_show_recent_record_days(self, test_user_id, test_num, test_day, test_type, expected, mocker):
        # Arrange
        mock_obj = mock_db_conn()
        mock_obj.Cursor.lastrowid = 1
        mock_obj.Cursor.fetchone_results = [ User.User() ]
        mock_obj.Cursor.fetchone = lambda: mock_obj.Cursor.fetchone_results.pop(0)
        mock_obj.Cursor.fetchall_results = [
            (1, 1, 20240103, 'coconut', 40, 'food', 'good_to_eat', '20240103')
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
    
class TestSearchRecord:
    @pytest.mark.parametrize("test_user_id, date_from, date_to, expected", [
        # assumse today is 20240103
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

class TestUpdateRecord:
    @pytest.mark.parametrize("test_user_id, test_record_id, test_date, test_item, test_cost, test_category, test_comment, expected", [
        (   1 , 1, '20240101', 'apple',  20 , 'food', 'good_to_eat', 'the record of this id does not exist')
    ])
    def test_update_user_record_id_is_exist( self, test_user_id, test_record_id, test_date, test_item, test_cost, test_category, test_comment, expected, mocker):
        #Arrange
        mock_obj = mock_db_conn()
        mock_obj.Cursor.lastrowid = 1
        mock_obj.Cursor.fetchone_results = [ None]
        mock_obj.Cursor.fetchone = lambda: mock_obj.Cursor.fetchone_results.pop(0)

        mocker.patch.object(sqlite3, 'connect', return_value=mock_obj)
        module = accounting.accountingFunction()

        #Act
        success, record, error_message = module.update_record(test_user_id, test_record_id, test_date, test_item, test_cost, test_category, test_comment)

        assert not success
        assert record == None
        assert error_message == expected
    
    @pytest.mark.parametrize("test_user_id, test_record_id, test_date, test_item, test_cost, test_category, test_comment, expected", [
        ('1', 1, '20240101', 'apple',  20 , 'food', 'good_to_eat', 'invalid user_id parameter'),
        (1, '1','20240101', 'apple',  20 , 'food', 'good_to_eat', 'invalid record_id parameter'),
        (1, 1,  20240101 , 'apple',  20 , 'food', 'good_to_eat', 'invalid date parameter'),
        (1, 1, '20240101', 20, 20, 'food', 'good_to_eat', 'invalid item parameter'),
        (1, 1, '20240101', 'apple', '20', 'food', 'good_to_eat', 'invalid cost parameter'),
        (1, 1, '20240101', 'apple',  20 ,   123 , 'good_to_eat', 'invalid category parameter'),
        (1, 1, '20240101', 'apple',  20 , 'food',          123 , 'invalid comment parameter')
    ])
    def test_update_user_record_invalid_parameter( self, test_user_id, test_record_id, test_date, test_item, test_cost, test_category, test_comment, expected, mocker):
        #Arrange
        mock_obj = mock_db_conn()
        mock_obj.Cursor.lastrowid = 1
        mock_obj.Cursor.fetchone_results = [ (1, 1, '20240101', 'apple', 20, 'food', 'good_to_eat', '20240101')]
        mock_obj.Cursor.fetchone = lambda: mock_obj.Cursor.fetchone_results.pop(0)

        mocker.patch.object(sqlite3, 'connect', return_value=mock_obj)
        module = accounting.accountingFunction()

        #Act
        success, record, error_message = module.update_record(test_user_id, test_record_id, test_date, test_item, test_cost, test_category, test_comment)

        assert not success
        assert record == None
        assert error_message == expected
    @pytest.mark.parametrize("test_user_id, test_record_id, test_date, test_item, test_cost, test_category, test_comment, expected", [
        (   1 , 1,'20240101', 'apple',  20 , 'food', 'good_to_eat', Record.Record(1, 1, '20240101', 'apple', 20, 'food', 'good_to_eat', '20240101') )
    ])
    def test_update_success( self, test_user_id, test_record_id, test_date, test_item, test_cost, test_category, test_comment, expected, mocker):
        #Arrange
        mock_obj = mock_db_conn()
        mock_obj.Cursor.lastrowid = 1
        mock_obj.Cursor.fetchone_results = [ (1, 1, '20240101', 'apple', 20, 'food', 'good_to_eat', '20240101')]
        mock_obj.Cursor.fetchone = lambda: mock_obj.Cursor.fetchone_results[0]
        mocker.patch.object(sqlite3, 'connect', return_value=mock_obj)
        module = accounting.accountingFunction()

        #Act
        success, record, error_message = module.update_record(test_user_id, test_record_id, test_date, test_item, test_cost, test_category, test_comment)
        assert success == True
        assert record.user_id == expected.user_id
        assert record.date == expected.date
        assert record.item == expected.item
        assert record.cost == expected.cost
        assert record.category == expected.category
        assert record.comment == expected.comment
        assert record.create_date != None   
        assert error_message == None

    def test_update_error_while_updating(self, mocker):
        #Arrange
        mock_obj = mock_db_conn()
        mock_obj.Cursor.lastrowid = 1
        mock_obj.Cursor.fetchone_results = [ (1, 1, '20240101', 'apple', 20, 'food', 'good_to_eat', '20240101')]
        mock_obj.Cursor.fetchone = lambda: mock_obj.Cursor.fetchone_results[0]
        exec_count = 0
        def raiseExceptionsWhileSecondExecute(*args):
            nonlocal exec_count
            exec_count += 1
            if exec_count == 2:
                raise sqlite3.Error('Error while updating record')
        mock_obj.Cursor.execute = raiseExceptionsWhileSecondExecute

        mocker.patch.object(sqlite3, 'connect', return_value=mock_obj)
        module = accounting.accountingFunction()

        #Act
        success, record, error_message = module.update_record(1, 1, 'apple', 20, 'food', 'good_to_eat')

        #Assert
        assert error_message != None
    @pytest.mark.parametrize("test_user_id, test_record_id, test_date, test_item, test_cost, test_category, test_comment, expected", [
        (   1 , 1,'20240101', 'apple',  20 , 'food', 'good_to_eat', 'Error while updating record' )
    ])
    def test_update_exception( self, test_user_id, test_record_id, test_date, test_item, test_cost, test_category, test_comment, expected, mocker):
        #Arrange
        mock_obj = mock_db_conn()
        mock_obj.Cursor.lastrowid = 1
        mock_obj.Cursor.fetchone_results = [ (1, 1, '20240101', 'apple', 20, 'food', 'good_to_eat', '20240101')]
        mock_obj.Cursor.fetchone = lambda: mock_obj.Cursor.fetchone_results[0]
        exec_count = 0
        def raiseExceptionsWhileSecondExecute(*args):
            nonlocal exec_count
            exec_count += 1
            if exec_count == 2:
                raise sqlite3.Error('Error while updating record')
        mock_obj.Cursor.execute = raiseExceptionsWhileSecondExecute

        mocker.patch.object(sqlite3, 'connect', return_value=mock_obj)
        module = accounting.accountingFunction()

        #Act
        success, record, error_message = module.update_record(test_user_id, test_record_id, test_date, test_item, test_cost, test_category, test_comment)
        assert success == False
        assert error_message == expected
class TestDeleteRecord:
    @pytest.mark.parametrize("test_user_id, test_record_id, expected", [
        (   2 , 1, 'the record of this id does not exist')
    ])
    def test_delete_user_record_id_is_exist( self, test_user_id, test_record_id, expected, mocker):
        #Arrange
        mock_obj = mock_db_conn()
        mock_obj.Cursor.lastrowid = 1
        mock_obj.Cursor.fetchone_results = [ None]
        mock_obj.Cursor.fetchone = lambda: mock_obj.Cursor.fetchone_results.pop(0)

        mocker.patch.object(sqlite3, 'connect', return_value=mock_obj)
        module = accounting.accountingFunction()

        #Act
        success,_, error_message = module.delete_record(test_user_id, test_record_id)

        assert not success
        assert error_message == expected
    
    @pytest.mark.parametrize("test_user_id, test_record_id, expected", [
        (  '1', 1, 'invalid user_id parameter'),
        (1, '1', 'invalid record_id parameter')
    ])
    def test_delete_user_record_invalid_parameter( self, test_user_id, test_record_id, expected, mocker):
        #Arrange
        mock_obj = mock_db_conn()
        mock_obj.Cursor.lastrowid = 1
        mock_obj.Cursor.fetchone_results = [ (1, 1, '20240101', 'apple', 20, 'food', 'good_to_eat', '20240101')]
        mock_obj.Cursor.fetchone = lambda: mock_obj.Cursor.fetchone_results.pop(0)

        mocker.patch.object(sqlite3, 'connect', return_value=mock_obj)
        module = accounting.accountingFunction()

        #Act
        success,_, error_message = module.delete_record(test_user_id, test_record_id)

        assert not success
        assert error_message == expected
    @pytest.mark.parametrize("test_user_id, test_record_id, expected", [
        (   1 , 1, None )
    ])
    def test_delete_success( self, test_user_id, test_record_id, expected, mocker):
        #Arrange
        mock_obj = mock_db_conn()
        mock_obj.Cursor.lastrowid = 1
        mock_obj.Cursor.fetchone_results = [ (1, 1, '20240101', 'apple', 20, 'food', 'good_to_eat', '20240101')]
        mock_obj.Cursor.fetchone = lambda: mock_obj.Cursor.fetchone_results[0]
        mocker.patch.object(sqlite3, 'connect', return_value=mock_obj)
        module = accounting.accountingFunction()

        #Act
        success, _, error_message = module.delete_record(test_user_id, test_record_id)
        assert success == True
        assert error_message == None
    @pytest.mark.parametrize("test_user_id, test_record_id, expected", [
        (   1 , 1, 'Error while deleting record' )
    ])
    def test_delete_exception( self, test_user_id, test_record_id, expected, mocker):
        #Arrange
        mock_obj = mock_db_conn()
        mock_obj.Cursor.lastrowid = 1
        mock_obj.Cursor.fetchone_results = [ (1, 1, '20240101', 'apple', 20, 'food', 'good_to_eat', '20240101')]
        mock_obj.Cursor.fetchone = lambda: mock_obj.Cursor.fetchone_results[0]
        exec_count = 0
        def raiseExceptionsWhileSecondExecute(*args):
            nonlocal exec_count
            exec_count += 1
            if exec_count == 2:
                raise sqlite3.Error('Error while deleting record')
        mock_obj.Cursor.execute = raiseExceptionsWhileSecondExecute

        mocker.patch.object(sqlite3, 'connect', return_value=mock_obj)
        module = accounting.accountingFunction()

        #Act
        success, _, error_message = module.delete_record(test_user_id, test_record_id)
        assert success == False
        assert error_message == expected
class TestRecordExport:
    @pytest.mark.parametrize("test_user_id, test_method, expected", [
        (   2 , 'this month', 'user_id does not exist')
    ])
    def test_export_user_id_is_exist( self, test_user_id, test_method, expected, mocker):
        #Arrange
        mock_obj = mock_db_conn()
        mock_obj.Cursor.lastrowid = 1
        mock_obj.Cursor.fetchone_results = [ None]
        mock_obj.Cursor.fetchone = lambda: mock_obj.Cursor.fetchone_results.pop(0)

        mocker.patch.object(sqlite3, 'connect', return_value=mock_obj)
        module = accounting.accountingFunction()

        #Act
        success, link, error_message = module.export_record(test_user_id, test_method)

        assert link == None
        assert success == False
        assert error_message == expected
    
    @pytest.mark.parametrize("test_user_id, test_method, expected", [
        (  '1', 'this month', 'invalid user_id parameter'),
        (1, '123', 'invalid method parameter')
    ])
    def test_export_invalid_parameter( self, test_user_id, test_method, expected, mocker):
        #Arrange
        mock_obj = mock_db_conn()
        mock_obj.Cursor.lastrowid = 1
        mock_obj.Cursor.fetchone_results = [ (1, 1, '20240101', 'apple', 20, 'food', 'good_to_eat', '20240101')]
        mock_obj.Cursor.fetchone = lambda: mock_obj.Cursor.fetchone_results.pop(0)

        mocker.patch.object(sqlite3, 'connect', return_value=mock_obj)
        module = accounting.accountingFunction()

        #Act
        success, link, error_message = module.export_record(test_user_id, test_method)
        assert success == False
        assert error_message == expected
        assert link == None
    @pytest.mark.parametrize("test_user_id, test_method, expected", [
        (   1 , 'this month', 'export success' ),
        (1, 'this year', 'export success'),
        (1, 'all', 'export success')
    ])
    def test_export_success( self, test_user_id, test_method, expected, mocker):
        #Arrange
        mock_obj = mock_db_conn()
        mock_obj.Cursor.lastrowid = 1
        mock_obj.Cursor.fetchone_results = [ User.User() ]
        mock_obj.Cursor.fetchone = lambda: mock_obj.Cursor.fetchone_results.pop(0)
        mock_obj.Cursor.fetchall_results = [
            (1, 1, 20240103, 'coconut', 40, 'food', 'good_to_eat', '20240103')
        ]
        mock_obj.Cursor.fetchall = lambda: mock_obj.Cursor.fetchall_results
        mocker.patch.object(sqlite3, 'connect', return_value=mock_obj)
        open = mocker.mock_open()
        mocker.patch('builtins.open', open)
        mock_upload_response = {
            'success': True,
            'link': 'https://example.com/file_link'
        }
        mocker.patch.object(Fileio, 'upload', return_value=mock_upload_response)
        # mock os.remove
        mocker.patch('os.remove', return_value=None)
        module = accounting.accountingFunction()
        #Act
        success, link, error_message = module.export_record(test_user_id, test_method)
        assert success == True
        assert error_message == None
        assert link != None
        assert link != ''
    @pytest.mark.parametrize("test_user_id, test_method, expected", [
        (   1 , 'this month', 'export false' )
    ])
    def test_export_false( self, test_user_id, test_method, expected, mocker):
        #Arrange
        mock_obj = mock_db_conn()
        mock_obj.Cursor.lastrowid = 1
        mock_obj.Cursor.fetchone_results = [ User.User() ]
        mock_obj.Cursor.fetchone = lambda: mock_obj.Cursor.fetchone_results.pop(0)
        mock_obj.Cursor.fetchall_results = [
            (1, 1, 20240103, 'coconut', 40, 'food', 'good_to_eat', '20240103')
        ]
        mock_obj.Cursor.fetchall = lambda: mock_obj.Cursor.fetchall_results
        mocker.patch.object(sqlite3, 'connect', return_value=mock_obj)
        open = mocker.mock_open()
        mocker.patch('builtins.open', open)
        mock_upload_response = {
            'success': False,
            'link': ''
        }
        mocker.patch.object(Fileio, 'upload', return_value=mock_upload_response)
        # mock os.remove
        mocker.patch('os.remove', return_value=None)
        module = accounting.accountingFunction()
        #Act
        success, link, error_message = module.export_record(test_user_id, test_method)
        assert success == False
        assert error_message == 'upload failed'
        assert link == ''
