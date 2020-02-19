import sqlite3
import numpy as np

def main():
    maxval = 0
    count = 11410 + 2
    db = sqlite3.connect('holstep.db')
    cursor = db.cursor()
    array = np.zeros((count, count), 5000, dtype='uint16')
    try:
        ids = [r[0] for r in cursor.execute('SELECT Id FROM Conjecture')]
        for a in ids:
            print(a)
            for b in ids:
                result = dist(array, a, b, cursor)
                if (result > maxval):
                    maxval = result
    finally:    
        db.close()
        np.save('cmetric_counts.npy', array)
    print('maxval: ' + str(maxval)) # => 2616

def dist(array, a, b, cursor):
    if (a > b):
        a, b = b, a
    if (array[a][b] == 5000):
        a_steps = get_steps(a, cursor)
        b_steps = get_steps(b, cursor)
        array[a][b] = len(a_steps & b_steps)
        return array[a][b]
    return 0

def get_steps(i, cursor):
    sql = 'SELECT CASE WHEN IsUseful = 1 THEN StepId ELSE -1 * StepId END AS Value '
    sql += 'FROM ConjectureStep WHERE ConjectureId = {}'.format(i)
    return set([x[0] for x in cursor.execute(sql)])

main()
