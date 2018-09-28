#coding:utf-8

import sys
sys.path.append(sys.path[0] + '/../')
from data_loader.data_loader import DataLoader

dataloader = DataLoader()

def transaction_sum(uid, bus_cate_dist, kwargs):
    bus_sum = len(bus_cate_dist.keys())
    if bus_sum >= 14 and bus_sum < 40:
        return uid
    else:
        return None

uids = dataloader.load(transaction_sum)
uids.remove(None)



with open('new_valid_uids.log', 'w') as f:
    for uid in uids:
        if uid is not None:
            f.write('%s\n'%uid)
