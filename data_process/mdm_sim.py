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

def latlon_to_3857(lat, lon):
    p1 = Proj(init='epsg:4326')
    p2 = Proj(init='epsg:3857')
    x1, y1 = p1(lon, lat)
    x2, y2 = transform(p1, p2, x1, y1, radians=True)
    return x2, y2

def calculate_center(latlons):
    ctr = np.array([0., 0.])
    for loc in latlons:
        lat = loc[0]
        lon = loc[1]
        ctr += np.array(latlon_to_3857(lat, lon))
    return ctr / len(latlons)

# with open(config['processed_data_path'] + "/lasvegas_user_vec.json") as geog_in:
#     geog_vec = json.load(geog_in)

# with open(config['processed_data_path'] + "/lasvegas_user_latlon.json") as latlon_in:
#     latlons = json.load(latlon_in)

# user_sim_data = {'uids':[], 'geog':[], 'geom':[]}
# user_sim_data['uids'] = random.sample(geog_vec.keys(), 20000)
# for uid in user_sim_data['uids']:
#     user_sim_data['geog'].append(geog_vec[uid])
#     user_sim_data['geom'].append(calculate_center(latlons[uid]).tolist())

# with open(config['processed_data_path'] + "/lasvegas_similarity.json", "w") as sim_out:
#     json.dump(user_sim_data, sim_out)

# with open(config['processed_data_path'] + "/lasvegas_similarity.json") as sim_in:
#     user_sim_data = json.load(sim_in)

# geog_range = [[-1., 0.]]
# for i in xrange(15):
#     down = i*0.2
#     if np.abs(down-1.4)  < 0.0001:
#         geog_range.append([down, 1.5])
#         geog_range.append([1.5, 1.6])
#         continue
#     else:
#         up = (i+1)*0.2
#         geog_range.append([down, up])
# geog_range.append([3., float('inf')])
# geog_count = [ 0 for i in xrange(len(geog_range)) ]

# geom_range = [[-1., 0.]]
# for i in xrange(15):
#     geom_range.append([i*3000., (i+1)*3000.])
# geom_range.append([45000, float('inf')])
# geom_count = [ 0 for i in xrange(len(geom_range)) ]

# print "=================== geog ====================="
# #geog
# for i in xrange(20000):
#     if i%10==0:
#         print i
#     for j in xrange(i+1, 20000):
#         u = np.array(user_sim_data['geog'][i])
#         v = np.array(user_sim_data['geog'][j])
#         dist = np.sqrt(np.sum((u-v)**2))
#         for idx, rg in enumerate(geog_range):
#             if dist > rg[0] and dist <= rg[1]:
#                 geog_count[idx] += 1
#                 break

# print "=================== geom ====================="
# #geom
# for i in xrange(20000):
#     if i%100==0:
#         print i
#     for j in xrange(i+1, 20000):
#         u = np.array(user_sim_data['geom'][i])
#         v = np.array(user_sim_data['geom'][j])
#         dist = np.sqrt(np.sum((u-v)**2))
#         for idx, rg in enumerate(geom_range):
#             if dist > rg[0] and dist <= rg[1]:
#                 geom_count[idx] += 1
#                 break

# print "done"
# with open(config['processed_data_path'] + "/lasvegas_similarity_rlt.json", "w") as out:
#     json.dump({'geog_range': geog_range, 'geog_count': geog_count, 'geom_range':geom_range, 'geom_count': geom_count},out)

with open(config['processed_data_path'] + "/lasvegas_similarity_rlt.json") as sim_in:
    X = json.load(sim_in)

'''geog'''


x_label = []
for r in X['geog_range']:
    x_label.append('(%.1f,%.1f]'%(r[0]/1, r[1]/1))
x_label[0]='=0'
y = X['geog_count']
fig = plt.figure()
fig.set_size_inches(8,8)
ax = plt.subplot()
ax.bar(x_label[0:13], y[0:13], width=-1., align='edge', color='#000000', edgecolor='#ffffff')
ax.set_xticklabels(x_label, rotation=27, horizontalalignment="right", fontsize=12)
for a, b in zip(x_label[0:13], y[0:13]):
    ax.text(a, b+0.000000001, '%.2f'%(b/100000000.), ha='right', va= 'bottom',fontsize=12)
ax.grid()
ax.spines['top'].set_visible(False)  #去掉上边框
ax.spines['right'].set_visible(False) #去掉右边框
ax.set_ylabel('count', rotation=90, fontsize=13)
ax.set_xlabel('GeoGraphical distance between users',fontsize=13)
#fig.text(0.905, 0.105, '1e3')
plt.show()