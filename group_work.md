# Groupwork: Logic Coverage for Your Project
## Team 7

<!-- Please design tests to satisfy PC (predicate coverage), CC(clause coverage), and CACC(correlated active clause coverage)  for your proposed project (if TDD with no implementation, design tests on the requirements or specifications). If it is hard to design tests from your proposed project with logic coverage, you can take Thermostat class (please look at additional file) as the target.  -->

對每個我們 spec 中的 function，我們將設計測試以滿足 PC, CC, 和 CACC。

以下 source code 為我們 github repository main 分支上中 419aa6b 的版本。

假設有一 predicate P = A && B，測試資料表達方法如下
`T t t`: P 為 true, A 為 true, B 為 true

## Line module
### def create_line_user(self, line_id):
Source code:
```python
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
            cursor.execute('SELECT * FROM user WHERE user_id = ?', (new_user_id,))
            row = cursor.fetchone()
            user = User.User(user_id=row[0], line_id=row[1], create_date=row[2])
            success = True
        except Exception as e:
            error_message = str(e)
            conn.rollback()

        conn.commit()
        conn.close()
        # DB related end
        
        return success, user, error_message
```
對於此 function，我們有兩個 predicate
- not isinstance(line_id, str)，以下簡稱 P1
    - A: isinstance(line_id, str)
    - P1: !A
    - 因此 predicate 只有一個 clause，故此處 CC = PC = CACC
    - 測試資料設計如下
        - T f
            - create_line_user(123456789)
        - F t
            - create_line_user("U123456789")
            - mock 資料庫使 fetchone() 回傳 None
    - 測試
- row != None，以下簡稱 P2
    - A: row != None
    - P2: A
    - 因此 predicate 只有一個 clause，故此處 CC = PC = CACC
    - 測試資料設計如下
        - T t
            - create_line_user("U123456789")
            - mock 資料庫使 fetchone() 回傳 User 資料為非 None
        - F f
            - create_line_user("U123456789")
            - mock 資料庫使 fetchone() 回傳 User 資料為 None


### def create_record(self, user_id, date, item, cost, category, comment)

Source code:
```python
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
```

對於此 function，我們有七個 predicate
- not isinstance(user_id, int):，以下簡稱 P1
    - A: isinstance(user_id, int)
    - P1: !A
    - 因此 predicate 只有一個 clause，故此處 CC = PC = CACC
    - 測試資料設計如下
        - T f
            - create_record('1', '20240101', 'apple',  20 , 'food', 'good_to_eat')
            - Expected: error_message = 'invalid line_id parameter'
        - F t
            - create_record(1 , '20240101', 'apple',  20 , 'food', 'good_to_eat')
            - mock 資料庫使 fetchone() 分別回傳 User 資料和 Record 資料皆為非 None
            - Expected: success = True, record = Record(1, '20240101', 'apple',  20 , 'food', 'good_to_eat')
- not isinstance(date, str):，以下簡稱 P2
    - A: isinstance(date, str)
    - P2: !A
    - 因此 predicate 只有一個 clause，故此處 CC = PC = CACC
    - 測試資料設計如下
        - T f
            - create_record(1 , 20240101, 'apple',  20 , 'food', 'good_to_eat')
            - Expected: error_message = 'invalid date parameter'
        - F t
            - create_record(1 , '20240101', 'apple',  20 , 'food', 'good_to_eat')
            - mock 資料庫使 fetchone() 分別回傳 User 資料和 Record 資料皆為非 None
            - Expected: success = True, record = Record(1, '20240101', 'apple',  20 , 'food', 'good_to_eat')
- not isinstance(item, str):，以下簡稱 P3
    - A: isinstance(item, str)
    - P3: !A
    - 因此 predicate 只有一個 clause，故此處 CC = PC = CACC
    - 測試資料設計如下
        - T f
            - create_record(1 , '20240101', 123,  20 , 'food', 'good_to_eat')
            - Expected: error_message = 'invalid item parameter'
        - F t
            - create_record(1 , '20240101', 'apple',  20 , 'food', 'good_to_eat')
            - mock 資料庫使 fetchone() 分別回傳 User 資料和 Record 資料皆為非 None
            - Expected: success = True, record = Record(1, '20240101', 'apple',  20 , 'food', 'good_to_eat')
- not isinstance(cost, int):，以下簡稱 P4
    - A: isinstance(cost, int)
    - P4: !A
    - 因此 predicate 只有一個 clause，故此處 CC = PC = CACC
    - 測試資料設計如下
        - T f
            - create_record(1 , '20240101', 'apple',  '20' , 'food', 'good_to_eat')
            - Expected: error_message = 'invalid cost parameter'
        - F t
            - create_record(1 , '20240101', 'apple',  20 , 'food', 'good_to_eat')
            - mock 資料庫使 fetchone() 分別回傳 User 資料和 Record 資料皆為非 None
            - Expected: success = True, record = Record(1, '20240101', 'apple',  20 , 'food', 'good_to_eat')
- not isinstance(category, str):
    - A: isinstance(category, str)
    - P5: !A
    - 因此 predicate 只有一個 clause，故此處 CC = PC = CACC
    - 測試資料設計如下
        - T f
            - create_record(1 , '20240101', 'apple',  20 , 123, 'good_to_eat')
            - Expected: error_message = 'invalid category parameter'
        - F t
            - create_record(1 , '20240101', 'apple',  20 , 'food', 'good_to_eat')
            - mock 資料庫使 fetchone() 分別回傳 User 資料和 Record 資料皆為非 None
            - Expected: success = True, record = Record(1, '20240101', 'apple',  20 , 'food', 'good_to_eat')
- not isinstance(comment, str):
    - A: isinstance(comment, str)
    - P6: !A
    - 因此 predicate 只有一個 clause，故此處 CC = PC = CACC
    - 測試資料設計如下
        - T f
            - create_record(1 , '20240101', 'apple',  20 , 'food', 123)
            - Expected: error_message = 'invalid comment parameter'
        - F t
            - create_record(1 , '20240101', 'apple',  20 , 'food', 'good_to_eat')
            - mock 資料庫使 fetchone() 分別回傳 User 資料和 Record 資料皆為非 None
            - Expected: success = True, record = Record(1, '20240101', 'apple',  20 , 'food', 'good_to_eat')
            
- row == None:
    - A: row == None
    - P7: A
    - 因此 predicate 只有一個 clause，故此處 CC = PC = CACC
    - 測試資料設計如下
        - T t
            - create_record(2 , '20240101', 'apple',  20 , 'food', 'good_to_eat')
            - mock 資料庫使 fetchone() 回傳 User 資料為 None
            - Expected: error_message = 'user_id does not exist'
        - F f
            - create_record(1 , '20240101', 'apple',  20 , 'food', 'good_to_eat')
            - mock 資料庫使 fetchone() 回傳 User 資料和 Record 資料皆為非 None
            - Expected: success = True, record = Record(1, '20240101', 'apple',  20 , 'food', 'good_to_eat')

###  def show_recent_record(self, user_id, num=5, days=3, type='num'):
Source code:
```python
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
```
對於此 function，我們有 6 個 predicate
- if not isinstance(user_id, int):，以下簡稱 P1
    - A: isinstance(user_id, int)
    - P1: !A
    - 因此 predicate 只有一個 clause，故此處 CC = PC = CACC
    - 測試資料設計如下
        - T f
            - show_recent_record('1',  3 ,  1 ,  'num')
            - Expected: error_message = 'invalid user_id parameter'        
        - F t
            - show_recent_record( 1 ,  3 ,  1 ,  'num')
            - mock 資料庫使 fetchone() 回傳 User 資料為非 None，且 Record 資料有 3 筆
            - Expected: success = True, len(records) = 3 
- if not isinstance(num, int):，以下簡稱 P2
    - A: isinstance(num, int)
    - P2: !A
    - 因此 predicate 只有一個 clause，故此處 CC = PC = CACC
    - 測試資料設計如下
        - T f
            - show_recent_record( 1 , '3' ,  1 ,  'num')
            - Expected: error_message = 'invalid num parameter'
        - F t
            - show_recent_record( 1 ,  3 ,  1 ,  'num')
            - mock 資料庫使 fetchone() 回傳 User 資料為非 None，且 Record 資料有 3 筆
            - Expected: success = True, len(records) = 3
- if not isinstance(days, int):，以下簡稱 P3
    - A: isinstance(days, int)
    - P3: !A
    - 因此 predicate 只有一個 clause，故此處 CC = PC = CACC
    - 測試資料設計如下
        - T f
            - show_recent_record( 1 ,  3 ,  '1' ,  'num')
            - Expected: error_message = 'invalid day parameter'
        - F t
            - show_recent_record( 1 ,  3 ,  1 ,  'num')
            - Expected: success = True, len(records) = 3
- if type!='num' and type!='days':，以下簡稱 P4
    - A: type != 'num'
    - B: type != 'days'
    - P4: A && B
    - PC:
        - T t t
            - show_recent_record( 1 ,  3 ,  1 , 123)
            - Expected: error_message = 'invalid type parameter'
        - F t f
            - show_recent_record( 1 ,  3 ,  1 , 'num')
            - mock 資料庫使 fetchone() 回傳 User 資料為非 None，且 Record 資料有 3 筆
            - Expected: success = True, len(records) = 3
    - CC:
        - F t f
            - show_recent_record( 1 ,  3 ,  1 , 'days')
            - mock 資料庫使 fetchone() 回傳 User 資料為非 None，且 Record 資料有 3 筆
            - Expected: success = True, len(records) = 3
        - F f t
            - show_recent_record( 1 ,  3 ,  1 , 'num')
            - mock 資料庫使 fetchone() 回傳 User 資料為非 None，且 Record 資料有 3 筆
            - Expected: success = True, len(records) = 3
    - CACC:
        - T t t ( A as Major )
            - show_recent_record( 1 ,  3 ,  1 , 123)
            - Expected: error_message = 'invalid type parameter'
        - F f t ( A as Major )
            - show_recent_record( 1 ,  3 ,  1 , 'num')
            - mock 資料庫使 fetchone() 回傳 User 資料為非 None，且 Record 資料有 3 筆
            - Expected: success = True, len(records) = 3
        - F t f ( B as Major )
            - show_recent_record( 1 ,  3 ,  1 , 'days')
            - mock 資料庫使 fetchone() 回傳 User 資料為非 None，且 Record 資料有 3 筆
            - Expected: success = True, len(records) = 3
- if row == None:，以下簡稱 P5
    - A: row == None
    - P5: A
    - 因此 predicate 只有一個 clause，故此處 CC = PC = CACC
    - 測試資料設計如下
        - T t
            - show_recent_record( 2 ,  3 ,  1 , 'num')
            - mock 資料庫使 fetchone() 回傳 User 資料為 None
            - Expected: error_message = 'user_id does not exist'
        - F f
            - show_recent_record( 1 ,  3 ,  1 , 'num')
            - mock 資料庫使 fetchone() 回傳 User 資料為非 None，且 Record 資料有 3 筆
            - Expected: success = True, len(records) = 3

- if type == 'num': ... elif type == 'days': ...，以下簡稱 P6
    - A: type == 'num'
    - B: type == 'days'
    - C6: A || (!A && B) 簡化後為 A || B
    - PC:
        - 無法完成 PC，因在實作上執行到此時，type 只會是 'num' 或 'days' 其中一個，故 predicate 必定為 true
    - CC:
        - T t f
            - show_recent_record( 1 ,  3 ,  1 , 'num')
            - mock 資料庫使 fetchone() 回傳 User 資料為非 None，且 Record 資料有 3 筆
            - Expected: success = True, len(records) = 3
        - T f t
            - show_recent_record( 1 ,  3 ,  1 , 'days')
            - mock 資料庫使 fetchone() 回傳 User 資料為非 None，且 Record 資料有 3 筆
            - Expected: success = True, len(records) = 3
    - CACC:
        - A as major
            - T t f (pick this)
            - F f f
        - B as major
            - T f t (pick this)
            - F f f 
        - T t f ( A as Major )
            - show_recent_record( 1 ,  3 ,  1 , 'num')
            - mock 資料庫使 fetchone() 回傳 User 資料為非 None，且 Record 資料有 3 筆
            - Expected: success = True, len(records) = 3
        - T f t ( B as Major )
            - show_recent_record( 1 ,  3 ,  1 , 'days')
            - mock 資料庫使 fetchone() 回傳 User 資料為非 None，且 Record 資料有 3 筆
            - Expected: success = True, len(records) = 3
        

### def search_record(self, user_id, date_from, date_to=None):

Source Code:
```python
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
```

對於此 function，我們有 5 個 predicate
- if not isinstance(user_id, int):，以下簡稱 P1
    - A: isinstance(user_id, int)
    - P1: !A
    - 因此 predicate 只有一個 clause，故此處 CC = PC = CACC
    - 測試資料設計如下
        - T f
            - search_record('1', '20240101', '20240103')
            - Expected: error_message = 'invalid user_id parameter'
        - F t
            - search_record(1, '20240101', '20240103')
            - mock 資料庫使 fetchone() 回傳 User 資料為非 None，且 Record 資料有 3 筆，當中有 3 筆符合條件
            - Expected: success = True, len(records) = 3
- if not isinstance(date_from, str):，以下簡稱 P2
    - A: isinstance(date_from, str)
    - P2: !A
    - 因此 predicate 只有一個 clause，故此處 CC = PC = CACC
    - 測試資料設計如下
        - T f
            - search_record(1, 20240101, '20240103')
            - Expected: error_message = 'invalid date_from parameter'
        - F t
            - search_record(1, '20240101', '20240103')
            - mock 資料庫使 fetchone() 回傳 User 資料為非 None，且 Record 資料有 3 筆，且當中有 3 筆符合條件
            - Expected: success = True, len(records) = 3
- if date_to != None and not isinstance(date_to, str):，以下簡稱 P3
    - A: date_to != None
    - B: isinstance(date_to, str)
    - P3: A && !B
    - PC:
        - T t f
            - search_record(1, '20240101', 20240103)
            - Expected: error_message = 'invalid date_to parameter'
        - F f t
            - search_record(1, '20240101', '20240103')
            - mock 資料庫使 fetchone() 回傳 User 資料為非 None，且 Record 資料有 3 筆，且當中有 3 筆符合條件
            - Expected: success = True, len(records) = 3
    - CC:
        - F t t
            - search_record(1, '20240101', '20240103')
            - mock 資料庫使 fetchone() 回傳 User 資料為非 None，且 Record 資料有 3 筆
            - Expected: success = True, len(records) = 3
        - F f f
            - search_record(1, '20240101', None)
            - mock 資料庫使 fetchone() 回傳 User 資料為非 None，且 Record 資料有 3 筆，但僅有 1 筆符合條件
            - Expected: success = True, len(records) = 1
    - CACC:
        - A as major
            - T t f 
            - F f f (pick this)
        - B as major
            - T t f
            - F t t (pick this)
        - F f f ( A as Major )
            - search_record(1, '20240101', None)
            - mock 資料庫使 fetchone() 回傳 User 資料為非 None，且 Record 資料有 3 筆，但僅有 1 筆符合條件
            - Expected: success = True, len(records) = 1
        - F t t ( B as Major )
            - search_record(1, '20240101', '20240103')
            - mock 資料庫使 fetchone() 回傳 User 資料為非 None，且 Record 資料有 3 筆
            - Expected: success = True, len(records) = 3
- if row == None:，以下簡稱 P4
    - A: row == None
    - P4: A
    - 因此 predicate 只有一個 clause，故此處 CC = PC = CACC
    - 測試資料設計如下
        - T t
            - search_record(2, '20240101', '20240103')
            - mock 資料庫使 fetchone() 回傳 User 資料為 None
            - Expected: error_message = 'user_id does not exist'
        - F f
            - search_record(1, '20240101', '20240103')
            - mock 資料庫使 fetchone() 回傳 User 資料為非 None，且 Record 資料有 3 筆
            - Expected: success = True, len(records) = 3

- if date_to == None:，以下簡稱 P5
    - A: date_to == None
    - P5: A
    - 因此 predicate 只有一個 clause，故此處 CC = PC = CACC
    - 測試資料設計如下
        - T t
            - search_record(1, '20240101', None)
            - mock 資料庫使 fetchone() 回傳 User 資料為非 None，且 Record 資料有 3 筆，且當中有 1 筆符合條件
            - Expected: success = True, len(records) = 1
        - F f
            - search_record(1, '20240101', '20240103')
            - mock 資料庫使 fetchone() 回傳 User 資料為非 None，且 Record 資料有 3 筆，且當中有 3 筆符合條件
            - Expected: success = True, len(records) = 3
