import sys
import glob
import numpy as np
from collections import Counter

sys.path.append('..')
from holstep import Holstep, HolstepTreeParser, QuickHolstepSeqParser
from data import dump_data, load_data

PATH = '..\\..\\data\\model\\'

def main():
    steps = []
    # comment out to limit which steps are executed
    steps.append(STEP_id_lists)
    steps.append(STEP_train_load_texts)
    steps.append(STEP_train_trees)
    steps.append(STEP_test_trees)
    steps.append(STEP_train_tokens_unique)
    steps.append(STEP_clean_train_tokens)
    steps.append(STEP_train_token_ids)
    steps.append(STEP_relationships)
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
    print('IDMAPS')
    for a in ['train', 'test']:
        for b in ['conjecture', 'premise']:
            build_id_map('{}_{}'.format(a, b))
    
def STEP_train_load_texts():
    load_texts('Conjecture', 'conjecture', 'train')
    load_texts('Step', 'premise', 'train')
    load_texts('Conjecture', 'conjecture', 'test')
    load_texts('Step', 'premise', 'test')

def STEP_train_trees():
    build_trees_per_table('conjecture', 'train')
    build_trees_per_table('premise', 'train')
    
def STEP_test_trees():
    build_trees_per_table('conjecture', 'test')
    build_trees_per_table('premise', 'test')

def STEP_train_tokens_unique():
    build_unique_tokens('conjecture', 'train')
    build_unique_tokens('premise', 'train')
    
def STEP_clean_train_tokens():
    clean_unique_tokens('conjecture', 'train')
    clean_unique_tokens('premise', 'train')
    
def STEP_train_token_ids():
    build_ids('conjecture', 'train', 'unique_tokens', 'tokens')
    build_ids('premise', 'train', 'unique_tokens', 'tokens')
    
def STEP_relationships():
    build_premise_conjecture_relationships('train')
    build_premise_conjecture_relationships('test')
    
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

def build_id_map(prefix):
    arr = np.load(PATH + '{}_ids.npy'.format(prefix))
    idmap = {k: i for i, k in enumerate(arr)}
    dump_data(PATH + '{}_idmap.data'.format(prefix), idmap)

# list together all text representations   
def load_texts(table, data_prefix, part_prefix):
    ids = np.load(PATH + '{}_{}_ids.npy'.format(part_prefix, data_prefix))
    texts = None
    with Holstep.Setup() as db:
        sql = 'SELECT Id, Text FROM {} ORDER BY Id'.format(table)
        texts = db.ex_many(sql)
        texts = [a[1] for a in texts if a[0] in ids]
    dump_data(PATH + '{}_{}_loaded_texts.data'.format(part_prefix, data_prefix), texts)  
    
def build_trees_per_table(data_prefix, part_prefix):
    parser = HolstepTreeParser()
    seqparser = QuickHolstepSeqParser()
    
    texts = load_data(PATH + '{}_{}_loaded_texts.data'.format(part_prefix, data_prefix))

    def save(t, n):
        n = ("000000" + str(n))[-6:]
        dump_data(PATH + '{}_{}_trees_{}.data'.format(part_prefix, data_prefix, n), t)
        
    i = 0
    trees = []
    for text in texts:
        i += 1
        if i % 10000 == 0:
            print(i)
            save(trees, i)
            trees = []
        
        tree = parser.parse(text)
        tree.build_unique_info()
        
        if tree.has_FILL():
            print(text)
            tree.printtree()
            raise Exception()
        if any([b > 3 for b in tree.unique_branching.keys()]):
            print(text)
            tree.printtree()
            raise Exception()
        seq = seqparser.parse(text)
        if len(seq) != tree.node_count():
            print(text)
            print(len(seq))
            print(tree.node_count())
            tree.printtree()
            raise Exception()
        if len(parser.stack) != 1:
            print(text)
            tree.printtree()
            print(parser.stack)
            raise Exception()
        trees.append((parser.varlist, parser.varfunclist, tree.as_lite()))
    save(trees, i)
    
def build_unique_tokens(data_prefix, part_prefix):
    unique_tokens = Counter()
    for v, vf, tree in iter_trees(data_prefix, part_prefix):
        unique_tokens.update(tree.unique_tokens())
    dump_data(PATH + '{}_{}_unique_tokens_base.data'.format(part_prefix, data_prefix), 
              unique_tokens) 
    
def clean_unique_tokens(data_prefix, part_prefix):
    tokens = load_data(PATH + '{}_{}_unique_tokens_base.data'.format(part_prefix, data_prefix))
    print(len(tokens))
    varset = set()
    varfuncset = set()
    for v, vf, tree in iter_trees(data_prefix, part_prefix):
        varset.update(v)
        varfuncset.update(vf)
    print(len(varset))
    print(len(varfuncset))
    keys_to_delete = []
    
    for k, kset in [('VAR', varset), ('VARFUNC', 'varfuncset')]:
        tokens[k] = 0
        for v in kset:
            if v in tokens:
                tokens[k] += tokens[v]
                keys_to_delete.append(v)
            
    tokens['_n'] = 0
    for k in tokens:
        if k[0] == '_' and k[1:].isdigit():
            tokens['_n'] += tokens[k]
            keys_to_delete.append(k)
            
    tokens['UNK'] = 0
    
    print(len(keys_to_delete))
    for k in keys_to_delete:
        del tokens[k]
     
    print(len(tokens))
    print()
    print()
    dump_data(PATH + '{}_{}_unique_tokens.data'.format(part_prefix, data_prefix), tokens)
    
def build_ids(data_prefix, part_prefix, input_counter, output_name):
    objs = load_data(PATH + '{}_{}_{}.data'.format(part_prefix, data_prefix, input_counter))
    
    ids = [k for k in objs.keys()]
    ids.sort()
    idmap = {k:i for i, k in enumerate(ids)}
    
    dump_data(PATH + '{}_{}_{}_ids.data'.format(part_prefix, data_prefix, output_name), ids)
    dump_data(PATH + '{}_{}_{}_idmap.data'.format(part_prefix, data_prefix, output_name), idmap)
    
def build_premise_conjecture_relationships(part_prefix):
    print(part_prefix)
    cids = np.load(PATH + '{}_conjecture_ids.npy'.format(part_prefix))
    cidmap = load_data(PATH + '{}_conjecture_idmap.data'.format(part_prefix))
    pidmap = load_data(PATH + '{}_premise_idmap.data'.format(part_prefix))
    relationships = None
    with Holstep.Setup() as db:
        sql = 'SELECT ConjectureId, StepId FROM ConjectureStep '
        sql += 'WHERE IsUseful = 1 ORDER BY ConjectureId'
        relationships = db.ex_many(sql)
        print('loaded')
    
    relationships = [(c, p) for c, p in relationships if c in cids]   
    result = np.empty((len(relationships), 2), dtype='uint16')
    for i, (cid, pid) in enumerate(relationships):
        result[i][0] = cidmap[cid]
        result[i][1] = pidmap[pid]
        
    print(result)
    print(result.shape)
    np.save(PATH + '{}_relationships.npy'.format(part_prefix), result)
    
def iter_trees(data_prefix, part_prefix):
    return iter_files('{}_{}_trees_'.format(part_prefix, data_prefix))
            
def iter_files(fileprefix):   
    for f in glob.glob(PATH + '{}*'.format(fileprefix)):
        trees = load_data(f)
        print(f)
        for t in trees:
            yield t

if __name__ == '__main__':
    main()
