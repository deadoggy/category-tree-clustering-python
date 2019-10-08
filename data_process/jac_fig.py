#coding:utf-8

from matplotlib import pyplot as plt
import sys
import time
import json
from matplotlib import ticker
import matplotlib
# jaccard similarity category
keys = [ -1., 0., .02, .04, .06, .08, .1, .12, .14, .16, .18, .2, .4, .6, .8, 1.]

dataset = 'amazon'
jac_stat = [0 for i in xrange(len(keys)-1)]
vec_stat = [0. for i in xrange(len(keys)-1)]

print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + " begin loading"
for key_index in xrange(len(keys)-1):
    count = 0
    with open("%s_distance_%f"%(dataset, keys[key_index+1]), 'r') as dist_in:
        print '=============================================='
        print '%s_distance_%f'%(dataset, keys[key_index+1])
        line = dist_in.readline()
        while line!='':
            count += 1
            if count%1000000==0:
                print count
            line = line.split(',')
            jac_stat[key_index] += 1
            for line_idx, str_v in enumerate(line):
                if line_idx<=2:
                    continue
                vec_stat[key_index] += float(str_v)
            line = dist_in.readline()
for j in xrange(len(keys)-1):
    vec_stat[j] /= jac_stat[j] if jac_stat[j] > 0 else 1
print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + " begin drawing"

with open("%s_distance_stat.json"%dataset, "w") as dis_out:
    out_dict = {"jac_stat":jac_stat, "vec_stat":vec_stat}
    print out_dict
    json.dump(out_dict, dis_out)

# with open('/home/yinjia/Documents/category-tree-clustering/%s_distance_stat.json'%dataset, 'r') as distance_in:
#     dist_json = json.load(distance_in)
#     vec_stat = dist_json['vec_stat']
#     jac_stat = dist_json['jac_stat']

# font = {'family' : 'normal',
#         'weight' : 'bold',
#         'size'   : 25}

# matplotlib.rc('font', **font)

# x_keys = [ str(keys[i]) for i in xrange(1, len(keys))]
# # #x_labels = [ "=0.00", "(0.00, 0.02]", "(0.02, 0.04]", "(0.04, 0.06]", "(0.06, 0.08]", "(0.08, 0.10]", "(0.10, 0.12]", "(0.12, 0.14]", "(0.14, 0.16]", "(0.16, 0.18]", "(0.18, 0.20]", "(0.20, 0.40]", "(0.40, 0.60]", "(0.60, 0.80]", "(0.80, 1.00]"]

# x_labels = [ "0.00", "0.02", "0.04", "0.06", "0.08", "0.10", "0.12", "0.14", "0.16", "0.18", "0.20", "0.40", "0.60", "0.80", "1.00"]

# # non_x_labels = [" "," "," "," "," "," "," "," "," "," "," "," "," "," "," ",]
# # fig = plt.figure(figsize=(15,10))
# # ax = plt.subplot()
# # ax.bar(x_keys, jac_stat, width=-1, align='edge', color='#000000', edgecolor='#ffffff')
# # # for a, b in zip(x_keys, jac_stat):
# # #     ax.text(a, b+0.000000001, '%d'%b, ha='right', va= 'bottom',fontsize=11)
# # # ax.set_title('Jaccard Similarity Distribution', fontsize = 16)
# # # ax.set_xlabel('jaccard similarity')
# # # ax.set_ylabel('count')
# # ax.set_xticklabels(x_labels, rotation=45, horizontalalignment="center")
# # #plt.savefig('JaccardSimilarityDistribution.png')
# # plt.show()


# fig = plt.figure()
# # ax1 = plt.subplot2grid((1, 8), (0, 0), colspan=2)
# # ax2 = plt.subplot2grid((1, 8), (0, 2), colspan=2)
# # ax3 = plt.subplot2grid((1, 8), (0, 4), colspan=2)
# # ax4 = plt.subplot2grid((1, 8), (0, 6), colspan=2)

# # axs = [ax1, ax2, ax3, ax4,]

# axs = [plt.subplot()] 

# fig.set_figwidth(15)
# fig.set_figheight(10)

# formatter = ticker.ScalarFormatter(useMathText=True)
# formatter.set_scientific(True) 
# formatter.set_powerlimits((-1,1)) 

# for d, ax in enumerate(axs):
#     if d>=len(vec_stat):
#         continue
    
#     y_step = int(max(vec_stat)/10)
#     y_label = [ j*y_step for j in xrange(10)]
#     ax.bar(x_keys,vec_stat, width=-1., align='edge', color='#696969', edgecolor='#ffffff')
#     # if i > 2:
#     #     ax.set_xlabel('jaccard similarity', fontsize=13)
#     # ax.text(x=x_keys[-6], y=max(vec_stat[i+1])*0.7, s=r"$\sigma$: %.3f"%sigmas[i+1])
#     # ax.set_ylabel('average vuc distance',fontsize=14)
#     ax.set_yticklabels(y_label)
#     ax.set_xticklabels(x_labels, rotation=45, horizontalalignment="right")
#     # if i> 2:
#     #     ax.set_xticklabels(x_labels, rotation=45, horizontalalignment="right", fontsize=14)
#     # else:
#     #     ax.set_xticklabels(non_x_labels)
#     ax.yaxis.set_major_formatter(formatter)

# plt.tight_layout()
# #plt.savefig('CateVecDist-Jaccard.png')
# plt.show()