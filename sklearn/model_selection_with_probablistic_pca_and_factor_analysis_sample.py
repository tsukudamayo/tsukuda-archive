# _*_ coding: utf-8 _*_
import numpy as np
import matplotlib.pyplot as plt
from scipy import linalg

from sklearn.decomposition import PCA, FactorAnalysis
from sklearn.covariance import ShrunkCovariance, LedoitWolf
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV


################################################################
# create the data
n_samples, n_features, rank = 1000, 50, 10
sigma = 1.
rng = np.random.RandomState(42)
U, _, _ = linalg.svd(rng.randn(n_features, n_features))
X = np.dot(rng.randn(n_samples, rank), U[:, :rank].T)

# Adding homoscedastic noise
X_homo = X + sigma * rng.randn(n_samples, n_features)

# Adding heteroscedestic noise
sigmas = sigma * rng.randn(n_features) * sigma / 2.
X_hetero = X + rng.randn(n_samples, n_features) * sigmas

################################################################
# Fit the models
n_components = np.arange(0, n_features, 5)

def compute_scores(X):
    pca = PCA(svd_solver='full')
    fa = FactorAnalysis()

    pca_scores, fa_scores = [], []
    for n in n_components:
        pca.n_components = n
        fa.n_components = n
        pca_scores.append(np.mean(cross_val_score(pca, X)))
        fa_scores.append(np.mean(cross_val_score(fa, X)))

    return pca_scores, fa_scores


def shurnk_cov_score(X):
    shrinkages = np.logspace(-2, 0, 30)
    cv = GridSearchCV(ShrunkCovariance(), {'shrinkage': shrinkages})

    return np.mean(cross_val_score(cv.fit(X).best_estimator_, X))


def lw_score(X):
    return np.mean(cross_val_score(LedoitWolf(), X))


for X, title in [(X_homo, 'Homoscedastic Noise'), (X_hetero, 'Heteroscedastic Noise')]:
    pca_scores, fa_scores = compute_scores(X)
    n_components_pca = n_components[np.argmax(pca_scores)]
    n_components_fa = n_components[np.argmax(fa_scores)]

    pca = PCA(svd_solver='full', n_components='mle')
    pca.fit(X)
    n_components_pca_mle = pca.n_components_

    print('best n_components by PCA CV = %d' % n_components_pca)
    print('best n_components by FA  CV = %d' % n_components_fa)
    print('best n_components by PCA MLE = %d' % n_components_pca_mle)

    plt.figure()
    plt.plot(n_components, pca_scores, 'b', label='PCA scores')
    plt.plot(n_components, fa_scores,  'r', label='FA scores')
    plt.axvline(rank, color='g', label='TRUTH: %d' % rank, linestyle='--')
    plt.axvline(n_components_fa,
                color='r',
                label='FA CV: %d' % n_components_pca,
                linestyle='--')
    plt.axvline(n_components_pca_mle,
                color='k',
                label='PCA MLE: %d' % n_components_pca_mle,
                linestyle='--')

    # compare with other covariance estimator
    plt.axvline(shurnk_cov_score(X),
                color='violet',
                label='Shurnk Covariance MLE', linestyle='-.')
    plt.axvline(lw_score(X),
                color='orange',
                label='LedoitWorf MLE' % n_components_pca_mle,
                linestyle='-.')
    plt.xlabel('nb of components')
    plt.xlabel('CV scores')
    plt.legend(loc='lower right')
    plt.title(title)

plt.show()
    
