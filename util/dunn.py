import numpy as np

def _calculate_dist_mat(data, metric):
    '''
        calculate a distance matrix

        argv:
            @data:
                np.ndarray, shape=(N_datapoints, N_features)
            @metric:
                callable, take two obj as two data points and return a double as distance
    
        return:
            np.ndarray, shape=(N_datapoints, N_datapoints)
    '''
    mat = np.zeros((data.shape[0], data.shape[0]))
    for i in range(data.shape[0]):
        for j in range(i, data.shape[0]):
            mat[i][j] = mat[j][i] = metric(data[i], data[j])
    return mat

def dunn_index(data, label, metric=None):
    '''
        calculate dunn index, ref:
        J. C. Dunn† (1974) Well-Separated Clusters and Optimal Fuzzy Partitions, Journal of Cybernetics, 4:1, 95-104, DOI: 10.1080/01969727408546059
        WB-index: A sum-of-squares based index for cluster validity
        argv:
            @data:
                np.ndarray, if metric=='precomputed', then (N_datapoints, N_datapoints) distance metrix
                if metric==None/callable function, then shape=(N_datapoints,N_features)
            @label:
                np.ndarray, shape=(N,)
            @metric:
                'precomputed' / None / callable function
        
        return:
            float: dunn index
    '''

    if metric == 'precomputed':
        mat = data
    elif metric is None:
        mat = _calculate_dist_mat(data, lambda x,y: np.sqrt(np.sum((x-y)**2)))
    else:
        mat = _calculate_dist_mat(data, metric)
    
    unique_label = np.unique(label)

    # step.1 calculate min distance between clusters
    min_betcls_dist = np.inf
    for i in range(len(unique_label)):
        for j in range(i+1, len(unique_label)):
            i_label = unique_label[i]
            j_label = unique_label[j]

            row_idx = np.where(label==i_label)[0]
            col_idx = np.where(label==j_label)[0]
            ij_min = np.min(mat[row_idx, :][:, col_idx])

            min_betcls_dist = min(min_betcls_dist, ij_min)
    
    # step.2 calculate max distance within cluster
    max_incls_dist = -np.inf
    for i, l in enumerate(unique_label):
        rowcol_idx = np.where(label==l)[0]
        i_max = np.max(mat[rowcol_idx,:][:,rowcol_idx])

        max_incls_dist = max(max_incls_dist, i_max)
    
    # step.3 return dunn index
    return min_betcls_dist/max_incls_dist