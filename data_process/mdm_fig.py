#coding: utf-8

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
import json
import random
from pyproj import Proj, transform
from matplotlib import pyplot as plt

def save_to_js(uids, labels, X_latlon):
    out_lonlat = []
    out_labels = []
    for idx, u in enumerate(uids):
        if -1 == labels[idx]:
            continue
        lonlats = X_latlon[u]
        for loc in lonlats:
            lat = loc[0]
            lon = loc[1]
            out_lonlat.append([lon, lat])
            out_labels.append(labels[idx])
    var_str = 'var lonlats = %s;\n'%str(out_lonlat)
    label_str = 'var labels = %s;'%str(out_labels)
    with open('db_variables.js', 'w') as out:
        out.write(var_str)
        out.write(label_str)

def save_3857_to_js(uids, labels, X_3857):
    out_lonlat = []
    out_labels = []
    for idx, u in enumerate(uids):
        if -1 == labels[idx]:
            continue
        lonlats = X_3857[idx]
        if lonlats[0] > -1.280e7 or lonlats[0] < -1.284e7 or lonlats[1] < 0 or lonlats[0] > -0.95e7:
            continue
        lon = lonlats[0]
        lat = lonlats[1]
        out_lonlat.append(list(convert_3857_to_lonlat(lon, lat)))
        out_labels.append(labels[idx])
    var_str = 'var lonlats = %s;\n'%str(out_lonlat)
    label_str = 'var labels = %s;'%str(out_labels)
    with open('db_variables_3857.js', 'w') as out:
        out.write(var_str)
        out.write(label_str)

def convert_3857_to_lonlat(x, y):
    p1 = Proj(init='epsg:3857')
    x2, y2 = p1(x, y, inverse=True)
    return x2, y2

def resort_affi(X, label):
    '''
        sort X by label and calculate affinity_mat
    '''
    #resort
    s_label = set(label)
    cls_sizes = [ label.tolist().count(i) for i in s_label ]
    cls_sufidx = [ int(np.sum(cls_sizes[0:i])) for i in xrange(len(s_label)) ]
    sorted_X = np.zeros_like(X)
    for idx, l in enumerate(label):
        sorted_X[cls_sufidx[l]] = X[idx]
        cls_sufidx[l] += 1
    affinity_mat = np.zeros([len(X), len(X)])
    for r in xrange(len(X)):
        for c in xrange(r, len(X)):
            affinity_mat[r][c] = affinity_mat[c][r] = np.sqrt(np.sum((sorted_X[r] - sorted_X[c])**2))
    return affinity_mat


def heatmap(X, title):
    ax = plt.subplot()
    ax.imshow(X, cmap='gray')
    #ax.set_title(title)
    ax.set_xticks([])
    ax.set_yticks([])
    plt.savefig('%s.png'%title)

def scatter(X, label):
    color_list = [ '#990033', '#ff99ff', '#660099', '#00ccff', '#ffcc00', '#ff6633', '#33ff33',
    '#99ff00','#336666','#666633', '#000000','grey','purple','#330033','#ff9966','#330099','#cc9999',]
    label_list = list(set(label))
    cls_set = [[],[]]
    color_set = []
    for idx, ux in enumerate(X):
        l = label[idx]
        for x in ux:
            if x[0] > -1.280e7 or x[0] < -1.284e7 or x[1] < 0 or x[0] > -0.95e7:
                continue
            cls_set[0].append(x[0])
            cls_set[1].append(x[1])
            color_set.append(color_list[l])

    ax = plt.subplot()
    ax.scatter(cls_set[0], cls_set[1], c=np.array(color_set), marker='.')
    ax.set_xticks([])
    ax.set_yticks([])
    
    plt.show()

config = Config().config
with open(config['processed_data_path'] + 'lasvegas_X.json', 'r') as X_in:
    X = json.load(X_in)
with open(config['processed_data_path'] + 'lasvegas_user_latlon.json', 'r') as X_in:
    X_latlon = json.load(X_in)

uids = X['uids']
epsg3857_X = X['user_3857_X']
address_X = X['user_X']
epsg3857_X_all = X['user_3857_all']
k = 20

_X = epsg3857_X
km_label = KMeans(n_clusters=k).fit_predict(_X)
print silhouette_score(_X, km_label)
# sp_label = SpectralClustering(n_clusters=k).fit_predict(_X)
# print silhouette_score(_X, sp_label)
# hac_label = AgglomerativeClustering(n_clusters=k).fit_predict(_X)
# print silhouette_score(_X, hac_label)
# db_label = DBSCAN(eps=800, min_samples=19).fit_predict(_X)
# print silhouette_score(_X, db_label)



# print len(set(db_label))
# cls_size = []
# for l in set(db_label):
#     cls_size.append(db_label.tolist().count(l))
# print cls_size

# max_sc = -3.
# max_eps = 0.
# max_minsample = 0
# max_k = -1 
# for i in xrange(1, 10):
#     for ms in xrange(2, 19):
#         print '====================='
#         print 'eps=%f, min_sample=%f'%(i*0.0000002, ms)
#         db_label = DBSCAN(eps=.0000002 * i, min_samples=ms).fit_predict(_X)
#         sc = silhouette_score(_X, db_label)
#         k = (len(set(db_label)) - (0 if -1 not in db_label else 1))
#         print "silhouette score = %f"%sc
#         print "k=%d"%k
#         if sc > max_sc:
#             max_sc = sc; max_eps = .01 * i; max_minsample = ms; max_k = k

# print "++++++++++++++++++++++++++++"
# print "eps=%f; min_sample=%d; k=%d; sc=%f"%(max_eps, max_minsample, max_k, max_sc)

def _scale(mat):
    mean = mat.mean()
    std_var = np.sqrt(mat.var())
    for i in xrange(len(mat)):
        for j in xrange(i+1, len(mat)):
            if mat[i][j] > 2.5 * mean:
                mat[i][j] = mat[j][i] = mean * 2.5
    return mat

km_affi_mat = resort_affi(_X, km_label)
print 'min=%f'%km_affi_mat.min()
print 'max=%f'%km_affi_mat.max()
print 'mean=%f'%km_affi_mat.mean()
print '>2.5*mean:%d'%len(km_affi_mat[km_affi_mat>2.5*km_affi_mat.mean()])
heatmap(km_affi_mat, 'GeoM+KMeans')
print 'KMeans'
# sp_affi_mat = resort_affi(_X, sp_label)
# sp_affi_mat = _scale(sp_affi_mat)
# heatmap(sp_affi_mat, 'GeoM+Spectral')
# print 'Spectral'
# hac_affi_mat = resort_affi(_X, hac_label)
# hac_affi_mat = _scale(hac_affi_mat)
# heatmap(hac_affi_mat, 'GeoM+Hierarchical')
# print 'Hierarchical'
# db_affi_mat = resort_affi(_X, db_label)
# db_affi_mat = _scale(db_affi_mat)
# heatmap(db_affi_mat, 'GeoM+DB')
# print 'DBSCAN'

# save_to_js(uids, db_label, X_latlon)
# save_3857_to_js(uids, db_label, epsg3857_X)

# scatter(epsg3857_X_all, km_label)

# address_km_label = KMeans(n_clusters=k).fit_predict(address_X)
# epsg_km_label = KMeans(n_clusters=k).fit_predict(epsg3857_X)

# while True:
#     idxs = random.sample(range(0, len(address_km_label)), 2)
#     if address_km_label[idxs[0]] == address_km_label[idxs[1]]:
#         continue
#     if epsg_km_label[idxs[0]] != epsg_km_label[idxs[1]]:
#         continue
#     loc_list = [[],[]]
#     color_list = []
#     u1_locs = epsg3857_X_all[idxs[0]]
#     u1_ll = X_latlon[uids[idxs[0]]]
#     u2_locs = epsg3857_X_all[idxs[1]]
#     u2_ll = X_latlon[uids[idxs[1]]]

#     if len(u1_locs)<=2 or len(u2_locs)<=2:
#         continue
#     color_list = [ 'red','purple']

#     for idx, users in enumerate([u1_locs, u2_locs]):
#         for loc in users: 
#             loc_list[0].append(loc[0])
#             loc_list[1].append(loc[1])
#             color_list.append(color_list[idx])
#     ax = plt.subplot()
#     ax.scatter(loc_list[0], loc_list[1], c=color_list)
#     ax.set_xticks([])
#     ax.set_yticks([])
#     print '===================='
#     for l in u1_ll:
#         print (l[1], l[0])
#     print '--------------------'
#     for l in u2_ll:
#         print (l[1], l[0])
#     plt.show()
    
