#coding:utf-8

#reference: WB-index: A sum-of-squares based index for cluster validity

import numpy as np
import sklearn

def calculate_centers(data, y_labels):
    '''
        calculate centers of every data obj's partition, only support vector type

        @data: np.array, shape: [n_samples, n_features]
        @y_labels: np.array, shape: [n_samples, 1]

        #return: list, shape:[n_samples, n_features]
    '''

    n_cls = max(y_labels)
    n_features = len(data[0])
    centers = np.array([[0.0 for f in xrange(n_features)] for c in xrange(n_cls+1)])
    for i, d in enumerate(data):
        label = y_labels[i]
        centers[label] = np.add(centers[label], d)
    cen_size = np.array([ [ y_labels.tolist().count(i) if y_labels.tolist().count(i)!=0 else 1] for i in xrange(n_cls+1) ])
    centers /= cen_size
    return np.array([ centers[y_labels[i]] for i in xrange(len(y_labels)) ])

def ssw(data, y_labels):
    '''
        calculate ssw of clustering results, only support vector type

        @data: np.array, shape: [n_samples, n_features]
        @y_labels: np.array, shape: [n_samples, 1]

        #return ssw
    '''
    centers = calculate_centers(data, y_labels)
    ssw = 0.0
    for i, d in enumerate(data):
        if y_labels[i] == -1:
            continue
        ssw += np.sum((d-centers[i])**2)
    return ssw 

def ssb(data, y_labels):
    '''
        calculate ssb of clustering results, only support vector type

        @data: np.array, shape: [n_samples, n_features]
        @y_labels: np.array, shape: [n_samples, 1]

        #return ssb
    '''
    data = np.array(data)
    x_avg = np.sum(data, 0) / float(len(data))
    centers = calculate_centers(data, y_labels)
    ssb = 0.0
    for i, d in enumerate(data):
        if y_labels[i] == -1:
            continue
        c = centers[i]
        ssb += np.sum((c-x_avg)**2)
    return ssb

def calinski_harabasz(data, y_labels):
    '''
        calculate calinski_harabasz of clustering results, only support vector type

        @data: np.array, shape: [n_samples, n_features]
        @y_labels: np.array, shape: [n_samples, 1]

        #return: calinski_harabasz
    '''
    N = len(data)
    M = len(set(y_labels)) - (1 if -1 in y_labels else 0)
    SSB = ssb(data, y_labels)
    SSW = ssw(data, y_labels)
    return (SSB/(M-1))/(SSW/(N-M))

def hartigan(data, y_labels):
    '''
        calculate hartigan of clustering results, only support vector type

        @data: np.array, shape: [n_samples, n_features]
        @y_labels: np.array, shape: [n_samples, 1]

        #return: hartigan
    '''
    SSW = ssw(data, y_labels)
    SSB = ssb(data, y_labels)
    return np.log2(SSB/SSW)

def diff(data, y_labels_m1, y_labels_m2):

    SSW_m1 = ssw(data, y_labels_m1)
    SSW_m2 = ssw(data, y_labels_m2)
    D = len(data[0])
    M = len(set(y_labels_m2)) - (1 if -1 in y_labels_m2 else 0)
    return np.power(M-1, 2/D) * SSW_m1 - np.power(M, 2/D) * SSW_m2

def krzanowski_lai(data, y_labels_m1, y_labels_m2, y_labels_m3):
    '''
        calculate krzanowski_lai of clustering results, only support vector type

        @data: np.array, shape: [n_samples, n_features]
        @y_labels_m1: np.array, shape: [n_samples, 1]
        @y_labels_m2: np.array, shape: [n_samples, 1]
        @y_labels_m3: np.array, shape: [n_samples, 1]

        #return: krzanowski_lai
    '''

    diff_1 = np.abs(diff(data, y_labels_m1, y_labels_m2))
    diff_2 = np.abs(diff(data, y_labels_m2, y_labels_m3))

    return diff_1 / diff_2

def ball_hall(data, y_labels):
    '''
        calculate Ball&Hall of clustering results, only support vector type

        @data: np.array, shape: [n_samples, n_features]
        @y_labels: np.array, shape: [n_samples, 1]

        #return: Ball&Hall
    '''

    SSW = ssw(data, y_labels)
    M = len(set(y_labels)) - (1 if -1 in y_labels else 0)
    return SSW / M

def xu_index(data, y_labels):
    '''
        calculate xu_index of clustering results, only support vector type

        @data: np.array, shape: [n_samples, n_features]
        @y_labels: np.array, shape: [n_samples, 1]

        #return: xu_index
    '''

    D = len(data[0])
    N = len(data)
    M = len(set(y_labels)) - (1 if -1 in y_labels else 0) 
    SSW = ssw(data, y_labels)
    log = np.log2(np.sqrt(SSW/(D*N*N)))
    return D * log + np.log2(M)

def d_bew_centers(c_1, c_2):
    res = float('inf')
    for d1 in c_1:
        for d2 in c_2:
            tmp_d = np.power(d1-d2, 2)
            if tmp_d < res:
                res = tmp_d
    return res

def diam(c):
    res = -1.0
    for i in xrange(len(c)):
        for j in xrange(i+1, len(c)):
            tmp_d = np.power(c[i]-c[j], 2)
            if tmp_d > res:
                res = tmp_d
    return res

def dunn_index(data, y_labels):
    '''
        calculate dunn_index of clustering results, only support vector type

        @data: np.array, shape: [n_samples, n_features]
        @y_labels: np.array, shape: [n_samples, 1]

        #return: dunn_index
    '''

    centers = calculate_centers(data, y_labels)
    min_up = float('inf')
    for i in xrange(len(centers)):
        for j in xrange(i+1, len(centers)):
            tmp_min_up = d_bew_centers(centers[i], centers[j])
            if tmp_min_up < min_up:
                min_up = tmp_min_up
    
    max_down = -1.0
    for c in centers:
        tmp_max_down = diam(c)
        if tmp_max_down > max_down:
            max_down = tmp_max_down
    return min_up / max_down

def R_ij(data, centers, y_labels, cls1, cls2):
    S_cls1 = 0.0
    count_cls1 = 0
    S_cls2 = 0.0
    count_cls2 = 0
    center_1 = None
    center_2 = None
    for i, d in enumerate(data):
        label = y_labels[i]
        if label == cls1:
            S_cls1 += np.sum((d - centers[i])**2)
            count_cls1 += 1
            center_1 = centers[i] if center_1 is None else center_1
        elif label == cls2:
            S_cls2 += np.sum((d - centers[i])**2)
            count_cls2 += 1
            center_2 = centers[i] if center_2 is None else center_2
    S_cls1 /= count_cls1
    S_cls2 /= count_cls2
    d = np.sum((center_1-center_2)**2)

    return (S_cls1 + S_cls2) / d

def R_i(data, centers, y_labels, cls1):
    up_bound = max(y_labels)
    res = -1.0
    for i in xrange(up_bound+1):
        if 0==y_labels.tolist().count(i) or i==cls1:
            continue
        tmp_res = R_ij(data, centers, y_labels, cls1, i)
        if tmp_res > res:
            res = tmp_res
    return res

def davies_bouldin(data, y_labels):
    '''
        calculate davies_bouldin of clustering results, only support vector type

        @data: np.array, shape: [n_samples, n_features]
        @y_labels: np.array, shape: [n_samples, 1]

        #return: davies_bouldin
    '''
    centers = calculate_centers(data, y_labels)
    M = len(set(y_labels)) - (1 if -1 in y_labels else 0) 
    res = 0.0
    for i in xrange(max(y_labels)+1):
        if y_labels.tolist().count(i)==0:
            continue
        res += R_i(data, centers, y_labels, i)
    return res/M

def bic(data, y_labels):
    '''
        calculate bic of clustering results, only support vector type

        @data: np.array, shape: [n_samples, n_features]
        @y_labels: np.array, shape: [n_samples, 1]

        #return: bic
    '''
    label_set = set(y_labels)
    dim = len(data[0])
    n = float(len(data))
    m = len(label_set) - (1 if -1 in y_labels else 0)
    bic = 0.0
    centers = calculate_centers(data, y_labels)

    sigma_list = np.array([ 0.0 for i in xrange(max(label_set)+1) ])
    for i, d in enumerate(data):
        if y_labels[i]==-1:
            continue
        cls_index = y_labels[i]
        sigma_list[cls_index] += np.sum((d - centers[i])**2)


    for l in label_set:
        if l == -1:
            continue
        n_l = float(y_labels.tolist().count(l))
        t = n_l*np.log2(n_l/n)-(n_l*dim/2.0)*np.log2(2.0*np.pi)-(n_l/2.0)*np.log2(sigma_list[l]/(n_l-m))-(n_l-m)/2.0
        bic += t
    bic -= (m*np.log2(n))/2
    print bic
    return bic


