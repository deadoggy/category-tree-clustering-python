#coding:utf-8

import sys
sys.path.append(sys.path[0] + '/../')
import unittest
from covertree.covertree import CoverTree
from covertree.node import Node
from ctc.density_covertree import DensityCoverTree
import numpy as np

def eul_dist(a,b):
    return np.sqrt(np.sum(np.square(a-b))) 

class CoverTreeTest(unittest.TestCase):

    def setUp(self):

        #read iris data from iris.data
        with open('iris.data') as iris_f:
            iris_data = iris_f.read().split('\n')
        self.data_sum = len(iris_data)
        #normalize to 0~1
        data = np.array([ [ float(line.split(',')[j]) for j in xrange(0,2) ] for line in iris_data])
        cols = data.shape[1]
        rows = data.shape[0]
        min_arr = np.array([ [ min(data[:,c]) for c in xrange(cols) ] for r in xrange(rows) ])
        max_arr = np.array([ [ max(data[:,c]) for c in xrange(cols) ] for r in xrange(rows) ])
        data = (data-min_arr)/(max_arr-min_arr)
        
        #insert to a cover tree
        self.cover_tree = DensityCoverTree(eul_dist, 0)

        for i in xrange(rows):
            n = Node(val=data[i])
            n.index = i
            self.cover_tree.insert(n)

    def test_covering(self):
        for i in xrange(len(self.cover_tree.level_stack)-1, 0, -1):
            for n in self.cover_tree.level_stack[i]:
                is_dist_valid = n.parent.self_chd is not n and n.dist_to_prt<np.power(2.0, self.cover_tree.top_level-(i-1))
                is_parent = n.parent.self_chd is n and n.dist_to_prt==0.0
                assert is_dist_valid or is_parent
    
    def test_separation(self):
        for l in xrange(len(self.cover_tree.level_stack)-1, 0, -1):
            level = self.cover_tree.level_stack[l]
            for i in xrange(len(level)-1):
                for j in xrange(i+1, len(level)):
                    assert eul_dist(level[i].val, level[j].val) > np.power(2.0, self.cover_tree.top_level-l)
    
    def test_nesting(self):
        sum_bottom_level = 0
        for n in self.cover_tree.level_stack[-1]:
            sum_bottom_level += len(n.same_val_set) + 1
        assert sum_bottom_level == self.data_sum

    def test_density(self):
        bottom_level = self.cover_tree.level_stack[-1]
        for level in self.cover_tree.level_stack:
            for n1 in level:
                count = 0

                for n2 in bottom_level:
                    if eul_dist(n1.val, n2.val) <= np.power(2.0, n1.level) :
                        count += 1
                        count += len(n2.same_val_set)
                density = self.cover_tree.estimate_density(n1)
                assert count == density


unittest.main()