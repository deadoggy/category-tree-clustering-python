import numpy as np
import math
import json


minmax_fns = ['amazon_distanceminmax', 'yelp_distanceminmax']
fns = ['amazon_distance', 'yelp_distance']
rg_size = 100
dist_dim = 6

def readminmax(fn):
    with open(fn) as fin:
        min_list = eval(fin.readline())
        max_list = eval(fin.readline())
    return (min_list, max_list)

rlt = {
}

for fidx in range(len(fns)):
    fn = fns[fidx]
    minmaxfn = minmax_fns[fidx]
    rlt[fn] = [ [0 for j in range(rg_size)] for i in range(dist_dim)]
    min_ls, max_ls = readminmax(minmaxfn)
    step = [ (max_ls[i]-min_ls[i])/rg_size for i in range(dist_dim)]
    with open(fn) as fin:
        line = fin.readline()
        while line!='':
            dists = map(lambda x:float(x), line.split(',')[2:])
            for i, d in enumerate(dists):
                idx = math.floor((d-min_ls[i])/step[i])
                if idx==rg_size:
                    idx -= 1
                rlt[fn][i][idx] += 1
            line = fin.readline()
with open('statistic', 'w') as fout:
    json.dump(rlt, fout)




