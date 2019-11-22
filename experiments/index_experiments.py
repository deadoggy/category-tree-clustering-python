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

config = Config().config
dataloader = DataLoader()
sigma = config['sigma']
pivots = generate_category_tree(dataloader)


with open('testdata1000', 'r') as valid_uid_f:
        valid_uids = valid_uid_f.read().split('\n')
    
with open('testtruth', 'r') as valid_truth_f:
    y_truth = valid_truth_f.read().split('\n')
    
for i in xrange(len(y_truth)):
    if y_truth[i] == '':
        continue
    else:
        y_truth[i] = int(y_truth[i])

data = dataloader.load(vectorized_convertor, pivots=pivots, sigma=sigma, valid_uid=valid_uids)
def alg_runner(k):
    '''
        run algorithm of test data

        @k: int, number of partition to clustering

        #return: [data, y_labels, y_truth]
    '''
    print str(len(data))
    kmeans = KMeans(n_clusters=k, max_iter=500)
    y_labels = kmeans.fit_predict(data)
    return (data, y_labels, y_truth)


def index(cls_list):
    '''
        run index and generate logs

        @cls_list: list of (data, y_labels, y_truth)

        #return: void
    '''
    ssw_list = np.array([0.0 for i in xrange(len(cls_list))])
    ssb_list = np.array([0.0 for i in xrange(len(cls_list))])
    ch_list = np.array([0.0 for i in xrange(len(cls_list))])
    h_list = np.array([0.0 for i in xrange(len(cls_list))])
    kl_list = np.array([0.0 for i in xrange(len(cls_list))])
    bh_list = np.array([0.0 for i in xrange(len(cls_list))])
    xu_list = np.array([0.0 for i in xrange(len(cls_list))])
    dunn_list = np.array([0.0 for i in xrange(len(cls_list))])
    db_list = np.array([0.0 for i in xrange(len(cls_list))])
    bic_list = np.array([0.0 for i in xrange(len(cls_list))])
    sc_list = np.array([0.0 for i in xrange(len(cls_list))])
    rand_list = np.array([0.0 for i in xrange(len(cls_list))])


    ssw_log = 'ssw: '
    ssb_log = 'ssb: '
    ch_log = 'calinski_harabasz: '
    h_log = 'hartigan: '
    kl_log = 'krzanowski_lai: '
    bh_log = 'ball_hall: '
    xu_log = 'xu_index: '
    #dunn_log = 'dunn_index: '
    db_log = 'davies_bouldin: '
    bic_log = 'bic: '
    sc_log = 'sc: '
    rand_log = 'rand: '

    for i, res in enumerate(cls_list):
        print '=========================================================='
        print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + ' %d clusters'%(i+2)
        print '=========================================================='
        data = res[0]
        y_labels = res[1]
        y_truth = res[2]

        print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + ' ssw'
        ssw_list[i] = ssw(data, y_labels)
        print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) +  ' ssb'
        ssb_list[i] = ssb(data, y_labels)
        print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + ' ch'
        ch_list[i] = calinski_harabasz(data, y_labels)
        print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + ' h'
        h_list[i] = hartigan(data, y_labels)
        if i>1:
            print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + ' kl'
            y_labels_m1 = cls_list[i-1][1]
            y_labels_m2 = cls_list[i-2][1]
            kl_list[i] = krzanowski_lai(data, y_labels_m1, y_labels_m2, y_labels)
        print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + ' bh'
        bh_list[i] = ball_hall(data, y_labels)
        print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + ' xu'
        xu_list[i] = xu_index(data, y_labels)
        #print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + ' dunn'
        #dunn_list[i] = dunn_index(data, y_labels)
        print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + ' db'
        db_list[i] = davies_bouldin(data, y_labels)
        print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + ' bic'
        bic_list[i] = bic(data, y_labels)
        print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + ' sc'
        sc_list[i] = silhouette_score(data, y_labels)
        print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + ' rand'
        rand_list[i] = adjusted_rand_score(y_labels, y_truth)
    
    for i in xrange(len(cls_list)):
        ssw_log += str(ssw_list[i]) + ' '
        ssb_log += str(ssb_list[i]) + ' '
        ch_log += str(ch_list[i]) + ' '
        h_log += str(h_list[i]) + ' '
        kl_log += str(kl_list[i]) + ' '
        bh_log += str(bh_list[i]) + ' '
        xu_log += str(xu_list[i]) + ' '
        #dunn_log += str(dunn_list[i]) + ' '
        db_log += str(db_list[i]) + ' '
        bic_log += str(bic_list[i]) + ' '
        sc_log += str(sc_list[i]) + ' '
        rand_log += str(rand_list[i]) + ' '
    
    with open('log', 'w') as log_f:
        log_f.writelines([
            ssw_log + '\n',
            ssb_log + '\n',
            ch_log + '\n',
            h_log + '\n',
            kl_log + '\n',
            bh_log + '\n',
            xu_log + '\n',
            #dunn_log + '\n',
            db_log + '\n',
            bic_log + '\n',
            sc_log + '\n',
            rand_log + '\n'
        ])
    


cls_res = []
for k in xrange(2,25):
    print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + ' k:%d'%k
    cls_res.append(alg_runner(k))
print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + ' kmeans done'

index(cls_res)