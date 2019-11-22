#coding:utf-8
import matplotlib.pyplot as plt
import numpy as np
import re
from matplotlib import ticker
    

k = [ str(i) for i in range(2, 30)]

#file_name = "/home/yinjia/Documents/randomRes/2018-12-17_randomdata5000_quality_exp.log"
#file_name = "/log/ctclog/2018-12-17_randomdata1000_quality_exp.log"
file_name = "/home/yinjia/log/bic_experiments.log"
with open(file_name, "r") as log_in:
    logs = log_in.read().split('\n')

#pattern = re.compile("k:.*?; dataset:.*?; alg:(.*?); distance_type:vec; runtime:.*?; sc:(.*?); mse:(.*?);")

pattern = re.compile("<(.*?)> k:.*? distance:eul sc:(.*?) mse:(.*?) cls")

data_dict = {
    "spectral":{
        "mse":[],
        "sc":[],
    },
    "cover-tree":{
        "mse":[],
        "sc":[],
    },
    "hierarchical":{
        "mse":[],
        "sc":[],
    }
}

for log_str in logs:
    if '' == log_str:
        continue
    content = pattern.findall(log_str)
    if 0==len(content):
        continue
    else:
        content = content[0]
    alg = content[0]
    sc = float(content[1])
    mse = float(content[2])

    data_dict[alg]['mse'].append(mse)
    data_dict[alg]['sc'].append(sc)


fig,axes = plt.subplots(nrows=3, ncols=1)
fig.set_size_inches(12, 9)
for idx, alg in enumerate(data_dict.keys()):
    ax = axes[idx]
    ax.set_title(alg)

    sc_ax  = ax
    mse_ax = sc_ax.twinx()   

    sc_ax.plot(k, data_dict[alg]['sc'], "k-o", linewidth = 1.5, label='SC')
    sc_ax.legend(loc='upper right', bbox_to_anchor=(0.1, 1.18),
               ncol=1, mode=None, borderaxespad=0., frameon=False , fontsize=12)
    mse_ax.plot(k, data_dict[alg]['mse'], "k-x", linewidth = 1.5, label='MSE')
    mse_ax.legend(loc='upper right', bbox_to_anchor=(0.3, 1.18),
               ncol=1, mode=None, borderaxespad=0., frameon=False , fontsize=12)
plt.tight_layout()
plt.show()