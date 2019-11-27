import sys
sys.path.append(sys.path[0] + '/../')
from sklearn.cluster import *
import numpy as np 
from sklearn.preprocessing import minmax_scale
from sklearn.metrics import jaccard_score
from data_loader.loc_data_loader import LocDataLoader
from sklearn.metrics import silhouette_score, adjusted_rand_score, mean_squared_error
from dist.vectorized_user_cate_dist import *
from config.load_config import Config
import json
import random
import math
from pyproj import Proj, itransform

config = Config().config
datasize = 2000
sigma = 1

# load all dataset
loc_dataloader = LocDataLoader('lasvegas_business.json','lasvegas_ub.json',2)
pivots = loc_dataloader.generate_pivots()
all_geog_data = loc_dataloader.load(vectorized_convertor, pivots=pivots)

def address_convert_func(uid, bus_addr, kwargs):
    ret = []
    for bid in bus_addr:
        ret.extend(bus_addr[bid][0])
    return ret

def latlon_to_3857(points):
    p1 = Proj(init='epsg:4326', preserve_units=False)
    p2 = Proj(init='epsg:3857', preserve_units=False)
    return [ pts for pts in itransform(p1, p2, points, switch=True) ]

def traj_to_3857(trajs):
    rlt = []
    for t in trajs:
        t = np.array(t) 
        rlt.append(np.array(latlon_to_3857(t.tolist())))
    
    return rlt

all_addr_data = loc_dataloader.load(address_convert_func)
with open(config['processed_data_path'] + 'lasvegas_user_latlon.json') as latlon_in:
    user_latlon = json.load(latlon_in)

# sample a exp dataset with size [datasize]
uids = []
geog_data = []
addr_data = []
while True:
    for uid in random.sample(all_geog_data.keys(), 50):
        if len(set(all_geog_data[uid])) >= 4 and len(geog_data)<datasize:
            uids.append(uid)
            geog_data.append(all_geog_data[uid])
            addr_data.append(all_addr_data[uid])
    if datasize == len(geog_data):
        break

geog_user_loc = {'uid': uids, 'locations': [ user_latlon[u] for u in uids]}
with open('geog_uid_loc.json', 'w') as user_loc_out:
    json.dump(geog_user_loc, user_loc_out)

geog_data = np.array(minmax_scale(geog_data, axis=1))

geom_data = []
for uid in uids:
    if len(geom_data)%10==0:
        print("geom:%d"%len(geom_data))
    geom_data.append(traj_to_3857([list(user_latlon[uid])])[0])

# calculate affinity matrix
geog_affi_mat = np.zeros((len(geog_data), len(geog_data)))
addr_affi_mat = np.zeros_like(geog_affi_mat)
geomctr_affi_mat = np.zeros_like(geog_affi_mat)
geombet_affi_mat = np.zeros_like(geog_affi_mat)

def jaccard(label_1, label_2):
    sl1 = set(label_1)
    sl2 = set(label_2)

    return len(sl1.intersection(sl2)) / len(sl1.union(sl2))

def geom_ctr(v1, v2):
    v1 = v1.mean(axis=0)
    v2 = v2.mean(axis=0)
    return np.sqrt(np.sum((v1 - v2)**2))

def geom_bet(v1, v2):
    rlt = 0.
    for i in v1:
        for j in v2:
            rlt += np.sqrt(np.sum((i - j)**2))
    return rlt / (len(v1) *  len(v2))


for i in range(0, len(geog_data)):
    if i%10 ==0:
        print('affinity matrix: %d'%i)
    for j in range(i, len(geog_data)):

        # geog data
        geog_affi_mat[i][j] = geog_affi_mat[j][i] = \
            np.sqrt(np.sum(np.power(geog_data[i]-geog_data[j], 2)))
            
        # addr data
        addr_affi_mat[i][j] = addr_affi_mat[j][i] = \
            1 - jaccard(addr_data[i], addr_data[j])

        # geom center data 
        geomctr_affi_mat[i][j] = geomctr_affi_mat[j][i] = \
            geom_ctr(geom_data[i], geom_data[j])
        
        # geom between each pair
        geombet_affi_mat[i][j] = geombet_affi_mat[j][i] = \
            geom_bet(geom_data[i], geom_data[j]) if i!=j else 0.

# save matrix to file
with open('geog_affi_mat', 'w') as geog_out:
    geog_affi_mat.tofile(geog_out)

with open('jacc_affi_mat', 'w') as jacc_out:
    addr_affi_mat.tofile(jacc_out)

with open('geomctr_affi_mat', 'w') as geomctr_out:
    geomctr_affi_mat.tofile(geomctr_out)

with open('geombet_affi_mat', 'w') as geombet_out:
    geombet_affi_mat.tofile(geombet_out)

