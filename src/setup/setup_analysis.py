import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

coords = np.load('../../data/subset_conjecture_coords.npy')
counts = [np.sum(np.abs(c)) for c in coords]
print(counts)
plt.figure()
sns.countplot(counts)
print("zeros: {}".format(sum([1 if x == 0 else 0 for x in counts])))
