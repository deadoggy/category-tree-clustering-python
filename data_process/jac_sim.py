#coding:utf-8

from __future__ import division
import sys
sys.path.append(sys.path[0] + '/../')
from data_loader.data_loader import DataLoader
from dist.vectorized_user_cate_dist import *
from copy import deepcopy, copy
import random
import json

# jaccard similarity category
keys = [ -1., 0., .02, .04, .06, .08, .1, .12, .14, .16, .18, .2, .4, .6, .8, 1.]
# category trees sigmods
sigmods = [1., 0.1, 0.01, 0.001, 0.0001]

dataloader = DataLoader()
def cluster_convertor(uid, bus_cate_dict, kwargs):
    return [ uid, bus_cate_dict.keys()]
data = dataloader.load(cluster_convertor)
valid_uid = []
valid_bus = []
for u in data:
    if len(u[1]) < 5:
        continue
    valid_uid.append(u[0])
    valid_bus.append(u[1])

pivots = generate_category_tree(dataloader)
sigmod_data = []
for sig in sigmods:
    sigmod_data.append(dataloader.load(vectorized_convertor, pivots = pivots, sigma=sig, valid_uid=valid_uid))


f_out = []
for i in xrange(len(keys)-1):
    f_out.append(open("distance_%f"%keys[i+1], 'a'))

for i in xrange(len(valid_uid)):
    print '%s/%s'%(i, len(valid_uid))
    for j in xrange(i+1, len(valid_uid)):
        a = set(valid_bus[i])
        b = set(valid_bus[j])
        ab_inter = a.intersection(b)
        jac_sim = len(ab_inter) / (len(a) + len(b) - len(ab_inter))

        for k in xrange(len(keys)-1):
            low = keys[k]
            up = keys[k+1]
            if jac_sim > low and jac_sim <= up:
                out_pair = "%s,%s,%f"%(valid_uid[i], valid_uid[j], jac_sim)
                for p in xrange(len(sigmods)):
                    out_pair += ",%f"%vectorized_dist_calculator(sigmod_data[p][i], sigmod_data[p][j])
                f_out[k].write(str(out_pair) + "\n")
                break
for f in f_out:
    f.close()

