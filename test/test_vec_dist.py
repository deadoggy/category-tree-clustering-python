#coding:utf-8

import sys
sys.path.append(sys.path[0] + '/../')
from dist.vectorized_user_cate_dist import *
import unittest
from data_loader.data_loader import DataLoader
import random
import numpy as np


class VectorizedUserDistTester(unittest.TestCase):

    def setUp(self):
        self.data_loader = DataLoader()
        self.pivots = generate_category_tree(self.data_loader)
        self.data = self.data_loader.load(vectorized_convertor, pivots=self.pivots, sigma=0.0001)
    
    def test_dist(self):
        random_index = int(len(self.data)*random.random())
        for d_1 in self.data:
            d_2 = self.data[random_index]
            assert vectorized_dist_calculator(d_1, d_2) >=0 and vectorized_dist_calculator(d_1, d_2) <= np.sqrt(len(d_1))

unittest.main()