import sqlite3

import sys
sys.path.append('..')

import ipdb
from models import User

class lineFunction:
    def __init__(self):
        self.db_name = '../db.sqlite3'

    def create_line_user(self, line_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        user = None

        if type(line_id) is not str:
            return None

        try:
            # insert new user
            cursor.execute('INSERT INTO user (line_id) VALUES (?)', (line_id,))
            new_user_id = cursor.lastrowid
            
            # get user_id and create_date from new data
            cursor.execute('SELECT * FROM user WHERE user_id = ?', (new_user_id,))
            row = cursor.fetchone()
            user = User.User(user_id=row[0], line_id=row[1], create_date=row[2])
        except Exception as e:
            conn.rollback()

        conn.commit()
        conn.close()
        
        return user