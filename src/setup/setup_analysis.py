import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import sys
import glob
from collections import Counter
sys.path.append('..')
from data import load_data

coords = np.load('../../data/subset_conjecture_coords.npy')
counts = [np.sum(np.abs(c)) for c in coords]
plt.figure()
plt.title('Premise Use Histogram')
sns.countplot(counts)
print("zeros: {}".format(sum([1 if x == 0 else 0 for x in counts])))

print()
print()

cts = load_data('../../data/model/train_conjecture_unique_tokens.data')     
counts = list(cts.values())
plt.figure()
plt.title('Conjecture Token Occurrences Histogram')
sns.countplot(counts)

cts = load_data('../../data/model/train_premise_unique_tokens.data')     
counts = list(cts.values())
plt.figure()
plt.title('Premise Token Occurrences Histogram')
sns.countplot(counts)

print()
print()

def iter_premise_subtrees():   
    for f in glob.glob('../../data/model/train_premise_subtrees_0*'):
        trees = load_data(f)
        print(f)
        for t in trees:
            yield t

cts = Counter([layers for a, b, c, d, e, f, layers in iter_premise_subtrees()])
print(cts.most_common(100))
