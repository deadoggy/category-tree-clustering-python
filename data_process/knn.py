import numpy as np
import sys
sys.path.append(sys.path[0] + '/../')
from data_loader.data_loader import DataLoader
from dist.vectorized_user_cate_dist import *
from copy import deepcopy, copy
import random
import json
from sklearn.neighbors import BallTree

sigmas = [0.001, 0.0001, 0.00001, 0.000001, 0.0000001, 0.00000001]
# load 3w user data

dataset = 'amazon'
if dataset == 'amazon':
    data_file_name = 'amazon_dist_ub_line.json'
    business_file_name = '/data/rec_dataset/amazon/amazon_business_category_line.json'
else:
    data_file_name = 'yelp_dist_ub_line.json'
    business_file_name = '/data/rec_dataset/yelp/processed/business_line.json'

dataloader = DataLoader(data_file_name=data_file_name, business_file_name=business_file_name)
pivots = generate_category_tree(dataloader)

uids = []
uid_bus = {}
def cluster_convertor(uid, bus_cate_dict, kwargs):
    uids.append(uid)
    uid_bus[uid] = bus_cate_dict
    ret = [ ]
    for sig in sigmas:
        kwargs['sigma'] = sig
        ret.append(vectorized_convertor(uid, bus_cate_dict, kwargs))
    return ret
data = np.array(dataloader.load(cluster_convertor, pivots = pivots))

selected_uid_idx = random.choice(range(len(uids)))
k = 5
knn_uid_idx = []
knn_uid_dists = []

for sig_idx, sig in enumerate(sigmas): # each sigma
    X = data[:,sig_idx]
    tree = BallTree(X)
    dist, idx = tree.query(X[selected_uid_idx:selected_uid_idx+1], k)
    knn_uid_idx.append(idx[0].tolist())
    knn_uid_dists.append(dist[0].tolist())

rlt_data = {
    'uid': uids[selected_uid_idx],
    'uid_bus' : uid_bus[uids[selected_uid_idx]],
    'knn_uid': [[uids[i] for i in idxs] for idxs in knn_uid_idx],
    'knn_dists': knn_uid_dists,
    'bus_cate': [[uid_bus[uids[i]] for i in idxs] for idxs in knn_uid_idx]
}

with open('%s_knn_out.json'%dataset, 'w') as out:
    json.dump(rlt_data, out)
