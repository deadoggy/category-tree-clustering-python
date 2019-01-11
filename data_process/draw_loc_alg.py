#coding:utf-8

from matplotlib import pyplot as plt
import sys
import time
import json
from matplotlib import ticker
import re

with open('/log/ctclog/geo_5000.log') as log_in:
    logs = log_in.read().split('\n')

pattern = re.compile('\[.*?\] \[INFO\] (.*?), (.*?), k=(.*?), sc=(.*?), mse=(.*?), ')

log_data = {
    'address': {
        'KMeans': {'sc':[], 'mse':[]},
        'Hierarchical': {'sc':[], 'mse':[]},
        'Spectral': {'sc':[], 'mse':[]}
    },
    'epsg3857': {
        'KMeans': {'sc':[], 'mse':[]},
        'Hierarchical': {'sc':[], 'mse':[]},
        'Spectral': {'sc':[], 'mse':[]}
    }
}

k = [ str(i) for i in range(2, 72)]

for l in logs:
    item = pattern.findall(l)
    if 0==len(item):
        continue
    else:
        item = item[0]
    
    alg = item[0]
    dataset = item[1]
    sc = float(item[3])
    mse = float(item[4])
    log_data[dataset][alg]['sc'].append(sc)
    log_data[dataset][alg]['mse'].append(mse)

plt.plot(k, log_data['address']['KMeans']['sc'])
plt.grid()
plt.show()

