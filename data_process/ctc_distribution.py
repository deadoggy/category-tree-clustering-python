#coding:utf-8

from __future__ import division
from matplotlib import pyplot as plt
import sys
import time
import json

keys = [ -1., 0., .02, .04, .06, .08, .1, .12, .14, .16, .18, .2, .4, .6, .8, 1.]
sigmas = [1., 0.1, 0.01, 0.001, 0.0001]

# # max min
# max_min_v = [[-0.1, 22] for i in xrange(len(sigmas))]

# print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + " begin loading"
# for key_index in xrange(len(keys)-1):
#     count = 0
#     with open(sys.path[0] + "/../distance_%f"%keys[key_index+1], 'r') as dist_in:
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

max_min_v = [[0.135873, 0.0], [1.783011, 0.0], [4.546957, 4e-06], [4.473014, 0.0], [4.472136, 0.0]]

ctc_step = []
for maxmin in max_min_v:
    ctc_step.append((maxmin[0] - maxmin[1])/20)
ctc_dist_data = [[0 for i in xrange(20)] for idx in xrange(len(sigmas))]


print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + " begin loading"
for key_index in xrange(len(keys)-1):
    count = 0
    with open(sys.path[0] + "/../distance_%f"%keys[key_index+1], 'r') as dist_in:
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
                for i in xrange(0, 20):
                    if (v >= min_v + i*step and v< min_v + (i+1)*step) or v == max_min_v[line_idx-3][0]:
                        ctc_dist_data[line_idx-3][i] += 1
            line = dist_in.readline()

with open("ctc_distribution_out.json", "w") as ctc_distri_out:
    json.dump({"ctc": ctc_dist_data}, ctc_distri_out) 

# fig, axs = plt.subplots(nrows=2, ncols=3, figsize=(8,8))
# fig.set_figwidth(18)
# fig.set_figheight(12)
# axs = axs.flatten()

# for i, ax in enumerate(axs.tolist()):
#     if i>=len(sigmas):
#         continue
#     min_v = max_min_v[i][1]
#     step = step = ctc_step[i]
#     x = [ str(min_v + j*step) for j in xrange(20)]
#     x_labels = [ str(min_v + j*step) if j%5==0 else " " for j in xrange(20)]
#     y = ctc_dist_data[i]
#     ax.bar(x, y, width=1., align='edge', edgecolor='#ffffff')
#     ax.set_xlabel('category tree distance')
#     ax.set_ylabel('count')
#     ax.set_title("Sigma:%f"%sigmas[i])
#     ax.set_xticks(x_labels)

# plt.tight_layout()

