#coding:utf-8

import sys
sys.path.append(sys.path[0] + '/../')
from data_loader.data_loader import DataLoader
import unittest

class DataLoaderTester(unittest.TestCase):

    def test_load(self):
        loader = DataLoader()
        def convert_func(uid, business_dict, arg_dict):
            return {uid: business_dict.values()}
        
        data = loader.load(convert_func, arg1=1)
        print 'load done'
    

unittest.main()