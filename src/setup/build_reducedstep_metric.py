import numpy as np

NOT_SET = 50000

def main():
    maxval = 0
    positions = np.load('../../data/conjecture_step_coords.npy')
    conjectures = np.load('../../data/conjecture_ids.npy')
    count = len(conjectures)
    results = np.full((count, count), NOT_SET, dtype='uint16')
    for a in range(count):
        print(a)
        for b in range(count):
            this = set_dist(positions, results, a, b)
            if (this > maxval):
                maxval = this
    np.save('reducedstep_metric.npy', results)
    print('maxval: ' + str(maxval)) # => 2616

def set_dist(positions, results, a, b):
    if (a > b):
        a, b = b, a
    if (results[a][b] == NOT_SET):
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
