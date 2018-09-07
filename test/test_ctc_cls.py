#coding:utf-8

import sys
sys.path.append(sys.path[0] + '/../')
from data_loader.data_loader import DataLoader
from covertree.covertree import CoverTree
from covertree.node import Node
from dist.bottom_up_edit_dist import *
from dist.vectorized_user_cate_dist import *
from ctc.density_covertree import DensityCoverTree
from ctc.covertree_clustering import covertree_clustering
import unittest

class ClusteringTest(unittest.TestCase):
    def setUp(self):
        self.data_loader = DataLoader()
        with open('testData1000','r') as valid_uid_f:
            self.valid_uid = valid_uid_f.read().split('\n')
    
    def test_vec_ctc(self):
        pivots = generate_category_tree(self.data_loader)
        data = self.data_loader.load(vectorized_convertor, pivots=pivots, sigma=0.0001, valid_uid=self.valid_uid)
        dct = DensityCoverTree(vectorized_dist_calculator, 3)
        for d in data:
            dct.insert(Node(val=d))
        
        for cls in covertree_clustering(dct, 4):
            assert len(cls) == 250


unittest.main()