import sys
import glob
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
    steps.append(STEP_train_conjecture_token_bag)
    steps.append(STEP_initial_premise_token_encoding)
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
    encodings = []
    for x in range(len(tokens)):
        encodings.append(np.random.uniform(low=0.0, high=1.0, size=(PREMISE_TOKEN_DIMENSION,)))
    encodings.sort(key=np.sum)
    
    result = np.empty((len(tokens), PREMISE_TOKEN_DIMENSION), dtype='double')
    for i in range(len(tokens)):
        result[i, :] = encodings[i]
        
    print(result)
    print(result.shape)
    np.save(PATH + 'PC_initial_token_encoding.npy', result)
    
###############################################################################

def iter_trees(data_prefix, part_prefix):
    return iter_files(PREMODEL + 'trees/{}_{}_trees_'.format(part_prefix, data_prefix))

def iter_files(fileprefix):   
    for f in glob.glob('{}*'.format(fileprefix)):
        trees = load_data(f)
        print(f)
        for t in trees:
            yield t

if __name__ == '__main__':
    main()
