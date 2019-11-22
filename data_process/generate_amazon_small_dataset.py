#coding:utf-8


import json


UID_FILE_PATH_LS = [
    '/home/yinjia/experiment_dataset/clustering/AMAZON_1000_600_600_800',
    '/home/yinjia/experiment_dataset/clustering/AMAZON_1000_50_550_1400',
    '/home/yinjia/experiment_dataset/clustering/AMAZON_2000_200_300_500',
    '/home/yinjia/experiment_dataset/clustering/AMAZON_200_400_100_300_800_600_750_150_900',
    '/home/yinjia/experiment_dataset/clustering/YELP_1000_600_600_800',
    '/home/yinjia/experiment_dataset/clustering/YELP_1000_50_550_1400',
    '/home/yinjia/experiment_dataset/clustering/YELP_2000_200_300_500',
    '/home/yinjia/experiment_dataset/clustering/YELP_200_400_100_300_800_600_750_150_900',
]
USER_BUSINESS_PATH_LS = [
    '/data/rec_dataset/amazon/amazon_user_business_line.json',
    '/data/rec_dataset/yelp/processed/user_business_line.json'
]

OUTPUT_FILE_PATH_LS = [
    '/home/yinjia/experiment_dataset/clustering/amazon_s1_user_business_line.json',
    '/home/yinjia/experiment_dataset/clustering/amazon_s2_user_business_line.json',
    '/home/yinjia/experiment_dataset/clustering/amazon_s3_user_business_line.json',
    '/home/yinjia/experiment_dataset/clustering/amazon_s4_user_business_line.json',
    '/home/yinjia/experiment_dataset/clustering/yelp_s1_user_business_line.json',
    '/home/yinjia/experiment_dataset/clustering/yelp_s2_user_business_line.json',
    '/home/yinjia/experiment_dataset/clustering/yelp_s3_user_business_line.json',
    '/home/yinjia/experiment_dataset/clustering/yelp_s4_user_business_line.json'
]

AMAZON_UB = {}
YELP_UB = {}

for i in range(4,8):
    print i
    UID_FILE_PATH = UID_FILE_PATH_LS[i]
    USER_BUSINESS_PATH = USER_BUSINESS_PATH_LS[0 if i < 4 else 1]
    OUTPUT_FILE_PATH = OUTPUT_FILE_PATH_LS[i]

    valid_uid = []
    with open(UID_FILE_PATH) as valid_uid_in:
        line = valid_uid_in.readline().strip()
        while line!="":
            valid_uid.append(line)
            line = valid_uid_in.readline().strip()

    user_business = AMAZON_UB if i < 4 else YELP_UB
    if len(user_business)==0:
        with open(USER_BUSINESS_PATH) as user_business_in:
            line = user_business_in.readline()
            while line!='':
                item = json.loads(line)
                user_business[item['uid']] = item['business']
                line = user_business_in.readline()

    print len(user_business)

    with open(OUTPUT_FILE_PATH, 'a') as output_f:
        for item in valid_uid:
            output_f.write(json.dumps({'uid':item, 'business':user_business[item]}))
            output_f.write('\n')
        

