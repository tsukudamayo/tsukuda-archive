# _*_ coding: utf-8 _*_p
import logging
from time import time

from numpy.random import RandomState
import matplotlib.pyplot as plt

from sklearn.datasets import fetch_olivetti_faces
from sklearn.cluster import MiniBatchKMeans
from sklearn import decomposition


n_row, n_col = 2, 3
print('n_row', n_row)
print('n_col', n_col)
n_components = n_row * n_col
print('n_components', n_components)
image_shape = (64, 64)
rng = RandomState(0)


def plot_gallery(title, images, n_col=n_col, n_row=n_row):
    plt.figure(figsize=(2. * n_col, 2.26 * n_row))
    plt.suptitle(title, size=16)
    for i, comp in enumerate(images):
        plt.subplot(n_row, n_col, i+1)
        vmax = max(comp.max(), -comp.min())
        plt.imshow(comp.reshape(image_shape),
                   cmap=plt.cm.gray,
                   interpolation='nearest',
                   vmin=-vmax,
                   vmax=vmax)
        plt.xticks(())
        plt.yticks(())
    plt.subplots_adjust(0.01, 0.05, 0.99, 0.93, 0.04, 0.)


# display progress log on stdout
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(Levelname)s %(message)s')


################################################################
# load faces data
dataset = fetch_olivetti_faces(shuffle=True, random_state=rng)
faces = dataset.data
print('faces/shppe', faces.shape)

n_samples, n_features = faces.shape

# flobal centering
faces_centered = faces - faces.mean(axis=0)
print('faces_centered/face - faces.mean(axis=0)', faces_centered)

# local centering
faces_centered -= faces_centered.mean(axis=1).reshape(n_samples, -1)
print('faces_centered/faces_centered.mean(axis=1).reshape(n_samples, -1)',
      faces_centered)

print('Dataset consists of %d faces' % n_samples)


################################################################
# list of the different estimators, whether to center and transpose the
# problem, and whether the transformer usesdec the clustering API.
estimators = [
    ('Eigenfaces - PCA using randomized SVD',
     decomposition.PCA(n_components=n_components,
                       svd_solver='randomized',
                       whiten=True),
     True),
    ('Non-negative components - NMF',
     decomposition.NMF(n_components=n_components,
                       init='nndsvda',
                       tol=5e-3),
     False),
    ('Independent components - FastICA',
     decomposition.FastICA(n_components=n_components, whiten=True),
     True),
    ('Sparse comp. - MiniBatchSparsePCA',
     decomposition.MiniBatchSparsePCA(n_components=n_components,
                                      alpha=0.8,
                                      n_iter=100,
                                      batch_size=3,
                                      random_state=rng),
     True),
    ('MiniBatchDictionaryLearning',
     decomposition.MiniBatchDictionaryLearning(n_components=15,
                                               alpha=0.1,
                                               n_iter=100,
                                               batch_size=3,
                                               random_state=rng),
     True),
    ('Cluster centers - MiniBatchKMeans',
     MiniBatchKMeans(n_clusters=n_components,
                     tol=1e-3,
                     batch_size=20,
                     max_iter=50,
                     random_state=rng),
     True),
    ('Factor Analysis components - FA',
     decomposition.FactorAnalysis(n_components=n_components,
                                  max_iter=2),
     True),
]

################################################################
# plot a sample of the input data

print('faces_centered[:n_components]', faces_centered[:n_components])
print('faces_centered[:n_components]/shape', faces_centered[:n_components].shape)
plot_gallery('First centered Olivetti faces', faces_centered[:n_components])

################################################################
# do the estimation and plot it

for name, estimator, centers in estimators:
    print('Extracting the top %d %s...' %(n_components, name))
    t0 = time()
    data = faces
    if centers:
        data = faces_centered
    estimator.fit(data)
    train_time = (time() - t0)
    print('done in %0.3fs' % train_time)
    if hasattr(estimator, 'cluster_centers_'):
        components_ = estimator.cluster_centers_
    else:
        components_ = estimator.components_

    if (hasattr(estimator, 'noise_variance_') and
            estimator.noise_variance_.ndim > 0):
        plot_gallery('Pixelwise variance',
                     estimator.noise_variance_.reshape(1, -1),
                     n_col=1,
                     n_row=1)
    plot_gallery('%s - Train time %.1fs' % (name, train_time),
                 components_[:n_components])

plt.show()
