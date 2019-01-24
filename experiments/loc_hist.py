#coding:utf-8

import sys
sys.path.append(sys.path[0] + '/../')
import numpy as np
from config.load_config import Config
import json
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

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

exit()

xLocator   = MultipleLocator(1)
ax = plt.subplot()
#ax.grid()
xsticks = ["0", "1"] + [ '('+str(ranges[i][0]) + ',' + str(ranges[i][1]) + ']' for i in range(1,9) ]
ax.bar([i for i in range(9)], dist, color='k')
for zi, (x, y) in enumerate(zip([i for i in range(9)], dist)):
    ax.text(x-0.1, y+0.000000001, '%d'%y, va= 'bottom',fontsize=10)
ax.xaxis.set_major_locator(xLocator)
ax.set_xticklabels(xsticks, rotation=20, horizontalalignment="right", fontsize=10)
ax.set_title("Distribution of Users' Location Size")
ax.set_xlabel("Size of Users' Locations")
ax.set_ylabel("Size of Users")
plt.show()



