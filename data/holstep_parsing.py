import os
import sqlite3

class LineType:
    
    def __init__(self, table):
        self.table = table
        
    def __eq__(self, other):
        return self.table == other.table
    
LineTypeCONJECTURE = LineType('Conjecture')
LineTypeDEPENDENCY = LineType('Dependency')
LineTypeSTEP = LineType('Step')

"""
N <name of conjecture>
C <text representation of the conjecture>
T <tokenization of the conjecture>

D <name of dependency>
A <text representation of the dependency>
T <tokenization of the conjecture>

+ <text representation of the intermediate step>
T <tokenization of the intermediate step>
"""
class LineReader:
    
    def __init__(self, db, cid, is_train):
        self.db = db
        self.cid = cid if is_train else (cid + 10000)
        self.is_train = is_train
        self.linetype = LineTypeCONJECTURE
        self.name = ''
        self.text = ''
        self.tokens = ''
        self.is_useful = False
        
    def read(self, line):
        key = line[0]
        line = line[2:]
        if key == 'N':
            self.name = line
        elif key == 'D':
            self.name = line
            self.linetype = LineTypeDEPENDENCY
        elif key == 'C' or key == 'A':
            self.text = line
        elif key == '+' or key == '-':
            self.text = line
            self.is_useful = (key == '+')
            self.linetype = LineTypeSTEP
        elif key == 'T':
            self.tokens = line
            self._update_db()
        else:
            raise Exception('Unknown line code')
            
    def _update_db(self):
        sql = 'error'
        if self.linetype == LineTypeCONJECTURE:
            sql = ('INSERT INTO {} (Id, IsTraining, Name, Text, Tokens)'.format(self.linetype.table) 
                    + " VALUES ({}, {}, '{}', '{}', '{}')".format(
                            self.cid, 
                            self._as_boolean(self.is_train), 
                            self._as_str(self.name), 
                            self._as_str(self.text), 
                            self._as_str(self.tokens)))
        elif self.linetype == LineTypeDEPENDENCY:
            sql = ('INSERT INTO {} (ConjectureId, Name, Text, Tokens)'.format(self.linetype.table)
                    + " VALUES ({}, '{}', '{}', '{}')".format(
                            self.cid, 
                            self._as_str(self.name), 
                            self._as_str(self.text), 
                            self._as_str(self.tokens)))
        elif self.linetype == LineTypeSTEP:
            sql = ('INSERT INTO {} (ConjectureId, IsUseful, Text, Tokens)'.format(self.linetype.table)
                    + " VALUES ({}, {}, '{}', '{}')".format(
                            self.cid, 
                            self._as_boolean(self.is_useful), 
                            self._as_str(self.text), 
                            self._as_str(self.tokens)))
        else:
            raise Exception('Unknown line type')
        self.db.execute(sql)
        self.db.commit()
        
    def _as_boolean(self, boolean):
        return '1' if boolean else '0'
    
    def _as_str(self, text):
        # escape
        return text.replace("'", "''").strip()

def read_folder(name, is_train):
    db = sqlite3.connect('holstep.db')
    try:
        for p in os.listdir('../holstep/' + name):
            cid = p
            print(cid)
            p = os.path.join('..', 'holstep', name, p)
            with open(p, 'r') as file:
                reader = LineReader(db, int(cid), is_train)
                for line in file:
                    reader.read(line)
    finally:    
        db.close()
        
read_folder('test', False)
read_folder('train', True)
   