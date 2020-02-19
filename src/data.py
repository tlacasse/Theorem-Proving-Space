import sqlite3
import math
import pickle
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
        return self.ex_single(query)
    
    def execute_many(self, query):
        print(query)
        return self.ex_many(query)
    
    # no printing
    
    def ex_many(self, query):
        return list(self.cursor.execute(query))
    
    def ex_single(self, query):
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        if result is None:
            raise DatabaseError(query)
        return result

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
    
def dump_data(filename, obj):
    with open(filename, 'wb') as file:
        pickle.dump(obj, file)

def load_data(filename):
    with open(filename, 'rb') as file:
        return pickle.load(file)
