#coding:utf-8
import sys
sys.path.append(sys.path[0] + '/../')
from sklearn.cluster import *
from data_loader.data_loader import DataLoader
from data_loader.loc_data_loader import LocDataLoader
import time
import logging
import numpy as np
from sklearn.preprocessing import minmax_scale
from sklearn.preprocessing import normalize
from sklearn.metrics import silhouette_score, adjusted_rand_score, mean_squared_error
from config.load_config import Config
import os
import json
import random
from pyproj import Proj, transform
from matplotlib import pyplot as plt

config = Config().config

with open(config['processed_data_path'] + 'lasvegas_X.json') as data_in:
    X = json.load(data_in)

print (X.keys())

all_dist_list = []

def dist_var(mean, loc_list):
    global all_dist_list
    mean = np.array(mean)
    loc_list = np.array(loc_list)
    dist_list = []
    for loc in  loc_list:
        dist = np.sqrt(np.sum((loc-mean)**2))
        # if dist > 80000:
        #     continue
        all_dist_list.append(dist)
        dist_list.append(dist)
    return np.var(dist_list)
    

loc_vars = []

for idx in range(5000):
    mean = X['user_3857_X'][idx]
    loc_list = X['user_3857_all'][idx]
    vari = dist_var(mean, loc_list)
    if vari < .3e11:
        loc_vars.append(vari)

print (np.array(all_dist_list).max())

print (len(all_dist_list))

rgs = [[-1., 0.]]
for i in range(0, 40):
    rgs.append([i*2e6, (i+1)*2e6])
var_count = [0 for i  in range(len(rgs))]
for v in loc_vars:
    for idx in range(len(var_count)):
        if v > rgs[idx][0] and v <= rgs[idx][1]:
            var_count[idx] += 1
            break

fig = plt.figure()
var_ax = plt.subplot()
x_label = []
def v2s(v):
    if v<1e6:
        return str(v)
    else:
        return "%.1f"%(v/1000000)

for r in rgs:
    down = r[0]
    up = r[1]
    x_label.append('(%s,%s]'%(v2s(down), v2s(up)))    
x_label[0] = '=0'
var_ax.bar(x_label, var_count, width=-1., align='edge', color='#000000', edgecolor='#ffffff')
var_ax.set_xticklabels(x_label, rotation=45, horizontalalignment="right", fontsize=9)
for a, b in zip(x_label, var_count):
    var_ax.text(a, b+0.000000001, '%d'%b, ha='right', va= 'bottom',fontsize=10)
var_ax.grid()
var_ax.spines['top'].set_visible(False)  #去掉上边框
var_ax.spines['right'].set_visible(False) #去掉右边框
var_ax.set_ylabel('count', rotation=90, fontsize=12)
fig.text(0.905, 0.105, '1e6')
plt.show()
