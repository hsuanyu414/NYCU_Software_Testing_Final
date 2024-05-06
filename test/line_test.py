import pytest

import sys

sys.path.append('..')
from line import line

class TestLine:
    def test_create_line_user(self):
        # Arrange
        module = line.lineFunction()
        test_line_id = 'U123456789'

        # Act
        ret_val = module.create_line_user(test_line_id)

        # Assert
        assert ret_val != None