import sys
import numpy as np
import json

sys.path.append('../src')
from holstep import Holstep

def main():
    steps = []
    # if False:
    steps.append(STEP_build_tsne)
    steps.append(STEP_build_pca)
    for step in steps:
        print()
        print(step)
        print()
        step()
        print()
            
def STEP_build_tsne():
    x = np.load('../data/vissetup/holstepview_tsne_2d.npy')
    data = x.tolist()
    cnames = None
    with Holstep(path='../data/holstep.db') as db:
        sql = 'SELECT Name FROM Conjecture ORDER BY Id'
        cs = db.ex_many(sql)
        cnames = [r[0] for r in cs]
    for points, name in zip(data, cnames):
        points.insert(0, name)
    with open('tsne.json', 'w+') as file:
        file.write(json.dumps(data))
        
def STEP_build_pca():
    x = np.load('../data/vissetup/holstepview_pca_2d.npy')
    data = x.tolist()
    cnames = None
    with Holstep(path='../data/holstep.db') as db:
        sql = 'SELECT Name FROM Conjecture ORDER BY Id'
        cs = db.ex_many(sql)
        cnames = [r[0] for r in cs]
    for points, name in zip(data, cnames):
        points.insert(0, name)
    with open('pca.json', 'w+') as file:
        file.write(json.dumps(data))

if __name__ == '__main__':
    main()
