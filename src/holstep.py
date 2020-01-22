import sqlite3
from sqlite3 import DatabaseError

class HolStep:
    
    def __init__(self, path='data/holstep.db'):
        self.path = path
        self.db = None
        self.cursor = None
        self.TEST_ID_START = 10000
    
    def __enter__(self):
        self.db = sqlite3.connect(self.path)
        self.cursor = self.db.cursor()
        return self
        
    def __exit__(self, exception_type, exception_value, traceback):
        self.cursor = None
        self.db.close()
        self.db = None
        
    def execute_single(self, query):
        print(query)
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        if result is None:
            raise DatabaseError(query)
        return result
    
    def execute_many(self, query):
        print(query)
        return list(self.cursor.execute(query))
    
    def get_conjecture(self, i, train=True):
        if not train:
            i += self.TEST_ID_START
        return self.execute_single('SELECT * FROM Conjecture WHERE Id={}'.format(i))

def build_search_conjecture(query):
    query = query.replace("'", '').replace('\\', '').strip()
    queries = query.split(' ')
    queries = map(lambda s: "Name LIKE '%{}%'".format(s), queries)
    queries = ' OR '.join(queries)
    if (len(queries) > 0):
        queries = ' WHERE ' + queries
    return 'SELECT Id, IsTraining, Name FROM Conjecture' + queries
