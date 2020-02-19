from pyclustering.cluster.kmedoids import kmedoids
from pyclustering.cluster import cluster_visualizer
from pyclustering.utils import read_sample
from pyclustering.samples.definitions import FCPS_SAMPLES
# Load list of points for cluster analysis.
#sample = read_sample(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS)
# Set random initial medoids.
#initial_medoids = [1, 500]
# Create instance of K-Medoids algorithm.
#kmedoids_instance = kmedoids(sample, initial_medoids)
# Run cluster analysis and obtain results.
#kmedoids_instance.process()
#clusters = kmedoids_instance.get_clusters()
# Show allocated clusters.
#print(clusters)
# Display clusters.
#visualizer = cluster_visualizer()
#visualizer.append_clusters(clusters, sample)
#visualizer.show()

import pickle
from src.data import Holstep
import numpy as np
from pyclustering.utils.metric import distance_metric, type_metric

def get_all_conjectures():
    with Holstep() as db:
        return db.list_conjecture_ids()
    
array = np.load('data/cmetric.npy')

def dist(a, b):
    if (a > b):
        a, b = b, a
    return array[a][b]

metric = distance_metric(type_metric.USER_DEFINED, func=dist)

data = get_all_conjectures()

k = 10
init = np.random.permutation(len(data))[:k]    
    
clustering = kmedoids(data, init, metric=metric)

clustering.process()

clusters = clustering.get_clusters()
medoids = clustering.get_medoids()

with open('data/clusters.labels', 'wb') as file:
    pickle.dump(clusters, file)
with open('data/clusters.medoids', 'wb') as file:
    pickle.dump(medoids, file)

print(clusters)
print(clustering.get_medoids())
