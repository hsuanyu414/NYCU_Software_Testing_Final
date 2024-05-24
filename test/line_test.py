import pytest

import sys

sys.path.append('..')
from line import line
from models import User
from mock_obj import mock_db_conn

import sqlite3
        
class TestLine:
    @pytest.mark.parametrize("test_line_id, expected", [
        ('U123456789', 'U123456789'),
        (123456789, 'invalid line_id parameter')
    ])
    def test_create_line_user_single(self, test_line_id, expected, mocker):
        # Arrange
        mock_obj = mock_db_conn()
        mock_obj.Cursor.lastrowid = 1
        mock_obj.Cursor.fetchone_results = [None, (1, 'U123456789', '2021-01-01 00:00:00')]
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

        

    @pytest.mark.parametrize("test_line_ids, expecteds", [
        (['U123456789', 'U123456789'], ['U123456789', 'line_id already exists'])
    ])
    def test_create_line_user_multiple(self, test_line_ids, expecteds, mocker):
        # Arrange
        mock_obj = mock_db_conn()
        mock_obj.Cursor.lastrowid = 1
        mock_obj.Cursor.fetchone_results = [None, (1, 'U123456789', '2021-01-01 00:00:00'), (1, 'U123456789', '2021-01-01 00:00:00')]
        mock_obj.Cursor.fetchone = lambda: mock_obj.Cursor.fetchone_results.pop(0)

        module = line.lineFunction()
        mocker.patch.object(sqlite3, 'connect', return_value=mock_obj)
        
        # Act
        for test_line_id, expected in zip(test_line_ids, expecteds):
            success, user, error_message = module.create_line_user(test_line_id)
            
            # Assert
            if success:
                assert user.line_id == expected
            else:
                assert error_message == expected

    @pytest.mark.parametrize("test_line_id, expected", [
        ('U123456789', 'U123456789'),
        (123456789, 'invalid line_id parameter')
    ])
    def test_get_user_by_line_id(self, test_line_id, expected, mocker):
        # Arrange
        mock_obj = mock_db_conn()
        mock_obj.Cursor.fetchone_results = [(1, 'U123456789', '2021-01-01 00:00:00')]
        mock_obj.Cursor.fetchone = lambda: mock_obj.Cursor.fetchone_results.pop(0)

        module = line.lineFunction()
        mocker.patch.object(sqlite3, 'connect', return_value=mock_obj)
        
        # Act
        success, user, error_message = module.get_user_by_line_id(test_line_id)
        
        # Assert
        if success:
            assert user.line_id == expected
        else:
            assert error_message == expected