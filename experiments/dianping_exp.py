#coding:utf-8
from __future__ import division
import sys
sys.path.append(sys.path[0] + "/../")
from config.load_config import Config
from dist import vectorized_user_cate_dist
from index.index import *
from data_loader.data_loader import DataLoader
from dist.vectorized_user_cate_dist import *
from pyproj import Proj, transform
from sklearn.cluster import KMeans, dbscan
from sklearn.metrics import silhouette_score, mean_squared_error
from matplotlib import pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import KDTree
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestRegressor
import json
import numpy as np

config = Config().config
PATH_BEG_OFFSET = 0
PATH_END_PFFSET = 1
GAUSSIAN_SIGMA = 0.
RADIUS = 200

distance_type = sys.argv[1]
cluster_algorithm = sys.argv[2]
max_ngb = 100

# KMeans arg
kmeans_k = 15

# DBSCAN arg
dbscan_eps = 0.01
dbscan_minpts = 24

exception_bid = []

def lonlat_to_3857(lon, lat):
    p1 = Proj(init='epsg:4326')
    p2 = Proj(init='epsg:3857')
    x1, y1 = p1(lon, lat)
    x2, y2 = transform(p1, p2, x1, y1, radians=True)
    return x2, y2

def generate_geog_pivots(plus_offset, minus_offset):
    '''
        generate a address pivots set 

        @plus_offset: offset at the begining of path
        @minus_offset: offset at the end of path
    '''
    with open("/data/shanghai_business_info.json", "r") as din:
        datajson = json.load(din)

    pivots_list = {}
    for bid in datajson.keys():
        if bid in exception_bid:
            continue
        shop = datajson[bid]
        neighborhood = shop['neighborhood']
        if neighborhood not in pivots_list.keys():
            pivots_list[neighborhood] = CateTree()

        addrpath = shop['address']
        if addrpath == '':
            addrpath = ['']
        
        pivots_list[neighborhood].insert(addrpath[plus_offset : len(addrpath)-minus_offset])
    
    return pivots_list.values()

def generate_geog_vec():
    shopvec = {}
    pivots = generate_geog_pivots(PATH_BEG_OFFSET, PATH_END_PFFSET)
    
    with open("/data/shanghai_business_info.json") as din:
        datajson = json.load(din)
    
    for bid in datajson:
        if bid in exception_bid:
            continue
        addrpath = datajson[bid]['address']
        if addrpath == '':
            addrpath = ['']
        shopvec[bid] = [ 0. for i in xrange(len(pivots)) ]

        for idx in xrange(len(pivots)):
            shopvec[bid][idx] = pivots[idx].similarity([addrpath[PATH_BEG_OFFSET : len(addrpath)-PATH_END_PFFSET]])
            if GAUSSIAN_SIGMA != 0.:
                shopvec[bid][idx] = np.exp(-(np.power(shopvec[bid][idx], 2.))/(2*GAUSSIAN_SIGMA**2))
    return shopvec

def generate_geom_vec():
    shopvec = {}
    with open('/data/shanghai_business_info.json') as din:
        datajson = json.load(din)
    
    for bid in datajson:
        if bid in exception_bid:
            continue
        lat = datajson[bid]['latitude']
        lon = datajson[bid]['longitude']
        x,y = lonlat_to_3857(lon, lat)
        shopvec[bid] = [x, y]
    return shopvec

def generate_rate():
    with open('/data/shanghai_business_info.json') as din:
        datajson = json.load(din)
    shoprate = {}
    for bid in datajson:
        if bid in exception_bid:
            continue
        shoprate[bid] = datajson[bid]['stars']
    return shoprate


print "Generating GeoG Vectors..."
geog_data = generate_geog_vec()
print "Generating GeoM Vectors..."
geom_data = generate_geom_vec()

ori_geog_vec = np.array(geog_data.values())
ori_geom_vec = np.array(geom_data.values())

minmaxscaler = MinMaxScaler()

geog_vec = minmaxscaler.fit_transform(ori_geog_vec)
geom_vec = minmaxscaler.fit_transform(ori_geom_vec)

if distance_type=='GeoM':
    vec = geom_vec
elif distance_type=='GeoG':
    vec = geog_vec
elif distance_type=='Both':
    vec = np.concatenate((geog_vec, geom_vec), axis=1)

with open('/data/dataset/processed/dianping_business_exp_features_%s_%s.json'%(distance_type, cluster_algorithm)) as feature_in:
    features = json.load(feature_in)


print ('rate data')
rate_data = np.array(generate_rate().values())
# kfold

X = np.concatenate((np.array(features), vec), axis=1)
minmaxscaler = MinMaxScaler()
print np.sum(np.isnan(X))
X[np.isnan(X)] = 0.
X = minmaxscaler.fit_transform(X)
Y = rate_data 

kf = KFold(n_splits=5, shuffle=True)

print '\nLinear Regression\n=========='
average_loss = 0.
k = 0
for train_idx, test_idx in kf.split(X):
    k += 1                                                                                                            
    X_train, X_test = X[train_idx], X[test_idx]
    Y_train, Y_test = Y[train_idx], Y[test_idx]
    lnreg = LinearRegression(fit_intercept=True, normalize=True).fit(X_train, Y_train)
    Y_predict = lnreg.predict(X_test)
    loss = np.sum(np.abs(Y_predict - Y_test)) / Y_test.shape[0]
    average_loss += loss

average_loss /= k

print 'average_loss: %f'%average_loss

print '\nRF Regression\n=========='
average_loss = 0.
k=0
for train_idx, test_idx in kf.split(X):
    k += 1
    print k
    X_train, X_test = X[train_idx], X[test_idx]
    Y_train, Y_test = Y[train_idx], Y[test_idx]
    lnreg = RandomForestRegressor(max_depth=None, random_state=0, n_estimators=100).fit(X_train, Y_train)
    print lnreg.feature_importances_
    Y_predict = lnreg.predict(X_test)
    loss = np.sum(np.abs(Y_predict - Y_test)) / Y_test.shape[0]
    average_loss += loss

average_loss /= k

Y_label = Y.astype(int)

print 'average_loss: %f'%average_loss

# print '\nSVM\n=========='
# average_acc = 0.
# k = 0
# for train_idx, test_idx in kf.split(X):
#     k += 1
#     print k
#     X_train, X_test = X[train_idx], X[test_idx]
#     Y_train, Y_test = Y_label[train_idx], Y_label[test_idx]
#     clf = SVC()
#     clf.fit(X_train, Y_train)
#     Y_predict = clf.predict(X_test)
#     acc = np.sum(Y_predict == Y_test) / Y_test.shape[0]
#     average_acc += acc
# average_acc /= k
# print 'average_acc: %f'%average_acc