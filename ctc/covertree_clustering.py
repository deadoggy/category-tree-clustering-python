#coding:utf-8

import sys
sys.path.append(sys.path[0] + '/../')
from covertree.covertree import CoverTree
from covertree.node import Node
from density_covertree import DensityCoverTree
import numpy as np

def covertree_clustering(dct, k):
    '''
        run covertree clustering algorithm

        @dct: a density cover tree
        @k: number of clusters

        #return: [label_1, label_2, ...]
    '''

    #check dct and k
    if dct.__class__ != DensityCoverTree:
        raise Exception('arg#1 not a  density cover tree')
    if k<=0 or k>len(dct.level_stack[-1]):
        raise Exception('invalid k')

    # 1. find initial centers
    # 1.1 calculate all densities of nodes in first valid level
    candidate_centers = {}
    for level in dct.level_stack:
        #the first level that len(level) >= k or the first biggest level when max(len(level)) < k
        if len(level) >= k or (len(level)<k and len(level)==len(dct.level_stack[-1])):
            for n in level:
                density_n = dct.estimate_density(n)
                if not candidate_centers.has_key(density_n):
                    candidate_centers[density_n] = []
                candidate_centers[density_n].append(n)
            break
    sorted_densities = np.sort(candidate_centers.keys())
    
    # 1.2 find first k centers with biggest density
    result_set = {}
    k_size = 0
    for density_i in xrange(len(sorted_densities)-1, -1, -1):
        density = sorted_densities[density_i]
        quit_loop = False

        for center in candidate_centers[density]:
            result_set[center] = []
            k_size += 1
            if k_size >= k:
                quit_loop = True
                break
        if quit_loop:
            break
    
    # 2. assign all nodes to their nearest node
    dist = dct.dist_calculator
    centers = result_set.keys()
    labels = np.array([-1 for i in xrange(dct.size)])
    for n in dct.level_stack[-1]:
        clus = -1
        min_dist = float('inf')
        for i, c in enumerate(centers):
            dist_c_n = dist(c.val,n.val)
            if dist_c_n < min_dist:
                min_dist = dist_c_n
                clus = i
        labels[n.index] = clus
        for sn in n.same_val_set:
            labels[sn.index] = clus

    return labels