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
    return [ uid, pivots.values(), bus_cate_dict.keys()]

data = dataloader.load(cluster_convertor)
attributes = ori_pivots.keys()

valid_users = []
for u in data:
    non_zero_count = 0
    max_v = -1
    for v in u[1]:
        if v>0:
            non_zero_count+=1
        if v>max_v:
            max_v=v
    if non_zero_count < 2:
        continue
    if max_v < 5:
        continue
    valid_users.append(u)

best_a = []
best_n = []
best_count = -1
def run(ui):
    global best_a
    global best_n
    global best_count

    a = data[ui]
    print a
    print '==============================='
    critrions = [0., .2, .4, .6, .8, 1.]
    n_uid = []
    count = 0
    for i in xrange(0, 5):
        lower_bound = critrions[i]
        upper_bound = critrions[i+1]
        found = False
        for u in valid_users:
            u_set = set(u[2])
            a_set = set(a[2])
            inter_frac = float(len(u_set.intersection(a_set)))/float(len(a_set.union(u_set)))
            if inter_frac >= lower_bound and inter_frac < upper_bound:
                n_uid.append(u)
                count += 1
                found = True
                break
        if not found:
            n_uid.append(["None"])
        
    if count>=best_count and (best_a == [] or len(a[2]) > len(best_a[2])):
        best_a = a
        best_n = n_uid
        best_count = count
        with open(sys.path[0] + "/../a", "w") as a_out:
            a_out.write(str({"uid":a[0], "bus":a[2]}))
        with open(sys.path[0] + "/../n", "w") as n_out:
            for n in n_uid:
                n_out.write(str({"uid":n[0], "bus":n[2]} if n[0] != "None" else "") + "\n")
        print best_count
    return count

print len(valid_users)
for i in xrange(len(data)):
    l = run(i)
    if l==5:
        print 'done'
        break
