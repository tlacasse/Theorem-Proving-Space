import sqlite3

class _Holder:
    
    def __init__(self, path='data/holstep.db'):
        self.db = None
        self.path = path
        
    def connect(self):
        self.db = sqlite3.connect(self.path)
        return self.db.cursor()
        
    def close(self):
        self.db.close()
        self.db = None
        
    def execute_single(self, query):
        try:
            c = self.connect()
            c.execute(query)
            return c.fetchone()
        finally:
            self.close()
            
    def execute_many(self, query):
        try:
            c = self.connect()
            return list(c.execute(query))
        finally:
            self.close()
        
_DB = _Holder()

class HolStep:
    
    def __init__(self):
        self.TEST_ID_START = 10000
    
    def get_conjecture(self, i, train=True):
        if not train:
            i += self.TEST_ID_START
        return _DB.execute_single('SELECT * FROM Conjecture WHERE Id={}'.format(i))
    