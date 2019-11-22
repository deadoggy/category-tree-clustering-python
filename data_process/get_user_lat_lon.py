#coding:utf-8

import sys
sys.path.append(sys.path[0] + "/../")
import json
from config.load_config import Config
import gc

config = Config().config

business_latlon = {}
user_latlon = {}

all_bus = []
lasvegas_bus = {}
with open(config['original_data_path'] + 'business.json') as lb_in:
    line = lb_in.readline()
    while line != '':
        b = json.loads(line)
        if b['city'] == 'Las Vegas':
            lasvegas_bus[b['business_id']] = b
        line = lb_in.readline()

print 'done'

with open(config['processed_data_path'] + 'lasvegas_ub.json') as ub_in:
    lasvegas_ub = json.load(ub_in)

for uid in lasvegas_ub:
    bus_list = lasvegas_ub[uid]
    u_lat_lon_list = []
    for bid in bus_list:
        lat = lasvegas_bus[bid]['latitude']
        lon = lasvegas_bus[bid]['longitude']
        u_lat_lon_list.append([lat, lon])
    user_latlon[uid] = u_lat_lon_list

with open(config['processed_data_path'] + 'lasvegas_user_latlon.json', 'w') as out:
    json.dump(user_latlon, out)

