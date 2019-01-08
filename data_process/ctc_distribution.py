#coding:utf-8

from __future__ import division
from matplotlib import pyplot as plt
import sys
import time
import json
from matplotlib import ticker
    

keys = [ -1., 0., .02, .04, .06, .08, .1, .12, .14, .16, .18, .2, .4, .6, .8, 1.]
sigmas = [1., 0.1, 0.01, 0.001, 0.0001]

# max min
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
    ctc_step.append((maxmin[0] - maxmin[1])/20.)
ctc_dist_data = [[0 for i in xrange(20)] for idx in xrange(len(sigmas))]


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
#                 min_v = max_min_v[line_idx-3][1]
#                 step = ctc_step[line_idx-3]
#                 for i in xrange(0, 10):
#                     if (v >= min_v + i*step and v< min_v + (i+1)*step) or v == max_min_v[line_idx-3][0]:
#                         ctc_dist_data[line_idx-3][i] += 1
#             line = dist_in.readline()

# with open("ctc_distribution_out.json", "w") as ctc_distri_out:
#     json.dump({"ctc": ctc_dist_data}, ctc_distri_out) 

ctc_dist_data = [[534390996, 2070876, 6764093, 301003, 131899, 230493, 372, 131683, 185, 14, 5, 7, 1, 1, 1, 1, 1, 1, 98920, 33], [415440923, 78467737, 22419434, 9060403, 5703998, 3219736, 1220568, 728127, 4051654, 2267962, 473045, 615102, 220346, 85781, 83605, 30645, 31423, 77, 14, 5], [6375664, 24943945, 40634860, 57480966, 82319064, 88627002, 80337444, 60968270, 39833635, 23932038, 14699875, 9382119, 6196443, 3939129, 2278283, 1194167, 611744, 240879, 91353, 33705], [2942981, 1482805, 1366794, 1313180, 17332507, 7920130, 41349558, 57546936, 69045202, 73911667, 90559945, 68552591, 45762932, 27631628, 21864827, 7674252, 5708995, 1791902, 346390, 15382], [4649809, 530, 530, 530, 18808421, 530, 40622019, 63912796, 80764563, 1506610, 159769984, 59767986, 42279966, 27833421, 28433361, 6815203, 6693137, 1963564, 298321, 9355]]

fig = plt.figure()
ax1 = plt.subplot2grid((2, 6), (0, 0), colspan=2)
ax2 = plt.subplot2grid((2, 6), (0, 2), colspan=2)
ax3 = plt.subplot2grid((2, 6), (0, 4), colspan=2)
ax4 = plt.subplot2grid((2, 6), (1, 1), colspan=2)
ax5 = plt.subplot2grid((2, 6), (1, 3), colspan=2)

axs = [ax1, ax2, ax3, ax4, ax5]

fig.set_figwidth(18)
fig.set_figheight(12)

formatter = ticker.ScalarFormatter(useMathText=True)
formatter.set_scientific(True) 
formatter.set_powerlimits((-1,1)) 


for i, ax in enumerate(axs):
    if i>=len(sigmas):
        continue
    min_v = max_min_v[i][1]
    step = ctc_step[i]
    x = [ "%.4f"%(min_v + j*step) for j in xrange(21)]
    x_labels = [ "%.4f"%(min_v + j*step)  if (j)%5==0 or j==0 else "" for j in xrange(21)]
    y = ctc_dist_data[i] + [0]
    y_step = int(max(y)/10)
    y_labels = [ j*y_step for j in xrange(10)]
    ax.bar(x, y, width=1., align='edge', color='#696969',edgecolor='#ffffff')
    # lv = -1.
    # for zi, (a, b) in enumerate(zip(x, y)):
    #     v = (b/100000000.)
    #     ax.text(str(float(a)+(0.1*step if zi > 15 else -0.1*step)), b+0.000000001, '%.2f'%v if v>0.15 and abs(lv-v)>0.01  else " ", va= 'bottom',fontsize=12)
    #     lv = v
    if i > 2:
        ax.set_xlabel('Vuc Distance',fontsize=20)
    ax.set_ylabel('count',fontsize=16)
    ax.text(x=x[-6], y=max(y)*0.55, s="$\sigma$: %.4f"%sigmas[i], fontsize=25)
    ax.set_xticklabels(x_labels,fontsize=14)
    ax.set_yticklabels(y_labels, fontsize=15)
    ax.yaxis.set_major_formatter(formatter)
    


plt.tight_layout()
plt.show()

