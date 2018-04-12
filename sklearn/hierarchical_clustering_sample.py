# _*_ coding: utf-8 _*_
import time as time
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
from sklearn.cluster import AgglomerativeClustering
from sklearn.datasets.samples_generator import make_swiss_roll


n_samples = 1500
noise = 0.05
X, _ = make_swiss_roll(n_samples, noise)
X[:, 1] *= .5

################################################################
# computing clustering
print('compute unstructured hierarchical clustering...')
st = time.time()
ward = AgglomerativeClustering(n_clusters=6, linkage='ward').fit(X)
elapsed_time = time.time() - st
label = ward.labels_
print('Elapsed time: %.2fs' % elapsed_time)
print('Number of points: %i' % label.size)

################################################################
# plot result
fig = plt.figure()
ax = p3.Axes3D(fig)
ax.view_init(7, -80)
for l in np.unique(label):
    ax.scatter(X[label == l, 0],
               X[label == l, 1],
               X[label == l, 2],
               color=plt.cm.jet(np.float(l) / np.max(label + 1)),
               s=20,
               edgecolor='k')
    plt.title('without connectivity constrains (time %.2fs)' % elapsed_time)

################################################################
# define the structure A of the data. here a 10 nearest neighbors
from sklearn.neighbors import kneighbors_graph
connectivity = kneighbors_graph(X, n_neighbors=10, include_self=False)

################################################################
# computing clustering
print('compute structured hierarchical clustering...')
st = time.time() - st
ward = AgglomerativeClustering(
    n_clusters=6,
    connectivity=connectivity,
    linkage='ward'
)
ward = ward.fit(X)
elapsed_time = time.time() - st
label = ward.labels_
print('Elapsed time: %.2fs' % elapsed_time)
print('Number of points: %i' % label.size)

################################################################
# plot result
fig = plt.figure()
ax = p3.Axes3D(fig)
ax.view_init(7, -80)
for l in np.unique(label):
    ax.scatter(X[label == l, 0],
               X[label == l, 1],
               X[label == l, 2],
               color=plt.cm.jet(float(l) / np.max(label + 1)),
               s=20,
               edgecolor='k')
plt.title('with connectivity constraints (time %.2f)' % elapsed_time)
plt.show()
