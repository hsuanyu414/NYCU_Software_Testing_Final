import sqlite3

import sys
sys.path.append('..')

from models import Record

class accountingFunction:
    def __init__(self):
        self.db_name = '../db.sqlite3'
    def create_record(self, user_id, date, item, cost, category, comment):
        success = False
        record = None
        error_message = None

        # check if user_id is valid
        if not isinstance(user_id, int):
            error_message = 'invalid line_id parameter'
            return success, record, error_message

        # check if date is valid
        if not isinstance(date, str):
            error_message = 'invalid date parameter'
            return success, record, error_message

        # check if item is valid
        if not isinstance(item, str):
            error_message = 'invalid item parameter'
            return success, record, error_message

        # check if cost is valid
        if not isinstance(cost, int):
            error_message = 'invalid cost parameter'
            return success, record, error_message

        # check if category is valid
        if not isinstance(category, str):
            error_message = 'invalid category parameter'
            return success, record, error_message

        # check if comment is valid
        if not isinstance(comment, str):
            error_message = 'invalid comment parameter'
            return success, record, error_message

        # DB related
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # check if user_id exists
        cursor.execute('SELECT * FROM user WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        if row == None:
            error_message = 'user_id does not exist'
            return success, record, error_message

        try:
            # insert new record
            cursor.execute('INSERT INTO record (user_id, date, item, cost, category, comment) VALUES (?, ?, ?, ?, ?, ?)', (user_id, date, item, cost, category, comment))
            new_record_id = cursor.lastrowid

            # get record_id and create_date from new data
            cursor.execute('SELECT * FROM record WHERE record_id = ?', (new_record_id,))
            row = cursor.fetchone()
            record = Record.Record(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            record.date = str(record.date)
            record.create_date = str(record.create_date)
            success = True
        except Exception as e:
            error_message = str(e)
            conn.rollback()

        conn.commit()
        conn.close()
        # DB related end

        return success, record, error_message
    
    def show_recent_record(self, user_id, num=5, days=3, type='num'):
        success = False
        records = None
        error_message = None

        if not isinstance(user_id, int):
            error_message = 'invalid user_id parameter'
            return success, records, error_message
        
        if not isinstance(num, int):
            error_message = 'invalid num parameter'
            return success, records, error_message
        
        if not isinstance(days, int):
            error_message = 'invalid day parameter'
            return success, records, error_message
        
        if type!='num' and type!='days':
            error_message = 'invalid type parameter'
            return success, records, error_message
        
        # DB related
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # check if user_id exists
        cursor.execute('SELECT * FROM user WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        if row == None:
            error_message = 'user_id does not exist'
            return success, records, error_message
        
        if type == 'num':
            cursor.execute('SELECT * FROM record WHERE user_id = ? ORDER BY create_date DESC LIMIT ?', (user_id, num))
        elif type == 'days':
            cursor.execute('SELECT * FROM record WHERE user_id = ? AND create_date >= date("now", "-' + str(days) + ' day") ORDER BY create_date DESC', (user_id,))
        
        rows = cursor.fetchall()
        records = []


        for row in rows:
            record = Record.Record(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            record.date = str(record.date)
            record.create_date = str(record.create_date)
            records.append(record)
        success = True

        return success, records, error_message
            
    def search_record(self, user_id, date_from, date_to=None):
        success = False
        records = None
        error_message = None

        if not isinstance(user_id, int):
            error_message = 'invalid user_id parameter'
            return success, records, error_message

        if not isinstance(date_from, str):
            error_message = 'invalid date_from parameter'
            return success, records, error_message

        if date_to != None and not isinstance(date_to, str):
            error_message = 'invalid date_to parameter'
            return success, records, error_message

        # DB related
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # check if user_id exists
        cursor.execute('SELECT * FROM user WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        if row == None:
            error_message = 'user_id does not exist'
            return success, records, error_message

        if date_to == None:
            cursor.execute('SELECT * FROM record WHERE user_id = ? AND date = ?', (user_id, date_from))
        else:
            cursor.execute('SELECT * FROM record WHERE user_id = ? AND date >= ? AND date <= ?', (user_id, date_from, date_to))

        rows = cursor.fetchall()
        records = []

        for row in rows:
            record = Record.Record(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            record.date = str(record.date)
            record.create_date = str(record.create_date)
            records.append(record)
        success = True

        return success, records, error_message
