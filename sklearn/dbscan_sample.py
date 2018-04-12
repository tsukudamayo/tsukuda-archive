# _*_ coding: utf-8 _*_
import numpy as np

from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler


################################################################
# generate sample data
centers = [[1, 1], [-1, -1], [1, -1]]
X, labels_true = make_blobs(n_samples=750,
                            centers=centers,
                            cluster_std=0.4,
                            random_state=0)
print('X', X)
print(X.shape)
X = StandardScaler().fit_transform(X)
print('X_StandardScalar().fit_transform(X)', X)
print(X.shape)

################################################################
# compute DBSCAN
db = DBSCAN(eps=0.1, min_samples=10).fit(X)
print('db.labels_.shape', db.labels_.shape)
core_sample_mask = np.zeros_like(db.labels_, dtype=bool)
# print('core_sample_mask = np.zeros_like(db.labels_, dtype=bool)', core_sample_mask)
core_sample_mask[db.core_sample_indices_] = True
# print('core_sample_mask[db.core_sample_indices_] = True', core_sample_mask)
labels = db.labels_
print('labels', labels)
print('len(set(labels))', len(set(labels)))

# number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

print('estimated number of clusters: %d' % n_clusters_)
print('Homogenety: %0.3f' % metrics.homogeneity_score(labels_true, labels))
print('Completeness: %0.3f' % metrics.completeness_score(labels_true, labels))
print('V-measure: %0.3f' % metrics.v_measure_score(labels_true, labels))
print('Adjust Radn Index: %0.3f' % metrics.adjusted_rand_score(labels_true, labels))
print('Adjust Mutual Information: %0.3f' % metrics.adjusted_mutual_info_score(labels_true, labels))
print('Silhouette Coefficient: %0.3f' % metrics.silhouette_score(X, labels))

################################################################
# plot result
import matplotlib.pyplot as plt

# black removed and is used for noise instead.
unique_labels = set(labels)
colors = [plt.cm.Spectral(each)
              for each in np.linspace(0, 1, len(unique_labels))]
for k, col in zip(unique_labels, colors):
    if k == -1:
        # black used for noise
        col = [0, 0, 0, 1]
    class_member_mask = (labels == k)

    xy = X[class_member_mask & core_sample_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
             markeredgecolor='k', markersize=14)

    xy = X[class_member_mask & ~core_sample_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
             markeredgecolor='k', markersize=6)

plt.title('estimated number of clusters: %d' % n_clusters_)
plt.show()
