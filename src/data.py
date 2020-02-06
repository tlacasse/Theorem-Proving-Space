import sqlite3
import math
from sqlite3 import DatabaseError

class DatabaseAccess:
    
    def __init__(self, path):
        self.path = path
        self.db = None
        self.cursor = None
    
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

class HolStep(DatabaseAccess):
    
    def __init__(self, path='data/holstep.db'):
        super().__init__(path)
        self.TEST_ID_START = 10000
    
    def get_conjecture(self, i, train=True):
        if not train:
            i += self.TEST_ID_START
        return self.execute_single('SELECT * FROM Conjecture WHERE Id={}'.format(i))

    @staticmethod
    def build_search_conjecture(query, order_by):
        query = query.replace("'", '').replace('\\', '').strip()
        queries = query.split(' ')
        queries = map(lambda s: "Name LIKE '%{}%'".format(s), queries)
        queries = ' AND '.join(queries)
        if (len(queries) > 0):
            queries = ' WHERE ' + queries
        queries += ' ORDER BY IsTraining DESC, ' + order_by
        return 'SELECT Id, IsTraining, Name FROM Conjecture' + queries
    
class MLL(DatabaseAccess):
    
    def __init__(self, path='data/mll.db'):
        super().__init__(path)
    
    @staticmethod
    def build_search_conjecture(query):
        select = 'SELECT A.Name, T.Id, T.Type, T.Statement '
        select += 'FROM Theorem AS T '
        select += 'INNER JOIN Article AS A '
        select += 'ON T.ArticleId = A.Id '
        select += 'WHERE HasProof = 1 '
        select += "AND Statement != '' "
        select += 'AND '
        
        query = query.replace("'", '').replace('\\', '').strip()
        queries = query.split(' ')
        queries = map(lambda s: "T.Statement LIKE '%{}%'".format(s), queries)
        queries = ' AND '.join(queries)
        queries += ' ORDER BY T.Id'

        return select + queries
    
class PageResults:
    
    def __init__(self, count_per_page):
        self.count_per_page = count_per_page
        self.results = []
        self.pages = 1
        
    def update_search(self, results):
        self.results = results
        self.pages = math.ceil(len(results) / self.count_per_page)
        
    def fetch_page(self, page):
        size = self.count_per_page
        return self.results[size * page : size * (page + 1)]
