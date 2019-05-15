#coding:utf-8
from __future__ import division
from __future__ import print_function
import sys
sys.path.append(sys.path[0] + "/../")
from config.load_config import Config
from dist import vectorized_user_cate_dist
from index.index import *
from data_loader.data_loader import DataLoader
from dist.vectorized_user_cate_dist import *
from pyproj import Proj, transform
from sklearn.cluster import KMeans, dbscan
from sklearn.metrics import silhouette_score, mean_squared_error, mean_absolute_error
from matplotlib import pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import KDTree
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestRegressor
import json
import numpy as np

config = Config().config
PATH_BEG_OFFSET = 0
PATH_END_PFFSET = 1
GAUSSIAN_SIGMA = 0.
RADIUS = 200

distance_type = sys.argv[1]
cluster_algorithm = sys.argv[2]
max_ngb = 100

# KMeans arg
kmeans_k = 50

# DBSCAN arg
dbscan_eps = 0.01
dbscan_minpts = 24

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
    with open("/data/shanghai_business_info.json", "r") as din:
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
    
    with open("/data/shanghai_business_info.json") as din:
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
    with open("/data/shanghai_business_info.json") as din:
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
    with open('/data/shanghai_business_cate_similarity.json') as din:
        datajson = json.load(din)
    for bid in datajson:
        if bid in exception_bid:
            continue
        shopcatevec[bid] = datajson[bid]['similarity']
    return shopcatevec

def generate_checkin():
    with open("/data/shanghai_business_info.json") as din:
        datajson = json.load(din)
    shopckin = {}
    for bid in datajson:
        if bid in exception_bid:
            continue
        shopckin[bid] = datajson[bid]['review_count']
    return shopckin

def generate_rate():
    with open("/data/shanghai_business_info.json") as din:
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
    predict = [ clusters_centers[i] if i!=-1 else data[d] for d, i in enumerate(y_predict.tolist()) ]
    return mean_absolute_error(predict, data)

print( "Generating GeoG Vectors...")
geog_data = generate_geog_vec()
print("Generating GeoM Vectors...")
geom_data = generate_geom_vec()

ori_geog_vec = np.array(geog_data.values())
ori_geom_vec = np.array(geom_data.values())

minmaxscaler = MinMaxScaler()

geog_vec = minmaxscaler.fit_transform(ori_geog_vec)
geom_vec = minmaxscaler.fit_transform(ori_geom_vec)

if distance_type=='GeoM':
    vec = geom_vec
    kmeans_k = 15
    dbscan_eps = 0.01
    dbscan_minpts = 20
elif distance_type=='GeoG':
    vec = geog_vec
    kmeans_k = 55
    dbscan_eps = 0.01
    dbscan_minpts = 5
elif distance_type=='Both':
    vec = np.concatenate((geog_vec, geom_vec), axis=1)
    kmeans_k = 55
    dbscan_eps = 0.01
    dbscan_minpts = 24

# print(vec)


# #KMeans 
# top_k = 120
# print (top_k)
# mse_vals = []
# for k in xrange(2, top_k):
#     label = KMeans(n_clusters=k).fit_predict(vec)
#     mse = calmse(label, vec, k)
#     print("k=%d, mse=%f"%(k, mse))
#     mse_vals.append(mse)

# plt.plot(range(2, top_k), mse_vals)
# plt.savefig("geog+mse.png")

# exit()
# print("DBSCAN...")

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
#             print('eps=%f, minpts=%d'%(step_eps*i, min_pts + j*step_min_pts))
#             label = dbscan(vec, eps=step_eps*i, min_samples=min_pts + j*step_min_pts)[1]
#             tmp_k = len(set(label)) - 1 if -1 in label else 0
#             tmp_mse = calmse(label, vec, tmp_k)
#             print ('k=%d, mse=%f, noise=%d'%(tmp_k, tmp_mse, len(label[label==-1])))
#             print ('=================================')
#             if tmp_mse < best_mse:
#                 best_mse = tmp_mse
#                 best_k = tmp_k
#                 best_eps = step_eps*i
#                 best_minpts = min_pts + j*step_min_pts
# except Exception, e:
#     print (e.message)
# finally:
#     print ('best_k=%d, best_eps=%f, best_minpts=%d, best_mse=%f'%(best_k, best_eps, best_minpts, best_mse))




# print ('KMeans...')

# km_label = KMeans(n_clusters=15).fit_predict(vec)

# print ('DBSCAN...')

# db_label = dbscan(vec, eps=0.01, min_samples=24)[1]

# with open('km_db_label.json', 'w') as kmdb_out:
#     json.dump({'kmeans': km_label.tolist(), 'dbscan': db_label.tolist()}, kmdb_out)

if cluster_algorithm=='kmeans':
    print ('kmeans')
    ngb_label = KMeans(n_clusters=kmeans_k).fit_predict(vec)
elif cluster_algorithm=='dbscan':
    print ('dbscan')
    ngb_label = dbscan(vec, eps=dbscan_eps, min_samples=dbscan_minpts)[1]



# generate kdtree
# n_samples = len(vec)
# leaf_size = int(n_samples/2+1)
# tree = KDTree(ori_geom_vec, leaf_size=leaf_size)

# generate checkin and rate data
print ('generating features')
print ('checkin data')
checkin_data = np.array(generate_checkin().values())
print ('rate data')
rate_data = np.array(generate_rate().values())
print ('cate data')
cate_data = np.array(generate_cate_vec().values())


print ('ngb_cate_data..')

cls_idx = {}
for l in set(ngb_label):
    cls_idx[l] = np.argwhere(ngb_label == l).T[0]

cls_cate_arr = {}
cls_ckin_arr = {}
for l in set(ngb_label):
    cls_cate_arr[l] = cate_data[cls_idx[l]]
    cls_ckin_arr[l] = checkin_data[cls_idx[l]]

def generate_ngb_cache():
    ngb_cate_data = []
    ngb_ckin_data = []
    for idx in xrange(len(vec)):
        print('\r %d'%idx, end='')
        l = ngb_label[idx]
        ngb_cate_data.append(cls_cate_arr[l])
        ngb_ckin_data.append(cls_ckin_arr[l])
    
    return np.array(ngb_cate_data),  np.array(ngb_ckin_data)

ngb_cate_data, ngb_ckin_data = generate_ngb_cache()

# generate average category number in RADIUS
print ('\ncatengb_mat..')
def generate_catengb_mat():
    dim = cate_data.shape[1]
    catengb_mat = np.zeros((dim, dim))
    catengb_cnt_mat = np.zeros((dim, dim))

    #cache for the same category in the same cluster
    cache_mat = {}
    cache_cnt_mat = {}
    for l in set(ngb_label):
        cache_mat[l] = [None for i in xrange(dim)]
        cache_cnt_mat[l] = [None for i in xrange(dim)]

    for idx in xrange(len(ori_geom_vec)):
        print('\r %d'%idx, end='')
        ngb_cate_arr = ngb_cate_data[idx]
        cate_arr = cate_data[idx]
        idx_l = ngb_label[idx]
        
        for dr in xrange(dim):
            if cate_arr[dr]!=0.:
                #check cache
                if cache_mat[idx_l][dr] is None:
                    cache_mat[idx_l][dr] = np.zeros((dim, dim))
                    cache_cnt_mat[idx_l][dr] = np.zeros((dim, dim))
                    for dc in xrange(dim):
                        cache_cnt_mat[idx_l][dr][dr, dc] += 1
                        col = ngb_cate_arr[:,dc]
                        cache_mat[idx_l][dr][dr, dc] += col[col!=0.].shape[0]
                
                catengb_mat += cache_mat[idx_l][dr]
                catengb_cnt_mat += cache_cnt_mat[idx_l][dr]
    
    ret_mat = catengb_mat/catengb_cnt_mat
    ret_mat[np.isnan(ret_mat)] = 0.
    return ret_mat

avg_catengb_data = generate_catengb_mat()

cate_cnt = np.array([ np.count_nonzero(cate_data[:,col]) for col in xrange(cate_data.shape[1]) ])
cls_cate_cnt = {}
for l in set(ngb_label):
    mat = cls_cate_arr[l]
    cls_cate_cnt[l] = np.array([ np.count_nonzero(mat[:,col]) for col in xrange(mat.shape[1]) ])

def cal_k_beta(beta_idx, gamma_idx):
    N = len(ori_geog_vec)
    N_beta = cate_cnt[beta_idx]
    N_gamma = cate_cnt[gamma_idx]
    
    tmp_sum = 0.
    for p in xrange(len(cate_data)):
        p_l = ngb_label[p]
        if cate_data[p][beta_idx] != 0.:
            Np = len(cls_idx[p_l])
            Np_gamma = cls_cate_cnt[p_l][gamma_idx]
            Np_beta = cls_cate_cnt[p_l][beta_idx]
            tmp_sum += Np_gamma / (Np - Np_beta) if Np != Np_beta else 0.
    
    return tmp_sum * (N - N_beta) / (N_beta * N_gamma)

print ('\ncache_k_beta..')
cache_k_beta = np.zeros((cate_data.shape[1],cate_data.shape[1]))
for i in xrange(cate_data.shape[1]):
    print('\r %d'%i, end='')
    for j in xrange(cate_data.shape[1]):
        cache_k_beta[i,j] = cal_k_beta(i,j)
        
def cal_geo_features(idx):
    dim = cate_data.shape[1]
    ngb_cate_arr = ngb_cate_data[idx]
    
    #f_{r}^D
    frd = ngb_cate_arr.shape[0]

    #f_{r}^{NE}
    frNE = 0.
    for d in xrange(dim):
        col = ngb_cate_arr[:,d]
        Nc = col[col!=0.].shape[0]
        if Nc != 0.:
            frNE += -1. * (Nc/frd) * np.log(Nc/frd)
    
    #f_{r}^{Com}
    frCom = ngb_cate_arr[np.sum(ngb_cate_arr * cate_data[idx]) != 0.].shape[0] / frd

    #f_{r}^{QJ}
    frQJ = 0.
    for d_gamma in xrange(dim): 
        if cate_data[idx][d_gamma] != 0.:
            for d_beta in xrange(dim):
                col = ngb_cate_arr[:, d_beta]
                N_beta = col[col!=0.].shape[0]
                N_beta_avg = avg_catengb_data[d_gamma, d_beta]
                k_beta_gamma = cache_k_beta[d_beta, d_gamma]
                if k_beta_gamma != 0.:
                    frQJ += np.log(k_beta_gamma) * (N_beta - N_beta_avg)
    
    #f_{r}^{CD}
    frCD = 0.
    for d_gamma in xrange(dim):
        if cate_data[idx][d_gamma] != 0.:
            col = ngb_cate_arr[:, d_gamma]
            N_gamma = col[col!=0.].shape[0]
            for d_beta in xrange(dim):
                col = ngb_cate_arr[:, d_beta]
                N_beta = col[col!=0.].shape[0]
                N_gamma_avg = avg_catengb_data[d_beta, d_gamma]
                N = frd
                frCD += N_beta * N_gamma_avg / float(N * N_gamma)

    return np.array([ frd, frNE, frCom, frQJ, frCD ])
                
def cal_mob_features(idx):
    ngb_ckin_arr = ngb_ckin_data[idx]
    
    # f_r^{AP2}
    frAP = np.sum(ngb_ckin_arr)


    return np.array([frAP])

def save_features(features):
    size = len(features)
    with open('/data/dataset/processed/dianping_business_exp_features_%s_%s.json'%(distance_type, cluster_algorithm), 'w') as out:
        json.dump(features, out)

print('\nfeatures...')
geo_features_list = []
for bidx in xrange(len(ori_geog_vec)):
     
    print('\r %d'%bidx, end='')
    try:
        geo_feature = cal_geo_features(bidx)
        mob_feature = cal_mob_features(bidx)
        geo_features_list.append(np.concatenate((geo_feature, mob_feature), axis=0).tolist())
    except Exception, e:
        save_features(geo_features_list)
save_features(geo_features_list)




