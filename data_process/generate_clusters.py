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

if SOURCE_DATASET == 'YELP':
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

data = dataloader.load(cluster_convertor)

print( "loading users done")

if len(data[0][1]) != AMAZON_DIMENSION:
    AMAZON_DIMENSION = len(data[0][1])


print( len(data) )


# sizes_list = [
#     # [1000, 600, 600, 800],
#     # [1000, 50, 550, 1400],
#     # [2000, 200, 300, 500],
#     [200, 400, 100, 300, 200, 600, 750, 150]
# ]

# sizes_list = [[10000, 8000, 6000, 7000, 9000, 11000, 9000, 5000, 5000, 10000, 8000, 5000, 7000]]

for sizes in sizes_list:
    valid_user = []
    label = []
    dimension_cnt = []
    d_index = range(AMAZON_DIMENSION)
    current_size_index = 0
    existed_dim = set()

    for current_size_index in range(len(sizes)):
        print('current size index: %d'%current_size_index)
        size = sizes[current_size_index]
        for d in d_index:
            if d in existed_dim:
                continue

            d_valid_uid = []
            d_dim_cnt = []
            flag = False
            for item in data:
                uid = item[0]
                vec = item[1]
                if len(np.nonzero(vec)[0]) <= 1:
                    continue
                # if vec[-1] > 0:
                #     continue
                max_dim = max(vec)
                if max_dim != vec[d] or vec.count(max_dim) > 1:
                    continue
                # if max_dim < 3:
                #     continue
                second_max = -1
                for val in vec:
                    if val < max_dim and val > second_max:
                        second_max = val
                if (float(second_max) / float(max_dim)) >= .0 and (float(second_max) / float(max_dim)) <= .6:
                    if item[0] not in valid_user and item[0] not in d_valid_uid:
                        d_valid_uid.append(item[0])
                        d_dim_cnt.append(item[1])
                    if len(d_valid_uid) == size:
                        print( d )
                        existed_dim.add(d)
                        valid_user.extend(d_valid_uid)
                        dimension_cnt.extend(d_dim_cnt)
                        label.extend([current_size_index for i in range(size)])
                        flag = True
                        print('     dim index: %d'%d)
                        break
            if flag:
                break
    if len(set(valid_user)) != len(valid_user):
        print( "Duplicates" )

    FILE_NAME = SOURCE_DATASET

    for s in sizes:
        FILE_NAME += "_%d"%s

    with open('/home/yinjia/experiment_dataset/clustering/wsdm/%s'%FILE_NAME, 'w') as uid_out:
        with open('/home/yinjia/experiment_dataset/clustering/wsdm/%s_label'%FILE_NAME, 'w') as  label_out:
            with open('/home/yinjia/experiment_dataset/clustering/wsdm/%s_dim_count'%FILE_NAME, 'w') as vec_out:
                for u in valid_user:
                    uid_out.write(u)
                    if u != valid_user[-1]:
                        uid_out.write('\n')
                for v in dimension_cnt:
                    vec_out.write(str(v))
                    vec_out.write('\n')
                for i, l in enumerate(label):
                    label_out.write(str(l))
                    if i+1 != len(label):
                        label_out.write('\n')
