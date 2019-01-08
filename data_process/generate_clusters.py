#coding:utf-8

import sys
sys.path.append(sys.path[0] + '/../')
from data_loader.data_loader import DataLoader
from copy import deepcopy, copy
import random

dataloader = DataLoader()

#generate pivots:
category_paths = dataloader.get_all_cate_path()
ori_pivots = {}

for path in category_paths:
    root_label = path[0]
    if path[0] not in ori_pivots.keys():
        ori_pivots[root_label] = 0
    if len(ori_pivots.keys())==22:
        break



def cluster_convertor(uid, bus_cate_dict, kwargs):
    pivots = deepcopy(ori_pivots)
    for bid in bus_cate_dict:
        for cate_path in bus_cate_dict[bid]:
            pivots[cate_path[0]] += 1
    return [ uid, pivots.values() ]

data = dataloader.load(cluster_convertor)

# valid_user = random.sample(data, 5000)

valid_user = []
label = []
# with open('/home/yinjia/random5000', 'w') as uid_out:
#     for u in valid_user:
#         uid_out.write(u[0])
#         if u != valid_user[-1]:
#             uid_out.write('\n')

d_index = range(22)
sizes = [1000, 600, 600, 800]

print len(data)
current_label = 0
current_size_index = 0

for d in d_index:
    size = sizes[current_size_index]
    d_valid_uid = []
    for item in data:
        uid = item[0]
        vec = item[1]
        # if len(set(vec)) <= 2 or vec[-1] > 0:
        #     continue
        if vec[-1] > 0:
            continue
        max_dim = max(vec)
        if max_dim != vec[d] or vec.count(max_dim) > 1:
            continue
        if max_dim < 3:
            continue
        second_max = -1
        for val in vec:
            if val < max_dim and val > second_max:
                second_max = val
        if (float(second_max) / float(max_dim)) >= .0 and (float(second_max) / float(max_dim)) <= .4:
            print (float(second_max) / float(max_dim))
            if item[0] not in valid_user and item[0] not in d_valid_uid:
                d_valid_uid.append(item[0])
            if len(d_valid_uid) == size:
                valid_user.extend(d_valid_uid)
                label.extend([current_label for i in xrange(size)])
                current_size_index += 1
                current_label += 1
                break
    if current_size_index == 4:
        break

if len(set(valid_user)) != len(valid_user):
    print "Duplicates"


with open('/home/yinjia/Documents/besttestdata3000_var', 'w') as uid_out:
    with open('/home/yinjia/Documents/testtruth_var', 'w') as  label_out:
        with open('/home/yinjia/Documents/bestvec', 'w') as vec_out:
            for u in valid_user:
                uid_out.write(u)
                vec_out.write(str(u[1]) + "\n")
                if u != valid_user[-1]:
                    uid_out.write('\n')
            for i, l in enumerate(label):
                label_out.write(str(l))
                if i+1 != len(label):
                    label_out.write('\n')
