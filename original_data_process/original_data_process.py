#coding:utf-8

import sys
sys.path.append(sys.path[0] + '/../')
from config.load_config import Config
import json
import pandas as pd
import os

class OriginalDataProcessor:

    def __init__(self):
        self.__config = Config().config

    def processCategoryJson(self):
        #读取原始文件中的分类
        with open(self.__config['original_data_path'] + "categories.json") as f:
            categoryJson = f.read()
        originalCategory = json.loads(categoryJson)                                                                                       
        
        #把原始分类转换成csv
        title = []
        parents = []
        alias = []
        for cate in originalCategory:
            titles = cate['title'].split(", ")
            for t in titles:
                alias.append(cate['alias'])
                parents.append(cate['parents'][0] if len(cate['parents']) > 0 else '')
                title.append(t)
        
        titleToAliasFrame = pd.DataFrame(data=alias, columns=['alias'], index=title)
        aliasToParentsFrame = pd.DataFrame(data=parents, columns=['parents'], index=alias)
        os.mkdir(self.__config['processed_data_path'] + 'category/')
        titleToAliasFrame.to_csv(self.__config['processed_data_path']+'category/titleToAlias.csv')
        aliasToParentsFrame.to_csv(self.__config['processed_data_path']+'category/aliasToParents.csv')

    def generateBusinessData(self):
        '''
            把原始的business数据提取出category， id并形成新的json文件
            {
                id_1: [category_1, category_2, ...]
                id_2: [...]
            }
        '''

        #load business数据
        businessData = {}
        with open(self.__config['original_data_path' ]+'business.json','r') as bf:
            line = bf.readline()
            while line!='':
                bitem = json.loads(line)
                businessData[bitem['business_id']] = bitem['categories']
                line = bf.readline()
        
        #load category 的 titleToAlias 和 aliasToParent的数据
        aliasToParents = pd.read_csv(self.__config['processed_data_path']+'/category/aliasToParents.csv', index_col=0, quotechar="\"")
        titleToAlias = pd.read_csv(self.__config['processed_data_path']+'/category/titleToAlias.csv', index_col=0, quotechar="\"")

        '''
            获取一个cate的category 链条：
            [cate, ..., root]
        '''
        def getCateList(end):
            retList = []
            parent = end
            try:
                while not pd.isnull(parent):
                    retList.append(parent)
                    parent = aliasToParents.loc[parent, u'parents']
                    if type(parent)==pd.Series:
                        parent = parent[0]
            except Exception, e:
                print end, parent
            return retList

        #逐条处理business的category
        for id in businessData:
            old_cate = businessData[id]
            new_cate = []

            for title in old_cate:
                alias = ''

                #business数据中有些Category字典里没有
                try:
                    alias = titleToAlias.loc[title, u'alias']
                except Exception, e:
                    alias = ''
                if alias=='':
                    continue
                
                aliasCateList = getCateList(alias)
                opnext = {'append': True, 'remove': []}
                for tc in new_cate:
                    tcList = getCateList(tc)
                    #不添加
                    if tcList[-1]==aliasCateList[-1] and len(tcList)>=len(aliasCateList) and aliasCateList[0] in tcList:
                        opnext['append'] = False
                        break    
                    #添加， 但是检查是否用删除之前的cate
                    if tcList[-1]==aliasCateList[-1] and len(tcList)<=len(aliasCateList) and tcList[0] in aliasCateList:
                        opnext['remove'].append(tc)
                if opnext['append']:
                    new_cate.append(alias)
                for r in opnext['remove']:
                    new_cate.remove(r)

            businessData[id] = new_cate

        #持久化
        with open(self.__config['processed_data_path']+'business.json', 'w') as tbf:
            json.dump(businessData, tbf)
            
    def generatePurchaseData(self):
        userData = {}
        userCateData = {}
        with open(self.__config['original_data_path' ]+'review.json','r') as reviewFile:
            line = reviewFile.readline()
            while line!='':
                rec = json.loads(line)
                userData[rec['user_id']] = [rec['business_id']]
                line = reviewFile.readline()
        
        with open(self.__config['original_data_path' ]+'tip.json','r') as tipFile:
            line = tipFile.readline()
            while line!='':
                rec = json.loads(line)
                if userData.has_key(rec['user_id']):
                    userData[rec['user_id']].append(rec['business_id'])
                else:
                    userData[rec['user_id']] = [rec['business_id']]
                line = tipFile.readline()

        with open(self.__config['processed_data_path' ]+'business.json','r') as businessFile:
            businessCate = json.load(businessFile)
            for userId in userData:
                cate = []
                for business in userData[userId]:
                    cate += businessCate[business]
                userCateData[userId] = cate
        
        with open(self.__config['processed_data_path']+'user_business.json', 'w') as ubf:
            json.dump(userData, ubf)

        with open(self.__config['processed_data_path']+'purchase_'+str(len(userData))+'.json', 'w') as tpf:
            json.dump(userCateData, tpf)
    
    def getUserByCity(self, city):
        ret_users = {}
        with open(self.__config['processed_data_path' ]+'user_business.json','r') as user_business:
            with open(self.__config['processed_data_path' ]+'city_business.json','r') as city_business:
                business_list = json.load(city_business)[city]
                users = json.load(user_business)
                for user_id in users.keys():
                    in_city = False
                    for business in users[user_id]:
                        if business in business_list:
                            in_city=True
                            break
                    if in_city:
                        ret_users[user_id] = users[user_id]
        with open(self.__config['processed_data_path' ]+ city +'_user_business.json','w') as out:
            json.dump(ret_users, out) 

    

if __name__=='__main__':
    processor = OriginalDataProcessor()
    #processor.processCategoryJson()
    #processor.generateBusinessData()
    #processor.generatePurchaseData()
    processor.getUserByCity('Las Vegas')