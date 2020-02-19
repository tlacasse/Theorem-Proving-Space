from sklearn.manifold import TSNE
import numpy as np

array = np.load('../../data/conjecture_step_coords.npy')

def dist(positions, a, b):
    d = 5000
    for x, y in zip(a, b):
        if x != 0 and x == y:
            d -= 1
    return d

tsne = TSNE(n_components=3, verbose=1)
tsne_results = tsne.fit_transform(array)

tsne_results = np.array(tsne_results)
np.save('../../data/tsne2.npy', tsne_results)
