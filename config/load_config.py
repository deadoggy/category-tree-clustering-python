#coding:utf-8
import json

class Config:

    def __init__(self):
        
        with open('config.json') as f:
            config_json = f.read()
        
        self.config = json.loads(config_json)
