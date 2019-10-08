#coding:utf-8

from __future__ import division
from matplotlib import pyplot as plt
import sys
import time
import json
from matplotlib import ticker
import matplotlib
import numpy as np
    
dataset = 'amazon'

keys = [ -1., 0., .02, .04, .06, .08, .1, .12, .14, .16, .18, .2, .4, .6, .8, 1.]
sigmas = [1., 0.1, 0.01, 0.001, 0.0001]
# max min
max_min_v = [[-0.1, 100000000] for i in xrange(len(sigmas))]

print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + " begin loading"
for key_index in xrange(len(keys)-1):
    count = 0
    with open("/data/SDM_result/Jaccard/%s_distance_%f"%(dataset, keys[key_index+1]), 'r') as dist_in:
        print '=============================================='
        print 'distance_%f'%keys[key_index+1]
        line = dist_in.readline()
        while line!='':
            count += 1
            if count%1000000==0:
                print count
            line = line.split(',')
            for line_idx, str_v in enumerate(line):
                if line_idx<=2:
                    continue
                v = float(str_v)
                if v > max_min_v[line_idx-3][0]:
                    max_min_v[line_idx-3][0] = v
                
                if v < max_min_v[line_idx-3][1]:
                    max_min_v[line_idx-3][1] = v
            line = dist_in.readline()
print max_min_v

ctc_step = []
for maxmin in max_min_v:
    ctc_step.append((maxmin[0] - maxmin[1])/20.)
ctc_dist_data = [[0 for i in xrange(20)] for idx in xrange(len(sigmas))]


print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + " begin loading"
for key_index in xrange(len(keys)-1):
    count = 0
    with open("/data/SDM_result/Jaccard/%s_distance_%f"%(dataset,keys[key_index+1]), 'r') as dist_in:
        print '=============================================='
        print 'distance_%f'%keys[key_index+1]
        line = dist_in.readline()
        while line!='':
            count += 1
            if count%1000000==0:
                print count
            line = line.split(',')
            for line_idx, str_v in enumerate(line):
                if line_idx<=2:
                    continue
                v = float(str_v)
                min_v = max_min_v[line_idx-3][1]
                step = ctc_step[line_idx-3]
                ctc_dist_data[line_idx-3][int(np.floor(v//step))] += 1
                # for i in xrange(0, 20):
                #     if (v >= min_v + i*step and v< min_v + (i+1)*step) or v == max_min_v[line_idx-3][0]:
                #         ctc_dist_data[line_idx-3][i] += 1
            line = dist_in.readline()

with open("/data/SDM_result/Jaccard/_ctc_distribution_out.json"%dataset, "w") as ctc_distri_out:
    json.dump({"ctc": ctc_dist_data}, ctc_distri_out) 

# ctc_dist_data = [[448509896, 59902, 0, 149765, 0, 1228065, 205, 0, 0, 0, 0, 0, 0, 0, 41, 0, 0, 0, 0, 29958], [447194038, 1315899, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 59902, 149755, 1257934, 0, 0, 0, 10, 294], [441917855, 1220542, 2318896, 242124, 417838, 120272, 132, 59605, 89364, 149642, 477709, 521, 26, 2911880, 45829, 205, 788, 1573, 0, 3031], [414775504, 9348124, 4622166, 1609002, 1790567, 7142893, 9484007, 350804, 656909, 98772, 66954, 1291, 809, 29, 2, 14, 29217, 528, 238, 2], [273665474, 30766065, 24726337, 30910777, 62554694, 17907586, 5111368, 2616998, 837627, 503454, 183568, 96642, 34931, 31639, 631, 43, 110, 26636, 3224, 28]]

# font = {'family' : 'normal',
#         'weight' : 'normal',
#         'size'   : 13}
# matplotlib.rc('font', **font)



# fig = plt.figure()
# ax1 = plt.subplot2grid((1, 10), (0, 0), colspan=2)
# ax2 = plt.subplot2grid((1, 10), (0, 2), colspan=2)
# ax3 = plt.subplot2grid((1, 10), (0, 4), colspan=2)
# ax4 = plt.subplot2grid((1, 10), (0, 6), colspan=2)
# ax5 = plt.subplot2grid((1, 10), (0, 8), colspan=2)

# axs = [ax1, ax2, ax3, ax4, ax5]

# fig.set_figwidth(18)
# fig.set_figheight(4)

# formatter = ticker.ScalarFormatter(useMathText=True)
# formatter.set_scientific(True) 
# formatter.set_powerlimits((-1,1)) 


# for i, ax in enumerate(axs):
#     if i>=len(sigmas):
#         continue
#     min_v = max_min_v[i][1]
#     step = ctc_step[i]
#     x = [ "%.4f"%(min_v + j*step) for j in xrange(21)]
#     x_labels = [ "%.4f"%(min_v + j*step)  if (j)%5==0 or j==0 else "" for j in xrange(21)]
#     y = ctc_dist_data[i] + [0]
#     y_step = int(max(y)/10)
#     y_labels = [ j*y_step for j in xrange(10)]
#     ax.bar(x, y, width=1., align='edge', color='#696969',edgecolor='#ffffff')
#     # lv = -1.
#     # for zi, (a, b) in enumerate(zip(x, y)):
#     #     v = (b/100000000.)
#     #     ax.text(str(float(a)+(0.1*step if zi > 15 else -0.1*step)), b+0.000000001, '%.2f'%v if v>0.15 and abs(lv-v)>0.01  else " ", va= 'bottom',fontsize=12)
#     #     lv = v
#     # ax.set_xlabel('Vuc Distance',fontsize=14)
#     # ax.set_ylabel('count',fontsize=16)
#     ax.text(x=x[-8], y=max(y)*0.55, s="$\sigma$: %f"%sigmas[i])
#     ax.set_xticklabels(x_labels, rotation=30, fontsize=20)
#     ax.set_yticklabels(y_labels)
#     ax.yaxis.set_major_formatter(formatter)
    


# plt.tight_layout()
# plt.show()

