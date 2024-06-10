# Group work

## Predicate coverage & clause coverage & correlative active clause coverage

- # update record

```python
def update_record(self, user_id, record_id, date=None, item=None, cost=None, category=None, comment=None):
        success = False
        record = None
        error_message = None

        # check if user_id is valid
        if not isinstance(user_id, int):
            error_message = 'invalid user_id parameter'
            return success, record, error_message

        # check if record_id is valid
        if not isinstance(record_id, int):
            error_message = 'invalid record_id parameter'
            return success, record, error_message

        # check if item is valid
        if item != None and not isinstance(item, str):
            error_message = 'invalid item parameter'
            return success, record, error_message

        # check if cost is valid
        if cost != None and not isinstance(cost, int):
            error_message = 'invalid cost parameter'
            return success, record, error_message

        # check if category is valid
        if category != None and not isinstance(category, str):
            error_message = 'invalid category parameter'
            return success, record, error_message

        # check if comment is valid
        if comment != None and not isinstance(comment, str):
            error_message = 'invalid comment parameter'
            return success, record, error_message

        # check if date is valid
        if date != None and not isinstance(date, str):
            error_message = 'invalid date parameter'
            return success, record, error_message
        # DB related
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # check if user_id exists
        cursor.execute(
            'SELECT * FROM record WHERE user_id = ? AND record_id = ?', (user_id, record_id))
        row = cursor.fetchone()
        if row == None:
            error_message = 'the record of this id does not exist'
            return success, record, error_message
        # update record
        try:
            cursor.execute('UPDATE record SET item = COALESCE(?, item), cost = COALESCE(?, cost), category = COALESCE(?, category), comment = COALESCE(?, comment), date = COALESCE(?, date) WHERE user_id = ? AND record_id = ?',
                           (item, cost, category, comment, date, user_id, record_id))
            conn.commit()
            cursor.execute(
                'SELECT * FROM record WHERE user_id = ? AND record_id = ?', (user_id, record_id))
            row = cursor.fetchone()
            record = Record.Record(
                row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            record.date = str(record.date)
            record.create_date = str(record.create_date)
            success = True
        except Exception as e:
            error_message = str(e)
            conn.rollback()
        conn.close()
        return success, record, error_message
```
### 有 8 predicates
- if not isinstance(user_id, int):
    - predicate coverage
        - T  
            - ('123', 1, None, None, None, None, None)
        - F
            - (123, 1, None, None, None, None, None)
    - clause coverage (same as predicate coverage)
        - (not isinstance(user_id, int)) **(True)** (T)
            - ('123', 1, None, None, None, None, None)
        - (not isinstance(user_id, int)) **(False)** (F)
            - (123, 1, None, None, None, None, None)
    - correlative active clause coverage (same as predicate coverage)
        - (not isinstance(user_id, int)) **(True)** (T)
            - ('123', 1, None, None, None, None, None)
        - (not isinstance(user_id, int)) **(False)** (F)
            - (123, 1, None, None, None, None, None)
- if not isinstance(record_id, int):
    - predicate coverage
        - T
           - (1, '123', None, None, None, None, None)
        - F
           - (1, 123, None, None, None, None, None)
    - clause coverage (same as predicate coverage)
        - (not isinstance(record_id, int)) **(True)** (T)
           - (1, '123', None, None, None, None, None)
        - (not isinstance(record_id, int)) **(False)** (F)
           - (1, 123, None, None, None, None, None)
    - correlative active clause coverage (same as predicate coverage)
        - (not isinstance(record_id, int)) **(True)** (T)
           - (1, '123', None, None, None, None, None)
        - (not isinstance(record_id, int)) **(False)** (F)
           - (1, 123, None, None, None, None, None)
- if item != None and not isinstance(item, str):
    - predicate coverage
        - T
           - (1, 1, None, 123, None, None, None)
        - F
           - (1, 1, None, '123', None, None, None)
    - clause coverage
        - (item != None) **(True)** and (not isinstance(item, str)) **(True)** (T)
            - (1, 1, None, 123, None, None, None)
        - (item != None) **(True)** and (not isinstance(item, str)) **(False)** (F)
            - (1, 1, None, '123', None, None, None)
        - (item != None) **(False)** (F)
            - (1, 1, None, None, None, None, None)
    - correlative active clause coverage
        - (item != None)為Major
            - (item != None) **(True)** and (not isinstance(item, str)) **(True)** (T)
                - (1, 1, None, 123, None, None, None)
            - (item != None) **(False)** and (not isinstance(item, str)) **(True)** (F) (不可能發生)
        - (not isinstance(item, str))為Major
            - (item != None) **(True)** and (not isinstance(item, str)) **(True)** (T)
                - (1, 1, None, 123, None, None, None)
            - (item != None) **(True)** and (not isinstance(item, str)) **(False)** (F)
                - (1, 1, None, '123', None, None, None)
- if cost != None and not isinstance(cost, int):
    - predicate coverage
        - T
           - (1, 1, None, None, '123', None, None)
        - F
           - (1, 1, None, None, 123, None, None)
    - clause coverage
        - (cost != None) **(True)** and (not isinstance(cost, int)) **(True)** (T)
            - (1, 1, None, None, '123', None, None)
        - (cost != None) **(True)** and (not isinstance(cost, int)) **(False)** (F)
            - (1, 1, None, None, 123, None, None)
        - (cost != None) **(False)** (F)
            - (1, 1, None, None, None, None, None)
    - correlative active clause coverage
        - (cost != None)為Major
            - (cost != None) **(True)** and (not isinstance(cost, int)) **(True)** (T)
                - (1, 1, None, None, '123', None, None)
            - (cost != None) **(False)** and (not isinstance(cost, int)) **(True)** (F) (不可能發生)
        - (not isinstance(cost, int))為Major
            - (cost != None) **(True)** and (not isinstance(cost, int)) **(True)** (T)
                - (1, 1, None, None, '123', None, None)
            - (cost != None) **(True)** and (not isinstance(cost, int)) **(False)** (F)
                - (1, 1, None, None, 123, None, None)
- if category != None and not isinstance(category, str):
    - predicate coverage
        - T
           - (1, 1, None, None, None, 123, None)
        - F
           - (1, 1, None, None, None, '123', None)
    - clause coverage
        - (category != None) **(True)** and (not isinstance(category, str)) **(True)** (T)
            - (1, 1, None, None, None, 123, None)
        - (category != None) **(True)** and (not isinstance(category, str)) **(False)** (F)
            - (1, 1, None, None, None, '123', None)
        - (category != None) **(False)** (F)
            - (1, 1, None, None, None, None, None)
    - correlative active clause coverage
        - (category != None)為Major
            - (category != None) **(True)** and (not isinstance(category, str)) **(True)** (T)
                - (1, 1, None, None, None, 123, None)
            - (category != None) **(False)** and (not isinstance(category, str)) **(True)** (F) (不可能發生)
        - (not isinstance(category, str))為Major
            - (category != None) **(True)** and (not isinstance(category, str)) **(True)** (T)
                - (1, 1, None, None, None, 123, None)
            - (category != None) **(True)** and (not isinstance(category, str)) **(False)** (F)
                - (1, 1, None, None, None, '123', None)
- if comment != None and not isinstance(comment, str):
    - predicate coverage
        - T
           - (1, 1, None, None, None, None, 123)
        - F
           - (1, 1, None, None, None, None, '123')
    - clause coverage
        - (comment != None) **(True)** and (not isinstance(comment, str)) **(True)** (T)
            - (1, 1, None, None, None, None, 123)
        - (comment != None) **(True)** and (not isinstance(comment, str)) **(False)** (F)
            - (1, 1, None, None, None, None, '123')
        - (comment != None) **(False)** (F)
            - (1, 1, None, None, None, None, None)
    - correlative active clause coverage
        - (comment != None)為Major
            - (comment != None) **(True)** and (not isinstance(comment, str)) **(True)** (T)
                - (1, 1, None, None, None, None, 123)
            - (comment != None) **(False)** and (not isinstance(comment, str)) **(True)** (F) (不可能發生)
        - (not isinstance(comment, str))為Major
            - (comment != None) **(True)** and (not isinstance(comment, str)) **(True)** (T)
                - (1, 1, None, None, None, None, 123)
            - (comment != None) **(True)** and (not isinstance(comment, str)) **(False)** (F)
                - (1, 1, None, None, None, None, '123')
- if date != None and not isinstance(date, str):
    - predicate coverage
        - T
           - (1, 1, 20240103, None, None, None, None)
        - F
           - (1, 1, '20240103', None, None, None, None)
    - clause coverage
        - (date != None) **(True)** and (not isinstance(date, str)) **(True)** (T)
            - (1, 1, 20240103, None, None, None, None)
        - (date != None) **(True)** and (not isinstance(date, str)) **(False)** (F)
            - (1, 1, '20240103', None, None, None, None)
        - (date != None) **(False)** (F)
            - (1, 1, None, None, None, None, None)
    - correlative active clause coverage
        - (date != None)為Major
            - (date != None) **(True)** and (not isinstance(date, str)) **(True)** (T)
                - (1, 1, 20240103, None, None, None, None)
            - (date != None) **(False)** and (not isinstance(date, str)) **(True)** (F) (不可能發生)
        - (not isinstance(date, str))為Major
            - (date != None) **(True)** and (not isinstance(date, str)) **(True)** (T)
                - (1, 1, 20240103, None, None, None, None)
            - (date != None) **(True)** and (not isinstance(date, str)) **(False)** (F)
                - (1, 1, '20240103', None, None, None, None)
- if row == None:
    - predicate coverage
        - T
           - (1, 2, None, None, None, None, None) (if the record of this id does not exist)
        - F
           - (1, 1, None, None, None, None, None) (if the record of this id exists)     
    - clause coverage(same as predicate coverage)
        - (row == None) **(True)** (T)
            - (1, 2, None, None, None, None, None) (if the record of this id does not exist)
        - (row == None) **(False)** (F)
            - (1, 1, None, None, None, None, None) (if the record of this id exists)
    - correlative active clause coverage(same as predicate coverage)
        - (row == None) **(True)** (T)
            - (1, 2, None, None, None, None, None) (if the record of this id does not exist)
        - (row == None) **(False)** (F)
            - (1, 1, None, None, None, None, None) (if the record of this id exists)
- # delete record

```python
def delete_record(self, user_id, record_id):
        success = False
        error_message = None

        # check if user_id is valid
        if not isinstance(user_id, int):
            error_message = 'invalid user_id parameter'
            return success, None, error_message

        # check if record_id is valid
        if not isinstance(record_id, int):
            error_message = 'invalid record_id parameter'
            return success, None, error_message

        # DB related
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # check if the record of the user_id exists
        cursor.execute(
            'SELECT * FROM record WHERE user_id = ? AND record_id = ?', (user_id, record_id))
        row = cursor.fetchone()
        if row == None:
            error_message = 'the record of this id does not exist'
            return success, None, error_message

        try:
            cursor.execute(
                'DELETE FROM record WHERE record_id = ? AND user_id = ?', (record_id, user_id))
            conn.commit()
            success = True

        except Exception as e:
            error_message = str(e)
            conn.rollback()

        conn.close()
        return success, None, error_message
```
### 有 3 predicates
- if not isinstance(user_id, int):
    - predicate coverage
        - T  
            - ('123', 1)
        - F
            - (123, 1)
    - clause coverage (same as predicate coverage)
        - (not isinstance(user_id, int)) **(True)** (T)
            - ('123', 1)
        - (not isinstance(user_id, int)) **(False)** (F)
            - (123, 1)
    - correlative active clause coverage (same as predicate coverage)
        - (not isinstance(user_id, int)) **(True)** (T)
            - ('123', 1)
        - (not isinstance(user_id, int)) **(False)** (F)
            - (123, 1)
- if not isinstance(record_id, int):
    - predicate coverage
        - T
           - (1, '123')
        - F
           - (1, 123)
    - clause coverage (same as predicate coverage)
        - (not isinstance(record_id, int)) **(True)** (T)
           - (1, '123')
        - (not isinstance(record_id, int)) **(False)** (F)
           - (1, 123)
    - correlative active clause coverage (same as predicate coverage)
        - (not isinstance(record_id, int)) **(True)** (T)
           - (1, '123')
        - (not isinstance(record_id, int)) **(False)** (F)
           - (1, 123)
- if row == None:
    - predicate coverage
        - T
           - (1, 2) (if the record of this id does not exist)
        - F
           - (1, 1) (if the record of this id exists)     
    - clause coverage(same as predicate coverage)
        - (row == None) **(True)** (T)
            - (1, 2) (if the record of this id does not exist)
        - (row == None) **(False)** (F)
            - (1, 1) (if the record of this id exists)
    - correlative active clause coverage(same as predicate coverage)
        - (row == None) **(True)** (T)
            - (1, 2) (if the record of this id does not exist)
        - (row == None) **(False)** (F)
            - (1, 1) (if the record of this id exists)
- # export_record
    
```python
def export_record(self, user_id, method='this month'):
        # method: may this_month, this_year, all
        # transit a csv file to the user
        success = False
        error_message = None
        link = None
        if not isinstance(user_id, int):
            error_message = 'invalid user_id parameter'
            return success, link, error_message

        if method != 'this month' and method != 'this year' and method != 'all':
            error_message = 'invalid method parameter'
            return success, link, error_message

        # DB related
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # check if user_id exists
        cursor.execute('SELECT * FROM user WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        link = row
        if row == None:
            error_message = 'user_id does not exist'
            return success, link, error_message

        if method == 'this_month':
            cursor.execute(
                'SELECT * FROM record WHERE user_id = ? AND date >= date("now", "start of month")', (user_id,))
        elif method == 'this_year':
            cursor.execute(
                'SELECT * FROM record WHERE user_id = ? AND date >= date("now", "start of year")', (user_id,))
        elif method == 'all':
            cursor.execute(
                'SELECT * FROM record WHERE user_id = ?', (user_id,))

        rows = cursor.fetchall()
        conn.close()
        # write to csv file
        filepath = 'export_' + str(user_id) + '.csv'

        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['record_id', 'user_id', 'date', 'item',
                            'cost', 'category', 'comment', 'create_date'])
            for row in rows:
                writer.writerow(row)
        # upload to file.io
        resp = Fileio.upload(filepath, expires="5m")
        success = resp['success']  # True if upload was successful
        link = resp['link']
        os.remove(filepath)
        if not success:
            error_message = 'upload failed'
        return success, link, error_message
```
### 有 5 predicates
- if not isinstance(user_id, int):
    - predicate coverage
        - T  
            - ('123', 'this month')
        - F
            - (123, 'this month')
    - clause coverage (same as predicate coverage)
        - (not isinstance(user_id, int)) **(True)** (T)
            - ('123', 'this month')
        - (not isinstance(user_id, int)) **(False)** (F)
            - (123, 'this month')
    - correlative active clause coverage (same as predicate coverage)
        - (not isinstance(user_id, int)) **(True)** (T)
            - ('123', 'this month')
        - (not isinstance(user_id, int)) **(False)** (F)
            - (123, 'this month')
- if method != 'this month' and method != 'this year' and method != 'all':
    - predicate coverage
        - T
           - (1, 'this month')
        - F
           - (1, 'Hello')
    - clause coverage
        - (method != 'this month') **(True)** and (method != 'this year') **(True)** and (method != 'all') **(True)** (T)
            - (1, 'Hello')
        - (method != 'this month') **(True)** and (method != 'this year') **(True)** and (method != 'all') **(False)** (F)
            - (1, 'all')
        - (method != 'this month') **(True)** and (method != 'this year') **(False)**  and (method != 'all') **(True)** (F)
            - (1, 'this year')
        - (method != 'this month') **(False)** and (method != 'this year') **(True)** and (method != 'all') **(True)** (F)
            - (1, 'this month')
    - correlative active clause coverage
        - (method != 'this month')為Major
            - (method != 'this month') **(True)** and (method != 'this year') **(True)** and (method != 'all') **(True)** (T)
                - (1, 'Hello')
            - (method != 'this month') **(False)** and (method != 'this year') **(True)** and (method != 'all') **(True)** (F)
                - (1, 'this month')
        - (method != 'this year')為Major
            - (method != 'this month') **(True)** and (method != 'this year') **(True)** and (method != 'all') **(True)** (T)
                - (1, 'Hello')
            - (method != 'this month') **(True)** and (method != 'this year') **(False)** and (method != 'all') **(True)** (F)
                - (1, 'this year')
        - (method != 'all')為Major
            - (method != 'this month') **(True)** and (method != 'this year') **(True)** and (method != 'all') **(True)** (T)
                - (1, 'Hello')
            - (method != 'this month') **(True)** and (method != 'this year') **(True)** and (method != 'all') **(False)** (F)
                - (1, 'all')
- if row == None:
    - predicate coverage
        - T
           - (2, 'this month') (if user_id does not exist)
        - F
           - (1, 'this month') (if user_id exists)
    - clause coverage(same as predicate coverage)
        - (row == None) **(True)** (T)
            - (2, 'this month') (if user_id does not exist)
        - (row == None) **(False)** (F)
            - (1, 'this month') (if user_id exists)
    - correlative active clause coverage(same as predicate coverage)
        - (row == None) **(True)** (T)
            - (2, 'this month') (if user_id does not exist)
        - (row == None) **(False)** (F)
            - (1, 'this month') (if user_id exists)
- if method == 'this_month':
    - predicate coverage
        - T
           - (1, 'this month')
        - F
           - (1, 'this year')
    - clause coverage
        - (method == 'this_month') **(True)** (T)
            - (1, 'this month')
        - (method == 'this_month') **(False)** (F)
            - (1, 'this year')
    - correlative active clause coverage
        - (method == 'this_month') **(True)** (T)
            - (1, 'this month')
        - (method == 'this_month') **(False)** (F)
            - (1, 'this year')
- if method == 'this_year':
    - predicate coverage
        - T
           - (1, 'this year')
        - F
           - (1, 'this month')
    - clause coverage
        - (method == 'this_year') **(True)** (T)
            - (1, 'this year')
        - (method == 'this_year') **(False)** (F)
            - (1, 'this month')
    - correlative active clause coverage
        - (method == 'this_year') **(True)** (T)
            - (1, 'this year')
        - (method == 'this_year') **(False)** (F)
            - (1, 'this month')
- if method == 'all':
    - predicate coverage
        - T
           - (1, 'all')
        - F
           - (1, 'this month')
    - clause coverage
        - (method == 'all') **(True)** (T)
            - (1, 'all')
        - (method == 'all') **(False)** (F)
            - (1, 'this month')
    - correlative active clause coverage
        - (method == 'all') **(True)** (T)
            - (1, 'all')
        - (method == 'all') **(False)** (F)
            - (1, 'this month')
- if not success:
    - predicate coverage
        - T
           - (1, 'this month') (if upload failed)
        - F
           - (1, 'this month') (if upload success)
    - clause coverage(same as predicate coverage)
        - (not success) **(True)** (T)
            - (1, 'this month') (if upload failed)
        - (not success) **(False)** (F)
            - (1, 'this month') (if upload success)
    - correlative active clause coverage(same as predicate coverage)
        - (not success) **(True)** (T)
            - (1, 'this month') (if upload failed)
        - (not success) **(False)** (F)
            - (1, 'this month') (if upload success) 
        