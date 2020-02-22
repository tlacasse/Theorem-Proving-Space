from sklearn.manifold import TSNE
import numpy as np

def main():
    reduce_to_dimension(2)
    reduce_to_dimension(3)

def reduce_to_dimension(dim):
    dists = np.load('../../data/holstepview_metric.npy')

    tsne = TSNE(n_components=dim, verbose=1, metric='precomputed')
    tsne_results = tsne.fit_transform(dists)
    
    tsne_results = np.array(tsne_results)
    np.save('../../data/holstepview_tsne_{}d.npy'.format(dim), tsne_results)
    
main()
