# _*_ coding: utf-8 _*_
import time
import argparse
import functools

import numpy as np
import matplotlib.pyplot as plt

from sklearn.datasets import load_iris

from sklearn.decomposition import PCA
from sklearn.decomposition import IncrementalPCA
from sklearn.decomposition import NMF
from sklearn.decomposition import FastICA
from sklearn.decomposition import MiniBatchSparsePCA
from sklearn.decomposition import MiniBatchDictionaryLearning
from sklearn.decomposition import FactorAnalysis
from sklearn.decomposition import KernelPCA

from sklearn.cluster import MiniBatchKMeans


####################
# dataset function #
####################


######################
# decompose function #
######################
def decompose_pca(X, n_components):
    pca = PCA(n_components=n_components)
    X_pca = pca.fit_transform(X)
    print('pca', pca)
    print('pca/fit', pca.fit(X))
    print('pca/fit_transform', pca.fit_transform(X))
    
    return X_pca

def decompose_incremental_pca(X, n_components, batch_size=10):    
    ipca = IncrementalPCA(n_components=n_components, batch_size=batch_size)
    X_ipca = ipca.fit_transform(X)
    print('incremental_pca', ipca)
    print('ipca/fit', ipca.fit(X))
    print('ipca/fit_transform', ipca.fit_transform(X))
    
    return X_ipca

def decompose_nmf(X, n_components, init='nndsvda', tol=5e-3):
    nmf = NMF(n_components=n_components, init=init, tol=tol)
    X_nmf = nmf.fit_transform(X)

    return X_nmf


def decompose_fast_ica(X, n_components, whiten=True):
    fast_ica = FastICA(X, n_components=n_components, whiten=whiten)
    X_fast_ica = fast_ica.fit_transform(X)

    return X_fast_ica


def decompose_minibatch_sparse_pca(X,
                                      n_components,
                                      alpha=0.8,
                                      n_iter=100,
                                      batch_size=3,
                                      random_state=np.random.RandomState(42)):
    minibatch_sparse_pca = MiniBatchSparsePCA(n_components=n_components,
                                              alpha=alpha,
                                              n_iter=n_iter,
                                              batch_size=batch_size,
                                              random_state=random_state,)
    X_minibatch_sparse_pca = minibatch_sparse_pca.fit_transform(X)

    return X_minibatch_sparse_pca


def decompose_minibatch_kmeans(X,
                                  n_components,
                                  tol=1e-3,
                                  batch_size=20,
                                  max_iter=50,
                                  random_state=np.random.RandomState(42)):
    minibatch_k_means = MiniBatchKMeans(n_components=n_clusters,
                                        tol=tol,
                                        batch_size=batch_size,
                                        max_iter=max_iter,
                                        random_state=random_state,)
    X_minibatch_k_means = minibatch_k_means.fit_transform(X)

    return X_minibatch_k_means


def decompose_factor_analysis(X, n_components, max_iter=2):
    factor_analysis = FactorAnalysis(n_components=n_components, max_iter=max_iter)
    X_factor_analysis = factor_analysis.fit_transform(X)

    return X_factor_analysis


def decompose_kernel_pca(X,
                           n_components=None,
                           kernel='rbf',
                           fit_inverse_transform=True,
                           gamma=10):
    kpca = KernelPCA(kernel=kernel,
                     fit_inverse_transform=fit_inverse_transform,
                     gamma=gamma)
    X_kpca = kpca.fit_transform(X)

    return X_kpca


def decomposing_factory(decomposing_name,
                          X,
                          n_components,
                          batch_size=None,
                          init=None,
                          tol=None,
                          whiten=None):
    decomposing_map = {
        'pca': decompose_pca,
        'incremental_pca': decompose_incremental_pca,
        'nmf': decompose_nmf,
        'fast_ica': decompose_fast_ica,
        'minibatch_sparse_pca': decompose_minibatch_sparse_pca,
        'minibatch_kmeans': decompose_minibatch_kmeans,
        'factor_analysis': decompose_factor_analysis,
        'kernel_pca': decompose_kernel_pca,
    }

    if decomposing_name not in decomposing_map:
        raise ValueError('Name of decomposing map unknown %s' % decomposing_name)
    func = decomposing_map[decomposing_name]
    @functools.wraps(func)
    def decomposing_fn(X, n_components, **kwargs):
        if decomposing_name == 'pca':
            return func(X, n_components)
        elif decomposing_name == 'incremental_pca':
            return func(X, n_components, batch_size=batch_size)
        elif decomposing_name == 'nmf':
            return func(X, n_components, init=init, tol=tol)
        elif decomposing_name == 'fast_ica':
            return func(X, n_components, whiten=whiten)
        else:
            ValueError('invalie argument %s' % decomposing_name)

    return decomposing_fn


#################
# main function #
#################
def main(decomposing_name,
          batch_size,
          init,
          tol,
          whiten,):
    colors = ['navy', 'turquoise', 'darkorange']

    n_components = 2

    iris = load_iris()
    X = iris.data
    y = iris.target

    print('batch_size', batch_size)
    print('init', init)
    print('tol', tol)
    print('whiten', whiten)
    decomposing_fn = decomposing_factory(decomposing_name,
                                         X,
                                         n_components,
                                         batch_size=batch_size,
                                         init=init,
                                         tol=tol,
                                         whiten=whiten,)
    print('decomposing_fn', decomposing_fn)
    if decomposing_name == 'pca':
        X_transformed = decomposing_fn(X, n_components)
    elif decomposing_name == 'incremental_pca':
        X_transformed = decomposing_fn(X, n_components, batch_size=batch_size)
    elif decomposing_name == 'nmf':
        X_transformed = decomposing_fn(X, n_components, init=init, tol=tol)
    elif decomposing_name == 'fast_ica':
        X_transformed = decomposing_fn(X, n_components, whiten=whiten)
    else:
        ValueError('invalid argument %s' % decomposing_name)
    
    plt.figure()
    for color, i, target_name in zip(colors, [0, 1, 2], iris.target_names):
        plt.scatter(X_transformed[y == i, 0],
                    X_transformed[y == i, 1],
                    color=color,
                    lw=2,
                    label=target_name)
    plt.title(str(decomposing_name) + ' of iris dataset')
    plt.legend(loc='best', shadow=False, scatterpoints=1)
    
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='dimentionally reduction sample'
    )
    parser.add_argument('--decomposing_name',
                        dest='decomposing_name',
                        nargs=1,
                        default=None,
                        type=str,
                        help='pca, incremental_pca, nmf, fast_ica,'
                             'minibatch_sparse_pca, minibatch_kmeans,'
                             'factor_analysis, kernel_pca')
    parser.add_argument('--batch_size',
                        dest='batch_size',
                        nargs='?',
                        default=10,
                        type=int,
                        help='specified batch size when using batch_size')
    parser.add_argument('--init',
                        dest='init',
                        nargs='?',
                        default='nndsvda',
                        type=str,
                        help='specified nmf init parameter')
    parser.add_argument('--tol',
                        dest='tol',
                        nargs='?',
                        default=5e-3,
                        type=float,
                        help='specified nmf tol parmeter')
    parser.add_argument('--whiten',
                        dest='whiten',
                        nargs='?',
                        default=True,
                        type=bool,
                        help='specified fast_ica parameter')
    argv = parser.parse_args()

    # main
    main(argv.decomposing_name[0],
         argv.batch_size,
         argv.init,
         argv.tol,
         argv.whiten,)
