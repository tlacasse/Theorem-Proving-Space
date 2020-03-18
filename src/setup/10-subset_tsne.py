from sklearn.manifold import TSNE
import numpy as np

def main():
    reduce_to_dimension(2)
    reduce_to_dimension(3)

def reduce_to_dimension(dim):
    dists = np.load('../../data/subset_metric.npy')

    tsne = TSNE(n_components=dim, perplexity=40, verbose=1, metric='precomputed')
    tsne_results = tsne.fit_transform(dists)
    
    tsne_results = np.array(tsne_results)
    np.save('../../data/subset_tsne_{}d.npy'.format(dim), tsne_results)
    
main()
