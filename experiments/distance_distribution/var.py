# calcuate variance

import numpy as np

fns = ['amazon_distance', 'yelp_distance']
dist_dim = 6
for fn in fns:
    print(fn)

    # D(X) = E(X^2) - [E(X)]^2
    line_cnt = 0.
    xp2_sum = np.array([0. for i in range(dist_dim)])
    x_sum = np.array([0. for i in range(dist_dim)])
    with open(fn) as fin:
        line = fin.readline()
        while line!='':
            line_cnt += 1
            if line_cnt%1000000==0:
                print(line_cnt)
            dists = line.split(',')[2:]
            dists = np.array(list(map(lambda x:float(x), dists)))
            xp2_sum += dists**2
            x_sum += dists
            line = fin.readline()
    D = xp2_sum/line_cnt - (x_sum/line_cnt)**2
    with open(fn+'var', 'w') as var_out:
        var_out.write(str(D.tolist()))
    with open(fn+'mean', 'w') as mean_out:
        mean_out.write(str((x_sum/line_cnt).tolist()))

