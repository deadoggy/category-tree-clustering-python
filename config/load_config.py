#coding:utf-8
import json
import sys
class Config:

    def __init__(self):
        
        with open('/home/yinjia/category-tree-clustering/config/config.json') as f:
            config_json = f.read()
        
        self.config = json.loads(config_json)
