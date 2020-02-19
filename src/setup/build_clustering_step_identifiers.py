import sys
import numpy as np

sys.path.append('..')
from holstep import Holstep
from data import dump_data

# steps need to be used at least this many times
LOWER_BOUND = 20

def main():
    with Holstep.Setup() as db:
        sql = 'SELECT StepId FROM ConjectureStep '
        sql += 'GROUP BY StepId HAVING COUNT(StepId) >= {} '.format(LOWER_BOUND)
        sql += 'ORDER BY StepId'
        steps = db.ex_many(sql)
        steps = [a[0] for a in steps]
        
        id_to_step = np.array(steps)
        np.save('../../data/reducedsteps_id_to_step.npy', id_to_step)
        print(id_to_step)
        
        step_to_id = {}
        for i, x in enumerate(steps):
            step_to_id[x] = i
        dump_data('../../data/reducedsteps_step_to_id.data', step_to_id)
        print(step_to_id)

main()
