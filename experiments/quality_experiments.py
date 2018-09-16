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
from sklearn.metrics import silhouette_score, adjusted_rand_score

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

def algorithm_runner(alg, dist, **kwargs):
    '''
        run algorithms

        @alg: string, which clustering algorithm to use, in ['covertree', 'hierarichical', 'dbscan', 'kmeans', 'spectral']
        @dist: string, which distance to use, in ['vec', 'edit']
    '''

    if alg not in ['covertree', 'hierarchical', 'dbscan', 'kmeans', 'spectral']:
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
        dct = DensityCoverTree(calculator, 5)
        for i, d in enumerate(data):
            dct.insert(Node(val=d, index=i))
        labels = covertree_clustering(dct, k)

    #end
    end_time = time.time()
    return (data, labels, end_time-start_time)

def index(data, y_predict, index_name, dist_name, y_truth = None):
    '''
        index to evaluate the experiment result

        @data: list, all data
        @y_predict: ndarray, shape(len(data),), predicted value
        @index_name: index to evaluate results, in ['sc', 'mae', 'rand']
        @dist_name: name of dist, in ['vec', 'edit']
        @y_truth: ndarray, shape(len(data),), truth
        return: float
    '''
    if index_name not in ['sc', 'mae', 'rand']:
        raise Exception('%s not supported'%index_name)
    if dist_name not in ['vec', 'edit']:
        raise Exception('%s not supported'%dist_name)

    if 'vec' == dist_name:
        dist = vectorized_dist_calculator
    else:
        dist = bottomup_edit_dist_calculator
    k = len(set(y_predict)) - (1 if -1 in y_predict else 0)
    # mae
    # here we do not calculate centers but calculate mean dist between each pair of datanodes
    # within a cluster
    if index_name == 'mae':
        clusters = [ [] for i in xrange(k) ]
        for i, cls_i in enumerate(y_predict):
            if -1 != cls_i:
                clusters[cls_i].append(data[i])
        mae = 0.0
        for clus in clusters:
            cls_mae = 0.0
            for i in xrange(len(clus)):
                for j in xrange(len(clus)):
                    cls_mae += dist(clus[i], clus[j])
            mae += cls_mae / len(clus)
        return mae
    elif index_name == 'sc':
        X = _data_format(data, precomputed=True, dist_func=dist)
        return silhouette_score(X, y_predict, metric='precomputed')
    else:
        if y_truth is None:
            raise Exception('rand index requires y_truth')
        return adjusted_rand_score(y_truth, y_predict)

def experiments(dataset_name, k):
    '''
        run experiments, evaluate index of results and generate log

        @dataset_name: in ['testdata1000', 'randomdata1000']
    '''

    logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='/log/ctclog/%s_%s_exp.log'%(time.strftime("%Y-%m-%d", time.localtime()),dataset_name),
    filemode='w')

    algs = ['covertree', 'hierarchical', 'kmeans', 'spectral']
    dists = ['edit']
    indexs = ['sc', 'mae', 'rand']
    with open(dataset_name,'r') as valid_uid_f:
            valid_uid = valid_uid_f.read().split('\n')

    y_truth = None
    if dataset_name == 'testdata1000':
        with open('testtruth','r') as truth_f:
            y_truth = truth_f.read().split('\n')
        for i in xrange(len(y_truth)):
            y_truth[i] = int(y_truth[i])
    
    for alg in algs:
        for dist in dists:
            if alg=='kmeans' and dist=='edit':
                continue
            data, labels, run_time = algorithm_runner(alg, dist, valid_uid=valid_uid, sigma=0.0001, k=k)
            log_content = 'k:%s; dataset:%s; alg:%s; distance_type:%s; ' % (k, alg,dist,dataset_name)
            for idx in indexs:
                index_val = index(data, labels, idx, dist, y_truth)
                log_content += '%s:%s; '%(idx, str(index_val))
            logging.info(log_content)
        
    
experiments('testdata1000', 4)
