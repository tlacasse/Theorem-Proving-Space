import sqlite3

db = sqlite3.connect('holstep.db')
try:
    i = 0
    for s in db.execute('SELECT DISTINCT Text FROM Step'):
        i += 1
        sql = "INSERT INTO StepKey (Id, Text) VALUES ({}, '{}')"
        db.update(sql.format(i, s[0].replace("'", "''")))
    db.commit()
finally:
    db.close()
