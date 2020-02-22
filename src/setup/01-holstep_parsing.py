import os
import sqlite3

def main():
    counters = Counters()       
    read_folder('test', False, counters)
    read_folder('train', True, counters)
    
def read_folder(name, is_train, counters):
    db = sqlite3.connect('../../data/holstep.db')
    
    try:
        for p in os.listdir('../../holstep/' + name):
            cid = p
            print(cid)
            p = os.path.join('..', '..', 'holstep', name, p)
            with open(p, 'r') as file:
                reader = LineReader(db, int(cid), is_train, counters)
                for line in file:
                    reader.read(line)
    finally:    
        db.close()

class LineType:
    
    def __init__(self, table):
        self.table = table
        
    def __eq__(self, other):
        return self.table == other.table
    
LineTypeCONJECTURE = LineType('Conjecture')
LineTypeDEPENDENCY = LineType('Dependency')
LineTypeSTEP = LineType('Step')

class Counters:
    
    def __init__(self):
        self.DEPENDENCY_ID = 0
        self.STEP_ID = 0

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
    
    def __init__(self, db, cid, is_train, counters):
        self.db = db
        self.cid = cid if is_train else (cid + 10000)
        self.is_train = is_train
        self.counters = counters
        self.linetype = LineTypeCONJECTURE
        self.name = ''
        self.text = ''
        self.tokens = ''
        self.is_useful = False
        self.cursor = self.db.cursor()
        
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
            sql = self._update_db_dependency()
        elif self.linetype == LineTypeSTEP:
            sql = self._update_db_step()
        else:
            raise Exception('Unknown line type')
        self.db.execute(sql)
        self.db.commit()
        
    def _update_db_dependency(self):
        id_to_use = None
        self.cursor.execute("SELECT Id FROM Dependency WHERE Name = '{}'".format(self._as_str(self.name)))
        c = self.cursor.fetchone()
        if (c is None):
            self.counters.DEPENDENCY_ID += 1
            id_to_use = self.counters.DEPENDENCY_ID
            sql = 'INSERT INTO Dependency (Id, Name, Text, Tokens) ' 
            sql += "VALUES ({}, '{}', '{}', '{}')".format(
                    id_to_use, 
                    self._as_str(self.name), 
                    self._as_str(self.text), 
                    self._as_str(self.tokens))
            self.db.execute(sql)
        else:
            id_to_use = c[0]
        sql = 'INSERT INTO ConjectureDependency (ConjectureId, DependencyId) '
        sql += "VALUES ({}, {})".format(self.cid, id_to_use)
        return sql
        
    def _update_db_step(self):
        id_to_use = None
        self.cursor.execute("SELECT Id FROM Step WHERE Text = '{}'".format(self._as_str(self.text)))
        c = self.cursor.fetchone()
        if (c is None):
            self.counters.STEP_ID += 1
            id_to_use = self.counters.STEP_ID
            sql = 'INSERT INTO Step (Id, Text, Tokens) '
            sql += "VALUES ({}, '{}', '{}')".format(
                    id_to_use, 
                    self._as_str(self.text), 
                    self._as_str(self.tokens))
            self.db.execute(sql)
        else:
            id_to_use = c[0]
        sql = 'INSERT INTO ConjectureStep (ConjectureId, StepId, IsUseful) '
        sql += "VALUES ({}, {}, {})".format(
                self.cid, 
                id_to_use,
                self._as_boolean(self.is_useful))
        return sql
        
    def _as_boolean(self, boolean):
        return '1' if boolean else '0'
    
    def _as_str(self, text):
        # escape
        return text.replace("'", "''").strip()

main()
