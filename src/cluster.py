from difflib import SequenceMatcher
from holstep import Holstep
import numpy as np
import os

CHOICES = [
    1513
    ,1090
    ,8567
    ,6288
    ,6723
    ,1009
    ,1438
    ,742	
    ,8915
    ,5762
    ,5568
    ,3936
    ,1428
    ,3289
    ,2070
    ,2847
    ,821	
    ,9388
    ,3254
    ,6378
    ,1427
    ,7980
    ,6401
    ,1930
    ,7316
    ,2578
    ,6827
    ,3903
    ,6059
    ,3353
    ,9550
    ,7758
    ,7041
    ,5330
    ,1393
    ,8517
    ,4318
    ,31	
    ,5665
    ,2111
    ,6914
    ,9453
    ,3607
    ,2951
    ,8690
    ,5237
    ,7373
    ,564	
    ,6672
    ,3053
    ,9436
    ,9810
    ,979	
    ,5137
    ,7253
    ,6770
    ,458
    ,6775
    ,7986
    ,6817
    ,1436
    ,4221
    ,7309
    ,2759
    ,89	
    ,1288
    ,7061
    ,2780
    ,8840
    ,8550
    ,7450
    ,9993
    ,4312
    ,7119
    ,6119
    ,3210
    ,6587
    ,886	
    ,8263
    ,9614
    ,1119
    ,4827
    ,3758
    ,8294
    ,1146
    ,6836
    ,6156
    ,1975
    ,5504
    ,6076
    ,9720
    ,7408
    ,702	
    ,8944
    ,2730
    ,2344
    ,9260
    ,573	
    ,7390
    ,6386
    ,9702
    ,5835
    ,1172
    ,7777
    ,9185
    ,5122
    ,9339
    ,7962
    ,9925
    ,9401
    ,1628
    ,55	
    ,5490
    ,8110]

def get_all_conjectures():
    with Holstep() as db:
        return db.list_conjectures()
    
def get_random_subset(data, count):
    ixs = np.random.permutation(len(data))[:count]
    return [data[i - 1] for i in CHOICES] # - 1 to resolve offset

def build_nodes(data):
    result = []
    for i, t, n in data:
        result.append(dict(id=i, group=t))
    return result

def build_links(data, link_function):
    result = []
    i = 1
    for i1, t1, n1 in data:
        for i2, t2, n2 in data[i:]:
            if (link_function(n1, n2)):
                result.append(dict(source=i1, target=i2))
        i += 1
    return result

def build_data(data, link_function):
    return dict(nodes=build_nodes(data), 
                links=build_links(data, link_function))
    
def link_if_similar_length(a, b):
    return abs(len(a) - len(b)) < 3

def link_if_related_name(a, b):
    return SequenceMatcher(None, a, b).ratio() > 0.95

class HolstepMetricCache:
    
    def __init__(self, db, path='data/cmetric.npy', reset=False):
        self.db = db
        self.path = path
        self.array = None;
        if os.path.isfile(path) and not reset:
            self.array = np.load(path)
        else:
            self.array = np.full((11410, 11410), 255, dtype='uint8')
    
    def save(self):
        np.save(self.path, self.array)
        
    def dist(self, a, b):
        ixa = self._map_id(a)
        ixb = self._map_id(b)
        if (ixa > ixb):
            ixa, ixb = ixb, ixa
        if (self.array[ixa][ixb] == 255):
            a_steps = self._get_steps(a)
            b_steps = self._get_steps(b)
            self.array[ixa][ixb] = len(a_steps & b_steps)
        return self.array[ixa][ixb]
    
    def _map_id(self, x):
        if (x > 10000):
            x -= 1 # 10001 - 1 => 10000, 1 after 9999
        return x - 1 # 1 => 0
    
    def _get_steps(self, i):
        sql = 'SELECT CASE WHEN IsUseful = 1 THEN StepId ELSE -1 * StepId END AS Value '
        sql += 'FROM ConjectureStep WHERE ConjectureId = {}'.format(i)
        return set([x[0] for x in self.db.execute_many_np(sql)])



"""
class KMedoids():
    
    def __init__(self, points, k, distance_metric):
        self.points = points
        self.k = k # number of clusters
        self.distance_metric = distance_metric
        self.count = len(points)
        self.classes = np.zeros((self.count,), dtype=int)
        self.centers = np.random.permutation(self.count)[:k]
        
    def iterate(self, n):
        if (n == 0):
            return
        self.iterate(n - 1)
        
        # assign classes
        for i, p in enumerate(self.points):
            closest = 0
            prev = None
            for j, c in enumerate(self.clusters):
                dist = self.distance_metric(p, self.points[c])
                if (prev is None or dist < prev):
                    closest = j
            self.classes[i] = closest
        
        # recompute centers
        for c in range(self.k):
            in_this_cluster = []
            for i in range(self.count):
                if 
                    in_this_cluster.append()
            in_this_cluster = filter((lambda j: self.classes[j] == i))
            in_this_one = filter(, 
                                 range(len(self.points)))
            in_this_one = list(map((lambda j: self.points[j]), in_this_one))
            medoids_test = [0] * len(in_this_one)
            for j, p in enumerate(in_this_one):
                medoids_test[j] = self.sum_dist(p, in_this_one)
            
            self.clusters[i] = in_this_one[argmin(medoids_test)]
            
            for j, p in enumerate(in_this_one):
                print('? medoid({}) == {}:'.format(i, p))
                print('sum(d({}, x) for x in [{}])\n\t    = {} = {}'.format(
                        p, ', '.join([str(x) for x in in_this_one]), 
                        ' + '.join([str(self.dist(p, x)) for x in in_this_one]),
                        medoids_test[j]
                        ))
            print()
            print('medoid({}) = {}'.format(i, self.clusters[i]))
            print()
        print()
        
    def dist(self, p1, p2):
        return float(abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]))
    
    def sum_dist(self, c, ps):
        return sum(self.dist(c, p) for p in ps)
"""