import numpy as np

array = np.load('cmetric_counts.npy')
array[:,:] = 2616 - array[:,:]
np.save('cmetric.npy', array)
