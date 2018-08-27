#coding:utf-8

from covertree.covertree import CoverTree
from covertree.node import Node
from covertree.density_covertree import DensityCoverTree

def covertree_clustering(dct, k):
    '''
        run covertree clustering algorithm

        @dct: a density cover tree
        @k: number of clusters

        #return: [[node_1, node_2, ...], [...], ..., [...]]
    '''

    #check dct and k
    if dct.__class__ != DensityCoverTree:
        raise Exception('arg#1 not a  density cover tree')
    if k<=0 or k>len(dct.level_stack):
        raise Exception('invalid k')