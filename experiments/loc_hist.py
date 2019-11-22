#coding:utf-8

import sys
sys.path.append(sys.path[0] + '/../')
import numpy as np
from config.load_config import Config
import json
from matplotlib import pyplot as plt
from matplotlib.ticker import *

config = Config().config

with open(config['processed_data_path'] + 'lasvegas_user_latlon.json') as vec_in:
    vec_data = json.load(vec_in)

dist = [0 for i in xrange(9)]
ranges = [[1., 1.], [1, 5], [5, 10], [10, 50], [50, 100], [100, 200], [200, 500], [500, 1000], [1000, 2000]]

sum_num = 0.

for uid in vec_data.keys():
    item = vec_data[uid]
    num = len(vec_data[uid])
    sum_num += num
    try:
        if num == 1:
            dist[0] += 1
        else:
            for i in xrange(1, 9):
                if num > ranges[i][0] and num <= ranges[i][1]:
                    dist[i]+=1
                    break
    except Exception, e:
        print num

print "users:%f; average numbers:%f"%(len(vec_data.keys()), sum_num / len(vec_data.keys())) 


formatter = ScalarFormatter(useMathText=False)
formatter.set_powerlimits((-1,1))
fig = plt.figure()
fig.set_size_inches(8,8)
ax = plt.subplot()
#ax.grid()
xsticks = [ "=1"] + [ '('+str(ranges[i][0]) + ',' + str(ranges[i][1]) + ']' for i in range(1,9) ]
ax.bar(xsticks, dist, width=-1., align='edge', color='#000000', edgecolor='#ffffff')
for x, y in zip(xsticks, dist):
    ax.text(x, y+0.000000001, '%d'%y, va= 'bottom',fontsize=10, ha='right')
# ax.xaxis.set_major_locator(xLocator)
ax.set_xticklabels(xsticks, rotation=17, horizontalalignment="right", fontsize=12)
ax.yaxis.set_major_formatter(formatter)
#ax.set_title("Distribution of Users' Location Size")
ax.set_xlabel("size of users' locations", fontsize=12)
ax.set_ylabel("size of users", fontsize=12)
ax.grid()
ax.spines['top'].set_visible(False)  #去掉上边框
ax.spines['right'].set_visible(False) #去掉右边框
plt.show()



