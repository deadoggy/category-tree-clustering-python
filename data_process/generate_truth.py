#coding:utf-8

import sys
sys.path.append(sys.path[0] + '/../')
from data_loader.data_loader import DataLoader
from ctc.covertree_clustering import *
from dist.vectorized_user_cate_dist import *

with open('testdata1000', 'r') as valid_uid_f:
    valid_uid = valid_uid_f.read().split('\n')

data_loader = DataLoader()
pivots = generate_category_tree(data_loader)
data = data_loader.load(vectorized_convertor, pivots=pivots, sigma=0.0001, valid_uid=valid_uid)

y_truth = []
non_one_table = []

for d in data:
    #check which dimension is not zero
    for i, v in enumerate(d):
        if v != 1.0:
            if i not in non_one_table:
                non_one_table.append(i)
                y_truth.append(len(non_one_table)-1)
                break
            else:
                for ni, label in enumerate(non_one_table):
                    if label==i:
                        y_truth.append(ni)
                        break
with open('testtruth', 'w') as out:
    for t in y_truth:
        out.write(str(t))
        out.write('\n')