import sys
sys.path.append(sys.path[0] + '/../')
import numpy as np
from sklearn.cluster import KMeans, AgglomerativeClustering, SpectralClustering
from ctc.covertree_clustering import *
from ctc.density_covertree import *
from dist.vectorized_user_cate_dist import * 
from sklearn.metrics import silhouette_score, adjusted_rand_score, mean_squared_error, normalized_mutual_info_score
import json

def calculate_center(X, label, k):
    dim = X.shape[1]
    size = X.shape[0]
    centers = [np.zeros(dim) for i in range(k)]
    counter = [0 for i in range(k)]
    for idx in range(X.shape[0]):
        centers[label[idx]] += X[idx]
        counter[label[idx]] += 1
    
    for i in range(k):
        centers[i] /= counter[i]

    ret = np.array([centers[label[i]] for i in range(size)])

    return ret

def clusters_size(cls):
    labels = set(cls)
    rlt = []
    for l in labels:
        rlt.append(cls.tolist().count(l))
    return rlt

def load_truth(fn):
    truth = []
    with open(fn) as truth_in:
        line = truth_in.readlines()
    return np.array([t for t in map(lambda x: eval(x.strip()), line)])


def clustering(data, truth, sigma, fn):
    clustering_result = {
        "hac":{
            'sc':[],
            'ari': [],
            'clusters_size': [],
            'mse': [],
            'nmi': []
        },
        "kmeans": {
            'sc':[],
            'ari': [],
            'clusters_size': [],
            'mse': [],
            'nmi': []
        },
        "covertree": {
            'sc':[],
            'ari': [],
            'clusters_size': [],
            'mse': [],
            'nmi': []
        },
        "spec": {
            'sc':[],
            'ari': [],
            'clusters_size': [],
            'mse': [],
            'nmi': []
        }
    }

    data = np.exp(-np.power(data,2)/(2.*np.power(sigma,2)))
    calculator = vectorized_dist_calculator
    top_level = 5 
    density_tree = DensityCoverTree(calculator, top_level)
    for i, d in enumerate(data):
        density_tree.insert(Node(val=d, index=i))

    for k in range(2, 21):
        # truth
        print('===================================')
        print('k=%d'%k)
        print('===================================')

        print('hac')
        hacor = AgglomerativeClustering(n_clusters=k, linkage='average')
        hacor.fit(data)
        clustering_result['hac']['nmi'].append(normalized_mutual_info_score(truth, hacor.labels_.tolist()))
        clustering_result['hac']['ari'].append(adjusted_rand_score(truth, hacor.labels_.tolist()))
        clustering_result['hac']['sc'].append(silhouette_score(data, hacor.labels_.tolist()))
        clustering_result['hac']['mse'].append(mean_squared_error(data, calculate_center(data, hacor.labels_.tolist(), k)))
        clustering_result['hac']['clusters_size'].append(clusters_size(hacor.labels_))
        print('ari ' + str(clustering_result['hac']['ari'][-1]))
        print('sc ' + str(clustering_result['hac']['sc'][-1]))
        print('mse ' + str(clustering_result['hac']['mse'][-1]))
        print(clustering_result['hac']['clusters_size'][-1])

        print('kmeans')
        kmor = KMeans(n_clusters=k, tol=1e-200)
        kmor.fit(data)
        clustering_result['kmeans']['nmi'].append(normalized_mutual_info_score(truth, kmor.labels_.tolist()))
        clustering_result['kmeans']['ari'].append(adjusted_rand_score(truth, kmor.labels_.tolist()))
        clustering_result['kmeans']['sc'].append(silhouette_score(data, kmor.labels_.tolist()))
        
        clustering_result['kmeans']['mse'].append(mean_squared_error(data, calculate_center(data, kmor.labels_.tolist(), k)))
        clustering_result['kmeans']['clusters_size'].append(clusters_size(kmor.labels_))
        print('ari ' + str(clustering_result['kmeans']['ari'][-1]))
        print('sc ' + str(clustering_result['kmeans']['sc'][-1]))
        print('mse ' + str(clustering_result['kmeans']['mse'][-1]))
        print(clustering_result['kmeans']['clusters_size'][-1])

        print('covertree')
        ct_label = covertree_clustering(density_tree, k)
        clustering_result['covertree']['nmi'].append(normalized_mutual_info_score(truth, ct_label)) 
        clustering_result['covertree']['ari'].append(adjusted_rand_score(truth, ct_label))
        clustering_result['covertree']['sc'].append(silhouette_score(data, ct_label))
        clustering_result['covertree']['mse'].append(mean_squared_error(data, calculate_center(data, ct_label, k)))
        clustering_result['covertree']['clusters_size'].append(clusters_size(ct_label))
        print('ari ' + str(clustering_result['covertree']['ari'][-1]))
        print('sc ' + str(clustering_result['covertree']['sc'][-1]))
        print('mse '+ str(clustering_result['covertree']['mse'][-1]))
        print(clustering_result['covertree']['clusters_size'][-1])

        print('spectral')
        spector = SpectralClustering(n_clusters=k, gamma=0.5)
        spector.fit(data)
        clustering_result['spec']['nmi'].append(normalized_mutual_info_score(truth, spector.labels_.tolist()))
        clustering_result['spec']['mse'].append(mean_squared_error(data, calculate_center(data, spector.labels_, k)))
        clustering_result['spec']['ari'].append(adjusted_rand_score(truth, spector.labels_.tolist()))
        clustering_result['spec']['sc'].append(silhouette_score(data, spector.labels_.tolist()))
        clustering_result['spec']['clusters_size'].append(clusters_size(spector.labels_))
        print('ari ' + str(clustering_result['spec']['ari'][-1]))
        print('sc ' + str(clustering_result['spec']['sc'][-1]))
        print('mse '+ str(clustering_result['spec']['mse'][-1]))
        print(clustering_result['spec']['clusters_size'][-1])

    with open(fn, 'w') as out:
        json.dump(clustering_result, out)


sim_fn_format = '/home/yinjia/experiment_dataset/clustering/%s_%s_simlarity.json'
truth_fn_format = '/home/yinjia/experiment_dataset/clustering/%s_truth/%s_%s_truth'
sigmas = [
    1e-7,
    1e-5
]
for source_idx, source_tag in enumerate(['amazon', 'yelp']):
    if source_idx==0:
        continue
    for dataset_no in ['s1', 's2', 's3', 's4']:
        print('%s   %s'%(source_tag, dataset_no))
        data = []
        with open(sim_fn_format%(source_tag, dataset_no)) as simvec_in:
            lines = simvec_in.readlines()
            for l in lines:
                data.append([i for i in map(lambda x: eval(x), l.strip().split(' '))])
        data = np.array(data)
        truth = load_truth(truth_fn_format%(source_tag, source_tag, dataset_no))
        clustering(data, truth, sigmas[source_idx], 'uni_%s_%s_result.json'%(source_tag, dataset_no))

        
