import sys
import numpy as np
from collections import Counter

sys.path.append('..')
from holstep import Holstep, HolstepTokenizer
from data import dump_data, load_data

# conjecture tokens need to be used at least this many times
TOKEN_USAGE_LOWER_BOUND = 2

def main():
    steps = []
    # comment out to limit which steps are executed
    steps.append(STEP_tokens_per_conjecture)
    steps.append(STEP_unique_tokens)
    for step in steps:
        print()
        print(step)
        print()
        step()
        print()
      
###############################################################################

def STEP_tokens_per_conjecture():
    cids = np.load('../../data/subset_conjecture_ids.npy')
    with Holstep.Setup() as db:
        sql = 'SELECT Id, Tokens FROM Conjecture ORDER BY Id'
        exprs = db.ex_many(sql)
        exprs = [a[1] for a in exprs if a[0] in cids]
        
        parser = HolstepTokenizer()
        results = []
        for i, e in enumerate(exprs):
            print(i)
            results.append([t.token for t in parser.parse(e) if t.kind == 'FUN'])
        dump_data('../../data/conjecture_tokens_per.data', results)
        
def STEP_unique_tokens():
    cts = load_data('../../data/conjecture_tokens_per.data')
    all_tokens = []
    for c in cts:
        for t in c:
            all_tokens.append(t)
        
    counts = Counter(all_tokens)
    tokens = [t for t, c in counts.items() if c > TOKEN_USAGE_LOWER_BOUND]

    dump_data('../../data/conjecture_tokens.data', tokens)
    print(tokens)
    print(len(tokens))
    
    tokens_map = {t: i for i, t in enumerate(tokens)}
    dump_data('../../data/conjecture_tokens_id_map.data', tokens_map)
        
###############################################################################

main()
