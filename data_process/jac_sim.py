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
sigmas = [0.001, 0.0001, 0.00001, 0.000001, 0.0000001, 0.00000001]

dataset = sys.argv[1]
if dataset == 'amazon':
    data_file_name = 'amazon_dist_ub_line.json'
    business_file_name = '/data/rec_dataset/amazon/amazon_business_category_line.json'
else:
    data_file_name = 'yelp_dist_ub_line.json'
    business_file_name = '/data/rec_dataset/yelp/processed/business_line.json'

dataloader = DataLoader(data_file_name=data_file_name, business_file_name=business_file_name)
pivots = generate_category_tree(dataloader)
def cluster_convertor(uid, bus_cate_dict, kwargs):
    ret = [ uid, bus_cate_dict.keys(), ]
    for sig in sigmas:
        kwargs['sigma'] = sig
        ret.append(vectorized_convertor(uid, bus_cate_dict, kwargs))
    return ret
data = dataloader.load(cluster_convertor, pivots = pivots)

valid_uid = []
valid_bus = []
sigma_data = [[], [], [], [], [], []]
for u in data:
    valid_uid.append(u[0])
    valid_bus.append(u[1])
    for i in range(len(sigmas)):
        sigma_data[i].append(u[i+2])

sigma_data = np.array(sigma_data)
for sig_idx in range(len(sigmas)):
    dim = sigma_data[sig_idx].shape[1]
    for dim_idx in range(dim):
        mean = np.mean(sigma_data[sig_idx][:,dim_idx])
        std_var = np.sqrt(np.var(sigma_data[sig_idx][:, dim_idx]))
        if std_var!=0.:
            sigma_data[sig_idx][:, dim_idx] = (sigma_data[sig_idx][:, dim_idx] - mean) / (np.sqrt(2) * std_var)

print ("++++++++++++++++++++ begin ++++++++++++++++++++++++++++++")
print (len(valid_uid))
# f_out = []
# for i in range(len(keys)-1):
#     f_out.append(open("/data/SDM_result/Jaccard/%s_distance_%f"%(dataset, keys[i+1]), 'a'))
f_out = open("/data/SDM_result/chi/%s_distance"%dataset, 'a')
for i in range(0,len(valid_uid)):
    print ('%s/%s'%(i, len(valid_uid)))
    for j in range(i+1, len(valid_uid)):
        # a = set(valid_bus[i])
        # b = set(valid_bus[j])
        # ab_inter = a.intersection(b)
        # jac_sim = len(ab_inter) / (len(a) + len(b) - len(ab_inter))

        # for k in range(len(keys)-1):
        #     low = keys[k]
        #     up = keys[k+1]
        #     if jac_sim > low and jac_sim <= up:
        #         out_pair = "%s,%s,%f"%(valid_uid[i], valid_uid[j], jac_sim)
        #         for p in range(len(sigmas)):
        #             out_pair += ",%f"%vectorized_dist_calculator(sigma_data[p][i], sigma_data[p][j])
        #         f_out[k].write(str(out_pair) + "\n")
        #         break
        out_pair = "%s,%s"%(valid_uid[i], valid_uid[j])
        for p in range(len(sigmas)):
            out_pair += ",%f"%vectorized_dist_calculator(sigma_data[p][i], sigma_data[p][j])
        f_out.write(out_pair + "\n")         

# for f in f_out:
#     f.close()
f_out.flush()
f_out.close()
