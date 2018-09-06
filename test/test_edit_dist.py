#coding:utf-8

import sys
sys.path.append(sys.path[0] + '/../')
from dist.bottom_up_edit_dist import *
import numpy as np
from data_loader.data_loader import DataLoader
import unittest
import random
from config.load_config import Config
import json
import Queue

class EditDistTest(unittest.TestCase):

    def setUp(self):
        self.data_loader = DataLoader()
        self.data = self.data_loader.load(bottomup_edit_dist_converter)
        config = Config().config
        self.data_file_name = config['data_file_name']
        self.cate_file_name = config['cate_file_name']

    def deep_copy_tree(self, t):
        uid = t.root.label
        with open(self.data_file_name) as user_data_f:
            user_data = json.load(user_data_f)[uid]
        bus_dict = {}
        for bid in user_data:
            bus_dict[bid] = self.data_loader.get_business_cate_path(bid)
        return bottomup_edit_dist_converter(uid, bus_dict, {})


    def test_edit_dist(self):
        
        random_index = int(random.random()*len(self.data))
        base_tree = self.data[random_index]

        # 1.dist(t1,t2) == dist(t2,t1)
        random_index_2 = int(random.random()*len(self.data))
        sec_tree = self.data[random_index_2]
        assert bottomup_edit_dist_calculator(sec_tree, base_tree) == bottomup_edit_dist_calculator(base_tree, sec_tree)

        # 2.same tree => dist==0
        mirror_tree = self.deep_copy_tree(base_tree)
        assert bottomup_edit_dist_calculator(mirror_tree, base_tree) == 0.0
        
        

        # 3.dist(t1,t2) + dist(t2,t3) >= dist(t1,t3)
        random_index_3 = int(random.random()*len(self.data))
        thd_tree = self.data[random_index_3]
        assert bottomup_edit_dist_calculator(base_tree, sec_tree) + bottomup_edit_dist_calculator(sec_tree, thd_tree) >= bottomup_edit_dist_calculator(base_tree, thd_tree)
        
        # 4.one empty and another not empty => dist == size(not empty tree)-1
        empty_tree = BUEditTree('empty')
        d = bottomup_edit_dist_calculator(empty_tree, base_tree)
        assert base_tree.size-1  == d
        

unittest.main()