import sys
import numpy as np
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA

sys.path.append('..')
from holstep import Holstep
from data import dump_data, load_data

PATH = '..\\..\\data\\vissetup\\'

# steps need to be used at least this many times
# to be considered as a dimension in the conjecture position
HOLSTEP_STEPUSAGE_LOWER_BOUND = 20
SUBSET_STEPUSAGE_LOWER_BOUND = 10

# not set value, this multiplied by HOLSTEP_METRIC_MAX, with overflow in uint16,
# will wrap around to a value greater than HOLSTEP_METRIC_MAX.
HOLSTEP_METRIC_BUILD_NOT_SET = -0.001

# maximum distance between conjectures
HOLSTEP_METRIC_MAX = 65000

# subset boundaries of the 2d holstep tnse data
SUBSET_X_MIN = 9
SUBSET_X_MAX = 63
SUBSET_Y_MIN = -55
SUBSET_Y_MAX = -2

def main():
    steps = []
    # comment out to limit which steps are executed
    steps.append(STEP_holstep_conjecture_ids)
    steps.append(STEP_holstepview_premise_identifiers)
    steps.append(STEP_holstepview_conjecture_coordinates)
    steps.append(STEP_holstepview_metric_base)
    steps.append(STEP_holstepview_metric_fix)
    steps.append(STEP_holstepview_tsne)
    steps.append(STEP_holstepview_pca)
    steps.append(STEP_subset_list)
    steps.append(STEP_subset_premise_identifiers)
    steps.append(STEP_subset_conjecture_coordinates)
    steps.append(STEP_subset_zero_premise_conjectures)
    steps.append(STEP_subset_list_without_zero_premises)
    steps.append(STEP_subset_premise_identifiers)
    steps.append(STEP_subset_conjecture_coordinates)
    steps.append(STEP_subset_metric_base)
    steps.append(STEP_subset_metric_fix)
    steps.append(STEP_subset_tsne)
    steps.append(STEP_subset_pca)
    for step in steps:
        print()
        print(step)
        print()
        step()
        print()

###############################################################################

def STEP_holstep_conjecture_ids():
    with Holstep.Setup() as db:
        sql = 'SELECT Id FROM Conjecture ORDER BY Id'
        ids = db.ex_many(sql)
        ids = [a[0] for a in ids]
        
        ids = np.array(ids)
        np.save(PATH + 'holstep_conjecture_ids.npy', ids)
        print(ids)
        print(ids.shape)
     
def STEP_holstepview_premise_identifiers():
    build_premise_identifiers('holstepview', HOLSTEP_STEPUSAGE_LOWER_BOUND)

def STEP_holstepview_conjecture_coordinates():
    build_conjecture_coordinates('holstepview')

def STEP_holstepview_metric_base():
    build_metric('holstepview')
    
def STEP_holstepview_metric_fix():
    fix_metric('holstepview')
    
def STEP_holstepview_tsne():
    inpath = PATH + 'holstepview_metric.npy'
    outpath = PATH + 'holstepview_tsne_{}d.npy'
    apply_tsne(inpath, outpath, 2)
    apply_tsne(inpath, outpath, 3)
    
def STEP_holstepview_pca():
    inpath = PATH + 'holstepview_conjecture_coords.npy'
    outpath = PATH + 'holstepview_pca_{}d.npy'
    apply_pca(inpath, outpath, 2)
    apply_pca(inpath, outpath, 3)
    
def STEP_subset_list():
    build_subset_list(additional_deletions=None)
    
def STEP_subset_premise_identifiers():
    build_premise_identifiers('subset', SUBSET_STEPUSAGE_LOWER_BOUND)
    
def STEP_subset_conjecture_coordinates():
    build_conjecture_coordinates('subset')
    
def STEP_subset_zero_premise_conjectures():
    coords = np.load(PATH + 'subset_conjecture_coords.npy')
    counts = [np.sum(np.abs(c)) for c in coords]
    zeros = [i for i in range(len(counts)) if counts[i] == 0]
    zeros = np.array(zeros)
    print(zeros)
    print(zeros.shape)
    np.save(PATH + 'subset_zero_conjectures.npy', zeros)
    
def STEP_subset_list_without_zero_premises():
    zeros = np.load(PATH + 'subset_zero_conjectures.npy')
    build_subset_list(additional_deletions=zeros)
    
def STEP_subset_metric_base():
    build_metric('subset')
    
def STEP_subset_metric_fix():
    fix_metric('subset')
    
def STEP_subset_tsne():
    inpath = PATH + 'subset_metric.npy'
    outpath = PATH + 'subset_tsne_{}d.npy'
    apply_tsne(inpath, outpath, 2)
    apply_tsne(inpath, outpath, 3)
    
def STEP_subset_pca():
    inpath = PATH + 'subset_conjecture_coords.npy'
    outpath = PATH + 'subset_pca_{}d.npy'
    apply_pca(inpath, outpath, 2)
    apply_pca(inpath, outpath, 3)
    
###############################################################################

def build_premise_identifiers(prefix, premise_lower_bound):
    cids = np.load(PATH + '{}_conjecture_ids.npy'.format(prefix))
    with Holstep.Setup() as db:
        sql = 'SELECT ConjectureId, StepId FROM ConjectureStep '
        sql += 'GROUP BY StepId HAVING COUNT(StepId) >= {} '.format(premise_lower_bound)
        steps = db.ex_many(sql)
        steps = [a[1] for a in steps if a[0] in cids]
        steps = sorted(list(set(steps)))    
    
        id_to_step = np.array(steps)
        np.save(PATH + '{}_premise_id_to_step.npy'.format(prefix), id_to_step)
        print(id_to_step)
        print(len(id_to_step))
        
        step_to_id = {}
        for i, x in enumerate(steps):
            step_to_id[x] = i
        dump_data(PATH + '{}_premise_step_to_id.data'.format(prefix), step_to_id)
        print(step_to_id)
        print(len(step_to_id))
        
def build_conjecture_coordinates(prefix):
    cids = np.load(PATH + '{}_conjecture_ids.npy'.format(prefix))
    id_to_step = np.load(PATH + '{}_premise_id_to_step.npy'.format(prefix))
    step_to_id = load_data(PATH + '{}_premise_step_to_id.data'.format(prefix))
    positions = np.zeros((len(cids), len(id_to_step)), dtype=int)
    with Holstep.Setup() as db:
        for i, cid in enumerate(cids):
            print(cid)
            sql = 'SELECT StepId, IsUseful FROM ConjectureStep '
            sql += 'WHERE ConjectureId = {}'.format(cid)
            steps = db.ex_many(sql)
            
            for sid, is_useful in steps:
                if (sid in step_to_id):
                    positions[i][step_to_id[sid]] = (1 if is_useful == 1 else -1)

    positions = np.array(positions)
    np.save(PATH + '{}_conjecture_coords.npy'.format(prefix), positions)
    print(positions)
    print(positions.shape)
    
def build_subset_list(additional_deletions=None):
    tsne = np.load(PATH + 'holstepview_tsne_2d.npy')
    vbetween = np.vectorize(between)
    subset_x = vbetween(tsne[:, 0], SUBSET_X_MIN, SUBSET_X_MAX) 
    subset_y = vbetween(tsne[:, 1], SUBSET_Y_MIN, SUBSET_Y_MAX)
    subset_compl = [i for i in range(tsne.shape[0]) if not (subset_x[i] and subset_y[i])]
    
    # reverse so early deleted indices do not affect later ones
    subset_compl = sorted(subset_compl)[::-1]
    
    print(subset_compl)
    print(len(subset_compl))
    subset_compl = np.array(subset_compl)
    
    ids = np.load(PATH + 'holstep_conjecture_ids.npy')
    ids = np.delete(ids, subset_compl, axis=0)
    
    if additional_deletions is not None:
        ids = np.delete(ids, additional_deletions, axis=0)
    
    print(list(ids))
    print(ids.shape)
    np.save(PATH + 'subset_conjecture_ids.npy', ids)
    
def build_metric(prefix):
    def load_coords():
        return np.load(PATH + '{}_conjecture_coords.npy'.format(prefix))
    
    # example:
    # intersect: [-2, -1, 0, 1, 2] => [1, 0, 0, 0, 1]
    # union: [-2, -1, 0, 1, 2] => [1, 1, 0, 1, 1]
    
    # number of conjectures
    count = load_coords().shape[0]
    
    # pairwise distances
    results = np.full((count, count), HOLSTEP_METRIC_BUILD_NOT_SET, dtype='double')

    for i in range(count):
        print(i)
        # need to load each time as this is overwritten
        positions = load_coords()
        
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
            
    np.save(PATH + '{}_metric_base.npy'.format(prefix), results)
    
def fix_metric(prefix):
    array = np.load(PATH + '{}_metric_base.npy'.format(prefix))
    
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

    np.save(PATH + '{}_metric.npy'.format(prefix), array)

def apply_tsne(inpath, outpath, dim):
    dists = np.load(inpath)

    tsne = TSNE(n_components=dim, perplexity=40, verbose=1, metric='precomputed')
    tsne_results = tsne.fit_transform(dists)
    
    tsne_results = np.array(tsne_results)
    np.save(outpath.format(dim), tsne_results)
    
def apply_pca(inpath, outpath, dim):
    coords = np.load(inpath)

    pca = PCA(n_components=dim)
    pca_results = pca.fit_transform(coords)
    
    pca_results = np.array(pca_results)
    np.save(outpath.format(dim), pca_results) 

###############################################################################
    
def between(x, a, b):
    return x >= a and x <= b

if __name__ == '__main__':
    main()
