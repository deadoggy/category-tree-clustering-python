#coding:utf-8

import sys
sys.path.append(sys.path[0] + '/../')
from sklearn.cluster import *
from data_loader.data_loader import DataLoader
from data_loader.loc_data_loader import LocDataLoader
from dist.bottom_up_edit_dist import *
from dist.vectorized_user_cate_dist import *
from ctc.density_covertree import *
from ctc.covertree_clustering import *
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

config = Config().config

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='/log/ctclog/%s_%s_efficiency_exp.log'%(time.strftime("%Y-%m-%d:%H:%M", time.localtime()), sys.argv[2]),
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


switcher = [True, True, True]
sizes = [1000, 5000, 10000, 20000, 40000, 80000, 160000, 320000, 500000]

for size in sizes:

    load_start = time.time()
    data= loc_dataloader.load(vectorized_convertor, pivots=pivots, data_size=size).values()
    load_end = time.time()
    load_time = load_end - load_start

    try:
        if switcher[0]:
            km_start = time.time()
            KMeans(n_clusters=16).fit_predict(data)
            km_end = time.time()
            km_time = km_end - km_start
        else:
            km_time = float('inf')
    except Exception, e:
        switcher[0] = False

    try:
        if switcher[1]:
            sp_start = time.time()
            SpectralClustering(n_clusters=16).fit_predict(data)
            sp_end = time.time()
            sp_time = sp_end - sp_start
        else:
            sp_time = float('inf')
    except Exception, e:
        switcher[1] = False

    try:
        if switcher[2]:
            ha_start = time.time()
            AgglomerativeClustering(n_clusters=16).fit_predict(data)
            ha_end = time.time()
            ha_time = ha_end - ha_start
        else:
            ha_time = float('inf')
    except Exception, e:
        switcher[2] = False
    
    log_msg = 'load time:%fs, KMeans:%fs, Spectral:%fs, Hierarchical:%fs'%(load_time, km_time, sp_time, ha_time)
    logging.info(log_msg)



