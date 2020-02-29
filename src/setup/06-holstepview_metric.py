import numpy as np
from setup_vars import HOLSTEP_METRIC_BUILD_NOT_SET

# intersect: [-2, -1, 0, 1, 2] => [1, 0, 0, 0, 1]
# union: [-2, -1, 0, 1, 2] => [1, 1, 0, 1, 1]

def main():
    # number of conjectures
    count = load_positions().shape[0]
    
    # pairwise distances
    results = np.full((count, count), HOLSTEP_METRIC_BUILD_NOT_SET, dtype='double')

    for i in range(count):
        print(i)
        # need to load each time as this is overwritten
        positions = load_positions()
        
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
        
def load_positions():
    return np.load('../../data/holstepview_conjecture_coords.npy')

main()
