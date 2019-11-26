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

datashape = (2000, 2000)
sigma = 1
# restore data from file

with open('geog_affi_mat') as geog_in:
    geog_affi_mat = np.reshape(np.fromfile(geog_in), datashape)

with open('jacc_affi_mat') as jacc_in:
    addr_affi_mat = np.reshape(np.fromfile(jacc_in), datashape)

with open('geomctr_affi_mat') as geomctr_in:
    geomctr_affi_mat = np.reshape(np.fromfile(geomctr_in), datashape)

with open('geombet_affi_mat') as geombet_in:
    geombet_affi_mat = np.reshape(np.fromfile(geombet_in), datashape)

# run clustering algorithm

## normalize the geomctr_affi_mat & geombet_affi_mat

geomctr_affi_mat = (geomctr_affi_mat - geomctr_affi_mat.min()) / (geomctr_affi_mat.max() - geomctr_affi_mat.min())
geombet_affi_mat = (geombet_affi_mat - geombet_affi_mat.min()) / (geombet_affi_mat.max() - geombet_affi_mat.min())

def cls_size(label):
    tags = set(label)
    rlt = []
    for t in tags:
        rlt.append(label.tolist().count(t))
    return rlt
def rbf(X, sigma):
    return np.exp(- X ** 2 / (2. * sigma ** 2))

result_obj = {
    'geog':{
        'sc':[],
        'labels':[],
        'cls_size':[]
    },
    'jaccard':{
        'sc':[],
        'labels':[],
        'cls_size':[]
    },
    'geom_ctr':{
        'sc':[],
        'labels':[],
        'cls_size':[]
    },
    'geom_bet':{
        'sc':[],
        'labels':[],
        'cls_size':[]
    },
    'ari':{
        'val':[],
        'type': ['jaccard','geom_ctr', 'geom_bet']
    }
}

keys = ['geog', 'jaccard', 'geom_ctr', 'geom_bet']

for k in range(2, math.floor(math.sqrt(datashape[0]))):

    #spectral   

    for idx, X in enumerate([geog_affi_mat, addr_affi_mat, geomctr_affi_mat, geombet_affi_mat]):
        X_name = 'geog' if idx==0 else 'addr'
        rbf_X = rbf(X, sigma)

        try:
            sp_label = SpectralClustering(n_clusters=k, affinity='precomputed', eigen_solver='arpack').fit_predict(rbf_X)
            sp_sc = silhouette_score(X, sp_label, metric='precomputed') if len(set(sp_label)) >= 2 else -2
            sp_cls_size = cls_size(sp_label)
        except Exception as e:
            sp_label = None
            sp_sc = -2
            sp_cls_size = None
        print('Spectral, %s, k=%d, sc=%f, size=%s'%(X_name, k, sp_sc, sp_cls_size))
        result_obj[keys[idx]]['sc'].append(sp_sc)
        result_obj[keys[idx]]['labels'].append(sp_label.tolist() if sp_label is not None else None)
        result_obj[keys[idx]]['cls_size'].append(sp_cls_size if sp_cls_size is not None else None) 

    ari = []
    for i in range(1,4):
        if result_obj[keys[i]]['labels'][-1] is not None:
            ari.append(adjusted_rand_score(result_obj['geog']['labels'][-1], result_obj[keys[i]]['labels'][-1]))
        else:
            ari.append(-2.)
    
    result_obj['ari']['val'].append(ari)


with open('geog_result.js', 'w') as out:
    json.dump(result_obj, out)
