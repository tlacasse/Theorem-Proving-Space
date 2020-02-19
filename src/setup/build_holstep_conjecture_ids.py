import sys
import numpy as np

sys.path.append('..')
from holstep import Holstep

def main():
    with Holstep.Setup() as db:
        sql = 'SELECT Id FROM Conjecture ORDER BY Id'
        ids = db.ex_many(sql)
        ids = [a[0] for a in ids]
        
        ids = np.array(ids)
        np.save('../../data/conjecture_ids.npy', ids)
        print(ids)
        print(ids.shape)

main()
