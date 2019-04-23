#coding:utf-8

import json


rdtypes = ['St', 'Ln', 'Rt', 'Lane','Str.', 'Str', 'Rd', 'Cir', 
'Road', 'Street', 'Ave', 'Dr', 'Blvd', 'Avenue', 'Boulevard', 
'Drive','St.', 'Rd.', 'Hwy', 'Highway', 'Way', 'Pkwy', 'Cir', 'Ct']

drcttype = ['W', 'E', 'S', 'N']

numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

def find_number(addrls):
    for i, item in enumerate(addrls):
        if len(set(item).intersection(set(numbers))) > 0 and item.find('\\x') == -1 and 'Ste' not in addrls[i-1]:
            if type(addrls) != unicode:
                addrls.remove(item)
            return item
    return None

def find_direction(addrls):
    for item in addrls:
        for dr in drcttype:
            if item == dr or item == dr + ',':
                addrls.remove(item)
                return item
    return None

lv_bus = {}

with open("/data/dataset/original/business.json") as busin:
    line = busin.readline()
    while line!= '':
        busjson = json.loads(line)
        bid = busjson["business_id"]
        if busjson['city']=='Las Vegas':
            lv_bus[bid] = {
                'address': busjson['address'], 
                'neighborhood': busjson['neighborhood'],
                'stars': busjson['stars'],
                'review_count': busjson['review_count'],
                'is_open': busjson['is_open'],
                'longitude': busjson['longitude'],
                'latitude': busjson['latitude']
            }
        line = busin.readline()

# divide address into list, from neighborhood to No. 

for bid in lv_bus.keys():
    addrls = []
    if lv_bus[bid]['address']=='':
        lv_bus.pop(bid)
        continue

    ori_addr_list = lv_bus[bid]['address']
    if ori_addr_list.find(',') > 0:
        ori_addr_list = lv_bus[bid]['address'].split(',')
        if find_number(ori_addr_list[0]) is None and ori_addr_list[1].find('Ste')<0:
            ori_addr_list = ori_addr_list[1]
        else:
            ori_addr_list = ori_addr_list[0]

    ori_addr_list = ori_addr_list.split(' ')
    if '' in ori_addr_list: 
        ori_addr_list.remove('')
    for rd in rdtypes:
        for item in ori_addr_list:
            if rd in item:
                ori_addr_list.remove(item)
    
    num = find_number(ori_addr_list)
    if num is not None:
        addrls.insert(0, num)
    drc = find_direction(ori_addr_list)
    if drc is not None:
        addrls.insert(0, drc)
    
    while find_number(ori_addr_list) is not None:
        pass
    rd = ''.join(ori_addr_list)
    if rd.find(',')>0:
        rd = rd[0:rd.find(',')]
    addrls.insert(0, rd)

    addrls.insert(0, lv_bus[bid]['neighborhood'] if lv_bus[bid]['neighborhood'] != '' else u'None' )
    if '' in addrls:
        addrls.remove('')
    lv_bus[bid]['address'] = addrls
    
with open('/data/dataset/processed/lasvegas_business_info.json', 'w') as binout:
    json.dump(lv_bus, binout)
