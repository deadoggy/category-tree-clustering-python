#coding:utf-8

from matplotlib import pyplot as plt
import sys
import time
import json

keys = [ -1., 0., .02, .04, .06, .08, .1, .12, .14, .16, .18, .2, .4, .6, .8, 1.]
sigmas = [1., 0.1, 0.01, 0.001, 0.0001]

# max min
max_min_v = [[-0.1, 22] for i in xrange(len(sigmas))]

print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + " begin loading"
for key_index in xrange(len(keys)-1):
    count = 0
    with open(sys.path[0] + "/../distance_%f"%keys[key_index+1], 'r') as dist_in:
        print '=============================================='
        print 'distance_%f'%keys[key_index+1]
        line = dist_in.readline()
        while line!='':
            count += 1
            if count%1000000==0:
                print count
            line = line.split(',')
            for line_idx, str_v in enumerate(line):
                if line_idx<=2:
                    continue
                v = float(str_v)
                if v > max_min_v[line_idx-3][0]:
                    max_min_v[line_idx-3][0] = v
                
                if v < max_min_v[line_idx-3][1]:
                    max_min_v[line_idx-3][1] = v
            line = dist_in.readline()
print max_min_v

