#coding:utf-8


import json


UID_FILE_PATH = ''
USER_BUSINESS_PATH = ''
OUTPUT_FILE_PATH = ''

valid_uid = {}
with open(UID_FILE_PATH) as valid_uid_in:
    line = valid_uid_in.readline()
    while line!="":
        valid_uid[line] = ''
        line = valid_uid_in.readline()

valid_user = []
with open(USER_BUSINESS_PATH) as user_business_in:
    line = valid_uid_in.readline()
    while line!='':
        item = json.loads(line)
        if valid_uid.has_key(item['uid']):
            valid_user.append(item)
        line = valid_uid_in.readline()

with open(OUTPUT_FILE_PATH, 'w') as output_f:
    for item in valid_user:
        json.dump(item, output_f)
        output_f.write('\n')
        

