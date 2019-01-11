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

    def __init__(self, business_file, user_business_file, top_level):
        '''
            init function of LocDataLoader

            @business_file: str, name of business_file
            @user_business_file: str, name of user_business_file
            @top_level: int, state,0 => city,1 => neighborhood,2 => street,3
        '''

        self.config = Config().config
        self.business_file = self.config['processed_data_path'] + business_file
        self.user_business_file = self.config['processed_data_path'] + user_business_file
        self.top_level = top_level

        with open(self.business_file) as business_in:
            self.business = json.load(business_in)


    def generate_pivots(self):
        '''
            generate pivots

            #return: a list of pivots
        '''

        pivots_dict = {}
        for bid in self.business.keys():
            path = self.business[bid]
            name = path[self.top_level]
            if not pivots_dict.has_key(name):
                pivots_dict[name] = CateTree()
            pivots_dict[name].insert(path[self.top_level:])
        
        return pivots_dict.values()
    
    def load(self, convert_func, **kwargs):
        '''
            load a user's all location path
        
            @convert_func: convert function, to convert 
            category path to data point. Parameters of convert_func
            is: uid, business_loc_dict and a kwargs. uid is
            the id of a user, business_loc_dict
            is a dict {business_1: [loc_path], ...} and
            kwargs is a list of other helpful parameters.
            Return of the fucntion is a data node
            @kwargs: a dict of other parameters to deliver to convert_func 
            and some other parameters

            #return: a list of data node
        '''
        if type(convert_func).__name__ != 'function':
            raise Exception('convert_func must be a function')
        print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + ' begin loading...'
        with open(self.user_business_file) as user_data_in:
            user_data = json.load(user_data_in)
        
        valid_uid = kwargs['valid_uid'] if kwargs.has_key('valid_uid') else user_data.keys()
        data_size = kwargs['data_size'] if kwargs.has_key('data_size') else float('inf')
        #ret_data = [None for i in xrange(len(user_data.keys()))] if valid_uid is None else [None for i in xrange(len(valid_uid))]
        ret_data = {}

        for idx, uid in enumerate(valid_uid):
            if idx+1 > data_size:
                break
            if (idx + 1)%10000==0:
                print idx
            bus_loc_dict = {}
            for bid in user_data[uid]:
                bus_loc_dict[bid] = [self.business[bid][self.top_level:]]
            ret_idx = idx if len(valid_uid)==len(user_data) else valid_uid.index(uid)
            ret_data[uid] = convert_func(uid, bus_loc_dict, kwargs)
        print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + ' loading finished'
        return ret_data
