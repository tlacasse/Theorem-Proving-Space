import re
from data import DatabaseAccess

class Holstep(DatabaseAccess):
    
    def __init__(self, path='data/holstep.db'):
        super().__init__(path)
        self.TEST_ID_START = 10000
        
    @classmethod
    def Setup(cls):
        return cls(path='../../data/holstep.db')
    
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
    
    def list_conjectures(self):
        return self.execute_many('SELECT Id, IsTraining, Name FROM Conjecture')
    
    def list_conjecture_ids(self):
        return [x[0] for x in self.execute_many('SELECT Id FROM Conjecture')]

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
        tokenized.append(HolstepToken(token, self.get_kind(token)))
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
