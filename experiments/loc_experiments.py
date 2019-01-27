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
import json
import random
from pyproj import Proj, transform


config = Config().config

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='/log/ctclog/%s_%s_quality_exp.log'%(time.strftime("%Y-%m-%d:%H:%M", time.localtime()), sys.argv[2]),
    filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

def latlon_to_3857(lat, lon):
    p1 = Proj(init='epsg:4326')
    p2 = Proj(init='epsg:3857')
    x1, y1 = p1(lon, lat)
    x2, y2 = transform(p1, p2, x1, y1, radians=True)
    return x2, y2

loc_dataloader = LocDataLoader('lasvegas_business.json','lasvegas_ub.json',2)
pivots = loc_dataloader.generate_pivots()
data = loc_dataloader.load(vectorized_convertor, pivots=pivots)

root_name = []
for p in pivots:
    root_name.append(p.root.chd_set[0].label)

with open("/home/yinjia/pivots_name.txt", "w") as o:
    for n in root_name:
        o.write(n)
        o.write('\n')
exit()
# with open(config['processed_data_path'] + 'lasvegas_user_vec.json', 'w') as out:
#     json.dump(data, out)


''' generate 5000 users '''

# with open(config['processed_data_path'] + 'lasvegas_user_vec.json') as vec_in:
#     user_data = json.load(vec_in)
# with open(config['processed_data_path'] + 'lasvegas_user_latlon.json') as latlon_in:
#     user_latlon = json.load(latlon_in)

# # calculate center of latlon
# user_3857_data = {}
# for uid in user_latlon.keys():
#     ctr_x = 0.
#     ctr_y = 0.
#     for lat_lon in user_latlon[uid]:
#         x2, y2 = latlon_to_3857(lat_lon[0], lat_lon[1])
#         ctr_x += x2
#         ctr_y += y2
#     l = len(user_latlon[uid])
#     user_3857_data[uid] = [ctr_x/l, ctr_y/l]

# #uniform the orders

# user_X = []
# user_3857_X = []
# uids = []

# for uid in random.sample(user_3857_data.keys(), 5000):
#     uids.append(uid)
#     user_X.append(user_data[uid])
#     user_3857_X.append(user_3857_data[uid])

# with open(config['processed_data_path'] + 'lasvegas_X.json', 'w') as X_out:
#     json.dump({'uids':uids, 'user_X': user_X, 'user_3857_X': user_3857_X}, X_out)


''' run alg '''
with open(config['processed_data_path'] + 'lasvegas_X.json', 'r') as X_in:
    X = json.load(X_in)

epsg3857_X = X['user_3857_X']
address_X = X['user_X']

n_clusters = 10

def eul(a,b):
    return np.sqrt(np.sum(np.power((a-b)**2,2)))

def sc(X, label):
    return silhouette_score(X, label)

def mse(X, label):
    k = len(set(label))
    ctrs = np.array([ [0. for i in xrange(len(X[0]))] for i in xrange(k)])
    ctrs_sz = [0 for i in xrange(k)]
    for i, l in enumerate(label):
        ctrs[l] += X[i]
        ctrs[l] += X[i]
        ctrs_sz[l] += 1
    for i, ctr in enumerate(ctrs):
        ctr[0] /= ctrs_sz[i]
    y_true = np.array([ ctrs[l] for l in label ])
    return mean_squared_error(y_true, X)

def ari(label_1, label_2):
    return adjusted_rand_score(label_1, label_2)
def cls_size(label):
    tags = set(label)
    rlt = []
    for t in tags:
        rlt.append(label.tolist().count(t))
    return rlt 

#address
X_list = [np.array(address_X) ,np.array(epsg3857_X)]
X_names = ['address','epsg3857']
for k in xrange(2, 46):
    for idx, _X in enumerate(X_list):
        X_name = X_names[idx]
        #kmeans
        km_label = KMeans(n_clusters=k).fit_predict(_X)
        print km_label
        km_sc = sc(_X, km_label)
        print km_sc
        km_mse = mse(_X, km_label)
        km_cls_size = str(cls_size(km_label))
        logging.info('KMeans, %s, k=%d, sc=%f, mse=%f, size=%s'%(X_name, k, km_sc, km_mse, km_cls_size))

        #spectral
        if idx!=1:
            sp_label = SpectralClustering(n_clusters=k).fit_predict(_X)
            sp_sc = sc(_X, sp_label)
            sp_mse = mse(_X, sp_label)
            sp_cls_size = str(cls_size(sp_label))
            logging.info('Spectral, %s, k=%d, sc=%f, mse=%f, size=%s'%(X_name, k, sp_sc, sp_mse, sp_cls_size))

        #hierarchical
        ha_label = AgglomerativeClustering(n_clusters=k).fit_predict(_X)
        ha_sc = sc(_X, ha_label)
        ha_mse = mse(_X, ha_label)
        ha_cls_size = str(cls_size(ha_label))
        logging.info('Hierarchical, %s, k=%d, sc=%f, mse=%f, size=%s'%(X_name, k, ha_sc, ha_mse, ha_cls_size))
    

