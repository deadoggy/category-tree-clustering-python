#coding:utf-8

import sys
sys.path.append(sys.path[0] + '/../')
from sklearn.cluster import *
from data_loader.data_loader import DataLoader
from data_loader.loc_data_loader import LocDataLoader
import time
import logging
import numpy as np
from sklearn.preprocessing import minmax_scale
from sklearn.preprocessing import normalize
from sklearn.metrics import silhouette_score, adjusted_rand_score, mean_squared_error
from config.load_config import Config
import os
from geopy.distance import vincenty
import json
import random
from pyproj import Proj, transform
from util.kmeans import KMeans, generate_new_centers, rand_center, dist_metric


logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='/log/ctclog/%s_%s_quality_tx_exp.log'%(time.strftime("%Y-%m-%d:%H:%M", time.localtime()), sys.argv[2]),
    filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

def rbf(dist):
    '''
        Gaussian rbf kernal function
        formula: np.exp(- (d(X,X)**2)/(2 * sigma**2 ))

        @dist: float
    '''
    #parameter modified here#
    sigma = config['rbf_sigma']
    return np.exp(-(dist**2)/(2*(10000**2)))

def latlon_to_3857(lat, lon):
    p1 = Proj(init='epsg:4326')
    p2 = Proj(init='epsg:3857')
    x1, y1 = p1(lon, lat)
    x2, y2 = transform(p1, p2, x1, y1, radians=True)
    return [x2, y2]

config = Config().config
# with open(config['processed_data_path'] + 'lasvegas_user_latlon.json') as latlon_in:
#     user_latlon = json.load(latlon_in)
# with open(config['processed_data_path'] + 'lasvegas_X.json', 'r') as X_in:
#     X = json.load(X_in)
# uids = X['uids']
# X_3857 = []
# for uid in uids:
#     tmp_loc = [ latlon_to_3857(loc[0], loc[1]) for loc in user_latlon[uid] ]
#     X_3857.append(tmp_loc)
# X['user_3857_all'] = X_3857
# with open(config['processed_data_path'] + 'lasvegas_X.json', 'w') as X_out:
#     json.dump(X,X_out)

#load data
with open(config['processed_data_path'] + 'lasvegas_X.json', 'r') as X_in:
    X = json.load(X_in)['user_3857_all']




def calculate_affinity(X):
    '''
        calculate affinity matrix of X

        @X: dataset

        #return: np.ndarray, shape=[n_sample, n_sample]
    '''
    ret_mat = np.array([[0. for j in xrange(len(X)) ] for i in xrange(len(X))])
    for i_idx in xrange(len(X)):
        print i_idx
        for j_idx in xrange(i_idx+1, len(X)):
            ret_mat[i_idx][j_idx] = ret_mat[j_idx][i_idx] = dist_metric(X[i_idx], X[j_idx])
    return ret_mat
    
def mse(X, labels, dist):
    '''
        calculate mean squared error of X and labels

        @X: list, shape=[N:x:2], N=(size of dataset), x=(a user's locations), 2=(location)
        @labels: list, labels of X
        @dist: callable, func to calculate distance between data points
    '''
    mse = 0.

    k = len(set(labels))
    clusters = [[] for i in xrange(k)]
    for idx, x in enumerate(X):
        clusters[labels[idx]].append(x)
    centers = generate_new_centers(X, labels, k)
    for idx, x in enumerate(X):
        print idx
        center = centers[labels[idx]]
        mse += np.power(dist(x, center), 2)
    return mse / len(labels)

def cls_size(label):
    tags = set(label)
    rlt = []
    for t in tags:
        rlt.append(label.tolist().count(t))
    return rlt 

# print 'calculating affinity matrix..'
# affinity_mat = calculate_affinity(X).tolist()
# with open(config['processed_data_path'] + 'tx_affinity_mat.json', 'w') as affinity_mat_out:
#     json.dump(affinity_mat, affinity_mat_out)
# print 'calculating done'
# exit()

with open(config['processed_data_path'] + 'tx_affinity_mat.json', 'r') as affinity_mat_in:
    affinity_mat = np.array(json.load(affinity_mat_in))

print 'load done'

def calculate_spectral_affinity(sigma, affinity_matrix):
    '''
        convert affinity matrix using rbf

        @signma: 
        @affinity_matrix: np.ndarray
    '''
    ret_mat = np.exp( -affinity_matrix**2/(2 * sigma**2)  )
    return ret_mat

spectral_mat = calculate_spectral_affinity(7000, affinity_mat)


for k in xrange(2, 72):
    #spectral

    sp_label = SpectralClustering(n_clusters=k, affinity='precomputed').fit(spectral_mat).labels_
    sp_sc = silhouette_score(affinity_mat, sp_label, metric='precomputed')
    #sp_mse = mse(X, sp_label, dist_metric)
    sp_mse = 0.
    sp_cls_size = str(cls_size(sp_label))
    logging.info('Spectral, epsg3857-tx, k=%d, sc=%f, mse=%f, size=%s'%(k, sp_sc, sp_mse, sp_cls_size))

    #hierarchical
    ha_label = AgglomerativeClustering(n_clusters=k, affinity='precomputed', linkage='average').fit(affinity_mat).labels_
    ha_sc = silhouette_score(affinity_mat, ha_label, metric='precomputed')
    # ha_mse = mse(X, ha_label, dist_metric)
    ha_mse = 0.
    ha_cls_size = str(cls_size(ha_label))
    logging.info('Hierarchical, epsg3857-tx, k=%d, sc=%f, mse=%f, size=%s'%(k, ha_sc, ha_mse, ha_cls_size))

    #kmeans
    # km_start = time.time()
    # km_label = KMeans(X, k, rand_center, generate_new_centers, dist_metric)
    # km_end = time.time()
    # print "km time:%ds"%(km_end - km_start)
    # km_sc = sc(X, km_label, dist_metric, affinity_mat)
    # km_mse = mse(X, km_label, dist_metric)
    # km_cls_size = str(cls_size(km_label))
    # logging.info('KMeans, epsg3857-tx, k=%d, sc=%f, mse=%f, size=%s'%(k, km_sc, km_mse, km_cls_size))