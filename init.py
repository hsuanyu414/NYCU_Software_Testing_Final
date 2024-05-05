import sqlite3


def init_db(db_name='db.sqlite3'):

    """
    Initialize database with tables
    
    user 
    - user_id (primary key) autoincrement
    - line_id (unique)
    - create_date

    record
    - user_id (foreign key)
    - record_id (primary key) autoincrement
    - date
    - item
    - cost
    - category
    - comment
    - create_date
    """

    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute('''
    CREATE TABLE user (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        line_id TEXT UNIQUE,
        create_date DATE DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    c.execute('''
    CREATE TABLE record (
        user_id INTEGER,
        record_id INTEGER PRIMARY KEY AUTOINCREMENT,
        date DATE DEFAULT CURRENT_TIMESTAMP,
        item TEXT,
        cost INTEGER,
        category TEXT,
        comment TEXT,
        create_date DATE DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES user(user_id)
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
