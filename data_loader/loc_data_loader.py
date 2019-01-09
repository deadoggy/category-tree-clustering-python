#coding:utf-8

import sys
sys.path.append(sys.path[0] + '/../')
from config.load_config import Config
from dist.vectorized_user_cate_dist import CateTreeNode, CateTree
import csv
import json
import time

# load location data by state,0 => city,1 => neighborhood,2 => street,3

class LocDataLoader:

    def __init__(self, business_file, user_business_file):
        '''
            init function of LocDataLoader

            @business_file: str, name of business_file
            @user_business_file: str, name of user_business_file
        '''

        self.config = Config().config
        self.business_file = self.config['processed_data_path'] + business_file
        self.user_business_file = self.config['processed_data_path'] + user_business_file

        with open(self.business_file) as business_in:
            self.business = json.load(business_in)


    def generate_pivots(self, top_level):
        '''
            generate pivots

            @top_level: int, state,0 => city,1 => neighborhood,2 => street,3

            #return: a list of pivots
        '''

        pivots_dict = {}
        for bid in self.business.keys():
            path = self.business[bid]
            name = path[top_level]
            if not pivots_dict.has_key(name):
                pivots_dict[name] = CateTree()
            pivots_dict[name].insert(path[top_level:])
        




