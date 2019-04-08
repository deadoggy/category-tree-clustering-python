#coding:utf-8

import sys
sys.path.append(sys.path[0] + '/../')
from sklearn.cluster import *
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
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='/log/buslog/%s_%s_quality_exp.log'%(time.strftime("%Y-%m-%d:%H:%M", time.localtime()), sys.argv[2]),
    filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
config = Config().config
dataloader = DataLoader()
business_vec = {}
def latlon_to_3857(lat, lon):
    p1 = Proj(init='epsg:4326')
    p2 = Proj(init='epsg:3857')
    x1, y1 = p1(lon, lat)
    x2, y2 = transform(p1, p2, x1, y1, radians=True)
    return x2, y2
def load_business(bids):
    
    pivots = generate_category_tree(dataloader)
    for c, bid in enumerate(bids):
        if c%1000==0:
            print c
        business_vec[bid] = {"similarity": [ 0. for i in xrange(len(pivots)) ], "lonlat": []}
        for d, p in enumerate(pivots):
            business_vec[bid]["similarity"][d] = p.similarity(dataloader.get_business_cate_path(bid))
    return business_vec
def get_lasvegas_buslatlon():
    count = 0
    with open(config['original_data_path'] + '/business.json') as fin:
        line = fin.readline()
        while ''!=line:
            line_json = json.loads(line)
            if line_json['city'] == 'Las Vegas' and business_vec.has_key(line_json["business_id"]):
                count += 1
                if count%1000==0:
                    print count
                business_vec[line_json["business_id"]]['lonlat'] = [ line_json['longitude'], line_json['latitude'] ]
            line = fin.readline()

def get_lasvegas_bids():
    bids_set = set()
    with open(config["processed_data_path"] + "lasvegas_ub.json") as fin:
        ub_dist = json.load(fin)
    for uid in ub_dist:
        for bid in ub_dist[uid]:
            bids_set.add(bid)
    return list(bids_set)
load_business(get_lasvegas_bids())
get_lasvegas_buslatlon()
with open(config["processed_data_path"] + "lasvegas_business_cate_similarity.json", "w") as fout:
    json.dump(business_vec, fout)


