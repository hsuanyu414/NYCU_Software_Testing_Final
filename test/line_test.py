import pytest

import sys

sys.path.append('..')
from line import line
from models import User
import sqlite3

class TestLine:
    @pytest.mark.parametrize("test_line_id, expected", [
        ('U123456789', 'U123456789'),
        ('U123456789', 'line_id already exists'),
        (123456789, 'invalid line_id parameter')

    ])
    def test_create_line_user(self, test_line_id, expected):
        # Arrange
        module = line.lineFunction()
        
        # Act
        success, user, error_message = module.create_line_user(test_line_id)

        # Assert
        if success:
            assert user.line_id == expected
        else:
            assert error_message == expected