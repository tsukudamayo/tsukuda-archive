# _*_ coding: utf-8 _*_
import unittest
import clustering

import numpy as np
from sklearn import datasets


class TestSweet(unittest.TestCase):

    def test_datasets_factory(self):
        expected_data = (150, 4)
        expected_target = (150,)
        expected_target_names = 3
        result = clustering.datasets_factory('iris')
        self.assertTupleEqual(expected_data, result.data.shape)
        self.assertTupleEqual(expected_target, result.target.shape)
        self.assertEqual(expected_target_names, len(result.target_names))

    def test_compute_pca(self):
        test_data = datasets.load_iris()
        test_X = test_data.data
        expected_X = (150, 2)
        _, result_X = clustering.compute_pca(test_X, 2)
        self.assertTupleEqual(expected_X, result_X.shape)

    def test_clustering_k_means(self):
        test_data = datasets.load_iris()
        test_X = test_data.data
        _, test_X =clustering.compute_pca(test_X, 2)
        expected_center = (3, 2)
        expected_prediciton = 150
        cluster, center, prediction = clustering.clustering_k_means(
            test_X,
            3,
        )
        self.assertTupleEqual(expected_center, center.shape)
        self.assertEqual(expected_prediciton, len(prediction))

    def test_clustering_minibatch_k_means(self):
        test_data = datasets.load_iris()
        test_X = test_data.data
        _, test_X = clustering.compute_pca(test_X, 2)
        expected_center = (3, 2)
        expected_prediciton = 150
        cluster, center, prediction = clustering.clustering_minibatch_k_means(
            test_X,
            3,
            10
        )
        self.assertTupleEqual(expected_center, center.shape)
        self.assertEqual(expected_prediciton, len(prediction))

    def test_clustering_affinitypropagation(self):
        test_data = datasets.load_iris()
        test_X = test_data.data
        _, test_X = clustering.compute_pca(test_X, 2)
        expected_center = (3,)
        expected_prediciton = 150
        cluster, center, prediction = clustering.clustering_affinitypropagation(
            test_X,
        )
        print('clustering_affinitypropagation/center', center)
        print('clustering_affinitypropagation/prediction', prediction)
        self.assertTupleEqual(expected_center, center.shape)
        self.assertEqual(expected_prediciton, len(prediction))

    def test_clustering_mean_shift(self):
        test_data = datasets.load_iris()
        test_X = test_data.data
        _, test_X = clustering.compute_pca(test_X, 2)
        expected_center = (3, 2)
        expected_prediciton = 150
        cluster, center, prediction = clustering.clustering_mean_shift(
            test_X,
        )
        print('clustering_mean_shift/center', center)
        print('clustering_mean_shift/prediction', prediction)
        self.assertTupleEqual(expected_center, center.shape)
        self.assertEqual(expected_prediciton, len(prediction))

    def test_clustering_hieralchical_clustering(self):
        test_data = datasets.load_iris()
        test_X = test_data.data
        _, test_X = clustering.compute_pca(test_X, 2)
        expected_center = (3, 2)
        expected_prediciton = 150
        ward = clustering.clustering_hieralchical_clustering(

    def test_clustering_factory(self):
        clustering_names = [
            'k_means', 'minibatch_k_means', 'affinitypropagation'
        ]
        n_clusters = 3
        batch_size = 10
        test_data = datasets.load_iris()
        test_X = test_data.data
        _, test_X = clustering.compute_pca(test_X, 2)
        for clustering_name in clustering_names:
            clustering_fn = clustering.clustering_factory(clustering_name,
                                                          test_X,
                                                          n_clusters,
                                                          batch_size)
            if clustering_name == 'k_means':
                cluster, center, prediction = clustering_fn(
                    test_X,
                    n_clusters=n_clusters,
                )
            elif clustering_name == 'minibatch_k_means':
                cluster, center, prediction = clustering_fn(
                    test_X,
                    n_clusters=n_clusters,
                    batch_size=batch_size,
                )
            else:
                cluster, center, prediction = clustering_fn(
                    test_X,
                )
        expected_center = (3, 2)
        expected_prediciton = 150
        self.assertTupleEqual(expected_center, center.shape)
        self.assertTrue = (expected_prediciton, len(prediction))
