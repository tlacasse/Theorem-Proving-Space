import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from collections import Counter
import sys
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

cts = load_data('../../data/conjecture_tokens_per.data')
all_tokens = []
for c in cts:
    for t in c:
        all_tokens.append(t)
        
counts = list(Counter(all_tokens).values())

plt.figure()
plt.title('Token Occurence Histogram')
sns.countplot(counts)
