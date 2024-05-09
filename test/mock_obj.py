class mock_db_conn:
    def __init__(self):
        self.Cursor = self.Cursor()
    class Cursor:
        def __init__(self):
            pass
        def execute(self, *args):
            pass
        def fetchone(self):
            pass
            
    def cursor(self):
        return self.Cursor
    def commit(self):
        pass
    def rollback(self):
        pass
    def close(self):
        pass