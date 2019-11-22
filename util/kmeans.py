#coding:utf-8
'''
    Our implementation of K-Means, which is a naive version. The implementations supplied by
    sklearn and scipy does not support customized distance metric.
'''
from __future__ import division
import numpy as np
import random

def generate_new_centers(dataset, labels, k):
    '''
        generate new centers from labels

        @dataset: list, shape = [N:x:2], where N=(Size of Data), x=(Size of locations of a user), 2=([x,y] of location)
        @labels: list, shape = [N:], labels of data point

        #return: list, shape = [k:x:2], where k=(Size of target clusters), x=(Size of locations of a cluster), 2=([x,y] of location)
    '''
    
    centers = [ [] for i in xrange(k) ]
    for idx, dp in enumerate(dataset):
        centers[labels[idx]].append(dp)
    return centers

def rand_center(dataset, k):
    '''
        generate the random dataset centers

        @dataset: list, shape = [N, x, 2], where N=(Size of Data), x=(Size of locations of a user), 2=([x,y] of location)
        @k: int, size of target clusters

        #return: list, shape = [k:x:2], where k=(Size of target clusters), x=(Size of locations of a user), 2=([x,y] of location)
    '''
    return random.sample(dataset, k)

def dist_metric(dp_1, dp_2):
    '''
        calculate distance between dp_1 and dp_2

        @dp_1: object, data point 1
        @dp_2: object, data point 2

        #return: float, distance between dp_1 and dp_2
    '''
    ret_dist = 0.
    for loc_1 in dp_1:
        for loc_2 in dp_2:
            nparr_loc_1 = np.array(loc_1)
            nparr_loc_2 = np.array(loc_2)
            ret_dist += np.sqrt(np.sum((nparr_loc_1-nparr_loc_2)**2))
    return ret_dist / (len(dp_1) * len(dp_2))

def KMeans(dataset, k, ctr_initializer, ctr_generator, dist, max_itrs = 300):
    '''
        process k-means on locations data set

        @dataset: list, shape=[N:x:2], N=(size of dataset), x=(a user's locations), 2=(location)
        @k: int, size of target clusters
        @ctr_initializer: callable, func to initialize k random centers, args=(dataset, k)
        @ctr_generator: callabel, func to generate new centers, args=(dataset, labels, k)
        @dist: callable, func to calculate distance between data points args=(dp_1, dp_2)
        @max_itrs: int, max times of iterations


        #return: list, shape=[N:], labels of data point
    '''
    labels = np.array([ -1 for i in xrange(len(dataset)) ])
    centers = ctr_initializer(dataset, k)
    labels_changed = True
    itrs = 0
    while itrs <= max_itrs and labels_changed:
        # print itrs
        labels_changed = False
        for idx, dp in enumerate(dataset): # assign each data point to the nearest center
        
            min_dist = float('inf'); min_label = -1
            for l, ctr in enumerate(centers):
                # print "==="
                # print len(ctr)
                # print "==="
                tmp_dist = dist(dp, ctr)
                if tmp_dist<min_dist:
                    min_dist=tmp_dist; min_label=l
            if min_label!= labels[idx]: # check if the clusters changes
                labels_changed = True
                labels[idx] = min_label
        centers = ctr_generator(dataset, labels, k)
        itrs += 1
    return labels

def test():
    '''
        test KMeans
    '''
    dataset = [
        [[1,2], [3,4], [0,1], [2,1]],
        [[1,0], [2,2], [1,1]],
        [[100, 90], [110, 100]],
        [[98, 100], [105, 97], [100, 120]]
    ]
    labels = KMeans(dataset, 2, rand_center, generate_new_centers, dist=dist_metric)
    print labels

if __name__=='__main__':
    test()