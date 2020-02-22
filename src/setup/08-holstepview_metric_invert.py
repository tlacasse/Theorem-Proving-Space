import numpy as np
from setup_vars import HOLSTEP_METRIC_MAX

array = np.load('../../data/holstepview_metric_counts_symmetric.npy')

array[:,:] = HOLSTEP_METRIC_MAX - array[:,:]

np.save('../../data/holstepview_metric.npy', array)
