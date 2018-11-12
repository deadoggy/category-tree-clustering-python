#coding:utf-8

import sys
sys.path.append(sys.path[0] + "/../")
from data_loader.data_loader import DataLoader
from copy import deepcopy, copy

dataloader = DataLoader()


for path in category_paths:
    root_label = path[0]
    if path[0] not in ori_pivots.keys():
        ori_pivots[root_label] = 0
    if len(ori_pivots.keys())==22:
        break

def cluster_convertor(uid, bus_cate_dict, kwargs):
    return [ uid, bus_cate_dict.keys()]

data = dataloader.load(cluster_convertor)

valid_users = []
for u in data:
    if len(u[1]) < 5:
        continue
    valid_users.append(u)

best_a = []
best_n = []
best_count = -1
def run(ui):
    global best_a
    global best_n
    global best_count

    a = valid_users[ui]
    print a
    print '==============================='
    critrions = [0., .2, .4, .6, .8, 1.]
    n_uid = []
    count = 0
    for i in xrange(0, 5):
        lower_bound = critrions[i]
        upper_bound = critrions[i+1]
        found = False
        for u in data:
            u_set = set(u[1])
            a_set = set(a[1])
            inter_frac = float(len(u_set.intersection(a_set)))/float(len(a_set.union(u_set)))
            if inter_frac >= lower_bound and inter_frac < upper_bound:
                n_uid.append(u)
                count += 1
                found = True
                break
        if not found:
            n_uid.append(["None"])
        
    if count>best_count or (count == best_count and (best_a == [] or len(a[1]) > len(best_a[1]))):
        best_a = a
        best_n = n_uid
        best_count = count
        with open(sys.path[0] + "/../a", "w") as a_out:
            a_out.write(str({"uid":a[0], "bus":a[1]}))
        with open(sys.path[0] + "/../n", "w") as n_out:
            for n in n_uid:
                n_out.write(str({"uid":n[0], "bus":n[1]} if n[0] != "None" else "") + "\n")
        print '++++++++++++++++++++++++++++++'
        print best_count
        print '++++++++++++++++++++++++++++++'
    return count

print len(valid_users)
for i in xrange(len(valid_users)):
    l = run(i)