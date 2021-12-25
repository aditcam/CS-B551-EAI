# k_nearest_neighbors.py: Machine learning implementation of a K-Nearest Neighbors classifier from scratch.
#
# Submitted by: [enter your full name here] -- [enter your IU username here]
#
# Based on skeleton code by CSCI-B 551 Fall 2021 Course Staff

import numpy as np
from sklearn import neighbors
from utils import euclidean_distance, manhattan_distance


class KNearestNeighbors:
    """
    A class representing the machine learning implementation of a K-Nearest Neighbors classifier from scratch.

    Attributes:
        n_neighbors
            An integer representing the number of neighbors a sample is compared with when predicting target class
            values.

        weights
            A string representing the weight function used when predicting target class values. The possible options are
            {'uniform', 'distance'}.

        _X
            A numpy array of shape (n_samples, n_features) representing the input data used when fitting the model and
            predicting target class values.

        _y
            A numpy array of shape (n_samples,) representing the true class values for each sample in the input data
            used when fitting the model and predicting target class values.

        _distance
            An attribute representing which distance metric is used to calculate distances between samples. This is set
            when creating the object to either the euclidean_distance or manhattan_distance functions defined in
            utils.py based on what argument is passed into the metric parameter of the class.

    Methods:
        fit(X, y)
            Fits the model to the provided data matrix X and targets y.

        predict(X)
            Predicts class target values for the given test data matrix X using the fitted classifier model.
    """

    def __init__(self, n_neighbors = 5, weights = 'uniform', metric = 'l2'):
        # Check if the provided arguments are valid
        if weights not in ['uniform', 'distance'] or metric not in ['l1', 'l2'] or not isinstance(n_neighbors, int):
            raise ValueError('The provided class parameter arguments are not recognized.')

        # Define and setup the attributes for the KNearestNeighbors model object
        self.n_neighbors = n_neighbors
        self.weights = weights
        self._X = None
        self._y = None
        self._distance = euclidean_distance if metric == 'l2' else manhattan_distance

    def fit(self, X, y):
        """
        Fits the model to the provided data matrix X and targets y.

        Args:
            X: A numpy array of shape (n_samples, n_features) representing the input data.
            y: A numpy array of shape (n_samples,) representing the true class values for each sample in the input data.

        Returns:
            None.
        """
        self._X = X
        self._y = y

        return

        # raise NotImplementedError('This function must be implemented by the student.')

    def predict(self, X):
        """
        Predicts class target values for the given test data matrix X using the fitted classifier model.

        Args:
            X: A numpy array of shape (n_samples, n_features) representing the test data.

        Returns:
            A numpy array of shape (n_samples,) representing the predicted target class values for the given test data.
        """

        predicted_class = []
        if self.weights == 'uniform':
            for i in range(np.shape(X)[0]):
                distance = []
                for j in range(np.shape(self._X)[0]):
                    distance.append(self._distance(X[i],self._X[j]))

                # Ref : https://stackoverflow.com/questions/34226400/find-the-index-of-the-k-smallest-values-of-a-numpy-array
                idx = np.argpartition(np.array(distance),self.n_neighbors)
                neighbor_classes = self._y[idx[:self.n_neighbors]]
                # Ref : https://www.geeksforgeeks.org/find-the-most-frequent-value-in-a-numpy-array/
                predicted_class.append(np.bincount(neighbor_classes).argmax()) # the smallest value will be taken if there is a tie case of an even number of k or if there are classes having the same number of nearest neighbours

            result = np.array(predicted_class)
            return result

        elif self.weights == 'distance':
            for i in range(np.shape(X)[0]):
                distance = []
                for j in range(np.shape(self._X)[0]):
                    dist = self._distance(X[i],self._X[j])
                    if dist != 0:
                        distance.append(1/dist)
                    else :
                        distance.append(np.inf)
                temp_dict = {}
                for p in range(np.min(self._y),np.max(self._y)+1):
                    temp_dict[p]=0 
                for p in range(np.shape(self._X)[0]):
                    temp_dict[self._y[p]]+=distance[p]
                
                # Ref : https://www.geeksforgeeks.org/python-get-key-with-maximum-value-in-dictionary/
                maxkey = max(zip(temp_dict.values(), temp_dict.keys()))[1]
                predicted_class.append(maxkey)

            result = np.array(predicted_class)
            return result  

        # raise NotImplementedError('This function must be implemented by the student.')
