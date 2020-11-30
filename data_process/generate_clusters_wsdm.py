#coding:utf-8

import sys
sys.path.append(sys.path[0] + '/../')
from data_loader.data_loader import DataLoader
from copy import deepcopy, copy
import random
import json
import numpy as np

dataloader = DataLoader()
print("load finished")


YELP_DIMENSION = 22
AMAZON_DIMENSION = 85

SOURCE_DATASET = 'YELP'

ori_pivots = {}

buscate = dataloader.business_cate

if SOURCE_DATASET == 'AMAZON':
    for bid in buscate:
        paths = buscate[bid]
        for p in paths:
            if p[0] not in ori_pivots:
                ori_pivots[p[0]] = 0
        if len(ori_pivots.keys())==AMAZON_DIMENSION:
            break
else:
    category_paths = dataloader.get_all_cate_path()
    for path in category_paths:
        root_label = path[0]
        if path[0] not in ori_pivots.keys():
            ori_pivots[root_label] = 0
        if len(ori_pivots.keys())==YELP_DIMENSION:
            break



def cluster_convertor(uid, bus_cate_dict, kwargs):
    global flag
    pivots = deepcopy(ori_pivots)
    if len(bus_cate_dict) >= 4:
        for bid in bus_cate_dict:
            for cate_path in bus_cate_dict[bid]:
                if cate_path[0] not in pivots:
                    pivots[cate_path[0]] = 0
                pivots[cate_path[0]] += 1
    return [ uid, list(pivots.values()) ]

print( "loading users" )

data = dataloader.load(cluster_convertor, data_size=5000000 if SOURCE_DATASET=='AMAZON' else np.inf)

print( "loading users done")

if len(data[0][1]) != AMAZON_DIMENSION:
    print(len(data[0][1]))
    AMAZON_DIMENSION = len(data[0][1])


print( len(data) )


d_index = range(AMAZON_DIMENSION)


for d in d_index:
    print('current: %d'%d)
    d_valid_uid = []
    d_dim_cnt = []
    flag = False
    for idx, item in enumerate(data):
        if idx % 100000==0:
            print(idx)
        if idx == 2000000:
            break
        if item is None:
            continue
        uid = item[0]
        vec = item[1]
        if len(np.nonzero(vec)[0]) <= 1:
            continue
        sorted_vec = sorted(vec)
        max_dim = sorted_vec[-1]
        if max_dim != vec[d]:
            continue
        second_max = sorted_vec[-2]
        
        if (float(second_max) / float(max_dim)) >= .4 and (float(second_max) / float(max_dim)) <= .6:
            d_valid_uid.append(item[0])
            d_dim_cnt.append(item[1])
        if len(d_valid_uid) > 10000:
            break

    FILE_NAME = SOURCE_DATASET + '_dim%d'%d

    with open('/home/yinjia/experiment_dataset/clustering/wsdmr06/%s'%FILE_NAME, 'w') as uid_out:
        with open('/home/yinjia/experiment_dataset/clustering/wsdmr06/%s_dim_count'%FILE_NAME, 'w') as vec_out:
            for u in d_valid_uid:
                uid_out.write(u)
                if u != d_valid_uid[-1]:
                    uid_out.write('\n')
            for v in d_dim_cnt:
                vec_out.write(str(v))
                vec_out.write('\n')