import re
from data import DatabaseAccess
from collections import Counter

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
        
    def __repr__(self):
        return '<"{}" : "{}">'.format(self.token, self.kind)
    
    def __str__(self):
        return repr(self)
    
    def __eq__(self, other):
        return self.token == other.token and self.kind == other.kind
    
    def __hash__(self):
        return hash((self.token, self.kind))

# parse through "text" column
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

# parse through "tokens" column   
class HolstepTokenizer:
    
    def __init__(self):
        pass
    
    def get_token_kind(self, token):
        if token[0] == 'c':
            if token[1].isalpha():
                return 'FUN'
            else:
                return 'OPR'
        else:
            if token[0].isalpha():
                return 'VAR'
            else:
                return 'SYM'
    
    def parse(self, tokens):
        
        return [HolstepToken(t, self.get_token_kind(t)) for t in tokens]

class HolstepTreeNode:
    
    def __init__(self, token):
        self.settoken(token)
        self.children = []
        self.unique_tokens = Counter()
        self.unique_branching = Counter()
        
    def settoken(self, token):
        self.token = token
        self.value = token.token
        
    def consumefirstchild(self):
        first = self.children[0]
        tail = self.children[1:]
        self.settoken(first.token)
        self.children = first.children + tail
        
    def printtree(self, indent=0):
        print(('   ' * indent) + self.value)
        for c in self.children:
            c.printtree(indent=indent+1)
            
    def to_list(self):
        result = []
        result.append(self.value)
        for c in self.children:
            result += c.to_list()
        return result
            
    def build_unique_info(self):
        for c in self.children:
            c.build_unique_info()
            self.unique_tokens.update(c.unique_tokens)
            self.unique_branching.update(c.unique_branching)
        self.unique_tokens.update([self.token])
        self.unique_branching.update([len(self.children)])
        
    def has_FILL(self):
        for c in self.children:
            if (c.has_FILL()):
                return True
        return self.value == 'FILL'
    
    def node_count(self, is_inner=False):
        count = 0 if is_inner else 1
        for c in self.children:
            count += 1 + c.node_count(is_inner=True)
        return count
            
    def __repr__(self):
        return '[{}, {}]'.format(self.value, len(self.children))
    
    def __str__(self):
        return repr(self)
    
class QuickHolstepSeqParser:
    
    def __init__(self):
        pass
    
    def parse(self, tokens):
        tokensspl = tokens.split(' ')
        tokens = []
        for token in tokensspl:
            token = token.lstrip('(').rstrip(')')
            if len(token) >= 2 and token[1].isalpha() and not token[0].isalpha():
                tokens.append(token[0])
                tokens.append(token[1])
                token = token[2:]
                if token != '':
                    tokens.append(token)
            else:
                tokens.append(token)
        return tokens
    
class HolstepTreeParser:
    
    def __init__(self):
        self.varlist = []
        self.varfunclist = []
        self.stack = []
        self.latest_source = None
        self.prevtoken = None
        
    def parse(self, tokens):
        self.latest_source = tokens
        tokens = tokens.split(' ')
        self.varlist = []
        self.varfunclist = []
        
        root = HolstepTreeNode(HolstepToken('ROOT', 'ROOT'))
        self.stack = [root]
        
        for token in tokens:
            if token == '|-':
                self._handle_fun('|-')
            elif token[0] == '(':
                self._handle_beginning_paren(token)
            elif self.is_word(token):
                self._handle_word(token)
            else:
                self._handle_operation(token)
            self.prevtoken = token
        return root

    def _handle_beginning_paren(self, token):
        # multiple '((((('
        while token[0] == '(':
            node = HolstepTreeNode(HolstepToken('FILL', 'FILL'))
            self.stack[-1].children.append(node)
            self.stack.append(node)
            token = token[1:]
        if self.is_word(token):
            # funcs or constants or vars
            self._handle_word(token)
        else:
            if len(token) > 1 and token[1].isalpha():
                # quantifiers
                if len(token) == 2:
                    print(self.latest_source)
                    raise Exception(token)
                self._handle_quantifier(token)
            else:
                # symbol func like '~'
                self._handle_fun(token)
                
    def _handle_quantifier(self, token):
        qnt = token[0]
        token = token[1:]
        self._handle_fun(qnt, kind='QNT')
        
        var = None
        syms = None
        if token[1].isalpha():
            var = token[:2]
            syms = token[2:]
        else:
            var = token[0]
            syms = token[1:]
        self._handle_var(var, syms=syms)
        
    def _handle_word(self, token):
        token, parens = self.split_end_parens(token)
        #self._handle_higher_order_fun(token)
        if self.prevtoken is not None and self.prevtoken.lstrip('(') in self.varfunclist:
            # predicate on var
            self.stack[-1].consumefirstchild()
        if token in self.varlist:
            # var
            self._handle_var(token)
        elif token in self.varfunclist:
            # predicate
            self._handle_var(token)
            #self._handle_fun(token, kind='VFN')
        elif token[0] == '_' or token in ['T', 'F']:
            # constant ex: '_0' or 'T'
            self._handle_value(token)
        elif token == 'o':
            self._handle_operation(token)
        else:
            if len(token) == 1:
                # assume var
                self._handle_var(token)
            else:
                # function
                self._handle_fun(token)
        if parens is not None:
            for i in range(len(parens)):
                if self.stack[-1].value == 'FILL':
                    self.stack[-1].consumefirstchild()
                self.stack.pop()
                
    def _handle_operation(self, token):
        self._handle_fun(token, kind='OPR')
            
    def _handle_fun(self, token, kind='FUN'):
        self.stack[-1].settoken(HolstepToken(token, kind))
        
    def _handle_var(self, var, syms=None):
        varnode = None
        if var.islower():
            if var not in self.varlist:
                self.varlist.append(var)
            varnode = HolstepTreeNode(HolstepToken(var, 'VAR'))
        else:
            if var not in self.varfunclist:
                self.varfunclist.append(var)
            varnode = HolstepTreeNode(HolstepToken(var, 'VFN'))
        
        qnt = self.stack[-1]
        if qnt.value == 'o':
            qnt.children[0].children.append(varnode)
        else:
            qnt.children.append(varnode)
        
        if syms is not None:
            symsnode = HolstepTreeNode(HolstepToken(syms, 'DOT'))
            varnode.children.append(symsnode)
  
    def _handle_value(self, token):
        node = HolstepTreeNode(HolstepToken(token, 'VAL'))
        self.stack[-1].children.append(node)
        
    def _handle_higher_order_fun(self, token):
        if self.stack[-1].token.kind == 'FILL' and self.prevtoken[-1] == ')':
            self._consume_child(self.stack[-1])
        
    def is_word(self, token):
        return token[0].isalpha() or token[0] == '_'
    
    def split_end_parens(self, token):
        i = token.find(')')
        if i == -1:
            return (token, None)
        else:
            return (token[:i], token[i:])
