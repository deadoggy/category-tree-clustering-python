#coding:utf-8

import sys
sys.path.append(sys.path[0] + '/../')
from sklearn.cluster import *
from data_loader.data_loader import DataLoader
from dist.bottom_up_edit_dist import *
from dist.vectorized_user_cate_dist import *
from ctc.density_covertree import *
from ctc.covertree_clustering import *
import time
import logging
import numpy as np
from sklearn.metrics import silhouette_score, adjusted_rand_score
from config.load_config import Config
from index.index import *
from matplotlib import pyplot as plt


config = Config()
dataloader = DataLoader()
#read a
with open(sys.path[0] + "/../a") as a_in:
    aid = a_in.read().split('\n')[0]

#read
with open(sys.path[0] + "/../n") as n_in:
    nids = n_in.read().split('\n')

nids.remove('None')
if '' in nids:
    nids.remove('')

cate_trees = generate_category_tree(dataloader)

rlt_dist = {1.:[], 0.1:[], 0.01:[], 0.001:[], 0.0001:[]}
x_axis = ['0%', '20%', '40%', '60%']

fig, axs = plt.subplots(ncols=5)

sigmas = [1., 0.1, 0.01, 0.001, 0.0001]
for row, sigma in enumerate(sigmas):
    ax = axs[row]
    data = dataloader.load(vectorized_convertor, pivots = cate_trees, sigma=sigma, valid_uid=[aid] + nids)
    avec = data[0]
    nvecs = data[1:]
    for nv in nvecs:
        rlt_dist[sigma].append(vectorized_dist_calculator(np.array(avec), np.array(nv)))
    ax.bar(x_axis, rlt_dist[sigma], width = 0.4)
    ax.set_title(str(sigma))
plt.show()