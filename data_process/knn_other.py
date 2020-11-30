import numpy as np
import sys
sys.path.append(sys.path[0] + '/../')
from data_loader.data_loader import DataLoader
from dist.vectorized_user_cate_dist import *
from copy import deepcopy, copy
import random
import json

dataset = 'yelp'
k = 3000
with open('/data/SDM_result/figure/knn_result/%s_otherdist.json'%dataset) as fin:
    other_dists = json.load(fin)

if dataset == 'amazon': # line number 12280; index 12279
    data_file_name = '/home/yinjia/experiment_dataset/clustering/amazon_dist_ub_line.json'
    business_file_name = '/data/rec_dataset/amazon/amazon_business_category_line.json'
    selected_idx = 12279
else: # yelp line number 16581; index 16580
    data_file_name = '/home/yinjia/experiment_dataset/clustering/yelp_dist_ub_line.json'
    business_file_name = '/data/rec_dataset/yelp/processed/business_line.json'
    selected_idx = 16580

dataloader = DataLoader(data_file_name=data_file_name, business_file_name=business_file_name)
pivots = generate_category_tree(dataloader)

uids = []
uid_bus = {}
def cluster_convertor(uid, bus_cate_dict, kwargs):
    uids.append(uid)
    uid_bus[uid] = bus_cate_dict
    return None 

dataloader.load(cluster_convertor, pivots=pivots)

# sorted idx

for disttype in ['pqgram', 'binary', 'bottomup', 'jaccard']:
    print(disttype)
    dists = other_dists[disttype]
    sorted_dist_idx = np.argsort(dists)
    knn_uid_idx = sorted_dist_idx[0:k].tolist()
    knn_uid_dists = [dists[i] for i in knn_uid_idx]
    rlt_data = {
        'uid': uids[selected_idx],
        'uid_bus' : uid_bus[uids[selected_idx]],
        'knn_uid': [[ uids[i] for i in knn_uid_idx]] ,
        'knn_dists': [knn_uid_dists],
        'bus_cate': [[uid_bus[uids[i]] for i in knn_uid_idx]]
    }
    with open('/data/SDM_result/figure/knn_result/many_%s_%s_knn_out.json'%(dataset, disttype), 'w') as out:
        json.dump(rlt_data, out)

