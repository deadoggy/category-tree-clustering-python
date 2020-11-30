#coding:utf-8

from __future__ import division
from matplotlib import pyplot as plt
import sys
import time
import json
from matplotlib import ticker
import matplotlib
import numpy as np
    
dataset = 'yelp'

keys = [ -1., 0., .02, .04, .06, .08, .1, .12, .14, .16, .18, .2, .4, .6, .8, 1.]
sigmas = [0.001, 0.0001, 0.00001, 0.000001, 0.0000001, 0.00000001]
# max min
# max_min_v = [[-0.1, 100000000] for i in xrange(len(sigmas))]

# print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + " begin loading"
# for key_index in xrange(len(keys)-1):
#     count = 0
#     with open("/data/SDM_result/Jaccard/%s_distance_%f"%(dataset, keys[key_index+1]), 'r') as dist_in:
#         print '=============================================='
#         print 'distance_%f'%keys[key_index+1]
#         line = dist_in.readline()
#         while line!='':
#             count += 1
#             if count%1000000==0:
#                 print count
#             line = line.split(',')
#             for line_idx, str_v in enumerate(line):
#                 if line_idx<=2:
#                     continue
#                 v = float(str_v)
#                 if v > max_min_v[line_idx-3][0]:
#                     max_min_v[line_idx-3][0] = v
                
#                 if v < max_min_v[line_idx-3][1]:
#                     max_min_v[line_idx-3][1] = v
#             line = dist_in.readline()
# print max_min_v






# print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + " begin loading"
# for key_index in xrange(len(keys)-1):
#     count = 0
#     with open("/data/SDM_result/Jaccard/%s_distance_%f"%(dataset,keys[key_index+1]), 'r') as dist_in:
#         print '=============================================='
#         print 'distance_%f'%keys[key_index+1]
#         line = dist_in.readline()
#         while line!='':
#             count += 1
#             if count%1000000==0:
#                 print count
#             line = line.split(',')
#             for line_idx, str_v in enumerate(line):
#                 if line_idx<=2:
#                     continue
#                 v = float(str_v)
#                 min_v = max_min_v[line_idx-3][1]
#                 step = ctc_step[line_idx-3]
#                 #ctc_dist_data[line_idx-3][int(np.floor(v//step))] += 1
#                 for i in xrange(0, 20):
#                     if (v >= min_v + i*step and v< min_v + (i+1)*step) or v == max_min_v[line_idx-3][0]:
#                         ctc_dist_data[line_idx-3][i] += 1
#             line = dist_in.readline()

# with open("/data/SDM_result/Jaccard/%s_ctc_distribution_out.json"%dataset, "w") as ctc_distri_out:
#     json.dump({"ctc": ctc_dist_data}, ctc_distri_out) 


if 'yelp' == dataset:
    max_min_v = [[4.143863, 0.0], [4.582569, 0.0], [4.582321, 0.0], [4.582576, 0.0], [4.582576, 0.0], [4.582576, 0.0]]
else:
    max_min_v = [[3.2215, 0.0], [4.923029, 0.0], [5.862137, 0.0], [6.424258, 0.0], [6.598742, 0.0], [6.557439, 0.0]]

ctc_step = []
for maxmin in max_min_v:
    ctc_step.append((maxmin[0] - maxmin[1])/20.)
ctc_dist_data = [[0 for i in range(20)] for idx in range(len(sigmas))]

with open("/data/SDM_result/Jaccard/%s_ctc_distribution_out.json"%dataset) as ctc_distri_in:
    ctc_dist_data = json.load(ctc_distri_in)['ctc']

font = {'family' : 'serif',
        'weight' : 'normal',
        'size'   : 13}
matplotlib.rc('font', **font)



fig = plt.figure()
ax1 = plt.subplot2grid((1, 8), (0, 0), colspan=2)
ax2 = plt.subplot2grid((1, 8), (0, 2), colspan=2)
ax3 = plt.subplot2grid((1, 8), (0, 4), colspan=2)
ax4 = plt.subplot2grid((1, 8), (0, 6), colspan=2)
# ax5 = plt.subplot2grid((1, 10), (0, 8), colspan=2)
#ax6 = plt.subplot2grid((2, 6), (1, 4), colspan=2)
sigmas = ['$10^{-3}$', '$10^{-4}$','$10^{-5}$','$10^{-6}$',]

axs = [ax1, ax2, ax3, ax4, ]

fig.set_figwidth(12)
fig.set_figheight(3.5)

formatter = ticker.ScalarFormatter(useMathText=True)
formatter.set_scientific(True) 
formatter.set_powerlimits((-1,1)) 


for i, ax in enumerate(axs):
    if i>=len(sigmas):
        continue
    min_v = max_min_v[i][1]
    step = ctc_step[i]
    x = [ "%.4f"%(min_v + j*step) for j in range(21)]
    x_labels = [ "%.2f"%(min_v + j*step)  if (j)%5==0 or j==0 else "" for j in range(21)]
    y = ctc_dist_data[i] + [0]
    y_step = int(max(y)/10)
    y_labels = [ j*y_step for j in range(10)]
    # ax.grid()
    ax.bar(x, y, width=1., align='edge', color='#000000', edgecolor='#ffffff')
    # lv = -1.
    # for zi, (a, b) in enumerate(zip(x, y)):
    #     v = (b/100000000.)
    #     ax.text(str(float(a)+(0.1*step if zi > 15 else -0.1*step)), b+0.000000001, '%.2f'%v if v>0.15 and abs(lv-v)>0.01  else " ", va= 'bottom',fontsize=12)
    #     lv = v
    ax.set_xlabel('Proposed distance',fontsize=13)
    ax.set_ylabel('Numbers of user pairs',fontsize=13)
    ax.text(x=x[-9], y=max(y)*0.75, s="$\sigma$: "+sigmas[i],fontsize=13)
    ax.set_xticklabels(x_labels, rotation=30, fontsize=11)
    ax.set_yticklabels(y_labels, fontsize=11)
    ax.yaxis.set_major_formatter(formatter)
    


plt.tight_layout()
plt.show()

