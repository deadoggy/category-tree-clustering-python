#coding:utf-8

import numpy as np
import sklearn

def calculate_centers(data, y_labels):
    '''
        calculate centers of every data obj's partition, only support vector type

        @data: list, shape: [n_samples, n_features]
        @y_labels: list, shape: [n_samples, 1]

        #return: list, shape:[n_samples, n_features]
    '''

    n_cls = len(set(y_labels)) - (1 if -1 in y_labels else 0)
    n_features = len(data[0])
    centers = np.array([[0.0 for f in xrange(n_features)] for c in xrange(n_cls)])
    for i, d in enumerate(data):
        label = y_labels[i]
        centers[label] += np.add(centers[label], d)
    cen_size = np.array([ [len(centers[i]) if len(centers[i])!=0 else 1] for i in xrange(n_cls) ])
    centers /= cen_size
    return np.array([ centers[y_labels[i]] for i in xrange(len(y_labels)) ])


def ssw(data, y_labels):
    '''
        calculate ssw of clustering results, only support vector type

        @data: list, shape: [n_samples, n_features]
        @y_labels: list, shape: [n_samples, 1]

        #return ssw
    '''
    centers = calculate_centers(data, y_labels)
    ssw = 0.0
    for i, d in enumerate(data):
        ssw += np.sqrt(np.sum((d-centers[i])**2))
    return ssw / len(data)





