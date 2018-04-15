# _*_ coding: utf-8 _*_
import time
from datetime import datetime
import argparse
import functools

import numpy as np
import matplotlib.pyplot as plt

from sklearn import datasets
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.cluster import MiniBatchKMeans
from sklearn.cluster import AffinityPropagation
from sklearn.cluster import MeanShift
from sklearn.cluster import estimate_bandwidth
from sklearn.metrics.pairwise import pairwise_distances_argmin
from sklearn.neighbors import kneighbors_graph
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import DBSCAN


###########
# dataset #
###########
def datasets_factory(dataset_name):
    dataset_map = {
        'iris': datasets.load_iris()
    }

    return dataset_map[dataset_name]


###########################
# dimensionally reduction #
###########################
def compute_pca(X, n_components=2):
    pca = PCA(n_components)

    return pca, pca.fit(X).transform(X)


def pca_plot(X, y, lw):
    plt.figure()
    for i in range(len(set(y))):
        plt.scatter(X[y == i, 0], X[y == i, 1], alpha=.8, lw=lw,)
    plt.legend(loc='best', shadow=False, scatterpoints=1)
    plt.title('PCA of IRIS dataset')
    plt.show()


#######################
# clustering function #
#######################
def clustering_k_means(X,
                         n_clusters,
                         init='k-means++',
                         n_init=10):
    t0 = time.time()
    k_means = KMeans(n_clusters).fit(X)
    k_means_time = time.time() - t0
    print('k_means_time:', k_means_time)
    k_means_cluster_centers = np.sort(k_means.cluster_centers_, axis=0)
    k_means_label = pairwise_distances_argmin(X, k_means_cluster_centers)

    return k_means, k_means_cluster_centers, k_means_label


def clustering_minibatch_k_means(X,
                                    n_clusters,
                                    batch_size,
                                    init='k-means++',
                                    n_init=10,
                                    max_no_improvement=10,
                                    verbose=0):

    mbk = MiniBatchKMeans(n_clusters=n_clusters,
                          batch_size=batch_size,
                          init=init,
                          n_init=n_init,
                          max_no_improvement=max_no_improvement,
                          verbose=verbose)
    t0 = time.time()
    mbk.fit(X)
    mbk_time = time.time() - t0
    print('minibatch_k_means_time:', mbk_time)

    mbk_means_cluster_centers = np.sort(mbk.cluster_centers_, axis=0)
    mbk_means_label = pairwise_distances_argmin(X, mbk_means_cluster_centers)

    return mbk.fit(X), mbk_means_cluster_centers, mbk_means_label


def clustering_affinitypropagation(X):
    t0 = time.time()
    af = AffinityPropagation(preference=-50).fit(X)
    af_time = time.time() - t0
    print('affinitypropagation_time', af_time)
    
    cluster_center_indices = af.cluster_centers_indices_
    labels = af.labels_

    print('n_clusters %s' % len(cluster_center_indices))

    return af, cluster_center_indices, labels


def clustering_mean_shift(X):
    bandwidth = estimate_bandwidth(X, quantile=0.2, n_samples=105)
    ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
    t0 = time.time()
    ms.fit(X)
    ms_time = time.time() - t0
    print('mean_shift_time:', ms_time)
    labels = ms.labels_
    cluster_center = ms.cluster_centers_
    labels_unique = set(labels)
    n_clusters = len(labels_unique)
    print('n_clusters', n_clusters)

    return ms.fit(X), cluster_center, labels


def clustering_hierarchical(X, n_clusters=3, linkage='ward'):
    connectivity=kneighbors_graph(X, n_neighbors=10, include_self=False)
    t0 = time.time()
    ward = AgglomerativeClustering(n_clusters=n_clusters, linkage=linkage).fit(X)
    agg_time = time.time() - t0
    print('hierarchical_time:', agg_time)
    label = ward.labels_

    return ward, label


def clustering_dbscan(X, eps=0.3, min_samples=10,):
    db = DBSCAN(eps=eps, min_samples=min_samples).fit(X)
    labels = db.labels_
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    
    return db, db.labels_, n_clusters_


def clustering_factory(clustering_name,
                        X,
                        n_clusters=None,
                        batch_size=None,
                        eps=None,
                        min_samples=None):
    """ apply clustering function """
    clustering_map = {
        'k_means': clustering_k_means,
        'minibatch_k_means': clustering_minibatch_k_means,
        'affinitypropagation': clustering_affinitypropagation,
        'mean_shift': clustering_mean_shift,
        'hierarchical': clustering_hierarchical,
        'dbscan': clustering_dbscan,
    }

    if clustering_name not in clustering_map:
        raise ValueError('Name of clustering map unknown %s' % clustering_name)
    func = clustering_map[clustering_name]
    @functools.wraps(func)
    def clustering_fn(X, **kwargs):
        if clustering_name == 'k_means':
            return func(X, n_clusters)
        elif clustering_name == 'minibatch_k_means':
            return func(X, n_clusters, batch_size)
        elif clustering_name == 'hierarchical':
            return func(X, n_clusters)
        elif clustering_name == 'dbscan':
            return func(X, eps, min_samples)
        else:
            return func(X)

    return clustering_fn


def cluster_plot(X,
                  clustering_name,
                  prediction,
                  now,
                  dataset_name,
                  n_clusters,
                  centers=None,):
    colors = [plt.cm.jet(each)
                  for each in np.linspace(0, 1, n_clusters)]
    if centers is not None:
        plt.figure()
        for k, col in zip(range(n_clusters), colors):
            my_members = prediction == k
            cluster_center = centers[k]
            plt.plot(X[my_members, 0],
                     X[my_members, 1],
                     'w',
                     markerfacecolor=col,
                     marker='.')
            plt.plot(cluster_center[0],
                     cluster_center[1],
                     'o',
                     markerfacecolor=col,
                     markeredgecolor='k',
                     markersize=6)
    else:
        plt.figure()
        for l in np.unique(prediction):
            plt.scatter(X[prediction == l, 0],
                        X[prediction == l, 1],
                        color=plt.cm.jet(np.float(l) / np.max(prediction + 1)),
                        s=20,
                        edgecolor='k')
    plt.title('clustering_' + str(n_clusters) + '_' + str(clustering_name))
    plt.savefig(str(dataset_name) + '_'
                + str(clustering_name) + '_'
                + str(now) + '.png')
    plt.show()


#################
# main function #
#################
def main(dataset_name,
         clustering_name,
         n_clusters=None,
         batch_size=None,
         eps=None,
         min_samples=None):
    # now ##################################################
    now = datetime.now().strftime('%Y%m%d')

    # load dataset #########################################
    sample = datasets_factory(dataset_name)
    X = sample.data
    # print(X)
    # define variables
    X = sample.data
    y = sample.target
    target_names = sample.target_names

    # dimentioanl reduction ################################
    # compute pca
    pca, X_r = compute_pca(X)
    # plot pca
    lw = 2
    pca_plot(X_r, y, lw)
    # Percentage of variance explained for each components
    print('explained variance ratio (first two components): %s'
          % str(pca.explained_variance_ratio_))

    # clustering ##########################################
    centers = None
    clustering_fn = clustering_factory(clustering_name,
                                       X_r,
                                       n_clusters,
                                       batch_size,
                                       eps,
                                       min_samples)
    print('clustering_fn', clustering_fn)
    if clustering_name == 'k_means':
        compute, centers, prediction = clustering_fn(X_r, n_clusters=n_clusters)
    elif clustering_name == 'hierarchical':
        compute, prediction = clustering_fn(X_r, n_clusters=n_clusters)
    elif clustering_name == 'minibatch_k_means':
        compute, centers, prediction = clustering_fn(
            X_r,
            n_clusters=n_clusters,
            batch_size=batch_size,
        )
    elif clustering_name == 'dbscan':
        compute, prediction, n_clusters = clustering_fn(
            X_r,
            eps=eps,
            min_samples=min_samples
        )
    else:
        compute, centers, prediction = clustering_fn(X_r)
    print('clustering_fn', clustering_fn)
    # plot k_means
    cluster_plot(X_r,
                 clustering_name,
                 prediction,
                 now,
                 dataset_name,
                 n_clusters=n_clusters,
                 centers=centers,)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='clustering sample'
    )
    parser.add_argument('--dataset_name',
                        dest='dataset_name',
                        default=None,
                        type=str,
                        nargs=1,
                        help='enter dataset name')
    parser.add_argument('--clustering_name',
                        dest='clustering_name',
                        default=None,
                        type=str,
                        nargs=1,
                        help='enter clustering name')
    parser.add_argument('--n_clusters',
                        dest='n_clusters',
                        default=0,
                        type=int,
                        nargs='?',
                        help='define number of cluster when using k_means')
    parser.add_argument('--batch_size',
                        dest='batch_size',
                        default=0,
                        type=int,
                        nargs='?',
                        help='define batch size when using minibatch_k_means')
    parser.add_argument('--eps',
                        dest='eps',
                        default=0,
                        type=float,
                        nargs='?',
                        help='dbscan density parameter')
    parser.add_argument('--min_samples',
                        dest='min_samples',
                        default=0,
                        type=int,
                        nargs='?',
                        help='dbscan density parameter')
    argv = parser.parse_args()
    # main
    main(argv.dataset_name[0],
         argv.clustering_name[0],
         argv.n_clusters,
         argv.batch_size,
         argv.eps,
         argv.min_samples)
