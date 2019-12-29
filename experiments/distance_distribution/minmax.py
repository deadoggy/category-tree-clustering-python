import numpy as np


dist_dim = 6
for fn in ['amazon_distance', 'yelp_distance']:
    print(fn)
    with open(fn) as fin:
        minarr = [1e10 for i in range(dist_dim)]
        maxarr = [-1e10 for i in range(dist_dim)]
        lc = 0
        line = fin.readline()
        while line!='':
            lc += 1
            if lc%100000==0:
                print(lc)
            data = map(lambda x:float(x), line.split(',')[2:])
            for i, d in enumerate(data):
                minarr[i] = min(d, minarr[i])
                maxarr[i] = max(d, maxarr[i])
            line = fin.readline()
        with open(fn+'minmax', 'w') as fout:
            fout.write(str(minarr) + '\n')
            fout.write(str(maxarr) + '\n')

