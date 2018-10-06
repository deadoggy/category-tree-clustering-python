#coding:utf-8

#reference: WB-index: A sum-of-squares based index for cluster validity

import numpy as np
import sklearn

def calculate_centers(data, y_labels):
    '''
        calculate centers of every data obj's partition, only support vector type

        @data: np.array, shape: [n_samples, n_features]
        @y_labels: np.array, shape: [n_samples, 1]

        #return: list, shape:[n_samples, n_features]
    '''

    n_cls = max(y_labels)+1
    n_features = len(data[0])
    centers = np.array([[0.0 for f in xrange(n_features)] for c in xrange(n_cls)])
    for i, d in enumerate(data):
        label = y_labels[i]
        centers[label] = np.add(centers[label], d)
    cen_size = np.array([ [ y_labels.tolist().count(i) if y_labels.tolist().count(i)!=0 else 1] for i in xrange(n_cls) ])
    centers /= cen_size
    return np.array([ centers[y_labels[i]] for i in xrange(len(y_labels)) ])


def ssw(data, y_labels):
    '''
        calculate ssw of clustering results, only support vector type

        @data: np.array, shape: [n_samples, n_features]
        @y_labels: np.array, shape: [n_samples, 1]

        #return ssw
    '''
    centers = calculate_centers(data, y_labels)
    ssw = 0.0
    for i, d in enumerate(data):
        ssw += np.sqrt(np.sum((d-centers[i])**2))
    return ssw 


def ssb(data, y_labels):
    '''
        calculate ssb of clustering results, only support vector type

        @data: np.array, shape: [n_samples, n_features]
        @y_labels: np.array, shape: [n_samples, 1]

        #return ssb
    '''
    data = np.array(data)
    x_avg = np.sum(data, 0) / float(len(data))
    centers = calculate_centers(data, y_labels)
    ssb = 0.0
    for i, d in enumerate(data):
        if y_labels[i] == -1:
            continue
        c = centers[i]
        ssb += np.sqrt(np.sum((c-x_avg)**2))
    return ssb

#test

data = np.array([ [0.,0.],[0.,0.5],[0.5,0.],[0.5,0.5], [2.,2.],[2.,1.5],[1.5,2.],[1.5,1.5] ])
y_labels = np.array([0,0,0,0,1,1,1,1])

ssw = ssw(data, y_labels)
ssb = ssb(data, y_labels)
print ssw
print ssb
