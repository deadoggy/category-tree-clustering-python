#coding:utf-8

import sys
sys.path.append(sys.path[0] + '/../')
from sklearn.cluster import *
from sklearn import manifold
from data_loader.data_loader import DataLoader
from dist.vectorized_user_cate_dist import *
import time
import logging
import numpy as np
from config.load_config import Config
import os
import json
import random
from pyproj import Proj, transform
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
from sklearn.metrics import silhouette_score, adjusted_rand_score, mean_squared_error


config = Config().config
sigma = 0.001
def lonlat_to_3857(lon, lat):
    p1 = Proj(init='epsg:4326')
    p2 = Proj(init='epsg:3857')
    x1, y1 = p1(lon, lat)
    x2, y2 = transform(p1, p2, x1, y1, radians=True)
    return x2, y2

def get_data():
    with open(config['processed_data_path'] + "lasvegas_business_cate_similarity.json") as fin:
        ori_data = json.load(fin)
    data = []
    lonlat_data = []
    for bid in ori_data.keys():
        sim = np.array(ori_data[bid]['similarity'])
        lonlat = ori_data[bid]['lonlat']
        data.append( np.exp(- np.power(sim,2)/np.power(sigma, 2)) )
        # data.append(sim)
        lonlat_data.append( np.array(lonlat_to_3857(lonlat[0], lonlat[1])) )
    return data, lonlat_data

data, lonlat_data = get_data()
# print "begin t-SNE"
# X_embedded = manifold.TSNE(n_components=2, learning_rate=10, n_iter=1000).fit_transform(data[0:100])
# print "t-SNE done"

# lonlat_data = sorted(lonlat_data, cmp=lambda x,y:int(y[0]-x[0]))
# lonlat_data = sorted(lonlat_data[100:-100], cmp=lambda x,y:int(y[1]-x[1]))[0:-2]
# vor = Voronoi(lonlat_data)
# voronoi_plot_2d(vor, show_vertices=False, point_size=0.5)
# plt.show()


max_k = int(np.sqrt(len(lonlat_data)))
mse = []
print ("max_k: %d"%max_k)
for ki in range(2, max_k):
    print (ki)
    km =KMeans(n_clusters=ki)
    _labels = km.fit_predict(lonlat_data)
    ctr_sum = [np.array([0. for i in range(2)]) for i in range(len(set(_labels)))]
    ctr_size = [0 for i in range(len(set(_labels)))]
    for j, d in enumerate(lonlat_data):
        ctr_sum[_labels[j]] += d
        ctr_size[_labels[j]] += 1
    for k in range(len(set(_labels))):
        ctr_sum[k] /= ctr_size[k]
    y_predict = [ ctr_sum[_labels[x]] for x in range(len(data)) ]
    mse.append(mean_squared_error(y_predict, lonlat_data))

plt.plot(mse)
plt.show()

