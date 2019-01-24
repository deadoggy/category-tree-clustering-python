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

def load_latlon(size):
    with open(config['processed_data_path'] + 'lasvegas_user_latlon.json') as latlon_in:
        user_latlon = json.load(latlon_in)
    # calculate center of latlon
    user_3857_data = []
    for idx, uid in enumerate(user_latlon.keys()):
        if idx >= size:
            break
        ctr_x = 0.
        ctr_y = 0.
        for lat_lon in user_latlon[uid]:
            x2, y2 = latlon_to_3857(lat_lon[0], lat_lon[1])
            ctr_x += x2
            ctr_y += y2
        l = len(user_latlon[uid])
        user_3857_data.append([ctr_x/l, ctr_y/l])
    return user_3857_data
    


loc_dataloader = LocDataLoader('lasvegas_business.json','lasvegas_ub.json',2)
pivots = loc_dataloader.generate_pivots()



sizes = [1000, 5000, 10000, 20000, 40000, 80000, 160000, 320000, 500000]

cate_switcher = [True, True, True]
latlon_switcher = [True, True, True]

def latlon_dist(size):
    global latlon_switcher
    load_start = time.time()
    data= load_latlon(size)
    load_end = time.time()
    load_time = load_end - load_start

    try:
        if latlon_switcher[0]:
            km_start = time.time()
            KMeans(n_clusters=16).fit_predict(data)
            km_end = time.time()
            km_time = km_end - km_start
        else:
            km_time = float('inf')
    except Exception, e:
        km_time = float('inf')
        latlon_switcher[0] = False

    try:
        if latlon_switcher[1]:
            sp_start = time.time()
            SpectralClustering(n_clusters=16).fit_predict(data)
            sp_end = time.time()
            sp_time = sp_end - sp_start
        else:
            sp_time = float('inf')
    except Exception, e:
        sp_time = float('inf')
        latlon_switcher[1] = False

    try:
        if latlon_switcher[2]:
            ha_start = time.time()
            AgglomerativeClustering(n_clusters=16).fit_predict(data)
            ha_end = time.time()
            ha_time = ha_end - ha_start
        else:
            ha_time = float('inf')
    except Exception, e:
        ha_time = float('inf')
        latlon_switcher[2] = False
    
    log_msg = 'dist:latlon, load time:%fs, KMeans:%fs, Spectral:%fs, Hierarchical:%fs'%(load_time, km_time, sp_time, ha_time)
    return log_msg

def category_dist(size):
    global cate_switcher
    load_start = time.time()
    data= loc_dataloader.load(vectorized_convertor, pivots=pivots, data_size=size).values()
    load_end = time.time()
    load_time = load_end - load_start

    try:
        if cate_switcher[0]:
            km_start = time.time()
            KMeans(n_clusters=16).fit_predict(data)
            km_end = time.time()
            km_time = km_end - km_start
        else:
            km_time = float('inf')
    except Exception, e:
        km_time = float('inf')
        cate_switcher[0] = False

    try:
        if cate_switcher[1]:
            sp_start = time.time()
            SpectralClustering(n_clusters=16).fit_predict(data)
            sp_end = time.time()
            sp_time = sp_end - sp_start
        else:
            sp_time = float('inf')
    except Exception, e:
        sp_time = float('inf')
        cate_switcher[1] = False

    try:
        if cate_switcher[2]:
            ha_start = time.time()
            AgglomerativeClustering(n_clusters=16).fit_predict(data)
            ha_end = time.time()
            ha_time = ha_end - ha_start
        else:
            ha_time = float('inf')
    except Exception, e:
        ha_time = float('inf')
        cate_switcher[2] = False
    
    log_msg = 'dist:cate, load time:%fs, KMeans:%fs, Spectral:%fs, Hierarchical:%fs'%(load_time, km_time, sp_time, ha_time)
    return log_msg


for size in sizes:
    for dist in ['cate','latlon']:
        if dist=='cate':    
            logging.info(category_dist(size))
        else:
            logging.info(latlon_dist(size))




