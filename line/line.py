from models import User
import sqlite3

import sys
sys.path.append('..')


class lineFunction:
    def __init__(self, db_name = "../db.sqlite3"):
        self.db_name = db_name

    def create_line_user(self, line_id):
        success = False
        user = None
        error_message = None

        # check if line_id is valid
        if not isinstance(line_id, str):
            error_message = 'invalid line_id parameter'
            return success, user, error_message

        # DB related
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # check if line_id is already in the database
        cursor.execute('SELECT * FROM user WHERE line_id = ?', (line_id,))
        row = cursor.fetchone()
        if row != None:
            error_message = 'line_id already exists'
            return success, user, error_message

        try:
            # insert new user
            cursor.execute('INSERT INTO user (line_id) VALUES (?)', (line_id,))
            new_user_id = cursor.lastrowid

            # get user_id and create_date from new data
            cursor.execute(
                'SELECT * FROM user WHERE user_id = ?', (new_user_id,))
            row = cursor.fetchone()
            user = User.User(
                user_id=row[0], line_id=row[1], create_date=row[2])
            success = True
        except Exception as e:
            error_message = str(e)
            conn.rollback()

        conn.commit()
        conn.close()
        # DB related end

        return success, user, error_message

    def get_user_by_line_id(self, line_id):
        '''
        Get line_id for accounting functions by line_id warpped in MessageEvent object
        arg: 
            - line_id (str)
        '''
        success = False
        user = None
        error_message = None

        # check if line_id is valid
        if not isinstance(line_id, str):
            error_message = 'invalid line_id parameter'
            return success, user, error_message

        # DB related
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # find user by line_id
        cursor.execute('SELECT * FROM user WHERE line_id = ?', (line_id,))
        row = cursor.fetchone()
        if row == None:
            error_message = 'user not found'
            return success, user, error_message

        user = User.User(user_id=row[0], line_id=row[1], create_date=row[2])

        success = True
        conn.close()
        # DB related end

        return success, user, error_message
