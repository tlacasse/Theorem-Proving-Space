import sys
import glob
import re
import numpy as np

sys.path.append('..')
from data import load_data
from var import PREMISE_TOKEN_DIMENSION

PATH = '..\\..\\data\\training\\'
PREMODEL = '..\\..\\data\\premodel\\'
MODELS = '..\\..\\data\\models\\'

def main():
    steps = []
    # comment out to limit which steps are executed
    # if False:
    steps.append(STEP_train_conjecture_token_bag)
    steps.append(STEP_initial_premise_token_encoding)
    steps.append(STEP_subtree_encodings_structure)
    steps.append(STEP_training_arrays)
    for step in steps:
        print()
        print(step)
        print()
        step()
        print()

###############################################################################       
    
def STEP_train_conjecture_token_bag():
    build_conjecture_token_bag('train')
    
def STEP_initial_premise_token_encoding():
    build_initial_premise_token_encodings()

def STEP_subtree_encodings_structure():
    build_subtree_encodings_structure()
    
def STEP_training_arrays():
    build_training_arrays()
    
###############################################################################

def build_conjecture_token_bag(part_prefix):
    cids = np.load(PREMODEL + '{}_conjecture_ids.npy'.format(part_prefix))
    tokens = load_data(PREMODEL + '{}_conjecture_tokens_ids.data'.format(part_prefix))
    tokenmap = load_data(PREMODEL + '{}_conjecture_tokens_idmap.data'.format(part_prefix))
    
    result = np.zeros((cids.shape[0], len(tokens)), dtype='uint8')
    for i, (v, vf, tree) in enumerate(iter_trees('conjecture', part_prefix)):
        tree.cleanreplace(v, vf, tokens)
        tree_tokens = tree.unique_tokens()
        for j, t in enumerate(tree_tokens.keys()):
            result[i][tokenmap[t]] = 1
            
    print(result)
    print(result.shape)
    np.save(PATH + 'PC_{}_conjecture_token_bag.npy'.format(part_prefix), result)
    
def build_initial_premise_token_encodings():
    tokens = load_data(PREMODEL + 'train_premise_tokens_ids.data')
    
    def get_val(i, bound=0.001):
        return bound + ((1 - bound - bound) * (i / len(tokens)))
    
    result = np.empty((len(tokens), PREMISE_TOKEN_DIMENSION), dtype='double')
    for i in range(len(tokens)):
        result[i, :] = np.full((PREMISE_TOKEN_DIMENSION,), get_val(i), dtype='double')
        
    print(result)
    print(result.shape)
    np.save(PATH + 'PC_initial_token_encoding.npy', result)
    
def build_subtree_encodings_structure():
    subtrees = load_data(PREMODEL + 'train_premise_subtrees_idmap.data')
    result = np.zeros((len(subtrees), PREMISE_TOKEN_DIMENSION), dtype='double')  
    
    print(result)
    print(result.shape)
    np.save(MODELS + 'PC_subtree_encoding.npy', result)
    
def build_training_arrays():
    #conjecture_records = np.load(PATH + 'PC_train_conjecture_token_bag.npy')
    layer_groups = ['002', '003', '004', '005', '006', '007', '008', '009', '010',
                    '11-15', '16-30', 'gt30', 'whole']
    
    def iter_records(layer_group):
        for f in glob.glob(records_train__trees_0.format(layer_group) + '*'):
            yield f
    
    for layer in layer_groups:
        print(layer)
        for c, f in enumerate(iter_records(layer)):
            records = load_data(f)
            
            n = len(records)
            X = np.empty((n, 4), dtype='uint32')
            Y = np.empty((n,), dtype='uint8')
        
            for i, (token, stid, left, right, cid) in enumerate(records):
                X[i, 0] = stid
                X[i, 1] = token
                X[i, 2] = left
                X[i, 3] = right
                Y[i] = cid
                
            print(X)
            print(X.shape)
            print(Y)
            print(Y.shape)
            np.save(PATH + 'points/PC_{}_premise_map_{}.npy'.format(layer, c), X)
            np.save(PATH + 'points/PC-A_{}_conjecture_tokens_{}.npy'.format(layer, c), Y)
    
###############################################################################

records_train__trees_0 = PREMODEL + 'records\\train_{}_0'

def iter_trees(data_prefix, part_prefix):
    return iter_files(PREMODEL + 'trees/{}_{}_trees_'.format(part_prefix, data_prefix))

def iter_files(fileprefix):   
    for f in glob.glob('{}*'.format(fileprefix)):
        trees = load_data(f)
        print(f)
        for t in trees:
            yield t
          
def get_iter_records_count(layer_group):
    path = records_train__trees_0.format(layer_group) + '*'
    last_path = list(glob.glob(path))[-1]
    last_path = last_path[last_path.rfind('_'):]
    return int(re.sub('[^0-9]', '', last_path))

if __name__ == '__main__':
    main()
