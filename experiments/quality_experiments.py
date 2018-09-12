#coding:utf-8

import sys
sys.path.append(sys.path[0] + '/../')
from sklearn.cluster import *
from data_loader.data_loader import DataLoader
from dist.bottom_up_edit_dist import *
from dist.vectorized_user_cate_dist import *
from ctc.density_covertree import *
from ctc.covertree_clustering import *
import time
import logging
import numpy as np


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='/log/ctclog/%s_exp.log'%time.strftime("%Y-%m-%d", time.localtime()),
    filemode='w')

def _data_format(data, precomputed=False, dist_func=None):
    '''
        format data to numpy

        @data: list, each element is a data point
        @precomputed: boolean, False:not precomputed; True:precomputed
        
        #return: if precomputed => a square matrix; else => feature vec ndarray
    '''
    if not precomputed:
        return np.array(data)
    
    if dist_func is None or not callable(dist_func):
        raise Exception('a callable distance function is required')

    dist_matrix = np.array(
        [
            [ 0.0 for i in xrange(len(data))] for j in xrange(len(data))
        ]
    )
    for i in xrange(len(data)):
        for j in xrange(i, len(data)):
            if i==j:
                dist_matrix[i,j] = 0.0
            else:
                dist_matrix[i,j] = dist_func(data[i], data[j])
    
    return dist_matrix


def experiments(alg, dist, data_size, **kwargs):
    '''
        run experiments

        @alg: string, which clustering algorithm to use, in ['covertree', 'hierarichical', 'dbscan', 'kmeans', 'spectral']
        @dist: string, which distance to use, in ['vec', 'edit']
        @data_size: integer, size of experiments data
    
    '''

    if alg not in ['covertree', 'hierarichical', 'dbscan', 'kmeans', 'spectral']:
        raise Exception('alg in experiments not valid')
    
    if dist not in ['vec', 'edit']:
        raise Exception('dist in experiments not valid')

    #start
    start_time = time.time()

    data_loader = DataLoader()
    #valid uid
    valid_uid = None if not kwargs.has_key('valid_uid') else kwargs['valid_uid']
    if type(valid_uid) != list:
        raise Exception('valid_uid must be a list')

    #load data based on dist type
    if dist == 'vec':
        if not kwargs.has_key('sigma'):
            raise Exception('sigma is required in vectorized distance')
        sigma = kwargs['sigma']
        pivots = generate_category_tree(data_loader)
        data = data_loader.load(vectorized_convertor, pivots=pivots,sigma=sigma, valid_uid=valid_uid)
        metric = 'euclidean'
        X = _data_format(data, False, vectorized_dist_calculator)
    else:
        data = data_loader.load(bottomup_edit_dist_converter, valid_uid=valid_uid)
        metric = 'precomputed' 
        X = _data_format(data, True, bottomup_edit_dist_calculator)
    
    #dbscan
    if alg == 'dbscan':
        if (not kwargs.has_key('eps')) or (not kwargs.has_key('min_samples')):
            raise Exception('eps and min_samples are required in dbscan')
        eps = kwargs['eps']
        min_samples = kwargs['min_samples']
        dbscan = DBSCAN(eps=eps, min_samples=min_samples, metric=metric)
        labels = dbscan.fit_predict(X)
        
    
    if not kwargs.has_key('k'):
        raise Exception('k is required in %s'%alg)
    k = kwargs['k']
    
    #kmeans
    if alg == 'kmeans':
        if dist == 'edit':
            raise Exception('edit distance is not supported in kmeans')
        kmeans = KMeans(n_clusters=k, max_iter=300)
        labels = kmeans.fit_predict(X)
        
    #spectral
    if alg == 'spectral':
        labels = spectral_clustering(affinity=X, n_clusters=k)
    
    #hierarchical
    if alg == 'hierarchical':
        labels = AgglomerativeClustering(n_clusters=k, affinity='precomputed', linkage='average').fit_predict(X)
    
    #covertree
    if alg == 'covertree':
        calculator = vectorized_dist_calculator if dist=='vec' else bottomup_edit_dist_calculator
        pivots = generate_category_tree(data_loader)
        dct = DensityCoverTree(calculator, 3)
        for i, d in enumerate(data):
            dct.insert(Node(val=d, index=i))
        labels = covertree_clustering(dct, k)

    #end
    end_time = time.time()
    return (data, labels, end_time-start_time)

def index(data, label, index_name):
    '''
        index to evaluate the experiment result

        @data: list, all data
        @label: ndarray, shape(len(data),)
        @index_name: index to evaluate results, in ['sc', 'mae', 'rand']

        return: float
    '''
    pass
