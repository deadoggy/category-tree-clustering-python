#coding:utf-8

from matplotlib import pyplot as plt
import sys
import time
import json
from matplotlib import ticker
import re

#distance + cluster alg
with open("/log/ctclog/2019-01-11_eff_efficiency_exp.log") as eff_in:
    eff_logs = eff_in.read().split('\n')

pattern = re.compile("load time:(.*?)s, KMeans:(.*?)s, Spectral:(.*?)s, Hierarchical:(.*?)s")
eff_data = {
    'Load': [],
    'KMeans': [],
    'Hierarchical': [],
    'Spectral': []
}

for l in eff_logs:
    item = pattern.findall(l)
    if len(item) != 0:
        item = item[0]
    else:
        continue

    load_time = float(item[0])
    km_time = float(item[1])
    hac_time = float(item[2])
    sp_time = float(item[3])
    eff_data['Load'].append(load_time)
    eff_data['KMeans'].append(km_time)
    eff_data['Hierarchical'].append(hac_time)
    eff_data['Spectral'].append(sp_time)



