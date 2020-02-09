import sqlite3
import math
import re
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

class Holstep(DatabaseAccess):
    
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
    
class Mizar(DatabaseAccess):
    
    def __init__(self, path='data/mizar.db'):
        super().__init__(path)
    
    def get_theorem_and_proof(self, i):
        sql = 'SELECT 0 AS Id, Header AS Text, 0 AS IsProofStep '
        sql += 'FROM Theorem WHERE Id = {0} UNION ALL '
        sql += 'SELECT Id, Text, IsProofStep '
        sql += 'FROM Step WHERE TheoremId = {0} ORDER BY Id'
        proof = self.execute_many(sql.format(i))
        sql = 'SELECT A.Name, T.Id, T.Type '
        sql += 'FROM Theorem AS T INNER JOIN Article AS A '
        sql += 'ON T.ArticleId = A.Id '
        sql += 'WHERE T.Id = {}'
        theorem = self.execute_single(sql.format(i))
        return theorem, proof

    @staticmethod
    def build_search_theorem(query):
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

class HolstepToken:
    
    def __init__(self, token, kind):
        self.token = token
        self.kind = kind
  
class HolstepParser:
    
    def __init__(self):
        pass
    
    def get_char_kind(self, char):
        if re.search(r'[a-z0-9_]', char, re.IGNORECASE):
            return 'VAR'
        if re.search(r'[\s]', char, re.IGNORECASE):
            return 'SPC'
        if re.search(r'[\(\)]', char, re.IGNORECASE):
            return 'PAR'
        return 'SYM'
    
    def get_kind(self, token):
        kind = self.get_char_kind(token[0])
        if kind == 'VAR' and len(token) > 2:
            return 'FUN'
        return kind
    
    def parse(self, code):
        tokenized = []
        prevkind = ''
        token = ''
        for char in code:
            kind = self.get_char_kind(char)
            if kind != prevkind or char == '(' or char == ')':
                if token != '':
                    tokenized.append(HolstepToken(token, self.get_kind(token)))
                token = ''
            token += char
            prevkind = kind
        return tokenized
    
    def prettyprint(self, code):
        tokens = self.parse(code)
        result = []
        indent = 0
        
        def size_of_next_parenth_block(i):
            i += 1
            count = 0;
            while tokens[i].token != ')':
                if tokens[i].token == '(':
                    return 1000
                if tokens[i].kind != 'SPC':
                    count += 1
                i += 1
            return count
        
        def add_new_line():
            result.append(HolstepToken('<br>', 'BRK'))
            for j in range(indent):
                result.append(HolstepToken('  ', 'SPC'))
        
        i = 0
        while i < len(tokens):
            on = tokens[i]
            def add_to_result():
                result.append(tokens[i])
            if on.kind == 'PAR':
                if on.token == '(':
                    if (size_of_next_parenth_block(i) <= 3):
                        while tokens[i].token != ')':
                            add_to_result()
                            i += 1
                        add_to_result()
                    else:
                        add_to_result()
                        indent += 1
                        add_new_line()
                elif on.token == ')':
                    indent -= 1
                    add_new_line()
                    add_to_result()
                else:
                    add_to_result()
            else:
                add_to_result()
            i += 1
            
        return [(t.token, t.kind) for t in result]
  
class MizarToken(HolstepToken):
    
    def __init__(self, token, kind, is_proof_step):
        super().__init__(token, kind)
        self.is_proof_step = is_proof_step 
    
class MizarParser:
    
    def __init__(self):
        self.keywords = ['theorem', 'registration', 'assume', 'then', 'hereby', 
                         'reconsider', 'thus', 'let', 'end', 'such', 'that', 
                         'given', 'hence', 'thesis', 'by', 'now', 'proof',
                         'definition', 'st', 'uniqueness', 'iff', 'from',
                         'take', 'holds', 'defpred', 'consider', 'existence',
                         'coherence', 'reserve', 'func', 'contradiction', 'case',
                         'cases', 'per', 'scheme', 'suppose']
    
    def get_char_kind(self, char):
        if re.search(r'[a-z0-9_:\-]', char, re.IGNORECASE):
            return 'VAR'
        if re.search(r'[\s]', char, re.IGNORECASE):
            return 'SPC'
        if re.search(r'[\(\)]', char, re.IGNORECASE):
            return 'PAR'
        return 'SYM'
    
    def get_kind(self, token):
        kind = self.get_char_kind(token[0])
        if kind == 'VAR':
            if  token in self.keywords:
                return 'KEY'
            if token.find(':') >= 0:
                return 'LAB'
            if token[0].isupper():
                if re.sub(r'[A-Za-z]', '', token[1:]).isdigit():
                    return 'LAB'
            if token.replace('-', '') == '':
                return 'SYM'
            if len(token) > 1:
                return 'FUN'
        return kind
    
    def parse(self, code_lines):
        tokenized = []
        prevkind = ''
        token = ''
        for line in code_lines:
            is_proof = line[2] == 1
            line = line[1]
            
            def save_token(t):
                if t != '':
                    tokenized.append(MizarToken(t, self.get_kind(t), is_proof))
                    
            for char in line:
                kind = self.get_char_kind(char)
                if kind != prevkind:
                    save_token(token)
                    token = ''
                token += char
                prevkind = kind
            save_token(token)
            token = ''
            tokenized.append(MizarToken('<br>', 'BRK', is_proof))
        return [(t.token, t.kind, t.is_proof_step) for t in tokenized]
