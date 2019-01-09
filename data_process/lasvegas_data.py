#coding:utf-8

import sys
sys.path.append(sys.path[0] + "/../")
import json
from config.load_config import Config
import gc

config = Config().config
# get business in las vegas, save and keep ids
with open(config['original_data_path'] + '/business.json') as business_in:
    all_business_str = business_in.read().split('\n')
lasvegas_buss = {}
buss_ids = {}
for idx, l in enumerate(all_business_str):
    if idx%10000==0:
        print idx
    if l=='':
        continue
    item = json.loads(l)
    if item['city'] == u'Las Vegas':

        state = item['state']
        city = item['city']
        neighborhood = item['neighborhood']
        full_address = item['address']
        first_space = full_address.find(' ')
        if first_space == -1:
            first_space = 0
        comma = full_address.find(',')
        if comma == -1:
            comma = len(full_address)
        address = full_address[first_space+1: comma]

        loc = [state, city, neighborhood, address]

        lasvegas_buss[item['business_id']] = loc
        buss_ids[item['business_id']] = True
    else:
        buss_ids[item['business_id']] = False
with open(config['processed_data_path'] + '/lasvegas_business.json', 'w') as business_out:
    json.dump(lasvegas_buss, business_out)


# print "review data"
# # get user who went to las vegas, save and keep ids
# u_b_dict = {}
# with open(config['original_data_path'] + '/review.json') as review_in:
#     line = review_in.readline()
#     count = 0
#     while line != '':
#         if line=='':
#             break
#         try:
#             item = json.loads(line)
#             user_id = item['user_id']
#             buss_id = item['business_id']
#             if buss_ids[buss_id]:
#                 if not u_b_dict.has_key(user_id):
#                     u_b_dict[user_id] = []
#                 u_b_dict[user_id].append(buss_id)
#         except Exception, e:
#             print line
#             print e.message
            
#         count += 1
#         if count%10000==0:
#             print count
#         line = review_in.readline()


# with open(config['original_data_path'] + '/lasvegas_ub.json', 'w') as ub_out:
#     json.dump(u_b_dict, ub_out)

