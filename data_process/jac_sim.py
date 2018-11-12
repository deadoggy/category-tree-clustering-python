#coding:utf-8

from __future__ import division
import sys
sys.path.append(sys.path[0] + '/../')
from data_loader.data_loader import DataLoader
from copy import deepcopy, copy
import random
import json

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
    return [ uid, bus_cate_dict.keys()]

data = dataloader.load(cluster_convertor)
attributes = ori_pivots.keys()

valid_users = []
for u in data:
    if len(u[1]) < 5:
        continue
    valid_users.append(u)

result = {
    0.:[],
    .2:[],
    .4:[],
    .6:[],
    .8:[]
}

keys = [0., .2, .4, .6, .8, 1.]
f_out = []
for i in xrange(5):
    f_out.append(open("result_%f"%keys[i], 'a'))

for i in xrange(len(valid_users)):
    print '%s/%s'%(i, len(valid_users))
    for j in xrange(i+1, len(valid_users)):
        a = set(valid_users[i][1])
        b = set(valid_users[j][1])
        ab_inter = a.intersection(b)
        jac_sim = len(ab_inter) / (len(a) + len(b) - len(ab_inter))
        for k in xrange(5):
            low = keys[k]
            up = keys[k+1]
            if jac_sim >= low and jac_sim < up:
                out_pair = "%s,%s"%(valid_users[i][0], valid_users[j][0])
                f_out[k].write(str(out_pair) + "\n")
                break
for i in xrange(5):
    f_out[i].close()

