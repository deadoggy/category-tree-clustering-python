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

all_addr_data = loc_dataloader.load(address_convert_func)

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

geog_data = np.array(minmax_scale(geog_data, axis=1))

# calculate affinity matrix
geog_affi_mat = np.zeros((len(geog_data), len(geog_data)))
addr_affi_mat = np.zeros_like(geog_affi_mat)

def jaccard(label_1, label_2):
    sl1 = set(label_1)
    sl2 = set(label_2)

    return len(sl1.intersection(sl2)) / len(sl1.union(sl2))

for i in range(0, len(geog_data)):
    for j in range(i, len(geog_data)):

        # geog data
        geog_affi_mat[i][j] = geog_affi_mat[j][i] = \
            np.sqrt(np.sum(np.power(geog_data[i]-geog_data[j], 2)))
            
        
        # addr data
        addr_affi_mat[i][j] = addr_affi_mat[j][i] = \
            1 - jaccard(addr_data[i], addr_data[j])
            

# run clustering algorithm

def cls_size(label):
    tags = set(label)
    rlt = []
    for t in tags:
        rlt.append(label.tolist().count(t))
    return rlt
def rbf(X, sigma):
    return np.exp(- X ** 2 / (2. * sigma ** 2))

geog_labels = []
addr_labels = []

for k in range(2, math.floor(math.sqrt(datasize))):

    #spectral   

    for idx, X in enumerate([geog_affi_mat, addr_affi_mat]):
        X_name = 'geog' if idx==0 else 'addr'
        sp_label = SpectralClustering(n_clusters=k, affinity='precomputed').fit_predict(rbf(X, sigma))
        sp_sc = silhouette_score(X, sp_label, metric='precomputed')
        sp_cls_size = str(cls_size(sp_label))
        print('Spectral, %s, k=%d, sc=%f, size=%s'%(X_name, k, sp_sc, sp_cls_size))
        if 0==idx:
            geog_labels.append(sp_label)
        else:
            addr_labels.append(sp_label)

with open(config['processed_data_path'] + 'lasvegas_user_latlon.json') as latlon_in:
    user_latlon = json.load(latlon_in)
user_loc = []
for uid in uids:
    user_loc.append(list(user_latlon[uid]))

with open('geog_result.js', 'w') as out:
    json.dump({'locations': np.array(user_loc).tolist(), 'geog_labels': np.array(geog_labels).tolist(), 
    'addr_labels': np.array(addr_labels).tolist()}, out)

