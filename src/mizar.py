import re
from data import DatabaseAccess
  
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

class MizarToken():
    
    def __init__(self, token, kind, is_proof_step):
        self.token = token
        self.kind = kind
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
