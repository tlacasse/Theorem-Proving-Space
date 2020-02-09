import os
import sqlite3

def main():
    db = sqlite3.connect('mll.db')
    try:
        stuff = Stuff(db)
        for p in os.listdir('../mmlfull'):
            fname = p
            print(fname)
            if fname == 'lopban_7.miz':
                # this one causes problems because no ending 'end;'
                continue
            
            stuff.ARTICLE_ID += 1
            sql = ("INSERT INTO Article (Id, Name) VALUES ({}, '{}')"
                   .format(stuff.ARTICLE_ID, fname[:-4]))
            db.execute(sql)
            p = os.path.join('..', 'mmlfull', fname)
            with open(p, 'r') as file:
                read_file(fname, file.readlines(), stuff)
        db.commit()
    finally:    
        db.close() 

class Stuff:
    
    def __init__(self, db):
        self.db = db
        self.ARTICLE_ID = 0
        self.THEOREM_ID = 0
        self.STEP_ID = 0
        
    def execute(self, sql):
        self.db.execute(sql)
        
    def save_step(self, store, is_proof_step):
        self.STEP_ID += 1
        sql = ('INSERT INTO Step (Id, TheoremId, Text, IsProofStep)'
                + " VALUES ({}, {}, '{}', {})".format(
                        self.STEP_ID,
                        self.THEOREM_ID, 
                        escape(store),
                        as_boolean(is_proof_step)))
        self.execute(sql)
        
def escape(text):
    return text.replace("'", "''")

def as_boolean(boolean):
    return '1' if boolean else '0'

class Reader:
    
    def __init__(self, item, header, stuff):
        self.item = item
        self.header = header.strip()
        self.stuff = stuff
        self.store = ''
        self.done = False

        self.stuff.THEOREM_ID += 1
        sql = ('INSERT INTO Theorem (Id, ArticleId, Type, Header, HasProof)'
                + " VALUES ({}, {}, '{}', '{}', {})".format(
                        self.stuff.THEOREM_ID, 
                        self.stuff.ARTICLE_ID, 
                        escape(item), 
                        escape(header),
                        as_boolean(False)))
        self.stuff.execute(sql)
    
    def read(self, line):
        pass
    
    def save_store(self):
        if self.store != '':
            self.stuff.save_step(self.store, False)
            self.store = ''
    
    def result(self):
        return None if self.done else self
    
class BasicReader(Reader):
    
    def __init__(self, item, header, stuff):
        super().__init__(item, header, stuff)
    
    def read(self, line):
        if line.startswith('begin'):
            self.done = True
        else:
            self.store = line
            self.save_store()
    
class SingleReader(Reader):
    
    def __init__(self, item, header, stuff):
        super().__init__(item, header, stuff)
        self.done = self.header[-1] == ';'
    
    def read(self, line):
        self.store = line
        if self.store != '' and self.store[-1] == ';':
            self.done = True
        self.save_store()
    
class TheoremReader(Reader):
    
    def __init__(self, item, header, stuff):
        super().__init__(item, header, stuff)
        self.in_proof = False
        self.prev = ''
        self.statement = ''
    
    def read(self, line):
        if line == '' and self.prev == 'end;':
            self.done = True
        else:
            if line.strip() == 'proof' and not self.in_proof:
                self.save_store()
                self.in_proof = True  
                self.store = line
                self.save_store()
                self._update_theorem()
            else:
                self.store = line
                if (self.statement != ''):
                    self.statement += ' '
                self.statement += line.strip()
                self.save_store()
        self.prev = line
        
    def save_store(self):
        if self.store != '':
            self.stuff.save_step(self.store, self.in_proof)
            self.store = ''
            
    def _update_theorem(self):
        self.stuff.db.commit()
        sql = 'UPDATE Theorem '
        sql += "SET HasProof={}, Statement='{}' "
        sql += 'WHERE Id={}'
        sql = sql.format(as_boolean(True), escape(self.statement), self.stuff.THEOREM_ID)
        self.stuff.execute(sql)

thm_starts = ['registration',
              'definition', 
              'theorem',
              'scheme', 
              'notation',
              'defpred',
              'Lm',
              'Lem',
              'LM',
              'Lem', 
              'lm',
              'Thm',
              'Th',
              'th',
              'reserve',
              'deffunc',
              'func',
              'for',
              'reconsider',
              'INV',
              'LAST',
              # nothing else matches
              '1 < tau']

def get_theorem_start(line):
    for s in thm_starts:
        if (line.strip().startswith(s)):
            return s
    return None

def get_labeled_start(line):
    letters = 0
    while letters < len(line) and line[letters].isalpha():
        letters += 1
    digits = 0
    while letters + digits < len(line) and line[letters + digits].isdigit():
        digits += 1
    letters2 = 0
    while letters + digits + letters2 < len(line) and line[letters + digits + letters2].isalpha():
        letters2 += 1
    if letters > 0:
        if letters + digits + letters2 < len(line):
            if line[letters + digits + letters2] == ':':
                return line[:letters] + ':'
    return None

def read_file(fname, lines, stuff):
    reader = None
    for line in lines:
        line = line.rstrip() # want indents still
        if reader is None:
            if line.strip() == '':
                continue
            if line.strip().startswith('::'):
                # comments at top
                continue
            theorem_start = get_theorem_start(line)
            labeled_start = get_labeled_start(line)
            if line.startswith('environ'):
                reader = BasicReader('environ', line, stuff)
                
            elif theorem_start is not None:
                reader = TheoremReader(theorem_start, line, stuff)
                
            elif labeled_start is not None:
                reader = TheoremReader(labeled_start, line, stuff)
                
            elif line.strip().startswith('set'):
                reader = SingleReader('set', line, stuff)
            elif line.strip().startswith('ex'):
                reader = SingleReader('ex', line, stuff)
            elif line.strip().startswith('v0'):
                reader = SingleReader('v0', line, stuff)  
            elif line.strip().startswith('((('):
                reader = SingleReader('(((', line, stuff)
            elif line.endswith(';') and not line.startswith('  '):
                reader = SingleReader(';', line, stuff)

            elif line.startswith('begin'):
                continue
            elif line.startswith('then'):
                # i don't know what else to do here
                continue
            elif line.startswith('consider'):
                # i don't know what else to do here
                continue
            else:
                raise Exception('{} - "{}"'.format(fname, line))
        else:
            reader.read(line)
        if reader is not None:
            reader = reader.result()

main()
