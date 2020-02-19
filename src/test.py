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

from difflib import SequenceMatcher
from data import Holstep
import numpy as np

def get_all_conjectures():
    with Holstep() as db:
        return db.list_conjectures()
    
def link_if_related_name(a, b):
    return SequenceMatcher(None, a, b).ratio() > 0.95

data = get_all_conjectures()
data = [c[2] for c in data]    

k = 10
init = np.random.permutation(len(data))[:k]    
    
clustering = kmedoids(data, init, metric=link_if_related_name)

clustering.process()

clusters = clustering.get_clusters()

print(clusters)
    
    
