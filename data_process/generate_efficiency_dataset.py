import sys
sys.path.append(sys.path[0] + '/../')
from data_loader.data_loader import DataLoader
from copy import deepcopy, copy
from dist.vectorized_user_cate_dist import * 

import random
import json

dataloader = DataLoader()
print("load finished")

pivots = generate_category_tree(dataloader)
data = dataloader.load(vectorized_convertor, pivots=pivots)

with open('yelp_all.json', 'w') as out:
    for v in data:
        jsstr = json.dumps(v)
        out.write(jsstr)
        out.write('\n')
        
