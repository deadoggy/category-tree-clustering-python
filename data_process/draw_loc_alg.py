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

k = [ i for i in range(2, 72)]

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


formatter = ticker.ScalarFormatter(useMathText=True)
formatter.set_scientific(True) 
formatter.set_powerlimits((-1,1)) 

fig, axs = plt.subplots(nrows=3, ncols=2)
fig.set_size_inches(12, 9)
for didx, dataset in enumerate(['address','epsg3857']):
    for aidx, alg in enumerate(['KMeans','Spectral','Hierarchical']):
        sc_ax = axs[aidx][didx]
        mse_ax = sc_ax.twinx()
        sc_ax.set_title(dataset + ":" + alg, fontsize=10)
        mse_ax.set_title(dataset + ":" + alg, fontsize=10)
        sc_ax.grid('true', linestyle=":", linewidth=0.7)
        mse_ax.grid('true', linestyle=":", linewidth=0.7)
        mse_ax.spines['top'].set_visible(False)
        sc_ax.plot(k, log_data[dataset][alg]['sc'], linestyle='-', color='k', label='SC')
        if didx==0 and aidx==0:
            sc_ax.legend(loc='upper right', bbox_to_anchor=(0.1, 1.18),
               ncol=1, mode=None, borderaxespad=0., frameon=False , fontsize=12)
        mse_ax.plot(k, log_data[dataset][alg]['mse'], linestyle=':', color='k', label='MSE')
        mse_ax.yaxis.set_major_formatter(formatter)
        if didx==0 and aidx==0:
            mse_ax.legend(loc='upper right', bbox_to_anchor=(0.3, 1.18),
            ncol=1, mode=None, borderaxespad=0., frameon=False , fontsize=12)

plt.tight_layout()
plt.show()

