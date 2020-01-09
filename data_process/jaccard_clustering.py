import numpy as np
from sklearn.cluster import SpectralClustering
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import KMeans
from sklearn.metrics import mean_squared_error
from sklearn.metrics import silhouette_score
from sklearn.metrics.cluster import adjusted_rand_score
import json


user_file_format = "/home/yinjia/experiment_dataset/clustering/%s_s%d_user_business_line.json"
truth_format = "/home/yinjia/experiment_dataset/clustering/%s%slabel"
output_dir = "/data/SDM_result/%s_s%d/jaccard_dist_mat_cls_rlt.json"
truth_midname=["_1000_600_600_800_", "_1000_50_550_1400_", "_2000_200_300_500_", "_200_400_100_300_800_600_750_150_900_"]

def clusters_size(label):
    unique_labels = set(label)
    return [label.tolist().count(l) for l in unique_labels]

def jaccard_dist(s1, s2):
    unique_s1 = set(s1)
    unique_s2 = set(s2)

    numerator = len(unique_s1.intersection(unique_s2))
    denominator = len(unique_s1) + len(unique_s2) - numerator

    return 1 - numerator/denominator

def rbf(dist):
    return np.exp(-(dist**2)/(2*(1.0**2)))



for dataset_tag in ['amazon', 'yelp']:
    for dataset_no in range(1,5):

        #load data
        user_data = []
        uids = []
        with open(user_file_format%(dataset_tag, dataset_no)) as user_in:
            line = user_in.readline()
            while line!='':
                item = json.loads(line)
                uids.append(item['uid'])
                user_data.append(item['business'])
                line = user_in.readline()
        
        #load truth
        truth = []
        with open(truth_format%(dataset_tag.upper(), truth_midname[dataset_no-1])) as truth_in:
            lines = truth_in.readlines()
            truth = list(map(lambda x:int(x), lines))
        
        #calculate distance matrix
        dist_mat = np.zeros((len(user_data), len(user_data)))
        for i in range(len(user_data)):
            for j in range(i+1, len(user_data)):
                dist_mat[i][j] = dist_mat[j][i] = jaccard_dist(user_data[i], user_data[j])
        
        # run clustering algorithm

        clustering_result = {
            "hac":{
                'sc':[],
                'ari': [],
                'clusters_size': []
            },
            "spec": {
                'sc':[],
                'ari': [],
                'clusters_size': []
            },
            "kmeans": {
                'sc':[],
                'ari': [],
                'clusters_size': []
            }
        }
        for k in range(2, 21):
            print('===================================')
            print('k=%d'%k)
            print('===================================')

            print('hac')
            hacor = AgglomerativeClustering(n_clusters=k, affinity='precomputed', linkage='average')
            hacor.fit(dist_mat)
            clustering_result['hac']['ari'].append(adjusted_rand_score(truth, hacor.labels_.tolist()))
            clustering_result['hac']['sc'].append(silhouette_score(dist_mat, hacor.labels_.tolist(),metric='precomputed'))
            clustering_result['hac']['clusters_size'].append(clusters_size(hacor.labels_))

            print('spectral')
            affinity_mat = rbf(dist_mat)
            spector = SpectralClustering(n_clusters=k, affinity="precomputed")
            spector.fit(affinity_mat)
            clustering_result['spec']['ari'].append(adjusted_rand_score(truth, spector.labels_.tolist()))
            clustering_result['spec']['sc'].append(silhouette_score(dist_mat, spector.labels_.tolist(), metric='precomputed'))
            clustering_result['spec']['clusters_size'].append(clusters_size(spector.labels_))
        with open(output_dir%(dataset_tag, dataset_no), 'w') as out:
            json.dump(clustering_result, out)