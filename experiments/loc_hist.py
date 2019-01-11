#coding:utf-8

import sys
sys.path.append(sys.path[0] + '/../')
import numpy as np
from config.load_config import Config
import json
from matplotlib import pyplot as plt

config = Config().config

with open(config['processed_data_path'] + 'lasvegas_user_latlon.json') as vec_in:
    vec_data = json.load(vec_in)

dist = [0 for i in xrange(2000)]

for uid in vec_data.keys():
    item = vec_data[uid]
    num = len(vec_data[uid])
    try:
        dist[num] += 1
    except Exception, e:
        print num

plt.bar(range(2000), dist)
plt.show()



