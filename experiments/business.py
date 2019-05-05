#coding:utf-8

import sys
sys.path.append(sys.path[0] + "/../")
from config.load_config import Config
from dist import vectorized_user_cate_dist
from index.index import *
from data_loader.data_loader import DataLoader
from dist.vectorized_user_cate_dist import *
from pyproj import Proj, transform
from sklearn.cluster import KMeans, dbscan
from sklearn.metrics import silhouette_score, mean_squared_error
from matplotlib import pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import KDTree
import json
import numpy as np

config = Config().config
PATH_BEG_OFFSET = 0
PATH_END_PFFSET = 1
GAUSSIAN_SIGMA = 0.
RADIUS = 200

# u'CorrByydi35r-6SvmhYFHA'
exception_bid = [
    u'nMMlTMTLgtG7tJg6w7vmSA',
    u'fJFVpJN6X5rB1KjwtP4VZg'
    u'LwG4QsmvOibEsEUlryrPsw',
    u'8d8QHAktYg8Q2C3ZpAhwvQ',
    u'ivLJuOmDavlBmKIh0nnisg',
    u'FlLkjcSzfqmQBK6iEHRtTg',
    u'FaUk138U3lXk5EaTpI_37w',
    u's44fonP-M6Gzh7goJi559w',
    u'NTu31vavstnDW4pc68HJOA',
    u'CES01QjtAbJpYn_HI98gHg',
    u'HIZ5619cs1L-EA4MAHlWnw',
    u'MOKA2TABC6T04tKjzZ1_rw',
    u'b12qS86-9a_prAfFIdRD2w',
    u'pYeoaUJ6veQ3FEiSBnVMcw',
    u'ZpK3cU9lIPddzFcaV_rygg', 
]

def lonlat_to_3857(lon, lat):
    p1 = Proj(init='epsg:4326')
    p2 = Proj(init='epsg:3857')
    x1, y1 = p1(lon, lat)
    x2, y2 = transform(p1, p2, x1, y1, radians=True)
    return x2, y2

def generate_geog_pivots(plus_offset, minus_offset):
    '''
        generate a address pivots set 

        @plus_offset: offset at the begining of path
        @minus_offset: offset at the end of path
    '''
    with open(config["processed_data_path"] + "/lasvegas_business_info.json", "r") as din:
        datajson = json.load(din)

    pivots_list = {}
    for bid in datajson.keys():
        if bid in exception_bid:
            continue
        shop = datajson[bid]
        neighborhood = shop['neighborhood']
        if neighborhood not in pivots_list.keys():
            pivots_list[neighborhood] = CateTree()

        addrpath = shop['address']
        if addrpath == '':
            addrpath = ['']
        
        pivots_list[neighborhood].insert(addrpath[plus_offset : len(addrpath)-minus_offset])
    
    return pivots_list.values()

def generate_geog_vec():
    shopvec = {}
    pivots = generate_geog_pivots(PATH_BEG_OFFSET, PATH_END_PFFSET)
    
    with open(config['processed_data_path'] + "/lasvegas_business_info.json") as din:
        datajson = json.load(din)
    
    for bid in datajson:
        if bid in exception_bid:
            continue
        addrpath = datajson[bid]['address']
        if addrpath == '':
            addrpath = ['']
        shopvec[bid] = [ 0. for i in xrange(len(pivots)) ]

        for idx in xrange(len(pivots)):
            shopvec[bid][idx] = pivots[idx].similarity([addrpath[PATH_BEG_OFFSET : len(addrpath)-PATH_END_PFFSET]])
            if GAUSSIAN_SIGMA != 0.:
                shopvec[bid][idx] = np.exp(-(np.power(shopvec[bid][idx], 2.))/(2*GAUSSIAN_SIGMA**2))
    return shopvec

def generate_geom_vec():
    shopvec = {}
    with open(config['processed_data_path'] + '/lasvegas_business_info.json') as din:
        datajson = json.load(din)
    
    for bid in datajson:
        if bid in exception_bid:
            continue
        lat = datajson[bid]['latitude']
        lon = datajson[bid]['longitude']
        x,y = lonlat_to_3857(lon, lat)
        shopvec[bid] = [x, y]
    return shopvec

def generate_cate_vec():
    shopcatevec = {}
    with open(config['processed_data_path'] + '/lasvegas_business_cate_similarity.json') as din:
        datajson = json.load(din)
    for bid in datajson:
        if bid in exception_bid:
            continue
        shopcatevec[bid] = datajson[bid]['similarity']
    return shopcatevec

def generate_checkin():
    with open(config['processed_data_path'] + '/lasvegas_business_info.json') as din:
        datajson = json.load(din)
    shopckin = {}
    for bid in datajson:
        if bid in exception_bid:
            continue
        shopckin[bid] = datajson[bid]['review_count']
    return shopckin

def generate_rate():
    with open(config['processed_data_path'] + '/lasvegas_business_info.json') as din:
        datajson = json.load(din)
    shoprate = {}
    for bid in datajson:
        if bid in exception_bid:
            continue
        shoprate[bid] = datajson[bid]['stars']
    return shoprate

def calmse(y_predict, data, k):
    d = len(vec[0])
    clusters_centers = [ np.array(np.zeros(d)) for i in xrange(k) ]
    clusters_count = [ 0 for i in xrange(k) ]
    for i, cls_i in enumerate(y_predict):
            if -1 != cls_i:
                clusters_centers[cls_i] += np.array(data[i])
                clusters_count[cls_i] += 1
    for i, ctr in enumerate(clusters_centers):
        clusters_centers[i] = ctr/clusters_count[i]
    return mean_squared_error([ clusters_centers[i] if i!=-1 else data[d] for d, i in enumerate(y_predict) ], data)

print "Generating GeoG Vectors..."
geog_data = generate_geog_vec()
print "Generating GeoM Vectors..."
geom_data = generate_geom_vec()

ori_geog_vec = np.array(geog_data.values())
ori_geom_vec = np.array(geom_data.values())

minmaxscaler = MinMaxScaler()

geog_vec = minmaxscaler.fit_transform(ori_geog_vec)
geom_vec = minmaxscaler.fit_transform(ori_geom_vec)

vec = np.concatenate((geog_vec, geom_vec), axis=1)

# print vec

# print "KMeans..."
# #KMeans 
# #top_k = int(np.sqrt(len(vec)))
# top_k = 40
# print top_k
# mse_vals = []
# for k in xrange(2, top_k):
#     label = KMeans(n_clusters=k).fit_predict(vec)
#     mse = calmse(label, vec, k)
#     print "k=%d, mse=%f"%(k, mse)
#     mse_vals.append(mse)

# plt.plot(range(2, top_k), mse_vals)
# plt.savefig("geog+geom+mse.png")


# print "DBSCAN..."

# n_samples = len(vec)
# leaf_size = int(n_samples/2+1)

# tree = KDTree(vec, leaf_size=leaf_size)

# dist_array = []

# for i in xrange(len(vec)):
#     if i%100==0:
#         print i
#     dist, ind = tree.query(vec[i:i+1], k=50)
#     dist_array.append(dist[0][2])

# dist_array = sorted(dist_array)

# plt.plot(range(len(dist_array)), dist_array)
# plt.show()

# step_eps = 0.01
# min_pts= 5
# step_min_pts = 1

# best_k = -1
# best_eps = 0.01
# best_minpts = 5
# best_mse = np.inf

# try:
#     for i in xrange(1, 15):
#         for j in xrange(20):
#             print 'eps=%f, minpts=%d'%(step_eps*i, min_pts + j*step_min_pts)
#             label = dbscan(vec, eps=step_eps*i, min_samples=min_pts + j*step_min_pts)[1]
#             tmp_k = len(set(label)) - 1 if -1 in label else 0
#             tmp_mse = calmse(label, vec, tmp_k)
#             print 'k=%d, mse=%f, noise=%d'%(tmp_k, tmp_mse, len(label[label==-1]))
#             print '================================='
#             if tmp_mse < best_mse:
#                 best_mse = tmp_mse
#                 best_k = tmp_k
#                 best_eps = step_eps*i
#                 best_minpts = min_pts + j*step_min_pts
# except Exception, e:
#     print e.message
# finally:
#     print 'best_k=%d, best_eps=%f, best_minpts=%d, best_mse=%f'%(best_k, best_eps, best_minpts, best_mse)

# print 'KMeans...'

# km_label = KMeans(n_clusters=15).fit_predict(vec)

# print 'DBSCAN...'

# db_label = dbscan(vec, eps=0.01, min_samples=24)[1]

# with open('km_db_label.json', 'w') as kmdb_out:
#     json.dump({'kmeans': km_label.tolist(), 'dbscan': db_label.tolist()}, kmdb_out)


# generate checkin and rate data
checkin_data = np.array(generate_checkin().values())
rate_data = np.array(generate_rate().values())
cate_data = np.array(generate_cate_vec().values())

# generate kdtree
n_samples = len(vec)
leaf_size = int(n_samples/2+1)
tree = KDTree(ori_geom_vec, leaf_size=leaf_size)

# generate average category number in RADIUS
def generate_catengb_mat():
    dim = cate_data.shape[1]
    catengb_mat = np.zeros((dim, dim))
    catengb_cnt_mat = np.zeros((dim, dim))

    for idx in xrange(len(ori_geom_vec)):
        ngb_idx = tree.query_radius(ori_geom_vec[idx:idx+1], r=RADIUS)[0]
        ngb_cate_arr = np.array([ cate_data[i] for i in ngb_idx ])
        cate_arr = cate_data[idx]

        for dr in xrange(dim):
            if cate_arr[dr]!=0.:
                for dc in xrange(dim):
                    catengb_cnt_mat[dr, dc] += 1
                    col = ngb_cate_arr[:,dc]
                    catengb_mat[dr, dc] += col[col!=0.].shape[0]
    
    ret_mat = catengb_mat/catengb_cnt_mat
    ret_mat[np.isnan(ret_mat)] = 0.
    return ret_mat

avg_catengb_data = generate_catengb_mat()

def cal_geo_features(idx):
    dim = cate_data.shape[1]
    ngb_idx = tree.query_radius(ori_geom_vec[idx:idx+1], r=RADIUS)[0]
    ngb_cate_arr = np.array([ cate_data[i] for i in ngb_idx ])
    
    #f_{r}^D
    frd = len(ngb_idx)

    #f_{r}^{NE}
    frNE = 0.
    for d in dim:
        Nc = ngb_cate_arr[ngb_cate_arr[d]!=0.].shape[0]
        if Nc != 0.:
            frNE += -1. * (Nc/frd) * np.log(Nc/frd)
    
    #f_{r}^{Com}
    frCom = ngb_cate_arr[np.sum(ngb_cate_arr * cate_data[idx]) != 0.].shape[0] / frd

    return 

def cal_mob_features(bid):
    pass
