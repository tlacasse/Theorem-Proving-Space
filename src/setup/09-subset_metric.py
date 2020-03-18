import numpy as np

X_MIN = 9
X_MAX = 63
Y_MIN = -55
Y_MAX = -2

def main():
    tsne = np.load('../../data/holstepview_tsne_2d.npy')
    vbetween = np.vectorize(between)
    subset_x = vbetween(tsne[:, 0], X_MIN, X_MAX) 
    subset_y = vbetween(tsne[:, 1], Y_MIN, Y_MAX)
    subset_compl = [i for i in range(tsne.shape[0]) if not (subset_x[i] and subset_y[i])]
    
    # reverse so early deleted indices do not affect later ones
    subset_compl = sorted(subset_compl)[::-1]
    
    print(subset_compl)
    print(len(subset_compl))
    
    dists = np.load('../../data/holstepview_metric.npy')
    for axis in [0, 1]:
        print(axis)
        dists = np.delete(dists, subset_compl, axis=axis)
        
    print(dists)
    print(dists.shape)
            
    np.save('../../data/subset_metric.npy', dists)
    
def between(x, a, b):
    return x >= a and x <= b
    
main()
