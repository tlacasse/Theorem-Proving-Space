import sys
import numpy as np

sys.path.append('..')
from holstep import Holstep
from data import load_data

def main():
    id_to_step = np.load('../../data/reducedsteps_id_to_step.npy')
    step_to_id = load_data('../../data/reducedsteps_step_to_id.data')
    conjectures = np.load('../../data/conjecture_ids.npy')
    
    positions = np.zeros((len(conjectures), len(id_to_step)), dtype=int)
    with Holstep.Setup() as db:
        for i, cid in enumerate(conjectures):
            print(cid)
            sql = 'SELECT StepId, IsUseful FROM ConjectureStep '
            sql += 'WHERE ConjectureId = {}'.format(cid)
            steps = db.ex_many(sql)
            
            for sid, is_useful in steps:
                if (sid in step_to_id):
                    positions[i][step_to_id[sid]] = (1 if is_useful == 1 else -1)

    positions = np.array(positions)
    np.save('../../data/conjecture_step_coords.npy', positions)
    print(positions)
    print(positions.shape)

main()
