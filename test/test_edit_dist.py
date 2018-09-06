#coding:utf-8

import sys
sys.path.append(sys.path[0] + '/../')
from dist.bottom_up_edit_dist import *
import numpy as np
from data_loader.data_loader import DataLoader
import unittest

class EditDistTest(unittest.TestCase):

    def setUp(self):
        self.data_loader = DataLoader()
        self.data = self.data_loader.load(bottomup_edit_dist_converter)

    def test_edit_dist(self):
        
        print 'begin'
        # same tree => dist==0


        # one empty and another not empty => dist == size(not empty tree)
        # dist(t1,t2) == dist(t2,t1)

unittest.main()