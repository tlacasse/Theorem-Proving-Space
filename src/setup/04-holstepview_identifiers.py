import sys
import numpy as np

sys.path.append('..')
from holstep import Holstep
from data import dump_data

from setup_vars import HOLSTEP_STEPUSAGE_LOWER_BOUND

def main():
    with Holstep.Setup() as db:
        sql = 'SELECT StepId FROM ConjectureStep '
        sql += 'GROUP BY StepId HAVING COUNT(StepId) >= {} '.format(HOLSTEP_STEPUSAGE_LOWER_BOUND)
        sql += 'ORDER BY StepId'
        steps = db.ex_many(sql)
        steps = [a[0] for a in steps]
        
        id_to_step = np.array(steps)
        np.save('../../data/holstepview_id_to_step.npy', id_to_step)
        print(id_to_step)
        
        step_to_id = {}
        for i, x in enumerate(steps):
            step_to_id[x] = i
        dump_data('../../data/holstepview_step_to_id.data', step_to_id)
        print(step_to_id)

main()
