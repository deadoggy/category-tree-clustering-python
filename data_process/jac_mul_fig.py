#coding:utf-8

from matplotlib import pyplot as plt
import sys
import time
import json
from matplotlib import ticker
import matplotlib
# jaccard similarity category
keys = [ -1., 0., .02, .04, .06, .08, .1, .12, .14, .16, .18, .2, .4, .6, .8, 1.]
sigmas = [1., 0.1, 0.01, 0.001, 0.0001]

# jac_stat = [0 for i in xrange(len(keys)-1)]
# vec_stat = [[0. for i in xrange(len(keys)-1)] for j in xrange(len(sigmas))]

# print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + " begin loading"
# for key_index in xrange(len(keys)-1):
#     count = 0
#     with open("/data/SDM_result/Jaccard/distance_%f"%keys[key_index+1], 'r') as dist_in:
#         print '=============================================='
#         print 'distance_%f'%keys[key_index+1]
#         line = dist_in.readline()
#         while line!='':
#             count += 1
#             if count%1000000==0:
#                 print count
#             line = line.split(',')
#             jac_stat[key_index] += 1
#             for line_idx, str_v in enumerate(line):
#                 if line_idx<=2:
#                     continue
#                 vec_stat[line_idx-3][key_index] += float(str_v)
#             line = dist_in.readline()
# for i in xrange(len(sigmas)):
#     for j in xrange(len(keys)-1):
#         vec_stat[i][j] /= jac_stat[j] if jac_stat[j] > 0 else 1
# print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + " begin drawing"

# with open("/data/SDM_result/Jaccard/amazon_distance_stat.json", "w") as dis_out:
#     out_dict = {"jac_stat":jac_stat, "vec_stat":vec_stat}
#     print out_dict
#     json.dump(out_dict, dis_out)

with open('/data/SDM_result/Jaccard/yelp_distance_stat.json', 'r') as distance_in:
    dist_json = json.load(distance_in)
    vec_stat = dist_json['vec_stat']
    jac_stat = dist_json['jac_stat']

font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 13}

matplotlib.rc('font', **font)

x_keys = [ str(keys[i]) for i in xrange(1, len(keys))]
#x_labels = [ "=0.00", "(0.00, 0.02]", "(0.02, 0.04]", "(0.04, 0.06]", "(0.06, 0.08]", "(0.08, 0.10]", "(0.10, 0.12]", "(0.12, 0.14]", "(0.14, 0.16]", "(0.16, 0.18]", "(0.18, 0.20]", "(0.20, 0.40]", "(0.40, 0.60]", "(0.60, 0.80]", "(0.80, 1.00]"]

x_labels = [ "0.00", "0.02", "0.04", "0.06", "0.08", "0.10", "0.12", "0.14", "0.16", "0.18", "0.20", "0.40", "0.60", "0.80", "1.00"]

non_x_labels = [" "," "," "," "," "," "," "," "," "," "," "," "," "," "," ",]
fig = plt.figure(figsize=(15,10))
ax = plt.subplot()
ax.bar(x_keys, jac_stat, width=-1, align='edge', color='#000000', edgecolor='#ffffff')
# for a, b in zip(x_keys, jac_stat):
#     ax.text(a, b+0.000000001, '%d'%b, ha='right', va= 'bottom',fontsize=11)
# ax.set_title('Jaccard Similarity Distribution', fontsize = 16)
# ax.set_xlabel('jaccard similarity')
# ax.set_ylabel('count')
ax.set_xticklabels(x_labels, rotation=45, horizontalalignment="center")
#plt.savefig('JaccardSimilarityDistribution.png')
plt.show()


# fig = plt.figure()
# ax1 = plt.subplot2grid((1, 10), (0, 0), colspan=2)
# ax2 = plt.subplot2grid((1, 10), (0, 2), colspan=2)
# ax3 = plt.subplot2grid((1, 10), (0, 4), colspan=2)
# ax4 = plt.subplot2grid((1, 10), (0, 6), colspan=2)
# ax5 = plt.subplot2grid((1, 10), (0, 8), colspan=2)

# axs = [ax1, ax2, ax3, ax4,ax5]


# fig.set_figwidth(18)
# fig.set_figheight(4)

# formatter = ticker.ScalarFormatter(useMathText=True)
# formatter.set_scientific(True) 
# formatter.set_powerlimits((-1,1)) 

# for d, ax in enumerate(axs):
#     if d>=len(vec_stat):
#         continue
    
#     i=d-1
#     y_step = int(max(vec_stat[i+1])/10)
#     y_label = [ j*y_step for j in xrange(10)]
#     ax.grid()
#     ax.bar(x_keys,vec_stat[i+1], width=-1., align='edge', color='#000000', edgecolor='#ffffff')
    
#     # if i > 2:
#     #     ax.set_xlabel('jaccard similarity', fontsize=13)
#     format_str = r"$\sigma$: %." + (str(d) if d>0 else str(d+1))
#     format_str +=  r"f"
#     ax.text(x=x_keys[-6], y=max(vec_stat[i+1])*0.7, s=format_str%sigmas[i+1], fontsize=14)
#     # ax.set_ylabel('average vuc distance',fontsize=14)
#     ax.set_yticklabels(y_label)
#     ax.set_xticklabels(x_labels, rotation=45, horizontalalignment="right", fontsize=10)
#     # if i> 2:
#     #     ax.set_xticklabels(x_labels, rotation=45, horizontalalignment="right", fontsize=14)
#     # else:
#     #     ax.set_xticklabels(non_x_labels)
#     ax.yaxis.set_major_formatter(formatter)

# plt.tight_layout()
# #plt.savefig('CateVecDist-Jaccard.png')
# plt.show()