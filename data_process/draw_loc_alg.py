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
k_label = [ str(i) if i==2 or i%5==0 else '' for i in range(2, 72) ]
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


formatter = ticker.ScalarFormatter(useMathText=False)
formatter.set_scientific(True) 
formatter.set_powerlimits((-1,1))


label_locator = ticker.MultipleLocator(.5e5)

fig, axs = plt.subplots(nrows=3, ncols=2)

fig.set_size_inches(12, 9)
for didx, dataset in enumerate(['address','epsg3857']):
    for aidx, alg in enumerate(['KMeans','Spectral','Hierarchical']):
        sc_ax = axs[aidx][didx]
        mse_ax = sc_ax.twinx()
        
        sc_ax.grid('true', linestyle=":", linewidth=0.7)
        mse_ax.grid('true', linestyle=":", linewidth=0.7)
        mse_ax.spines['top'].set_visible(False)
        sc_ax.plot(k, log_data[dataset][alg]['sc'], linestyle='-', color='k', label='SC')
        if didx==0 and aidx==0:
            sc_ax.legend(loc='upper right', bbox_to_anchor=(0.1, 1.18),
               ncol=1, mode=None, borderaxespad=0., frameon=False , fontsize=12)
        mse_ax.plot(k, log_data[dataset][alg]['mse'], linestyle=':', color='k', label='MSE')
        mse_ax.yaxis.set_major_formatter(formatter)
        if didx == 0:
            mse_ax.yaxis.set_major_locator(label_locator)
        
        mse_ax.set_xticklabels(k_label)
        if didx==0 and aidx==0:
            mse_ax.legend(loc='upper right', bbox_to_anchor=(0.3, 1.18),
            ncol=1, mode=None, borderaxespad=0., frameon=False , fontsize=12)
        
        if dataset=="address":
            tdataset = 'GeoGraphical'
        else:
            tdataset = 'GeoMetric'
        
        if alg=='KMeans':
            talg='kmeans'
        if alg=='Spectral':
            talg='spectral'
        if alg=='Hierarchical':
            talg='hierarchical'

        if aidx==0:
            yloc = 0.82
        elif aidx==1:
            yloc = 0.5
        else:
            yloc=0.2

        if didx==0:
            xloc=0.20
        else:
            xloc=0.64
        
        axv_k = '17' if aidx!=0 else '16'
        if aidx==0 and didx==0:
            fig.text(0.15, 0.90, 'k=16')
        elif aidx==1 and didx==0:
            fig.text(0.155, 0.57, 'k=17')
        elif aidx==2 and didx==0:
            fig.text(0.155, 0.25, 'k=17')

        if didx!=1:
            sc_ax.axvline(axv_k, color="#000000", linestyle=":")

        
        fig.text(xloc, yloc,tdataset + "+" + talg, fontsize=12)
        
        #sc_ax.set_title(tdataset + ":" + talg, fontsize=10)
        #mse_ax.set_title(tdataset + ":" + talg, fontsize=10)
        sc_ax.set_xlabel('K')
        sc_ax.set_ylabel('SC', rotation=90, fontsize=11)
        mse_ax.set_ylabel('MSE', rotation=90, fontsize=11)


plt.tight_layout()
plt.show()

