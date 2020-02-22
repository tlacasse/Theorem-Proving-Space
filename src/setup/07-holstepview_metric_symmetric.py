import numpy as np
from setup_vars import HOLSTEP_METRIC_NOT_SET

array = np.load('../../data/holstepview_metric_counts.npy')

for i in range(array.shape[0]):
    for j in range(array.shape[1]):
        if array[i][j] == HOLSTEP_METRIC_NOT_SET:
            array[i][j] = array[j][i]

np.save('../../data/holstepview_metric_counts_symmetric.npy', array)
