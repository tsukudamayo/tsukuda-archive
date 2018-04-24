# _*_ coding: utf-8 _*_
import matplotlib as mpl
import matplotlib.pyplot as plt

import numpy as np

from sklearn import datasets
from sklearn.mixture import GaussianMixture
from sklearn.model_selection import StratifiedKFold


colors = ['navy', 'turquoise', 'darkorange']


def make_ellipses(gmm, ax):
    return 


iris = datasets.load_iris()


skf = StratifiedKFold(n_splits=4)
train_index, test_index = next(iter(skf.split(iris.data, iris.target)))

X_train = iris.data[train_index]
y_train = iris.target[train_index]
X_test = iris.data[test_index]
y_test = iris.target[test_index]

print(X_train)
print(y_train)
print(X_test)
print(y_test)

n_classes = len(np.unique(y_train))
print(n_classes)

estimators = dict(
    (cov_type, GaussianMixture(
        n_components=n_classes,
        covariance_type=cov_type,
        max_iter=20,
        random_state=0))
        for cov_type in ['spherical', 'diag', 'tied', 'full']
)

n_estimators = len(estimators)
print('n_estimators', n_estimators)

plt.figure(figsize=(3*n_estimators // 2, 6))
plt.subplots_adjust(bottom=.01,
                    top=0.95,
                    hspace=.15,
                    wspace=.05,
                    left=.01,
                    right=.99)

for index, (name, estimator) in enumerate(estimators.items()):
    estimator.means_init = np.array([X_train[y_train == i].mean(axis=0)
                                    for i in range(n_classes)])
    print('estimator.means_init', estimator.means_init)
    estimator.fit(X_train)
    print('estimator.fit(X_train)', estimator.fit(X_train))

    h = plt.subplot(2, n_estimators // 2, index+1)
    print('h=plt.subplot', h)
    make_ellipses(estimator, h)
    print('make_ellipses(estimator, h)', make_ellipses(estimator, h))

    for n, color in enumerate(colors):
        print('n', n)
        print('color', color)
        data = iris.data[iris.target == n]
        plt.scatter(data[:, 0],
                    data[:, 1],
                    s=0.8,
                    color=color,
                    label=iris.target_names[n])
        print(plt.scatter(data[:, 0],
                    data[:, 1],
                    s=0.8,
                    color=color,
                    label=iris.target_names[n]))
    for n, color in enumerate(colors):
        data = X_test[y_test == n]
        print('data', data)
        print('data[:, 0]', len(data[:, 0]))
        print('data[:, 1]', len(data[:, 1]))
        plt.scatter(data[:, 0],
                   data[:, 1],
                   marker='x',
                   color=color)
        print(plt.scatter(data[:, 0],
                   data[:, 1],
                   marker='x',
                   color=color))

    y_train_pred = estimator.predict(X_train)
    print('y_train_pred', y_train_pred)
    train_accuracy = np.mean(y_train_pred.ravel() == y_train.ravel()) * 100
    print('train_accuracy', train_accuracy)

    plt.text(0.05, 0.9, 'Train accuracy: &.1f' % train_accuracy,
             transform=h.transAxes)
    print(plt.text(0.05, 0.9, 'Train accuracy: &.1f' % train_accuracy,
             transform=h.transAxes))

    y_test_pred = estimator.predict(X_test)
    print('y_test_pred', y_test_pred)
    test_accuracy = np.mean(y_test_pred.ravel() == y_test.ravel()) * 100
    print('test_accuracy', test_accuracy)

    plt.xticks(())
    plt.yticks(())
    plt.title(name)

plt.legend(scatterpoints=1, loc='lower right', prop=dict(size=12))
plt.show()
        

