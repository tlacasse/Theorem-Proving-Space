import numpy as np
from setup_vars import HOLSTEP_METRIC_NOT_SET

def main():
    # keep track of maximum value
    # each distance will be subracted from the max
    # so the closest conjectures will have distance 0
    maxval = 0
    positions = np.load('../../data/holstepview_conjecture_coords.npy')
    conjectures = np.load('../../data/holstep_conjecture_ids.npy')
    
    count = len(conjectures)
    results = np.full((count, count), HOLSTEP_METRIC_NOT_SET, dtype='uint16')
    if False:
        # loading to continue
        results = np.load('../../data/holstepview_metric_counts.npy')

    try:
        for a in range(count):
            print(a)
            for b in range(count):
                this = set_dist(positions, results, a, b)
                if (this > maxval):
                    maxval = this
                    
    finally:
        np.save('../../data/holstepview_metric_counts.npy', results)
        print('maxval: ' + str(maxval)) # => 908

def set_dist(positions, results, a, b):
    if (a > b):
        a, b = b, a
    if (results[a][b] == HOLSTEP_METRIC_NOT_SET):
        results[a][b] = dist(positions, a, b)
        return results[a][b]
    return 0

def dist(positions, a, b):
    d = 0
    for x, y in zip(positions[a], positions[b]):
        if x != 0 and x == y:
            d += 1
    return d

main()
