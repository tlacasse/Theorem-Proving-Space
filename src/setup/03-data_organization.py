import sys
import numpy as np
from sklearn.manifold import TSNE

sys.path.append('..')
from holstep import Holstep
from data import dump_data, load_data

# steps need to be used at least this many times
# to be considered as a dimension in the conjecture position
HOLSTEP_STEPUSAGE_LOWER_BOUND = 20

# not set value, this multiplied by HOLSTEP_METRIC_MAX, with overflow in uint16,
# will wrap around to a value greater than HOLSTEP_METRIC_MAX.
HOLSTEP_METRIC_BUILD_NOT_SET = -0.001

# maximum distance between conjectures
HOLSTEP_METRIC_MAX = 65000

def main():
    steps = []
    # comment out to limit which steps are executed
    steps.append(STEP_holstep_conjecture_ids)
    steps.append(STEP_holstepview_identifiers)
    steps.append(STEP_holstepview_conjecture_coordinates)
    steps.append(STEP_holstepview_metric_first)
    steps.append(STEP_holstepview_metric_fix)
    steps.append(STEP_holstepview_tsne)
    for step in steps:
        print()
        print(step)
        step()
        print()

###############################################################################

def STEP_holstep_conjecture_ids():
    with Holstep.Setup() as db:
        sql = 'SELECT Id FROM Conjecture ORDER BY Id'
        ids = db.ex_many(sql)
        ids = [a[0] for a in ids]
        
        ids = np.array(ids)
        np.save('../../data/holstep_conjecture_ids.npy', ids)
        print(ids)
        print(ids.shape)
     
def STEP_holstepview_identifiers():
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

def STEP_holstepview_conjecture_coordinates():
    id_to_step = np.load('../../data/holstepview_id_to_step.npy')
    step_to_id = load_data('../../data/holstepview_step_to_id.data')
    conjectures = np.load('../../data/holstep_conjecture_ids.npy')
    
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
    np.save('../../data/holstepview_conjecture_coords.npy', positions)
    print(positions)
    print(positions.shape)

def STEP_holstepview_metric_first():
    # example:
    # intersect: [-2, -1, 0, 1, 2] => [1, 0, 0, 0, 1]
    # union: [-2, -1, 0, 1, 2] => [1, 1, 0, 1, 1]
    
    # number of conjectures
    count = load_holstepview_coords().shape[0]
    
    # pairwise distances
    results = np.full((count, count), HOLSTEP_METRIC_BUILD_NOT_SET, dtype='double')

    for i in range(count):
        print(i)
        # need to load each time as this is overwritten
        positions = load_holstepview_coords()
        
        for j in range(i + 1, count):
            # efficient way to determine relationship between conjectures
            positions[j, :] += positions[i, :]
        
        # matching useless premises should count the same as useful ones
        positions[:,:] = np.abs(positions[:,:])
        
        pos_intersect = positions
        pos_union = np.copy(positions)
        
        # to count only the matching ones, the intersection
        to_zero = pos_intersect[:,:] < 2  
        pos_intersect[to_zero] = 0
        pos_intersect[:,:] = pos_intersect[:,:] / 2
        
        # prevent double counting the intersection in the union.
        to_one = pos_union[:,:] > 1
        pos_union[to_one] = 1
        
        for j in range(i + 1, count):
            # jaccard similarity
            results[i][j] = np.sum(pos_intersect[j,:]) / np.sum(pos_union[j,:])
            
    np.save('../../data/holstepview_metric_base.npy', results)
    
def STEP_holstepview_metric_fix():
    array = np.load('../../data/holstepview_metric_base.npy')
    
    def fill_in_diagonal(array):
        for i in range(array.shape[0]):
            array[i][i] = 1.0
        return array
    
    def convert_to_uint16(array):
        array[:,:] *= HOLSTEP_METRIC_MAX
        array = array.astype('uint16')
        array = np.round(array)
        return array
    
    def make_symmetric(array):
        for i in range(array.shape[0]):
            for j in range(array.shape[1]):
                if array[i][j] > HOLSTEP_METRIC_MAX:
                    array[i][j] = array[j][i]
        return array
    
    def invert_metric(array):
        array[:,:] = HOLSTEP_METRIC_MAX - array[:,:]
        return array
    
    ops = [fill_in_diagonal, convert_to_uint16, make_symmetric, invert_metric]
    for f in ops:
        print(f)
        array = f(array)

    np.save('../../data/holstepview_metric.npy', array)
    
def STEP_holstepview_tsne():
    inpath = '../../data/holstepview_metric.npy'
    outpath = '../../data/holstepview_tsne_{}d.npy'
    apply_tsne(inpath, outpath, 2)
    apply_tsne(inpath, outpath, 3)
    
###############################################################################
        
def load_holstepview_coords():
    return np.load('../../data/holstepview_conjecture_coords.npy')

def apply_tsne(inpath, outpath, dim):
    dists = np.load(inpath)

    tsne = TSNE(n_components=dim, perplexity=40, verbose=1, metric='precomputed')
    tsne_results = tsne.fit_transform(dists)
    
    tsne_results = np.array(tsne_results)
    np.save(outpath.format(dim), tsne_results)

main()
