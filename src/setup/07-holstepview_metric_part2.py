import numpy as np
from setup_vars import HOLSTEP_METRIC_MAX

def main():
    array = np.load('../../data/holstepview_metric_base.npy')
    
    ops = [fill_in_diagonal, convert_to_uint16, make_symmetric, invert_metric]
    for f in ops:
        print(f)
        array = f(array)

    np.save('../../data/holstepview_metric.npy', array)
    
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

main()
