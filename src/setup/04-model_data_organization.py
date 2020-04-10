import sys
import numpy as np
from collections import Counter

sys.path.append('..')
from holstep import Holstep
from data import dump_data, load_data

PATH = '../../data/model/'

def main():
    steps = []
    # comment out to limit which steps are executed
    steps.append(STEP_id_lists)
    steps.append(STEP_train_load_texts)
    for step in steps:
        print()
        print(step)
        print()
        step()
        print()
      
###############################################################################

def STEP_id_lists():
    print('CONJECTURES')
    cids = np.load('../../data/subset_conjecture_ids.npy')
    train_cids = cids[cids < 10000]
    test_cids = cids[cids >= 10000]
    np.save(PATH + 'train_conjecture_ids.npy', train_cids)
    np.save(PATH + 'test_conjecture_ids.npy', test_cids)
    print('train')
    print(train_cids)
    print(train_cids.shape)
    print('test')
    print(test_cids)
    print(test_cids.shape)
    print('PREMISES')
    build_premise_list(train_cids, 'train')
    build_premise_list(test_cids, 'test')
    
def STEP_train_load_texts():
    load_texts('Conjecture', 'conjecture', 'train')
    load_texts('Step', 'premise', 'train')
    
###############################################################################

def build_premise_list(cids, prefix):
    premises = None
    with Holstep.Setup() as db:
        sql = 'SELECT ConjectureId, StepId FROM ConjectureStep '
        sql += 'WHERE IsUseful = 1'
        premises = db.ex_many(sql)
        
    premises = [a[1] for a in premises if a[0] in cids]
    premises = list(set(premises))
    premises.sort()
    premises = np.array(premises)
    print(prefix)
    print(premises)
    print(premises.shape)
    np.save(PATH + '{}_premise_ids.npy'.format(prefix), premises)

# list together all text representations   
def load_texts(table, data_prefix, part_prefix):
    ids = np.load(PATH + '{}_{}_ids.npy'.format(part_prefix, data_prefix))
    texts = None
    with Holstep.Setup() as db:
        sql = 'SELECT Id, Text FROM {} ORDER BY Id'.format(table)
        texts = db.ex_many(sql)
        texts = [a[1] for a in texts if a[0] in ids]
    dump_data(PATH + '{}_{}_loaded_texts.data'.format(part_prefix, data_prefix), texts)  
    
if __name__ == '__main__':
    main()
