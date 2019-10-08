import json
import random

MAX_SIZE = 30000
MIN_PDT = 5
DATASET = 'yelp'
#USER_BUSINESS_FILE = '/data/rec_dataset/amazon/amazon_user_business_line.json'
USER_BUSINESS_FILE = '/data/rec_dataset/yelp/processed/user_business_line.json'
OUTPUT_FILE = '%s_dist_ub_line.json'%DATASET

# find all users with at least MIN_PDT products
user_set = []
with open(USER_BUSINESS_FILE) as ubin:
    line = ubin.readline()
    while line != '':
        item = json.loads(line)
        if len(item['business']) > MIN_PDT:
            user_set.append(item)
        line = ubin.readline()

# sampling 
print(len(user_set))
sampling_rlt = []
for idx, item in enumerate(user_set):
    if idx < MAX_SIZE:
        sampling_rlt.append(item)
    else:
        rdv = random.randint(0, len(user_set))
        if rdv < MAX_SIZE:
            sampling_rlt[rdv] = item

with open(OUTPUT_FILE, 'w') as out:
    for item in sampling_rlt:
        out.write(json.dumps(item) + '\n')


