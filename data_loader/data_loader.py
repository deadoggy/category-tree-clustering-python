#coding:utf-8

from config.load_config import Config
import csv
import json

class DataLoader:

    def __init__(self):
        '''
            load config and category information from processed data
        '''

        #load config
        config = Config().config
        self.data_file_name = config['data_file_name']
        self.cate_file_name = config['cate_file_name']
        self.business_file_name = config['business_file_name']

        #load category
        self.cate_parent = {}
        with open(self.cate_file_name) as cate_csv:
            try:
                cate_rec = csv.reader(cate_csv)
                for row in cate_rec:
                    self.cate_parent[row[0]] = row[1]
            except Exception, e:
                raise e
        
        #load business's category info
        with open(self.business_file_name) as businss_cate_json:
            self.business_cate = json.load(businss_cate_json)

    def get_cate_list(self, cate):
        '''
            get a category's category path from root category

            @cate: the most detailed category

            #return: [root, cate_1, cate_2, ..., cate]
        '''
        path = []
        p = cate
        while p is not None and p != '':
            path.insert(0,p)
            p = self.cate_parent[p]
        return path

    def get_business_cate_path(self, bs_name):
        '''
            get all category path of a business

            @bs_name: business name to get all category paths

            #return: [ [<path_1>], [<path_2>], ...]
        '''
        paths = []
        tail_cate = self.business_cate[bs_name]
        for tc in tail_cate:
            path = self.get_cate_list(tc)
            paths.append(path)
        return paths
    
    def get_all_cate_path(self):
        '''
            get all category paths

            #return [ [<path_1>], [<path_2>], ...]
        '''
        paths = []
        for bs in self.business_cate.keys():
            paths += self.get_business_cate_path(bs)
        return paths

    def load(self, convert_func, other_para={}):
        '''
            load a user's all category path
        
            @convert_func: convert function, to convert 
            category path to data point. Parameters of convert_func
            is: uid, business_categorypath_dict and a other_para. uid is
            the id of a user, business_categorypath_dict
            is a dict {business_1: [[path_1],[path_2],...], ...} and
            other_para is a list of other helpful parameters.
            Return of the fucntion is a data node
            @other_para: a dict of other parameters to deliver to convert_func

            #return: a list of data node
        '''
        if type(convert_func).__name__ != 'function':
            raise Exception('convert_func must be a function')
        if type(other_para) != list:
            raise Exception('other_para must be a list')

        with open(self.data_file_name) as user_data_f:
            user_data = json.load(user_data_f)
        
        ret_data = []
        for uid in user_data.keys():
            bus_dict = {}
            for bid in user_data[uid]:
                bus_dict[bid] = self.get_business_cate_path(bid)
            ret_data.append(convert_func(uid, bus_dict, other_para))
        return ret_data

        
